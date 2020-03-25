''' Contains all the functions called during database creation.
Functions include calculation of laser response, sound response, frequency tuning, suppression index, etc'''


import os
import numpy as np

from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis

from scipy import stats

# for correcting sound onset times for cells recorded before installation of Cliff box
AVERAGE_JITTER = {'bandwidth':0.0093,
                  'harmonics':0.0094,
                  'tuningCurve':0.0095,
                  'AM':0.0091,
                  'noiseAmps': 0.0091}

def get_sound_onset_times(ephysData, sessionType):
    '''Corrects onset times using estimated average jitter for data collected before installation of sound detector.
    
    Inputs:
        ephysData: full dictionary of ephys data for session in question
        sessionType: string, type of session (for finding proper correction to use)
    Outputs:
        eventOnsetTimes: time stamps of event onset, either according to sound detector (if that data exists) or estimated from stimOn and correction
    '''
    eventOnsetTimes = ephysData['events']['soundDetectorOn']
    if len(eventOnsetTimes)==0: #some cells recorded before sound detector installed
        eventOnsetTimes = ephysData['events']['stimOn'] + AVERAGE_JITTER[sessionType] #correction for onset times, determined by comparing sound detector onset to stim event onset
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.2)
    return eventOnsetTimes

def laser_response(ephysData, baseRange = [-0.05,-0.04], responseRange = [0.0, 0.01]):
    '''Compares firing rate during laser response range and base range.
    
    Inputs:
        ephysData: full dictionary of ephys data for laser pulse (or train) session
        baseRange: time range (relative to laser onset) to be used as baseline, list of [start time, end time]
        responseRange: time range (relative to laser onset) to be used as response, list of [start time, end time]
        
    Outputs:
        testStatistic: U test statistic of ranksums test between baseline and response
        pVal: p-value of ranksums test between baseline and response
        laserChangeFR: change in firing rate from baseline to response
    '''
    fullTimeRange = [baseRange[0], responseRange[1]]
    eventOnsetTimes = ephysData['events']['laserOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.5)
    spikeTimestamps = ephysData['spikeTimes']
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = \
            spikesanalysis.eventlocked_spiketimes(spikeTimestamps,
                                                      eventOnsetTimes,
                                                      fullTimeRange)
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                 indexLimitsEachTrial,
                                                                 baseRange)
    laserSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                  indexLimitsEachTrial,
                                                                  responseRange)
    [testStatistic, pVal] = stats.ranksums(laserSpikeCountMat, baseSpikeCountMat)
    laserChangeFR = np.mean(laserSpikeCountMat-baseSpikeCountMat)
    return testStatistic, pVal, laserChangeFR

def sound_response_any_stimulus(eventOnsetTimes, spikeTimeStamps, trialsEachCond, timeRange=[0.0,1.0], baseRange=[-1.1,-0.1]):
    '''Determines if there is any combination of parameters that yields a change in firing rate.
    
    Inputs:
        eventOnsetTimes: array of timestamps indicating sound onsets
        spikeTimeStamps: array of timestamps indicating when spikes occured
        trialsEachCond: (N trials x N conditions) array indicating which condition occured for each trial. Currently only checks over one parameter used during session.
        timeRange: time range (relative to sound onset) to be used as response, list of [start time, end time]
        baseRange: time range (relative to sound onset) to be used as baseline, list of [start time, end time]
        
    Outputs:
        maxzscore: maximum U test statistic found after comparing response for each condition to baseline
        minpVal: minimum p value found after comparing response for each condition to baseline, NOT CORRECTED FOR MULTIPLE COMPARISONS
    '''
    fullTimeRange = [min(min(timeRange),min(baseRange)), max(max(timeRange),max(baseRange))]
    
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimeStamps, 
                                                                                                                   eventOnsetTimes, 
                                                                                                                   fullTimeRange)
    stimSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseRange)
        
    minpVal = np.inf
    maxzscore = -np.inf
    for cond in range(trialsEachCond.shape[1]):
        trialsThisCond = trialsEachCond[:,cond]
        if stimSpikeCountMat.shape[0] == len(trialsThisCond)+1:
            stimSpikeCountMat = stimSpikeCountMat[:-1,:]
        if any(trialsThisCond):
            thisFirstStimCounts = stimSpikeCountMat[trialsThisCond].flatten()
            thisStimBaseSpikeCouns = baseSpikeCountMat[trialsThisCond].flatten()
            thiszscore, pValThisFirst = stats.ranksums(thisFirstStimCounts, thisStimBaseSpikeCouns)
            if pValThisFirst < minpVal:
                minpVal = pValThisFirst
            if thiszscore > maxzscore:
                maxzscore = thiszscore
    return maxzscore, minpVal

