#!/usr/bin/env python

import jinja2
from giant.giant_base import BaseGiantClient
from .project_variables import load_variables
import os

class SwaggerPirate(BaseGiantClient):

    def custom_variables(self):
        '''Additional variables to make available to your templates.'''
        variables = load_variables()
        return {
            'bundle_identifier': variables['bundle_id'],
        }

    def loader(self):
        '''Returns the Jinja2 template loader for your templates.'''
        path = os.path.dirname(os.path.realpath(__file__))
        return jinja2.FileSystemLoader(os.path.join(path, 'templates'))

    def helpers_loader(self):
        '''Returns the Jinja2 template loader for your template helpers.'''
        path = os.path.dirname(os.path.realpath(__file__))
        return jinja2.FileSystemLoader(os.path.join(path, 'template-res'))

    def customize_env(self, environment):
        '''Call to allow plugin customization of the Jinja2 environment.'''
        pass
        
    def filters(self):
        '''Call to allow plugin customization of available Jinja2 filters.'''
        from .filters import filters
        return filters
                
    def tests(self):
        '''Call to allow plugin customization of available Jinja2 tests.'''
        pass