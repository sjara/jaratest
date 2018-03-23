import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os
from jaratoolbox import settings
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots
from jaratoolbox import ephyscore

def load_all_spikedata(cell):
    '''
    Load the spike data for all recorded sessions into a set of arrays.
    Args:
        dbRow (pandas.Series): One row from a pandas cell database created using generate_cell_database or by
                              manually constructing a pandas.Series object that contains the required fields.
    Returns:
        timestamps (np.array): The timestamps for all spikes across all sessions
        samples (np.array): The samples for all spikes across all sessions
        recordingNumber (np.array): The index of the session where the spike was recorded
    '''
    samples=np.array([])
    timestamps=np.array([])
    recordingNumber=np.array([])
    for ind, sessionType in enumerate(cell.dbRow['sessionType']):
        ephysData, bdata = cell.load(sessionType)
        numSpikes = len(ephysData['spikeTimes'])
        sessionVector = np.zeros(numSpikes)+ind
        if len(samples)==0:
            samples = ephysData['samples']
            timestamps = ephysData['spikeTimes']
            recordingNumber = sessionVector
        else:
            samples = np.concatenate([samples, ephysData['samples']])
            # Check to see if next session ts[0] is lower than self.timestamps[-1]
            # If so, add self.timestamps[-1] to all new timestamps before concat
            if not len(ephysData['spikeTimes'])==0:
                if ephysData['spikeTimes'][0]<timestamps[-1]:
                    ephysData['spikeTimes'] = ephysData['spikeTimes'] + timestamps[-1]
                timestamps = np.concatenate([timestamps, ephysData['spikeTimes']])
                recordingNumber = np.concatenate([recordingNumber, sessionVector])
    return timestamps, samples, recordingNumber

def plot_example_with_rate(subplotSpec, spikeTimes, indexLimitsEachTrial, freqEachTrial, color='k'):
    fig = plt.gcf()

    gs = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=subplotSpec, wspace=-0.45, hspace=0.0 )

    specRaster = gs[0:2]
    axRaster = plt.Subplot(fig, specRaster)
    fig.add_subplot(axRaster)

    # spikeTimes = exampleSpikeTimes[exampleName]
    # indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
    timeRange = [-0.2, 0.7]
    # freqEachTrial = exampleFreqEachTrial[exampleName]
    possibleFreq = np.unique(freqEachTrial)
    freqLabels = ['{0:.1f}'.format(freq) for freq in possibleFreq]
    trialsEachCondition = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)
    pRaster, hCond, zline = extraplots.raster_plot(spikeTimes, indexLimitsEachTrial,
                                                   timeRange, trialsEachCondition, labels=freqLabels)
    plt.setp(pRaster, ms=2)
    ax = plt.gca()
    ax.set_xticks([0, 0.5])
    ax.set_xlabel('Time from\nsound onset (s)')
    ax.set_ylabel('AM Rate (Hz)')

    # ax.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
    #             fontsize=fontSizePanel, fontweight='bold')


    countRange = [0.1, 0.5]
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimes,indexLimitsEachTrial,countRange)
    numSpikesInTimeRangeEachTrial = np.squeeze(spikeCountMat)

    numSpikesInTimeRangeEachTrial = np.squeeze(np.diff(indexLimitsEachTrial,
                                                       axis=0))

    if len(numSpikesInTimeRangeEachTrial) == len(freqEachTrial)+1:
        numSpikesInTimeRangeEachTrial = numSpikesInTimeRangeEachTrial[:-1]
    conditionMatShape = np.shape(trialsEachCondition)
    numRepeats = np.product(conditionMatShape[1:])
    nSpikesMat = np.reshape(numSpikesInTimeRangeEachTrial.repeat(numRepeats),
                            conditionMatShape)
    spikesFilteredByTrialType = nSpikesMat * trialsEachCondition
    avgSpikesArray = np.sum(spikesFilteredByTrialType, 0) / np.sum(
        trialsEachCondition, 0).astype('float')/np.diff(np.array(countRange))
    stdSpikesArray = np.std(spikesFilteredByTrialType, 0)/np.diff(np.array(countRange))

    specRate = gs[3]
    axRate = plt.Subplot(fig, specRate)
    fig.add_subplot(axRate)

    nRates = len(possibleFreq)
    plt.hold(True)
    plt.plot(avgSpikesArray, range(nRates), 'ro-', mec='none', ms=7, lw=3, color=color)
    plt.plot(avgSpikesArray-stdSpikesArray, range(len(possibleFreq)), 'k:')
    plt.plot(avgSpikesArray+stdSpikesArray, range(len(possibleFreq)), 'k:')
    axRate.set_ylim([-0.5, nRates-0.5])
    axRate.set_yticks(range(nRates))
    axRate.set_yticklabels([])

    #ax = plt.gca()
    axRate.set_xlabel('Firing rate\n(spk/s)')
    extraplots.boxoff(axRate)
    # extraplots.boxoff(ax, keep='right')
    return (axRaster, axRate)

