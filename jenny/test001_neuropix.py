import os
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis


inforecFile = os.path.join(settings.INFOREC_PATH,'npix001_inforec.py')
celldb = celldatabase.generate_cell_database(inforecFile)

for indRow, dbRow in celldb.iterrows():
oneCell = ephyscore.Cell(dbRow)
ephysData, bdata = oneCell.load('VOT')


# Align spikes to an event
spikeTimes = ephysData['spikeTimes']
eventOnsetTimes = ephysData['events']['stimOn']
timeRange = [-0.5, 3]  # In seconds

(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)


# Plot rasters

timeRange = [-0.5,3]

#pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange)
#plt.show()


# Type-sorted rasters
timeRange = [-0.5,3]

soundParamsEachTrial = bdata['targetPercentage']
possibleParams = np.unique(soundParamsEachTrial)
trialsEachCond = behavioranalysis.find_trials_each_type(soundParamsEachTrial, possibleParams)

#fRaster = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange, trialsEachCond)
#plt.show()


# Plot PSTH

binWidth = 0.020
timeRange = [-0.5, 3]
timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
smoothWinSizePsth = 2 
lwPsth = 2
downsampleFactorPsth = 1

spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth,timeVec,trialsEachCond, colorEachCond, linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
plt.show()

'''
# Look at Single Cell
cellDict = {'subject' : 'feat001', 'date' : '2021-11-19', 'pdepth' : 3320, 'egroup' : 0, 'cluster' : 10}              


cellInd, dbRow = celldatabase.find_cell(celldb, **cellDict)
oneCell = ephyscore.Cell(dbRow)
ephysData, bdata = oneCell.load('VOT')


# Align spikes to an event
spikeTimes = ephysData['spikeTimes']
eventOnsetTimes = ephysData['events']['stimOn']
timeRange = [-0.5, 3]  # In seconds

(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)


# Plot rasters

timeRange = [-0.5,3]

#pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange)
#plt.show()


# Type-sorted rasters
timeRange = [-0.5,3]

soundParamsEachTrial = bdata['targetPercentage']
possibleParams = np.unique(soundParamsEachTrial)
trialsEachCond = behavioranalysis.find_trials_each_type(soundParamsEachTrial, possibleParams)

#fRaster = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange, trialsEachCond)
#plt.show()


# Plot PSTH

binWidth = 0.020
timeRange = [-0.5, 3]
timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
smoothWinSizePsth = 2 
lwPsth = 2
downsampleFactorPsth = 1

spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth,timeVec,trialsEachCond, colorEachCond, linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
plt.show()
'''
