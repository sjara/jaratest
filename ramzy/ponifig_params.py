"""
Common parameters for figures related to this study.
"""

from jaratoolbox import colorpalette as cp
import matplotlib

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To render as font rather than outlines

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

'''
colors = {}
colors['oddball'] = cp.TangoPalette['Aluminium5']
colors['standard'] = cp.TangoPalette['Aluminium3']

colors['blueLaser'] = cp.TangoPalette['SkyBlue1']
colors['sound'] = cp.TangoPalette['Butter2']
colors['condition1'] = cp.TangoPalette['ScarletRed1']
colors['condition2'] = cp.TangoPalette['SkyBlue2']
'''

colorSpikeTemplate1 = 'teal'
colorSpikeTemplate2 = 'olivedrab'
colorVoltageTrace = colorSpikeTemplate1

colorStim = cp.TangoPalette['Butter2']
colors = {'pre': cp.TangoPalette['Aluminium4'],
          'on': cp.TangoPalette['SkyBlue2'],
          'off': cp.TangoPalette['ScarletRed1']}
colorsLight = {k: matplotlib.colors.colorConverter.to_rgba(onecol, alpha=0.5)
               for k,onecol in colors.items()}
colorsLightDark = {'pre': [colorsLight['pre'], colors['pre']],
                   'off': [colorsLight['off'], colors['off']],
                   'on': [colorsLight['on'], colors['on']]}

'''
colorsOdd = {'off':cp.TangoPalette['SkyBlue2'], 'on': cp.TangoPalette['ScarletRed1']}
colorsStd = {k: matplotlib.colors.colorConverter.to_rgba(onecol, alpha=0.5)
             for k,onecol in colorsOdd.items()}
COLORS_EACH_REAGENT = {'pre': ['0.75','0.5'],
                       'off': [colorsStd['off'], colorsOdd['off']],
                       'on': [colorsStd['on'], colorsOdd['on']]}
'''
