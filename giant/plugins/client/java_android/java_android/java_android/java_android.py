#!/usr/bin/env python

import jinja2
from giant.giant_base import BaseGiantClient
import os

class SwaggerPirate(BaseGiantClient):

    def custom_variables(self):
        '''Additional variables to make available to your templates.'''
        return {
            'generated_citation': 'Plugin generated using giant-plugin!',
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
        environment.trim_blocks = True
        environment.lstrip_blocks = True
        '''Call to allow plugin customization of the Jinja2 environment.'''
        pass

    def filters(self):
        '''Call to allow plugin customization of available Jinja2 filters.'''
        from . import filters
        filters.swagger = self.swagger
        return filters.filters

    def tests(self):
        '''Call to allow plugin customization of available Jinja2 tests.'''
        pass
