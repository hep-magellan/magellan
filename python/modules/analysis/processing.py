#!/usr/bin/env python

import time
import os
from glob import glob
import pandas as pd
import h5py
import numpy as np


def append_chi2_HS_ST( in_fname, out_fname, out_dsname, out_format,  compression, pytables_format='table'):

    chi2_HS_ref_file  = '/scratch/de3u14/2HDM/2HDM-PyPScan/analysis/auxiliary/chi2_HS_matrix/chi2HS_reference.dat'
    form              = 'table'
    compr             = 'zlib'

    ####################
    ### --- Data --- ###
    ####################
     
    print('Reading in file(s) {}...'.format(in_fname) )

    ts = time.time()
    df_orig = pd.read_csv(in_fname, delimiter=r"\s+")
    te = time.time()
    dt = (te-ts)/60
    print('Read in took {} minutes'.format( dt ))



#    pd.set_option('precision', 4)
#    pd.set_option('chop_threshold', .05)
        
    print( 'Number of points: {}'.format( len(df_orig) ) )


    # - chi2_HS lookup
    df_chi2_HS = pd.read_csv( chi2_HS_ref_file, delimiter=r"\s+")
    
    ##################
    
#    cba_nBins    = 41
#    cba_Min      = -1.0
#    cba_binWidth = 0.05
#    
#    tb_nBins     = 39
#    tb_Min       = 1.5
#    tb_binWidth  = 0.5
#    
#    cba_bin = lambda cba: math.floor( (cba - cba_Min) /cba_binWidth)
#    tb_bin  = lambda tb: math.floor( (tb - tb_Min) /tb_binWidth)
#    
#    chi2_HS = np.genfromtxt( chi2_HS_ref_file, delimiter=None, skip_header=0, skip_footer=0, names=True )
#    lu_chi2_HS = np.resize(chi2_HS, (cba_nBins,tb_nBins) )
    
#    print('Binning fuction tests:')
#    print("cba_bin(-1.00): ", cba_bin(-1.00))
#    print('lu_chi2_HS', lu_chi2_HS )
#    print("lu_chi2_HS['chi2_HS'][ cba_bin( 0.01)  ][ tb_bin( 10.0) ]: ", lu_chi2_HS['chi2_HS'][ cba_bin( 0.01)  ][ tb_bin( 10.0) ] )
        
#    def get_chi2_HS( row ):
#        return lu_chi2_HS['chi2_HS'][ cba_bin( row['cba'] )][ tb_bin( row['tb'] )]
    
    
    ##########################
    ### --- Processing --- ###
    ##########################
    
    print('Appending with chi2_ST...')
    ts = time.time()
    df_orig['chi2_ST']  = Calc_chi2_ST( df_orig['S'], df_orig['T'] )
    te = time.time()
    dt = (te-ts)/60
    print('Appending with chi2_ST took {} minutes'.format( dt ))

    print('Appending with chi2_HS...')
    ts = time.time()
    df_orig = df_orig.merge( df_chi2_HS, on=['cba', 'tb'] )
    te = time.time()
    dt = (te-ts)/60

    print('Appending with chi2_HS took {} minutes'.format( dt ))

    ts = time.time()
    df_orig['chi2_Tot'] = (df_orig['chi2_ST'] + df_orig['chi2_HS'])
    te = time.time()
    dt = (te-ts)/60

    print('Summing chi2 s {} minutes'.format( dt ))

    ######################
    ### --- Output --- ###
    ######################
    
    print('Creating file {}...'.format(out_fname) )

    ts = time.time()
    if out_format == 'ascii':
        df_orig.to_csv( out_fname, sep=r" ", index=False )
    elif out_format == 'hdf':
        df_orig.to_hdf( out_fname, key=out_dsname, format=pytables_format, complib=compression )

    te = time.time()
    dt = (te-ts)/60
    print('Writing files took {} minutes'.format( dt ))

def append_chi2_ST( in_fname, out_fname, out_dsname, out_format,  compression, pytables_format='table'):

    form              = 'table'
    compr             = 'zlib'

    ####################
    ### --- Data --- ###
    ####################
     
    print('Reading in file(s) {}...'.format(in_fname) )

    ts = time.time()
    df_orig = pd.read_csv(in_fname, delimiter=r"\s+")
    te = time.time()
    dt = (te-ts)/60
    print('Read in took {} minutes'.format( dt ))


