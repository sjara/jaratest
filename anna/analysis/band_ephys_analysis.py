import numpy as np
import os
from scipy import stats

from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import behavioranalysis
from jaratoolbox import settings


# for correcting sound onset times for cells recorded before installation of Cliff box
AVERAGE_JITTER = {'bandwidth':0.0093,
                  'harmonics':0.0094,
                  'tuningCurve':0.0095,
                  'AM':0.0091}

def get_sound_onset_times(ephysData, sessionType):
    eventOnsetTimes = ephysData['events']['soundDetectorOn']
    if len(eventOnsetTimes)==0: #some cells recorded before sound detector installed
        eventOnsetTimes = ephysData['events']['stimOn'] + AVERAGE_JITTER[sessionType] #correction for onset times, determined by comparing sound detector onset to stim event onset
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.2)
    return eventOnsetTimes

# --- Methods for calculating aspects of data used in selection of cells ---

def best_index(cellObj, bestFreqs, behavType):
    behavIndex = cellObj.get_session_inds(behavType)
    charFreqs = []

    for ind in behavIndex:
        bdata = cellObj.load_behavior_by_index(ind) 
        charFreq = np.unique(bdata['charFreq'])[0]
        charFreqs.append(charFreq)

    # determine distance from best freq (in octaves) of char freq used and select closest session
    octavesFromBest = []
    behavIndices = []
    for ind, freq in enumerate(bestFreqs):
        if freq is not None:
            octaveDiff = np.zeros(len(charFreqs))
            for ind2, charFreq in enumerate(charFreqs):
                octaveDiff[ind2] = np.log2(freq/charFreq)
            octaveDiff = np.abs(octaveDiff)
            behavIndexThisInd = behavIndex[np.argmin(octaveDiff)]
            octavesFromBestThisInd = min(octaveDiff)
            behavIndices.append(behavIndexThisInd)
            octavesFromBest.append(octavesFromBestThisInd)
        else:
            behavIndices.append(None)
            octavesFromBest.append(None)
    return behavIndices, octavesFromBest

def best_window_freq_tuning(spikeTimesFromEventOnset,indexLimitsEachTrial, freqEachTrial):
    windowsToTry = [[0.0,0.1],[0.0,0.05],[0.1,0.15]]
    numFreqs = np.unique(freqEachTrial)
    
    zscores = np.zeros((len(windowsToTry),len(numFreqs)))
    for ind, window in enumerate(windowsToTry):
        duration = window[1]-window[0]
        baseTimeRange = [-0.1-duration, -0.1]
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, window)
        baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseTimeRange)
        
        trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial, numFreqs)
        for ind2 in range(len(numFreqs)):
            trialsThisFreq = trialsEachFreq[:,ind2]
            spikeCountsThisFreq = spikeCountMat[trialsThisFreq]
            baseCountsThisFreq = baseSpikeCountMat[trialsThisFreq]
            zScore, pVal = stats.ranksums(spikeCountsThisFreq, baseCountsThisFreq)
            zscores[ind,ind2] = zScore

    maxInd = np.unravel_index(zscores.argmax(), zscores.shape)
    windowToUse = windowsToTry[maxInd[0]]
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, windowToUse)
    return spikeCountMat, windowToUse

            

def freq_tuning_fit(eventOnsetTimes, spikeTimestamps, bdata, timeRange = [-0.2, 0.2], intensityInds = None):
    # determine the best frequency of the cell by fitting gaussian curve to tuning data
    gaussFits = []
    bestFreqs = []
    Rsquareds = []
    
    freqEachTrial = bdata['currentFreq']
    intensityEachTrial = bdata['currentIntensity']
    numIntensities = np.unique(intensityEachTrial)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimestamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        timeRange)
    trialsEachInt = behavioranalysis.find_trials_each_type(intensityEachTrial, numIntensities)
    if intensityInds is None:
        intensityInds = range(len(numIntensities))
    
    spikeCountMat, window = best_window_freq_tuning(spikeTimesFromEventOnset, indexLimitsEachTrial, freqEachTrial)
    for intensityInd in intensityInds:
        trialsThisIntensity = trialsEachInt[:,intensityInd]
        tuningSpikeRates = (spikeCountMat[trialsThisIntensity].flatten())/(window[1]-window[0])
        freqsThisIntensity = freqEachTrial[trialsThisIntensity]
        gaussFit, Rsquared = response_curve_fit(np.log2(freqsThisIntensity), tuningSpikeRates)
        bestFreq = 2**gaussFit[0] if gaussFit is not None else None
        gaussFits.append(gaussFit)
        bestFreqs.append(bestFreq)
        Rsquareds.append(Rsquared)
    
    return gaussFits, bestFreqs, Rsquareds, window
    
    
