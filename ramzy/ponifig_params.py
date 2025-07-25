"""
Common parameters for figures related to this study.
"""

from jaratoolbox import colorpalette as cp
import matplotlib as mpl
import poni_params as studyparams

mpl.rcParams['font.family'] = 'Helvetica'
mpl.rcParams['svg.fonttype'] = 'none'  # To render as font rather than outlines

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

tangomap = []
for num in range(3):
    for key in cp.TangoPalette:
        if str(num+1) in key:
            tangomap.append(cp.TangoPalette[key])

colorStim = cp.TangoPalette['Butter2']
colors = {}
colorsLight = {}
colorsLightDark = {}

SET2_CMAP = mpl.pyplot.get_cmap('Set2')

for sessionType in studyparams.REAGENTS:
    colors[sessionType] = {'pre': cp.TangoPalette['Aluminium4'],
                                'off': cp.TangoPalette['SkyBlue2'],
                                'on': cp.TangoPalette['ScarletRed1']}
    
    for indr,reagent in enumerate(studyparams.REAGENTS[sessionType][1:]):
        colors[sessionType][reagent] = SET2_CMAP(indr)


    colorsLight[sessionType] = {k: mpl.colors.colorConverter.to_rgba(onecol, alpha=0.5) \
                                    for k,onecol in colors[sessionType].items()}

    colorsLightDark[sessionType] = {key: [colorsLight[sessionType][key], colors[sessionType][key]] \
                                    for key in colors[sessionType]}

'''
colorsOdd = {'off':cp.TangoPalette['SkyBlue2'], 'on': cp.TangoPalette['ScarletRed1']}
colorsStd = {k: mpl.colors.colorConverter.to_rgba(onecol, alpha=0.5)
             for k,onecol in colorsOdd.items()}
COLORS_EACH_REAGENT = {'pre': ['0.75','0.5'],
                       'off': [colorsStd['off'], colorsOdd['off']],
                       'on': [colorsStd['on'], colorsOdd['on']]}
'''
