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


subject = 'arch013'

inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
celldb = celldatabase.generate_cell_database(inforecFile, ignoreMissing=True)

dbRow = celldb.iloc[12]  # Get metadata for one cell in database
oneCell = ephyscore.Cell(dbRow)  # The Cell object has methods for loading specific data sessions 

ephysData, bdata = oneCell.load('optoTuningAM') # Load data for session with AM sounds

currentStim = bdata['currentFreq']
eventOnsetTimes = ephysData['events']['stimOn']
nTrials = len(currentStim)
# If we have one more (incomplete) trial in the behavior file, remove it.
if len(currentStim) == len(eventOnsetTimes)-1:
        eventOnsetTimes = eventOnsetTimes[:nTrials]
        
spikeTimes = ephysData['spikeTimes']

timeRange = [-0.5, 1]

(spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

if 0:
    plt.clf()
    plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')
    plt.xlabel('Time from sound onset (s)')
    plt.ylabel('Trial number')
    plt.show()

possibleStim = np.unique(currentStim)
trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStim)

plt.clf()
fRaster = extraplots.raster_plot(spikeTimesFromEventOnset,
                                 indexLimitsEachTrial,
                                 timeRange, np.fliplr(trialsEachCond))
plt.xlabel('Time from sound onset (s)')

plt.show()

