'''
Common parameters for figures and data related to these figures.
'''

from jaratoolbox import colorpalette as cp
import matplotlib

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # So font is selectable in SVG

STUDY_NAME = '2016astr'

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

colp = {}
colp['blueLaser'] = cp.TangoPalette['SkyBlue1']
colp['MidFreqR'] = cp.TangoPalette['Chameleon3']
colp['MidFreqL'] = cp.TangoPalette['ScarletRed1']


'''
# To avoid converting text to paths
matplotlib.rcParams['svg.fonttype'] = 'none'

matplotlib.rcParams['axes.color_cycle'] = ???

colp = {}
colp['LowFreq'] = cp.TangoPalette['Orange2']

colp['HighFreq'] = cp.TangoPalette['SkyBlue2']


'''
