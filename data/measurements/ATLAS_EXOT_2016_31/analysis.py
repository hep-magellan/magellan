from measurement.measurement import Measurement
import pandas as pd

m = Measurement.from_hepdata(
               hepdata_filename = "scalar.yaml",
               description = "ATLAS Higgs H -> hh -> bbbb, sqrt(s) = 13 TeV, lumi = 24.3 fb-1",
               tag = "ATLAS_EXOT_2016_31",
               label = "ATLAS-EXOT-2016-31",
               process = r"$H \rightarrow hh \rightarrow bbbb$",
               factor = 1.0,
               observables = {
                                       "xsec_sushi_ggh_H_NNLO_x_br_H_hh": {"func" : None,
                                           "args":["mH"]},
                                      },
               sqrt_s = 13.0,
               luminosity = 24.3,
               resonance_search = {"mass_variable": "mH"},
               url = "https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/EXOT-2016-31/",
               comment = "") 

def limit_vs_mass_func(vars, limit_type):

    if isinstance(vars, pd.DataFrame):
        mass = vars.iloc[:,0]
    else:
        mass = vars

    val = m.interpolation[limit_type]['interpolation_func'](mass)/((0.5809**2)* 1000.0)
    return val

m.observables["xsec_sushi_ggh_H_NNLO_x_br_H_hh"]["func"] = limit_vs_mass_func