def band_tuning_fit(eventOnsetTimes, spikeTimestamps, bdata, secondSortParam='currentAmp', timeRange = [0.0, 1.0]):
    
    bandEachTrial = bdata['currentBand']
    secondSort = bdata[secondSortParam]
    numBands = np.unique(bandEachTrial)
    if np.isinf(numBands[-1]):
        numBands[-1] = 5.0 #setting white noise bandwidth to mouse hearing range in octaves
    numSec = np.unique(secondSort)
    
    spikeArray, errorArray, baselineSpikeRate = calculate_tuning_curve_inputs(spikeTimestamps, eventOnsetTimes, bandEachTrial, secondSort, timeRange, [0.0,0.7])
    fitParams = []
    for amp in len(spikeArray.shape[1]):
        curveFit, bestBand, Rsquared = response_curve_fit(numBands, spikeArray[:,amp], type='carandini')
        fitParams.append([curveFit, bestBand, Rsquared])
    return fitParams
            
def response_curve_fit(stimArray, responseArray, type='gaussian'):
    #find best fit for frequency or bandwidth (or others) spike data
    from scipy.optimize import curve_fit
    try:
        if type=='gaussian':
            maxInd = np.argmax(responseArray)
            p0 = [stimArray[maxInd], responseArray[maxInd], 1.,0.]
            curveFit = curve_fit(gaussian, stimArray, responseArray, p0=p0, maxfev=10000)[0]
        elif type=='carandini':
            from scipy.special import erf
            maxInd = np.argmax(responseArray)
            initmExp = 2.5
            initSigmaD = stimArray[maxInd]
            initSigmaS = 2*stimArray[maxInd]
            initRD = responseArray[maxInd]/(erf(stimArray[maxInd]/(np.sqrt(2)*initSigmaD)))**initmExp
            initRS = (-1 + initRD/responseArray[maxInd])/(erf(stimArray[maxInd]/(np.sqrt(2)*initSigmaS)))**initmExp
            p0 = [initRD, initRS, initSigmaD, initSigmaS, initmExp]
            curveFit = curve_fit(carandini_form, stimArray, responseArray, p0=p0, maxfev=10000)[0]
    except RuntimeError:
        print "Could not fit {} curve to tuning data.".format(type)
        return None, None
    
    #calculate R^2 value for fit
    if type=='gaussian':
        fitResponseArray = gaussian(stimArray, curveFit[0], curveFit[1], curveFit[2], curveFit[3])
    elif type=='carandini':
        fitResponseArray = carandini_form(stimArray, curveFit[0], curveFit[1], curveFit[2], curveFit[3], curveFit[4])
    residuals = responseArray - fitResponseArray
    SSresidual = np.sum(residuals**2)
    SStotal = np.sum((responseArray-np.mean(responseArray))**2)
    Rsquared = 1-(SSresidual/SStotal)
    
    return curveFit, Rsquared

def gaussian(x, mu, amp, sigma, offset):
    return offset+amp*np.exp(-((x-mu)/sigma)**2)

def carandini_form(x, RD, RS, sigmaD, sigmaS, mExp):
    from scipy.special import erf
    return (RD*(erf(x/(np.sqrt(2)*sigmaD)))**mExp)/(1+RS*(erf(x/(np.sqrt(2)*sigmaS)))**mExp)

def laser_response(eventOnsetTimes, spikeTimeStamps, timeRange=[0.0, 0.1], baseRange=[-0.2, -0.1]):
    fullTimeRange = [min(min(timeRange),min(baseRange)), max(max(timeRange),max(baseRange))]
    
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimeStamps, 
                                                                                                                   eventOnsetTimes, 
                                                                                                                   fullTimeRange)
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseRange)
    baselineSpikeRate = np.mean(baseSpikeCountMat)/(baseRange[1]-baseRange[0])
    baselineSpikeRateSTD = np.std(baseSpikeCountMat)/(baseRange[1]-baseRange[0])
    laserSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    laserSpikeRate = np.mean(laserSpikeCountMat)/(timeRange[1]-timeRange[0])
    laserpVal = stats.ranksums(laserSpikeCountMat, baseSpikeCountMat)[1]
    laserstdFromBase = (laserSpikeRate - baselineSpikeRate)/baselineSpikeRateSTD

    return laserpVal, laserstdFromBase

                    
