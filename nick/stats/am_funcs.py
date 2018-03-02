import numpy as np
from jaratest.nick.stats import circstats
from jaratoolbox import spikesanalysis
from jaratest.nick.database import dataloader_v2 as dataloader
from jaratoolbox import behavioranalysis
from jaratest.nick.database import dataplotter
from scipy import stats
from matplotlib import pyplot as plt


#######################3
#Extracts spikes and plots a cycle histogram

# timeRange = [0, 0.5]
# spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
#     spikeTimestamps, eventOnsetTimes, timeRange)

# freq = 128
# select = np.flatnonzero(currentFreq==freq)
# selectspikes = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, select)]
# selectinds = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, select)]
# squeezedinds=np.array([list(np.unique(selectinds)).index(x) for x in selectinds])

# radsPerSec=freq*2*np.pi
# spikeRads = (selectspikes*radsPerSec)%(2*np.pi)
# hist(spikeRads, bins=10*np.pi, histtype='stepfilled', color='k')
# xlim([0, 2*np.pi])

# from jaratest.nick import circstats

# ral_test = circstats.rayleigh_test(spikeRads)

#############################

defaultAMtype = 'am'
eventChannelToUse = 5 #Using the output of the stim detector for AM stuff


def AM_vector_strength(spikeTimestamps, eventOnsetTimes, behavData, timeRange, ignoreBefore=0.03):
    currentFreq = behavData['currentFreq']
    possibleFreq = np.unique(currentFreq)
    vs_array=np.array([])
    ral_array=np.array([])
    pval_array = np.array([])
    timeRange = [0, 0.5]
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeTimestamps, eventOnsetTimes, timeRange)
    for freq in possibleFreq:
        select = np.flatnonzero(currentFreq==freq)
        selectspikes = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, select)]
        selectinds = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, select)]
        squeezedinds=np.array([list(np.unique(selectinds)).index(x) for x in selectinds])
        spikesAfterFirstCycle = selectspikes[selectspikes>ignoreBefore]
        indsAfterFirstCycle = selectinds[selectspikes>ignoreBefore]
        strength, phase = vectorstrength(spikesAfterFirstCycle, 1.0/freq)
        
        vs_array=np.concatenate((vs_array, np.array([strength])))
        #Compute the pval for the vector strength

        radsPerSec=freq*2*np.pi
        spikeRads = (spikesAfterFirstCycle*radsPerSec)%(2*np.pi)
        ral_test = circstats.rayleigh_test(spikeRads)
        pval = np.array([ral_test['pvalue']])
        ral =np.array([2*len(spikesAfterFirstCycle)*(strength**2)]) 
        pval_array = np.concatenate((pval_array, pval))
        ral_array = np.concatenate((ral_array, ral))
    return vs_array, pval_array, ral_array

def average_AM_firing_rate(spikeTimestamps, eventOnsetTimes, behavData, timeRange):

    currentFreq = behavData['currentFreq']
    possibleFreq = np.unique(currentFreq)


    fr_array=np.array([])
    #Only need to calculate this once, the loop then selects for each freq
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeTimestamps, eventOnsetTimes, timeRange)

    for freq in possibleFreq:
        select = np.flatnonzero(currentFreq==freq)
        selectspikes = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, select)]
        selectinds = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, select)]
        selectlimits = indexLimitsEachTrial[:, select]


        numSpikesEachTrial = np.squeeze(np.diff(selectlimits, axis=0))
        spikeRateEachTrial = numSpikesEachTrial / float(timeRange[1]-timeRange[0])
        averageFR = spikeRateEachTrial.mean()

        fr_array=np.concatenate((fr_array, np.array([averageFR])))

    return fr_array

# def vectorstrength(events, period):
#     '''
#     Determine the vector strength of the events corresponding to the given
#     period.
#     The vector strength is a measure of phase synchrony, how well the
#     timing of the events is synchronized to a single period of a periodic
#     signal.
#     If multiple periods are used, calculate the vector strength of each.
#     This is called the "resonating vector strength".
#     Parameters
#     ----------
#     events : 1D array_like
#         An array of time points containing the timing of the events.
#     period : float or array_like
#         The period of the signal that the events should synchronize to.
#         The period is in the same units as `events`.  It can also be an array
#         of periods, in which case the outputs are arrays of the same length.
#     Returns
#     -------
#     strength : float or 1D array
#         The strength of the synchronization.  1.0 is perfect synchronization
#         and 0.0 is no synchronization.  If `period` is an array, this is also
#         an array with each element containing the vector strength at the
#         corresponding period.
#     phase : float or array
#         The phase that the events are most strongly synchronized to in radians.
#         If `period` is an array, this is also an array with each element
#         containing the phase for the corresponding period.
#     References
#     ----------
#     van Hemmen, JL, Longtin, A, and Vollmayr, AN. Testing resonating vector
#         strength: Auditory system, electric fish, and noise.
#         Chaos 21, 047508 (2011);
#         doi: 10.1063/1.3670512
#     van Hemmen, JL.  Vector strength after Goldberg, Brown, and von Mises:
#         biological and mathematical perspectives.  Biol Cybern.
#         2013 Aug;107(4):385-96. doi: 10.1007/s00422-013-0561-7.
#     van Hemmen, JL and Vollmayr, AN.  Resonating vector strength: what happens
#         when we vary the "probing" frequency while keeping the spike times
#         fixed.  Biol Cybern. 2013 Aug;107(4):491-94.
#         doi: 10.1007/s00422-013-0560-8
#     '''
#     events = np.asarray(events)
#     period = np.asarray(period)
#     if events.ndim > 1:
#         raise ValueError('events cannot have dimensions more than 1')
#     if period.ndim > 1:
#         raise ValueError('period cannot have dimensions more than 1')

