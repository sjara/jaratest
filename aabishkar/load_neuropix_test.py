
import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots


subject = 'feat015'
sessionDate = '2024-03-20'
probeDepth = 2413

# c. create a cell database from an inforec file
inforecFile = os.path.join(settings.INFOREC_PATH,f'{subject}_inforec.py')
inforecFile = inforecFile.replace('.py','.test.py')
celldb = celldatabase.generate_cell_database(inforecFile)

# d. load ephys and stimulus data for one cell
dbRow = celldb.iloc[15]  # Get metadata for one cell in database
oneCell = ephyscore.Cell(dbRow)  # The Cell object has methods for loading specific data sessions
ephysData, bdata = oneCell.load('AM') # Load data for session with AM

nTrials = len(bdata['currentFreq'])
spikeTimes = ephysData['spikeTimes']
eventOnsetTimes = ephysData['events']['stimOn'][:nTrials] # Ignore trials not in bdata
timeRange = [-0.5, 1]  # In seconds

(spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

currentStim = bdata['currentFreq']
possibleStim = np.unique(currentStim)
trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStim)


# raster_plot function is erroring with broadcast error. Ask why
#  e. align spikes to the onset of each stimulus
rasterTimeRange = [-0.5, 1]  # In seconds
pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial,
                                               rasterTimeRange, trialsEachCond, labels=possibleStim)
plt.setp(pRaster, ms=2)
plt.xlabel('Time (s)')
plt.ylabel('AM rate (Hz)')
plt.show()

# f. raster plot with trials sorted by trial type

# fRaster = extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange, trialsEachCond)
# plt.setp(fRaster, ms =2)

#
