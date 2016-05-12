#!/usr/bin/env python

from collections import defaultdict
from . import examples as _examples
from giant.giant_base import filters as base_filters
import random
import string

swagger = None

_swagger_to_objc_map = {
    'string': defaultdict(lambda: 'NSString *',
        {
            'guid': 'NSString *',
            'date': 'NSDate *',
            'date-time': 'NSDate *',
            'byte': 'NSData *',
            'binary': 'NSData *',
            'password': 'NSString *'
        }
    ),
    'integer': defaultdict(lambda: 'NSNumber *',
        {
            'int32': 'NSNumber *',
            'int64': 'NSNumber *'
        }
    ),
    'number': defaultdict(lambda: 'NSNumber *',
        {
            'float': 'NSNumber *',
            'double': 'NSNumber *'
        }
    ),
    'boolean': defaultdict(lambda: 'NSNumber *'),
    'array': defaultdict(lambda: 'NSArray *'),
    'object': defaultdict(lambda: 'NSDictionary *'),
}

_swagger_to_xcdatamodel_map = {
    'string': defaultdict(lambda: 'String',
        {
            'guid': 'String',
            'date': 'Date',
            'date-time': 'Date',
            'byte': 'Binary',
            'binary': 'Binary',
            'password': 'String'
        }
    ),
    'integer': defaultdict(lambda: 'Integer 32',
        {
            'int32': 'Integer 32',
            'int64': 'Integer 64'
        }
    ),
    'number': defaultdict(lambda: 'Double',
        {
            'float': 'Float',
            'double': 'Double'
        }
    ),
    'boolean': defaultdict(lambda: 'Boolean'),
}

_swagger_to_objc_access_semantics_map = {
    'string': defaultdict(lambda: 'copy',
        {
            'guid': 'copy',
            'date': 'strong',
            'date-time': 'strong',
            'byte': 'copy',
            'binary': 'copy',
            'password': 'copy'
        }
    ),
    'integer': defaultdict(lambda: 'strong',
        {
            'int32': 'strong',
            'int64': 'strong'
        }
    ),
    'number': defaultdict(lambda: 'strong',
        {
            'float': 'strong',
            'double': 'strong'
        }
    ),
    'boolean': defaultdict(lambda: 'strong'),
    'array': defaultdict(lambda: 'copy'),
    'object': defaultdict(lambda: 'copy'),
}

def _get_property(prop):
    if '$ref' in prop:
        return swagger['definitions'][prop['$ref'].split('/')[-1]]
    return prop
    
def _get_parameter(param):
    if '$ref' in param:
        return swagger['parameters'][param['$ref'].split('/')[-1]]
    return param
    
def _get_schema(schema):
    if '$ref' in schema:
        return swagger['definitions'][schema['$ref'].split('/')[-1]]
    return schema
    
def _ios_attribute_optional(definition, property_name):
    if 'required' not in definition:
        return False
    return property_name in definition['required']
    
def _property_type(prop):
    prop = _get_property(prop)
    return _swagger_to_objc_map[prop['type']][prop.get('format')]
    
def _parameter_type(param):
        param = _get_parameter(param)
        if param['in'] == 'body':
            return _definition_type(param['schema'])
        return _swagger_to_objc_map[param['type']][param.get('format')]
    
def _ios_datamodel_attribute_type(prop):
    return _swagger_to_xcdatamodel_map[prop['type']][prop.get('format')]
    
def _template_string_in_af_format(string_value):
    import re
    return re.subn('\{([^}]+)\}', ':\\1', string_value)[0]
    
def _parameters_in(operation, in_types):
    results = []
    if 'parameters' not in operation:
        return []
    for param in operation['parameters']:
        param = _get_parameter(param)
        if param['in'] == in_types or param['in'] in in_types:
            results.append(param)
    return results
    
def _example_parameter(param):
    param = _get_parameter(param)
    if param['in'] == 'body':
        return _example_definition(param['schema'])
    return _example_primitive(param)
    
def _definition_type(schema):
    schema = _get_schema(schema)
    if 'type' not in schema or schema['type'] == 'object':
        return '{}Model *'.format(schema['name'])
    elif schema['type'] == 'array':
        return 'NSArray<{}> *'.format(_definition_type(schema['items']))
    else:
        return _property_type(schema)
        
def _example_definition(schema):
    schema = _get_schema(schema)
    if 'type' not in schema or schema['type'] == 'object':
        return '[{}Model new]'.format(schema['name'])
    elif schema['type'] == 'array':
        return '@[{}]'.format(_example_definition(schema['items']))
    else:
        return _example_primitive(schema)
        
def _example_primitive(schema):
    # if 'enum' in schema:
    #     return _examples.swagger_to_objc_enum_example_map[schema['type']][schema.get('format')](schema['enum'])
    return _examples.swagger_to_objc_example_map[schema['type']][schema.get('format')](schema)
    
def _example_primitive_string(schema):
    return _examples.swagger_to_objc_example_string_map[schema['type']][schema.get('format')](schema)
    
