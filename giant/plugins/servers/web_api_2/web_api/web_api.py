#!/usr/bin/env python

from .filters import *
from .project_variables import load_variables
import jinja2
from giant.giant_base.giant_base import BaseGiantServer
import os

class SwaggerGiant(BaseGiantServer):
    
    def custom_variables(self):
        variables = load_variables()
        return {
            'project_guid': variables['project'],
            'assembly_guid': variables['assembly']
        }
    
    def customize_env(self, environment):
        environment.trim_blocks = True
        environment.lstrip_blocks = True
    
    def loader(self):
        # return jinja2.PackageLoader('sagiant_ios', 'templates')
        path = os.path.dirname(os.path.realpath(__file__))
        return jinja2.FileSystemLoader(os.path.join(path, 'templates'))
    
    def helpers_loader(self):
        # return jinja2.PackageLoader('sagiant_ios', 'template-res')
        path = os.path.dirname(os.path.realpath(__file__))
        return jinja2.FileSystemLoader(os.path.join(path, 'template-res'))
    
    def filters(self):
        from . import filters
        filters.swagger = self.swagger
        return filters.filters
                
    def tests(self):
        return (('equalto', lambda value, other : value == other),
               ('in', lambda value, other : value in other))
        