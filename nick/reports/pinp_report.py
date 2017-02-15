import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os

from jaratoolbox import settings
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots

from jaratest.nick.database import dataplotter

#Define the gridspec for the report

def plot_pinp_report(cell, saveDir):
    plt.clf()
    gs = gridspec.GridSpec(9, 6)

    #Laser pulse raster
    ax0 = plt.subplot(gs[0:2, 0:3])
    if 'laserpulse' in cell['sessiontype']:
        spikeData, eventData = get_session_ephys(cell, 'laserpulse')
        eventOnsetTimes = eventData.get_event_onset_times()

        # timeRange = [-0.5, 1]
        # (spikeTimesFromEventOnset,
        #  trialIndexForEachSpike,
        #  indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
        #                                                                eventOnsetTimes,
        #                                                                timeRange)
        # extraplots.raster_plot(spikeTimesFromEventOnset,
        #                        indexLimitsEachTrial,
        #                        timeRange)
        if spikeData.timestamps is not None:
            dataplotter.plot_raster(spikeData.timestamps, eventOnsetTimes)

    #Laser pulse psth
    ax1 = plt.subplot(gs[2:4, 0:3])
    if 'laserpulse' in cell['sessiontype']:
        spikeData, eventData = get_session_ephys(cell, 'laserpulse')
        if spikeData.timestamps is not None:
            dataplotter.plot_psth(spikeData.timestamps, eventOnsetTimes)

    #Laser train raster
    ax2 = plt.subplot(gs[0:2, 3:6])
    spikeData, eventData = get_session_ephys(cell, 'lasertrain')
    eventOnsetTimes = eventData.get_event_onset_times()
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)
    if spikeData.timestamps is not None:
        dataplotter.plot_raster(spikeData.timestamps, eventOnsetTimes)

    #Laser train psth
    ax3 = plt.subplot(gs[2:4, 3:6])
    if spikeData.timestamps is not None:
        dataplotter.plot_psth(spikeData.timestamps, eventOnsetTimes)

    #Sorted tuning raster
    ax4 = plt.subplot(gs[4:6, 0:3])
    spikeData, eventData = get_session_ephys(cell, 'tc')
    eventOnsetTimes = eventData.get_event_onset_times()
    bdata = get_session_bdata(cell, 'tc')
    if spikeData.timestamps is not None:
        dataplotter.plot_raster(spikeData.timestamps, eventOnsetTimes, sortArray=bdata['currentFreq'])

    #TC heatmap
    ax5 = plt.subplot(gs[6:8, 0:3])
    if spikeData.timestamps is not None:
        try:
            dataplotter.two_axis_heatmap(spikeData.timestamps,
                                        eventOnsetTimes,
                                        firstSortArray = bdata['currentIntensity'],
                                        secondSortArray = bdata['currentFreq'])
        except:
            print 'TC heatmap error'

    #Sorted am raster
    ax6 = plt.subplot(gs[4:6, 3:6])
    spikeData, eventData = get_session_ephys(cell, 'am')
    eventOnsetTimes = eventData.get_event_onset_times()
    bdata = get_session_bdata(cell, 'am')
    colors = get_colors(len(np.unique(bdata['currentFreq'])))
    if spikeData.timestamps is not None:
        dataplotter.plot_raster(spikeData.timestamps,
                                eventOnsetTimes,
                                sortArray=bdata['currentFreq'],
                                colorEachCond=colors)

    #AM psth
    ax7 = plt.subplot(gs[6:8, 3:6])
    if spikeData.timestamps is not None:
        dataplotter.plot_psth(spikeData.timestamps,
                            eventOnsetTimes,
                            sortArray=bdata['currentFreq'],
                            colorEachCond=colors)


    (timestamps,
     samples,
     recordingNumber) = load_all_spikedata(cell)

    #ISI loghist
    ax8 = plt.subplot(gs[8, 0:2])
    if timestamps is not None:
        try:
            spikesorting.plot_isi_loghist(timestamps)
        except:
            raise AttributeError
            print "problem with isi vals"

    #Waveforms
    ax9 = plt.subplot(gs[8, 2:4])
    if timestamps is not None:
        spikesorting.plot_waveforms(samples)

    #Events in time
    ax10 = plt.subplot(gs[8, 4:6])
    if timestamps is not None:
        try:
            spikesorting.plot_events_in_time(timestamps)
        except:
            print "problem with isi vals"

    fig = plt.gcf()
    fig.set_size_inches(8.5, 11)

    figName = 'exp{}site{}tetrode{}c{}.png'.format(int(cell['experimentInd']),
                                                   int(cell['siteInd']),
                                                   int(cell['tetrode']),
                                                   int(cell['cluster']))
    figPath = os.path.join(saveDir, figName)
    plt.savefig(figPath)

