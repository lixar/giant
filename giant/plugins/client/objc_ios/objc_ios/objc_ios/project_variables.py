#!/usr/bin/env python

import uuid
import os
import json

_config = None

def load_variables():
    if 'ios.config' in os.listdir(os.getcwd()):
        with open(os.path.join(os.getcwd(), 'ios.config'), 'r') as config_json:
            _config = json.load(config_json)
    else:
        _config = {
            'bundle_identifier': str('com.bundle.identifier'),
            'class_prefix': 'GNT',
            'project_name': None
        }
        for key in _config.keys():
            new_value = raw_input('{} [{}]: '.format(key, _config[key]))
            if new_value == '':
                continue
            _config[key] = new_value
        with open(os.path.join(os.getcwd(), 'ios.config'), 'w') as config_json:
            json.dump(_config, config_json)
    return _config
    
        