#    pd.set_option('precision', 4)
#    pd.set_option('chop_threshold', .05)
        
    print( 'Number of points: {}'.format( len(df_orig) ) )

    ##################
    
    ##########################
    ### --- Processing --- ###
    ##########################
    
    print('Appending with chi2_ST...')
    ts = time.time()
    df_orig['chi2_ST']  = Calc_chi2_ST( df_orig['S'], df_orig['T'] )
    te = time.time()
    dt = (te-ts)/60
    print('Appending with chi2_ST took {} minutes'.format( dt ))

    ts = time.time()
    df_orig['chi2_Tot'] = (df_orig['chi2_ST'] + df_orig['chi2_HS'])
    te = time.time()
    dt = (te-ts)/60

    print('Summing chi2 s {} minutes'.format( dt ))

    ######################
    ### --- Output --- ###
    ######################
    
    print('Creating file {}...'.format(out_fname) )

    ts = time.time()
    if out_format == 'ascii':
        df_orig.to_csv( out_fname, sep=r" ", index=False )
    elif out_format == 'hdf':
        df_orig.to_hdf( out_fname, key=out_dsname, format=pytables_format, complib=compression )

    te = time.time()
    dt = (te-ts)/60
    print('Writing files took {} minutes'.format( dt ))


##############################################################################################
def ascii_to_hdf5_append_with_chi2_ST( in_fname, out_fname, out_dsname, compression, chunksize, pytables_format='table'):

    print('Reading in file(s) {}...'.format(in_fname) )
    
    ts = time.time()
    #chunks = pd.read_table(in_fname, delimiter=r"\s+", chunksize=10*10**6)
    #chunks = pd.read_table(in_fname, delimiter=r"\s+", chunksize=10**7)
    chunks = pd.read_table(in_fname, delimiter=r"\s+", chunksize=chunksize)
    
    print('Chunk size: ', chunks.chunksize )
    te = time.time()
    dt = (te-ts)
    print('TextFileReader setup took {:.1} seconds'.format( dt ))
    
    # - Creating HDFStore
    hdf_out = pd.HDFStore(out_fname, 'w', complib=compression, format=pytables_format)
    
    tot_ts = time.time()
    for i, df_chunk in enumerate(chunks):
    
        print('\n#############\nAt chunk # {}'.format( i ) )
        print('Appending with chi2_ST...')
        ts = time.time()
        df_chunk['chi2_ST_gfitter']  = Calc_chi2_ST( df_chunk['S'], df_chunk['T'], 'gfitter' )
        df_chunk['chi2_ST_hepfit']   = Calc_chi2_ST( df_chunk['S'], df_chunk['T'], 'hepfit' )
        te = time.time()
        dt = (te-ts)
        print('Appending with chi2_ST took {:.1f} seconds'.format( dt ))
        
        ts = time.time()
        df_chunk['chi2_Tot_gfitter'] = (df_chunk['chi2_ST_gfitter'] + df_chunk['chi2_HS'])
        df_chunk['chi2_Tot_hepfit']  = (df_chunk['chi2_ST_hepfit'] + df_chunk['chi2_HS'])
        te = time.time()
        dt = (te-ts)
        print('Appending with chi2_Tot took {:.1f} seconds'.format( dt ))
    
        ts = time.time()
        hdf_out.append('THDM_type2', df_chunk, index=False)
        te = time.time()
        dt = (te-ts)
        print('Storing chunk to hdf took {:.1f} seconds'.format( dt ))
    
    tot_te = time.time()
    tot_dt = (tot_te-tot_ts)/60
    print('\nTotal runtime: {:.1f} min'.format( tot_dt ))
    
    hdf_out_fname.close()



###############################

def ASCII_to_pd_h5f( input, output, out_ds_name, form, compr ):

    import pandas as pd

    start = time.time()
    all_files = glob( input )
    print('Input:\n', all_files)
    
    print('Reading in file(s) {}...'.format(input) )
    df_from_each_file = (pd.read_csv(f, delimiter=r"\s+") for f in all_files)
    
    print( 'Concatenating...' )
    df = pd.concat(df_from_each_file, ignore_index=True)
    
    print('Creating file {}...'.format(output) )
    df.to_hdf( output, key=out_ds_name, format=form, complib=compr )
    
    print( 'Finished.' )
    
    #####################
    ### --- Stats --- ###
    #####################
    
    input_size  = os.path.getsize( input  )/1024/1024
    output_size = os.path.getsize( output )/1024/1024
    
    end = time.time()
    elapsed = end-start
    
    print('Conversion time')
    print('{:.0f}s.'.format(elapsed))
    print('Size')
    print('input -> output')
    print('{:.0f} MB -> {:.0f} MB'.format( input_size, output_size))


