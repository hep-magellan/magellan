import os
import pandas as pd
import magellan.config as magconf
import numpy as np
from measurement.measurement import Measurement
from measurement.measurement import UpperLimitData

hepdata_limit = os.path.join(magconf.paths['measurements'], 'ATLAS_EXOT_2016_31', './scalar.yaml')

m = Measurement(
                 data        = UpperLimitData.from_hepdatafile(hepdata_limit, independent_variables=['mH']),
                 description = "ATLAS Higgs H -> hh -> bbbb, sqrt(s) = 13 TeV, lumi = 24.3 fb-1",
                 tag         = "ATLAS_EXOT_2016_31",
                 label       = "ATLAS-EXOT-2016-31",
                 process     = r"$H \rightarrow hh \rightarrow bbbb$",
                 factor      = 1.0,
                 observables = {
                                         "xsec_sushi_ggh_H_NNLO_x_br_H_hh_x_br_hh_bbbb":
                                       {"upper_limit" : {"function" : None,
                                                "arguments" : ["mH", "GammaH_div_mH"]}}
                                        },
                 CL          = 0.95,
                 sqrt_s     = 13.0,
                 luminosity = 24.3,
                 url = "https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/EXOT-2016-31/",
                 comment = ""
               ) 

def limit_vs_mass_func(vars, limit_type='limit_exp'):

    interpolation_function = m.data['interpolation'][limit_type]['function']

    if isinstance(vars, pd.DataFrame):
        mass = vars.iloc[:,0]
        GammaH_div_mH = vars.iloc[:,1]
    else:
        mass = vars[0]
        GammaH_div_mH = vars[1]

    val = interpolation_function(mass)/(1000.0)
    val = np.where(GammaH_div_mH > 0.05, np.inf, val)

    return val


m.observables["xsec_sushi_ggh_H_NNLO_x_br_H_hh_x_br_hh_bbbb"]["upper_limit"]["function"] = limit_vs_mass_func
