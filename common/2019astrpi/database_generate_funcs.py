'''
create functions for calculating spike rates, created on 051319
'''
import numpy as np
from jaratoolbox import spikesanalysis
from scipy import stats
from scipy import optimize
from numpy import inf


def gaussian(x,a,x0,sigma,y0):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+y0

def retrofit_gaussian_log2(y,a,x0,sigma,y0):#not to confuse with inverse gaussain. inverse_gaussian is a totally different math function
    sqrtInner = -1*np.log((y-y0)/a)*2*sigma**2
    if sqrtInner<0: #No solutions
        return None
    else:
        lower = 2**(x0 - np.sqrt(sqrtInner)) #log2(freq)=output >> 2**(output)=freq
        upper = 2**(x0 + np.sqrt(sqrtInner))
        return [lower, upper]

def calculate_firing_rate(ephysData, baseRange,session, selectinds=[]):

    eventOnsetTimes = ephysData['events']['stimOn']
    if selectinds !=[]:#.size != 0:
        #=====================index mismatch correction========================
        while selectinds[-1] >= eventOnsetTimes.shape[0]:
             selectinds = np.delete(selectinds,-1,0)
    #-----------------end of correction--------------------------------------
        eventOnsetTimes = eventOnsetTimes[selectinds]
    else:
        pass
        # print "it's empty"


    spikeTimes = ephysData['spikeTimes']
    binTime = baseRange[1]-baseRange[0]
    responseRange = [0, 0+binTime] if session != 'am' else [0.1, 0.5]
    alignmentRange = [baseRange[0], responseRange[1]]# if session != 'laserpulse' else [baseRange[0], 0.5]

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
    # initial guuess p0
    p0 = [1, np.log2(uniqFreq[7]),1,allIntenBase.mean()]
    # setting up lower and upper boundaries
    bounds = ([0,np.log(uniqFreq[0]),0,0],[inf,np.log2(uniqFreq[-1]),inf,inf])
    return p0, bounds

def calculate_fit(uniqFreq,allIntenBase,freqs,spks):

    p0, bounds = calculate_fit_params(uniqFreq, allIntenBase)

    try:
        popt,pcov = optimize.curve_fit(gaussian,np.log2(freqs),spks,p0=p0, bounds=bounds)#sigma none? ,sigma = None
#Get R**2 value for evaluating fit later
#[3]Get residuals, and sum of squared residuals (SSQ)
        gaussianResp = gaussian(np.log2(freqs),*popt)
        # print "this is gaussianResp"
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
    return allIntenBase.mean() + fraThreshold*(respSpikeMean.max()-allIntenBase.mean())

def calculate_intensity_threshold_and_CF_indices(fra,respSpikeMean):
    results = []
    for inten, row in enumerate(fra):
        for indCol, column in enumerate(row):
            if column:
                colAbove = fra[inten:,indCol]
                if colAbove.mean() > 0.85:
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
# [8.1] get the inverse gaussian to find the frequencies[upper and lower], to do that, get Rsquared value and popt
    try:
        poptBW10 = popts[ind10Above]
        RsquaredBW10 = Rsquareds[ind10Above].mean() #I made up the mean
    except IndexError:
        print "Failure indexerror didn't get 10 above"
        print intensityThreshold
        failed=True
        #We were not able to catch 10db above threshold. In this case, we can still get cf and thresh, but not uF/lF
        # no10dbAboveInds.append(indIter)
        upperFreq = None
        lowerFreq = None
        RsquaredBW10 = np.nan
     #-----------------------------------------error expected, maybe in need of error management
#[8.2] retrofit gaussian to get the lower frequency and upper frequency at theshold
    else:
        freqLimits = retrofit_gaussian_log2(responseThreshold, *poptBW10) #-----------------------------------------error expected, maybe in need of error management
#[8.3] get bw10
        if freqLimits is not None:
            lowerFreq, upperFreq = freqLimits
        else:
            # ind10AboveButNone.append(indRow)
            lowerFreq=None
            upperFreq=None
            RsquaredBW10 = np.nan


    return lowerFreq, upperFreq, RsquaredBW10