#     # we need to know later if period was originally a scalar
#     scalarperiod = not period.ndim

#     events = np.atleast_2d(events)
#     period = np.atleast_2d(period)
#     if (period <= 0).any():
#         raise ValueError('periods must be positive')

#     # this converts the times to vectors
#     vectors = np.exp(np.dot(2j*np.pi/period.T, events))

#     # the vector strength is just the magnitude of the mean of the vectors
#     # the vector phase is the angle of the mean of the vectors
#     vectormean = np.mean(vectors, axis=1)
#     strength = abs(vectormean)
#     phase = np.angle(vectormean)

#     # if the original period was a scalar, return scalars
#     if scalarperiod:
#         strength = strength[0]
#         phase = phase[0]
#     return strength, phase

# def am_dependence(cell, frArray=False):
#     '''
#     Calculate the average firing rate of a cell during the 0.5sec AM sound.
#     Perform a linear regression on average firing rate and AM rate, and
#     return the correlation coefficient for the regression.
#     '''

#     try:
#         sessiontypeIndex = cell['sessiontype'].index(defaultAMtype)
#     except ValueError: #The cell does not have this session type
#         return None

#     #Initialize a data loader for this animal
#     loader = dataloader.DataLoader(cell['subject'])

#     #Get the behavior data
#     behavData = loader.get_session_behavior(cell['behavior'][sessiontypeIndex])
#     freqEachTrial = behavData['currentFreq']

#     possibleFreq = np.unique(freqEachTrial)

#     ephysDir = cell['ephys'][sessiontypeIndex]
#     clusterSpikeData = loader.get_session_spikes(ephysDir, int(cell['tetrode']), cluster=int(cell['cluster']))
#     clusterSpikeTimes = clusterSpikeData.timestamps

#     #Get the events for this session and calculate onset times
#     eventData = loader.get_session_events(ephysDir)
#     eventOnsetTimes = loader.get_event_onset_times(eventData, minEventOnsetDiff=None)

#     timeRange = [0, 0.5]

#     trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, possibleFreq)

#     spikeArray = dataplotter.avg_spikes_in_event_locked_timerange_each_cond(clusterSpikeTimes,
#                                                                             trialsEachCond,
#                                                                             eventOnsetTimes,
#                                                                             timeRange)

#     slope, intercept, r_value, p_value, std_err = stats.linregress(spikeArray, possibleFreq)

#     if not frArray:
#         return r_value
#     else:
#         return r_value, spikeArray, possibleFreq

def am_dependence(spikesEachTrial, rateEachTrial):
    '''
    Calculate the average firing rate of a cell during the 0.5sec AM sound.
    Perform a linear regression on average firing rate and AM rate, and
    return the correlation coefficient for the regression.
    '''

    try:
        sessiontypeIndex = cell['sessiontype'].index(defaultAMtype)
    except ValueError: #The cell does not have this session type
        return None

    #Initialize a data loader for this animal
    loader = dataloader.DataLoader(cell['subject'])

    #Get the behavior data
    behavData = loader.get_session_behavior(cell['behavior'][sessiontypeIndex])
    freqEachTrial = behavData['currentFreq']

    possibleFreq = np.unique(freqEachTrial)

    ephysDir = cell['ephys'][sessiontypeIndex]
    clusterSpikeData = loader.get_session_spikes(ephysDir, int(cell['tetrode']), cluster=int(cell['cluster']))
    clusterSpikeTimes = clusterSpikeData.timestamps

    #Get the events for this session and calculate onset times
    eventData = loader.get_session_events(ephysDir)
    eventOnsetTimes = loader.get_event_onset_times(eventData, minEventOnsetDiff=None)

    timeRange = [0, 0.5]

    trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, possibleFreq)

    spikeArray = dataplotter.avg_spikes_in_event_locked_timerange_each_cond(clusterSpikeTimes,
                                                                            trialsEachCond,
                                                                            eventOnsetTimes,
                                                                            timeRange)

    slope, intercept, r_value, p_value, std_err = stats.linregress(spikeArray, possibleFreq)

    if not frArray:
        return r_value
    else:
        return r_value, spikeArray, possibleFreq

