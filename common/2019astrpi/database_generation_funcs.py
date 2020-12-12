"""
Contains all functions used in database_generation.py that don't come from
standard libraries or jaratoolbox.
"""
import numpy as np
import copy
from numpy import inf
from scipy import optimize
from scipy import signal
from scipy import stats
from collections import Counter
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis


def gaussian(x, a, x0, sigma, y0):
    """
    Gaussian function
    Args:
        x (numpy.ndarray): input data
        a (float?): the height of the curve's peak
        x0 (float?): the position of the center of the peak
        sigma (float?): standard variation that determines the width of the 'bell'
        y0 (float?): constant

    Returns:
        output of gaussian function
    """
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+y0
#FIXME I am unsure of the types for the items in the docstring above so it's a best guess based on what I could find


def retrofit_gaussian_log2(y, a, x0, sigma, y0):
    """
    Reverse function of gaussian. Not to confuse with inverse gaussian,
    which is description of Brownian motion with positive drift to reach the
    fixed positive level. This function finds the lower and upper frequencies
    with desirable response threshold output, and optimal parameters (*popt)
    for 10dB above the current bandwidth

    Args:
        y (numpy.ndarray): Gaussian fit
        a (float): the height of the curve's peak
        x0 (float): the position of the center of the peak
        sigma (float): standard variation that determines the width of the 'bell'
        y0 (float): constant

    Returns:
        lower (flaot): Value of the lower boundary of the gaussian at a set
        intensity
        upper (float): Value of the upper boundary of the gaussian at a set
        intensity
    """
    sqrtInner = -1*np.log((y-y0)/a)*2*sigma**2
    if sqrtInner < 0:  # No solutions
        return None
    else:
        lower = 2**(x0 - np.sqrt(sqrtInner))
        upper = 2**(x0 + np.sqrt(sqrtInner))
        return [lower, upper]


def calculate_firing_rate(eventOnsetTimes, spikeTimes, baseRange, selectinds=[]):
    """
    Creates functions for calculating spike rates
    Within the function, the module calculates response range(responseRange),
    and entire range(alignmentRange). Response range mirrors baseRange but on the
    post-stimulus time. It has the equal time distance from the stimulus
    and the same amount of time range as baseRange
    Args:
        eventOnsetTimes (numpy.ndarray): [nTrials, 1], each row is the time of the
            trial start
        spikeTimes (numpy.ndarray): [nTrials, 1], each row is a timestamp for when
            a spike was detected
        baseRange (list): [startTime, endTime], contains the time range defined
            for the baseline spikes
        selectinds (numpy.ndarray): indices of event onset time points for specific
            frequency and specific intensity, used for frequency tuning analysis,
            empty by default

    Returns:
        nspkBase (numpy.ndarray): [ntrials, 1], each row represents the number
            of spikes occured in the trial within base range(pre-stimulus)
        nspkResp (numpy.ndarray): [ntrials, 1], each row represents the nubmer
            of spikes occured in the trial within response range(post-stimulus)
    """
    if selectinds != []:
        # =====================index mismatch correction========================
        while selectinds[-1] >= eventOnsetTimes.shape[0]:
            selectinds = np.delete(selectinds, -1, 0)
    # -----------------end of correction--------------------------------------
        eventOnsetTimes = eventOnsetTimes[selectinds]

    binTime = baseRange[1]-baseRange[0]
    responseRangeStart = baseRange[1]*(-1)  # if session != laserpulse else 0
    responseRange = [responseRangeStart, responseRangeStart+binTime]
    alignmentRange = [baseRange[0], responseRange[1]]

    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   alignmentRange)
    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial, baseRange)
    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial, responseRange)
    return nspkBase, nspkResp


def calculate_fit_params(uniqFreq, allIntenBase):
    """
    Defines fit input parameters for a Gaussian
    Args:
        uniqFreq (numpy.ndarray): Contains unique frequencies presented during
            the session
        allIntenBase (numpy.ndarray): Cumulated number of spikes on pre-stimulus
            range with all frequencies and all intensities

    Returns:
        p0 (list): initial guess parameters to fit to
        bounds (tuple): lower and upper boundaries
    """
    p0 = [1, np.log2(uniqFreq[7]), 1, allIntenBase.mean()]
    bounds = ([0, np.log(uniqFreq[0]), 0, 0], [inf, np.log2(uniqFreq[-1]), inf, inf])
    return p0, bounds


