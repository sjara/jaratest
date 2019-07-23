'''
WRITE DESCRIPTION HERE!

This script takes as argument the name of the animal to process.

TO DO:
- Make sure inforec files get reloaded (by celldatabase.py)
'''

import sys
import os
import pandas as pd
import numpy as np

from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
reload(settings)

import subjects_info
reload(subjects_info)

from scipy import stats


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

# compares firing rate during response range and base range, gives p value and test statistic
def laser_response(ephysData, baseRange = [-0.05,-0.04], responseRange = [0.0, 0.01]):
    fullTimeRange = [baseRange[0], responseRange[1]]
    eventOnsetTimes = ephysData['events']['laserOn']
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
    return testStatistic, pVal

# determines if there's any combination of parameters that yields a change
def sound_response_any_stimulus(eventOnsetTimes, spikeTimeStamps, trialsEachCond, timeRange=[0.0,1.0], baseRange=[-1.1,-0.1]):
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
        
        for ind2 in range(len(numFreqs)):
            trialsThisFreq = trialsEachFreq[:,ind2]
            spikeCountsThisFreq = spikeCountMat[trialsThisFreq]
            baseCountsThisFreq = baseSpikeCountMat[trialsThisFreq]
            zScore, pVal = stats.ranksums(spikeCountsThisFreq, baseCountsThisFreq)
            zscores[ind,ind2] = zScore

    maxInd = np.unravel_index(zscores.argmax(), zscores.shape)
    windowToUse = windowsToTry[maxInd[0]]
    return windowToUse

# fits gaussian curve to frequency tuning data
def gaussian_tuning_fit(stimArray, responseArray):
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

# determine distance between cell's pref frequency and frequency presented during bandwidth session
# also determines index of bandwidth session with center frequency closest to pref freq if multiple sessions were done
def best_index(cellObj, bestFreq, behavType = 'bandwidth'):
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


