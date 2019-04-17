#!/usr/bin/env python

import glob
import os
import collections
import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import plotting.plotting as pl
from plotting.cosmetics import *
import hepdata.hepdata as hepdata
import magellan.config as magconf
import interpolation.interpolation as interputils


class MeasurementBase:

    def __init__(self,
                 data   = {},
                 description = 'analysis in X production mode decaying to YZ',
                 tag         = 'ANALYSIS-TAG-001',
                 label       = "label",
                 process     = 'X -> YZ',
                 factor      = 1.0,
                 observables = {"observable1":{"upper_limit":{"function":lambda x:x, "arguments":["arg1" , "arg2"]}}},
                 CL          = "0.95",
                 sqrt_s      = 13,
                 luminosity  = 1.0,
                 url         = '',
                 comment     = None,
                 ):

        self.container = {}
        self.container['data']        = data
        self.container['description'] = description
        self.container['tag']         = tag
        self.container['label']       = label
        self.container['process']     = process
        self.container['factor']      = factor
        self.container['luminosity']  = luminosity
        self.container['observables'] = observables
        self.container['sqrt_s']      = sqrt_s
        self.container['comment']     = comment
        self.container['url']         = url


    def get_idx_of_excluded_pts(self, df, observable='first', limit_type='expected', scale=1.0):

        if observable == 'first':
            observable = list(self.observables.keys())[0]

        observable_limit_function  = self.observables[observable]["upper_limit"]["function"]
        observable_limit_arguments = self.observables[observable]["upper_limit"]["arguments"]
        limit_value      = observable_limit_function(df[observable_limit_arguments], limit_type)
        idx_excluded_pts = df[observable] > limit_value * scale

        return idx_excluded_pts

    def get_excluded_pts(self, df, observable='first',  limit_type='limit_exp', scale=1.0):

        if observable == 'first':
            observable = list(self.observables.keys())[0]

        idxs = self.get_idx_of_excluded_pts(df, observable, limit_type, scale)
        dfr  = df[idxs]

        return dfr

    def add_excluded_pts_as_col(self, df, observable='first', limit_type='limit_exp'):

        if observable == 'first':
            observable = list(self.observables.keys())[0]
        
        new_col = "{}_{}_{}".format(observable, self.tag, limit_type)
        col_name_excl_bool = new_col + '_excl'
        df[newcol] = np.where(idx,  True, False )

    # - class variabales
    def __getitem__(self, key):
        return self.container[key]

    def __setitem__(self, key, value):
        self.container[key] = value

    def __getattr__(self, name):
        return self.container[name]

######################################################################################


class Measurement(MeasurementBase):


    def print_data(self):
        print(self.data)


    def plot_interpolated_pts(self, limit_type='limit_exp', ax=None, plot_kwargs={}):

        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = None

        x = self.interpolation[limit_type]['x_grid']
        y = self.interpolation[limit_type]['y_grid']
        ax.plot(x,y, **plot_kwargs)
        
        return fig, ax


    def plot_measured_pts(self, , limit_type='exp', ax=None, plot_kwargs={'marker':'o'}):

        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = None

        data_ycol = 'limit_{}'.format(limit_type)
        data_ycol = 'limit_{}'.format(limit_type)

        x = self.data['masspts']
        y = self.data[ycol]
        ax.plot(x, y, **plot_kwargs)
        
        return fig, ax

    def plot_excluded_pts(self, df, observable='first', limit_type='limit_exp',
                          xcol='first_arg', ycol='first_observable',
                          ax=None, scatter_kwargs_common={}, scale=1.0, excluded_color='firebrick',
                          show_interpolated_pts=True):

        if observable == 'first':
            observable = list(self.observables.keys())[0]

        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = None

        excluded_pts = self.get_excluded_pts(df, observable=observable, limit_type=limit_type,
                scale=scale)

        if xcol == 'first_arg':
            xcol = self.observables[observable]["upper_limit"]["arguments"][0]
        if ycol == 'first_observable':
            ycol = observable

        scatter_kwargs_all_pts      = dict(scatter_kwargs_common)
        scatter_kwargs_excluded_pts = dict(scatter_kwargs_common)
        scatter_kwargs_all_pts['c'] = cat_to_color['all'] 
        scatter_kwargs_excluded_pts['c'] = cat_to_color['excluded']
        pl.scatter(df, xcol, ycol, ax=ax, scatter_kwargs=scatter_kwargs_all_pts)
        pl.scatter(excluded_pts, xcol, ycol, ax=ax, scatter_kwargs=scatter_kwargs_excluded_pts)

        if show_interpolated_pts and len(self.observables[observable]["upper_limit"]["arguments"]) == 1:
            plot_kwargs_interpolated_pts = {'linestyle':'--', 'c':'k'}
            xmin, xmax = df[xcol].min(), df[xcol].max()
            xgrid = np.linspace(xmin, xmax, 100)
            ygrid = self.observables[observable]["upper_limit"]["function"](xgrid, limit_type)
            ax.plot(xgrid, ygrid, **plot_kwargs_interpolated_pts)
            
           #self.plot_interpolated_pts(ax=ax, limit_type=limit_type,
           #        plot_kwargs=plot_kwargs_interpolated_pts)
    
        return fig, ax

######################################################################################

class UpperLimitData:

    def __init__(self,
                 independent_variables = [],
                 measurement_data = pd.DataFrame({}),
                 ):

        self.container = {}
        self.container['independent_variables'] = independent_variables
        self.container['measurement_data']      = measurement_data
        self.container['interpolation']         = self.create_interpolation(measurement_data, independent_variables)


    @classmethod
    def from_datafile(cls,
                      input_datafile_path,
                      independent_variables=[],
                      ):

        measurement_data = pd.read_csv(input_datafile_path, delim_whitespace=True)
        
        return cls(independent_variables=independent_variables,
                   measurement_data=measurement_data
                  )


    def create_interpolation(self, measurement_data, independent_variables):
        interpolation = {}

        interpolation['limit_exp'] = interputils.create_interpolation_record_df_auto(measurement_data,
                                        dependent_variable='limit_exp', independent_variables=independent_variables)
        interpolation['limit_obs'] = interputils.create_interpolation_record_df_auto(measurement_data,
                                        dependent_variable='limit_obs', independent_variables=independent_variables)

        return interpolation

    def __getitem__(self, key):
        return self.container[key]

    def __setitem__(self, key, value):
        self.container[key] = value

    def __getattr__(self, name):
        return self.container[name]

