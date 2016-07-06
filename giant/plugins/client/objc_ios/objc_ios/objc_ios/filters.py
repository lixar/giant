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
    'array': defaultdict(lambda: 'NSArray<{object_type}*> *'),
    'object': defaultdict(lambda: 'NSDictionary *'),
}

_swagger_to_realm_map = {
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
    'integer': defaultdict(lambda: 'NSNumber<RLMInt> *',
        {
            'int32': 'NSNumber<RLMInt> *',
            'int64': 'NSNumber<RLMInt> *'
        }
    ),
    'number': defaultdict(lambda: 'NSNumber<RLMDouble> *',
        {
            'float': 'NSNumber<RLMFloat> *',
            'double': 'NSNumber<RLMDouble> *'
        }
    ),
    'boolean': defaultdict(lambda: 'NSNumber<RLMBool> *'),
    'array': defaultdict(lambda: 'RLMArray<{object_type}*><{object_type}> *'),
}

_swagger_to_realm_wrapper_map = {
    'string': defaultdict(lambda: 'RealmString *',
        {
            'guid': 'RealmString *',
            'date': 'RealmDate *',
            'date-time': 'RealmDate *',
            'byte': 'RealmData *',
            'binary': 'RealmData *',
            'password': 'RealmString *'
        }
    ),
    'integer': defaultdict(lambda: 'RealmNumber *',
        {
            'int32': 'RealmNumber *',
            'int64': 'RealmNumber *'
        }
    ),
    'number': defaultdict(lambda: 'RealmNumber *',
        {
            'float': 'RealmNumber *',
            'double': 'RealmNumber *'
        }
    ),
    'boolean': defaultdict(lambda: 'RealmNumber *'),
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
    
def _realm_property_type(prop, prefix):
    prop = _get_property(prop)
    if prop['type'] == 'object':
        return prefix + prop['name'] + ' *'
    value = _swagger_to_realm_map[prop['type']][prop.get('format')]
    if prop['type'] == 'array':
        if '$ref' in prop['items']:
            return value.format(object_type=prefix + prop['items']['$ref'].split('/')[-1])
        items_prop = _get_property(prop['items'])
        if 'type' not in items_prop or (items_prop['type'] != 'object' and items_prop['type'] != 'array'):
            items_type = _swagger_to_realm_wrapper_map[items_prop['type']][items_prop.get('format')][:-2]
            return value.format(object_type=prefix + items_type)
        else:
            return value.format(object_type=prefix + _swagger_to_objc_map[prop['items']['type']][prop['items'].get('format')])
    return value
    
def _property_array_items_type(items, prefix):
    if '$ref' in items:
        return prefix + items['$ref'].split('/')[-1]
    items_prop = _get_property(items)
    if 'type' not in items_prop or (items_prop['type'] != 'object' and items_prop['type'] != 'array'):
        items_type = _property_type(items_prop, prefix)
        return items_type[:-2]
    else:
        return prefix + _swagger_to_objc_map[items['type']][items.get('format')]
    
def _property_type(prop, prefix, do_persist=False):
    if do_persist or ('definition' in prop and 'x-persist' in prop['definition'] and prop['definition']['x-persist']):
        return _realm_property_type(prop, prefix)
    prop = _get_property(prop)
    value = _swagger_to_objc_map[prop['type']][prop.get('format')]
    if prop['type'] == 'array':
        items_type = _property_array_items_type(prop['items'], prefix)
        return value.format(object_type=items_type)
    return value
    
def _parameter_type(param, prefix):
    param = _get_parameter(param)
    if param['in'] == 'body':
        return _definition_type(param['schema'], prefix)
    return _property_type(param, prefix)
    
def _ios_datamodel_attribute_type(prop):
    prop = _get_property(prop)
    return _swagger_to_xcdatamodel_map[prop['type']][prop.get('format')]
    
def _template_string_in_af_format(string_value):
    import re
    return re.subn('\{([^}]+)\}', ':\\1', string_value)[0]
    
def _example_parameter(param, prefix):
    param = _get_parameter(param)
    if param['in'] == 'body':
        return _example_definition(param['schema'], prefix)
    return _example_primitive(param)
    
def _definition_type(schema, prefix):
    schema = _get_schema(schema)
    if 'type' not in schema or schema['type'] == 'object':
        return '{}{} *'.format(prefix, schema['name'])
    elif schema['type'] == 'array':
        return 'NSArray<{}> *'.format(_definition_type(schema['items'], prefix))
    else:
        return _property_type(schema, prefix)
        
def _array_definition_items_type(schema, prefix):
    schema = _get_schema(schema)
    if 'definition' in schema and 'x-persist' in schema['definition']:
        try:
            items = _get_schema(schema['items'])
            return prefix + _swagger_to_realm_wrapper_map[items['type']][items.get('format')]
        except StandardError as e:
            pass
    return _definition_type(schema['items'], prefix)
        
def _example_definition(schema, prefix):
    schema = _get_schema(schema)
    if 'type' not in schema or schema['type'] == 'object':
        if 'name' not in schema:
            # nameless schemas are dictionaries.
            model_template = '^{ NSMutableDictionary* model = [NSMutableDictionary dictionary]; '
            for prop_name, prop in schema['properties'].iteritems():
                prop_copy = dict(prop)
                prop['name'] = prop_name
                model_template = model_template + 'model[@"{prop_name}"] = {prop_example}; '.format(prop_name=prop_name, prop_example=_example_definition(prop, prefix))
        else:
            model_template = '^{{ {prefix}{schema_name}* model = [{prefix}{schema_name} new]; '.format(prefix=prefix, schema_name=schema['name'])
            for prop_name, prop in schema['properties'].iteritems():
                prop_copy = dict(prop)
                prop['name'] = prop_name
                model_template = model_template + 'model.{prop_name} = {prop_example}; '.format(prop_name=_objc_varname(base_filters.camel_case(prop_name)), prop_example=_example_definition(prop, prefix))
        model_template = model_template + 'return model; }()'
        return model_template
        # return '[{} new]'.format(schema['name'])
    elif schema['type'] == 'array':
        return '@[{}]'.format(_example_definition(schema['items'], prefix))
    else:
        return _example_primitive(schema)
        
def _example_primitive(schema):
    if 'enum' in schema:
        return _examples.swagger_to_objc_enum_example_map[schema['type']][schema.get('format')](schema['enum'])
    return _examples.swagger_to_objc_example_map[schema['type']][schema.get('format')](schema)
    
def _example_primitive_string(schema):
    return _examples.swagger_to_objc_example_string_map[schema['type']][schema.get('format')](schema)
    
def _response_schema(operation):
    if 'responses' not in operation:
        return None
    for response_code, response in operation['responses'].iteritems():
        if response_code >= 200 and response_code < 300 and 'schema' in response:
            return _get_schema(response['schema'])
    return None
    
def _response_type(operation, prefix):
    schema = _response_schema(operation)
    if schema == None:
        return ''
    return _definition_type(schema, prefix)
    
def _error_response_schema(operation):
    if 'responses' not in operation:
        return None
    if 'default' in operation['responses'].keys():
        return _get_schema(operation['responses']['default']['schema'])
    for response_code, response in operation['responses'].iteritems():
        if response_code < 200 or response_code >= 300 and 'schema' in response:
            return _get_schema(response['schema'])
    return None
    
def _error_response_type(operation, prefix):
    schema = _error_response_schema(operation)
    if schema == None:
        return ''
    return _definition_type(schema, prefix)
            
def _objc_method_signature(operation, prefix):
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
                    param_type=_parameter_type(param, prefix),
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
    
def _example_call(operation, success_block, failure_block, prefix):
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
                    param_example=_example_parameter(param, prefix)
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
    
def _type_to_string(param, variable_name):
    if variable_name == None:
        variable_name = param['name']
    if param['in'] == 'body':
        schema = _get_schema(param['schema'])
    else:
        schema = param
    return _examples.swagger_to_objc_string_map[schema['type']][schema.get('format')](schema, variable_name)
        
def _objc_property(param, prefix):
    param = _get_parameter(param)
    property_template = '@property (nonatomic, {param_access_semantics}) {param_type} {param_name};'
    if param['in'] == 'body':
        param_access_semantics = 'strong'
        param_type = _definition_type(param['schema'], prefix)
    else:
        param_access_semantics = _swagger_to_objc_access_semantics_map[param['type']][param.get('format')]
        param_type = _parameter_type(param, prefix)
    param_name = base_filters.camel_case(param['name'])
    return property_template.format(
        param_access_semantics=param_access_semantics, 
        param_type=param_type, 
        param_name=param_name)
        
def _model_base_type(definition):
    if 'x-persist' in definition:
        return 'RLMObject'
    else:
        return 'NSObject'
        
def _realm_property_import(prop, prefix):
    prop = _get_property(prop)
    if prop['type'] == 'array':
        prop = _get_property(prop['items'])
        if 'name' in prop:
            return '#import "{}{}.h"'.format(prefix, prop['name'])
    elif prop['type'] == 'object':
        return '#import "{}{}.h"'.format(prefix, prop['name'])
    return None
    
def _response_type_forward_decl(operation, prefix):
    for response_code, response in operation['responses'].iteritems():
        if response_code >= 200 and response_code < 300 and 'schema' in response:
            schema = _get_schema(response['schema'])
            if 'type' not in schema or schema['type'] == 'object':
                return '@class ' + prefix + schema['name'] + ';'
            elif schema['type'] == 'array' and '$ref' in schema['items']:
                return '@class ' + prefix + schema['items']['$ref'].split('/')[-1] + ';'
    return ''
    
def _error_response_type_forward_decl(operation, prefix):
    error_response = None
    if 'default' in operation['responses']:
        error_response = operation['responses']['default']
    for response_code, response in operation['responses'].iteritems():
        if response_code < 200 or response_code >= 300 and 'schema' in response:
            error_response = response
    if error_response != None:
        schema = _get_schema(error_response['schema'])
        if 'type' not in schema or schema['type'] == 'object':
            return '@class ' + prefix + schema['name'] + ';'
        elif schema['type'] == 'array' and '$ref' in schema['items']:
            return '@class ' + prefix + schema['items']['$ref'].split('/')[-1] + ';'
    return ''
    
def _response_type_import(operation, prefix):
    for response_code, response in operation['responses'].iteritems():
        if response_code >= 200 and response_code < 300 and 'schema' in response:
            schema = _get_schema(response['schema'])
            if 'type' not in schema or schema['type'] == 'object':
                return '#import "' + prefix + schema['name'] + '.h"'
            elif schema['type'] == 'array' and '$ref' in schema['items']:
                return '#import "' + prefix + schema['items']['$ref'].split('/')[-1] + '.h"'
    return ''
    
def _error_response_type_import(operation, prefix):
    error_response = None
    if 'default' in operation['responses']:
        error_response = operation['responses']['default']
    for response_code, response in operation['responses'].iteritems():
        if response_code < 200 or response_code >= 300 and 'schema' in response:
            error_response = response
    if error_response != None:
        schema = _get_schema(error_response['schema'])
        if 'type' not in schema or schema['type'] == 'object':
            return '#import "' + prefix + schema['name'] + '.h"'
        elif schema['type'] == 'array' and '$ref' in schema['items']:
            return '#import "' + prefix + schema['items']['$ref'].split('/')[-1] + '.h"'
    else:
        return ''
    

filters = (('ios_attribute_optional', _ios_attribute_optional),
    ('ios_datamodel_attribute_type', _ios_datamodel_attribute_type),
    ('property_type', _property_type),
    ('template_string_in_af_format', _template_string_in_af_format),
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
    ('example_parameter', _example_parameter),
    ('model_base_type', _model_base_type),
    ('realm_property_import', _realm_property_import),
    ('response_type_forward_decl', _response_type_forward_decl),
    ('response_type_import', _response_type_import),
    ('response_schema', _response_schema),
    ('array_definition_items_type', _array_definition_items_type),
    ('property_array_items_type', _property_array_items_type),
    ('error_response_schema', _error_response_schema),
    ('error_response_type', _error_response_type),
    ('error_response_type_import', _error_response_type_import),
    ('error_response_type_forward_decl', _error_response_type_forward_decl)
)
    
    
    
    