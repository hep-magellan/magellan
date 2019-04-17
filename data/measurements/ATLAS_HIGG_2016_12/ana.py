from measurement.measurement import Measurement
import pandas as pd

m = Measurement.from_hepdata(
               hepdata_filename = "ggF_limit.yaml",
               description = "ATLAS Higgs H/A -> tautau, sqrt(s) = 13 TeV, lumi = 36 fb-1",
               tag = "ATLAS_HIGG_2016_12",
               label = "ATLAS-HIGG-2016-12",
               process = r"$A/H \rightarrow \tau\tau$",
               factor = 1.0,
               observables = {
                                       "xsec_sushi_ggh_A_NNLO_x_br_A_tautau": {"func" : None, "args":["mA"]},
                                       "xsec_sushi_ggh_H_NNLO_x_br_H_tautau": {"func" : None, "args":["mH"]}
                                      },
               type = "upper limit",
               CL = 0.95,
               sqrt_s = 13.0,
               luminosity = 36.0,
               resonance_search = {"mass_variable": "mA"},
               url = "https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/HIGG-2016-12/",
               comment = "") 

def limit_vs_mass_func(vars, limit_type):

    if isinstance(vars, pd.DataFrame):
        mass = vars.iloc[:,0]
    else:
        mass = vars

    val = m.interpolation[limit_type]['interpolation_func'](mass)
    return val

m.observables["xsec_sushi_ggh_A_NNLO_x_br_A_tautau"]["func"] = limit_vs_mass_func
m.observables["xsec_sushi_ggh_H_NNLO_x_br_H_tautau"]["func"] = limit_vs_mass_func
