"""
Plot responses to oddball and standard before and after DOI injection.

Based on create_oddball_figures.py by Max Horrocks.
"""

import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
#sys.path.append('/home/jarauser/src/jaratest/maxh')
#sys.path.append('C:/Users/mdhor/Documents/GitHub/jaratest/maxh')
import oddball_analysis_functions as odbl
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import colorpalette as cp


SAVE_FIGURE = 1

stimDuration = 0.1 ### THIS SHOULD NOT BE HARDCODED!

timeRangePlot = [-0.3, 0.45]
timeRangeStim = [0.015, 0.115]
timeRangeBaseline = [-0.2, 0]
baselineDuration = timeRangeBaseline[1] - timeRangeBaseline[0]
stimDuration = timeRangeStim[1] - timeRangeStim[0]

colorStim = cp.TangoPalette['Butter3']
colorsOdd = {'saline':cp.TangoPalette['SkyBlue2'], 'doi': cp.TangoPalette['ScarletRed1']}
colorsStd = {k: matplotlib.colors.colorConverter.to_rgba(onecol, alpha=0.5)
             for k,onecol in colorsOdd.items()}
colorsEachCond = {'saline': [colorsStd['saline'], colorsOdd['saline']],
                  'doi': [colorsStd['doi'], colorsOdd['doi']]}

binWidth = 0.010
timeVec = np.arange(timeRangePlot[0],timeRangePlot[-1],binWidth)

oddballSessions = ('FM_Up', 'FM_Down')
reagents = ('saline', 'doi')


smoothWinSizePsth = 2 
lwPsth = 2.5
downsampleFactorPsth = 1

# Raster plot of high frequency
#colorsEachCond = ['#39b5c4', '#f04158']
highFreqLabels = ('Standard', "Oddball")


subject = 'acid006'

inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')

celldb = celldatabase.generate_cell_database(inforecFile)
dbPath = os.path.join(settings.DATABASE_PATH ,f'celldb_{subject}.h5')


# Add info for loading a specific cell.
cellDict = {'subject' : 'acid006',
            'date' : '2023-03-22',
            'pdepth' : 3000,
            'egroup' : 0,
            'cluster' : 135}

cellInd, dbRow = celldatabase.find_cell(celldb, **cellDict)
oneCell = ephyscore.Cell(dbRow)


def plot_stim(yLims, stimDuration, stimLineWidth=6, stimColor='#edd400'):
    # -- Plot the stimulus --
    yPos = 1.0*yLims[-1] + 0.075*(yLims[-1]-yLims[0])
    pstim = plt.plot([0, stimDuration], 2*[yPos], lw=stimLineWidth, color=stimColor,
                     clip_on=False, solid_capstyle='butt')
    return pstim[0]


#fig = plt.figure()
fig = plt.gcf()
fig.clf()
gsMain = gs.GridSpec(2, 2, fig)
gsMain.update(top=0.92, bottom=0.14, left=0.09, right=0.99, wspace=0.3, hspace=0.075)


if oneCell.get_session_inds(f'salineFM_Up') != []:
        (combinedSpikeTimesDown, combinedSpikeTimesUp, combinedIndexLimitsDown, combinedIndexLimitsUp,
         combinedTrialsDown, combinedTrialsUp, spikeCountMatDown, spikeCountMatUp) = \
                 odbl.combine_sessions(oneCell, timeRangePlot, 'salineFM_Down', 'salineFM_Up', timeVec)
        
        ax1 = plt.subplot(gsMain[0])
        # plt.xlabel('Time (s)')
        #plt.ylabel('Trials')
        plt.title(f'Saline', fontweight='bold', fontsize=14)
        ax1.tick_params(labelbottom=False) 
        pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesUp, combinedIndexLimitsUp,
                                                       timeRangePlot, combinedTrialsUp,
                                                       colorsEachCond['saline'],
                                                       labels= highFreqLabels)
        for p in pRaster:
            p.set_markersize(2)


        ax2 = plt.subplot(gsMain[2], sharex=ax1)    
        psthSaline = extraplots.plot_psth(spikeCountMatUp/binWidth, smoothWinSizePsth, timeVec,
                                          combinedTrialsUp, colorsEachCond['saline'], linestyle=None,
                                          linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time (s)')
        plt.ylabel('Firing rate (spk/s)')
        #plt.title(f'saline FM_UP')
        extraplots.boxoff(ax2)
        #plt.legend(['Standard', 'Oddball'], loc='upper left', handlelength=1.5)
        plt.legend(psthSaline[::-1],['Oddball', 'Standard'], loc='upper left', handlelength=1.5)

        PSTHyLims = plt.ylim()
        plot_stim(PSTHyLims, stimDuration)

        
        (combinedSpikeTimesDown, combinedSpikeTimesUp, combinedIndexLimitsDown, combinedIndexLimitsUp,
         combinedTrialsDown, combinedTrialsUp, spikeCountMatDown, spikeCountMatUp) = \
                 odbl.combine_sessions(oneCell, timeRangePlot, 'doiFM_Down', 'doiFM_Up', timeVec)
        
        ax3 = plt.subplot(gsMain[1])
        # plt.xlabel('Time (s)')
        #plt.ylabel('Trials')
        plt.title(f'DOI', fontweight='bold', fontsize=14)
        ax3.tick_params(labelbottom=False) 
        pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesUp, combinedIndexLimitsUp,
                                                       timeRangePlot, combinedTrialsUp,
                                                       colorsEachCond['doi'], labels= highFreqLabels)
        for p in pRaster:
            p.set_markersize(2)

        ax4 = plt.subplot(gsMain[3], sharex=ax2)    
        psthDOI = extraplots.plot_psth(spikeCountMatUp/binWidth, smoothWinSizePsth, timeVec,
                                       combinedTrialsUp, colorsEachCond['doi'], linestyle=None,
                                       linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time (s)')
        plt.ylabel('Firing rate (spk/s)')
        #plt.title(f'DOI FM_UP')
        extraplots.boxoff(ax4)
        plt.legend(psthDOI[::-1],['Oddball', 'Standard'], loc='upper left', handlelength=1.5)

        plot_stim(PSTHyLims, stimDuration)
        

        figDirectory = os.path.join(settings.FIGURES_DATA_PATH, f'{subject}/oddball')
        if not os.path.exists(figDirectory):
            os.makedirs(figDirectory)
        figName= f'{subject}_{dbRow.date}_{dbRow.maxDepth}um_c{dbRow.cluster}_oddball'
        fileName = os.path.join(figDirectory, figName)

        #plt.suptitle(f'{oneCell}', fontsize=16, fontweight='bold', y = 0.99)


        '''
        # Goes through each psth plot and calculutes the lowest and highest ylimit values.
        max_ylim = -np.inf
        min_ylim = np.inf
        for i, ax in enumerate(fig.get_axes()[1::2]):
            ylim = ax.get_ylim()
            if ylim[0] < min_ylim:
                min_ylim = ylim[0]
            if ylim[1] > max_ylim:
                max_ylim = ylim[1]
            
        # Iterates through each psth plot and changes the ylimits to the min and max ylimit.
        new_ylimits = [0, max_ylim]
        for i, ax in enumerate(fig.get_axes()[1::2]):
            ax.set_ylim(new_ylimits)
        '''
        

        plt.show()

        if SAVE_FIGURE:
            extraplots.save_figure(figName, 'png', [8, 3.5], outputDir='/tmp/', facecolor='w')
