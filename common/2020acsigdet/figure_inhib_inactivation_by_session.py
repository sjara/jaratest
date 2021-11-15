"""
Plot performance of each ArchT mouse session by session.
"""

import os
import sys
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import matplotlib.transforms
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots

import behaviour_analysis_funcs as bf
import figparams
import studyparams

FIGNAME = 'figure_inhibitory_inactivation'
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 1, 1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
CORRECTED = 0
outputDir = '/tmp/'

figFilename = 'Fig6_inhib_inactivation_by_session'
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [7.5, 4]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.32, 0.67, 0.34, 0.68]  # Horiz position for panel labels
labelPosY = [0.97, 0.60, 0.25]  # Vert position for panel labels

summaryFileName = 'all_behaviour_inhib_inactivation_by_session.npz'

baseColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']
connectLineColour = figparams.colp['connectLine']

lineWidth = figparams.lineWidth
markerSize = figparams.markerSize


dataFullPath = os.path.join(inactDataDir, summaryFileName)
data = np.load(dataFullPath, allow_pickle=True)

dprime = [ data['PVdprimeEachSession'], data['SOMdprimeEachSession'] ]
avgNoLaserdprime = [ data['PVexpNoLaserdprimeAllBands'], data['SOMexpNoLaserdprimeAllBands'] ]
avgLaserdprime = [ data['PVexpLaserdprimeAllBands'], data['SOMexpLaserdprimeAllBands'] ]
eachSessionLabels = data['eachSessionLabels']
laserSessionsInd = list(eachSessionLabels[0]).index('laser')
controlSessionsInd = list(eachSessionLabels[0]).index('control')
laserTrialsInd = list(eachSessionLabels[1]).index('bilateral')
noLaserTrialsInd = list(eachSessionLabels[1]).index('none')
nMice = [len(dprime[0]), len(dprime[1])]

          
fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 1)
gs.update(top=0.94, bottom=0.06, left=0.065, right=0.99, wspace=0.1, hspace=0.4)

cellTypeColours = [PVColour, SOMColour]
wspace = [0.2, 0.5]
#for indCell, cellName in enumerate(['PV','SOM']):
#   gsCell = gs[indCell].subgridspec(1,nMice[indCell])
#sys.exit()

avgLinePosX = 0.3*np.array([-1,1])
avgLineWidth = 4

for indCell, cellName in enumerate(['PV','SOM']):
    gsCell = gs[indCell].subgridspec(1,nMice[indCell],wspace=wspace[indCell])
    #gsCell.update(wspace=wspace[indCell])
    
    for indMouse in range(nMice[indCell]):

        axScatter = plt.subplot(gsCell[0,indMouse])
        #panelLabel = 'D'
        #yLim = [0, 2.2]
        #xTickLabels = ['baseline', 'no AC']
        dataToPlot = dprime[indCell][indMouse][laserSessionsInd]
        nSessions = dataToPlot.shape[0]
        for indSession in range(nSessions):
            plt.plot([0,1], dataToPlot.T, '-', color=figparams.colp['connectLine'])
        plt.plot(np.zeros(nSessions), dataToPlot[:,noLaserTrialsInd], 'o', ms=markerSize, mfc=baseColour, mec=baseColour)
        plt.plot(np.ones(nSessions), dataToPlot[:,laserTrialsInd], 'o', ms=markerSize, mfc='w', mec=cellTypeColours[indCell])

        plt.plot(avgLinePosX, np.tile(avgNoLaserdprime[indCell][indMouse],2), lw=avgLineWidth, color=baseColour)
        plt.plot(avgLinePosX+1, np.tile(avgLaserdprime[indCell][indMouse],2), lw=avgLineWidth, color=cellTypeColours[indCell])
    
        plt.xlim([-0.5, 1.5])
        plt.ylim([-0.2, 2.7])
        axScatter.set_xticks([0,1])
        axScatter.set_xticklabels(['B','M'])
        if indMouse==0:
            plt.ylabel("d'")
        else:
            axScatter.set_yticklabels([])
        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, figparams.fontSizeTicks)
        plt.title(f'{cellName}{indMouse+1}', fontsize=figparams.fontSizeTicks)

        wstat,pVal = stats.wilcoxon(dataToPlot[:,noLaserTrialsInd], dataToPlot[:,laserTrialsInd])
        #wstat,pVal = stats.ttest_rel(dataToPlot[:,noLaserTrialsInd], dataToPlot[:,laserTrialsInd])
        print(f'{cellName}{indMouse+1}: p={pVal:0.3}')
    #break
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
