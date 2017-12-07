import numpy as np
import os
from scipy import stats


from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import behavioranalysis
from jaratoolbox import settings


# --- Methods for calculating aspects of data used in selection of cells ---

def best_index(cell, bestFreqs, behavType):
    behavIndex = get_session_inds(cell, behavType)
    charFreqs = []
    if len(behavIndex)==0:
        print "No session of this type"
        return None, None

    for ind in behavIndex:
        bdata = load_behaviour_data(cell['subject'], cell['behavior'][ind]) 
        charFreq = np.unique(bdata['charFreq'])[0]
        charFreqs.append(charFreq)
    
    # best index selected separately for each intensity used in bandwidth tuning
    bandAmps = np.unique(bdata['currentAmp'])
    if max(bandAmps) < 1:
        bandAmps = np.array([53.7, 65.6]) #HARDCODED dB VALUE FOR SESSIONS DONE BEFORE NOISE CALIBRATION
    
    # find tone intensity that corresponds to tone sessions in bandwidth trial
    toneInts = bandAmps - 15.0 #HARDCODED DIFFERENCE IN TONE AND NOISE AMP BASED ON OSCILLOSCOPE READINGS FROM RIG 2
    intensityInds = []
    tuningIndex = get_session_inds(cell, 'tuningCurve')[-1]    
    tuningBData = load_behaviour_data(cell['subject'], cell['behavior'][tuningIndex])
    intensityEachTrial = tuningBData['currentIntensity']
    numIntensities = np.unique(intensityEachTrial)
    
    for ind, int in enumerate(toneInts):
        intensityInd = (np.abs(numIntensities-toneInts[ind])).argmin()
        intensityInds.append(intensityInd)

    # determine distance from best freq (in octaves) of char freq used and select closest session
    if bestFreqs is not None:
        octavesFromBest = []
        behavIndices = []
        for ind, int in enumerate(intensityInds):
            if bestFreqs[int] is not None:
                octaveDiff = np.zeros(len(charFreqs))
                for ind2, charFreq in enumerate(charFreqs):
                    octaveDiff[ind2] = np.log2(bestFreqs[int]/charFreq)
                octaveDiff = np.abs(octaveDiff)
                behavIndexThisInd = behavIndex[np.argmin(octaveDiff)]
                octavesFromBestThisInd = min(octaveDiff)
                behavIndices.append(behavIndexThisInd)
                octavesFromBest.append(octavesFromBestThisInd)
            else:
                behavIndices.append(None)
                octavesFromBest.append(None)
        return behavIndices, octavesFromBest
    else:
        print "Could not determine best index with tuning data available"
        return None, None

def best_window_freq_tuning(spikeTimesFromEventOnset,indexLimitsEachTrial, freqEachTrial):
    windowsToTry = [[0.01,0.11],[0.01,0.06],[0.11,0.16]]
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
    print maxInd
    print np.mean(zscores, axis=0)
    windowToUse = windowsToTry[maxInd[0]]
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, windowToUse)
    return spikeCountMat, windowToUse

            

def freq_tuning_fit(eventOnsetTimes, spikeTimestamps, bdata, timeRange = [-0.2, 0.2]):
    # determine the best frequency of the cell by fitting gaussian curve to tuning data
    gaussFits = []
    bestFreqs = []
    Rsquareds = []
    
    freqEachTrial = bdata['currentFreq']
    numFreqs = np.unique(freqEachTrial)
    
    intensityEachTrial = bdata['currentIntensity']
    numIntensities = np.unique(intensityEachTrial)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimestamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        timeRange)
    trialsEachInt = behavioranalysis.find_trials_each_type(intensityEachTrial, numIntensities)
    
    spikeCountMat, window = best_window_freq_tuning(spikeTimesFromEventOnset, indexLimitsEachTrial, freqEachTrial)
    for intensityInd in range(len(numIntensities)):
        trialsThisIntensity = trialsEachInt[:,intensityInd]
        tuningSpikeCounts = (spikeCountMat[trialsThisIntensity].flatten())/(timeRange[1]-timeRange[0])
        freqsThisIntensity = freqEachTrial[trialsThisIntensity]
        gaussFit, bestFreq, Rsquared = response_curve_fit(np.log2(freqsThisIntensity), tuningSpikeCounts)
        gaussFits.append(gaussFit)
        bestFreqs.append(bestFreq)
        Rsquareds.append(Rsquared)
    
    return gaussFits, bestFreqs, Rsquareds, window
    
    
