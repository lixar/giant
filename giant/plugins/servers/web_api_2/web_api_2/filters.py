#!/usr/bin/env python

from collections import defaultdict
from giant.giant_base import filters as base_filters
import random
from . import examples as _examples

_swagger_to_csharp_map = {
    'string': defaultdict(lambda: 'string',
        {
            'guid': 'Guid',
            'date': 'DateTime',
            'date-time': 'DateTime',
            'byte': 'byte[]',
            'binary': 'byte[]',
            'password': 'string'
        }
    ),
    'integer': defaultdict(lambda: 'int',
        {
            'int32': 'long',
            'int64': 'long'
        }
    ),
    'number': defaultdict(lambda: 'double',
        {
            'float': 'float',
            'double': 'double'
        }
    ),
    'boolean': defaultdict(lambda: 'bool'),
}

def _property_type(prop):
    return _swagger_to_csharp_map[prop['type']][prop.get('format')]

def _resolve_type(schema):
    if '$ref' in schema:
        return schema['$ref'].split('/')[-1]
    if schema['type'] == 'array':
        return 'IEnumerable<' + _resolve_type(schema['items']) + '>'
    if schema['type'] == 'object':
        #! TODO: Make this parse stuff correctly.
        return 'Dictionary<String, Object>'
    return _swagger_to_csharp_map(schema['type'])
    
def _resolve_example_type(prop):
    if '$ref' in prop:
        return prop['$ref'].split('/')[-1]
    if prop['type'] == 'array':
        return 'new List<' + _resolve_type(prop['items']) + '>();'
    if prop['type'] == 'object':
        #! TODO: Make this parse stuff correctly.
        return 'new Dictionary<String, Object>();'
    return _swagger_to_csharp_map(prop['type'])

def _success_response(operation):
    success_lambda = lambda codeResponse: codeResponse[0] >= 200 and codeResponse[0] < 300
    responses = filter(success_lambda, operation['responses'].iteritems())
    if len(responses) < 1:
        return None
    if len(responses) > 1:
        print('Uh oh... multiple success conditions.')
    return responses[0][1]

def _return_type(operation):
    response = _success_response(operation)
    try:
        return _resolve_type(response['schema'])
    except StandardError as e:
        return 'void'
        
def _parameter_type(parameter):
    if '$ref' in parameter:
        parameter = swagger['parameters'][parameter['$ref'].split('/')[-1]]
    if parameter['in'] == 'body':
        return _resolve_type(parameter['schema'])
    return _swagger_to_csharp_map[parameter['type']][parameter.get('format')]
        
def _get_parameter(param):
    if '$ref' in param:
        return swagger['parameters'][param['$ref'].split('/')[-1]]
    return param
        
def _parameters(operation):
    all_params = []
    if 'parameters' not in operation:
        return all_params
    if 'consumes' in operation and 'application/x-www-form-urlencoded' in operation['consumes']:
        param_type = base_filters.camel_to_pascal(operation['operationId'] + 'Request')
        param_name = operation['operationId']
        all_params.append(param_type + ' ' + param_name)
    for param in operation['parameters']:
        param = _get_parameter(param)
        if param['in'] == 'formData':
            continue
        param_name = param['name']
        param_type = _parameter_type(param)
        all_params.append(param_type + ' ' + param_name)
    return all_params
    
def _body_paramerer(operation):
    body_param = base_filters.parameters_in(operation, 'body')
    if len(body_param) == 0:
        return ''
    return '[FromBody] ' + body_param[0]

def _example_primitive(schema):
    if 'enum' in schema:
        return _examples.swagger_to_csharp_enum_example_map[schema['type']][schema.get('format')](schema['enum'])
    return _examples.swagger_to_csharp_example_map[schema['type']][schema.get('format')](schema)

swagger = None
    
filters = (
    ('property_type', _property_type),
    ('return_type', _return_type),
    ('resolve_example_type', _resolve_example_type),
    ('parameter_type', _parameter_type),
    ('parameters', _parameters),
    ('body_paramerer', _body_paramerer),
    ('success_response', _success_response),
    ('example_primitive', _example_primitive),
)