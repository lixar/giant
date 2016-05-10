#!/usr/bin/env python

import re

_non_letters_re = re.compile('([^a-zA-Z])')
_non_lowercase_re = re.compile('([^a-z])')
_one_or_more_letters = re.compile('[a-zA-Z]+')

def pascal_case(value):
    parts = _non_letters_re.split(value)
    parts = filter(lambda v: _one_or_more_letters.match(v), parts)
    splitted = []
    for part in parts:
        more_parts = _non_lowercase_re.split(part)
        splitted.append(more_parts[0].lower())
        for i in range(1, len(more_parts)-1, 2):
            splitted.append(more_parts[i].lower() + more_parts[i+1])
    splitted = filter(lambda v: v != '', splitted)
    splitted = ''.join(v.capitalize() for v in splitted)
    return splitted
    
def camel_case(value):
    pascal_cased = pascal_case(value)
    return pascal_cased[0].lower() + pascal_cased[1:]