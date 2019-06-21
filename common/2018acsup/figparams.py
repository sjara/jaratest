'''
Common parameters for figures and data related to these figures.
'''

from jaratoolbox import colorpalette as cp
import matplotlib
from matplotlib import pyplot as plt

plt.rcParams['svg.image_noscale'] = False
matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # So font is selectable in SVG

STUDY_NAME = '2018acsup'

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16
fontSizeTitles = 12
fontSizeLegend = 10

colp = {}
#colp['excitatoryCell'] = cp.TangoPalette['Chameleon3']
colp['excitatoryCell'] = 'k'
colp['excludedExcitatory'] = cp.TangoPalette['Plum1']

colp['SOMcell'] = cp.TangoPalette['ScarletRed1']
colp['PVcell'] = cp.TangoPalette['SkyBlue2']

colp['blueLaser'] = '#00FFFF'
colp['greenLaser'] = '#34FF7A'
colp['sound'] = '#d3d3c2'
#colp['sound'] = '#fcee25'
#colp['sound'] = cp.TangoPalette['Butter2']



#7570B3 - blupurp
#E7298A  - pink
#C51A8A  - pink
#D95F02  - orange
#BCBD22  - olive
#829910  - olive/citron