def band_tuning_fit(cell, bandIndex = None, timeRange = [0.0, 1.0]):
    if bandIndex is None:
        bandIndeces = get_session_inds(cell, 'bandwidth')
        if len(bandIndeces)==0:
            print "No session of this type"
            return None, None, None
        else:
            bandIndex = bandIndeces[0]
    eventData, spikeData = load_ephys_data(cell['subject'], cell['ephys'][bandIndex], int(cell['tetrode']), int(cell['cluster']))
    eventOnsetTimes = eventData.get_event_onset_times()
    spikeTimeStamps = spikeData.timestamps
    timeRange = [-0.2, 1.5]
    
    #load bandwidth behaviour data
    bandBData = load_behaviour_data(cell['subject'], cell['behavior'][bandIndex])  
    
    bandEachTrial = bandBData['currentBand']
    secondSort = bandBData['currentAmp']
    numBands = np.unique(bandEachTrial)
    numSec = np.unique(secondSort)
    
    spikeArray, errorArray, baselineSpikeRate = calculate_tuning_curve_inputs(spikeTimeStamps, eventOnsetTimes, bandEachTrial, secondSort, timeRange, [0.0,0.7])
    fitParams = []
    for amp in len(spikeArray.shape[1]):
        curveFit, bestBand, Rsquared = response_curve_fit(np.log2(numBands), spikeArray[1:-2,amp], type='quadratic')
        fitParams.append([curveFit, bestBand, Rsquared])
    return fitParams
            
def response_curve_fit(stimArray, responseArray, type='gaussian'):
    #find best fit for frequency or bandwidth (or others) spike data
    from scipy.optimize import curve_fit
    #logStimArray = np.log2(stimArray)
    maxInd = np.argmax(responseArray)
    try:
        if type=='gaussian':
            p0 = [stimArray[maxInd], responseArray[maxInd], 1.,0.]
            curveFit = curve_fit(gaussian, stimArray, responseArray, p0=p0, maxfev=10000)[0]
        elif type=='quadratic':
            curveFit = curve_fit(quadratic, stimArray, responseArray, p0=p0, maxfev=10000)[0]
    except RuntimeError:
        print "Could not fit {} curve to tuning data.".format(type)
        return None, None, None
    
    #estimate best frequency and calculate R^2 value for fit
    if type=='gaussian':
        bestFreq = 2**curveFit[0]
        fitResponseArray = gaussian(stimArray, curveFit[0], curveFit[1], curveFit[2], curveFit[3])
    elif type=='quadratic':
        bestFreq = curveFit[2]/(2*curveFit[1])
        fitResponseArray = quadratic(stimArray, curveFit[0], curveFit[1], curveFit[2])
    residuals = responseArray - fitResponseArray
    SSresidual = np.sum(residuals**2)
    SStotal = np.sum((responseArray-np.mean(responseArray))**2)
    Rsquared = 1-(SSresidual/SStotal)
    
    return curveFit, bestFreq, Rsquared

def gaussian(x, mu, amp, sigma, offset):
    p = [mu, amp, sigma, offset]
    return p[3]+p[1]* np.exp(-((x-p[0])/p[2])**2)

def quadratic(x, a, b, c):
    return a*(x**2)+b*x+c

