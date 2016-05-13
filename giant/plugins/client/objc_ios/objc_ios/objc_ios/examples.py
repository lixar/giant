#!/usr/bin/env python

import random
from collections import defaultdict
from giant.giant_base.giant_base import GiantError

def raise_(ex):
    raise ex

swagger_to_objc_enum_example_map = {
    'string': defaultdict(lambda: lambda enum: '@"' + random.choice(enum) + '"',
        {
            'guid': lambda enum: '@"' + random.choice(enum) + '"',
            'date': lambda enum: '@"' + random.choice(enum) + '"',
            'date-time': lambda enum: '@"' + random.choice(enum) + '"',
            'byte': lambda enum: raise_(GiantError('Shiver me timbers, I can\'t parse a enum byte type. Implement it yerself!')),
            'binary': lambda enum: raise_(GiantError('Shiver me timbers, I can\'t parse a enum binary type. Implement it yerself!')),
            'password': lambda enum: '@"' + random.choice(enum) + '"',
        }
    ),
    'integer': defaultdict(lambda: lambda enum: '@(' + str(random.choice(enum)) + ')',
        {
            'int32': lambda enum: '@(' + str(random.choice(enum)) + ')',
            'int64': lambda enum: '@(' + str(random.choice(enum)) + ')'
        }
    ),
    'number': defaultdict(lambda: lambda enum: '@(' + str(random.choice(enum)) + ')',
        {
            'float': lambda enum: '@(' + str(random.choice(enum)) + ')',
            'double': lambda enum: '@(' + str(random.choice(enum)) + ')',
        }
    ),
    'boolean': defaultdict(lambda: lambda enum: '@(' + str(random.choice(enum)) + ')')
}

def example_integer(schema):
    minimum = schema.get('minimum', 1)
    maximum = schema.get('maximum', minimum + 100)
    multiple = schema.get('multipleOf', 1)
    return random.choice(range(minimum, maximum, multiple))
    
def example_float(schema):
    minimum = schema.get('minimum', 0.0)
    maximum = schema.get('maximum', 100.0)
    multiple = schema.get('multipleOf', 0.01)
    return str(round(random.uniform(minimum, maximum) / multiple) * multiple)
    

swagger_to_objc_example_map = {
    'string': defaultdict(lambda: lambda schema: '@"ExampleString"',
        {
            'guid': lambda schema: '@"ExampleString"',
            'date': lambda schema: '[NSDate date]',
            'date-time': lambda schema: '[NSDate date]',
            'byte': lambda schema: '@"ExampleString"',
            'binary': lambda schema: '@"ExampleString"',
            'password': lambda schema: '@"thepasswordispassword"'
        }
    ),
    'integer': defaultdict(lambda: lambda schema: "@" + str(example_integer(schema)),
        {
            'int32': lambda schema: "@" + str(example_integer(schema)),
            'int64': lambda schema: "@" + str(example_integer(schema))
        }
    ),
    'number': defaultdict(lambda: lambda schema: str(example_float(schema)),
        {
            'float': lambda schema: "@" + str(example_float(schema)),
            'double': lambda schema: "@" + str(example_float(schema))
        }
    ),
    'boolean': defaultdict(lambda: lambda schema: random.choice('YES', 'NO')),
    'array': defaultdict(lambda: lambda schema: '@[]')
}

swagger_to_objc_example_string_map = {
    'string': defaultdict(lambda: lambda schema: '@"ExampleString"',
        {
            'guid': lambda schema: '@"ExampleString"',
            'date': lambda schema: '[NSDate date].iso8601;',
            'date-time': lambda schema: '[NSDate date].iso8601;',
            'byte': lambda schema: '@"ExampleString"',
            'binary': lambda schema: '@"ExampleString"',
            'password': lambda schema: '"thepasswordispassword"'
        }
    ),
    'integer': defaultdict(lambda: lambda schema: "@(" + str(example_integer(schema)) + ').stringValue',
        {
            'int32': lambda schema: "@(" + str(example_integer(schema)) + ').stringValue',
            'int64': lambda schema: "@(" + str(example_integer(schema)) + ').stringValue'
        }
    ),
    'number': defaultdict(lambda: lambda schema: str(example_float(schema)) + '.stringValue',
        {
            'float': lambda schema: "@(" + str(example_float(schema)) + ').stringValue',
            'double': lambda schema: "@(" + str(example_float(schema)) + ').stringValue'
        }
    ),
    'boolean': defaultdict(lambda: lambda schema: '@(' + random.choice('YES', 'NO') + ').stringValue'),
    'array': defaultdict(lambda: lambda schema: '@"[]"')
}

swagger_to_objc_string_map = {
    'string': defaultdict(lambda: lambda schema, variable_name: variable_name,
        {
            'guid': lambda schema, variable_name: variable_name,
            'date': lambda schema, variable_name: variable_name + '.iso8601;',
            'date-time': lambda schema, variable_name: variable_name + '.iso8601;',
            'byte': lambda schema, variable_name: variable_name,
            'binary': lambda schema, variable_name: variable_name,
            'password': lambda schema, variable_name: variable_name
        }
    ),
    'integer': defaultdict(lambda: lambda schema, variable_name: variable_name + '.stringValue',
        {
            'int32': lambda schema, variable_name: variable_name + '.stringValue',
            'int64': lambda schema, variable_name: variable_name + '.stringValue'
        }
    ),
    'number': defaultdict(lambda: lambda schema, variable_name: variable_name + '.stringValue',
        {
            'float': lambda schema, variable_name: variable_name + '.stringValue',
            'double': lambda schema, variable_name: variable_name + '.stringValue'
        }
    ),
    'boolean': defaultdict(lambda: lambda schema, variable_name: variable_name +'.stringValue')
}