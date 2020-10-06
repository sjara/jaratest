'''
Common parameters for figures and data related to these figures.
'''

import os
from jaratoolbox import colorpalette as cp
from jaratoolbox import settings
import matplotlib
from matplotlib import pyplot as plt
import studyparams

# Font settings 
# plt.rcParams['svg.image_noscale'] = False
matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # So font is selectable in SVG

FIGURE_OUTPUT_DIR = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 'output') # Where figures are saved 

# Font size settings 
fontSizeLabels = 7
fontSizeTicks = 6
fontSizePanel = 9
fontSizeTitles = 12
fontSizeNS = 10
fontSizeStars = 9

# Significance star placement  
starHeightFactor = 0.2
starGapFactor = 0.3
starYfactor = 0.1

dotEdgeColor = '0.5' 

rasterMS = 1 # Raster plot transparency

colors = {} # Color library used in figures 

colors['blueLaser'] = cp.TangoPalette['SkyBlue1']
colors['D1'] = cp.TangoPalette['SkyBlue2']
colors['nD1'] = cp.TangoPalette['ScarletRed1']