def calculate_fit(uniqFreq, allIntenBase, freqs, spks):
    """
    Calculates curve fitting with given pre-stimulus spikes
    Args:
        Used for calculate_fit_params:
            uniqFreq (numpy.ndarray): Contains unique frequencies presented during
                the session
            allIntenBase (numpy.ndarray): cumulated number of spikes on pre-stimulus
                range with all frequencies and intensities
        Used for curve_fit:
            freqs (numpy.ndarray): [total ntrials of all frequencies in response range]
                each number represents frequency of a specific trial
            spks (numpy.ndarray): [total ntrials of all frequencies in response range]
                an array of spikes in each trial

    Returns:
        Rsquared (float): R-squared value of the curve
        popt (list?): optimal parameters for the gaussian curve
    """
    p0, bounds = calculate_fit_params(uniqFreq, allIntenBase)

    try:
        popt, pcov = optimize.curve_fit(gaussian, np.log2(freqs), spks, p0=p0, bounds=bounds)

        gaussianResp = gaussian(np.log2(freqs), *popt)
        residuals = spks - gaussianResp
        ssquared = np.sum(residuals**2)
        ssTotal = np.sum((spks-np.mean(spks))**2)
        Rsquared = 1 - (ssquared/ssTotal)
        # corrcoeff,_ = stats.pearsonr(spks, gaussianResp)
        # Rsquared = corrcoeff**2

    except RuntimeError:
        print("Could not fit gaussian curve to tuning data.")
        Rsquared, popt = None, None  # gaussianResp

    return Rsquared, popt


def calculate_response_threshold(fraThreshold, allIntenBase, respSpikeMean):
    """
    Response threshold is defined to be the baseline firing rate plus
    20%(fraThreshold) of the difference between baseline and the cell's maximum
    firing rate under any condition
    (Sutter and Schreiner, https://doi.org/10.1152/jn.1991.65.5.1207)
    Args:
        fraThreshold (float): Chosen firing rate threshold for the frequency
            response area
        allIntenBase (numpy.ndarray): [nTrials, 1], each value is the number of
            spikes
        respSpikeMean (numpy.ndarray): [Intensity, Frequency], each value is the
            mean number of spikes at a specific frequency and intensity combination

    Returns:
        Response threshold value (float)
    """
    return allIntenBase.mean() + fraThreshold*(respSpikeMean.max()-allIntenBase.mean())


def calculate_intensity_threshold_and_CF_indices(fra, respSpikeMean, threshold=0.85):
    """
    Calculates intensity threshold index and characteristic frequency(CF) index.
    Neuron's CF is defined as the frequency with the lowest sound intensity inside
    the FRA where 85%(theshold) of the intensities above were also within the FRA
    Args:
        fra (numpy.ndarray): boolean array of shape (nInten, nFreq). Higher index
            means higher intensity
        respSpikeMean (numpy.ndarray): response spike number array of shape
        (nInten, nFreq). Higher index = higher intensity
        threshold (float): At least this proportion of the intensities above
            must have a response for the freq to be cf

    Returns:
        intensityInd (int): intensity threshold index
        freqInd (int): characteristic frequency(CF) index
    """
    results = []
    for inten, row in enumerate(fra):
        for indCol, column in enumerate(row):
            if column:
                colAbove = fra[inten:, indCol]
                if colAbove.mean() > threshold:
                    results.append((inten, indCol))
            else:
                resultWithMaxFiring = (None, None)
    resultIntenInds = [a for a, b in results]
    try:
        minResultIntenInd = min(resultIntenInds)

    except ValueError:
        resultWithMaxFiring = (None, None)

    else:
        resultsAtMinInten = [(a, b) for a, b in results if a == minResultIntenInd]
        resultSpikeCounts = [respSpikeMean[a, b] for a, b in resultsAtMinInten]
        resultWithMaxFiring = resultsAtMinInten[resultSpikeCounts.index(np.max(resultSpikeCounts))]

    intensityInd, freqInd = resultWithMaxFiring

    return intensityInd, freqInd


def calculate_BW10_params(ind10Above, popts, Rsquareds, responseThreshold, intensityThreshold):
    """
    Calculates lower/upper frequencies and Rsquared value for 10dB above the
    sound intensity threshold(SIT) with given index at 10dB above
    SIT(ind10Above)
    Args:
        ind10Above (int): represents the index of intensity threshold plus 10dB
        popts: optimal parameters for gaussian curve
        Rsquareds (list): Rsquare value for each intensity presented, with the
            intensities in sequential order
        responseThreshold (float): response firing threshold
        intensityThreshold (float): minimum intensity where 85% of the rest of
            intensity above is within FRA

    Returns:
        lowerFreq (float): lower bound frequency of BW10
        upperFreq (float): upper bound frequency of BW10
        Rsquared10AboveSIT (float) : mean rsquared value of intensity threshold
        plus 10dB

    """

    try:
        popt10AboveSIT = popts[ind10Above]
        Rsquared10AboveSIT = Rsquareds[ind10Above]
        if popt10AboveSIT is None:
            print("Index returns empty array")  # FIXME: This was done to catch a niche circumstance when the index 10 above grabs an empty array (Ex: Now processing ', 'd1pi041', '2019-08-25', 3400.0, 7, 6, 1410)
            raise IndexError
    except IndexError:
        print("Failure indexerror didn't get 10 above")
        print(intensityThreshold)
        # This is for the instance when we are not able to catch 10dB above threshold.
        # Even then we can still get cf and threshold, but not upperFreq/lowerFreq
        upperFreq = None
        lowerFreq = None
        Rsquared10AboveSIT = np.nan

    else:
        freqLimits = retrofit_gaussian_log2(responseThreshold, *popt10AboveSIT)

        if freqLimits is not None:
            lowerFreq, upperFreq = freqLimits
        else:
            # ind10AboveButNone.append(indRow)
            lowerFreq = None
            upperFreq = None
            Rsquared10AboveSIT = np.nan

    return lowerFreq, upperFreq, Rsquared10AboveSIT