def laser_response(eventOnsetTimes, spikeTimeStamps, timeRange=[0.0, 0.1], baseRange=[-0.2, -0.1]):
    fullTimeRange = [min(min(timeRange),min(baseRange)), max(max(timeRange),max(baseRange))]
    
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimeStamps, 
                                                                                                                   eventOnsetTimes, 
                                                                                                                   fullTimeRange)
    zStatsEachRange,pValueEachRange,maxZvalue = spikesanalysis.response_score(spikeTimesFromEventOnset, 
                                                                              indexLimitsEachTrial, 
                                                                              baseRange, 
                                                                              timeRange)
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseRange)
    baselineSpikeRate = np.mean(baseSpikeCountMat)/(baseRange[1]-baseRange[0])
    baselineSpikeRateSTD = np.std(baseSpikeCountMat)/(baseRange[1]-baseRange[0])
    laserSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    laserSpikeRate = np.mean(laserSpikeCountMat)/(timeRange[1]-timeRange[0])
    laserpVal = pValueEachRange[0]
    laserstdFromBase = (laserSpikeRate - baselineSpikeRate)/baselineSpikeRateSTD

    return laserpVal, laserstdFromBase

def onset_sustained_spike_proportion(cell, sessionType='bandwidth', sessionIndex=None, onsetTimeRange=[0.0,0.1], sustainedTimeRange=[0.1,1.0]):
    sessionIndices = get_session_inds(cell, sessionType)
    fullTimeRange = [onsetTimeRange[0], sustainedTimeRange[1]]
    if len(sessionIndices)>0:
        if sessionIndex is None:
            sessionIndex = sessionIndices[-1]
        eventData, spikeData = load_ephys_data(cell['subject'], cell['ephys'][sessionIndex], int(cell['tetrode']), int(cell['cluster']))
        eventOnsetTimes = eventData.get_event_onset_times()
        spikeTimeStamps = spikeData.timestamps
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimeStamps, 
                                                                                                                       eventOnsetTimes, 
                                                                                                                       fullTimeRange)
        
        onsetSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, onsetTimeRange)
        sustainedTimeRange = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, sustainedTimeRange)
        propOnset = 1.0*sum(onsetSpikeCountMat)/(sum(onsetSpikeCountMat)+sum(sustainedTimeRange))
        return propOnset
    else:
        return None

def sound_response_any_stimulus_old(cell, timeRange=[0.0,1.0], baseRange=[-1.1,-0.1], sessionType='bandwidth', sessionIndex=None):
    sessionIndices = get_session_inds(cell, sessionType)
    soundResponse = None
    fullTimeRange = [min(min(timeRange),min(baseRange)), max(max(timeRange),max(baseRange))]
    if len(sessionIndices)>0:
        soundResponse = False
        if sessionIndex is None:
            sessionIndex = sessionIndices[-1]
        eventData, spikeData = load_ephys_data(cell['subject'], cell['ephys'][sessionIndex], int(cell['tetrode']), int(cell['cluster']))
        eventOnsetTimes = eventData.get_event_onset_times()
        spikeTimeStamps = spikeData.timestamps
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimeStamps, 
                                                                                                                       eventOnsetTimes, 
                                                                                                                       fullTimeRange)
        stimSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
        baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseRange)
        baseSpikeCountMat = baseSpikeCountMat.flatten()
        
        if sessionType == 'bandwidth':
            bdata = load_behaviour_data(cell['subject'], cell['behavior'][sessionIndex])  
            firstSort = bdata['currentBand']
            numFirst = np.unique(firstSort)
            secondSort = bdata['currentAmp']
            numSec = np.unique(secondSort)
        
        totalConds = len(numFirst)*len(numSec)
        trialsEachCond = behavioranalysis.find_trials_each_combination(firstSort,numFirst,secondSort,numSec)
        
        alphaVal = 0.01/totalConds
        
        for sec in range(len(numSec)):
            trialsThisSec = trialsEachCond[:,:,sec]
            for first in range(len(numFirst)):
                trialsThisFirst = trialsThisSec[:,first]
                if stimSpikeCountMat.shape[0] != len(trialsThisFirst):
                    stimSpikeCountMat = stimSpikeCountMat[:-1,:]
                    print "FIXME: Using bad hack to make event onset times equal number of trials"
                if any(trialsThisFirst):
                    thisFirstStimCounts = stimSpikeCountMat[trialsThisFirst].flatten()
                    pValThisFirst = stats.ranksums(thisFirstStimCounts, baseSpikeCountMat)[1]
                    if pValThisFirst < alphaVal:
                        soundResponse = True
    return soundResponse
                    
