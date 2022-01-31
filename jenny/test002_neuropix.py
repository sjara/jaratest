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
    plt.clf()
    indplot = 1

    oneCell = ephyscore.Cell(dbRow)
    plt.subplot(331)
    plt.plot(dbRow.spikeShape)
    plt.text(30, -0.1, f"bestChannel = {dbRow.bestChannel}")
    plt.title(oneCell)

    #FTVOTBorders
    ephysData, bdata = oneCell.load('FTVOTBorders')

    # Align spikes to an event
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.3,  0.45]  # In seconds
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    # Type-sorted rasters -- FTVOTBorders
    timeRange = [-0.3, 0.45]
    VOTParamsEachTrial = bdata['targetVOTpercent']
    possibleVOTParams = np.unique(VOTParamsEachTrial)
    FTParamsEachTrial = bdata['targetFTpercent']
    possibleFTParams = np.unique(FTParamsEachTrial)
    trialsEachCond = behavioranalysis.find_trials_each_combination(VOTParamsEachTrial, possibleVOTParams, FTParamsEachTrial, possibleFTParams)


    plt.subplot(334)
    fRaster = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange, trialsEachCond)
    plt.xlabel('Time (s)')
    plt.ylabel('Trials')
    plt.title('FTVOTBorders')

    # PSTH -- FTVOTBorders
    binWidth = 0.010
    timeRange = [-0.3,  0.45]
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    smoothWinSizePsth = 6
    lwPsth = 2
    downsampleFactorPsth = 3
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
    plt.subplot(337)
    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth, timeVec, trialsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
    plt.xlabel('Time (s)')
    plt.ylabel('Firing Rate (Sp/s)')

    #AM
    ephysData, bdata = oneCell.load('AM')

    # Align spikes to an event
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.3,  0.75]  # In seconds
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    # Type-sorted rasters -- AM
    timeRange = [-0.3, 0.75]
    soundParamsEachTrial = bdata['currentFreq']
    possibleParams = np.unique(soundParamsEachTrial)
    trialsEachCond = behavioranalysis.find_trials_each_type(soundParamsEachTrial, possibleParams)
    plt.subplot(332)
    fRaster = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange, trialsEachCond)
    plt.xlabel('Time (s)')
    plt.ylabel('Trials')
    plt.title('AM')

    #pureTones
    ephysData, bdata = oneCell.load('pureTones')

    # Align spikes to an event
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.2,  0.3]  # In seconds
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    # Type-sorted rasters -- pureTones
    timeRange = [-0.2, 0.3]
    soundParamsEachTrial = bdata['currentFreq']
    possibleParams = np.unique(soundParamsEachTrial)
    trialsEachCond = behavioranalysis.find_trials_each_type(soundParamsEachTrial, possibleParams)
    plt.subplot(333)
    fRaster = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange, trialsEachCond)
    plt.xlabel('Time (s)')
    plt.ylabel('Trials')
    plt.title('Pure Tones')



    plt.gcf().set_size_inches([14, 12])
    print(oneCell)
    plt.show()
    input("press enter for next cell")
    indplot += 1
plt.close()


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

pPSTH = extraplots.plot_psth(spikeCountMat/binWidth, smoothWinSizePsth,timeVec,trialsEachCond, linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
plt.show()
'''