def _response_type(operation):
    for response_code, response in operation['responses'].iteritems():
        if response_code >= 200 and response_code < 300 and 'schema' in response:
            return _definition_type(response['schema'])
    return ''
            
def _objc_method_signature(operation):
    param_signature = '{param_name}:({param_type}){param_name_lower}'
    op_name = operation['operationId']
    parameters = []
    if 'parameters' in operation:
        base_signature = '+(void){op_name}With{parameters} onSuccess:(void(^)({response_type}))onSuccess onFailure:(void(^)(NSError*))onFailure'
        first = True
        for param in operation['parameters']:
            param = _get_parameter(param)
            param_name_lower = base_filters.camel_case(param['name'])
            if first:
                param_name = base_filters.pascal_case(param['name'])
                first = False
            else:
                param_name = param_name_lower
            parameters.append(param_signature.format(
                    param_name=param_name, 
                    param_type=_parameter_type(param),
                    param_name_lower=param_name_lower, 
                )
            )
    else:
        base_signature = '+(void){op_name}OnSuccess:(void(^)({response_type}))onSuccess onFailure:(void(^)(NSError*))onFailure'
    return base_signature.format(
        op_name=operation['operationId'],
        parameters=' '.join(parameters),
        response_type=_response_type(operation)
    )
    
def _example_call(operation, success_block, failure_block):
    response_type = _response_type(operation)
    if response_type != '':
        response_type = response_type + ' response'
    
    parameters = []
    if 'parameters' in operation:
        success_line = ' onSuccess:^({}){}'.format(response_type, success_block)
        first = True
        param_signature = '{param_name}:{param_example}'
        for param in operation['parameters']:
            param = _get_parameter(param)
            param_name_lower = base_filters.camel_case(param['name'])
            if first:
                param_name = 'With' + base_filters.pascal_case(param['name'])
                first = False
            else:
                param_name = param_name_lower
            parameters.append(param_signature.format(
                    param_name=param_name, 
                    param_example=_example_parameter(param)
                )
            )
    else:
        success_line = 'OnSuccess:^({}){}'.format(response_type, success_block)
    
    template = (
        '[Api '
            '{operation_name}{parameters}{success_line}'
            'onFailure:^(NSError* error){failure_block}'
        '];').format(
            operation_name=operation['operationId'],
            parameters=' '.join(parameters),
            success_line=success_line,
            failure_block=failure_block
        )
    return template
    
def _generate_pbxproj_id():
    return ''.join(random.choice(string.hexdigits) for _ in xrange(24)).upper()
    
_build_phase_file_ids = {}
def _build_phase_file_id(definition_name):
    if definition_name not in _build_phase_file_ids:
        _build_phase_file_ids[definition_name] = _generate_pbxproj_id()
    return _build_phase_file_ids[definition_name]
    
_file_ref_ids = {}
def _file_ref_id(definition_name):
    if definition_name not in _file_ref_ids:
        _file_ref_ids[definition_name] = _generate_pbxproj_id()
    return _file_ref_ids[definition_name]
    
def _objc_varname(variable_name):
    illegal_prefix = lambda value: any(value.startswith(v) for v in ('new',))
    illegal_value = lambda value: any(v == value for v in ('description',))
    if illegal_value(variable_name) or illegal_prefix(variable_name):
        return 'the' + variable_name[0].upper() + variable_name[1:]
    return variable_name
    
def _type_to_string(param):
    if param['in'] == 'body':
        schema = _get_schema(param['schema'])
    else:
        schema = param
    return _examples.swagger_to_objc_string_map[schema['type']][schema.get('format')](schema, param['name'])
        
def _objc_property(param):
    param = _get_parameter(param)
    property_template = '@property (nonatomic, {param_access_semantics}) {param_type} {param_name};'
    if param['in'] == 'body':
        param_access_semantics = 'strong'
        param_type = _definition_type(param['schema'])
    else:
        param_access_semantics = _swagger_to_objc_access_semantics_map[param['type']][param.get('format')]
        param_type = _parameter_type(param)
    param_name = base_filters.camel_case(param['name'])
    return property_template.format(
        param_access_semantics=param_access_semantics, 
        param_type=param_type, 
        param_name=param_name)

filters = (('ios_attribute_optional', _ios_attribute_optional),
    ('ios_datamodel_attribute_type', _ios_datamodel_attribute_type),
    ('property_type', _property_type),
    ('template_string_in_af_format', _template_string_in_af_format),
    ('parameters_in', _parameters_in),
    ('example_primitive', _example_primitive),
    ('example_primitive_string', _example_primitive_string),
    ('response_type', _response_type),
    ('objc_method_signature', _objc_method_signature),
    ('example_call', _example_call),
    ('build_phase_file_id', _build_phase_file_id),
    ('file_ref_id', _file_ref_id),
    ('objc_varname', _objc_varname),
    ('type_to_string', _type_to_string),
    ('objc_property', _objc_property),
    ('parameter_type', _parameter_type),
    ('example_parameter', _example_parameter))
    
    
    
    