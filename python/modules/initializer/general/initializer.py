#!/usr/bin/env python

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as patches
import matplotlib
import scipy.stats
import util_tools.util_tools as utl
from matplotlib.colors import LinearSegmentedColormap
import matplotlib_utils.cosmetics as mplcosm
import matplotlib_utils.plot_func as mplutils
import scipy

import plotting.plotting as pl
import analysis.analysis as analysis
import analysis.higgsbounds as hb
import jupyter_utils.jupyter_utils as jup

import warnings
warnings.filterwarnings('ignore')

from measurement.autoload import measurement_database
import magellan.config as magconf
import glob

jup.setup_jupyter()
