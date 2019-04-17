# coding: utf-8
# Default session for initializing parameter space data

import sys
import pandas as pd
import numpy as np
from scipy import stats
import THDM_utils.THDM_utils as thdm


# - Import plot definitions
from THDM_utils.plotting.plotting import *

#ds = 'Epsilon_all_data_with_sushi_merged.h5f'
ds = sys.argv[1]

# - Read in dataset

df_all = pd.read_hdf(ds)

print('Imported dataset: ', ds )
print('Number of points: ', len(df_all))

print('Header:\n',  df_all.head(2) )
print('Columns:\n', df_all.columns)

# - Create new columns

df_all['mA_minus_mHc']                            = df_all['mA'] - df_all['mHc']
df_all['mH_minus_mHc']                            = df_all['mH'] - df_all['mHc']
df_all['Gamma_div_mass_A'] = df_all['Gamma_A'] / df_all['mA']
df_all['Gamma_div_mass_H'] = df_all['Gamma_H'] / df_all['mH']
df_all.loc[df_all['k_hdd'] < 0.0, 'k_hdd_type']   = 'wrongsign'
df_all.loc[df_all['k_hdd'] > 0.0, 'k_hdd_type']   = 'alignment'

if 'xsec_sushi_ggh_A_NNLO' in df_all.columns:
    df_all['log_xsec_sushi_ggh_A_NNLO'] = np.log10(df_all['xsec_sushi_ggh_A_NNLO'])

if 'xsec_sushi_ggh_H_NNLO' in df_all.columns:
    df_all['log_xsec_sushi_ggh_H_NNLO'] = np.log10(df_all['xsec_sushi_ggh_H_NNLO'])

if 'sec_sushi_ggh_A_NNLO_x_br_A_Zh' in df_all.columns:
    df_all['log_xsec_sushi_ggh_A_NNLO_x_br_A_Zh'] = np.log10(df_all['xsec_sushi_ggh_A_NNLO_x_br_A_Zh'])

if 'xsec_sushi_ggh_A_NNLO_x_br_A_tautau' in df_all.columns:
    df_all['log_xsec_sushi_ggh_A_NNLO_x_br_A_tautau'] = np.log10(df_all['xsec_sushi_ggh_A_NNLO_x_br_A_tautau'])

if 'xsec_sushi_ggh_A_NNLO_x_br_A_bb' in df_all.columns:
    df_all['log_xsec_sushi_ggh_A_NNLO_x_br_A_bb']     = np.log10(df_all['xsec_sushi_ggh_A_NNLO_x_br_A_bb'])

if 'xsec_sushi_ggh_A_NNLO_x_br_A_tt' in df_all.columns:
    df_all['log_xsec_sushi_ggh_A_NNLO_x_br_A_tt']     = np.log10(df_all['xsec_sushi_ggh_A_NNLO_x_br_A_tt'])

if 'xsec_sushi_ggh_H_NNLO_x_br_H_ZA' in df_all.columns:
    df_all['log_xsec_sushi_ggh_H_NNLO_x_br_H_ZA']     = np.log10(df_all['xsec_sushi_ggh_H_NNLO_x_br_H_ZA'])

# - mA binning

mA_bins     = np.linspace(150, 1000, 18)
mH_bins     = np.linspace(150, 1000, 18)
mA_binlabel = np.convolve(mA_bins, [0.5, 0.5], 'valid')
mH_binlabel = np.convolve(mH_bins, [0.5, 0.5], 'valid')
df_all['mA_bin'] = pd.cut(df_all['mA'], mA_bins, labels=mA_binlabel)
df_all['mH_bin'] = pd.cut(df_all['mH'], mH_bins, labels=mH_binlabel)

df_all['index'] = df_all.index

# - Dataset information

print()
print('---------------------------')
print()
print('Dataset info')
print()