def calculate_latency(eventOnsetTimes, currentFreq,  uniqFreq, currentIntensity, uniqueIntensity, spikeTimes):
    """
    Calculate the time between a sound being presented and a neuron responding
    to it
    Args:
        eventOnsetTimes (numpy.ndarray): Same size as the number of trials with
            each value being the time sound detector turned on
        currentFreq (numpy.ndarray): Same size as number of trials presented with
            each value being a specific frequency for that trial
        currentIntensity (numpy.ndarray): Same size as number of trials presented
            with each value being a specific intensity for that trial
        uniqueIntensity (numpy.ndarray): Uses currentIntensity to find how many
            unique intensity values were presented and store each unique value
        uniqFreq (numpy.ndarray): Uses currentFreq to find how many unique frequency
            values were presented and store each unique value
        spikeTimes (numpy.ndarray): Each value is a time when a spike occurred;
            obtained from ephys data

    Returns:
        respLatency (float): Time, in seconds, from when the stimulus is
            presented and the cell responds

    """

    trialsEachCondition = behavioranalysis.find_trials_each_combination(currentIntensity, uniqueIntensity,
                                                                        currentFreq, uniqFreq)

    baseRange = [-0.1, 0]
    responseRange = [0, 0.1]
    alignmentRange = [-0.2, 0.2]
    thresholdFRA = 0.2

    # Align all spikes to events
    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   alignmentRange)

    # Count spikes in baseline and response ranges
    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        baseRange)
    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        responseRange)

    # Filter and average the response spikes by the condition matrix
    conditionMatShape = np.shape(trialsEachCondition)
    numRepeats = np.product(conditionMatShape[1:])
    nSpikesMat = np.reshape(nspkResp.squeeze().repeat(numRepeats), conditionMatShape)
    spikesFilteredByTrialType = nSpikesMat * trialsEachCondition
    avgRespArray = np.sum(spikesFilteredByTrialType, 0) / np.sum(
        trialsEachCondition, 0).astype('float')

    thresholdResponse = nspkBase.mean() + thresholdFRA * (avgRespArray.max() - nspkBase.mean())

    if not np.any(avgRespArray > thresholdResponse):
        print("Nothing above the threshold")
        respLatency = np.nan
        return respLatency

    # Determine trials that come from a I/F pair with a response above the threshold
    fra = avgRespArray > thresholdResponse
    selectedTrials = np.any(trialsEachCondition[:, fra], axis=1)

    # -- Calculate response latency --
    indexLimitsSelectedTrials = indexLimitsEachTrial[:, selectedTrials]
    timeRangeForLatency = [-0.1, 0.1]
    (respLatency, interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
                                                             indexLimitsSelectedTrials,
                                                             timeRangeForLatency, threshold=0.5,
                                                             win=signal.hanning(11))

    print('Response latency: {:0.1f} ms'.format(1e3 * respLatency))

    return respLatency


