'''
Common parameters for figures and data related to these figures.
'''

import os
from jaratoolbox import colorpalette as cp
from jaratoolbox import settings
import matplotlib
from matplotlib import pyplot as plt

# plt.rcParams['svg.image_noscale'] = False
matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # So font is selectable in SVG

STUDY_NAME = '2018thstr'
# FIGURE_OUTPUT_DIR = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'output')
FIGURE_OUTPUT_DIR = '/tmp/'

fontSizeLabels = 7
fontSizeTicks = 6
fontSizePanel = 9
fontSizeTitles = 12
fontSizeNS = 10
fontSizeStars = 9
starHeightFactor = 0.2
starGapFactor = 0.3
starYfactor = 0.1

dotEdgeColor = '0.5'
rasterMS = 1

colp = {}
colp['blueLaser'] = cp.TangoPalette['SkyBlue1']
colp['frontStrColor'] = cp.TangoPalette['Chameleon3']
colp['backStrColor'] = cp.TangoPalette['Plum2']

# colp['sound'] = cp.TangoPalette['Butter2']
colp['sound'] = cp.TangoPalette['Orange1']

colp['MidFreqR'] = cp.TangoPalette['ScarletRed1']
colp['MidFreqL'] = cp.TangoPalette['Chameleon3']

#colp['muscimol'] = cp.TangoPalette['Orange2']
colp['muscimol'] = cp.TangoPalette['Chocolate2']

#colp['stimLeft'] = cp.TangoPalette['ScarletRed1']
#colp['stimRight'] = cp.TangoPalette['Chameleon3']
colp['stimLeft'] = cp.TangoPalette['Orange2']
colp['stimRight'] = '#829910'

colp['thalColor'] = cp.TangoPalette['SkyBlue2']
colp['acColor'] = cp.TangoPalette['ScarletRed2']


#7570B3 - blupurp
#E7298A  - pink
#C51A8A  - pink
#D95F02  - orange
#BCBD22  - olive
#829910  - olive/citron

'''
# To avoid converting text to paths
matplotlib.rcParams['svg.fonttype'] = 'none'

matplotlib.rcParams['axes.color_cycle'] = ???

colp = {}
colp['LowFreq'] = cp.TangoPalette['Orange2']

colp['HighFreq'] = cp.TangoPalette['SkyBlue2']


'''