# determines best window for looking at frequency tuning based on which gives the largest zscore when compared to baseline response
def best_window_freq_tuning(spikeTimesFromEventOnset,indexLimitsEachTrial, trialsEachFreq, windowsToTry = [[0.0,0.1],[0.0,0.05],[0.1,0.15]]):
    zscores = np.zeros((len(windowsToTry),trialsEachFreq.shape[1]))

    for ind, window in enumerate(windowsToTry):
        duration = window[1]-window[0]
        baseTimeRange = [-0.1-duration, -0.1]
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, window)
        baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseTimeRange)
        
        for ind2 in range(trialsEachFreq.shape[1]):
            trialsThisFreq = trialsEachFreq[:,ind2]
            spikeCountsThisFreq = spikeCountMat[trialsThisFreq]
            baseCountsThisFreq = baseSpikeCountMat[trialsThisFreq]
            zScore, pVal = stats.ranksums(spikeCountsThisFreq, baseCountsThisFreq)
            zscores[ind,ind2] = zScore

    maxInd = np.unravel_index(zscores.argmax(), zscores.shape)
    windowToUse = windowsToTry[maxInd[0]]
    return windowToUse

def gaussian_tuning_fit(stimArray, responseArray):
    '''Fits gaussian curve to given data.
    
    Inputs:
        stimArray: array of length N trials giving stimulus used for each trial. For frequency tuning, take logarithm of frequencies (if presented freqs were on log scale)
        responseArray: array of length N trials giving spike rate during each trial.
        
    Outputs:
        curveFit: parameters for fit gaussian curve.
        Rsquared: R^2 value for fit curve compared to raw data.
    '''
    from scipy.optimize import curve_fit
    try:
        maxInd = np.argmax(responseArray)
        p0 = [stimArray[maxInd], responseArray[maxInd], 1.,0.]
        curveFit = curve_fit(gaussian, stimArray, responseArray, p0=p0, maxfev=10000)[0]
    except RuntimeError:
        print "Could not fit {} curve to tuning data.".format(type)
        return None, None
    
    #calculate R^2 value for fit
    fitResponseArray = gaussian(stimArray, curveFit[0], curveFit[1], curveFit[2], curveFit[3])
    residuals = responseArray - fitResponseArray
    SSresidual = np.sum(residuals**2)
    SStotal = np.sum((responseArray-np.mean(responseArray))**2)
    Rsquared = 1-(SSresidual/SStotal)
    
    return curveFit, Rsquared

def gaussian(x, mu, amp, sigma, offset):
    return offset+amp*np.exp(-((x-mu)/sigma)**2)

def best_index(cellObj, bestFreq, behavType = 'bandwidth'):
    '''Determines distance (in octaves) between cell's preferred frequency and centre frequency used during bandiwdth session.
    Also determines index of bandwidth session with centre frequency closes to preferred frequency if multiple bandwidth session were done.
    
    Inputs:
        cellObj: celldatabase cell object that allows for loading ephys and behaviour data (needed for loading multiple bandwidth sessions)
        bestFreq: calculated preferred frequency for this cell (float)
        behavType: type of session to analyse (string), defaults to 'bandwidth'
        
    Outputs:
        bestBehavIndex: index of session whose centre frequency best matches the preferred frequency.
        octavesFromBest: distance between preferred frequency and presented centre frequency (in octaves).
    '''
    behavIndex = cellObj.get_session_inds(behavType)
    charFreqs = []

    for ind in behavIndex:
        bdata = cellObj.load_behavior_by_index(ind) 
        charFreq = np.unique(bdata['charFreq'])[0]
        charFreqs.append(charFreq)

    # determine distance from best freq (in octaves) of char freq used and select closest session
    if bestFreq is not None and len(charFreqs)>0:
        octaveDiff = np.zeros(len(charFreqs))
        for ind, charFreq in enumerate(charFreqs):
            octaveDiff[ind] = np.log2(bestFreq/charFreq)
        octaveDiff = np.abs(octaveDiff)
        bestBehavIndex = behavIndex[np.argmin(octaveDiff)]
        octavesFromBest = min(octaveDiff)
    else:
        bestBehavIndex = None
        octavesFromBest = None
    return bestBehavIndex, octavesFromBest

