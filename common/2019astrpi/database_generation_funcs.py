"""
create functions for calculating parameters
"""
import numpy as np
from numpy import inf
from scipy import optimize
from scipy import signal
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis


def gaussian(x, a, x0, sigma, y0):
    """
    Gaussian function
    Parameters:
            x: input data
            a: the height of the curve's peak
            x0: the position of the center of the peak
            sigma: standard variation that determines the width of the 'bell'
            y0: constant
    Returns:
            output of gaussian function
    """
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+y0


def retrofit_gaussian_log2(y, a, x0, sigma, y0):
    """
    Reverse function of gaussian. Not to confuse with inverse gaussian, \
    which is description of Brownian motion with positive drift to reach the fixed positive level
    This function finds the lower and upper frequencies with desirable response threshold output,\
    and optimal parameters (*popt) for 10dB above the current bandwidth
    """
    sqrtInner = -1*np.log((y-y0)/a)*2*sigma**2
    if sqrtInner < 0:  # No solutions
        return None
    else:
        lower = 2**(x0 - np.sqrt(sqrtInner))
        upper = 2**(x0 + np.sqrt(sqrtInner))
        return [lower, upper]


def calculate_firing_rate(ephysData, baseRange, session, selectinds=[]):
    """
    Creates functions for calculating spike rates
    Within the function, the module calculates response range(responseRange), \
    and entire range(alignmentRange). response Range mirrors baseRange but on the\
    post-stimulus time. It has the equal time distance from the stimulus\
    and the same amount of time range as baseRange
            ephysData (dict): generated using ephyscore.Cell.load. it contains three\
            keys (['samples'(float64,np.array), 'spikeTimes'(float64,np.array), 'events'(dict)])
            electro physiology data, see ephyscore for more detailed information
            baseRange (list): range of the time frame before the application of stimulus
            session (str): name of session
            selectinds (list): indices of event onset time points for specific frequency\
            and specific intensity, used for frequency tuning analysis, empty by default
    Returns:
            nspkBase (np.array): [ntrials, 1], each row represents the number of \
            spikes occured in the trial within base range(pre-stimulus)
            nspkResp (np.array): [ntrials, 1], each row represents the nubmer of \
            spikes occured in the trial within response range(post-stimulus)
    """
    eventOnsetTimes = ephysData['events']['stimOn']
    if selectinds != []:
        # =====================index mismatch correction========================
        while selectinds[-1] >= eventOnsetTimes.shape[0]:
            selectinds = np.delete(selectinds, -1, 0)
    # -----------------end of correction--------------------------------------
        eventOnsetTimes = eventOnsetTimes[selectinds]
    else:
        pass

    spikeTimes = ephysData['spikeTimes']
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
    Defines fit input parameters
    Parameters:
                uniqFreq (list): list of unique frequencies
                allIntenBase (np.array): cumulated number of spikes on pre-stimulus range with all\
                frequencies and all intensities
    Returns:
            p0 (list): initial guess
            bounds (tuple): lower and upper boundaries
    """
    p0 = [1, np.log2(uniqFreq[7]), 1, allIntenBase.mean()]
    bounds = ([0, np.log(uniqFreq[0]), 0, 0], [inf, np.log2(uniqFreq[-1]), inf, inf])
    return p0, bounds


def calculate_fit(uniqFreq, allIntenBase, freqs, spks):
    """
    Calculates curve fitting with given pre-stimulus spikes
    Parameters:
                Used for calculate_fit_params:
                    uniqFreq: list of unique frequencices
                    allIntenBase: cumulated number of spikes on pre-stimulus range with all\
                    frequencies and intensities
                Used for curve_fit:
                freqs (np.array): [total ntrials of all frequencies in response range] each number represents frequency
                spks (np.array): [total ntrials of all frequencies in response range] an array of spikes in each trial
    Returns:
                Rsquared: R-squared value of the curve
                popt: optimal parameters for the gaussian curve
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
    Response threshold is defined to be the baseline firiting rate plus 20%(fraThreshold)\
    of the difference between baseline and the cell's maximum firitng rate under any \
    condition (Sutter and Schreiner, https://doi.org/10.1152/jn.1991.65.5.1207)
    returns responseThreshold(float)
    """
    return allIntenBase.mean() + fraThreshold*(respSpikeMean.max()-allIntenBase.mean())


def calculate_intensity_threshold_and_CF_indices(fra, respSpikeMean, threshold=0.85):
    """
    Calculates intensity threshold index and characteristic frequency(CF) index
    Neuron's CF is defined as the frequency with the lowest sound intensity inside
    the FRA where 85%(theshold) of the intensities above were also within the FRA
    Parameters:
            fra (np.array): boolean array of shape (nInten, nFreq). Higher index = higher intensity
            respSpikeMean (np.array): response spike number array of shape (nInten, nFreq). Higher index = higher intensity
            threshold (float): At least this proportion of the intensities above must have a response for the freq to be cf
    Returns:
            intensityInd: intensity threshold index
            freqInd: characteristic frequency(CF) index
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
    Calculates lower/upper frequencies and Rsquared value for 10dB above the sound intensity threshold(SIT)
    with given index at 10dB above SIT(ind10Above)
    Parameters:
                ind10Above (int): represents the index of intensity threshold plus 10dB
                popts: optimal parameters for gaussian curve
                Rsquareds (np.array): [nIntensity, nFrequency] within the Rsquareds array,\
                each array represents the intensities in sequencial order. Each intensity array \
                contains R-squared value for each frequency
                responseThreshold (float): response firing threshold
                intensityThreshold (float): minimum intensity where 85% of the rest of intensity above is within FRA
    Returns:
            lowerFreq (float): lower bound frequency of BW10
            upperFreq (float): upper bound frequency of BW10
            Rsquared10AboveSIT (float) : mean rsquared value of intensity threshold plus 10dB

    """

    try:
        popt10AboveSIT = popts[ind10Above]
        Rsquared10AboveSIT = Rsquareds[ind10Above].mean()  # I made up the mean
        if popt10AboveSIT is None:
            print("Index returns empty array")  #FIXME: This was done to catch a niche circumstance when the index 10 above grabs an empty array (Ex: Now processing ', 'd1pi041', '2019-08-25', 3400.0, 7, 6, 1410)
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


def calculate_latency(eventOnsetTimes, currentFreq,  uniqFreq, currentIntensity, uniqueIntensity, spikeTimes, indRow):
    """

    Args:
        eventOnsetTimes (np.array): Same size as the number of trials with each value being the time sound detector turned on
        currentFreq (np.array): Same size as number of trials presented with each value being a specific frequency for that trial
        currentIntensity (np.array): Same size as number of trials presented with each value being a specific intensity for that trial
        uniqueIntensity (np.array): Uses currentIntensity to find how many unique intensity values were presented and store each unique value
        uniqFreq (np.array): Uses currentFreq to find how many unique frequency values were presented and store each unique value
        spikeTimes (np.array): Each value is a time when a spike occurred; obtained from ephys data
        indRow (int): Row number of cell in database(DataFrame)

    Returns:
        respLatency (float): Time, in seconds, from when the stimulus is presented and the cell responds

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
    try:
        (respLatency, interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
                                                                 indexLimitsSelectedTrials,
                                                                 timeRangeForLatency, threshold=0.5,
                                                                 win=signal.hanning(11))
        # TODO capture the exception outside in the database file itself
    except IndexError:
        print("Index error for cell {}".format(indRow))  # If there are no spikes in the timeRangeForLatency
        respLatency = np.nan

    print('Response latency: {:0.1f} ms'.format(1e3 * respLatency))

    return respLatency


