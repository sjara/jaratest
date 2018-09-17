import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec
from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import ephyscore
from jaratoolbox import extraplots
from jaratoolbox import colorpalette as cp
from scipy import stats

inforec_path = '/home/nick/src/jaratest/common/inforecordings/pinp031_inforec.py'

dataframe = celldatabase.generate_cell_database(inforec_path)

figSize = (8, 11)

colorNoise = cp.TangoPalette['Orange1']
colorLaser = cp.TangoPalette['SkyBlue1']


#Calculate whether or not the cell is "Tagged" according to the criterion in our paper
for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):

    cell = ephyscore.Cell(dbRow)

    try:
        pulseData, _ = cell.load('laserpulse_pre')
    except (IndexError, ValueError):
        print "Cell has no laserpulse session, loading laser train session for pulse data"
        try:
            pulseData, _ = cell.load('lasertrain_pre') ##FIXME!!! Loading train if we have no pulse. Bad idea??
        except (IndexError, ValueError):
            print "Cell has no laser train session or no spikes. FAIL!"
            dataframe.loc[indRow, 'autoTagged'] = 0
            continue
    try:
        trainData, _ = cell.load('lasertrain_pre')
    except (IndexError, ValueError):
        print "Cell has no laser train session or no spikes. FAIL!"
        dataframe.loc[indRow, 'autoTagged'] = 0
        continue

    #Laser pulse analysis
    spikeTimes = pulseData['spikeTimes']
    eventOnsetTimes = pulseData['events']['stimOn']
    baseRange = [-0.050,-0.04]              # Baseline range (in seconds)
    binTime = baseRange[1]-baseRange[0]         # Time-bin size
    responseRange = [0, 0+binTime]
    alignmentRange = [baseRange[0], responseRange[1]]
    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   alignmentRange)
    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,baseRange)
    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,responseRange)

    try:
        zStat, pVal = stats.mannwhitneyu(nspkResp, nspkBase)
    except ValueError: #All numbers identical will cause mann whitney to fail
        zStat, pVal = [0, 1]

    # if pVal<0.05 and zStat>0: #This does not work because MW still gives positive Z if response goes down
    if (pVal<0.05) and (nspkResp.ravel().mean() > nspkBase.ravel().mean()):
        passPulse = True
    else:
        passPulse = False


    #Lasertrain analysis
    #There should be a significant response to all of the pulses
    spikeTimes = trainData['spikeTimes']
    trainPulseOnsetTimes = trainData['events']['stimOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(trainPulseOnsetTimes, 0.5)
    baseRange = [-0.050,-0.04]              # Baseline range (in seconds)
    pulseTimes = [0, 0.2, 0.4, 0.6, 0.8]
    baseRange = [-0.05, -0.03]
    binTime = baseRange[1]-baseRange[0]         # Time-bin size
    alignmentRange = [baseRange[0], pulseTimes[-1]+binTime]

    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   alignmentRange)


    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,baseRange)

    zStats = np.empty(len(pulseTimes))
    pVals = np.empty(len(pulseTimes))
    respSpikeMean = np.empty(len(pulseTimes))
    for indPulse, pulse in enumerate(pulseTimes):
        responseRange = [pulse, pulse+binTime]
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                           indexLimitsEachTrial,responseRange)
        respSpikeMean[indPulse] = nspkResp.ravel().mean()
        try:
            zStats[indPulse], pVals[indPulse] = stats.mannwhitneyu(nspkResp, nspkBase)
        except ValueError: #All numbers identical will cause mann whitney to fail
            zStats[indPulse], pVals[indPulse] = [0, 1]

    # if (pVals[0] < 0.05) and (sum(pVals[1:]<0.05) >= 3) and all(zStats>0):
    if (pVals[0] < 0.05) and (sum(pVals[1:]<0.05) >= 3) and (all(respSpikeMean > nspkBase.ravel().mean())):
        passTrain = True
    else:
        passTrain = False

    if passPulse and passTrain:
        print "PASS"
        dataframe.loc[indRow, 'autoTagged'] = 1
    else:
        print "FAIL"
        dataframe.loc[indRow, 'autoTagged'] = 0