def highest_significant_sync(cell):
    try:
        sessiontypeIndex = cell['sessiontype'].index(defaultAMtype)
    except ValueError: #The cell does not have this session type
        return None
    #Initialize a data loader for this animal
    loader = dataloader.DataLoader(cell['subject'])
    #Get the behavior data
    behavData = loader.get_session_behavior(cell['behavior'][sessiontypeIndex])
    freqEachTrial = behavData['currentFreq']
    possibleFreq = np.unique(freqEachTrial)
    ephysDir = cell['ephys'][sessiontypeIndex]
    clusterSpikeData = loader.get_session_spikes(ephysDir, int(cell['tetrode']), cluster=int(cell['cluster']))
    clusterSpikeTimes = clusterSpikeData.timestamps
    #Get the events for this session and calculate onset times
    eventData = loader.get_session_events(ephysDir)
    eventOnsetTimes = loader.get_event_onset_times(eventData, minEventOnsetDiff=None)
    timeRange = [0, 0.5]
    trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, possibleFreq)
    vs_array, pval_array, ral_array = AM_vector_strength(clusterSpikeTimes, eventOnsetTimes, behavData, timeRange)
    if np.any(pval_array<0.05):
        highestSync = np.max(possibleFreq[pval_array<0.05])
    else:
        highestSync = 0
    return highestSync


def plot_am_psth(cell):
    try:
        sessiontypeIndex = cell['sessiontype'].index(defaultAMtype)
    except ValueError: #The cell does not have this session type
        return None

    #Initialize a data loader for this animal
    loader = dataloader.DataLoader(cell['subject'])

    #Get the behavior data
    behavData = loader.get_session_behavior(cell['behavior'][sessiontypeIndex])

    freqEachTrial = behavData['currentFreq']
    possibleFreq = np.unique(freqEachTrial)

    ephysDir = cell['ephys'][sessiontypeIndex]
    clusterSpikeData = loader.get_session_spikes(ephysDir, int(cell['tetrode']), cluster=int(cell['cluster']))
    clusterSpikeTimes = clusterSpikeData.timestamps

    #Get the events for this session and calculate onset times
    eventData = loader.get_session_events(ephysDir)
    eventOnsetTimes = loader.get_event_onset_times(eventData, minEventOnsetDiff=None)

    # timeRange = [-0.1, 0.6]

    # spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(clusterSpikeTimes, eventOnsetTimes, timeRange)

    # colourList = ['b', 'g', 'y', 'orange', 'r']
    nColors = len(possibleFreq)
    # colors = plt.cm.viridis(np.linspace(0, 1, nColors))
    colors = plt.cm.jet(np.linspace(0, 1, nColors))

    # numRates = np.unique(rateEachTrial)
    # trialsEachCond = behavioranalysis.find_trials_each_type(rateEachTrial, numRates)

    dataplotter.plot_psth(clusterSpikeTimes, eventOnsetTimes, freqEachTrial, timeRange = [-0.2, 0.8], binsize = 50, colorEachCond = colors)

    plt.xlabel('Time from sound onset (sec)')
    plt.ylabel('Firing rate (Hz)')
    plt.title('AM PSTH')

def plot_am_raster(cell):
    try:
        sessiontypeIndex = cell['sessiontype'].index(defaultAMtype)
    except ValueError: #The cell does not have this session type
        return None

    #Initialize a data loader for this animal
    loader = dataloader.DataLoader(cell['subject'])

    #Get the behavior data
    behavData = loader.get_session_behavior(cell['behavior'][sessiontypeIndex])

    freqEachTrial = behavData['currentFreq']
    possibleFreq = np.unique(freqEachTrial)

    ephysDir = cell['ephys'][sessiontypeIndex]
    clusterSpikeData = loader.get_session_spikes(ephysDir, int(cell['tetrode']), cluster=int(cell['cluster']))
    clusterSpikeTimes = clusterSpikeData.timestamps

    #Get the events for this session and calculate onset times
    eventData = loader.get_session_events(ephysDir)
    eventOnsetTimes = loader.get_event_onset_times(eventData, minEventOnsetDiff=None)

    timeRange = [-0.2, 0.8]
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(clusterSpikeTimes, eventOnsetTimes, timeRange)

    nColors = len(possibleFreq)
    # colors = plt.cm.viridis(np.linspace(0, 1, nColors))
    colors = plt.cm.jet(np.linspace(0, 1, nColors))

    freqLabels = ["%.0f" % rate for rate in np.unique(freqEachTrial)]
    dataplotter.plot_raster(clusterSpikeTimes, eventOnsetTimes, sortArray=freqEachTrial, timeRange=[-0.2, 0.8], labels=freqLabels, colorEachCond=colors)
    plt.xlabel('Time from sound onset (sec)')
    plt.ylabel('Modulation Rate (Hz)')
    plt.title('AM Raster')
