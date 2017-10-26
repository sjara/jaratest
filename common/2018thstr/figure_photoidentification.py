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
figFilename = 'plots_photoidentification' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [7,5] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.07, 0.40]   # Horiz position for panel labels
labelPosY = [0.9, 0.65, 0.42, 0.19]    # Vert position for panel labels

# Define colors, use figparams
laserColor = figparams.colp['blueLaser']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(8, 5)
gs.update(left=0.15, right=0.98, top=0.95, bottom=0.1, wspace=.1, hspace=0.3)

# -- Panel: Cortex recording cartoon --
axP = plt.subplot(gs[0:4, 0:2])
axP.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axP.axis('off')
if PANELS[0]:
    # Plot stuff
    pass

# -- Panel: Cortex direct cell and waveform --
axPraster = plt.subplot(gs[0, 2:4])
axPraster.axis('off')
axPpsth = plt.subplot(gs[1, 2:4])
axP.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
axPwaveform = plt.subplot(gs[0:2, 4])
axPwaveform.axis('off')
if PANELS[1]:
    # Plot stuff
    pass

# -- Panel: Cortex indirect cell and waveform--
axPraster = plt.subplot(gs[2, 2:4])
axPraster.axis('off')
axPpsth = plt.subplot(gs[3, 2:4])
axP.annotate('C', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
axPwaveform = plt.subplot(gs[2:4, 4])
axPwaveform.axis('off')
if PANELS[1]:
    # Plot stuff
    pass

# -- Panel: Thalamus recording cartoon --
axP = plt.subplot(gs[4:8, 0:2])
axP.annotate('D', xy=(labelPosX[0],labelPosY[2]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axP.axis('off')
if PANELS[0]:
    # Plot stuff
    pass

# -- Panel: Thalamus direct cell and waveform --
axPraster = plt.subplot(gs[4, 2:4])
axPraster.axis('off')
axPpsth = plt.subplot(gs[5, 2:4])
axP.annotate('E', xy=(labelPosX[1],labelPosY[2]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
axPwaveform = plt.subplot(gs[4:6, 4])
axPwaveform.axis('off')
if PANELS[1]:
    # Plot stuff
    pass

# -- Panel: Thalamus indirect cell and waveform--
axPraster = plt.subplot(gs[6, 2:4])
axPraster.axis('off')
axPpsth = plt.subplot(gs[7, 2:4])
axPpsth.set_xlabel('Time from laser onset (s)')
axP.annotate('F', xy=(labelPosX[1],labelPosY[3]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
axPwaveform = plt.subplot(gs[6:8, 4])
axPwaveform.axis('off')
if PANELS[1]:
    # Plot stuff
    pass
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
