#!/usr/bin/env python

import random
from collections import defaultdict
from giant.giant_base.giant_base import GiantError

def raise_(ex):
    raise ex

swagger_to_csharp_enum_example_map = {
    'string': defaultdict(lambda: lambda enum: '"' + random.choice(enum) + '";',
        {
            'guid': lambda enum: 'new Guid(' + random.choice(enum) + ');',
            'date': lambda enum: 'DateTime.parse(' + random.choice(enum) + ');',
            'date-time': lambda enum: 'DateTime.parse(' + random.choice(enum) + ');',
            'byte': lambda enum: raise_(GiantError('Shiver me timbers, I can\'t parse a enum byte type. Implement it yerself!')),
            'binary': lambda enum: raise_(GiantError('Shiver me timbers, I can\'t parse a enum binary type. Implement it yerself!')),
            'password': lambda enum: random.choice(enum)
        }
    ),
    'integer': defaultdict(lambda: lambda enum: str(random.choice(enum)) + ';',
        {
            'int32': lambda enum: str(random.choice(enum)) + ';',
            'int64': lambda enum: str(random.choice(enum)) + ';'
        }
    ),
    'number': defaultdict(lambda: lambda enum: str(random.choice(enum)) + ';',
        {
            'float': lambda enum: str(random.choice(enum)) + ';',
            'double': lambda enum: str(random.choice(enum)) + ';'
        }
    ),
    'boolean': defaultdict(lambda: lambda: str(random.choice(enum)) + ';')
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
    

swagger_to_csharp_example_map = {
    'string': defaultdict(lambda: lambda schema: '"ExampleString";',
        {
            'guid': lambda schema: 'new Guid();',
            'date': lambda schema: 'new DateTime();',
            'date-time': lambda schema: 'new DateTime();',
            'byte': lambda schema: 'new byte[10];',
            'binary': lambda schema: 'new byte[10];',
            'password': lambda schema: '"thepasswordispassword"'
        }
    ),
    'integer': defaultdict(lambda: lambda schema: str(example_integer(schema)) + ';',
        {
            'int32': lambda schema: str(example_integer(schema)) + ';',
            'int64': lambda schema: str(example_integer(schema)) + ';'
        }
    ),
    'number': defaultdict(lambda: lambda schema: str(example_float(schema)) + ';',
        {
            'float': lambda schema: str(example_float(schema)) + ';',
            'double': lambda schema: str(example_float(schema)) + ';'
        }
    ),
    'boolean': defaultdict(lambda: lambda schema: random.choice(('true;', 'false;')))
}