def calculate_monotonicity_index(eventOnsetTimes, currentFreq, currentIntensity, uniqueIntensity, spikeTimes, cf):
    """

    Args:
        eventOnsetTimes (numpy.ndarray): Same size as the number of trials with each
            value being the time sound detector turned on
        currentFreq (numpy.ndarray): Same size as number of trials presented with each
            value being a specific frequency for that trial
        currentIntensity (numpy.ndarray): Same size as number of trials presented
            with each value being a specific intensity for that trial
        uniqueIntensity (numpy.ndarray): Uses currentIntensity to find how many unique
            intensity values were presented and store each unique value in
            ascending order
        spikeTimes (numpy.ndarray): Each value is a time when a spike occurred;
            obtained from ephys data
        cf (float): Characteristic frequency of the cell, calculated by analyzing
            lowest threshold value for a cell

    Returns:
        monoIndex (float): Index value for monotonicity of a cell, between 0
            and 1
        overallMaxSpikes (float): Mean number of spikes at the intensity that
            had the most spikes for a stimulus
    """

    # if len(eventOnsetTimes) != len(freqEachTrial):
    #     eventOnsetTimes = eventOnsetTimes[:-1]
    #     if len(eventOnsetTimes) != len(freqEachTrial):
    #         continue
    # cfTrials = currentFreq == dbRow['cf']  # cf is characteristic frequency
    cfTrials = currentFreq == cf
    eventsThisFreq = eventOnsetTimes[cfTrials]
    intenThisFreq = currentIntensity[cfTrials]

    baseRange = [-0.1, 0]
    responseRange = [0, 0.1]
    alignmentRange = [baseRange[0], responseRange[1]]

    meanSpikesAllInten = np.empty(len(uniqueIntensity))
    maxSpikesAllInten = np.empty(len(uniqueIntensity))
    baseSpikesAllInten = np.empty(len(uniqueIntensity))
    for indInten, inten in enumerate(uniqueIntensity):
        # print inten
        trialsThisIntensity = intenThisFreq == inten
        eventsThisCombo = eventsThisFreq[trialsThisIntensity]

        (spikeTimesFromEventOnset,
         trialIndexForEachSpike,
         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                       eventsThisCombo,
                                                                       alignmentRange)
        nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            baseRange)
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            responseRange)

        spikesThisInten = nspkResp[:, 0]
        baselineThisInten = nspkBase[:, 0]
        # print spikesThisInten
        try:
            meanSpikesThisInten = np.mean(spikesThisInten)
            meanBaselineSpikesThisInten = np.mean(baselineThisInten)
            maxSpikesThisInten = np.max(spikesThisInten)
        except ValueError:
            meanSpikesThisInten = 0
            maxSpikesThisInten = 0
            meanBaselineSpikesThisInten = 0

        meanSpikesAllInten[indInten] = meanSpikesThisInten
        maxSpikesAllInten[indInten] = maxSpikesThisInten
        baseSpikesAllInten[indInten] = meanBaselineSpikesThisInten

    baseline = np.mean(baseSpikesAllInten)
    monoIndex = (meanSpikesAllInten[-1] - baseline) / (np.max(meanSpikesAllInten) - baseline)

    overallMaxSpikes = np.max(maxSpikesAllInten)

    return monoIndex, overallMaxSpikes


def calculate_onset_to_sustained_ratio(eventOnsetTimes, spikeTimes, currentFreq, currentIntensity, uniqIntensity,
                                       cf, respLatency):
    """
    Find the ratio of onset firing rate of the cell to the sustained firing rate
    of the cell. Selects subset of trials  with the CF and the top 5 intensities
    Args:
        eventOnsetTimes (numpy.ndarray): Same size as the number of trials with each
            value being the time sound detector turned on
        spikeTimes (numpy.ndarray): Each value is a time when a spike occurred;
            obtained from ephys data
        currentFreq (numpy.ndarray): Same size as number of trials presented with
            each value being a specific frequency for that trial
        currentIntensity (numpy.ndarray): Same size as number of trials presented with
            each value being a specific intensity for that trial
        uniqIntensity (numpy.ndarray): Uses currentIntensity to find how many unique
            intensity values were presented and store each unique value in
            ascending order
        cf (float): The characteristic frequency of the neuron
        respLatency (float): Time in seconds that the cell takes to respond to
            the stimulus being presented
    Returns:
        onsetRate (float): The number of spikes that happen within the response
            time range
        sustainedRate (float): The number of spikes that happen within the
            sustained time range
        baseRate (float): The number of spikes that happen within the baseline
            time range

    """
    cfTrials = currentFreq == cf
    eventsThisFreq = eventOnsetTimes[cfTrials]
    intenThisFreq = currentIntensity[cfTrials]

    # Get only the trials with the CF and the top 5 intensities
    if len(uniqIntensity) > 4:
        intenToUse = uniqIntensity[-5:]
    else:
        intenToUse = uniqIntensity

    # Boolean of which trials from this frequency were high intensity
    highIntenTrials = np.in1d(intenThisFreq, intenToUse)

    # Filter the events this frequency to just take the ones from high intensity
    eventsThisFreqHighIntensity = eventsThisFreq[highIntenTrials]

    if not respLatency > 0:
        print("Negative latency!! Skipping")
        onsetRate = np.nan
        sustainedRate = np.nan
        baseRate = np.nan
        return onsetRate, sustainedRate, baseRate

    baseRange = [-0.1, -0.05]
    # responseRange = [0, 0.05, 0.1]
    responseRange = [respLatency, respLatency + 0.05, 0.1 + respLatency]
    # if dbRow['brainArea']=='rightAC':
    #     # responseRange = [0.02, 0.07, 0.12]
    #     responseRange = [0.02, 0.07, 0.1]
    # elif dbRow['brainArea']=='rightThal':
    #     # responseRange = [0.005, 0.015, 0.105]
    #     responseRange = [0.005, 0.015, 0.1]

    alignmentRange = [baseRange[0], responseRange[-1]]

    # Align spikes just to the selected event onset times
    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventsThisFreqHighIntensity,
                                                                   alignmentRange)

    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        baseRange)

    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        responseRange)

    avgResponse = nspkResp.mean(axis=0)
    onsetSpikes = avgResponse[0]
    sustainedSpikes = avgResponse[1]
    onsetRate = onsetSpikes / (responseRange[1] - responseRange[0])
    sustainedRate = sustainedSpikes / (responseRange[2] - responseRange[1])

    baseSpikes = nspkBase.mean()
    baseRate = baseSpikes / (baseRange[1] - baseRange[0])

    return onsetRate, sustainedRate, baseRate


