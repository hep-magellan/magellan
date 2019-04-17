#!/usr/bin/env python

from initializer.general.initializer import *


if jup.in_ipynb():
	# - Auto reload import libraries
	get_ipython().magic('load_ext autoreload')
	get_ipython().magic('autoreload 2')
	
	# - Pandas settings
	pd.options.display.max_seq_items = 2000
	
	# - Inline matplotlib figures
	get_ipython().magic('matplotlib inline')

	print("Setup script loaded.")
	print("Available commands: ")
	print(" - ignore_warnings()")
	print(" - load_mpl_style()")
	print(" - jup.save_to_html()")


def load_mpl_style(style_file):
    style_file_fullpath = os.path.join(ENV_MATPLOTLIB_STYLES_DIR, style_file)
    plt.style.use(style_file_fullpath)


def ignore_warnings():
    import warnings
    warnings.filterwarnings('ignore')
