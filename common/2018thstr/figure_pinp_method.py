import os
import numpy as np
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import colorpalette as cp
import figparams
reload(figparams)
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_NBQX.h5')
database = celldatabase.load_hdf(dbPath)

figSize = (8, 11)

colorNoise = cp.TangoPalette['Orange1']
colorLaser = cp.TangoPalette['SkyBlue1']

# cell = ephyscore.Cell(dbRow)

examples = [
    {'subject':'pinp031',
     'date':'2018-06-26',
     'depth':1901.0,
     'tetrode':3,
     'cluster':2},

    {'subject':'pinp031',
     'date':'2018-06-26',
     'depth':1901,
     'tetrode':6,
     'cluster':6
    },

    {'subject':'pinp031',
     'date':'2018-06-28',
     'depth':2251.0,
     'tetrode':6,
     'cluster':4}

    # {'subject':'pinp031',
    #  'date':'2018-06-25',
    #  'depth':1400.2,
    #  'tetrode':2,
    #  'cluster':4}
    ]

plt.clf()
nCriteria = 3
gsAllCriteria = gridspec.GridSpec(nCriteria, 1, hspace=0.5, wspace=0.5)
nExamples = 3

gsCriterion = []
examplesAllCriteria = []
for indCriterion in range(nCriteria):
    gsThisCriterion = gridspec.GridSpecFromSubplotSpec(1, nExamples, subplot_spec=gsAllCriteria[indCriterion])
    gsCriterion.append(gsThisCriterion)
    examplesThisCriterion = []
    for indExample in range(nExamples):
        #Define the shape for each subplot here
        gsThisExample = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=gsThisCriterion[indExample])
        examplesThisCriterion.append(gsThisExample)
    examplesAllCriteria.append(examplesThisCriterion)

plt.clf()



# Criterion 1: Responds to laser pulse

