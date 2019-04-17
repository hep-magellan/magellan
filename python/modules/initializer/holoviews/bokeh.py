#!/usr/bin/env python

from initializer.holoviews.common import *
import plotting.holoviews as hvplot

hv.notebook_extension('bokeh')
hv.Store.renderers['bokeh'].webgl = True

hvrenderer = hv.renderer('bokeh')

points_opts1 = opts.Points(tools=['lasso_select', 'box_select'],
                           color='navy', selection_color='tomato', nonselection_color='navy', 
                           nonselection_alpha=0.1, alpha=0.50)

layout_shared = opts.Layout(shared_axes=True, shared_datasource=True)
