#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jinja2
import os
import filecmp
import StringIO
import tempfile
from yapsy.IPlugin import IPlugin
from datetime import datetime
from collections import defaultdict
import logging
import json

_start_of_file_token = '<<<SOF:'

def _safe_create_dir(directory):
    try:
        os.mkdir(directory)
    except:
        pass
    
def _safe_create_dirs(directory_path):
    try:
        os.makedirs(directory_path)
    except:
        pass
        
        
class GiantError(StandardError):
    
    def __init__(self, msg):
        super(GiantError, self).__init__(msg)
        
class GenerationTracker(object):
    
    def __init__(self, project_name, force_overwrite):
        self.project_name = project_name
        self._log_directory = os.path.join(os.getcwd(), '.giant')
        self._log_file_path = os.path.join(self._log_directory, project_name+'.gen')
        self._setup_log_dicts()
        self._force_overwrite = force_overwrite
        
    def check_skip_write_file(self, file_path, real_file_path, generated_template_data):
        if (os.path.exists(file_path) and real_file_path in self._previous_generation_log
        and int(os.stat(file_path).st_mtime) != self._previous_generation_log.get(real_file_path)):
            if self._previous_generation_log.get(real_file_path) == -1:
                self._file_generation_log[real_file_path] = -1
                return True # Always skip
            if self._force_overwrite != None:
                if not self._force_overwrite:
                    self._file_generation_log[real_file_path] = self._previous_generation_log.get(real_file_path)
                return not self._force_overwrite
            diff = self._create_diff(real_file_path, generated_template_data)
            if diff != '':
                return self._prompt_skip_file(real_file_path, generated_template_data, diff)
        return False
            
    def log_file_generated(self, file_path):
        self._file_generation_log[file_path] = int(os.stat(file_path).st_mtime)
        
    def write_log(self):
        with open(self._log_file_path, 'w') as f:
            json.dump(self._file_generation_log, f, sort_keys=True, indent=4, separators=(',', ': '))
        
    def _setup_log_dicts(self):
        try:
            os.mkdir(self._log_directory)
        except:
            pass
        self._file_generation_log = {}
        try:
            with open(self._log_file_path, 'r') as f:
                self._previous_generation_log = json.load(f)
        except:
            self._previous_generation_log = {}

    def _prompt_skip_file(self, real_file_path, generated_template_data, diff):
        logging.warning('It appears you have edited the following file.\n{}\n'.format(real_file_path))
        overwrite = ''
        while overwrite.lower() not in ('y', 'n'):
            while overwrite.lower() not in ('y', 'n', 'd', 'a'):
                overwrite = raw_input('Do you wish to overwrite it. (y)es, (N)o, (a)lways No, (d)iff, ? ')
                if overwrite == '':
                    overwrite = 'N'
            if overwrite.lower() == 'n':
                self._file_generation_log[real_file_path] = self._previous_generation_log.get(real_file_path)
                return True # Skip the file.
            if overwrite.lower() == 'a':
                self._file_generation_log[real_file_path] = -1
                return True # Skip the file.
            if overwrite.lower() == 'd':
                print(diff)
                overwrite = ''
        return False # Don't skip the file.

    def _create_diff(self, real_file_path, generated_template_data):
        import difflib
        string_list = generated_template_data.splitlines(True)
        with open(real_file_path, 'r') as existing_file:
            existing_lines = [unicode(line, 'utf-8') for line in existing_file.readlines()]
        diff = difflib.unified_diff(existing_lines, string_list)
        value = u''.join(diff)
        return value
    

