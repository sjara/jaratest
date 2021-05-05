'''
Common parameters for figures and data related to these figures.
'''

from jaratoolbox import colorpalette as cp
import matplotlib

#plt.rcParams['svg.image_noscale'] = False
matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # So font is selectable in SVG

fontSizeLabels = 10
fontSizeTicks = 8
fontSizePanel = 14
fontSizeTitles = 10
fontSizeLegend = 8

markerSize = 5
lineWidth = 2

colp = {}
colp['baseline'] = 'k'
colp['SOMmanip'] = cp.TangoPalette['ScarletRed1']
colp['PVmanip'] = cp.TangoPalette['SkyBlue2']

colp['control'] = cp.TangoPalette['Orange1']

colp['connectLine'] = '0.7'
