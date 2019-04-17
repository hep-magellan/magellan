#!/usr/bin/env python

import os
import glob
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
import scipy.stats

import plotting.plotting as pl
import analysis.analysis as analysis
import analysis.higgsbounds as hb
import jupyter_utils.jupyter_utils as jup

import magellan.config as magconf
import mcmc.diagnostics as mcdiag

jup.setup_jupyter()
