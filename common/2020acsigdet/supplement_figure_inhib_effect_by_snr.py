import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
import studyparams

FIGNAME = 'figure_inhibitory_inactivation'
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'FigX_inhib_inactivation_by_snr'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [4,4]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.36, 0.66, 0.42]  # Horiz position for panel labels
labelPosY = [0.98, 0.78, 0.48, 0.28]  # Vert position for panel labels

summaryFileName = 'change_behaviour_by_snr_inhib_inactivation.npz'

ExcColour = figparams.colp['excitatoryCell']
PVColour = figparams.colp['PVcell']
SOMColour = figparams.colp['SOMcell']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 1)
gs.update(top=0.95, bottom=0.15, left=0.17, right=0.94, wspace=0.5, hspace=0.3)

# --- summary of change in accuracy during PV or SOM inactivation ---
if PANELS[0]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVdetectDiff = summaryData['PVchangeToneDetect']
    SOMdetectDiff = summaryData['SOMchangeToneDetect']
    possibleSNRs = summaryData['possibleSNRs']

    colours = [PVColour, SOMColour]
    changeData = [PVdetectDiff, SOMdetectDiff]

    axCurves = plt.subplot(gs[0,0])
    xVals = range(len(possibleSNRs))

    plt.plot([-10,10], [0,0], '--', color='0.5')

    for indType, changes in enumerate(changeData):
        for indMouse in range(changes.shape[0]):
            plt.plot(xVals, changes[indMouse,:], '-', color=colours[indType], alpha=0.3)

        median = np.median(changes, axis=0)
        plt.plot(xVals, median, 'o-', color=colours[indType], lw=3, ms=9)

        axCurves.set_xlim(xVals[0]-0.3, xVals[-1]+0.3)
        axCurves.set_xticks(xVals)
        axCurves.set_xticklabels(possibleSNRs)
        axCurves.set_xlabel('SNR (dB)', fontsize=fontSizeLabels)

        axCurves.set_ylim(-40,20)
        axCurves.set_ylabel('Change in accuracy (%)', fontsize=fontSizeLabels)

        extraplots.boxoff(axCurves)
        extraplots.set_ticks_fontsize(axCurves, fontSizeTicks)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
