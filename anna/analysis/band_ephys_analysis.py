from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
reload(loadopenephys)
from jaratoolbox import settings
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from scipy import stats
import os
import pdb

# --- Methods for loading raw data ---

def get_session_inds(cell, sessiontype):
    return [i for i, st in enumerate(cell['sessiontype']) if st==sessiontype]

def load_ephys_data(subject, session, tetrode, cluster=None):
    ephysBaseDir = os.path.join(settings.EPHYS_PATH, subject)
    eventFilename=os.path.join(ephysBaseDir,
                               session,
                               'all_channels.events')
    spikesFilename=os.path.join(ephysBaseDir,
                                session,
                                'Tetrode{}.spikes'.format(tetrode))
    eventData=loadopenephys.Events(eventFilename)
    spikeData = loadopenephys.DataSpikes(spikesFilename)
    clustersDir = os.path.join(ephysBaseDir, '{}_kk'.format(session))
    clustersFile = os.path.join(clustersDir,'Tetrode{}.clu.1'.format(tetrode))
    spikeData.set_clusters(clustersFile)
    if cluster is not None:
        spikeData.samples=spikeData.samples[spikeData.clusters==cluster]
        spikeData.timestamps=spikeData.timestamps[spikeData.clusters==cluster]
    
    # convert to seconds and millivolts
    spikeData.samples = spikeData.samples.astype(float)-2**15
    spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
    spikeData.timestamps = spikeData.timestamps/spikeData.samplingRate
    eventData.timestamps = eventData.timestamps/eventData.samplingRate
    return eventData, spikeData
    
def load_behaviour_data(subject, fileName):
    behavFile = os.path.join(settings.BEHAVIOR_PATH,subject,fileName)
    bdata = loadbehavior.BehaviorData(behavFile,readmode='full')
    return bdata

# --- Methods for generating intermediate data ---

def best_index(cell, behavType):
    behavIndex = get_session_inds(cell, behavType)
    charFreqs = []
    if len(behavIndex)==0:
        print "No session of this type"
        return None, None, None, None, None
    for ind in behavIndex:
        bdata = load_behaviour_data(cell['subject'], cell['behavior'][ind]) 
        charFreq = np.unique(bdata['charFreq'])[0]
        charFreqs.append(charFreq)
    
    # high amp bandwidth trials used to select appropriate frequency
    maxAmp = max(np.unique(bdata['currentAmp']))
    if maxAmp < 1:
        maxAmp = 66.0 #HARDCODED dB VALUE FOR SESSIONS DONE BEFORE NOISE CALIBRATION
    
    # find tone intensity that corresponds to tone sessions in bandwidth trial
    toneInt = maxAmp - 15.0 #HARDCODED DIFFERENCE IN TONE AND NOISE AMP BASED ON OSCILLOSCOPE READINGS FROM RIG 2
    
    # determine the best frequency of the cell by fitting gaussian curve to tuning data
    tuningIndex = get_session_inds(cell, 'tuningCurve')[0]
    tuningBData = load_behaviour_data(cell['subject'], cell['behavior'][tuningIndex])
    eventData, spikeData = load_ephys_data(cell['subject'], cell['ephys'][tuningIndex], int(cell['tetrode']), int(cell['cluster']))
    eventOnsetTimes = eventData.get_event_onset_times()
    spikeTimeStamps = spikeData.timestamps
    freqEachTrial = tuningBData['currentFreq']
    numFreqs = np.unique(freqEachTrial)
    
    intensityEachTrial = tuningBData['currentIntensity']
    numIntensities = np.unique(intensityEachTrial)
    if toneInt in numIntensities:
        intensityInd = np.where(numIntensities==toneInt)
    else:
        intensityInd = (np.abs(numIntensities-toneInt)).argmin()
    spikeArray, errorArray, baselineSpikeRate = calculate_tuning_curve_inputs(spikeTimeStamps, eventOnsetTimes, freqEachTrial, intensityEachTrial, [0.0,0.1], [0.0,0.7])
    tuningArray = spikeArray[:,intensityInd].flatten()
    gaussFit, bestFreq, Rsquared = gaussian_freq_fit(numFreqs, tuningArray)
    
    # determine distance from best freq (in octaves) of char freq used and select closest session
    if bestFreq is not None:
        octaveDiff = np.zeros(len(charFreqs))
        for ind, charFreq in enumerate(charFreqs):
            octaveDiff[ind] = np.log2(bestFreq/charFreq)
        octaveDiff = np.abs(octaveDiff)
        behavIndex = behavIndex[np.argmin(octaveDiff)]
        octavesFromBest = min(octaveDiff)
        return behavIndex, bestFreq, gaussFit, Rsquared, octavesFromBest
    else:
        print "Could not determine best index with tuning data available"
        return None, None, None, None, None