def plot_pinp_report(dbRow, saveDir):

    #Init cell object
    cell = ephyscore.Cell(dbRow)

    plt.clf()
    gs = gridspec.GridSpec(9, 6)
    gs.update(left=0.15, right=0.95, bottom=0.15, wspace=1, hspace=1)

    if 'laserpulse' in dbRow['sessionType']: #DONE
        #Laser pulse raster
        ax0 = plt.subplot(gs[0:2, 0:3])
        ephysData, bdata = cell.load('laserpulse')
        eventOnsetTimes = ephysData['events']['stimOn']
        timeRange = [-0.5, 1]
        (spikeTimesFromEventOnset,
         trialIndexForEachSpike,
         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(ephysData['spikeTimes'],
                                                                       eventOnsetTimes,
                                                                       timeRange)
        extraplots.raster_plot(spikeTimesFromEventOnset,
                               indexLimitsEachTrial,
                               timeRange)
        #Laser pulse psth
        ax1 = plt.subplot(gs[2:4, 0:3])
        win = np.array([0, 0.25, 0.75, 1, 0.75, 0.25, 0]) # scipy.signal.hanning(7)
        win = win/np.sum(win)
        binEdges = np.arange(timeRange[0],timeRange[-1],0.001)
        timeVec = binEdges[1:]  # FIXME: is this the best way to define the time axis?
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                 indexLimitsEachTrial,binEdges)
        avResp = np.mean(spikeCountMat,axis=0)
        smoothPSTH = np.convolve(avResp,win, mode='same')
        plt.plot(timeVec, smoothPSTH,'b-', mec='none' ,lw=3)

    if 'lasertrain' in dbRow['sessionType']: #DONE
        #Laser train raster
        ax2 = plt.subplot(gs[0:2, 3:6])
        ephysData, bdata = cell.load('lasertrain')
        eventOnsetTimes = ephysData['events']['stimOn']
        eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)

        timeRange = [-0.5, 1]
        (spikeTimesFromEventOnset,
         trialIndexForEachSpike,
         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(ephysData['spikeTimes'],
                                                                       eventOnsetTimes,
                                                                       timeRange)
        extraplots.raster_plot(spikeTimesFromEventOnset,
                               indexLimitsEachTrial,
                               timeRange)

        #Laser train psth
        ax3 = plt.subplot(gs[2:4, 3:6])
        win = np.array([0, 0.25, 0.75, 1, 0.75, 0.25, 0]) # scipy.signal.hanning(7)
        win = win/np.sum(win)
        binEdges = np.arange(timeRange[0],timeRange[-1],0.001)
        timeVec = binEdges[1:]  # FIXME: is this the best way to define the time axis?
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                 indexLimitsEachTrial,binEdges)
        avResp = np.mean(spikeCountMat,axis=0)
        smoothPSTH = np.convolve(avResp,win, mode='same')
        plt.plot(timeVec, smoothPSTH,'b-', mec='none' ,lw=3)

    #Sorted tuning raster
    if 'tc' in dbRow['sessionType']: #DONE
        ax4 = plt.subplot(gs[4:6, 0:3])
        ephysData, bdata = cell.load('tc')
        eventOnsetTimes = ephysData['events']['stimOn']
        timeRange = [-0.5, 1]
        (spikeTimesFromEventOnset,
         trialIndexForEachSpike,
         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(ephysData['spikeTimes'],
                                                                       eventOnsetTimes,
                                                                       timeRange)
        freqEachTrial = bdata['currentFreq']
        possibleFreq = np.unique(freqEachTrial)
        trialsEachCondition = behavioranalysis.find_trials_each_type(freqEachTrial, possibleFreq)

        extraplots.raster_plot(spikeTimesFromEventOnset,
                               indexLimitsEachTrial,
                               timeRange,
                               trialsEachCond=trialsEachCondition)

        #TC heatmap
        ax5 = plt.subplot(gs[6:8, 0:3])

        baseRange = [-0.1, 0]
        responseRange = [0, 0.1]
        alignmentRange = [baseRange[0], responseRange[1]]

        freqEachTrial = bdata['currentFreq']
        possibleFreq = np.unique(freqEachTrial)
        intensityEachTrial = bdata['currentIntensity']
        possibleIntensity = np.unique(intensityEachTrial)

        #Init arrays to hold the baseline and response spike counts per condition
        allIntenBase = np.array([])
        allIntenResp = np.empty((len(possibleIntensity), len(possibleFreq)))

        spikeTimes = ephysData['spikeTimes']

        for indinten, inten in enumerate(possibleIntensity):
            spks = np.array([])
            freqs = np.array([])
            base = np.array([])
            for indfreq, freq in enumerate(possibleFreq):
                selectinds = np.flatnonzero((freqEachTrial==freq)&(intensityEachTrial==inten))
                selectedOnsetTimes = eventOnsetTimes[selectinds]
                (spikeTimesFromEventOnset,
                trialIndexForEachSpike,
                indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                            selectedOnsetTimes,
                                                                            alignmentRange)
                nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                    indexLimitsEachTrial,
                                                                    baseRange)
                nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                    indexLimitsEachTrial,
                                                                    responseRange)
                base = np.concatenate([base, nspkBase.ravel()])
                spks = np.concatenate([spks, nspkResp.ravel()])
                # inds = np.concatenate([inds, np.ones(len(nspkResp.ravel()))*indfreq])
                freqs = np.concatenate([freqs, np.ones(len(nspkResp.ravel()))*freq])
                allIntenBase = np.concatenate([allIntenBase, nspkBase.ravel()])
                allIntenResp[indinten, indfreq] = np.mean(nspkResp)

        lowFreq = possibleFreq.min()
        highFreq = possibleFreq.max()
        nFreqLabels = 3

        freqTickLocations = np.linspace(0, len(possibleFreq), nFreqLabels)
        freqs = np.logspace(np.log10(lowFreq),np.log10(highFreq),nFreqLabels)
        freqs = np.round(freqs, decimals=1)

        nIntenLabels = 3
        intensities = np.linspace(possibleIntensity.min(), possibleIntensity.max(), nIntenLabels)
        intenTickLocations = np.linspace(0, len(possibleIntensity), nIntenLabels)

        plt.imshow(np.flipud(allIntenResp), interpolation='nearest', cmap='Blues')
        ax5.set_yticks(intenTickLocations)
        ax5.set_yticklabels(intensities[::-1])
        ax5.set_xticks(freqTickLocations)
        freqLabels = ['{0:.1f}'.format(freq) for freq in freqs]
        # ax.set_xticklabels(freqLabels, rotation='vertical')
        ax5.set_xticklabels(freqLabels)
        ax5.set_xlabel('Frequency (kHz)')
        plt.ylabel('Intensity (db SPL)')


    if 'am' in dbRow['sessionType']: #DONE
        #Sorted am raster
        # ax6 = plt.subplot(gs[4:6, 3:6])
        ax6spec = gs[4:6, 3:6]
        ephysData, bdata = cell.load('am')
        eventOnsetTimes = ephysData['events']['stimOn']

        colors = get_colors(len(np.unique(bdata['currentFreq'])))

        timeRange = [-0.5, 1]
        (spikeTimesFromEventOnset,
         trialIndexForEachSpike,
         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(ephysData['spikeTimes'],
                                                                       eventOnsetTimes,
                                                                       timeRange)
        # extraplots.raster_plot(spikeTimesFromEventOnset,
        #                        indexLimitsEachTrial,
        #                        timeRange,
        #                        trialsEachCond=bdata['currentFreq'],
        #                        colorsEachCond=colors)
        plot_example_with_rate(ax6spec, spikeTimesFromEventOnset, indexLimitsEachTrial, bdata['currentFreq'])

        #AM psth
        psthLineWidth = 2
        ax7 = plt.subplot(gs[6:8, 3:6])

        colorEachCond = colors
        binsize = 50
        sortArray = bdata['currentFreq']
        binsize = binsize/1000.0
        # If a sort array is supplied, find the trials that correspond to each value of the array
        trialsEachCond = behavioranalysis.find_trials_each_type(sortArray, np.unique(sortArray))

        (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(ephysData['spikeTimes'],
                                                                     eventOnsetTimes,
                                                                     [timeRange[0]-binsize,
                                                                      timeRange[1]])

        binEdges = np.around(np.arange(timeRange[0]-binsize, timeRange[1]+2*binsize, binsize), decimals=2)
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)
        pPSTH = extraplots.plot_psth(spikeCountMat/binsize, 1, binEdges[:-1], trialsEachCond, colorEachCond=colors)
        plt.setp(pPSTH, lw=psthLineWidth)
        plt.hold(True)
        zline = plt.axvline(0,color='0.75',zorder=-10)
        plt.xlim(timeRange)



    (timestamps,
     samples,
     recordingNumber) = load_all_spikedata(cell)

    #ISI loghist
    ax8 = plt.subplot(gs[8, 0:2])
    if timestamps is not None:
        try:
            spikesorting.plot_isi_loghist(timestamps)
        except:
            # raise AttributeError
            print "problem with isi vals"

    #Waveforms
    ax9 = plt.subplot(gs[8, 2:4])
    if len(samples)>0:
        spikesorting.plot_waveforms(samples)

    #Events in time
    ax10 = plt.subplot(gs[8, 4:6])
    if timestamps is not None:
        try:
            spikesorting.plot_events_in_time(timestamps)
        except:
            print "problem with isi vals"

    fig = plt.gcf()
    fig.set_size_inches(8.5*2, 11*2)

    figName = '{}_{}_{}um_TT{}c{}.png'.format(dbRow['subject'],
                                              dbRow['date'],
                                              int(dbRow['depth']),
                                              int(dbRow['tetrode']),
                                              int(dbRow['cluster']))

    plt.suptitle(figName[:-4])

    figPath = os.path.join(saveDir, figName)
    plt.savefig(figPath)

def get_colors(ncolors):
    ''' returns n distinct colours for plotting purpouses when you don't want to manually specify colours'''
    from matplotlib.pyplot import cm
    colors = cm.viridis(np.linspace(0,1,ncolors))
    return colors
