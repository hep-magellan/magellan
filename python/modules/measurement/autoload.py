#!/usr/bin/env python

import os
import importlib

import magellan.config as magconf
from .measurement import Measurement

measurement_database = {}

for dir in os.listdir(magconf.paths['measurements']):

    setup_file_path = os.path.join(magconf.paths['measurements'], dir, "analysis.py")
    if os.path.isfile(setup_file_path):

        module_name = "{}.analysis".format(dir)
        print("import {}".format(module_name))
        module = importlib.import_module(module_name)
        
        measurement_database[module.m['tag']] = module.m
