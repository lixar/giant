#!/usr/bin/env python

from collections import defaultdict

_swagger_to_objc_map = {
    'string': defaultdict(lambda: 'NSString*',
        {
            'guid': 'NSString*',
            'date': 'NSDate*',
            'date-time': 'NSDate*',
            'byte': 'NSData*',
            'binary': 'NSData*',
            'password': 'NSString*'
        }
    ),
    'integer': defaultdict(lambda: 'NSNumber*',
        {
            'int32': 'NSNumber*',
            'int64': 'NSNumber*'
        }
    ),
    'number': defaultdict(lambda: 'NSNumber*',
        {
            'float': 'NSNumber*',
            'double': 'NSNumber*'
        }
    ),
    'boolean': defaultdict(lambda: 'NSNumber*'),
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

def _get_property(prop):
    if '$ref' in prop:
        return swagger['definitions'][prop['$ref'].split('/')[-1]]
    return prop

def _ios_attribute_optional(definition, property_name):
    if 'required' not in definition:
        return False
    return property_name in definition['required']
    
def _property_type(prop):
    return _swagger_to_objc_map[prop['type']][prop.get('format')]
    
def _ios_datamodel_attribute_type(prop):
    return _swagger_to_xcdatamodel_map[prop['type']][prop.get('format')]
    
def _template_string_in_af_format(string_value):
    import re
    return re.subn('\{([^}]+)\}', ':\\1', string_value)[0]
    
filters = (('ios_attribute_optional', _ios_attribute_optional),
    ('ios_datamodel_attribute_type', _ios_datamodel_attribute_type),
    ('property_type', _property_type),
    ('template_string_in_af_format', _template_string_in_af_format))