class BaseGiant(IPlugin):
        
    def setup(self, swagger, output_dir, force_overwrite=None):
        self.swagger = swagger
        self.output_dir = output_dir
        self.environment = jinja2.Environment(loader=self._get_loaders())
        self.customize_env(self.environment)
        self.environment.add_extension('jinja2.ext.do')
        self.environment.add_extension('jinja2.ext.loopcontrols')
        self.environment.filters.update(self.filters() or {})
        self.environment.filters.update(self._get_default_filters())
        self.environment.tests.update(self.tests() or {})
        self.environment.tests.update(self._get_default_tests())
        self.generation_tracking = GenerationTracker(self.swagger['info']['title'], force_overwrite)
        
    def generate(self):
        print('Generating. ' + str(self._main_loader.list_templates()))
        
        _safe_create_dir(self.output_dir)
            
        for template in self._main_loader.list_templates():
            if os.path.split(template)[-1] == '.DS_Store': 
                continue # Skip .DS_Store files.
            if template.endswith('.jinja'):
                # Generate the template
                self._populate_template(template)
            else:
                # If it doesn't end with '.jinja' we do a straight copy of the file.
                import shutil
                output_path = os.path.join(self.output_dir, template)
                _safe_create_dirs(os.path.split(output_path)[0])
                shutil.copyfile(os.path.join(self._main_loader.searchpath[0], template), output_path)
                    
        # Write the generation report.
        self.generation_tracking.write_log()
    
    def _get_loaders(self):
        common_loader = jinja2.PackageLoader('giant.giant_base', 'common')
        self._main_loader = self.loader()
        helpers_loader = self.helpers_loader()
        loader = jinja2.ChoiceLoader([
            common_loader,
            self._main_loader,
            helpers_loader
        ])
        return loader
        
    def custom_variables(self):
        return {}
        
    def _get_default_filters(self):
        from . import filters
        filters.swagger = self.swagger
        return filters.filters
        
    def _get_default_tests(self):
        return (('equalto', lambda value, other : value == other),
               ('in', lambda value, other : value in other))
    
    def _populate_template(self, template_name):
        template = self.environment.get_template(template_name)
        file_type = template_name.split('.')[-2]
        operations = {}
        controllers = defaultdict(lambda: [])
        for path_name, path in self.swagger['paths'].iteritems():
            if 'x-swagger-router-controller' in path:
                operation_controller = controllers[path['x-swagger-router-controller']]
            for method_name, method in filter(lambda item: item[0] in ['get', 'put', 'post', 'delete', 'options', 'head', 'patch'], path.items()):
                operations[method['operationId']] = dict(method.items() + {
                    'method': method_name,
                    'path_name': path_name,
                    'path': path
                }.items())
                if 'x-swagger-router-controller' in method:
                    operation_controller = controllers[method['x-swagger-router-controller']]
                elif operation_controller == None:
                    operation_controller = controllers['AppService']
                operation = operations[method['operationId']]
                operation_controller.append(operation)
                operation['controller'] = operation_controller
                
                if 'parameters' in operation and 'parameters' in path:
                    operation['parameters'].extend(path['parameters'])
                elif 'parameters' in path:
                    operation['parameters'] = path['parameters']
                elif 'parameters' not in operation:
                    operation['parameters'] = []
                    
                if 'consumes' not in operation:
                    operation['consumes'] = self.swagger.get('consumes')
                if 'produces' not in operation:
                    operation['produces'] = self.swagger.get('produces')
                if 'security' not in operation:
                    if 'security' not in self.swagger:
                        operation['security'] = []
                    else:
                        operation['security'] = self.swagger.get('security')
                        
                for index, param in enumerate(operation['parameters']):
                    if '$ref' in param:
                        operation['parameters'][index] = self.swagger['parameters'][param['$ref'].split('/')[-1]]
                    
        for definition_name, definition in self.swagger['definitions'].iteritems():
            definition['name'] = definition_name
            if ('type' not in definition or definition['type'] == 'object') and 'properties' in definition:
                for prop_name, prop in definition['properties'].iteritems():
                    prop['definition'] = definition
                
        template_variables = {
            'swagger': self.swagger,
            'operations': operations,
            'controllers': controllers,
            'current_datetime': datetime.utcnow()}
        template_variables.update(self.custom_variables())
        results = template.render(**template_variables).split(_start_of_file_token)
        
        with open(os.path.join(self._main_loader.searchpath[0], template.name), 'r') as template_source:
            content = template_source.read()
            multi_file =  'start_of_file' in content
                
        if not multi_file:
            # if len(results) == 1: # no _start_of_file_token in file.
            output_pairs = [('.'.join(template_name.split('.')[:-2]), results[0])]
        else:
            file_results = (StringIO.StringIO(result) for result in results)
            output_pairs = ((file_result.readline().strip(), ''.join(file_result.readlines())) for file_result in file_results)
        
        for filename, data in output_pairs:
            if filename == None or len(filename) == 0:
                continue
            output_dir = self.output_dir
            try:
                path, filename = os.path.split(filename)
                output_dir = os.path.join(self.output_dir, path)
                os.makedirs(output_dir)
            except StandardError:
                pass
                
            if file_type != 'noext':
                filename = filename + '.' + file_type
            file_path = os.path.join(output_dir, filename)
            
            real_file_path = os.path.realpath(file_path)
            
            # Check if we should skip this file.
            if self.generation_tracking.check_skip_write_file(file_path, real_file_path, data):
                continue # Skip it.
            
            # Write the file.
            with open(file_path, 'w') as out:
                out.write(data.encode('utf-8'))
                
            # Log that we've written a new file.
            self.generation_tracking.log_file_generated(real_file_path)
        
        
class BaseGiantClient(BaseGiant):
    pass
    
    
class BaseGiantServer(BaseGiant):
    pass