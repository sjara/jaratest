import os
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import populationanalysis


inforecFile = os.path.join(settings.INFOREC_PATH,'npix001_inforec.py')
celldb = celldatabase.generate_cell_database(inforecFile)
zStatsAudDriven = np.empty(len(celldb))
pValueAudDriven = np.empty(len(celldb))
maxZvalueAudDriven = np.empty(len(celldb))
respLatency = np.empty(len(celldb))
zStatsAudDriven50ms = np.empty(len(celldb))
pValueAudDriven50ms = np.empty(len(celldb))
maxZvalueAudDriven50ms = np.empty(len(celldb))
meanSpikesFT = np.empty([len(celldb),2])
pValueFT= np.empty(len(celldb))
meanSpikesVOT = np.empty([len(celldb),2])
pValueVOT= np.empty(len(celldb))

#spontRate = np.empty(len(celldb))
#drivenRate = np.empty(len(celldb))
#audDriven = np.zeros(len(celldb))

for indRow, dbRow in celldb.iterrows():

    oneCell = ephyscore.Cell(dbRow)

    #FTVOTBorders
    ephysData, bdata = oneCell.load('FTVOTBorders')

    # Align spikes to an event
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.3,  0.45]  # In seconds
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    #Look at if cells are auditory driven
    soundEnd = bdata['targetDuration'][-1]
    timeRange = [0, soundEnd]
    baseRange = [-soundEnd, 0]
    zStatsAudDriven[indRow], pValueAudDriven[indRow], maxZvalueAudDriven[indRow] = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange,timeRange)


    timeRange = [-0.05,0.24]
    respLatency[indRow], interim = spikesanalysis.response_latency(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,threshold=0.5, win=None)


    timeRange2 = [0, .06]
    baseRange2 = [-.06, 0]
    zStatsAudDriven50ms[indRow], pValueAudDriven50ms[indRow], maxZvalueAudDriven50ms[indRow] = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange2,timeRange2)


    #Get possible params
    VOTParamsEachTrial = bdata['targetVOTpercent']
    possibleVOTParams = np.unique(VOTParamsEachTrial)
    FTParamsEachTrial = bdata['targetFTpercent']
    possibleFTParams = np.unique(FTParamsEachTrial)
    trialsEachCombo = behavioranalysis.find_trials_each_combination(VOTParamsEachTrial, possibleVOTParams, FTParamsEachTrial, possibleFTParams)
    trialsEachFT = behavioranalysis.find_trials_each_type(FTParamsEachTrial, possibleFTParams)
    trialsEachVOT = behavioranalysis.find_trials_each_type(VOTParamsEachTrial, possibleVOTParams)
    trialsExtremesFT = np.array([trialsEachFT[:,0], trialsEachFT[:,-1]])
    trialsExtremesVOT = np.array([trialsEachVOT[:,0], trialsEachVOT[:,-1]])

    #trialsEachCombo = [ntrials, nvalues1, nvalues2]
    responseRange = [0, soundEnd]
    meanSpikesFT[indRow,:], pValueFT[indRow] = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange,trialsExtremesFT)
    meanSpikesVOT[indRow,:], pValueVOT[indRow] = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange,trialsExtremesVOT)
    #meanSpikesCombo, pValueCombo = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange,trialsEachCombo)



    '''
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
    '''

audDriven = pValueAudDriven < 0.05