def index_all_true_before(arr):
    """
    Find the index for a boolean array where all the inds after are True
    Args:
        arr (1-d array of bool): an array of boolean vals
    Returns:
        ind (int): The index of the first True val where all subsequent vals
            are also True
    """
    if any(~arr):
        indLastTrue = np.min(np.where(~arr))-1
    else:
        indLastTrue = len(arr)-1
    return indLastTrue


def spiketimes_each_frequency(spikeTimesFromEventOnset, trialIndexForEachSpike, currentFreq, uniqFreq):
    """
    Generator func to return the spiketimes/trial indices for trials of each
    frequency
    Args:
        spikeTimesFromEventOnset (numpy.ndarray): Contains the spike times relative
            to the onset of the event (the event start being 0)
        trialIndexForEachSpike (numpy.ndarray): Contains all the indices of the
            spikes to use
        currentFreq (numpy.ndarray): [nTrials, 1] Each value is the frequency
            presented during the specific trial number
        uniqFreq (numpy.ndarray): An array of each unique frequency presented over
            the whole session
    """
    for freq in uniqFreq:
        trialsThisFreq = np.flatnonzero(currentFreq == freq)
        spikeTimesThisFreq = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, trialsThisFreq)]
        trialIndicesThisFreq = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, trialsThisFreq)]
        yield freq, spikeTimesThisFreq, trialIndicesThisFreq


def angle_population_vector_zar(angles):
    """
    Computes the length of the mean vector for a population of angles.
    Copied directly from Biostatistical analysis, Zar, 3rd ed, pg 598
    (Mike Wehr has this book)
    Args:
        angles (numpy.ndarray): Each value is an angle in radians
    Returns:
        r (float): Anglle population vector for calculations in Rayleigh
        test
    """
    X = np.mean(np.cos(angles))
    Y = np.mean(np.sin(angles))
    r = np.sqrt(X**2 + Y**2)
    return r


def rayleigh_test(angles):
    """
    Performs Rayleigh Test for non-uniformity of circular data.
    Compares against Null hypothesis of uniform distribution around circle
    Assume one mode and data sampled from Von Mises.
    Use other tests for different assumptions.
    Maths from [Biostatistical Analysis, Zar].
    Args:
        angles (numpy.ndarray): Each value is an angle in radians
    Returns:
        zVal (float): Statistic from Rayleigh test
        pVal (float): Significance value from Rayleigh test
    """
    if angles.ndim > 1:
        angles = angles.flatten()
    N = angles.size
    # Compute Rayleigh's R
    R = N*angle_population_vector_zar(angles)
    # Compute Rayleight's z
    zVal = R**2. / N
    # Compute pvalue (Zar, Eq 27.4)
    pVal = np.exp(np.sqrt(1. + 4*N + 4*(N**2. - R**2)) - 1. - 2.*N)
    return zVal, pVal


# Below defintion applies to if spikes are signficantly synced to a rate as it is comparing the periods of spiking as it cycles through the modulation
def calculate_am_significance_synchronization(amSyncSpikeTimesFromEventOnset, amSyncTrialIndexForEachSpike, amCurrentFreq, amUniqFreq):
    """
    Calculate significance values for cell responses matching up with cycles in
    the amplitude modulation presentations.
    Args:
        amSpikeTimes (numpy.ndarray): Each value is a time when a spike occurred.
            Obatained from Ephys Data
        amOnsetTimes (numpy.ndarray): Contains as many values as there were trials
            with each value being the tme a trial started.
        amBaseTime (list): Contains two values that represent the time range
            for the base firing rate
        amOnsetTime (list): Contains two values that represent the time range
            for the onset firing rate
        amCurrentFreq (numpy.ndarray): Contains as many values as there were trials
            with each value being the am rate for a specific trial. Obtained
            from Behavior Data
        amUniqFreq (numpy.ndarray): Contains as many values as there were unique am
            rates presented over the entire session.

    Returns:
        allFreqSyncPVal (numpy.ndarray): Contains one p-value for each unique am
            rate presented over the entire session
        allFreqSyncZScore (numpy.ndarray): Contains one z-value for each unique am
            rate presented over the entire session
        allFreqVectorStrength (numpy.ndarray): Vector strength of the response for
            each AM rate
        allFreqRal (numpy.ndarray): Related to Rayleigh Test

    """
    numFreq = len(amUniqFreq)

    allFreqSyncPVal = np.empty(numFreq)
    allFreqVectorStrength = np.empty(numFreq)
    allFreqRal = np.empty(numFreq)
    allFreqSyncZScore = np.empty(numFreq)

    for indFreq, (freq, spiketimes, trialInds) in enumerate(
            spiketimes_each_frequency(amSyncSpikeTimesFromEventOnset,
                                      amSyncTrialIndexForEachSpike,
                                      amCurrentFreq, amUniqFreq)):
        strength, phase = signal.vectorstrength(spiketimes, 1.0 / freq)

        radsPerSec = freq * 2 * np.pi
        spikeRads = (spiketimes * radsPerSec) % (2 * np.pi)
        ral = np.array([2 * len(spiketimes) * (strength ** 2)])

        # NOTE: I checked the math in this function using the text referenced (Mike W. has a copy if needed) - Nick
        zVal, pVal = rayleigh_test(spikeRads)

        allFreqVectorStrength[indFreq] = strength  # Frequency vector strength
        allFreqRal[indFreq] = ral  # Unsure what this is
        allFreqSyncPVal[indFreq] = pVal  # p-value
        allFreqSyncZScore[indFreq] = zVal

    return allFreqSyncPVal, allFreqSyncZScore, allFreqVectorStrength, allFreqRal

