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
fontSizeLabels = 10
fontSizeTicks = 9
fontSizePanel = 12
fontSizeTitles = 12
fontSizeNS = 10
fontSizeStars = 9

# Significance star placement  
starHeightFactor = 0.2
starGapFactor = 0.3
starYfactor = 0.1

dotEdgeColor = '0.5' 

rasterMarkerSize = 3 # Raster maerker size

colors = {} # Color library used in figures 

colors['soundStim'] = cp.TangoPalette['Butter2']
colors['blueLaser'] = '#00DDDD'  #cp.TangoPalette['SkyBlue1']
colors['D1'] = cp.TangoPalette['SkyBlue2']
colors['ND1'] = cp.TangoPalette['ScarletRed1']

