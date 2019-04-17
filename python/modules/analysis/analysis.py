#!/usr/bin/env python

import scipy.stats
import numpy as np
import pandas as pd
import logging


def Calc_chi2_ST( S, T, group ): 

    # - HEPfit (arXiv:1608.01509), U=0 fixed
    if group == 'hepfit':
        mu_S   = 0.10
        mu_T   = 0.12
        sig_S  = 0.08
        sig_T  = 0.07
        rho_ST = 0.86
    
    # - Gfitter (arXiv:1407.3792), U=0 fixed
    elif group == 'gfitter':
        mu_S   = 0.06
        mu_T   = 0.10
        sig_S  = 0.09
        sig_T  = 0.07
        rho_ST = 0.91

    Chi2_S    = ((S - mu_S)**2)/( (sig_S**2)*(1 - rho_ST**2) )
    Chi2_corr = - 2.0*rho_ST*(S - mu_S)*( T - mu_T)/(sig_S*sig_T*(1 - rho_ST**2))
    Chi2_T    = ((T - mu_T)**2)/((sig_T**2)*(1 - rho_ST**2))

    Chi2_ST = Chi2_S + Chi2_corr + Chi2_T

    return Chi2_ST



two_sided_prob_sigma = {
                         1 : 0.6827,
                         2 : 0.9545,
                         3 : 0.9973
                       }

sigma_to_probability = {
                         1 : 0.6827,
                         2 : 0.9545,
                         3 : 0.9973
                       }


chi2_1sig_df2 = scipy.stats.chi2.ppf( q=two_sided_prob_sigma[1], df=2)
chi2_2sig_df2 = scipy.stats.chi2.ppf( q=two_sided_prob_sigma[2], df=2)
chi2_3sig_df2 = scipy.stats.chi2.ppf( q=two_sided_prob_sigma[3], df=2)

chi2_1sig_df3 = scipy.stats.chi2.ppf( q=two_sided_prob_sigma[1], df=3)
chi2_2sig_df3 = scipy.stats.chi2.ppf( q=two_sided_prob_sigma[2], df=3)
chi2_3sig_df3 = scipy.stats.chi2.ppf( q=two_sided_prob_sigma[3], df=3)

chi2_1sig_df4 = scipy.stats.chi2.ppf( q=two_sided_prob_sigma[1], df=4)
chi2_2sig_df4 = scipy.stats.chi2.ppf( q=two_sided_prob_sigma[2], df=4)
chi2_3sig_df4 = scipy.stats.chi2.ppf( q=two_sided_prob_sigma[3], df=4)

chi2_1sig_df5 = scipy.stats.chi2.ppf( q=two_sided_prob_sigma[1], df=5)
chi2_2sig_df5 = scipy.stats.chi2.ppf( q=two_sided_prob_sigma[2], df=5)
chi2_3sig_df5 = scipy.stats.chi2.ppf( q=two_sided_prob_sigma[3], df=5)


def get_chi2_upper_bound_for_nsigma_dof(df, z_col, nsigma, dof):

    chi2_min = df[z_col].min()
    prob = two_sided_prob_sigma[nsigma]
    dchi2_upper_bound = scipy.stats.chi2.ppf(q=prob, df=dof)

    chi2_upper_bound = chi2_min + dchi2_upper_bound

    return chi2_upper_bound


def get_chi2_upper_bounds_123_sigma_for_dof(df, z_col, dof):

    chi2_sig1_upper_bound = get_chi2_upper_bound_for_nsigma_dof(df, z_col, nsigma=1, dof=dof)
    chi2_sig2_upper_bound = get_chi2_upper_bound_for_nsigma_dof(df, z_col, nsigma=2, dof=dof)
    chi2_sig3_upper_bound = get_chi2_upper_bound_for_nsigma_dof(df, z_col, nsigma=3, dof=dof)

    return chi2_sig1_upper_bound, chi2_sig2_upper_bound, chi2_sig3_upper_bound


def get_chi2_upper_bounds_123_sigma_dict_for_dof(df, z_col, dof):

    chi2_sig1_upper_bound = get_chi2_upper_bound_for_nsigma_dof(df, z_col, nsigma=1, dof=dof)
    chi2_sig2_upper_bound = get_chi2_upper_bound_for_nsigma_dof(df, z_col, nsigma=2, dof=dof)
    chi2_sig3_upper_bound = get_chi2_upper_bound_for_nsigma_dof(df, z_col, nsigma=3, dof=dof)

    result = {}
    result['chi2_sig1_upper_bound'] = chi2_sig1_upper_bound
    result['chi2_sig2_upper_bound'] = chi2_sig2_upper_bound
    result['chi2_sig3_upper_bound'] = chi2_sig3_upper_bound

    return result


def get_chi2_upper_bounds_123_sigma_multiple_dof(df, z_col, dofs=[2,3,4,5]):

    result = {}

    for dof in dofs:
        result[dof] = get_chi2_upper_bounds_123_sigma_dict_for_dof(df, z_col, dof)

    return result