def calculate_monotonicity_index(eventOnsetTimes, currentFreq, currentIntensity, uniqueIntensity, spikeTimes, cf):
    """

    Args:
        eventOnsetTimes (np.array): Same size as the number of trials with each value being the time sound detector turned on
        currentFreq (np.array): Same size as number of trials presented with each value being a specific frequency for that trial
        currentIntensity (np.array): Same size as number of trials presented with each value being a specific intensity for that trial
        uniqueIntensity (np.array): Uses currentIntensity to find how many unique intensity values were presented and store each unique value in ascending order
        spikeTimes (np.array): Each value is a time when a spike occurred; obtained from ephys data
        cf (float): Characteristic frequency of the cell, calculated by analyzing lowest threshold value for a cell

    Returns:
        monoIndex (float): Index value for monotonicity of a cell, between 0 and 1
        overallMaxSpikes (float): Mean number of spikes at the intensity that had the most spikes for a stimulus
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


def calculate_onset_to_sustained_ratio(eventOnsetTimes, spikeTimes, currentFreq, currentIntensity, cf, respLatency):
    """

    Args:
        eventOnsetTimes (np.array): Same size as the number of trials with each value being the time sound detector turned on
        currentFreq (np.array): Same size as number of trials presented with each value being a specific frequency for that trial
        currentIntensity (np.array): Same size as number of trials presented with each value being a specific intensity for that trial
        uniqueIntensity (np.array): Uses currentIntensity to find how many unique intensity values were presented and store each unique value in ascending order
        spikeTimes (np.array): Each value is a time when a spike occurred; obtained from ephys data
        respLatency (float): Time in seconds that the cell takes to respond to the stimulus being presented
    Returns:
        onsetRate (float): The number of spikes that happen within the response time range
        sustainedRate (float): The number of spikes that happen within the sustained time range
        baseRate (float): The number of spikes that happen within the baseline time range

    """
    cfTrials = currentFreq == cf
    eventsThisFreq = eventOnsetTimes[cfTrials]
    intenThisFreq = currentIntensity[cfTrials]

    # Get only the trials with the CF and the top 5 intensities
    uniqIntensity = np.unique(intenThisFreq)
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
