#!/usr/bin/env python

import os
import yaml

paths = {}
paths['Magellan']          = os.environ['Magellan_path']
paths['measurements']      = os.path.join(paths['Magellan'], './data/measurements/')
paths['figures']           = os.path.join(paths['Magellan'], './figures/')
paths['matplotlib_styles'] = os.environ['ENV_MATPLOTLIB_STYLES_DIR']
paths['local_config_path'] = os.path.join(paths['Magellan'], 'config', 'local.yaml')

with open(paths['local_config_path'], 'r') as stream:
    try:
        local_config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

paths.update(local_config['paths'])
