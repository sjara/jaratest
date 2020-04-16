'''
Common parameters for figures and data related to these figures.
'''

from jaratoolbox import colorpalette as cp
import matplotlib

#plt.rcParams['svg.image_noscale'] = False
matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # So font is selectable in SVG

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16
fontSizeTitles = 12
fontSizeLegend = 10

colp = {}
colp['excitatoryCell'] = 'k'
colp['SOMcell'] = cp.TangoPalette['ScarletRed1']
colp['PVcell'] = cp.TangoPalette['SkyBlue2']

colp['blueLaser'] = '#00FFFF'
colp['greenLaser'] = '#34FF7A'
#colp['sound'] = '#d3d3c2'
#colp['sound'] = '#fcee25'
colp['sound'] = cp.TangoPalette['Butter2']