def create_new_columns(df):

    df['mA_minus_mHc']     = df['mA'] - df['mHc']
    df['mH_minus_mHc']     = df['mH'] - df['mHc']
    df['Gamma_div_mass_A'] = df['Gamma_A'] / df['mA']
    df['Gamma_div_mass_H'] = df['Gamma_H'] / df['mH']
    df.loc[df['k_hdd'] < 0.0, 'k_hdd_type']   = 'wrongsign'
    df.loc[df['k_hdd'] > 0.0, 'k_hdd_type']   = 'alignment'
    
    if 'xsec_sushi_ggh_A_NNLO' in df.columns:
        df['log_xsec_sushi_ggh_A_NNLO'] = np.log10(df['xsec_sushi_ggh_A_NNLO'])
    
    if 'xsec_sushi_ggh_H_NNLO' in df.columns:
        df['log_xsec_sushi_ggh_H_NNLO'] = np.log10(df['xsec_sushi_ggh_H_NNLO'])
    
    if 'sec_sushi_ggh_A_NNLO_x_br_A_Zh' in df.columns:
        df['log_xsec_sushi_ggh_A_NNLO_x_br_A_Zh'] = np.log10(df['xsec_sushi_ggh_A_NNLO_x_br_A_Zh'])
    
    if 'xsec_sushi_ggh_A_NNLO_x_br_A_tautau' in df.columns:
        df['log_xsec_sushi_ggh_A_NNLO_x_br_A_tautau'] = np.log10(df['xsec_sushi_ggh_A_NNLO_x_br_A_tautau'])
    
    if 'xsec_sushi_ggh_A_NNLO_x_br_A_bb' in df.columns:
        df['log_xsec_sushi_ggh_A_NNLO_x_br_A_bb']     = np.log10(df['xsec_sushi_ggh_A_NNLO_x_br_A_bb'])
    
    if 'xsec_sushi_ggh_A_NNLO_x_br_A_tt' in df.columns:
        df['log_xsec_sushi_ggh_A_NNLO_x_br_A_tt']     = np.log10(df['xsec_sushi_ggh_A_NNLO_x_br_A_tt'])
    
    if 'xsec_sushi_ggh_H_NNLO_x_br_H_ZA' in df.columns:
        df['log_xsec_sushi_ggh_H_NNLO_x_br_H_ZA']     = np.log10(df['xsec_sushi_ggh_H_NNLO_x_br_H_ZA'])

    if 'xsec_sushi_ggh_H_NNLO_x_br_H_hh_bbbb' not in df.columns:
        df['xsec_sushi_ggh_H_NNLO_x_br_H_hh_bbbb'] = df['xsec_sushi_ggh_H_NNLO_x_br_H_hh'] * 0.5809**2


    # - mA binning
    mA_bins     = np.linspace(150, 1000, 18)
    mH_bins     = np.linspace(150, 1000, 18)
    mA_binlabel = np.convolve(mA_bins, [0.5, 0.5], 'valid')
    mH_binlabel = np.convolve(mH_bins, [0.5, 0.5], 'valid')
    df['mA_bin'] = pd.cut(df['mA'], mA_bins, labels=mA_binlabel)
    df['mH_bin'] = pd.cut(df['mH'], mH_bins, labels=mH_binlabel)
    
    df['index'] = df.index

    return df



def print_description(df):

    # - Dataset information
    chi2_Tot_min = df['chi2_Tot_gfitter'].min()
    chi2_Tot_max = df['chi2_Tot_gfitter'].max()
    chi2_HS_min  = df['chi2_HS'].min()
    chi2_HS_max  = df['chi2_HS'].max()
    chi2_ST_gfitter_min = df['chi2_ST_gfitter'].min()
    chi2_ST_gfitter_max = df['chi2_ST_gfitter'].max()
    
    m12_2_min = df['m12_2'].min()
    m12_2_max = df['m12_2'].max()

    print('Number of points: ', len(df))
    print('Header:\n',  df.head(2) )
    print('Columns:\n', df.columns)
    
    print()
    print('---------------------------')
    print()
    print('Dataset info')
    print()
    
    print('chi2_Tot_min:        {:.3f}'.format( chi2_Tot_min) )
    print('chi2_Tot_max:        {:.3f}'.format( chi2_Tot_max) )
    print('chi2_HS_min:         {:.3f}'.format( chi2_HS_min) )
    print('chi2_HS_max:         {:.3f}'.format( chi2_HS_max) )
    print('chi2_ST_gfitter_min: {:.3f}'.format( chi2_ST_gfitter_min) )
    print('chi2_ST_gfitter_max: {:.3f}'.format( chi2_ST_gfitter_max) )
    print('m12_2_min:           {:.3f}'.format( m12_2_min) )
    print('m12_2_max:           {:.3f}'.format( m12_2_max) )

    print('---------------------------')
    print()
    print('Number of points with (sta == 0 | per_4pi == 0 | uni == 0):',  len(df.query('sta == 0 | per_4pi == 0 | uni == 0')) )
    print('Number of points with (tot_hbobs > 1.0):', len(df.query('tot_hbobs > 1.0')) )
    print('Total number of points:', len(df) )