# To calculate the p-value for baseline vs onset response for each individual frequency
def calculate_am_significance(amSpikeTimes, amOnsetTimes, amBaseTime, amResponseTime, amCurrentFreq, amUniqFreq):
    """
    Calculate significance values for all rates of amplitude modulation sessions
    Args:
        amSpikeTimes (numpy.ndarray): Each value is a time when a spike occurred.
            Obatained from Ephys Data
        amOnsetTimes (numpy.ndarray): Contains as many values as there were trials
            with each value being the time a trial started.
        amBaseTime (list): Contains two values that represent the time range
            for the base firing rate
        amResponseTime (list): Contains two values that represent the time
            range for the onset firing rate
        amCurrentFreq (numpy.ndarray): Contains as many values as there were trials
            with each value being the am rate for a specific trial. Obtained
            from Behavior Data
        amUniqFreq (numpy.ndarray): Contains as many values as there were unique
            am rates presented over the entire session.

    Returns:
        allFreqPVal (numpy.ndarray): Contains one p-value for each unique am rate
            presented over the entire session
        allFreqZScore (numpy.ndarray): Contains one z-value for each unique am
            rate presented over the entire session
    """
    numFreq = len(amUniqFreq)

    allFreqPVal = np.empty(numFreq)
    allFreqZScore = np.empty(numFreq)

    amTimeRange = [amBaseTime[0], amResponseTime[1]]

    (amSyncSpikeTimesFromEventOnset,
     amSyncTrialIndexForEachSpike,
     amSyncIndexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(amSpikeTimes,
                                                                         amOnsetTimes,
                                                                         amTimeRange)
    # Generate spiketimes for each frequency to do comparisons with
    # FIXME: Two options: Add a condition where if spikeTimes and trialInds are empty to not try further calculations.
    # Otherwise model like Anna's where we get the spiketimes first and then use behavioranalysis.find_trials_each_type to create a mask for each frequency.
    # Her example is in database_gen_funcs sound_response_any_stim, Line 65
    for indFreq, (freq, spiketimes, trialInds) in enumerate(
            spiketimes_each_frequency(amSyncSpikeTimesFromEventOnset,
                                      amSyncTrialIndexForEachSpike,
                                      amCurrentFreq, amUniqFreq)):

        nBaseSpk = spikesanalysis.spiketimes_to_spikecounts(spiketimes, trialInds, amBaseTime)
        nRespSpk = spikesanalysis.spiketimes_to_spikecounts(spiketimes, trialInds, amResponseTime)

        # Comparing each frequencies baseline and response range spike counts
        zStats, pVal = stats.mannwhitneyu(nRespSpk, nBaseSpk, alternative='two-sided')
        allFreqPVal[indFreq] = pVal
        allFreqZScore[indFreq] = zStats

    return allFreqPVal, allFreqZScore


def sound_response_any_stimulus(eventOnsetTimes, spikeTimeStamps, trialsEachCond, timeRange=[0.0, 1.0],
                                baseRange=[-1.1, -0.1]):
    """
    Determines if there is any combination of parameters that yields a change
    in firing rate.
    Inputs:
        eventOnsetTimes: array of timestamps indicating sound onsets
        spikeTimeStamps: array of timestamps indicating when spikes occured
        trialsEachCond: (N trials x N conditions) array indicating which
            condition occured for each trial. Currently only checks over one
            parameter used during session.
        timeRange: time range (relative to sound onset) to be used as response,
            list of [start time, end time]
        baseRange: time range (relative to sound onset) to be used as baseline,
            list of [start time, end time]

    Outputs:
        maxzscore: maximum U test statistic found after comparing response for
            each condition to baseline
        minpVal: minimum p value found after comparing response for each
            condition to baseline, NOT CORRECTED FOR MULTIPLE COMPARISONS
    """
    fullTimeRange = [min(min(timeRange), min(baseRange)), max(max(timeRange), max(baseRange))]

    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeTimeStamps,
        eventOnsetTimes,
        fullTimeRange)
    stimSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial,
                                                                 timeRange)
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial,
                                                                 baseRange)

    minpVal = np.inf
    maxzscore = -np.inf
    for cond in range(trialsEachCond.shape[1]):
        trialsThisCond = trialsEachCond[:, cond]
        if stimSpikeCountMat.shape[0] == len(trialsThisCond) + 1:
            stimSpikeCountMat = stimSpikeCountMat[:-1, :]
            baseSpikeCountMat = baseSpikeCountMat[:-1, :]
        if any(trialsThisCond):
            thisFirstStimCounts = stimSpikeCountMat[trialsThisCond].flatten()
            thisStimBaseSpikeCouns = baseSpikeCountMat[trialsThisCond].flatten()
            try:
                thiszscore, pValThisFirst = stats.mannwhitneyu(thisFirstStimCounts, thisStimBaseSpikeCouns, alternative='two-sided')
            except ValueError:  # If all numbers are identical in the population, mannwhitney fails
                pValThisFirst = 1
                thiszscore = 0
            if pValThisFirst < minpVal:
                minpVal = pValThisFirst
            if thiszscore > maxzscore:
                maxzscore = thiszscore
    return maxzscore, minpVal


