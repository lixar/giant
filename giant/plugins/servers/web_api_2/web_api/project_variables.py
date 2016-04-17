#!/usr/bin/env python

import uuid
import os
import json

_config = None

def load_variables():
    if 'webapi.config' in os.listdir(os.getcwd()):
        with open(os.path.join(os.getcwd(), 'webapi.config'), 'r') as config_json:
            _config = json.load(config_json)
    else:
        _config = {
            'assembly': str(uuid.uuid4()),
            'project': str(uuid.uuid4())
        }
        with open(os.path.join(os.getcwd(), 'webapi.config'), 'w') as config_json:
            json.dump(_config, config_json)
    return _config
    
        