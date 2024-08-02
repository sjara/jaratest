import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis

plt.clf()

subject = 'feat015'
sessionDate = '2024-03-20'
probeDepth = 2413

inforecFile = os.path.join(settings.INFOREC_PATH,f'{subject}_inforec.py')
inforecFile = inforecFile.replace('.py','.test.py')
celldb = celldatabase.generate_cell_database(inforecFile)

celldbSubset = celldb[(celldb.date == sessionDate) & (celldb.pdepth == probeDepth)]
# g. load an ensemble of neurons
ensemble = ephyscore.CellEnsemble(celldbSubset)
ephysData, bdata = ensemble.load('AM')

nTrials = len(bdata['currentFreq'])
eventOnsetTimes = ephysData['events']['stimOn'][:nTrials] # Ignore trials not in bdata
timeRange = [-0.5, 1]  # In seconds

spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = \
    ensemble.eventlocked_spiketimes(eventOnsetTimes, timeRange)

currentStim = bdata['currentFreq']
possibleStim = np.unique(currentStim)
trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStim)
nTrialsEachCond = trialsEachCond.sum(axis=0)  # Not used, but in case you need it

# Here we create sorting array to be used later.
condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)
sortingInds = np.argsort(sortedTrials)  # This will be used to sort trialIndexForEachSpike

# rasters (with trials sorted by stimulus type) for a subset of cells
someCells = [5,10,15,21]
fig = plt.figure(figsize=[10, 6])
for count, indcell in enumerate(someCells):
    # And here is where we use the sorting array.
    sortedIndexForEachSpike = sortingInds[trialIndexForEachSpikeAll[indcell]]
    plt.subplot(2, 2, count+1)
    plt.plot(spikeTimesFromEventOnsetAll[indcell], sortedIndexForEachSpike, '.k', ms=3)
    plt.xlabel('Time (s)')
    plt.ylabel('Sorted trials')
plt.tight_layout()
plt.show()

# h. count the number of spikes for each cell in a particular time period
binSize = 0.005
binEdges = np.arange(timeRange[0], timeRange[1], binSize)
spikeCount = ensemble.spiketimes_to_spikecounts(binEdges)

sortedSpikeCount = spikeCount[:, sortedTrials, :]
fig = plt.figure(figsize=[10, 4])
cellToPlot = 10
plt.imshow(sortedSpikeCount[cellToPlot], aspect='auto', origin='lower')
plt.xlabel('Time bin')
plt.ylabel('Trial (sorted by stim type)')
plt.colorbar(label='N spikes')

plt.show()