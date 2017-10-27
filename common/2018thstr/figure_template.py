import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
import figparams
reload(figparams)

FIGNAME = 'figure_name'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_figure_name' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,5] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.07, 0.36, 0.7]   # Horiz position for panel labels
labelPosY = [0.9, 0.48]    # Vert position for panel labels

# Define colors, use figparams
laserColor = figparams.colp['blueLaser']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 1)
gs.update(left=0.15, right=0.98, top=0.95, bottom=0.05, wspace=.1, hspace=0.3)

# -- Panel: name of panel --
ax1 = plt.subplot(gs[0, 0])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')

if PANELS[0]:
    # Plot stuff
    pass

# -- Panel: name of next panel --
ax2 = plt.subplot(gs[1, 0])
ax2.annotate('B', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')

if PANELS[1]:
    # Plot stuff
    pass

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
