"""
Show raster plots of neurons in response to natural sounds.

 Feat015 2024-03-20 2413um
 feat015 2024-03-20 2413
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from importlib import reload
reload(celldatabase)

from jaratoolbox import loadneuropix
reload(loadneuropix)

SESSIONID = 0
if SESSIONID == 0:
    subject = 'feat015'
    sessionDate = "2024-03-20"
    probeDepth = 2413
if SESSIONID == 1:
    subject = 'feat016'
    sessionDate = "2024-04-08"
    probeDepth = 3000
if SESSIONID == 2:
    subject = 'feat017'
    sessionDate = "2024-03-26"
    probeDepth = 3000
if SESSIONID == 3:
    subject = 'feat017'
    sessionDate = "2024-03-29"
    probeDepth = 3000

if 0:
    inforecFile = os.path.join(settings.INFOREC_PATH,f'{subject}_inforec.py')
    inforecFile = inforecFile.replace('.py','.test.py')
    celldb = celldatabase.generate_cell_database(inforecFile)
else:
    inforecFile = os.path.join(settings.INFOREC_PATH,f'{subject}_inforec.py')
    celldb = celldatabase.generate_cell_database(inforecFile, ignoreMissing=True)

# -- Load the data --
celldbSubset = celldb[(celldb.date==sessionDate) & (celldb.pdepth==probeDepth)]

ensemble = ephyscore.CellEnsemble(celldbSubset)

if 1:
    ephysData, bdata = ensemble.load('naturalSound')
    currentStim = bdata['soundID']
    #timeRange = [-6, 10]  # In seconds
    timeRange = [-2, 6]  # In seconds
else:
    ephysData, bdata = ensemble.load('AM')
    currentStim = bdata['currentFreq']
    timeRange = [-0.5, 1]  # In seconds

#nTrials = len(bdata['timeTrialStart'])
nTrials = len(currentStim)
eventOnsetTimes = ephysData['events']['stimOn'][:nTrials] # Ignore trials not in bdata 

spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = \
    ensemble.eventlocked_spiketimes(eventOnsetTimes, timeRange)

possibleStim = np.unique(currentStim)
#possibleStim = np.arange(4)
trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStim)
nTrialsEachCond = trialsEachCond.sum(axis=0)  # Not used, but in case you need it

condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)
sortingInds = np.argsort(sortedTrials)  # This will be used to sort trialIndexForEachSpike

# -- Plot rasters --
#someCells = [13, 15, 16, 22]
#someCells = [6]
#someCells = np.arange(0,12)+12+5
someCells = np.arange(0,4*7) + 0*28
#someCells = np.arange(0,len(celldbSubset))
#someCells = [88, 95] # feat017 2024-03-26 (for duration of offset response)
plt.clf()
#fig = plt.figure(figsize=[10, 6])
for count, indcell in enumerate(someCells):
    if indcell >= len(celldbSubset):
        break
    sortedIndexForEachSpike = sortingInds[trialIndexForEachSpikeAll[indcell]]
    plt.subplot(4, 7, count+1)
    #plt.subplot(1, 2, count+1)
    #plt.subplot(1, 1, count+1)
    plt.plot(spikeTimesFromEventOnsetAll[indcell], sortedIndexForEachSpike, '.k', ms=1)
    plt.xlabel('Time (s)')
    plt.ylabel(f'[{indcell}] Sorted trials')
plt.tight_layout()
plt.show()