def filter_dataset(df_all,
                   per_constraint = '4pi',
                   mHc_lower_bound = 580.0,
                   hb_constraint = True, 
                   chi2_tot_sigma_cut = 2,
                   chi2_tot_df = 4,
                   show_diagnostics=True):

    # - Create new columns
    df_all = create_new_columns(df_all)

    print()
    print('################################')
    print('### --- Before selection --- ###')
    print('################################')

    print()
    print_description(df_all)
    print()
    print('#########################')
    print('### --- Selection --- ###')
    print('#########################')

    # - Queries
    queries = []

    if per_constraint:
        queries.append("per_{} == 1".format(per_constraint))

    if mHc_lower_bound:
        queries.append("mHc > 580.0")

    if hb_constraint:
        queries.append("tot_hbobs < 1.0")

    if chi2_tot_sigma_cut:
        chi2_tot_min = df_all['chi2_Tot_gfitter'].min()

        chi2_tot_cut = chi2_tot_min + scipy.stats.chi2.ppf(
                q=sigma_to_probability[chi2_tot_sigma_cut],
                df=chi2_tot_df)

        queries.append("chi2_Tot_gfitter < {:.3f}".format(chi2_tot_cut))

    selection = merge_query_strs(queries)
    print("Chosen chi2 CL level: {}".format(sigma_to_probability[chi2_tot_sigma_cut]))
    print("Chosen chi2 d.o.f: {}".format(chi2_tot_df))
    
    df = df_all.query(selection)
    
    df.reindex()


    print('Condition: ', selection)
    print()

    print('################################')
    print('### --- After selection --- ###')
    print('################################')

    print_description(df)

    return df



def merge_query_strs(query_strs):

    merged_query_strs = ""

    for query_str in query_strs:
        merged_query_strs += query_str + " & "
    merged_query_strs = merged_query_strs[:-3]

    return merged_query_strs



def info_sheet(df, model_parameters=['cba', 'tb', 'mH', 'mA', 'mHc', 'Z7']):

    alignment = df.query('k_hdd > 0.0')
    wrongsign = df.query('k_hdd < 0.0')

    alignment_chi2_HS_min         = alignment['chi2_HS'].min()
    wrongsign_chi2_HS_min         = wrongsign['chi2_HS'].min()
    alignment_chi2_ST_gfitter_min = alignment['chi2_ST_gfitter'].min()
    wrongsign_chi2_ST_gfitter_min = wrongsign['chi2_ST_gfitter'].min()
    alignment_chi2_Tot_gfitter_min = alignment['chi2_Tot_gfitter'].min()
    wrongsign_chi2_Tot_gfitter_min = wrongsign['chi2_Tot_gfitter'].min()

    print("####################")
    print("### --- chi2 --- ###")
    print("####################")
    print("")

    print("| Minimums  |")
    print("| --------- |")
    print("| Region    | chi2_HS | chi2_ST_gfitter | chi2_Tot_gfitter |")
    print("| --------- | ------- | --------------- | ---------------- |")
    print("| alignment | {:.3f}  | {:.3f}           | {:.3f}           |".format(alignment_chi2_HS_min, alignment_chi2_ST_gfitter_min, alignment_chi2_Tot_gfitter_min))
    print("| wrongsign | {:.3f}  | {:.3f}           | {:.3f}           |".format(wrongsign_chi2_HS_min, wrongsign_chi2_ST_gfitter_min, wrongsign_chi2_Tot_gfitter_min))
    

    print()
    print("chi2_Tot_gfitter minimum points")
    print()

    alignment_chi2_Tot_gfitter_minimum_pt = alignment.iloc[alignment['chi2_Tot_gfitter'].idxmin()]
    wrongsign_chi2_Tot_gfitter_minimum_pt = wrongsign.iloc[wrongsign['chi2_Tot_gfitter'].idxmin()]

    print("Alignment:")
    print(alignment_chi2_Tot_gfitter_minimum_pt[model_parameters])
    print()
    print("Wrong sign:")
    print(wrongsign_chi2_Tot_gfitter_minimum_pt[model_parameters])

    pars_to_describe = ['cba', 'tb', 'mH', 'mA', 'mHc', 'Z7']
    print()
    print("#############################" )
    print("### --- df.describe() --- ###" )
    print("#############################" )
    print()
    print("- alignment")
    print(alignment[pars_to_describe].describe())
    print()
    print("- wrongsign")
    print(wrongsign[pars_to_describe].describe())

