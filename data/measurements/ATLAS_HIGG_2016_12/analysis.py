import os
import pandas as pd
import magellan.config as magconf
import numpy as np
from measurement.measurement import Measurement
from measurement.measurement import UpperLimitData

hepdata_limit = os.path.join(magconf.paths['measurements'], 'ATLAS_HIGG_2016_12', './ggF_limit.yaml')


m = Measurement(
               data        = UpperLimitData.from_hepdatafile(hepdata_limit, independent_variables=['mass']),
               description = "ATLAS Higgs H/A -> tautau, sqrt(s) = 13 TeV, lumi = 36 fb-1",
               tag = "ATLAS_HIGG_2016_12",
               label = "ATLAS-HIGG-2016-12",
               process = r"$A/H \rightarrow \tau\tau$",
               factor = 1.0,
               observables = {
                                       "xsec_sushi_ggh_A_NNLO_x_br_A_tautau":
                                       {"upper_limit" : {"function" : None,
                                              "arguments" : ["mA", "GammaA_div_mA"]}
                                       },
                                       "xsec_sushi_ggh_H_NNLO_x_br_H_tautau":
                                       {"upper_limit" : {"function" : None,
                                              "arguments" : ["mH", "GammaH_div_mH"]}
                                       },

                                      },
               CL          = 0.95,
               sqrt_s = 13.0,
               luminosity = 36.0,
               url = "https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/HIGG-2016-12/",
               comment = "") 




def limit_vs_mass_func(vars, limit_type='limit_exp'):

    interpolation_function = m.data['interpolation'][limit_type]['function']

    if isinstance(vars, pd.DataFrame):
        mass = vars.iloc[:,0]
        relwidth = vars.iloc[:,1]
    else:
        mass = vars[0]
        relwidth = vars[1]

    val = interpolation_function(mass)
    val = np.where(relwidth > 0.10, np.inf, val)

    return val

m.observables["xsec_sushi_ggh_A_NNLO_x_br_A_tautau"]["upper_limit"]["function"] = limit_vs_mass_func
m.observables["xsec_sushi_ggh_H_NNLO_x_br_H_tautau"]["upper_limit"]["function"] = limit_vs_mass_func

#m.observables["xsec_sushi_ggh_H_NNLO_x_br_H_hh_x_br_hh_bbbb"]["upper_limit"]["function"] = limit_vs_mass_func
