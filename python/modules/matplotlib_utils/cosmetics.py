#!/usr/bin/env python

import matplotlib.pyplot as plt
import os

ENV_MATPLOTLIB_STYLES_DIR = os.environ['ENV_MATPLOTLIB_STYLES_DIR']

def load_mpl_style(style_file):
    style_file_fullpath = os.path.join(ENV_MATPLOTLIB_STYLES_DIR, style_file)
    plt.style.use(style_file_fullpath)
