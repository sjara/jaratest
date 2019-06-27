'''
create functions for calculating parameters
'''
import numpy as np
from jaratoolbox import spikesanalysis
from scipy import stats
from scipy import optimize
from numpy import inf


def gaussian(x,a,x0,sigma,y0):
    '''
    Gaussian function
    Parameters:
            x: input data
            a: the height of the curve's peak
            x0: the position of the center of the peak
            sigma: standard variation that determines the width of the 'bell'
            y0: constant
    Returns:
            output of gaussian function
    '''
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+y0

def retrofit_gaussian_log2(y,a,x0,sigma,y0):
    '''
    Reverse function of gaussian. Not to confuse with inverse gaussian, \
    which is description of Brownian motion with positive drift to reach the fixed positive level
    This function finds the lower and upper frequencies with desirable response threshold output,\
    and optimal parameters (*popt) for 10dB above the current bandwidth
    '''
    sqrtInner = -1*np.log((y-y0)/a)*2*sigma**2
    if sqrtInner<0: #No solutions
        return None
    else:
        lower = 2**(x0 - np.sqrt(sqrtInner))
        upper = 2**(x0 + np.sqrt(sqrtInner))
        return [lower, upper]

def calculate_firing_rate(ephysData, baseRange,session, selectinds=[]):
    '''
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
    '''
    eventOnsetTimes = ephysData['events']['stimOn']
    if selectinds !=[]:
        #=====================index mismatch correction========================
        while selectinds[-1] >= eventOnsetTimes.shape[0]:
             selectinds = np.delete(selectinds,-1,0)
    #-----------------end of correction--------------------------------------
        eventOnsetTimes = eventOnsetTimes[selectinds]
    else:
        pass

    spikeTimes = ephysData['spikeTimes']
    binTime = baseRange[1]-baseRange[0]
    responseRangeStart = baseRange[1]*(-1) #if session != laserpulse else 0
    responseRange = [responseRangeStart, responseRangeStart+binTime]
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
    return nspkBase, nspkResp

def calculate_fit_params(uniqFreq,allIntenBase):
    '''
    Defines fit input parameters
    Parameters:
                uniqFreq: list of unique frequencices
                allIntenBase: cumulated number of spikes on pre-stimulus range with all\
                frequencies and all intensities
    Returns:
            p0: intial guess
            bounds: lower and upper boundaries
    '''
    p0 = [1, np.log2(uniqFreq[7]),1, allIntenBase.mean()]
    bounds = ([0,np.log(uniqFreq[0]),0,0],[inf,np.log2(uniqFreq[-1]),inf,inf])
    return p0, bounds

def calculate_fit(uniqFreq,allIntenBase,freqs,spks):
    '''
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
    '''
    p0, bounds = calculate_fit_params(uniqFreq, allIntenBase)

    try:
        popt,pcov = optimize.curve_fit(gaussian, np.log2(freqs), spks, p0=p0, bounds=bounds)

        gaussianResp = gaussian(np.log2(freqs),*popt)
        residuals = spks - gaussianResp
        ssquared = np.sum(residuals**2)
        ssTotal = np.sum((spks-np.mean(spks))**2)
        Rsquared = 1 - (ssquared/ssTotal)
        # corrcoeff,_ = stats.pearsonr(spks, gaussianResp)
        # Rsquared = corrcoeff**2

    except RuntimeError:
        print "Could not fit gaussian curve to tuning data."
        Rsquared, popt = None, None #gaussianResp

    return Rsquared, popt

def calculate_response_threshold(fraThreshold,allIntenBase,respSpikeMean):
    '''
    Response threshold is defined to be the baseline firiting rate plus 20%(fraThreshold)\
    of the difference between baseline and the cell's maximum firitng rate under any \
    condition (Sutter and Schreiner, https://doi.org/10.1152/jn.1991.65.5.1207)
    returns responseThreshold(float)
    '''
    return allIntenBase.mean() + fraThreshold*(respSpikeMean.max()-allIntenBase.mean())

def calculate_intensity_threshold_and_CF_indices(fra,respSpikeMean, threshold=0.85):
    '''
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
    '''
    results = []
    for inten, row in enumerate(fra):
        for indCol, column in enumerate(row):
            if column:
                colAbove = fra[inten:,indCol]
                if colAbove.mean() > threshold:
                    results.append((inten,indCol))
            else:
                resultWithMaxFiring = (None, None)
    resultIntenInds = [a for a, b in results]
    try:
        minResultIntenInd = min(resultIntenInds)

    except ValueError:
        resultWithMaxFiring = (None, None)

    else:
        resultsAtMinInten = [(a,b) for a,b in results if a==minResultIntenInd]
        resultSpikeCounts = [respSpikeMean[a,b] for a, b in resultsAtMinInten]
        resultWithMaxFiring = resultsAtMinInten[resultSpikeCounts.index(np.max(resultSpikeCounts))]

    intensityInd, freqInd = resultWithMaxFiring

    return intensityInd, freqInd

def calculate_BW10_params(ind10Above, popts,Rsquareds,responseThreshold,intensityThreshold):
    '''
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

    '''
    try:
        popt10AboveSIT = popts[ind10Above]
        Rsquared10AboveSIT = Rsquareds[ind10Above].mean() #I made up the mean
    except IndexError:
        print "Failure indexerror didn't get 10 above"
        print intensityThreshold
        failed=True
        #This is for the instance when we are not able to catch 10dB above threshold.\
        # Even then we can still get cf and threshold, but not uF/lF
        upperFreq = None
        lowerFreq = None
        Rsquared10AboveSIT = np.nan

    else:
        freqLimits = retrofit_gaussian_log2(responseThreshold, *popt10AboveSIT)

        if freqLimits is not None:
            lowerFreq, upperFreq = freqLimits
        else:
            # ind10AboveButNone.append(indRow)
            lowerFreq=None
            upperFreq=None
            Rsquared10AboveSIT = np.nan


    return lowerFreq, upperFreq, Rsquared10AboveSIT