def sound_response_any_stimulus(eventOnsetTimes, spikeTimeStamps, bdata, timeRange=[0.0,1.0], baseRange=[-1.1,-0.1], sessionType='bandwidth', sessionIndex=None):
    fullTimeRange = [min(min(timeRange),min(baseRange)), max(max(timeRange),max(baseRange))]
    
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimeStamps, 
                                                                                                                   eventOnsetTimes, 
                                                                                                                   fullTimeRange)
    stimSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseRange)
    baseSpikeCountMat = baseSpikeCountMat.flatten()
    
    if sessionType == 'bandwidth': 
        firstSort = bdata['currentBand']
        numFirst = np.unique(firstSort)
        secondSort = bdata['currentAmp']
        numSec = np.unique(secondSort)
    elif sessionType == 'laserBandwidth':
        firstSort = bdata['currentBand']
        numFirst = np.unique(firstSort)
        secondSort = bdata['laserTrial']
        numSec = np.unique(secondSort)
    
    totalConds = len(numFirst)*len(numSec)
    trialsEachCond = behavioranalysis.find_trials_each_combination(firstSort,numFirst,secondSort,numSec)
    
    minpVal = np.inf
    
    for sec in range(len(numSec)):
        trialsThisSec = trialsEachCond[:,:,sec]
        for first in range(len(numFirst)):
            trialsThisFirst = trialsThisSec[:,first]
            if stimSpikeCountMat.shape[0] == len(trialsThisFirst)+1:
                stimSpikeCountMat = stimSpikeCountMat[:-1,:]
                #print "FIXME: Using bad hack to make event onset times equal number of trials"
            elif stimSpikeCountMat.shape[0] != len(trialsThisFirst):
                print "STOP NO THIS IS BAD"
                raise ValueError
            if any(trialsThisFirst):
                thisFirstStimCounts = stimSpikeCountMat[trialsThisFirst].flatten()
                pValThisFirst = stats.ranksums(thisFirstStimCounts, baseSpikeCountMat)[1]*totalConds
                if pValThisFirst < minpVal:
                    minpVal = pValThisFirst
    return minpVal
        

# --- Methods for generating intermediate data ---

def bandwidth_suppression_from_peak(tuningDict, subtractBaseline=False):
    spikeArray = tuningDict['responseArray']
    baselineSpikeRate = tuningDict['baselineSpikeRate']
    spikeCountMat = tuningDict['spikeCountMat']
    
    suppressionIndex = np.zeros(spikeArray.shape[1])
    facilitationIndex = np.zeros_like(suppressionIndex)
    
    suppressionpVal = np.zeros_like(suppressionIndex)
    facilitationpVal = np.zeros_like(suppressionIndex)
            
    if not subtractBaseline:
        baselineSpikeRate = 0
    
    for ind in range(len(suppressionIndex)):    
        suppressionIndex[ind] = (max(spikeArray[:,ind])-spikeArray[:,ind][-1])/(max(spikeArray[:,ind])-baselineSpikeRate)
        facilitationIndex[ind] = (max(spikeArray[:,ind])-spikeArray[:,ind][0])/(max(spikeArray[:,ind])-baselineSpikeRate)

        trialsThisSeconsVal = tuningDict['trialsEachCond'][:,:,ind]
        peakInd = np.argmax(spikeArray[:,ind])
        
        peakSpikeCounts = spikeCountMat[trialsThisSeconsVal[:,peakInd]].flatten()
        whiteNoiseSpikeCounts = spikeCountMat[trialsThisSeconsVal[:,-1]].flatten()
        pureToneSpikeCounts = spikeCountMat[trialsThisSeconsVal[:,0]].flatten()
        
        suppressionpVal[ind] = stats.ranksums(peakSpikeCounts, whiteNoiseSpikeCounts)[1]
        facilitationpVal[ind] = stats.ranksums(peakSpikeCounts, pureToneSpikeCounts)[1]
        
    
    suppressionDict = {'suppressionIndex':suppressionIndex,
                       'suppressionpVal':suppressionpVal,
                       'facilitationIndex':facilitationIndex,
                       'facilitationpVal':facilitationpVal}
    
    return suppressionDict