def linear_discriminator(spikesPref, spikesNonPref):
    """
    Finds a possible threshold and then classifies spikes based on if they pass
    the threshold or not, finding a threshold that gives the greatest accuracy
    for the discriminator
    Args:
        spikesPref (numpy.ndarray):
        spikesNonPref (numpy.ndarray):

    Returns:
        maxAccuracy (float): The accuracy of the chosen threshold
        threshold (float): The threshold that yielded the highest accuracy for
            the discriminator
    """

    if len(spikesPref) == 0:
        raise ValueError('SpikesPref is an empty thing')
    if len(spikesNonPref) == 0:
        raise ValueError('SpikesNonPref is an empty thing')

    # Count number of times each spike number occurred for pref and nonpref
    prefSpikeCount = Counter(spikesPref)
    nonPrefSpikeCount = Counter(spikesNonPref)

    # Find possible threshold values
    minSpikes = np.min(np.concatenate([spikesPref, spikesNonPref]))
    maxSpikes = np.max(np.concatenate([spikesPref, spikesNonPref]))
    possibleThresh = np.arange(minSpikes, maxSpikes+1)

    # Init array for accuracy
    accuracy = np.empty(len(possibleThresh))

    # Try each possible threshold
    for indThresh, threshold in enumerate(possibleThresh):

        # Misclassified preferred - below the threshold
        misPref = sum([prefSpikeCount[i] for i in possibleThresh[:indThresh]])

        # Misclassified non-preferred - above the threshold
        misNonPref = sum([nonPrefSpikeCount[i] for i in possibleThresh[indThresh:]])

        # Calculate accuracy for this threshold value
        totalTrials = sum([len(spikesPref), len(spikesNonPref)])
        accuracy[indThresh] = (totalTrials - (misPref + misNonPref)) / float(totalTrials)

    # Return max accuracy and corresponding threshold
    indMaxAccuracy = np.argmax(accuracy)
    maxAccuracy = accuracy[indMaxAccuracy]
    threshold = possibleThresh[indMaxAccuracy]
    return maxAccuracy, threshold


