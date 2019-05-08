#!/usr/bin/env python


analyses = {
             185 : {'ch': r'$h$ (VBF) $\rightarrow$ V (invisible)', 'analysis' : 'ATLAS-EXOT-2016-37', 'marker' :'o', 'color' : 'forestgreen', 'alpha' : 0.1},
             236 : {'ch': r'VBF $h \rightarrow WW$ ',               'analysis' : 'CMS-PAS-HIG-13-022',  'marker' :'^', 'color' : 'plum',        'alpha' : 0.1},
             303 : {'ch': r'$H \rightarrow VV$',                    'analysis' : '1504.00936 (CMS)',    'marker' :'o', 'color' : 'navy',        'alpha' : 0.1},
             371 : {'ch': r'$h$ combination',                       'analysis' : 'CMS-PAS-HIG-12-045',  'marker' :'P', 'color' : 'gold',        'alpha' : 0.1},
             792 : {'ch': r'$h \rightarrow \tau\tau$',              'analysis' : 'CMS-PAS-HIG-14-029',  'marker' :'P', 'color' : 'navy',        'alpha' : 0.1},
             793 : {'ch': r'$H \rightarrow \tau\tau$',              'analysis' : 'CMS-PAS-HIG-14-029',  'marker' :'P', 'color' : 'navy',        'alpha' : 0.1},
             794 : {'ch': r'$A \rightarrow \tau\tau$',              'analysis' : 'CMS-PAS-HIG-14-029',  'marker' :'P', 'color' : 'navy',        'alpha' : 0.1},
             795 : {'ch': r'$h \rightarrow \tau\tau$',              'analysis' : 'CMS-PAS-HIG-17-020',  'marker' :'P', 'color' : 'navy',        'alpha' : 0.1},
             796 : {'ch': r'$H \rightarrow \tau\tau$',              'analysis' : 'CMS-PAS-HIG-17-020',  'marker' :'P', 'color' : 'navy',        'alpha' : 0.1},
             797 : {'ch': r'$A \rightarrow \tau\tau$',              'analysis' : 'CMS-PAS-HIG-17-020',  'marker' :'P', 'color' : 'navy',        'alpha' : 0.1},
           }

# - In older version of HiggBounds
#analyses = {
#             175 : {'ch': r'$Z h$ / VBF, $h \rightarrow$ invisible', 'analysis' : '1404.1344 (CMS)',     'marker' :'o', 'color' : 'forestgreen', 'alpha' : 0.1},
#             211 : {'ch': r'$h \rightarrow WW$',                     'analysis' : 'ATLAS-CONF-2012-012', 'marker' :'v', 'color' : 'deepskyblue', 'alpha' : 0.1},
#             269 : {'ch': r'$H \rightarrow ZZ \rightarrow 4l$',      'analysis' : 'ATLAS-CONF-2013-013', 'marker' :'o', 'color' : 'navy',        'alpha' : 0.1},
#             277 : {'ch': r'$h \rightarrow ZZ \rightarrow 4l$',      'analysis' : 'CMS-PAS-HIG-13-002',  'marker' :'s', 'color' : 'olivedrab',   'alpha' : 0.1},
#             281 : {'ch': r'$H \rightarrow ZZ \rightarrow 4l$',      'analysis' : 'CMS-PAS-HIG-13-002',  'marker' :'p', 'color' : 'magenta',     'alpha' : 0.1},
#             368 : {'ch': r'$H \rightarrow hh$',                     'analysis' : '1509.04670 (ATLAS)',  'marker' :'H', 'color' : 'red',         'alpha' : 0.3},
#             422 : {'ch': r'$H \rightarrow \gamma \gamma$',          'analysis' : '1407.6583 (ATLAS)',   'marker' :'D', 'color' : 'silver',      'alpha' : 0.4},
#             423 : {'ch': r'$A \rightarrow \gamma \gamma$',          'analysis' : '1407.6583 (ATLAS)',   'marker' :'8', 'color' : 'black',       'alpha' : 0.3},
#             425 : {'ch': r'$h \rightarrow WW$',                     'analysis' : '1507.05930 (ATLAS)',  'marker' :'*', 'color' : 'crimson',     'alpha' : 0.2},
#             553 : {'ch': r'$H \rightarrow \tau \tau$',              'analysis' : 'CMS-HIG-PAS 14-029',  'marker' :'3', 'color' : 'darkorange',  'alpha' : 0.1},
#             554 : {'ch': r'$A \rightarrow \tau \tau$',              'analysis' : 'CMS-HIG-PAS 14-029',  'marker' :'4', 'color' : 'greenyellow', 'alpha' : 0.9},
#           }
