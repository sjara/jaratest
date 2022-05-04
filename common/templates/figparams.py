"""
Common parameters for figures related to this study.
"""

from jaratoolbox import colorpalette as cp
import matplotlib

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To render as font rather than outlines

STUDY_NAME = 'YEARstudyname'

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

colors = {}
colors['blueLaser'] = cp.TangoPalette['SkyBlue1']
colors['sound'] = cp.TangoPalette['Butter2']
colors['condition1'] = cp.TangoPalette['ScarletRed1']
colors['condition2'] = cp.TangoPalette['SkyBlue2']

