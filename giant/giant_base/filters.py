#!/usr/bin/env python

from .casing import *

_start_of_file_token = '<<<SOF:'

swagger = None

def start_of_file(filename):
    return _start_of_file_token + filename + '\n'

def camel_to_pascal(value):
    if len(value) == 0:
        return value
    elif len(value) == 1:
        return value.upper()
    return value[0].upper() + value[1:]
    
def controller_name(operation):
    if 'x-swagger-router-controller' in operation:
        return operation['x-swagger-router-controller']
    if 'x-swagger-router-controller' in operation['path']:
        return operation['path']['x-swagger-router-controller']
    return 'giant'
    
def controllers(operations, controller):
    return dict(filter(lambda opTuple: controller_name(opTuple[1]) == controller, operations.iteritems()))
    
def unique(items):
    return list(set(items))

def operation_consumes(operation):
    return operation.get('consumes', swagger['consumes'])
    
def remove_trailing_slash(path):
    if path.endswith('/'):
        return path[:-1]
    return path
    
filters = (
    ('camel_to_pascal', camel_to_pascal),
    ('start_of_file', start_of_file),
    ('controller_name', controller_name),
    ('controllers', controllers),
    ('unique', unique),
    ('operation_consumes', operation_consumes),
    ('pascal_case', pascal_case),
    ('camel_case', camel_case),
    ('remove_trailing_slash', remove_trailing_slash),
)