def calculate_tuning_curve_inputs(spikeCountEachTrial, firstSort, secondSort):
    '''Calculates average firing rates for each condition required to plot a tuning curve for a given session.
    
    Inputs:
        spikeCountEachTrial: array of length N trials indicating the number of spikes that occurred during each trial
        firstSort: array of length N trials indicating value of first parameter for each trial (ex. bandwidths)
        secondSort: array of length N trials indicating value of second parameter for each trial (ex. amplitudes)
        
    Outputs:
        responseArray: array of size (N unique first parameter, N unique second parameter) indicating average spike counts for all trials with each combination of the two parameters
        errorArray: like responseArray, indicating s.e.m. for each value in responseArray
    '''
    numFirst = np.unique(firstSort)
    numSec = np.unique(secondSort)
    
    trialsEachCond = behavioranalysis.find_trials_each_combination(firstSort, 
                                                                   numFirst, 
                                                                   secondSort, 
                                                                   numSec)

    spikeArray = np.zeros((len(numFirst), len(numSec)))
    errorArray = np.zeros_like(spikeArray)
    
    for sec in range(len(numSec)):
        trialsThisSec = trialsEachCond[:,:,sec]
        for first in range(len(numFirst)):
            trialsThisFirst = trialsThisSec[:,first]
            if spikeCountEachTrial.shape[0] != len(trialsThisFirst):
                spikeCountEachTrial = spikeCountEachTrial[:-1,:]
            if any(trialsThisFirst):
                thisFirstCounts = spikeCountEachTrial[trialsThisFirst].flatten()
                spikeArray[first,sec] = np.mean(thisFirstCounts)
                errorArray[first,sec] = stats.sem(thisFirstCounts)
            else:
                spikeArray[first,sec] = np.nan
                errorArray[first,sec] = np.nan
    return spikeArray, errorArray

def inactivated_cells_baselines(spikeTimeStamps, eventOnsetTimes, laserEachTrial, baselineRange=[-0.05, 0.0]):
    '''For cells recorded during inhibitory cell inactivation, calculates baseline firing rate with and without laser.
    
    Inputs:
        spikeTimeStamps: array of timestamps indicating when spikes occurred
        eventOnsetTimes: array of timestamps indicating sound onsets
        firstSort: array of length N trials indicating whether laser was presented for each trial
        baselineRange: time range (relative to sound onset) to be used as baseline, list of [start time, end time]
        
    Outputs:
        baselineSpikeRates: array of length (N laser trial types), indicating baseline firing rate for each type of laser trial
        baselineSEMs: like baselineSpikeRates, gives s.e.m. for each value in baselineSpikeRates
    '''
    bandSpikeTimesFromEventOnset, trialIndexForEachSpike, bandIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimeStamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        baselineRange)
    
    numLaser = np.unique(laserEachTrial)
    baselineDuration = baselineRange[1]-baselineRange[0]
    baselineSpikeRates = np.zeros(len(numLaser))
    baselineSEMs = np.zeros_like(baselineSpikeRates)
    trialsEachLaser = behavioranalysis.find_trials_each_type(laserEachTrial, numLaser)
    baselineSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset,
                                                                         bandIndexLimitsEachTrial, baselineRange)
    for las in range(len(numLaser)):
        trialsThisLaser = trialsEachLaser[:,las]
        baselineCounts = baselineSpikeCountMat[trialsThisLaser].flatten()
        baselineMean = np.mean(baselineCounts)/baselineDuration
        baselineSEM = stats.sem(baselineCounts)/baselineDuration
        
        baselineSpikeRates[las] = baselineMean
        baselineSEMs[las] = baselineSEM
    
    #[testStatistic, pVal] = stats.ranksums(laserSpikeCountMat, baseSpikeCountMat)
    
    return baselineSpikeRates, baselineSEMs

