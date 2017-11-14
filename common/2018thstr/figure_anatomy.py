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

PANELS = [0, 0, 0, 0, 0, 0] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_anatomy' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [7,5] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.05, 0.35, 0.65]   # Horiz position for panel labels
labelPosY = [0.95, 0.45]    # Vert position for panel labels

# Define colors, use figparams
laserColor = figparams.colp['blueLaser']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 3)
gs.update(left=0.15, right=0.98, top=0.95, bottom=0.09, wspace=.1, hspace=0.3)


# -- Panel: Injection method --
axP = plt.subplot(gs[0, 0])
axP.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axP.axis('off')
if PANELS[0]:
    # Plot stuff
    pass


# -- Panel: Cortex detail image--
axP = plt.subplot(gs[0, 1])
axP.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axP.axis('off')
if PANELS[1]:
    # Plot stuff
    pass


# -- Panel: Cortex cell depth histogram --
axP = plt.subplot(gs[0, 2])
axP.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axP.set_xlabel('Cell density')
axP.set_ylabel('Depth (um)')
if PANELS[2]:
    # Plot stuff
    pass


# -- Panel: Overview section with detail boxes --
axP = plt.subplot(gs[1, 0])
axP.annotate('D', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axP.axis('off')
if PANELS[3]:
    # Plot stuff
    pass


# -- Panel: Thalamus detail image --
axP = plt.subplot(gs[1, 1])
axP.annotate('E', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axP.axis('off')
if PANELS[4]:
    # Plot stuff
    pass


# -- Panel: Thalamus cell location histogram --
axP = plt.subplot(gs[1, 2])
axP.annotate('F', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axP.set_xlabel('Location')
axP.set_ylabel('Cell density')
if PANELS[5]:
    # Plot stuff
    pass

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
