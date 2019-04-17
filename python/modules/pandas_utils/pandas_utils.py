#!/usr/bin/env python

import os
import pandas as pd

filetype_pd_read_in_func =  {
                              'csv': pd.read_csv,
                              'hdf': pd.read_hdf,
                             }


def auto_detect_file_type_from_path(file_path):

    basename = os.path.basename(file_path)
    basename_splitted = basename.split('.')
    extension = basename_splitted[-1]

    if extension == "dat":
        print('csv file dfetected')
        return "csv"
    elif extension == "csv":
        print('csv file dfetected')
        return "csv"
    elif extension == "hdf":
        print('hdf file dfetected')
        return "hdf"
    elif extension == "h5f":
        print('hdf file dfetected')
        return "hdf"


def df_write_autodetect(df, output_path, *args, **kwargs):

    output_type = auto_detect_file_type_from_path(output_path)

    if output_type == 'csv':
        df.to_csv(args, kwargs)
    elif output_type == 'hdf':
        df.to_hdf(args, kwargs)
   
def df_read_autodetect(input_path, *args, **kwargs):

    input_type = auto_detect_file_type_from_path(input_path)

    df = filetype_pd_read_in_func[input_type](input_path, *args, **kwargs)

    return df
