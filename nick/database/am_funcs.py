import numpy as np
from jaratoolbox.test.nick import circstats
from jaratoolbox import spikesanalysis


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

# from jaratoolbox.test.nick import circstats

# ral_test = circstats.rayleigh_test(spikeRads)

#############################



def AM_vector_strength(spikeTimestamps, eventOnsetTimes, behavData, timeRange):

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

        spikesAfterFirstCycle = selectspikes[selectspikes>(1.0/freq)]
        indsAfterFirstCycle = selectinds[selectspikes>(1.0/freq)]

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

def vectorstrength(events, period):
    '''
    Determine the vector strength of the events corresponding to the given
    period.
    The vector strength is a measure of phase synchrony, how well the
    timing of the events is synchronized to a single period of a periodic
    signal.
    If multiple periods are used, calculate the vector strength of each.
    This is called the "resonating vector strength".
    Parameters
    ----------
    events : 1D array_like
        An array of time points containing the timing of the events.
    period : float or array_like
        The period of the signal that the events should synchronize to.
        The period is in the same units as `events`.  It can also be an array
        of periods, in which case the outputs are arrays of the same length.
    Returns
    -------
    strength : float or 1D array
        The strength of the synchronization.  1.0 is perfect synchronization
        and 0.0 is no synchronization.  If `period` is an array, this is also
        an array with each element containing the vector strength at the
        corresponding period.
    phase : float or array
        The phase that the events are most strongly synchronized to in radians.
        If `period` is an array, this is also an array with each element
        containing the phase for the corresponding period.
    References
    ----------
    van Hemmen, JL, Longtin, A, and Vollmayr, AN. Testing resonating vector
        strength: Auditory system, electric fish, and noise.
        Chaos 21, 047508 (2011);
        doi: 10.1063/1.3670512
    van Hemmen, JL.  Vector strength after Goldberg, Brown, and von Mises:
        biological and mathematical perspectives.  Biol Cybern.
        2013 Aug;107(4):385-96. doi: 10.1007/s00422-013-0561-7.
    van Hemmen, JL and Vollmayr, AN.  Resonating vector strength: what happens
        when we vary the "probing" frequency while keeping the spike times
        fixed.  Biol Cybern. 2013 Aug;107(4):491-94.
        doi: 10.1007/s00422-013-0560-8
    '''
    events = np.asarray(events)
    period = np.asarray(period)
    if events.ndim > 1:
        raise ValueError('events cannot have dimensions more than 1')
    if period.ndim > 1:
        raise ValueError('period cannot have dimensions more than 1')

    # we need to know later if period was originally a scalar
    scalarperiod = not period.ndim

    events = np.atleast_2d(events)
    period = np.atleast_2d(period)
    if (period <= 0).any():
        raise ValueError('periods must be positive')

    # this converts the times to vectors
    vectors = np.exp(np.dot(2j*np.pi/period.T, events))

    # the vector strength is just the magnitude of the mean of the vectors
    # the vector phase is the angle of the mean of the vectors
    vectormean = np.mean(vectors, axis=1)
    strength = abs(vectormean)
    phase = np.angle(vectormean)

    # if the original period was a scalar, return scalars
    if scalarperiod:
        strength = strength[0]
        phase = phase[0]
    return strength, phase
