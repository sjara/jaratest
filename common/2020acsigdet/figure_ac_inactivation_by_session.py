"""
Plot performance of each PV-ChR2 mouse session by session.
"""

import os
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

FIGNAME = 'figure_ac_inactivation'
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 1, 1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
CORRECTED = 0
outputDir = '/tmp/'

figFilename = 'Fig3_ac_inactivation_by_session'
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [7.5, 2.5]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.32, 0.67, 0.34, 0.68]  # Horiz position for panel labels
labelPosY = [0.97, 0.60, 0.25]  # Vert position for panel labels

summaryFileName = 'all_behaviour_ac_inactivation_by_session.npz'

baseColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
connectLineColour = figparams.colp['connectLine']

lineWidth = figparams.lineWidth
markerSize = figparams.markerSize+1


dataFullPath = os.path.join(inactDataDir, summaryFileName)
data = np.load(dataFullPath, allow_pickle=True)

dprime = data['dprimeEachSession']
avgNoLaserdprime = data['expNoLaserdprimeAllBandsAllBand']
avgLaserdprime = data['expLaserdprimeAllBands']
eachSessionLabels = data['eachSessionLabels']
laserSessionsInd = list(eachSessionLabels[0]).index('laser')
controlSessionsInd = list(eachSessionLabels[0]).index('control')
laserTrialsInd = list(eachSessionLabels[1]).index('bilateral')
noLaserTrialsInd = list(eachSessionLabels[1]).index('none')
nMice = len(dprime)

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, nMice)
gs.update(top=0.92, bottom=0.1, left=0.065, right=0.99, wspace=0.1, hspace=0.25)

avgLinePosX = 0.3*np.array([-1,1])
avgLineWidth = 4

for indMouse in range(nMice):
    axScatter = plt.subplot(gs[0,indMouse])
    #panelLabel = 'D'
    #yLim = [0, 2.2]
    #xTickLabels = ['baseline', 'no AC']
    dataToPlot = dprime[indMouse][laserSessionsInd]
    nSessions = dataToPlot.shape[0]
    for indSession in range(nSessions):
        plt.plot([0,1], dataToPlot.T, '-', color=figparams.colp['connectLine'])
    plt.plot(np.zeros(nSessions), dataToPlot[:,noLaserTrialsInd], 'o', ms=markerSize, mfc=baseColour, mec='none')
    plt.plot(np.ones(nSessions), dataToPlot[:,laserTrialsInd], 'o', ms=markerSize, mfc=PVColour, mec='none')

    plt.plot(avgLinePosX, np.tile(avgNoLaserdprime[indMouse],2), lw=avgLineWidth, color=baseColour)
    plt.plot(avgLinePosX+1, np.tile(avgLaserdprime[indMouse],2), lw=avgLineWidth, color=PVColour)
    
    plt.xlim([-0.5, 1.5])
    plt.ylim([-0.2, 2.5])
    axScatter.set_xticks([0,1])
    axScatter.set_xticklabels(['base','no AC'])
    if indMouse==0:
        plt.ylabel("d'")
    else:
        axScatter.set_yticklabels([])
    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, figparams.fontSizeTicks)
    plt.title(f'M{indMouse+1}', fontsize=figparams.fontSizeTicks) 

    wstat,pVal = stats.wilcoxon(dataToPlot[:,noLaserTrialsInd], dataToPlot[:,laserTrialsInd])
    print(f'M{indMouse+1}: p={pVal:0.3}')
   
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