def calculate_rate_discrimination_accuracy(spikeTimes, eventOnsetTimes, baseRange, responseRange, currentFreq,
                                           shuffle=False):  # From case==2 of am_preceptron.py of Nick's 2018thstr
    """
    Determine the ability of a cell to discriminate various amplitude
    modulation rates
    Args:
        spikeTimes (numpy.ndarray): [nTrials, 1] each value is a time stamp for when
            a spike was detected
        eventOnsetTimes (numpy.ndarray): [nTrials, 1] each value is a time stamp for
            when an event started
        baseRange (list): Contains the start and end time of the baseline range
        responseRange (list): Contains the start and end time of the response
            range
        currentFreq (numpy.ndarray): [nTrials, 1] where each value is the rate of
            amplitude modulation
        shuffle (bool): Whether to shuffle the AM rates or not

    Returns:
        rateDiscrimAccuracy (float): Value between 0 and 1 with 1 meaning the
            cells perfectly discriminate the rates of amplitude modulation

    """
    SHUFFLE = shuffle  # Set to true to shuffle AM rates, giving an estimate of the chance level.

    # if pVal > 0.05:  # No response
    #     svmScore = np.nan  # Unsure what this is used for so I am not bloating my db with it

    # --- Calculate best and worst rate ---

    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   responseRange)

    if SHUFFLE:
        currentFreq = np.random.permutation(currentFreq)

    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial,
                                                             responseRange)
    spikeCountEachTrial = spikeCountMat.flatten()
    if len(currentFreq) == len(spikeCountEachTrial) - 1:
        spikeCountEachTrial = spikeCountEachTrial[:-1]

    possibleRates = np.unique(currentFreq)
    avgSpikesEachRate = np.empty(len(possibleRates))
    for indRate, thisRate in enumerate(possibleRates):
        spikesThisRate = spikeCountEachTrial[currentFreq == thisRate]
        avgSpikesEachRate[indRate] = np.mean(spikesThisRate.ravel())

    # Find spikes each trial for pref and nonpref frequencies
    indPref = np.argmax(avgSpikesEachRate)
    indNonPref = np.argmin(avgSpikesEachRate)
    spikesPref = spikeCountEachTrial[currentFreq == possibleRates[indPref]]
    spikesNonPref = spikeCountEachTrial[currentFreq == possibleRates[indNonPref]]

    maxAccuracy, threshold = linear_discriminator(spikesPref, spikesNonPref)
    rateDiscrimAccuracy = maxAccuracy

    return rateDiscrimAccuracy


def calculate_phase_discrim_accuracy(spikeTimes, eventOnsetTimes, currentFreq, uniqFreq, shuffle=False):
    """
    Find the ability for a neuon to determine the phase of different amplitude
    modulation rates
    Args:
        spikeTimes (numpy.ndarray): [nTrials, 1] where each value is a time stamp
            for when a spike was detected
        eventOnsetTimes (numpy.ndarray): [nTrials, 1] where each value is a time
            stamp for when an event started
        currentFreq (numpy.ndarray): [nTrials, 1] where each value is the frequency
            for a specific trial
        uniqFreq (numpy.ndarray): Contains all the unique frequencies presented
        shuffle (bool): Whether to shuffle AM rates or not

    Returns:
        phaseDiscrimAccuracy (float): Value between 0 and 1 where 1 means a
            neuron can perfectly tell the phase of amplitude modulation

    """
    SHUFFLE = shuffle

    # Timerange for alignment?
    timeRange = [0.05, 0.5]  # Ignoring onset responses

    phaseDiscrimAccuracy = {}
    for thisFreq in uniqFreq:

        # Only use events for this frequency
        eventsThisFreq = eventOnsetTimes[currentFreq == thisFreq]

        (spikeTimesFromEventOnset,
         trialIndexForEachSpike,
         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                       eventsThisFreq,
                                                                       timeRange)

        # This is really all we need to do to bin things by phase.
        radsPerSec = thisFreq * 2 * np.pi
        spikeRads = (spikeTimesFromEventOnset * radsPerSec) % (2 * np.pi)

        strength, phase = signal.vectorstrength(spikeTimesFromEventOnset, 1.0 / thisFreq)
        phase = (phase + 2 * np.pi) % (2 * np.pi)

        shiftedRads = ((spikeRads - phase) + 2.25 * np.pi)
        if any(shiftedRads < 0):
            raise ValueError("Some shifted rads below 0")
        # shiftedRads = ((spikeRads - phase) + 2.25*np.pi)%(2*np.pi)
        spikeRads = shiftedRads % (2 * np.pi)

        nBins = 4
        binEdges = np.arange(0, 2.01 * np.pi, 2 * np.pi / nBins)  # The 2.01 makes it actually include 2pi
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeRads, indexLimitsEachTrial, binEdges)

        spikeCountMatCopy = copy.deepcopy(spikeCountMat)
        spikeCountMatShuffle = np.empty(np.shape(spikeCountMatCopy))
        for indMatRow in range(np.shape(spikeCountMatCopy)[0]):
            numRolls = np.random.choice(range(np.shape(spikeCountMatCopy)[1]))
            # numRolls = 0
            spikeCountMatShuffle[indMatRow, :] = np.roll(spikeCountMatCopy[indMatRow, :], numRolls)
        if SHUFFLE:
            spikeCountMat = spikeCountMatShuffle

        binMeans = np.mean(spikeCountMat, axis=0)
        prefInd = np.argmax(binMeans)
        nonPrefInd = np.argmin(binMeans)

        spikesPref = spikeCountMat[:, prefInd]
        spikesNonPref = spikeCountMat[:, nonPrefInd]

        maxAccuracy, threshold = linear_discriminator(spikesPref, spikesNonPref)

        # dataframe.set_value(indRow, 'phaseAccuracy_{}Hz'.format(int(thisFreq)), maxAccuracy)
        phaseDiscrimAccuracy[int(thisFreq)] = maxAccuracy
    return phaseDiscrimAccuracy

