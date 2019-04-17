#!/usr/bin/env python

import numpy as np
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
from plotting.cosmetics import *


headers = {
            "old" : ['Z7_mcmc', 'mH_mcmc', 'mHc_mcmc', 'mA_mcmc', 'cba_mcmc', 'tb_mcmc',
                         'Z7_2HDMC', 'mH_2HDMC', 'mHc_2HDMC', 'mA_2HDMC', 'cba_2HDMC', 'tb_2HDMC',
                         'sinba', 'Z4_c', 'Z5_c', 'm12_2', 'l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7',
                         'g_HpHmh', 'junk', 'Gamma_h', 'Gamma_H', 'Gamma_Hc', 'Gamma_A', 'br_A_tt',
                         'br_A_bb', 'br_A_gg', 'br_A_mumu', 'br_A_tautau', 'br_A_Zga', 'br_A_Zh',
                         'br_A_ZH', 'br_A_gaga', 'br_H_tt', 'br_H_bb', 'br_H_gg', 'br_H_mumu',
                         'br_H_tautau', 'br_H_Zga', 'br_H_Zh', 'br_H_WW', 'br_H_ZZ', 'br_H_ZA',
                         'br_H_AA', 'br_H_gaga', 'br_Hp_tb', 'br_Hp_taunu', 'br_Hp_Wh', 'br_Hp_WH',
                         'br_Hp_WA', 'sta', 'uni', 'per_4pi', 'per_8pi', 'S', 'T', 'U', 'V', 'W', 'X',
                         'delta_rho', 'delta_amu', 'tot_hbobs', 'sens_ch', 'chi2_HS', 'chi2_ST_hepfit',
                         'chi2_ST_gfitter', 'chi2_Tot_hepfit', 'chi2_Tot_gfitter', 'k_huu', 'k_hdd',
                         'likelihood', 'stay_count'],
            "default" : ['Z7_mcmc', 'mH_mcmc', 'mHc_mcmc', 'mA_mcmc', 'cba_mcmc', 'tb_mcmc',
                         'Z7_2HDMC', 'mH_2HDMC', 'mHc_2HDMC', 'mA_2HDMC', 'cba_2HDMC', 'tb_2HDMC',
                         'sinba', 'Z4_c', 'Z5_c', 'm12_2',
                         'l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7',
                         'g_HpHmh', 'Gamma_h', 'Gamma_H', 'Gamma_Hc', 'Gamma_A',
                         'br_h_bb', 'br_h_tautau', 'br_h_gg', 'br_h_WW', 'br_h_ZZ', 'br_h_gaga',
                         'br_A_tt', 'br_A_bb', 'br_A_gg', 'br_A_mumu', 'br_A_tautau', 'br_A_Zga', 'br_A_Zh',
                         'br_A_ZH', 'br_A_gaga',
                         'br_H_tt', 'br_H_bb', 'br_H_gg', 'br_H_mumu',
                         'br_H_tautau', 'br_H_Zga', 'br_H_Zh', 'br_H_WW', 'br_H_ZZ', 'br_H_ZA',
                         'br_H_hh', 'br_H_AA', 'br_H_gaga',
                         'br_Hp_tb', 'br_Hp_taunu', 'br_Hp_Wh', 'br_Hp_WH', 'br_Hp_WA',
                         'sta', 'uni', 'per_4pi', 'per_8pi',
                         'S', 'T', 'U', 'V', 'W', 'X',
                         'delta_rho', 'delta_amu', 'tot_hbobs', 'sens_ch',
                         'chi2_HS', 'chi2_ST_hepfit', 'chi2_ST_gfitter', 'chi2_Tot_hepfit', 'chi2_Tot_gfitter',
                         'k_huu', 'k_hdd',
                         'likelihood', 'stay_count']

          }

column_rename_scheme = {'Z7_2HDMC':'Z7', 'mH_2HDMC':'mH', 'mHc_2HDMC':'mHc', 'mA_2HDMC':'mA', 'cba_2HDMC':'cba', 'tb_2HDMC':'tb'}

parameters = ['Z7', 'mH', 'mHc', 'mA', 'cba', 'tb']
monitoring_parameters = ['Z7', 'mH', 'mHc', 'mA', 'cba', 'tb', 'chi2_HS', 'chi2_ST_gfitter', 'k_hdd']

####################################################################################################

##########################
### --- Processing --- ###
##########################

def load_in_chains_from_files(files, fileheader=headers['default'], skiprows=0,
        column_rename_dict=column_rename_scheme):

    nfiles = len(files)
    print("Loading in {} files".format(nfiles))

    chains = []
    for i, f in enumerate(files):
        chain = pd.read_table(f, index_col=None, names=fileheader, skiprows=skiprows, delim_whitespace=True, error_bad_lines=False)
        chain = chain.rename(columns=column_rename_dict)
        chains.append(chain)

    return chains


