#!/usr/bin/env python

import os
import glob
import collections
import yaml
import pandas as pd
import numpy as np

import interpolation.interpolation as interpolation
from scipy.interpolate import interp1d
from scipy.interpolate import interp2d


def limit_yaml_to_df_1d(input_file_path, independent_variables):


    with open(input_file_path, "r") as input_file:
    
        contents = yaml.load(input_file)
        
        indep_pts_list = []
        for i, var in enumerate(independent_variables):
            indep_pts_list.append([ m['value'] for m in contents['independent_variables'][0]['values']])

        limit_obs     = [ l['value'] for l in contents['dependent_variables'][0]['values']]
        limit_exp     = [ l['value'] for l in contents['dependent_variables'][1]['values']]
        limit_exp_m2s = [ l['errors'][1]['asymerror']['minus'] for l in contents['dependent_variables'][1]['values']]
        limit_exp_m1s = [ l['errors'][0]['asymerror']['minus'] for l in contents['dependent_variables'][1]['values']]
        limit_exp_p1s = [ l['errors'][0]['asymerror']['plus']  for l in contents['dependent_variables'][1]['values']]
        limit_exp_p2s = [ l['errors'][1]['asymerror']['plus']  for l in contents['dependent_variables'][1]['values']]
    
    
        measurement_database = collections.OrderedDict({
                                                         "limit_exp"             : limit_exp,
                                                         "limit_exp_m2s"         : limit_exp_m2s,
                                                         "limit_exp_m1s"         : limit_exp_m1s,
                                                         "limit_exp_p1s"         : limit_exp_p1s,
                                                         "limit_exp_p2s"         : limit_exp_p2s,
                                                         "limit_obs"             : limit_obs
                                                        })


        for var, pts in zip(independent_variables, indep_pts_list):
            measurement_database[var] = pts
    
        df = pd.DataFrame(measurement_database)

    return df



def interpolate_limits_1d(data, independent_variable):

    hepdata_interpolation = {}
    hepdata_interpolation['limit_exp_m2s'] = interpolation.interpolate_df_cols_1d(data, independent_variable, 'limit_exp_m2s')
    hepdata_interpolation['limit_exp_m1s'] = interpolation.interpolate_df_cols_1d(data, independent_variable, 'limit_exp_m1s')
    hepdata_interpolation['limit_exp']     = interpolation.interpolate_df_cols_1d(data, independent_variable, 'limit_exp')
    hepdata_interpolation['limit_exp_p1s'] = interpolation.interpolate_df_cols_1d(data, independent_variable, 'limit_exp_p1s')
    hepdata_interpolation['limit_exp_p2s'] = interpolation.interpolate_df_cols_1d(data, independent_variable, 'limit_exp_p2s')
    hepdata_interpolation['limit_obs']     = interpolation.interpolate_df_cols_1d(data, independent_variable, 'limit_obs')

    return hepdata_interpolation


def create_datablock_1d(input_file_path, independent_variable):

    df = limit_yaml_to_df_1d(input_file_path, independent_variable)
    hepdata_interpolation = interpolate_limits_1d(df, independent_variable)

    datablock = {}

    return datablock

