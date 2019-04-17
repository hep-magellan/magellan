#!/usr/bin/env python

import os
from glob import glob
import yaml
import pandas as pd

input_files = glob('./limit*.yaml')
output_path = "limit_vs_mA_Gamma_A.dat"

dfs = []

for file in input_files:

    base = os.path.basename(file)
    w = base.split('_')[1][1:]
    
    f = open(file)
    contents = yaml.load(f)
    mass      = [ m['value'] for m in contents['independent_variables'][0]['values']]
    limit_exp = [ l['value'] for l in contents['dependent_variables'][1]['values']]
    limit_obs = [ l['value'] for l in contents['dependent_variables'][0]['values']]
    dfi = pd.DataFrame({'mA': mass, 'limit_exp': limit_exp, 'limit_obs': limit_obs, 'GammaA_div_mA':float(w)/100.0})
    dfs.append(dfi)
    f.close()

df = pd.concat(dfs)
df.to_csv(output_path, sep=' ', index=False)
