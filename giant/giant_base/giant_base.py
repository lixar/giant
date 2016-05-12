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
            if os.path.split(template)[-1] == '.DS_Store':
                continue
            if template.endswith('.jinja'):
                self._populate_template(template)
            else:
                import shutil
                output_path = os.path.join(self.output_dir, template)
                try:
                    os.makedirs(os.path.split(output_path)[0])
                except:
                    pass
                shutil.copyfile(
                    os.path.join(self._main_loader.searchpath[0], template),
                    output_path)
    
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
            for method_name, method in filter(lambda item: item[0] in ['get', 'put', 'post', 'delete', 'options', 'head', 'patch'], path.items()):
                try:
                    operations[method['operationId']] = dict(method.items() + {
                        'method': method_name,
                        'path_name': path_name,
                        'path': path
                    }.items())
                    operation = operations[method['operationId']]
                    
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
                except StandardError as e:
                    import pdb; pdb.set_trace()
                    print(e)
        for definition_name, definition in self.swagger['definitions'].iteritems():
            definition['name'] = definition_name
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