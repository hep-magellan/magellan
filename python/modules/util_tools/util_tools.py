#!/usr/bin/env python

import os
import json


def load_json(input_path):

    with open(input_path, 'r') as f_in:
        contents = json.load(f_in)
        
    return contents


def timeit( orig_func ):
    
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time()
        dt = t2 - t1
        print('{} ran in: {} sec'.format(orig_func.__name__, dt) )
        return result
    
    return wrapper


class Timer:    


    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

