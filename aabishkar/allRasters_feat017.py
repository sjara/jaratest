"""
Show raster plots of neurons in response to natural sounds.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from importlib import reload
reload(celldatabase)

subject = 'feat017'
sessionDate = '2024-04-08'
probeDepth = 3000

inforecFile = os.path.join(settings.INFOREC_PATH,f'{subject}_inforec.py')
inforecFile = inforecFile.replace('.py','.test.py')
celldb = celldatabase.generate_cell_database(inforecFile)


# -- Load the data --
celldbSubset = celldb[(celldb.date == sessionDate) & (celldb.pdepth == probeDepth)]

ensemble = ephyscore.CellEnsemble(celldbSubset)

ephysData, bdata = ensemble.load('naturalSound')
currentStim = bdata['soundID']
timeRange = [-0.5, 4.5]  # In seconds

nTrials = len(currentStim)
eventOnsetTimes = ephysData['events']['stimOn'][:nTrials] # Ignore trials not in bdata

spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = \
    ensemble.eventlocked_spiketimes(eventOnsetTimes, timeRange)

possibleStim = np.unique(currentStim)
trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStim)
nTrialsEachCond = trialsEachCond.sum(axis=0)  # Not used, but in case you need it

condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)
sortingInds = np.argsort(sortedTrials)  # This will be used to sort trialIndexForEachSpike

# -- Plot rasters --
someCells = np.arange(0,28)
plt.clf()
for count, indcell in enumerate(someCells):
    if indcell >= len(celldbSubset):
        break
    sortedIndexForEachSpike = sortingInds[trialIndexForEachSpikeAll[indcell]]
    plt.subplot(4, 7, count+1)
    plt.plot(spikeTimesFromEventOnsetAll[indcell], sortedIndexForEachSpike, '.k', ms=1)
    plt.xlabel('Time (s)')
    plt.ylabel(f'[{indcell}] Sorted trials')
plt.tight_layout()
plt.show()