chi2_Tot_min = df_all['chi2_Tot_gfitter'].min()
chi2_Tot_max = df_all['chi2_Tot_gfitter'].max()
chi2_HS_min  = df_all['chi2_HS'].min()
chi2_HS_max  = df_all['chi2_HS'].max()
chi2_ST_gfitter_min = df_all['chi2_ST_gfitter'].min()
chi2_ST_gfitter_max = df_all['chi2_ST_gfitter'].max()

m12_2_min = df_all['m12_2'].min()
m12_2_max = df_all['m12_2'].max()

print('chi2_Tot_min:        {:.3f}'.format( chi2_Tot_min) )
print('chi2_Tot_max:        {:.3f}'.format( chi2_Tot_max) )
print('chi2_HS_min:         {:.3f}'.format( chi2_HS_min) )
print('chi2_HS_max:         {:.3f}'.format( chi2_HS_max) )
print('chi2_ST_gfitter_min: {:.3f}'.format( chi2_ST_gfitter_min) )
print('chi2_ST_gfitter_max: {:.3f}'.format( chi2_ST_gfitter_max) )
print('m12_2_min:           {:.3f}'.format( m12_2_min) )
print('m12_2_max:           {:.3f}'.format( m12_2_max) )

# - Statistics

print('---------------------------')
print('')
print('Statistics')
print('')

sig1 = 0.6827
sig2 = 0.9545
sig3 = 0.9973

chi2_1sig_df2 = stats.chi2.ppf( q=sig1, df=2)
chi2_2sig_df2 = stats.chi2.ppf( q=sig2, df=2)
chi2_3sig_df2 = stats.chi2.ppf( q=sig3, df=2)
chi2_1sig_df4 = stats.chi2.ppf( q=sig1, df=4)
chi2_2sig_df4 = stats.chi2.ppf( q=sig2, df=4)
chi2_3sig_df4 = stats.chi2.ppf( q=sig3, df=4)
chi2_1sig_df5 = stats.chi2.ppf( q=sig1, df=5)
chi2_2sig_df5 = stats.chi2.ppf( q=sig2, df=5)
chi2_3sig_df5 = stats.chi2.ppf( q=sig3, df=5)

print("chi2_1sig_df2 value: {}".format( chi2_1sig_df2 ) )
print("chi2_2sig_df2 value: {}".format( chi2_2sig_df2 ) )
print("chi2_3sig_df2 value: {}".format( chi2_3sig_df2 ) )
print("chi2_1sig_df4 value: {}".format( chi2_1sig_df4 ) )
print("chi2_2sig_df4 value: {}".format( chi2_2sig_df4 ) ) 
print("chi2_3sig_df4 value: {}".format( chi2_3sig_df4 ) ) 
print("chi2_1sig_df5 value: {}".format( chi2_1sig_df5 ) )
print("chi2_2sig_df5 value: {}".format( chi2_2sig_df5 ) ) 
print("chi2_3sig_df5 value: {}".format( chi2_3sig_df5 ) ) 


# - Selection

print()
print('---------------------------')
print()
print('Selection')
print()


constraints = []


per_constraint = 'per_8pi == 1'
bsg_constraint = 'mHc > 580'
hb_constraint = 'tot_hbobs < 1.0'

constraints.append(per_constraint)
constraints.append(bsg_constraint)
constraints.append(hb_constraint)

isSelection = False

if isSelection:

    nConstraints = len(constraints)
    condition_str = ''
    for i, constraint in enumearet(constraints):
        condition_str += constraint
        if i < nConstraints-1:
            condition_str += ' & '
        
    print('Condition: ', selection)
    print()

else:
    print("No further selection.")

#df = df_all.query(selection)
df = df_all

# - Validation

print('---------------------------')
print()
print('Constraints:')
print()
print('Number of points with (sta == 0 | per_4pi == 0 | uni == 0):',  len(df.query('sta == 0 | per_4pi == 0 | uni == 0')) )
print('Number of points with (tot_hbobs > 1.0):', len(df.query('tot_hbobs > 1.0')) )


# - Undersampling

r = df.iloc[::1, :]
print('Number of points after selection:', len(r) )
