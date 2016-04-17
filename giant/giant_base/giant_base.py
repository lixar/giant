#!/usr/bin/env python

import jinja2
import os
import StringIO
from yapsy.IPlugin import IPlugin
from datetime import datetime

_start_of_file_token = '<<<SOF:'

class GiantError(StandardError):
    
    def __init__(self, msg):
        super(GiantError, self).__init__(msg)
        

class BaseGiant(IPlugin):
        
    def setup(self, swagger, output_dir):
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
        
    def generate(self):
        print('Generating. ' + str(self._main_loader.list_templates()))
        try:
            os.mkdir(self.output_dir)
        except:
            pass
        for template in self._main_loader.list_templates():
            if template.endswith('.jinja'):
                self._populate_template(template)
            else:
                import shutil
                shutil.copyfile(
                    os.path.join(self._main_loader.searchpath[0], template),
                    os.path.join(self.output_dir, template))
    
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
        for path_name, path in self.swagger['paths'].iteritems():
            for method_name, method in path.items():
                try:
                    operations[method['operationId']] = dict(method.items() + {
                        'method': method_name,
                        'path_name': path_name,
                        'path': path
                    }.items())
                    if 'parameters' not in operations[method['operationId']]:
                        operations[method['operationId']]['parameters'] = path['parameters']
                    else:
                        operations[method['operationId']]['parameters'].extend(path['parameters'])
                except:
                    pass
        template_variables = {
            'swagger': self.swagger,
            'operations': operations,
            'current_datetime': datetime.utcnow()}
        template_variables.update(self.custom_variables())
        results = template.render(**template_variables).split(_start_of_file_token)
        if len(results) == 1: # no _start_of_file_token in file.
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
            try:
                if file_type != 'noext':
                    filename = filename + '.' + file_type
                with open(os.path.join(output_dir, filename), 'w') as out:
                    out.write(data.encode('utf-8'))
            except StandardError as e:
                import pdb; pdb.set_trace()
        
class BaseGiantClient(BaseGiant):
    pass
    
class BaseGiantServer(BaseGiant):
    pass