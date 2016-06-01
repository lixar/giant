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
            'bundle_id': str('com.bundle.identifier'),
            'class_prefix': 'GNT'
        }
        with open(os.path.join(os.getcwd(), 'ios.config'), 'w') as config_json:
            json.dump(_config, config_json)
    return _config
    
        