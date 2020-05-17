'''
Common parameters for figures and data related to this study.
'''

from jaratoolbox import colorpalette as cp
import matplotlib

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To render as font rather than outlines

STUDY_NAME = 'YEARstudyname'

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

colp = {}
colp['blueLaser'] = cp.TangoPalette['SkyBlue1']
colp['sound'] = cp.TangoPalette['Butter2']
colp['condition1'] = cp.TangoPalette['ScarletRed1']
colp['condition2'] = cp.TangoPalette['SkyBlue2']

