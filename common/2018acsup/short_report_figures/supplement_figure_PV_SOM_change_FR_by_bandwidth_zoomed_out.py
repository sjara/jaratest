import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors
import matplotlib.patches as patches

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots


import figparams


dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'figure_inhibitory_cell_inactivation') #use data for figure 2

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'SuppFig9_inactivation_change_FR_by_bandwidth_zoomed_out' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [4,4] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.2, 0.4, 0.59, 0.78]   # Horiz position for panel labels
labelPosY = [0.96, 0.48]    # Vert position for panel labels


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,1)
gs.update(top=0.95, bottom=0.18, left=0.15, right=0.95, wspace=0.6, hspace=0.2)


summaryFileName = 'all_inactivated_cells_stats.npz'

# --- zoomed out version of last panel of figure 2 ---
summaryDataFullPath = os.path.join(dataDir,summaryFileName)
summaryData = np.load(summaryDataFullPath)

PVpeakChangeFR = summaryData['fitPVpeakChangeFRNoZero']
PVWNChangeFR = summaryData['fitPVWNChangeFRNoZero']

SOMpeakChangeFR = summaryData['fitSOMpeakChangeFRNoZero']
SOMWNChangeFR = summaryData['fitSOMWNChangeFRNoZero']

PVpeakChange = summaryData['fitMeanPVpeakChangeNoZero']
PVWNChange = summaryData['fitMeanPVWNChangeNoZero']

semPVpeakChange = summaryData['fitSemPVpeakChangeNoZero']
semPVWNChange = summaryData['fitSemPVWNChangeNoZero']

SOMpeakChange = summaryData['fitMeanSOMpeakChangeNoZero']
SOMWNChange = summaryData['fitMeanSOMWNChangeNoZero']

semSOMpeakChange = summaryData['fitSemSOMpeakChangeNoZero']
semSOMWNChange = summaryData['fitSemSOMWNChangeNoZero']

#panelLabel = 'a'

PVcolour = figparams.colp['PVcell']
SOMcolour = figparams.colp['SOMcell']
cellTypeColours = [PVcolour, SOMcolour]

axScatter = plt.subplot(gs[0,0])

plt.hold(True)
plt.plot([-20,30],[-20,30], 'k--')
l2, = plt.plot(SOMpeakChangeFR,SOMWNChangeFR, 'o', color=SOMcolour, mec='none', ms=4)
l1, = plt.plot(PVpeakChangeFR,PVWNChangeFR, 'o', color=PVcolour, mec='none', ms=4)

# make box around what's shown in fig 2
plt.plot([-5,-5,8,8,-5],[-5,8,8,-5,-5],'-', color='0.75')

plt.xlim(-15,25)
plt.ylim(-15,25)

plt.ylabel('Change in response to WN (spk/s)',fontsize=fontSizeLabels)
plt.xlabel('Change in response to \n preferred bandwidth (spk/s)',fontsize=fontSizeLabels)

plt.legend([l1,l2], ['no PV+', 'no SOM+'], loc='upper left', fontsize=fontSizeLabels, numpoints=1, handlelength=0.3, markerscale=1.5)
# axScatter.annotate(panelLabel, xy=(labelPosX[4],labelPosY[1]), xycoords='figure fraction',
#                      fontsize=fontSizePanel, fontweight='bold')
extraplots.boxoff(axScatter)
    
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)