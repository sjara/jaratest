import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
sys.path.append('/home/jarauser/src/jaratest/maxh')
#sys.path.append('C:/Users/mdhor/Documents/GitHub/jaratest/maxh')
import oddball_analysis_functions as odbl
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis

timeRangePlot = [-0.3, 0.45]
timeRangeStim = [0.015, 0.115]
timeRangeBaseline = [-0.2, 0]
baselineDuration = timeRangeBaseline[1] - timeRangeBaseline[0]
stimDuration = timeRangeStim[1] - timeRangeStim[0]

binWidth = 0.010
timeVec = np.arange(timeRangePlot[0],timeRangePlot[-1],binWidth)

oddballSessions = ('FM_Up', 'FM_Down')
reagents = ('saline', 'doi')


smoothWinSizePsth = 2 
lwPsth = 2
downsampleFactorPsth = 1

# Raster plot of high frequency
colorsEachCond = ['#39b5c4', '#f04158']
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
            'cluster' : 232}

cellInd, dbRow = celldatabase.find_cell(celldb, **cellDict)
oneCell = ephyscore.Cell(dbRow)

fig = plt.figure()
gsMain = gs.GridSpec(2, 2, fig)


if oneCell.get_session_inds(f'salineFM_Up') != []:
        (combinedSpikeTimesDown, combinedSpikeTimesUp, combinedIndexLimitsDown, combinedIndexLimitsUp, combinedTrialsDown, combinedTrialsUp, spikeCountMatDown, spikeCountMatUp) = odbl.combine_sessions(oneCell, timeRangePlot, 'salineFM_Down', 'salineFM_Up', timeVec)
        
        ax1 = plt.subplot(gsMain[0])
        # plt.xlabel('Time (s)')
        plt.ylabel('Trials')
        plt.title(f'saline FM_UP')
        ax1.tick_params(labelbottom=False) 
        pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesUp, combinedIndexLimitsUp, timeRangePlot, combinedTrialsUp, colorsEachCond, labels= highFreqLabels)
        for p in pRaster:
            p.set_markersize(2)


        ax2 = plt.subplot(gsMain[2], sharex=ax1)    
        extraplots.plot_psth(spikeCountMatUp/binWidth, smoothWinSizePsth, timeVec, combinedTrialsUp, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time (s)')
        plt.ylabel('Firing Rate')
        plt.title(f'saline FM_UP')
        plt.legend(("Standard Tone", "Oddball Tone"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)

        
        (combinedSpikeTimesDown, combinedSpikeTimesUp, combinedIndexLimitsDown, combinedIndexLimitsUp, combinedTrialsDown, combinedTrialsUp, spikeCountMatDown, spikeCountMatUp) = odbl.combine_sessions(oneCell, timeRangePlot, 'doiFM_Down', 'doiFM_Up', timeVec)
        
        ax3 = plt.subplot(gsMain[1])
        # plt.xlabel('Time (s)')
        plt.ylabel('Trials')
        plt.title(f'DOI FM_UP')
        ax1.tick_params(labelbottom=False) 
        pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesUp, combinedIndexLimitsUp, timeRangePlot, combinedTrialsUp, colorsEachCond, labels= highFreqLabels)
        for p in pRaster:
            p.set_markersize(2)


        ax4 = plt.subplot(gsMain[3], sharex=ax2)    
        extraplots.plot_psth(spikeCountMatUp/binWidth, smoothWinSizePsth, timeVec, combinedTrialsUp, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time (s)')
        plt.ylabel('Firing Rate')
        plt.title(f'DOI FM_UP')
        plt.legend(("Standard Tone", "Oddball Tone"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)


        figDirectory = os.path.join(settings.FIGURES_DATA_PATH, f'{subject}/oddball')
        if not os.path.exists(figDirectory):
            os.makedirs(figDirectory)
        figName= f'{subject}_{dbRow.date}_{dbRow.maxDepth}um_c{dbRow.cluster}_oddball.png'
        fileName = os.path.join(figDirectory, figName)

        plt.suptitle(f'{oneCell}', fontsize=16, fontweight='bold', y = 0.99)


        
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
        

        plt.show()
        #plt.savefig(fileName, format='png')
        #print(f'saving image {figName}')
        #plt.close()
print('done')