def get_colors(ncolors):
    ''' returns n distinct colours for plotting purpouses when you don't want to manually specify colours'''
    from matplotlib.pyplot import cm
    colors = cm.viridis(np.linspace(0,1,ncolors))
    return colors

def get_session_inds(cell, sessiontype):
    return [i for i, st in enumerate(cell['sessiontype']) if st==sessiontype]

def get_session_bdata(cell, sessiontype):
    sessionInds = get_session_inds(cell, sessiontype)
    sessionInd = sessionInds[0] #FIXME: Just takes the first one for now
    behavFile = cell['behavior'][sessionInd]
    behavDataFilePath=os.path.join(settings.BEHAVIOR_PATH, cell['subject'], behavFile)
    bdata = loadbehavior.BehaviorData(behavDataFilePath,readmode='full')
    return bdata

def convert_openephys(dataObj):
    '''
    Converts to seconds and milivolts
    '''
    if hasattr(dataObj, 'samples'):
        dataObj.samples = dataObj.samples.astype(float)-2**15
        dataObj.samples = (1000.0/dataObj.gain[0,0]) * dataObj.samples
    if hasattr(dataObj, 'timestamps'):
        dataObj.timestamps = dataObj.timestamps/dataObj.samplingRate
    return dataObj

def get_session_ephys(cell, sessiontype):
    sessionInds = get_session_inds(cell, sessiontype)
    sessionInd = sessionInds[0] #FIXME: Just takes the first one for now
    ephysSession = cell['ephys'][sessionInd]
    ephysBaseDir = os.path.join(settings.EPHYS_PATH, cell['subject'])
    tetrode=int(cell['tetrode'])
    eventFilename=os.path.join(ephysBaseDir,
                               ephysSession,
                               'all_channels.events')
    spikesFilename=os.path.join(ephysBaseDir,
                                ephysSession,
                                'Tetrode{}.spikes'.format(tetrode))
    eventData=loadopenephys.Events(eventFilename)
    spikeData = loadopenephys.DataSpikes(spikesFilename)
    if spikeData.timestamps is not None:
        clustersDir = os.path.join(ephysBaseDir, '{}_kk'.format(ephysSession))
        clustersFile = os.path.join(clustersDir,'Tetrode{}.clu.1'.format(tetrode))
        spikeData.set_clusters(clustersFile)
        spikeData.samples=spikeData.samples[spikeData.clusters==cell['cluster']]
        spikeData.timestamps=spikeData.timestamps[spikeData.clusters==cell['cluster']]
        spikeData = convert_openephys(spikeData)
    eventData = convert_openephys(eventData)
    return spikeData, eventData

# def convert_openephys(spikeData, eventData):
#     '''
#     Converts to seconds and milivolts
#     '''
#     spikeData.samples = spikeData.samples.astype(float)-2**15
#     spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
#     spikeData.timestamps = spikeData.timestamps/spikeData.samplingRate
#     eventData.timestamps = np.array(eventData.timestamps)/eventData.samplingRate
#     return spikeData, eventData


def load_all_spikedata(cell):
    samples=None
    timestamps=None
    recordingNumber=None

    for ind, sessionType in enumerate(cell['sessiontype']):
        dataSpkObj, dataEvents = get_session_ephys(cell, sessionType)
        if dataSpkObj.timestamps is None:
            continue

        numSpikes = len(dataSpkObj.timestamps)
        sessionVector = np.zeros(numSpikes)+ind

        if samples is None:
            samples = dataSpkObj.samples
            timestamps = dataSpkObj.timestamps
            recordingNumber = sessionVector
        else:
            samples = np.concatenate([samples, dataSpkObj.samples])
            timestamps = np.concatenate([timestamps, dataSpkObj.timestamps])
            recordingNumber = np.concatenate([recordingNumber, sessionVector])

    return timestamps, samples, recordingNumber

def calculate_laser_train_reliability(cell):
    spikeData, eventData = get_session_ephys(cell, 'lasertrain')
    eventOnsetTimes = eventData.get_event_onset_times()
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)

    lasertimes = [0, 0.2, 0.4, 0.6, 0.8]
    windows = np.array([np.array([x, x+0.05]) for x in lasertimes])

    for window in windows:
        (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                      eventOnsetTimes,
                                                                      window)


        spikeCountMat = spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                  indexLimitsEachTrial,
                                                  binEdges)







