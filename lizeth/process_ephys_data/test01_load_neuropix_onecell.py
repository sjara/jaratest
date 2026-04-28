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


subject = 'arch033'
#2025-1027
inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
celldb = celldatabase.generate_cell_database(inforecFile, ignoreMissing=True) #each row contains information for one neuron

dbRow = celldb.iloc[262]  # Get metadata for one cell in database
oneCell = ephyscore.Cell(dbRow)  # The Cell object has methods for loading specific data sessions 

ephysData, bdata = oneCell.load('optoTuningAM') # Load data for session with AM sounds

currentStim = bdata['currentFreq'] #Frequencies presented
eventOnsetTimes = ephysData['events']['stimOn']
laserTrial = bdata['laserTrial']

nTrials = len(currentStim)
# If we have one more (incomplete) trial in the behavior file, remove it.
if len(currentStim) == len(eventOnsetTimes)-1:
        eventOnsetTimes = eventOnsetTimes[:nTrials]
        
spikeTimes = ephysData['spikeTimes']

timeRange = [-0.5, 1]

(spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

if 1:
    plt.clf()
    plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')
    plt.xlabel('Time from sound onset (s)')
    plt.ylabel('Trial number')
    plt.show()

possibleStim = np.unique(currentStim)
trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStim) #List with True and False for each freq

plt.clf()
fRaster = extraplots.raster_plot(spikeTimesFromEventOnset,
                                 indexLimitsEachTrial,
                                 timeRange, np.fliplr(trialsEachCond))
plt.xlabel('Time from sound onset (s)')

plt.show()