def sound_response_any_stimulus(eventOnsetTimes, spikeTimeStamps, bdata, timeRange=[0.0,1.0], baseRange=[-1.1,-0.1], sessionType='bandwidth', sessionIndex=None):
    soundResponse = False
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
    
    totalConds = len(numFirst)*len(numSec)
    trialsEachCond = behavioranalysis.find_trials_each_combination(firstSort,numFirst,secondSort,numSec)
    
    alphaVal = 0.01/totalConds
    
    for sec in range(len(numSec)):
        trialsThisSec = trialsEachCond[:,:,sec]
        for first in range(len(numFirst)):
            trialsThisFirst = trialsThisSec[:,first]
            if stimSpikeCountMat.shape[0] == len(trialsThisFirst)+1:
                stimSpikeCountMat = stimSpikeCountMat[:-1,:]
                print "FIXME: Using bad hack to make event onset times equal number of trials"
            elif stimSpikeCountMat.shape[0] != len(trialsThisFirst):
                print "STOP NO THIS IS BAD"
                raise ValueError
            if any(trialsThisFirst):
                thisFirstStimCounts = stimSpikeCountMat[trialsThisFirst].flatten()
                pValThisFirst = stats.ranksums(thisFirstStimCounts, baseSpikeCountMat)[1]
                if pValThisFirst < alphaVal:
                    soundResponse = True
    return soundResponse
        

# --- Methods for generating intermediate data ---

def bandwidth_tuning_stats(cell, bandIndex, timeRange=[0.0,1.0], baseRange=[-1.1,-0.1], subtractBaseline=False):
    if bandIndex is None:
        print "No bandwidth session given"
        return None, None, None
    
    suppressionIndex = np.zeros(len(bandIndex))
    facilitationIndex = np.zeros_like(suppressionIndex)
    preferedBandwidth = np.zeros_like(suppressionIndex)
    
    for ind,index in enumerate(bandIndex):
        if index is not None:
            eventData, spikeData = load_ephys_data(cell['subject'], cell['ephys'][index], int(cell['tetrode']), int(cell['cluster']))
            eventOnsetTimes = eventData.get_event_onset_times()
            spikeTimeStamps = spikeData.timestamps
            bandBData = load_behaviour_data(cell['subject'], cell['behavior'][index])
            
            bandEachTrial = bandBData['currentBand']
            ampEachTrial = bandBData['currentAmp']
            numBands = np.unique(bandEachTrial)
            
            spikeArray, errorArray, baselineSpikeRate = calculate_tuning_curve_inputs(spikeTimeStamps, eventOnsetTimes, ampEachTrial, bandEachTrial, timeRange, baseRange)
            
            if not subtractBaseline:
                baselineSpikeRate = 0
        
            suppressionIndex[ind] = (max(spikeArray[ind,:])-spikeArray[ind,:][-1])/(max(spikeArray[ind,:])-baselineSpikeRate)
            facilitationIndex[ind] = (max(spikeArray[ind,:])-spikeArray[ind,:][0])/(max(spikeArray[ind,:])-baselineSpikeRate)
            preferedBandwidth[ind] = numBands[np.argmax(spikeArray[ind,:])]
        else:
            suppressionIndex[ind] = None
            facilitationIndex[ind] = None
            preferedBandwidth[ind] = None
    return suppressionIndex, facilitationIndex, preferedBandwidth


def calculate_tuning_curve_inputs(spikeTimeStamps, eventOnsetTimes, firstSort, secondSort, timeRange, baseRange, errorType = 'sem'):
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
    for sec in range(len(numSec)):
        trialsThisSec = trialsEachCond[:,:,sec]
        for first in range(len(numFirst)):
            trialsThisFirst = trialsThisSec[:,first]
            if spikeCountMat.shape[0] != len(trialsThisFirst):
                spikeCountMat = spikeCountMat[:-1,:]
                print "FIXME: Using bad hack to make event onset times equal number of trials"
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
    return spikeArray, errorArray, baselineSpikeRate
    
    