"""
Load neuropixels data and show raster plots.
"""

import os
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots

SAVE_FIGS = 0

subject = 'arch042'
sessionDate = '2025-12-08'
probeDepth = 3700

outputDir = f'/data/reports/{subject}/'

# -- Create database of cells --
inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
celldb = celldatabase.generate_cell_database(inforecFile, ignoreMissing=True)

# -- Create subset of database for just one session --
celldbSubset = celldb[(celldb.date==sessionDate) & (celldb.pdepth==probeDepth)]

# -- Load the data --
ensemble = ephyscore.CellEnsemble(celldbSubset)

sessionType = 'optoTuningFreq'
ephysData, bdata = ensemble.load(sessionType)

# -- Align spikes to sound onset --
currentStim = bdata['currentFreq']
eventOnsetTimes = ephysData['events']['stimOn']
laserTrial = bdata['laserTrial']
possibleLaser = [0, 1]  # 0:NoLaser, 1:Laser
nTrials = len(currentStim)

# If we have one more (incomplete) trial in the behavior file, remove it.
if len(currentStim) == len(eventOnsetTimes)-1:
        eventOnsetTimes = eventOnsetTimes[:nTrials]

timeRange = [-0.5, 1]        
spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = \
    ensemble.eventlocked_spiketimes(eventOnsetTimes, timeRange)

# -- Plot a raster for one cell (spikes in chronological order) --
if 0:
    cellID = 27
    plt.clf()
    plt.plot(spikeTimesFromEventOnsetAll[cellID], trialIndexForEachSpikeAll[cellID], '.')
    plt.xlabel('Time from sound onset (s)')
    plt.ylabel('Trial number')
    plt.show()

# -- Find trials of each type --    
possibleStim = np.unique(currentStim)
#trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStim)
#nTrialsEachCond = trialsEachCond.sum(axis=0)  # Not used, but in case you need it
trialsEachComb = behavioranalysis.find_trials_each_combination(currentStim, possibleStim, laserTrial, possibleLaser)

#condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)
#sortingInds = np.argsort(sortedTrials)  # This will be used to sort trialIndexForEachSpike
    
# -- Plot rasters --
colorEachCond = ['0.5', 'g']
nCells = len(celldbSubset)
nRows = 4
nCols = 7
nPages = int(np.ceil(nCells/(nRows*nCols)))
fig = plt.gcf()
figSize = [25, 12.8]
fig.set_size_inches(figSize)
for indpage in range(nPages):
    plt.clf()
    someCells = np.arange(0, nRows*nCols) + indpage*nRows*nCols
    for count, indcell in enumerate(someCells):
        if indcell >= len(celldbSubset):
            break
        #sortedIndexForEachSpike = sortingInds[trialIndexForEachSpikeAll[indcell]]
        plt.subplot(nRows, nCols, count+1)
        #plt.plot(spikeTimesFromEventOnsetAll[indcell], sortedIndexForEachSpike, '.k', ms=1)
        (pRaster,hcond,zline) = extraplots.raster_plot_multicond(spikeTimesFromEventOnsetAll[indcell],
                                 indexLimitsEachTrialAll[indcell],
                                 timeRange, trialsEachComb,
                                 colorEachCond=colorEachCond)
        plt.setp(pRaster, ms=1)
        plt.xlabel('Time (s)')
        plt.ylabel(f'[{indcell}] Sorted trials')
    plt.suptitle(f'{subject} {sessionDate} {probeDepth}um {sessionType} ({indpage+1}/{nPages})',
                 fontweight='bold')
    plt.tight_layout()
    plt.show()
    #break
    plt.pause(0.1)

    if SAVE_FIGS:
        figFilename = f'{subject}_{sessionType}_{sessionDate}_{probeDepth}um_{indpage+1:02d}'
        extraplots.save_figure(figFilename, 'png', figSize, outputDir=outputDir, facecolor='w')
