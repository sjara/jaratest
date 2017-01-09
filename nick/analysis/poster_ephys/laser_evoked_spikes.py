from matplotlib import pyplot as plt
import pandas
import numpy as np
from jaratest.nick.database import dataloader_v2 as dataloader
from jaratest.nick.database import dataplotter
from jaratoolbox import colorpalette
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import clusteranalysis

thaldbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb_q10.pickle'
cortdbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb_q10.pickle'
thaldb = pandas.read_pickle(thaldbfn)
cortdb = pandas.read_pickle(cortdbfn)

def average_waveform_in_timerange(spikeSamples, spikeTimes, eventOnsetTimes, timeRange):

    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial, spikeIndices = spikesanalysis.eventlocked_spiketimes(
        spikeTimes,
        eventOnsetTimes,
        timeRange,
        spikeindex=True)
    samplesToPlot = spikeSamples[spikeIndices]
    ax = plt.gca()
    alignedWaveforms = spikesorting.align_waveforms(samplesToPlot)
    meanWaveforms = np.mean(alignedWaveforms,axis=0)
    stdWaveforms = np.std(alignedWaveforms, axis=0)
    allWaveforms = meanWaveforms.flatten()
    allStd = stdWaveforms.flatten()
    return allWaveforms, allStd

def compare_laser_spikeshapes(cell):
    try:
        sessiontypeIndex = cell['sessiontype'].index('LaserPulse')
    except ValueError: #The cell does not have this session type
        return numpy.nan, numpy.nan

    loader = dataloader.DataLoader(cell['subject'])
    clusterSpikeData = loader.get_session_spikes(cell['ephys'][sessiontypeIndex],
                                                cluster=int(cell['cluster']),
                                                tetrode=int(cell['tetrode']))
    eventData = loader.get_session_events(cell['ephys'][sessiontypeIndex])
    eventOnsetTimes = loader.get_event_onset_times(eventData)

    spontRange = [-0.1, -0]
    evokedRange = [0, 0.1]

    samples = clusterSpikeData.samples
    timestamps = clusterSpikeData.timestamps

    spontWaveform, spontStd = average_waveform_in_timerange(samples, timestamps,
                                                eventOnsetTimes, spontRange)
    evokedWaveform, evokedStd = average_waveform_in_timerange(samples, timestamps,
                                                eventOnsetTimes, evokedRange)

    return spontWaveform, evokedWaveform, spontStd, evokedStd

def extract_peak_window(waveform, binEdges=[0, 40, 80, 120, 160]):
    '''
    Get just the electrode with the largest spike shape for plotting
    '''
    maxima = []
    windows = zip(binEdges, binEdges[1:])
    for start, end in windows:
        maxima.append(np.max(waveform[start:end]))
    start, end = windows[np.argmax(maxima)]
    return waveform[start:end]

if __name__=="__main__":
    database = thaldb

    CASE=3

    if CASE==1:
        for indcell, cell in database.iterrows():
            spontWaveform, evokedWaveform, _, _ = compare_laser_spikeshapes(cell)
            plt.clf()
            plt.plot(spontWaveform, 'k')
            plt.plot(evokedWaveform, 'b')
            plt.waitforbuttonpress()

    elif CASE==2:
        corrVals = np.empty(len(database))
        for indcell, cell in database.iterrows():
            spontWaveform, evokedWaveform, _, _ = compare_laser_spikeshapes(cell)
            corr = np.corrcoef(x=spontWaveform, y=evokedWaveform)
            corrVals[indcell] = corr[0,1]
            database['laserEvokedCorrelation'] = corrVals
    elif CASE==3:

        goodcells = (database['isiViolations']<4) & (database['noiseburstZ']>2) & (database['lasertrainZ']>2)

        counter = 0
        mins = []
        maxs = []
        plt.clf()
        fig, axes = plt.subplots(4, 3)
        axes = axes.reshape(-1)
        plt.axis('off')

        for indcell, cell in database[goodcells][3:15].iterrows():

            spontWaveform, evokedWaveform, spontStd, evokedStd = compare_laser_spikeshapes(cell)

            mins.append(min(spontWaveform))
            maxs.append(max(evokedWaveform))


            spontWaveform = extract_peak_window(spontWaveform)
            evokedWaveform = extract_peak_window(evokedWaveform)

            timebase = range(len(spontWaveform))
            axes[counter].plot(timebase, spontWaveform, color='k', lw=3)
            axes[counter].plot(timebase, evokedWaveform, color='deepskyblue', lw=3)
            axes[counter].set_axis_off()

            counter+=1

        for ax in axes:
            ax.set_ylim([min(mins)-5, max(maxs)+5])

        scalebarSizeY = 30 #mv
        scalebarSizeX = 30 #samples, 1ms

        start = [-7, 30]
        axes[0].plot(2*[start[0]],[start[1],start[1]-scalebarSizeY],color='0.5',lw=2)
        axes[0].plot([start[0],start[0]+scalebarSizeX], 2*[start[1]],color='0.5',lw=2)

        plt.show()



