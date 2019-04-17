#!/usr/bin/env python

import pandas as pd

def save_to_html(notebook, output_html):
    from nbconvert import HTMLExporter
    import codecs
    import nbformat
    exporter = HTMLExporter()
    output_notebook = nbformat.read(notebook, as_version=4)
    output, resources = exporter.from_notebook_node(output_notebook)
    codecs.open(output_html, 'w', encoding='utf-8').write(output)


def in_ipynb():
    try:
        cfg = get_ipython().config 
        return True
    except NameError:
        return False

def ignore_warnings():
    import warnings
    warnings.filterwarnings('ignore')


def setup_jupyter():

    if in_ipynb():

    	# - Auto reload import libraries
    	get_ipython().magic('load_ext autoreload')
    	get_ipython().magic('autoreload 2')
    	
    	# - Pandas settings
    	pd.options.display.max_seq_items = 2000
    	
    	# - Inline matplotlib figures
    	get_ipython().magic('matplotlib inline')
    
    	print("Setup script loaded.")
    	print("Available commands: ")
    	print(" - jup.ignore_warnings()")
    	print(" - jup.save_to_html()")
    
