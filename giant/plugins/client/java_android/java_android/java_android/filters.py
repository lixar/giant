#!/usr/bin/env python

from collections import defaultdict
from giant.giant_base import filters as base_filters
from giant.giant_base import casing as base_casing
import random
import string

swagger = None

_swagger_to_java_map = {
    'string': defaultdict(lambda: 'String',
        {
            'guid': 'String',
            'date': 'OffsetDateTime',
            'date-time': 'OffsetDateTime',
            'byte': 'String',
            'binary': 'String',
            'password': 'String'
        }
    ),
    'integer': defaultdict(lambda: 'Integer',
        {
            'int32': 'Integer',
            'int64': 'Long'
        }
    ),
    'number': defaultdict(lambda: 'Double',
        {
            'float': 'Float',
            'double': 'Double'
        }
    ),
    'boolean': defaultdict(lambda: 'Boolean'),
    # 'array': defaultdict(lambda: 'List'),
    # 'object': defaultdict(lambda: 'HashMap'),
}

_swagger_to_example_map = {
    'string': defaultdict(lambda: '"ExampleString"',
        {
            'guid': '"ExampleString"',
            'date': 'OffsetDateTime.now()',
            'date-time': 'OffsetDateTime.now()',
            'byte': '"ExampleString"',
            'binary': '"ExampleString"',
            'password': '"ExampleString"'
        }
    ),
    'integer': defaultdict(lambda: 'new Integer({})'.format(random.randint(0, 10)),
        {
            'int32': 'new Integer({})'.format(random.randint(0, 10)),
            'int64': 'new Long({})'.format(random.randint(0, 10))
        }
    ),
    'number': defaultdict(lambda: 'new Double({})'.format(random.random() * 10),
        {
            'float': 'new Float({})'.format(random.random() * 10),
            'double': 'new Double({})'.format(random.random() * 10)
        }
    ),
    'boolean': defaultdict(lambda: 'new Boolean({})'.format(random.choice(['true', 'false']))),
    # 'array': defaultdict(lambda: 'List'),
    # 'object': defaultdict(lambda: 'HashMap'),
}

def _android_path_params(params):
    path_template = '@Path("{param_name}") {param_type} {param_name}'
    param_string = []
    for param in params:
        param_string.append(path_template.format(
            param_name=param['name'],
            param_type=_swagger_to_java_map[param['type']][param.get('format')]
        ))
    return param_string

def _android_query_params(params):
    path_template = '@Query("{param_name}") {param_type} {param_name}'
    param_string = []
    for param in params:
        if param['type'] == 'array':
            param_type = 'List<{item_type}>'.format(
                item_type=_swagger_to_java_map[param['items']['type']][param['items'].get('format')]
            )
        else:
            param_type = _swagger_to_java_map[param['type']][param.get('format')]
        param_string.append(path_template.format(
            param_name=param['name'],
            param_type=param_type
        ))
    return param_string

def _android_body_params(params):
    path_template = '@Body {param_type} {param_name}'
    param_string = []
    for param in params:
        param_string.append(path_template.format(
            param_name=param['name'],
            param_type=param['schema']['$ref'].split('/')[-1]
        ))
    return param_string

def _android_form_params(params):
    path_template = '@Field("{param_name}") {param_type} {param_name}'
    param_string = []
    for param in params:
        param_string.append(path_template.format(
            param_name=param['name'],
            param_type=_swagger_to_java_map[param['type']][param.get('format')]
        ))
    return param_string

def _android_multipart_params(params):
    path_template = '@Part("{param_name}") {param_type} {param_name}'
    param_string = []
    for param in params:
        param_string.append(path_template.format(
            param_name=param['name'],
            param_type=_swagger_to_java_map[param['type']][param.get('format')]
        ))
    return param_string

def _android_header_params(params):
    # @Header("Authorization") String authorization
    path_template = '@Header("{param_name}") {param_type} {var_param_name}'
    param_string = []
    for param in params:
        param_string.append(path_template.format(
            param_name=param['name'],
            param_type=_swagger_to_java_map[param['type']][param.get('format')],
            var_param_name=base_filters.camel_case(param['name'])
        ))
    return param_string

def _android_response_type(operation):
    for response_code, response in operation['responses'].iteritems():
        if response_code >= 200 and response_code < 300 and 'schema' in response:
            response_definition = response['schema']['$ref'].split('/')[-1]
            if (swagger['definitions'][response_definition]['type'] == 'array'):
                return 'List<{response_type}>'.format(
                    response_type = swagger['definitions'][response_definition]['items']['$ref'].split('/')[-1]
                )
            else:
                return response_definition
    return 'Void'

def _android_param_type(param):
    if param['in'] == 'body':
        return param['schema']['$ref'].split('/')[-1]
    if param['type'] == 'array':
        return 'List<{item_type}>'.format(
            item_type=_swagger_to_java_map[param['items']['type']][param['items'].get('format')]
        )
    return _swagger_to_java_map[param['type']][param.get('format')]

def _android_example_value(param):
    if param['in'] == 'body':
        return 'new {}()'.format(param['schema']['$ref'].split('/')[-1])
    if param['type'] == 'array':
        return 'new List<{item_type}>()'.format(
            item_type=_swagger_to_java_map[param['items']['type']][param['items'].get('format')]
        )
    return _swagger_to_example_map[param['type']][param.get('format')]

def _android_property_type(param):
    if '$ref' in param:
        return param['$ref'].split('/')[-1]
    if param['type'] == 'array':
        return 'List<{item_type}>'.format(
            item_type=_android_property_type(param['items'])
        )
    if param['type'] == 'object':
        import pdb; pdb.set_trace()
        print(param)
    return _swagger_to_java_map[param['type']][param.get('format')]
def _android_enum_value_name_map(param):
    if 'description' in param:
        original_enum_descriptions = param['description'].split(',')
        transformed_enum_descriptions = []
        for enum_description in original_enum_descriptions:
            transformed_enum_descriptions.append(base_casing.all_upper_case(enum_description.split('-')[1]))

        dictionary = dict(zip(param['enum'], transformed_enum_descriptions))
    return dictionary
def _android_enum_exist(param):
    if 'enum' in param:
        return True
    return False
def _android_ref_exist(param):
    if '$ref' in param:
        return True
    return False
def _android_should_persist(param):
    if 'x-persist' in param:
        return param['x-persist']
    return False
filters = (
    ('android_path_params', _android_path_params),
    ('android_query_params', _android_query_params),
    ('android_body_params', _android_body_params),
    ('android_form_params', _android_form_params),
    ('android_multipart_params', _android_multipart_params),
    ('android_header_params', _android_header_params),
    ('android_response_type', _android_response_type),
    ('android_param_type', _android_param_type),
    ('android_example_value', _android_example_value),
    ('android_property_type', _android_property_type),
    ('android_enum_value_name_map', _android_enum_value_name_map),
    ('android_enum_exist', _android_enum_exist),
    ('android_should_persist', _android_should_persist),
    ('android_ref_exist', _android_ref_exist)
)