indCriterion = 0
for indExample in range(nExamples):

    indRow, dbRow = celldatabase.find_cell(database, **examples[indExample])
    cell = ephyscore.Cell(dbRow)

    ### -- Pre -- ###
    sessiontype = 'laserpulse_pre'
    axPSTH = plt.subplot(examplesAllCriteria[indCriterion][indExample][0])

    ephysData, bdata = cell.load(sessiontype)
    eventOnsetTimes = ephysData['events']['stimOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.5)

    if not indCriterion == 2:
        timeRange = [-0.3, 1.0]
    else:
        timeRange = [-0.01, 0.05]

    (spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(ephysData['spikeTimes'],
                                                                    eventOnsetTimes,
                                                                    timeRange)


    smoothPSTH = True
    psthLineWidth = 2
    smoothWinSize = 3
    binsize = 10 #in milliseconds
    binEdges = np.around(np.arange(timeRange[0]-(binsize/1000.0), timeRange[1]+2*(binsize/1000.0), (binsize/1000.0)), decimals=2)
    winShape = np.concatenate((np.zeros(smoothWinSize),np.ones(smoothWinSize))) # Square (causal)
    winShape = winShape/np.sum(winShape)
    psthTimeBase = np.linspace(timeRange[0], timeRange[1], num=len(binEdges)-1)

    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,binEdges)

    thisPSTH = np.mean(spikeCountMat,axis=0)
    if smoothPSTH:
        thisPSTH = np.convolve(thisPSTH, winShape, mode='same')
    ratePSTH = thisPSTH/float(binsize/1000.0)
    maxRatePre = np.max(ratePSTH)
    axPSTH.plot(psthTimeBase, ratePSTH, '-',
                color=colorLaser, lw=psthLineWidth)
    axPSTH.set_ylim([0, maxRatePre])
    extraplots.boxoff(axPSTH)

    ### -- Post -- ###
    sessiontype = 'laserpulse_post'
    axPSTH = plt.subplot(examplesAllCriteria[indCriterion][indExample][1])

    ephysData, bdata = cell.load(sessiontype)
    eventOnsetTimes = ephysData['events']['stimOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.5)

    if not indCriterion == 2:
        timeRange = [-0.3, 1.0]
    else:
        timeRange = [-0.01, 0.05]

    (spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(ephysData['spikeTimes'],
                                                                    eventOnsetTimes,
                                                                    timeRange)

    smoothPSTH = True
    psthLineWidth = 2
    smoothWinSize = 3
    binsize = 10 #in milliseconds
    binEdges = np.around(np.arange(timeRange[0]-(binsize/1000.0), timeRange[1]+2*(binsize/1000.0), (binsize/1000.0)), decimals=2)
    winShape = np.concatenate((np.zeros(smoothWinSize),np.ones(smoothWinSize))) # Square (causal)
    winShape = winShape/np.sum(winShape)
    psthTimeBase = np.linspace(timeRange[0], timeRange[1], num=len(binEdges)-1)

    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,binEdges)

    thisPSTH = np.mean(spikeCountMat,axis=0)
    if smoothPSTH:
        thisPSTH = np.convolve(thisPSTH, winShape, mode='same')
    ratePSTH = thisPSTH/float(binsize/1000.0)
    axPSTH.plot(psthTimeBase, ratePSTH, '-',
                color=colorLaser, lw=psthLineWidth)

    axPSTH.set_ylim([0, maxRatePre])
    extraplots.boxoff(axPSTH)

    # # Waveform Comparison
    # plt.subplot(examplesAllCriteria[indCriterion][indExample][2])


# Criterion 2: Responds to laser pulse

indCriterion = 1
for indExample in range(nExamples):

    indRow, dbRow = celldatabase.find_cell(database, **examples[indExample])
    cell = ephyscore.Cell(dbRow)

    ### -- Pre -- ###
    sessiontype = 'lasertrain_pre'
    axPSTH = plt.subplot(examplesAllCriteria[indCriterion][indExample][0])

    ephysData, bdata = cell.load(sessiontype)
    eventOnsetTimes = ephysData['events']['stimOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.5)

    if not indCriterion == 2:
        timeRange = [-0.3, 1.0]
    else:
        timeRange = [-0.01, 0.05]

    (spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(ephysData['spikeTimes'],
                                                                    eventOnsetTimes,
                                                                    timeRange)


    smoothPSTH = True
    psthLineWidth = 2
    smoothWinSize = 3
    binsize = 10 #in milliseconds
    binEdges = np.around(np.arange(timeRange[0]-(binsize/1000.0), timeRange[1]+2*(binsize/1000.0), (binsize/1000.0)), decimals=2)
    winShape = np.concatenate((np.zeros(smoothWinSize),np.ones(smoothWinSize))) # Square (causal)
    winShape = winShape/np.sum(winShape)
    psthTimeBase = np.linspace(timeRange[0], timeRange[1], num=len(binEdges)-1)

    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,binEdges)

    thisPSTH = np.mean(spikeCountMat,axis=0)
    if smoothPSTH:
        thisPSTH = np.convolve(thisPSTH, winShape, mode='same')
    ratePSTH = thisPSTH/float(binsize/1000.0)
    maxRatePre = np.max(ratePSTH)
    axPSTH.plot(psthTimeBase, ratePSTH, '-',
                color=colorLaser, lw=psthLineWidth)
    axPSTH.set_ylim([0, maxRatePre])
    extraplots.boxoff(axPSTH)

    ### -- Post -- ###
    sessiontype = 'lasertrain_post'
    axPSTH = plt.subplot(examplesAllCriteria[indCriterion][indExample][1])

    ephysData, bdata = cell.load(sessiontype)
    eventOnsetTimes = ephysData['events']['stimOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.5)

    if not indCriterion == 2:
        timeRange = [-0.3, 1.0]
    else:
        timeRange = [-0.01, 0.05]

    (spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(ephysData['spikeTimes'],
                                                                    eventOnsetTimes,
                                                                    timeRange)

    smoothPSTH = True
    psthLineWidth = 2
    smoothWinSize = 3
    binsize = 10 #in milliseconds
    binEdges = np.around(np.arange(timeRange[0]-(binsize/1000.0), timeRange[1]+2*(binsize/1000.0), (binsize/1000.0)), decimals=2)
    winShape = np.concatenate((np.zeros(smoothWinSize),np.ones(smoothWinSize))) # Square (causal)
    winShape = winShape/np.sum(winShape)
    psthTimeBase = np.linspace(timeRange[0], timeRange[1], num=len(binEdges)-1)

    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,binEdges)

    thisPSTH = np.mean(spikeCountMat,axis=0)
    if smoothPSTH:
        thisPSTH = np.convolve(thisPSTH, winShape, mode='same')
    ratePSTH = thisPSTH/float(binsize/1000.0)
    axPSTH.plot(psthTimeBase, ratePSTH, '-',
                color=colorLaser, lw=psthLineWidth)

    axPSTH.set_ylim([0, maxRatePre])
    extraplots.boxoff(axPSTH)

    # # Waveform Comparison
    # plt.subplot(examplesAllCriteria[indCriterion][indExample][2])


indCriterion = 2
for indExample in range(nExamples):

    indRow, dbRow = celldatabase.find_cell(database, **examples[indExample])
    cell = ephyscore.Cell(dbRow)

    ### -- Pre -- ###
    sessiontype = 'laserpulse_pre'
    axRaster = plt.subplot(examplesAllCriteria[indCriterion][indExample][0])

    ephysData, bdata = cell.load(sessiontype)
    eventOnsetTimes = ephysData['events']['stimOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.5)

    timeRange = [-0.02, 0.04]

    (spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(ephysData['spikeTimes'],
                                                                    eventOnsetTimes,
                                                                    timeRange)

    axRaster.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.', ms=1)
    axRaster.axvline(x=0.01)
    extraplots.boxoff(axRaster)


#Waveform comparison plots
for indExample in range(nExamples):

    indRow, dbRow = celldatabase.find_cell(database, **examples[indExample])
    cell = ephyscore.Cell(dbRow)
    axWave = plt.subplot(examplesAllCriteria[indCriterion][indExample][1])
    axWave.hold(1)

    ### -- Pre -- ###
    sessiontype = 'noiseburst_pre'
    ephysData, bdata = cell.load(sessiontype)
    samples = ephysData['samples']
    channelMax = np.argmin(samples.mean(axis=0).min(axis=1)) #Find the index of the channel with the largest min (biggest channel)
    avgWave = samples.mean(axis=0)[channelMax,:]
    stdWave = samples.std(axis=0)[channelMax,:]
    axWave.plot(avgWave, 'k-')
    axWave.fill_between(range(len(avgWave)), avgWave+stdWave, avgWave-stdWave, color='0.5')


    ### -- Post -- ###
    sessiontype = 'noiseburst_post'
    ephysData, bdata = cell.load(sessiontype)

    samples = ephysData['samples']
    channelMax = np.argmin(samples.mean(axis=0).min(axis=1)) #Find the index of the channel with the largest min (biggest channel)
    avgWave = samples.mean(axis=0)[channelMax,:]
    stdWave = samples.std(axis=0)[channelMax,:]
    axWave.plot(avgWave, 'm-')
    axWave.fill_between(range(len(avgWave)), avgWave+stdWave, avgWave-stdWave, color='m', alpha=0.5)


plt.show()


    # def plot_raster_and_PSTH(sessiontype, gs, color='k'):
    #     axRaster = plt.subplot(gs[0])
    #     ephysData, bdata = cell.load(sessiontype)
    #     eventOnsetTimes = ephysData['events']['stimOn']
    #     eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.5)
    #     timeRange = [-0.3, 1.0]
    #     (spikeTimesFromEventOnset,
    #         trialIndexForEachSpike,
    #         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(ephysData['spikeTimes'],
    #                                                                     eventOnsetTimes,
    #                                                                     timeRange)
    #     # pRaster, hCond, zLine = extraplots.raster_plot(spikeTimesFromEventOnset,
    #     #                                                 indexLimitsEachTrial,
    #     #                                                 timeRange)
    #     axRaster.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.',
    #                         ms=1, rasterized=True)
    #     # plt.setp(pRaster, ms=1)
    #     axRaster.set_xlim(timeRange)
    #     axRaster.set_xticks([])
    #     # axRaster.axis('off')
    #     extraplots.boxoff(axRaster)
    #     axRaster.set_yticks([len(eventOnsetTimes)])

    #     axPSTH = plt.subplot(gs[1])
    #     smoothPSTH = True
    #     psthLineWidth = 2
    #     smoothWinSize = 1
    #     binsize = 10 #in milliseconds
    #     binEdges = np.around(np.arange(timeRange[0]-(binsize/1000.0), timeRange[1]+2*(binsize/1000.0), (binsize/1000.0)), decimals=2)
    #     winShape = np.concatenate((np.zeros(smoothWinSize),np.ones(smoothWinSize))) # Square (causal)
    #     winShape = winShape/np.sum(winShape)
    #     psthTimeBase = np.linspace(timeRange[0], timeRange[1], num=len(binEdges)-1)

    #     spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
    #                                                                 indexLimitsEachTrial,binEdges)

    #     thisPSTH = np.mean(spikeCountMat,axis=0)
    #     if smoothPSTH:
    #         thisPSTH = np.convolve(thisPSTH, winShape, mode='same')
    #     ratePSTH = thisPSTH/float(binsize/1000.0)
    #     axPSTH.plot(psthTimeBase, ratePSTH, '-',
    #                 color=color, lw=psthLineWidth)

    #     displayRange = timeRange
    #     axPSTH.set_xlim(displayRange)
    #     extraplots.boxoff(axPSTH)
    #     axPSTH.set_ylim([0, max(ratePSTH)])
    #     axPSTH.set_yticks([0, np.floor(np.max(ratePSTH))])
    #     # axPSTH.set_ylabel('spk/s', fontsize=fontSizeLabels)
    #     axPSTH.set_ylabel('spk/s')
    #     # axPSTH.set_xticks([0, 0.3])



    #     # avResp = np.mean(spikeCountMat,axis=0)
    #     # smoothPSTH = np.convolve(avResp,win, mode='same')
    #     # plt.plot(timeVec, smoothPSTH,'k-', mec='none' ,lw=2)
    #     # axPSTH.set_xlim(timeRange)
    #     # axPSTH.set_xlabel('Time from onset (s)')