if __name__=='__main__':

    import pdb
    archTmice = subjects_info.PV_ARCHT_MICE + subjects_info.SOM_ARCHT_MICE
    chr2mice = subjects_info.PV_CHR2_MICE + subjects_info.SOM_CHR2_MICE

    if len(sys.argv[1:]):
        if sys.argv[1] == 'archt':
            subjects = archTmice
            allSubjects = archTmice
            subType = 'archt'
        elif sys.argv[1] == 'chr2':
            subjects = chr2mice
            allSubjects = chr2mice
            subType = 'chr2'
        else:
            subjects = sys.argv[1:]
            if set(subjects).issubset(chr2mice):
                allSubjects = chr2mice
                subType = 'chr2'
            elif set(subjects).issubset(archTmice):
                allSubjects = archTmice
                subType = 'archt'
            else:
                sys.exit("Please ensure all subjects are from the same set (archt or chr2 mice)")
    else:
        sys.exit("Please input mice to analyse:\n\"archt\" for all archt mice\n\"chr2\" for all chr2 mice\nor any list of subjects of the same type (all archt or all chr2)")
    
    #pdb.set_trace()
    
    for subject in subjects:
        inforec = os.path.join(settings.INFOREC_PATH,'{0}_inforec.py'.format(subject))
        db = celldatabase.generate_cell_database(inforec)
                
        # --- Keep only good cells ---
        db = db[(db['isiViolations'] < 0.05) | (db['spikeShapeQuality'] > 2)]
        
        # --- compute statistics used for selection for each cell ---
        if subType == 'chr2':
            laserTestStatistic = np.empty(len(db))
            laserPVal = np.empty(len(db))
            laserTrainTestStatistic = np.empty(len(db))
            laserTrainPVal = np.empty(len(db))
        
        soundResponseTestStatistic = np.empty(len(db))
        soundResponsePVal = np.empty(len(db))
        onsetSoundResponseTestStatistic = np.empty(len(db))
        onsetSoundResponsePVal = np.empty(len(db))
        sustainedSoundResponseTestStatistic = np.empty(len(db))
        sustainedSoundResponsePVal = np.empty(len(db))
        
        gaussFit = []
        tuningTimeRange = []
        Rsquared = np.empty(len(db))
        prefFreq = np.empty(len(db))
        octavesFromPrefFreq = np.empty(len(db))
        bestBandSession = np.empty(len(db))
        
        for indRow, (dbIndex, dbRow) in enumerate(db.iterrows()):
            cellObj = ephyscore.Cell(dbRow)
            print "Now processing", dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster']
            
            # --- Laser responsiveness (photoidentification only) ---
            if subType == 'chr2':
                # --- Determine laser responsiveness of each cell (using laser pulse) ---
                try:
                    laserEphysData, noBehav = cellObj.load('laserPulse')
                except IndexError:
                    print "No laser pulse session for this cell"
                    testStatistic = None
                    pVal = None
                else:
                    testStatistic, pVal = laser_response(laserEphysData)
                laserTestStatistic[indRow] = testStatistic
                laserPVal[indRow] = pVal
                
                # --- Determine laser responsiveness of each cell (using laser train) ---
                try:
                    laserTrainEphysData, noBehav = cellObj.load('laserTrain')
                except IndexError:
                    print "No laser train session for this cell"
                    testStatistic = np.nan
                    pVal = np.nan
                else:
                    testStatistic, pVal = laser_response(laserTrainEphysData)
                laserTrainTestStatistic[indRow] = testStatistic
                laserTrainPVal[indRow] = pVal
            
            # --- Determine sound responsiveness during bandwidth sessions ---
            if subType == 'chr2':
                sessionType = 'bandwidth'
            elif subType == 'archt':
                sessionType = 'laserBandwidth'
            try:
                bandEphysData, bandBehavData = cellObj.load(sessionType)
            except IndexError:
                print "No bandwidth session for this cell"
                testStatistic = np.nan
                pVal = np.nan
                onsetTestStatistic = np.nan
                onsetpVal = np.nan
                sustainedTestStatistic = np.nan
                sustainedpVal = np.nan
            else:
                bandEventOnsetTimes = get_sound_onset_times(bandEphysData, 'bandwidth')
                bandSpikeTimestamps = bandEphysData['spikeTimes']
                bandEachTrial = bandBehavData['currentBand']
                if subType == 'chr2':
                    secondSort = bandBehavData['currentAmp']
                    cond = -1
                if subType == 'archt':
                    secondSort = bandBehavData['laserTrial']
                    cond = 0
                numBands = np.unique(bandEachTrial)
                numSec = np.unique(secondSort)
                trialsEachComb = behavioranalysis.find_trials_each_combination(bandEachTrial, numBands, secondSort, numSec)
                trialsEachBaseCond = trialsEachComb[:,:,cond] #using high amp trials for photoidentified, no laser for inactivation
                testStatistic, pVal = sound_response_any_stimulus(bandEventOnsetTimes, bandSpikeTimestamps, trialsEachBaseCond, [0.0, 1.0], [-1.2,-0.2])
                onsetTestStatistic, onsetpVal = sound_response_any_stimulus(bandEventOnsetTimes, bandSpikeTimestamps, trialsEachBaseCond, [0.0,0.05], [-0.25,0.2])
                sustainedTestStatistic, sustainedpVal = sound_response_any_stimulus(bandEventOnsetTimes, bandSpikeTimestamps, trialsEachBaseCond, [0.2,1.0], [-1.0,0.2])
                pVal *= len(numSec) #correction for multiple comparisons
                onsetpVal *= len(numSec)
                sustainedpVal *= len(numSec)
            soundResponseTestStatistic[indRow] = testStatistic
            soundResponsePVal[indRow] = pVal
            onsetSoundResponseTestStatistic[indRow] = onsetTestStatistic
            onsetSoundResponsePVal[indRow] = onsetpVal
            sustainedSoundResponseTestStatistic[indRow] = sustainedTestStatistic
            sustainedSoundResponsePVal[indRow] = sustainedpVal
            
            # --- Determine frequency tuning of cells ---
            try:
                tuningEphysData, tuningBehavData = cellObj.load('tuningCurve')
            except IndexError:
                print "No tuning session for this cell"
                freqFit = np.zeros(4)
                thisRsquared = np.nan
                bestFreq = np.nan
                tuningWindow = [0,0]
                octavesFromBest = np.nan
                bandIndex = np.nan
            else:
                tuningEventOnsetTimes = get_sound_onset_times(tuningEphysData, 'tuningCurve')
                tuningSpikeTimestamps = tuningEphysData['spikeTimes']
                freqEachTrial = tuningBehavData['currentFreq']
                intensityEachTrial = tuningBehavData['currentIntensity']
                numFreqs = np.unique(freqEachTrial)
                numIntensities = np.unique(intensityEachTrial)
                timeRange = [-0.2, 0.2]
                spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        tuningSpikeTimestamps, 
                                                                                                        tuningEventOnsetTimes,
                                                                                                        timeRange)
                trialsEachType = behavioranalysis.find_trials_each_type(intensityEachTrial, numIntensities)
                trialsHighInt = trialsEachType[:,-1]
                trialsEachComb = behavioranalysis.find_trials_each_combination(freqEachTrial, numFreqs, intensityEachTrial, numIntensities)
                trialsEachFreqHighInt = trialsEachComb[:,:,-1]
                tuningWindow = best_window_freq_tuning(spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachFreqHighInt)
                spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, tuningWindow)
                tuningSpikeRates = (spikeCountMat[trialsHighInt].flatten())/(tuningWindow[1]-tuningWindow[0])
                freqsThisIntensity = freqEachTrial[trialsHighInt]
                freqFit, thisRsquared = gaussian_tuning_fit(np.log2(freqsThisIntensity), tuningSpikeRates)
                if freqFit is not None:
                    bestFreq = 2**freqFit[0]
                    bandIndex, octavesFromBest = best_index(cellObj, bestFreq, sessionType)
                else:
                    freqFit = np.zeros(4)
                    bestFreq = np.nan
                    bandIndex = np.nan
                    octavesFromBest = np.nan
            gaussFit.append(freqFit)
            tuningTimeRange.append(tuningWindow)
            Rsquared[indRow] = thisRsquared
            prefFreq[indRow] = bestFreq
            octavesFromPrefFreq[indRow] = octavesFromBest
            bestBandSession[indRow] = bandIndex
                
        if subType == 'chr2': 
            db['laserPVal'] = laserPVal
            db['laserUStat'] = laserTestStatistic
            db['laserTrainPVal'] = laserTrainPVal
            db['laserTrainUStat'] = laserTrainTestStatistic
        
        db['soundResponseUStat'] = soundResponseTestStatistic
        db['soundResponsePVal'] = soundResponsePVal
        db['onsetSoundResponseUStat'] = onsetSoundResponseTestStatistic
        db['onsetSoundResponsePVal'] = onsetSoundResponsePVal
        db['sustainedSoundResponseUStat'] = sustainedSoundResponseTestStatistic
        db['sustainedSoundResponsePVal'] = sustainedSoundResponsePVal
        
        db['gaussFit'] = gaussFit
        db['tuningTimeRange'] = tuningTimeRange
        db['tuningFitR2'] = Rsquared
        db['prefFreq'] = prefFreq
        db['octavesFromPrefFreq'] = octavesFromPrefFreq
        db['bestBandSession'] = bestBandSession
        
        
        # save db as h5 
        dbFilenameNew = os.path.join(settings.DATABASE_PATH,'{0}_clusters.h5'.format(subject))
        celldatabase.save_hdf(db, dbFilenameNew)
        print('Saved database to: {}'.format(dbFilenameNew))
        
    fulldb = pd.DataFrame()
    for subject in allSubjects:
        dbFilename = os.path.join(settings.DATABASE_PATH,'{0}_clusters.h5'.format(subject))
        db = celldatabase.load_hdf(dbFilename)
        fulldb = fulldb.append(db, ignore_index=True)
    if subType == 'chr2':
        filename = 'photoidentification_cells.h5'
    elif subType == 'archt':
        filename = 'inactivation_cells.h5'
    fulldbFilename = os.path.join(settings.DATABASE_PATH,filename)
    celldatabase.save_hdf(fulldb, fulldbFilename)