def gaussian_freq_fit(freqArray, responseArray):
    #find best fit for frequency spike data
    from scipy.optimize import curve_fit
    logFreqArray = np.log2(freqArray)
    maxInd = np.argmax(responseArray)
    p0 = [logFreqArray[maxInd], responseArray[maxInd], 1.,0.]
    try:
        gaussFit = curve_fit(gaussian, logFreqArray, responseArray, p0=p0, maxfev=10000)[0]
    except RuntimeError:
        print "Could not fit gaussian curve to tuning data."
        return None, None, None
    #estimated best frequency based on gaussian fit
    bestFreq = 2**gaussFit[0]
    
    #calculate R^2 value for fit
    fitResponseArray = gaussian(logFreqArray, gaussFit[0], gaussFit[1], gaussFit[2], gaussFit[3])
    residuals = responseArray - fitResponseArray
    SSresidual = np.sum(residuals**2)
    SStotal = np.sum((responseArray-np.mean(responseArray))**2)
    Rsquared = 1-(SSresidual/SStotal)
    
    return gaussFit, bestFreq, Rsquared

def gaussian(x, mu, amp, sigma, offset):
    p = [mu, amp, sigma, offset]
    return p[3]+p[1]* np.exp(-((x-p[0])/p[2])**2)

def laser_response(cell, timeRange=[0.0, 0.1], baseRange=[0.5, 0.6]):
    laserIndex = get_session_inds(cell, 'laserPulse')
    if len(laserIndex)>0:
        eventData, spikeData = load_ephys_data(cell['subject'], cell['ephys'][laserIndex[-1]], int(cell['tetrode']), int(cell['cluster']))
        eventOnsetTimes = eventData.get_event_onset_times()
        spikeTimeStamps = spikeData.timestamps
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimeStamps, 
                                                                                                                       eventOnsetTimes, 
                                                                                                                       [min(timeRange),max(baseRange)])
        zStatsEachRange,pValueEachRange,maxZvalue = spikesanalysis.response_score(spikeTimesFromEventOnset, 
                                                                                  indexLimitsEachTrial, 
                                                                                  baseRange, 
                                                                                  timeRange)
        baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseRange)
        baselineSpikeRate = np.mean(baseSpikeCountMat)/(baseRange[1]-baseRange[0])
        laserSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
        laserSpikeRate = np.mean(laserSpikeCountMat)/(timeRange[1]-timeRange[0])
        laserResponse = (laserSpikeRate > baselineSpikeRate and pValueEachRange[0] < 0.00001)
    else:
        laserResponse = False

    return laserResponse

def bandwidth_tuning_stats(cell, bandIndex=None):
    import pdb
    if bandIndex is None:
        bandIndeces = get_session_inds(cell, 'bandwidth')
        if len(bandIndeces)==0:
            print "No session of this type"
            return None, None, None, None
        else:
            bandIndex = bandIndeces[0]
    eventData, spikeData = load_ephys_data(cell['subject'], cell['ephys'][bandIndex], int(cell['tetrode']), int(cell['cluster']))
    eventOnsetTimes = eventData.get_event_onset_times()
    spikeTimeStamps = spikeData.timestamps
    nBandSpikes = len(spikeTimeStamps)
    bandBData = load_behaviour_data(cell['subject'], cell['behavior'][bandIndex])
    
    timeRange = [0.0, 1.0]
    bandEachTrial = bandBData['currentBand']
    ampEachTrial = bandBData['currentAmp']
    numBands = np.unique(bandEachTrial)
    
    spikeArray, errorArray, baselineSpikeRate = calculate_tuning_curve_inputs(spikeTimeStamps, eventOnsetTimes, ampEachTrial, bandEachTrial, timeRange)
    
    suppressionIndex = np.zeros(spikeArray.shape[0])
    facilitationIndex = np.zeros_like(suppressionIndex)
    preferedBandwidth = np.zeros_like(suppressionIndex)

    for amp in range(len(suppressionIndex)):
        suppressionIndex[amp] = (max(spikeArray[amp,:])-spikeArray[amp,:][-1])/max(spikeArray[amp,:])
        facilitationIndex[amp] = (max(spikeArray[amp,:])-spikeArray[amp,:][0])/max(spikeArray[amp,:])
        preferedBandwidth[amp] = numBands[np.argmax(spikeArray[amp,:])]
        #pdb.set_trace()
        
    return suppressionIndex, facilitationIndex, preferedBandwidth, nBandSpikes
    
def calculate_tuning_curve_inputs(spikeTimeStamps, eventOnsetTimes, firstSort, secondSort, timeRange, fullRange = [0.0, 2.0]):
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
                                                                                                        fullRange)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    baseTimeRange = [timeRange[1]+0.5, fullRange[1]]
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseTimeRange)
    baselineSpikeRate = np.mean(baseSpikeCountMat)/(baseTimeRange[1]-baseTimeRange[0])
    plt.hold(True)
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
                errorArray[first,sec] = stats.sem(thisFirstCounts)/duration
            else:
                spikeArray[first,sec] = np.nan
                errorArray[first,sec] = np.nan
    return spikeArray, errorArray, baselineSpikeRate
    
    