def bandwidth_suppression_from_peak(spikeTimeStamps, eventOnsetTimes, firstSort, secondSort, timeRange=[0.2,1.0], baseRange=[-1.0,-0.2], subtractBaseline=False, zeroBWBaseline=True):
    '''Calculates suppression stats from raw data (no model).
    
    Inputs:
        spikeTimeStamps: array of timestamps indicating when spikes occurred
        eventOnsetTimes: array of timestamps indicating sound onsets
        firstSort: array of length N trials indicating value of first parameter for each trial (ex. bandwidths)
        secondSort: array of length N trials indicating value of second parameter for each trial. Second parameter should be manipulation being done (ex. laser), as it is used to calculate separate indices and baselines.
        timeRange: time period over which to calculate cell responses
        subtractBaseline: boolean, whether baseline firing rate should be subtracted from responses when calculating stats
        
    Output:
        suppressionIndex: suppression index for cell for each condition (e.g. for each amplitude, for each laser trial type)
        suppressionpVal: p value for each value in suppressionIndex
        facilitationIndex: facilitation index for cell for each condition
        facilitationpVal: p value for each value in facilitationIndex
        peakInd: index of responseArray containing largest firing rate (to calculate preferred bandwidth)
        spikeArray: array of size N condition 1 x N condition 2, average spike rates for each condition used to calculate suppression stats
    '''
    fullTimeRange = [baseRange[0], timeRange[1]]
    trialsEachCond = behavioranalysis.find_trials_each_combination(firstSort, 
                                                                   np.unique(firstSort), 
                                                                   secondSort, 
                                                                   np.unique(secondSort))
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimeStamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        fullTimeRange)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseRange)
    
    trialsEachSecondSort = behavioranalysis.find_trials_each_type(secondSort, np.unique(secondSort))
    
    spikeArray, errorArray = calculate_tuning_curve_inputs(spikeCountMat, firstSort, secondSort)
    spikeArray = spikeArray/(timeRange[1]-timeRange[0]) #convert spike counts to firing rate
    
    suppressionIndex = np.zeros(spikeArray.shape[1])
    facilitationIndex = np.zeros_like(suppressionIndex)
    peakInds = np.zeros_like(suppressionIndex)
    
    suppressionpVal = np.zeros_like(suppressionIndex)
    facilitationpVal = np.zeros_like(suppressionIndex)      
    
    for ind in range(len(suppressionIndex)):
        trialsThisSecondVal = trialsEachSecondSort[:,ind]
        
        thisCondResponse = spikeArray[:,ind]
        thisCondBaseline = np.mean(baseSpikeCountMat[trialsThisSecondVal].flatten())/(baseRange[1]-baseRange[0])
        
        if zeroBWBaseline:
            thisCondResponse[0] = thisCondBaseline
            
        if not subtractBaseline:
            thisCondBaseline = 0
            
        spikeArray[:,ind]=thisCondResponse
        
        suppressionIndex[ind] = (max(thisCondResponse)-thisCondResponse[-1])/(max(thisCondResponse)-thisCondBaseline)
        facilitationIndex[ind] = (max(thisCondResponse)-thisCondResponse[0])/(max(thisCondResponse)-thisCondBaseline)

        peakInd = np.argmax(thisCondResponse)
        peakInds[ind] = peakInd
        
        fullTrialsThisSecondVal = trialsEachCond[:,:,ind]
        
        if zeroBWBaseline:
            if peakInd==0:
                peakSpikeCounts = baseSpikeCountMat[trialsThisSecondVal].flatten()
            else:
                peakSpikeCounts = spikeCountMat[fullTrialsThisSecondVal[:,peakInd]].flatten()
            zeroBWSpikeCounts = baseSpikeCountMat[trialsThisSecondVal].flatten()
        else:
            peakSpikeCounts = spikeCountMat[fullTrialsThisSecondVal[:,peakInd]].flatten()
            zeroBWSpikeCounts = spikeCountMat[fullTrialsThisSecondVal[:,0]].flatten()
        
        
        whiteNoiseSpikeCounts = spikeCountMat[fullTrialsThisSecondVal[:,-1]].flatten()
        
        suppressionpVal[ind] = stats.ranksums(peakSpikeCounts, whiteNoiseSpikeCounts)[1]
        facilitationpVal[ind] = stats.ranksums(peakSpikeCounts, zeroBWSpikeCounts)[1]
        
    
    return suppressionIndex, suppressionpVal, facilitationIndex, facilitationpVal, peakInds, spikeArray

def onset_sustained_spike_proportion(spikeTimeStamps, eventOnsetTimes, onsetTimeRange=[0.0,0.05], sustainedTimeRange=[0.2,1.0]):
    '''Calculates proportion of spikes that occur at sound onset. Averaged across all bandwidths.
    
    Inputs:
        spikeTimeStamps: array of timestamps indicating when spikes occurred
        eventOnsetTimes: array of timestamps indicating sound onsets
        onsetTimeRange: time range (relative to sound onset) to be used for onset response, list of [start time, end time]
        sustainedTimeRange: time range (relative to sound onset) to be used for sustained response, list of [start time, end time]
        
    Outputs:
        propOnset: float, proportion of cell's total spikes that occur within indicated onset time range
        propSustained: float, proportion of cell's total spikes that occur within indicated sustained time range
    '''
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