def bandwidth_suppression_by_bins(tuningDict, lowBandInds=[1,2], highBandInds=[5,6], subtractBaseline=False):
    spikeArray = tuningDict['responseArray']
    spikeCountMat = tuningDict['spikeCountMat']
    baselineSpikeRate = tuningDict['baselineSpikeRate']
    
    if not subtractBaseline:
        baselineSpikeRate = 0
    
    suppressionIndex = np.zeros(spikeArray.shape[1])
    suppressionpVal = np.zeros_like(suppressionIndex)
    
    for ind in range(len(suppressionIndex)):
        trialsThisSeconsVal = tuningDict['trialsEachCond'][:,:,ind]
        
        lowBandSpikeCounts = []
        for lowInd in lowBandInds:
            thisBinCounts = spikeCountMat[trialsThisSeconsVal[:,lowInd]].flatten()
            lowBandSpikeCounts.extend(thisBinCounts)
            
        highBandSpikeCounts = []
        for highInd in highBandInds:
            thisBinCounts = spikeCountMat[trialsThisSeconsVal[:,highInd]].flatten()
            highBandSpikeCounts.extend(thisBinCounts)
            
        suppressionIndex[ind] = (np.mean(lowBandSpikeCounts)-np.mean(highBandSpikeCounts))/(np.mean(lowBandSpikeCounts)+np.mean(highBandSpikeCounts)-2*baselineSpikeRate)
        suppressionpVal[ind] = stats.ranksums(lowBandSpikeCounts, highBandSpikeCounts)[1]
    
    suppressionDict = {'suppressionIndex':suppressionIndex,
                       'suppressionpVal':suppressionpVal}
    
    return suppressionDict


def calculate_tuning_curve_inputs(spikeTimeStamps, eventOnsetTimes, firstSort, secondSort, timeRange, baseRange=[-1.1,-0.1], errorType = 'sem', info='full'):
    fullTimeRange = [min(min(timeRange),min(baseRange)), max(max(timeRange),max(baseRange))]
    
    numFirst = np.unique(firstSort)
    numSec = np.unique(secondSort)
    duration = timeRange[1]-timeRange[0]
    spikeArray = np.zeros((len(numFirst), len(numSec)))
    errorArray = np.zeros_like(spikeArray)
    trialsEachCond = behavioranalysis.find_trials_each_combination(firstSort, 
                                                                   numFirst, 
                                                                   secondSort, 
                                                                   numSec)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimeStamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        fullTimeRange)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseRange)
    baselineSpikeRate = np.mean(baseSpikeCountMat)/(baseRange[1]-baseRange[0])
    if errorType == 'sem':
        baselineError = stats.sem(baseSpikeCountMat)/(baseRange[1]-baseRange[0])
    elif errorType == 'std':
        baselineError = np.std(baseSpikeCountMat)/(baseRange[1]-baseRange[0])
    
    for sec in range(len(numSec)):
        trialsThisSec = trialsEachCond[:,:,sec]
        for first in range(len(numFirst)):
            trialsThisFirst = trialsThisSec[:,first]
            if spikeCountMat.shape[0] != len(trialsThisFirst):
                spikeCountMat = spikeCountMat[:-1,:]
            if any(trialsThisFirst):
                thisFirstCounts = spikeCountMat[trialsThisFirst].flatten()
                spikeArray[first,sec] = np.mean(thisFirstCounts)/duration
                if errorType == 'sem':
                    errorArray[first,sec] = stats.sem(thisFirstCounts)/duration
                elif errorType == 'std':
                    errorArray[first,sec] = np.std(thisFirstCounts)/duration
            else:
                spikeArray[first,sec] = np.nan
                errorArray[first,sec] = np.nan
    if info=='full':
        tuningDict = {'responseArray':spikeArray,
                      'errorArray':errorArray,
                      'baselineSpikeRate':baselineSpikeRate,
                      'baselineSpikeError':baselineError,
                      'spikeCountMat':spikeCountMat,
                      'trialsEachCond':trialsEachCond}
    elif info=='plotting':
        tuningDict = {'responseArray':spikeArray,
                      'errorArray':errorArray,
                      'baselineSpikeRate':baselineSpikeRate,
                      'baselineSpikeError':baselineError}
    else:
        raise NameError('That is not an info type you degenerate')
    return tuningDict


def onset_sustained_spike_proportion(spikeTimeStamps, eventOnsetTimes, onsetTimeRange=[0.0,0.05], sustainedTimeRange=[0.2,1.0]):
    fullTimeRange = [onsetTimeRange[0], sustainedTimeRange[1]]
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimeStamps, 
                                                                                                                       eventOnsetTimes, 
                                                                                                                       fullTimeRange)
        
    onsetSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, onsetTimeRange)
    sustainedSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, sustainedTimeRange)
    fullSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, fullTimeRange)
    propOnset = 1.0*sum(onsetSpikeCountMat)/sum(fullSpikeCountMat)
    propSustained = 1.0*sum(sustainedSpikeCountMat)/sum(fullSpikeCountMat)
    return propOnset, propSustained

    
    