def ASCII_to_h5py_h5f( input, output, out_ds_name, compr):

    start = time.time()
    
    all_files = glob( input )
    print('Input:\n', all_files)
    
    print('Reading in file(s) {}...'.format(input) )
    arrays = [ np.genfromtxt( f, delimiter=None, skip_header=0, skip_footer=0, names=True ) for f in all_files ]
    
    print( 'Concatenating...' )
    ds = np.concatenate(arrays)
    
    h5f = h5py.File( output, 'w')
    
    print('Creating file {}'.format(output) )
    data_h5f = h5f.create_dataset( out_ds_name, data=ds, compression=compr)
    
    h5f.close()
    print( 'Finished.' )
    
    #####################
    ### --- Stats --- ###
    #####################
    
    input_size  = os.path.getsize( input  )/1024/1024
    output_size = os.path.getsize( output )/1024/1024
    
    end = time.time()
    elapsed = end-start
    
    print('Conversion time')
    print('{:.0f}s.'.format(elapsed))
    print('Size')
    print('input -> output')
    print('{:.0f} MB -> {:.0f} MB'.format( input_size, output_size))


def drop_items_at_random(df, nptstokeep):

    dfr = df.copy()

    nelements = len(dfr)

    indeces = dfr.index.tolist()

    ndrops = nelements - nptstokeep
    print("Dropping {} points at random from the dataframe".format(ndrops))
    if ndrops > 0:
        drop_indices = np.random.choice(indeces, ndrops, replace=False)
        dfr = dfr.drop(drop_indices)
    print("Number of points left: {}".format(len(dfr)))

    return dfr


def drop_items_from_bins(df, var, nptstokeep):

    dfr = df.copy()
    bins = np.sort(dfr[var].unique())

    for bin in bins:
        indeces = dfr.index[dfr[var] == bin].tolist()
        nelements = len(indeces)

        ndrops = nelements - nptstokeep
        print("var: {} bin: {} ndrops: {}".format(var, bin, ndrops))
        if ndrops > 0:
            drop_indices = np.random.choice(indeces, ndrops, replace=False)
            dfr = dfr.drop(drop_indices)

    return dfr


def drop_items_from_bins_symmetric_khdd(df, var, nptstokeep):

    dfr = df.copy()
    bins = np.sort(dfr[var].unique())

    for bin in bins:

        indeces_al = dfr.index[(dfr[var] == bin) & (dfr['k_hdd'] > 0.0)].tolist()
        indeces_ws = dfr.index[(dfr[var] == bin) & (dfr['k_hdd'] < 0.0)].tolist()
        nelements_al = len(indeces_al)
        nelements_ws = len(indeces_ws)

        ndrops_al = nelements_al - nptstokeep
        ndrops_ws = nelements_ws - nptstokeep

        if ndrops_al > 0:
            drop_indices_al = np.random.choice(indeces_al, ndrops_al, replace=False)
            dfr = dfr.drop(drop_indices_al)
            print("var: {} bin: {} alignment ndrops: {}".format(var, bin, ndrops_al))
        if ndrops_ws > 0:
            drop_indices_ws = np.random.choice(indeces_ws, ndrops_ws, replace=False)
            dfr = dfr.drop(drop_indices_ws)
            print("var: {} bin: {} wrongsign ndrops: {}".format(var, bin, ndrops_ws))

    return dfr


def get_alignment_wrongsign(df):
    alignment = df.query('k_hdd < 0.0')
    wrongsign = df.query('k_hdd > 0.0')

    return alignment, wrongsign


def get_alignment_wrongsign_drop_pts(df, nptstokeep=2000):

    alignment, wrongsign = get_alignment_wrongsign(df)
    
    print("Alignment")
    alr = drop_items_at_random(alignment, nptstokeep=nptstokeep)

    print("Wrong-sign")
    wsr = drop_items_at_random(wrongsign, nptstokeep=nptstokeep)

    return alr, wsr