def plot_NBQX_report(dbRow, saveDir=None):
    #Init cell object
    cell = ephyscore.Cell(dbRow)

    plt.clf()
    gs = gridspec.GridSpec(4, 2, hspace=0.5, wspace=0.5)
    # gs.update(left=0.15, right=0.95, bottom=0.15, wspace=1, hspace=1)

    gsNoisePre = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[0, 0], hspace=0)
    gsPulsePre = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[1, 0], hspace=0)
    gsTrainPre = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[2, 0], hspace=0)

    gsNoisePost = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[0, 1], hspace=0)
    gsPulsePost = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[1, 1], hspace=0)
    gsTrainPost = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[2, 1], hspace=0)

    gsCluster = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=gs[3, :])

    #Noiseburst Pre

    def plot_raster_and_PSTH(sessiontype, gs, color='k'):
        axRaster = plt.subplot(gs[0])
        ephysData, bdata = cell.load(sessiontype)
        eventOnsetTimes = ephysData['events']['stimOn']
        eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.5)
        timeRange = [-0.3, 1.0]
        (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(ephysData['spikeTimes'],
                                                                        eventOnsetTimes,
                                                                        timeRange)
        # pRaster, hCond, zLine = extraplots.raster_plot(spikeTimesFromEventOnset,
        #                                                 indexLimitsEachTrial,
        #                                                 timeRange)
        axRaster.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.',
                            ms=1, rasterized=True)
        # plt.setp(pRaster, ms=1)
        axRaster.set_xlim(timeRange)
        axRaster.set_xticks([])
        # axRaster.axis('off')
        extraplots.boxoff(axRaster)
        axRaster.set_yticks([len(eventOnsetTimes)])

        axPSTH = plt.subplot(gs[1])
        smoothPSTH = True
        psthLineWidth = 2
        smoothWinSize = 1
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
                    color=color, lw=psthLineWidth)

        displayRange = timeRange
        axPSTH.set_xlim(displayRange)
        extraplots.boxoff(axPSTH)
        axPSTH.set_ylim([0, max(ratePSTH)])
        axPSTH.set_yticks([0, np.floor(np.max(ratePSTH))])
        # axPSTH.set_ylabel('spk/s', fontsize=fontSizeLabels)
        axPSTH.set_ylabel('spk/s')
        # axPSTH.set_xticks([0, 0.3])



        # avResp = np.mean(spikeCountMat,axis=0)
        # smoothPSTH = np.convolve(avResp,win, mode='same')
        # plt.plot(timeVec, smoothPSTH,'k-', mec='none' ,lw=2)
        # axPSTH.set_xlim(timeRange)
        # axPSTH.set_xlabel('Time from onset (s)')

    plot_raster_and_PSTH('noiseburst_pre', gsNoisePre, color=colorNoise)
    plot_raster_and_PSTH('laserpulse_pre', gsPulsePre, color=colorLaser)
    plot_raster_and_PSTH('lasertrain_pre', gsTrainPre, color=colorLaser)
    plot_raster_and_PSTH('noiseburst_post', gsNoisePost, color=colorNoise)
    plot_raster_and_PSTH('laserpulse_post', gsPulsePost, color=colorLaser)
    plot_raster_and_PSTH('lasertrain_post', gsTrainPost, color=colorLaser)


    (timestamps,
     samples,
     recordingNumber) = cell.load_all_spikedata()

    #ISI loghist
    axISI = plt.subplot(gsCluster[0])
    if timestamps is not None:
        try:
            spikesorting.plot_isi_loghist(timestamps)
        except:
            # raise AttributeError
            print "problem with isi vals"

    #Waveforms
    axWaves = plt.subplot(gsCluster[1])
    if len(samples)>0:
        spikesorting.plot_waveforms(samples)

    #Events in time
    axEvents = plt.subplot(gsCluster[2])
    if timestamps is not None:
        try:
            spikesorting.plot_events_in_time(timestamps)
        except:
            print "problem with isi vals"

    fig = plt.gcf()
    fig.set_size_inches(figSize)

    figName = '{}_{}_{}um_TT{}c{}.png'.format(dbRow['subject'],
                                              dbRow['date'],
                                              int(dbRow['depth']),
                                              int(dbRow['tetrode']),
                                              int(dbRow['cluster']))

    if dbRow['autoTagged']==1:
        autoTaggedStatus="PASS"
    elif dbRow['autoTagged']==0:
        autoTaggedStatus="FAIL"

    plt.suptitle("{}\nautoTagged:{}".format(figName[:-4], autoTaggedStatus))

    if saveDir is not None:
        figPath = os.path.join(saveDir, figName)
        print "Saving figure to: {}".format(figPath)
        plt.savefig(figPath)


NBQXsite = dataframe.query('depth==1400.2')
salineSite = dataframe.query('depth==1400.4')
# goodCells = NBQXsite.query('isiViolations<0.02 and spikeShapeQuality>2')

saveDir = '/home/nick/data/reports/nick/20180626_NBQX_pinp031'
for indCell, cell in NBQXsite.iterrows():
    print "Plotting report for cell {}".format(indCell)
    plot_NBQX_report(cell, saveDir=saveDir)

saveDir = '/home/nick/data/reports/nick/20180626_Saline_pinp031'
for indCell, cell in salineSite.iterrows():
    print "Plotting report for cell {}".format(indCell)
    plot_NBQX_report(cell, saveDir=saveDir)

