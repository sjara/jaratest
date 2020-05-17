"""
Script to formulate single PSTHs for either the ascending or descending session in the threetone sequence.
"""

from jaratoolbox import colorpalette as cp
import matplotlib

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # So font is selectable in SVG

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import spikesorting
import matplotlib.gridspec as gridspec


SAVE_FIGURE = 1
 
dbPath = '/mnt/jarahubdata/reports/2019threetone'
studyName = 'three_tone'

outputDir = '/tmp/'
figFilename = 'Fig_threetone' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [5,2.5] # In inches

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

dbFilename = os.path.join(dbPath,'celldb_{}.h5'.format(studyName))
celldb = celldatabase.load_hdf(dbFilename)

# -- PSTH variables --
binWidth = 0.01
timeRange = [-0.2, 0.5]
xLims = [-0.1,0.4]
timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
smoothWinSizePsth = 4
lwPsth = 3
downsampleFactorPsth = 1
# -- Legend for PSTH --
#oddball_patch = mpatches.Patch(color='b', label='Unexpected')
#standard_patch = mpatches.Patch(color='k', label='Expected')

# -- Defining the cell --
CELLID = 2
if CELLID==0:
    cellDict = {'subject' : 'chad016',
                'date' : '2019-08-29',
                'depth' : 1155,
                'tetrode' : 2,
                'cluster' : 2}
    stimMode = 'descending'
elif CELLID==1:
    cellDict = {'subject' : 'chad016',
                'date' : '2019-08-30',
                'depth' : 1030,
                'tetrode' : 5,
                'cluster' : 5}
elif CELLID==2:
    # -- Example shown in talk --
    cellDict = {'subject' : 'chad015',
                'date' : '2019-08-06',
                'depth' : 930,
                'tetrode' : 8,
                'cluster' : 6}
    stimMode = 'ascending'
elif CELLID==3:
    cellDict = {'subject' : 'chad015',
                'date' : '2019-08-06',
                'depth' : 880,
                'tetrode' : 1,
                'cluster' : 6}
elif CELLID==4:
    cellDict = {'subject' : 'chad015',
                'date' : '2019-08-06',
                'depth' : 880,
                'tetrode' : 8,
                'cluster' : 4}
elif CELLID==5:
    cellDict = {'subject' : 'chad015',
                'date' : '2019-08-08',
                'depth' : 1025,
                'tetrode' : 6,
                'cluster' : 5}

cellInd, dbRow = celldatabase.find_cell(celldb, **cellDict)
oneCell = ephyscore.Cell(dbRow)
#ephysData, bdata = oneCell.load('descending')
ephysData, bdata = oneCell.load(stimMode)

spikeTimes = ephysData['spikeTimes']
eventOnsetTimes = ephysData['events']['stimOn']
if len(eventOnsetTimes) == len(bdata['currentFreq']) + 1:
    eventOnsetTimes = eventOnsetTimes[:-1]
arrayOfFrequencies = np.unique(bdata['currentFreq'])
arrayOfFrequencieskHz = arrayOfFrequencies/1000

(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

stimCondition = bdata['stimCondition']
if stimCondition[-1] == 1:
    stimCondition = stimCondition[:-1]

oddballs = np.flatnonzero(stimCondition)

firstOddball = np.array(oddballs[::2])
secondOddball = np.array(oddballs[1::2])
thirdOddball = secondOddball + 1
firstStandard = firstOddball - 2
secondStandard = secondOddball - 4
thirdStandard = thirdOddball - 3

firstOddballIndexLimits = indexLimitsEachTrial[:,firstOddball]
secondOddballIndexLimits = indexLimitsEachTrial[:, secondOddball]
thirdOddballIndexLimits = indexLimitsEachTrial[:, thirdOddball]
firstStandardIndexLimits = indexLimitsEachTrial[:, firstStandard]
secondStandardIndexLimits = indexLimitsEachTrial[:, secondStandard]
thirdStandardIndexLimits = indexLimitsEachTrial[:, thirdStandard]

spikeCountMatFirstOddball = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, firstOddballIndexLimits, timeVec)
spikeCountMatSecondOddball = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, secondOddballIndexLimits, timeVec)
spikeCountMatThirdOddball = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, thirdOddballIndexLimits, timeVec)
spikeCountMatFirstStd = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, firstStandardIndexLimits, timeVec)
spikeCountMatSecondStd = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, secondStandardIndexLimits, timeVec)
spikeCountMatThirdStd = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, thirdStandardIndexLimits, timeVec)

# -- Plotting the PSTH --
gs = gridspec.GridSpec(1,1, top=0.85, left=0.2, right=0.95, bottom=0.25, wspace=0.5, hspace=0.3)

plt.figure(1)
plt.clf()
ax1 = plt.subplot(gs[0])
extraplots.plot_psth(spikeCountMatSecondOddball/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
        colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
extraplots.plot_psth(spikeCountMatSecondStd/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
        colorEachCond='0.25',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
plt.xlabel('Time from sound onset (s)', fontsize=fontSizeLabels)
plt.ylabel('Firing rate (spk/s)', fontsize=fontSizeLabels)
#plt.title('{} kHz Sound'.format(arrayOfFrequencieskHz[1]), fontsize=9)
#plt.legend(handles=[oddball_patch, standard_patch], fontsize=10, edgecolor=None)
plt.legend(['Unexpected','Expected'], fontsize=fontSizeLabels, frameon=False)
plt.xlim(xLims)
plt.axvline(0,color='0.5',ls='--')
extraplots.boxoff(ax1)
extraplots.set_ticks_fontsize(ax1,fontSizeTicks)

# -- Saving the PSTH --
figFilename ='{}_{}_{}um_T{}_c{}_PSTH.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
figFullpath = os.path.join(outputDir,figFilename)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

#plt.savefig(figFullpath,format=figFormat)


PLOT_RASTER = 0
if PLOT_RASTER:
    # -- Plotting the oddball raster --
    plt.figure(2)
    plt.clf()
    plt.subplot(2,1,1)
    extraplots.raster_plot(spikeTimesFromEventOnset,firstOddballIndexLimits,timeRange)
    plt.xlabel('Time From Event Onset [s]', fontsize=9)
    plt.ylabel('Trial', fontsize=9)
    plt.title('Oddball', fontsize=9)
    # -- Saving the odd raster --
    figFilename ='{}_{}_{}um_T{}_c{}_oddraster.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
                dbRow['tetrode'],dbRow['cluster'],figFormat)
    figFullpath = os.path.join(outputDir,figFilename)
    plt.savefig(figFullpath,format=figFormat)

    # -- Plotting the standard raster --
    plt.subplot(2,1,2)
    extraplots.raster_plot(spikeTimesFromEventOnset,firstStandardIndexLimits,timeRange)
    plt.xlabel('Time From Event Onset [s]', fontsize=9)
    plt.ylabel('Trial', fontsize=9)
    plt.title('Standard', fontsize=9)
    # -- Saving the std raster --
    figFilename ='{}_{}_{}um_T{}_c{}_stdraster.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
                dbRow['tetrode'],dbRow['cluster'],figFormat)
    figFullpath = os.path.join(outputDir,figFilename)


plt.show()