def filter_chains(chains, query):

    new_chains = []
    for chain in chains:
        new_chain = chain.query(query)
        if len(new_chain) > 0:
            new_chains.append(new_chain)

    return new_chains


def trim_chains(chains, start=0, end=None):

    new_chains = []
    for chain in chains:
        chain = chain.reindex()
        new_chain = chain[start:end]
        new_chains.append(new_chain)

    return new_chains

def split_chains_alignment_rightarm(chains, nchains=None, k_hdd_startpos=200):

    alignment = []
    rightarm = []
    
    for i,chain in enumerate(chains[:nchains]):
            
        if chain['k_hdd'][k_hdd_startpos:].mean() < 0.0:
            rightarm.append(chain)
        else:
            alignment.append(chain)

    return alignment, rightarm


##########################
### --- Statistics --- ###
##########################

def parameter_statistics(chains, parameters):
    """Calculate parameter mean and variance for each chain.
    Returns a pd.DataFrame with
    - rows corresponding the different chains, and
    - columnss of ["parameter1_mean", "parameter1_var", ...]."""
    
    nchains = len(chains)
    npars = len(parameters)

    columns = []

    for par in parameters:

        par_mean_key = "{}_mean".format(par)
        par_var_key  = "{}_var".format(par)
        columns.append(par_mean_key)
        columns.append(par_var_key)

    columns.append("chain_length")
    
    # - Create an empty dataframe
    df = pd.DataFrame(data=np.zeros((nchains, 2*npars+1)), columns=columns)
    
    for i, chain in enumerate(chains):
        for par in parameters:

            mean = chain[par].mean()
            var = chain[par].var()
            par_mean_key = "{}_mean".format(par)
            par_var_key = "{}_var".format(par)

            df.at[i, par_mean_key] = mean
            df.at[i, par_var_key] = var

        df.at[i, "chain_length"] = len(chain)
        
    return df


def gelman_rubin_statistic(chain_statistics, parameters):
    
    nchains = len(chain_statistics)
    npars = len(parameters)
    m = nchains

    df = pd.DataFrame(columns=['par', 'globmean', 'W', 'B_red', 'Vhat', 'R'])
    
    for par in parameters:

        par_mean_key = "{}_mean".format(par)
        par_var_key = "{}_var".format(par)
        
        row = {}

        W = chain_statistics[par_var_key].mean()
        B_red = chain_statistics[par_mean_key].var()

        Vhat = W + B_red

        row['par'] = par
        row['globmean'] = chain_statistics[par_mean_key].mean()
        row['W'] = W
        row['B_red'] = B_red
        row['Vhat'] = Vhat
        row['R'] = np.sqrt(Vhat/W)

        row = pd.DataFrame([row], columns=row.keys())

        df = df.append(row)
        
    return df


def display_chain_statistics(chains, parameters):
    npars = len(parameters)
    fig, axes = plt.subplots(nrows=npars)
    axes = axes.flatten()
    axes.hist()







########################
### --- Plotting --- ###
########################


def chain_lengths_histo(chains):

    chain_lengths = []
    for chain in chains:
        chain_length = len(chain)
        chain_lengths.append(chain_length)

    fig, ax = plt.subplots()
    ax.hist(chain_lengths)

    return fig, ax

def traceplot(chains, par, start=0, stop=-1):

    fig, ax = plt.subplots()

    for chain in chains:
        r = chain[start:stop]
        ax.plot(range(len(r)), r[par], alpha=0.3, label=None, rasterized=True)
#       chain[:onlyshowfirstnpoints].plot(y=par, ax=ax, alpha=0.3, label=None, legend=False, rasterized=True)
    ax.set_xlabel("Iteration")
    ax.set_ylabel(var_to_label[par])

    return fig, ax


def traceplots(chains, pars, ncols=3, start=0, stop=-1):

    nwindows = len(pars)
    nrows = int(nwindows/ncols + 0.5)

    fig, ax = plt.subplots(ncols=ncols, nrows=nrows)
    ax = ax.flatten()

    for i, par in enumerate(pars):
        for chain in chains:
            r = chain[start:stop]
            ax[i].plot(range(len(r)), r[par], alpha=0.3, label=None, rasterized=True)
#           chain[:onlyshowfirstnpoints].plot(y=par, ax=ax[i], alpha=0.3, label=None, legend=False, rasterized=True)

        ax[i].set_xlabel("Iteration")
        ax[i].set_ylabel(var_to_label[par])
    
    return fig, ax


def chains_projection(chains, xcol, ycol, kind='line', alpha=0.3):

    fig, ax = plt.subplots()

    for chain in chains:
        chain.plot(xcol, ycol, ax=ax, alpha=alpha, legend=False, kind=kind)

    ax.set_xlabel(var_to_label[xcol])
    ax.set_ylabel(var_to_label[ycol])

    return fig, ax
