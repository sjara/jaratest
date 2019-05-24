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
reload(celldatabase)
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
reload(settings)

#import subjects_info
#reload(subjects_info)

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
def stim_response(ephysData, baseRange = [-0.05,-0.04], responseRange = [0.0, 0.01], stimType = 'laser'):
    fullTimeRange = [baseRange[0], responseRange[1]]
    if stimType == 'laser':
        eventOnsetTimes = ephysData['events']['laserOn']
    elif stimType == 'sound':
        eventOnsetTimes = get_sound_onset_times(ephysData, 'bandwidth')
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

    if len(sys.argv[1:]):
        subjects = sys.argv[1:]
    else:
        subjects = subjects_info.PV_ARCHT_MICE + subjects_info.SOM_ARCHT_MICE
    
    for subject in subjects:
        inforec = '/home/jarauser/src/jaratest/common/inforecordings/{0}_inforec.py'.format(subject)
        #inforec = os.path.join(settings.INFOREC_PATH,'{0}_inforec.py'.format(subject))
        db = celldatabase.generate_cell_database(inforec)
        
#         # NOTE: this way to remove bad cells seems too convoluted
#         #db = db.drop(db[(db['isiViolations'] > 0.05) | (db['spikeShapeQuality'] < 2)].index).reset_index(drop=True)
        
#         # --- Keep only good cells ---
#         db = db[(db['isiViolations'] < 0.05) | (db['spikeShapeQuality'] > 2)]
        
#         # --- compute statistics used for selection for each cell ---
#         laserTestStatistic = np.empty(len(db))
#         laserPVal = np.empty(len(db))
#         laserTrainTestStatistic = np.empty(len(db))
#         laserTrainPVal = np.empty(len(db))
        
#         soundResponseTestStatistic = np.empty(len(db))
#         soundResponsePVal = np.empty(len(db))
#         onsetSoundResponseTestStatistic = np.empty(len(db))
#         onsetSoundResponsePVal = np.empty(len(db))
#         sustainedSoundResponseTestStatistic = np.empty(len(db))
#         sustainedSoundResponsePVal = np.empty(len(db))
        
#         gaussFit = []
#         tuningTimeRange = []
#         Rsquared = np.empty(len(db))
#         prefFreq = np.empty(len(db))
#         octavesFromPrefFreq = np.empty(len(db))
#         bestBandSession = np.empty(len(db))
        
#         for indRow, (dbIndex, dbRow) in enumerate(db.iterrows()):
#             cellObj = ephyscore.Cell(dbRow)
#             print "Now processing", dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster']
            
#             # --- Determine laser responsiveness of each cell (using laser pulse) ---
#             try:
#                 laserEphysData, noBehav = cellObj.load('laserPulse')
#             except IndexError:
#                 print "No laser pulse session for this cell"
#                 testStatistic = None
#                 pVal = None
#             else:
#                 testStatistic, pVal = stim_response(laserEphysData)
#             laserTestStatistic[indRow] = testStatistic
#             laserPVal[indRow] = pVal
            
#             # --- Determine laser responsiveness of each cell (using laser train) ---
#             try:
#                 laserTrainEphysData, noBehav = cellObj.load('laserTrain')
#             except IndexError:
#                 print "No laser train session for this cell"
#                 testStatistic = None
#                 pVal = None
#             else:
#                 testStatistic, pVal = stim_response(laserTrainEphysData)
#             laserTrainTestStatistic[indRow] = testStatistic
#             laserTrainPVal[indRow] = pVal
            
#             '''
#             # --- Determine sound responsiveness during bandwidth sessions ---
#             try:
#                 bandEphysData, bandBehavData = cellObj.load('laserBandwidth')
#             except IndexError:
#                 print "No bandwidth session for this cell"
#                 testStatistic = None
#                 pVal = None
#                 onsetTestStatistic = None
#                 onsetpVal = None
#                 sustainedTestStatistic = None
#                 sustainedpVal = None
#             else:
#                 testStatistic, pVal = stim_response(bandEphysData, [-1.0,0.0], [0.0,1.0], 'sound')
#                 onsetTestStatistic, onsetpVal = stim_response(bandEphysData, [-0.05,0.0], [0.0,0.05], 'sound')
#                 sustainedTestStatistic, sustainedpVal = stim_response(bandEphysData, [-0.8,0.0], [0.2,1.0], 'sound')
#             soundResponseTestStatistic[indRow] = testStatistic
#             soundResponsePVal[indRow] = pVal
#             onsetSoundResponseTestStatistic[indRow] = onsetTestStatistic
#             onsetSoundResponsePVal[indRow] = onsetpVal
#             sustainedSoundResponseTestStatistic[indRow] = sustainedTestStatistic
#             sustainedSoundResponsePVal[indRow] = sustainedpVal
#             '''

#             # --- Determine frequency tuning of cells ---
#             try:
#                 tuningEphysData, tuningBehavData = cellObj.load('tuningCurve')
#             except IndexError:
#                 print "No tuning session for this cell"
#                 freqFit = np.zeros(4)
#                 thisRsquared = None
#                 bestFreq = None
#                 tuningWindow = [0,0]
#                 octavesFromBest = None
#                 bandIndex = None
#             else:
#                 tuningEventOnsetTimes = get_sound_onset_times(tuningEphysData, 'tuningCurve')
#                 tuningSpikeTimestamps = tuningEphysData['spikeTimes']
#                 freqEachTrial = tuningBehavData['currentFreq']
#                 intensityEachTrial = tuningBehavData['currentIntensity']
#                 numFreqs = np.unique(freqEachTrial)
#                 numIntensities = np.unique(intensityEachTrial)
#                 timeRange = [-0.2, 0.2]
#                 spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
#                                                                                                         tuningSpikeTimestamps, 
#                                                                                                         tuningEventOnsetTimes,
#                                                                                                         timeRange)
#                 trialsEachType = behavioranalysis.find_trials_each_type(intensityEachTrial, numIntensities)
#                 trialsHighInt = trialsEachType[:,-1]
#                 trialsEachComb = behavioranalysis.find_trials_each_combination(freqEachTrial, numFreqs, intensityEachTrial, numIntensities)
#                 trialsEachFreqHighInt = trialsEachComb[:,:,-1]
#                 tuningWindow = best_window_freq_tuning(spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachFreqHighInt)
#                 spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, tuningWindow)
#                 tuningSpikeRates = (spikeCountMat[trialsHighInt].flatten())/(tuningWindow[1]-tuningWindow[0])
#                 freqsThisIntensity = freqEachTrial[trialsHighInt]
#                 freqFit, thisRsquared = gaussian_tuning_fit(np.log2(freqsThisIntensity), tuningSpikeRates)
#                 if freqFit is not None:
#                     bestFreq = 2**freqFit[0]
#                     bandIndex, octavesFromBest = best_index(cellObj, bestFreq)
#                 else:
#                     freqFit = np.zeros(4)
#                     bestFreq = None
#                     bandIndex = None
#                     octavesFromBest = None

#             # --- Determine laser frequency tuning of cells ---
#             try:
#                 laserTuningEphysData, laserTuningBehavData = cellObj.load('laserTuningCurve')
#             except IndexError:
#                 print("No laser tuning session for this cell")
#                 laserFreqFit = np.zeros(4)
#                 thisRsquared = None
#                 bestFreq = None
#             else:
#                 laserTuningEventOnsetTimes = get_sound_onset_times(laserTuningEphysData, 'laserTuningCurve')
#                 laserTuningSpikeTimestamps = laserTuningEphysData['spikeTimes']
#                 freqEachTrial = laserTuningBehavData['currentFreq']
#                 intensityEachTrial = laserTuningBehavData['currentIntensity']
#                 laserEachTrial = laserTuningBehavData['laserOn']
#                 numFreqs = np.unique(freqEachTrial)
#                 numIntensities = np.unique(intensityEachTrial)
#                 numLasers = np.unique(laserEachTrial)
#                 timeRange = [-0.3, 0.6]
#                 spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
#                                                                                                         laserTuningSpikeTimestamps, 
#                                                                                                         laserTuningEventOnsetTimes,
#                                                                                                         timeRange)
#                 laserTrialsEachType = behavioranalysis.find_trials_each_type(laserEachTrial, numLasers)
#                 intTrialsEachType = behavioranalysis.find_trials_each_type(intensityEachTrial, numIntensities)
#                 laserTrialsEachComb = behavioranalysis.find_trials_each_combination(freqEachTrial, numFreqs, laserEachTrial, numLasers)
#                 intTrialsEachComb = behavioranalysis.find_trials_each_combination(freqEachTrial, numFreqs, intensityEachTrial, numIntensities)
#                 for indLaser in numLasers:
#                     #trialsEachType = behavioranalysis.find_trials_each_type(intensityEachTrial, numIntensities)
#                     #trialsHighInt = trialsEachType[:,-1]
#                     #trialsEachComb = behavioranalysis.find_trials_each_combination(freqEachTrial, numFreqs, intensityEachTrial, numIntensities)
#                     #trialsEachfreqHighInt = trialsEachComb[:,:,-1]
#                     trialsHighInt = laserTrialsEachType[:,indLaser] & intTrialsEachType[:,-1]
#                     trialsEachFreqHighInt = laserTrialsEachComb[:,:,indLaser] & intTrialsEachComb[:,:,-1]     
#                     tuningWindow = best_window_freq_tuning(spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachFreqHighInt)
#                     spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, tuningWindow)
#                     tuningSpikeRates = (spikeCountMat[trialsHighInt].flatten())/(tuningWindow[1]-tuningWindow[0])
#                     freqsThisIntensity = freqEachTrial[trialsHighInt]
#                     freqFit, thisRsquared = gaussian_tuning_fit(np.log2(freqsThisIntensity), tuningSpikeRates)
#                     if freqFit is not None:
#                         bestFreq = 2**freqFit[0]
#                         #bandIndex, octavesFromBest = best_index(cellObj, bestFreq)
#                     else:
#                         freqFit = np.zeros(4)
#                         bestFreq = None
#                         #bandIndex = None
#                         #octavesFromBest = None


#             gaussFit.append(freqFit)
#             tuningTimeRange.append(tuningWindow)
#             Rsquared[indRow] = thisRsquared
#             prefFreq[indRow] = bestFreq
#             #octavesFromPrefFreq[indRow] = octavesFromBest
#             #bestBandSession[indRow] = bandIndex
                
        
# #         db['laserPVal'] = laserPVal
# #         db['laserUStat'] = laserTestStatistic
# #         db['laserTrainPVal'] = laserTrainPVal
# #         db['laserTrainUStat'] = laserTrainTestStatistic
        
#         # db['soundResponseUStat'] = soundResponseTestStatistic
#         # db['soundResponsePVal'] = soundResponsePVal
#         # db['onsetSoundResponseUStat'] = onsetSoundResponseTestStatistic
#         # db['onsetSoundResponsePVal'] = onsetSoundResponsePVal
#         # db['sustainedSoundResponseUStat'] = sustainedSoundResponseTestStatistic
#         # db['sustainedSoundResponsePVal'] = sustainedSoundResponsePVal
        
#         db['gaussFit'] = gaussFit
#         db['tuningTimeRange'] = tuningTimeRange
#         db['Rsquared'] = Rsquared
#         db['prefFreq'] = prefFreq
#         # db['octavesFromPrefFreq'] = octavesFromPrefFreq
#         # db['bestBandSession'] = bestBandSession

        
#         # save db as h5 and csv
        
#         '''
#         dbFilename = os.path.join(settings.DATABASE_PATH,'{0}_test.h5'.format(subject))
#         db.to_hdf(dbFilename, 'database',mode='w')
#         print('Saved database to: {}'.format(dbFilename))
        
#         db.to_csv(dbFilename+'.csv')
#         print('Saved database to: {}'.format(dbFilename+'.csv'))
#         '''
        
        #dbFilenameNew = os.path.join(settings.DATABASE_PATH,'{0}_new.h5'.format(subject))
        dbFilenameNew = '/home/jarauser/data/databases/tmp/{}_new.h5'.format(subject)
        celldatabase.save_hdf(db, dbFilenameNew)
        print('Saved database to: {}'.format(dbFilenameNew))
        
        # -- To load the HDF5 --
        # df = celldatabase.load_hdf('/tmp/band045_new.h5')
        
    #allSubjects = subjects_info.PV_ARCHT_MICE + subjects_info.SOM_ARCHT_MICE
    #allSubjects = ['dapa012', 'dapa013', 'dapa014', 'dapa015']
    allSubjects = []
    fulldb = pd.DataFrame()
    for subject in allSubjects:
        db = celldatabase.load_hdf('/tmp/{}_new.h5'.format(subject))
        fulldb = fulldb.append(db, ignore_index=True)
    fulldbFilename = os.path.join(settings.DATABASE_PATH,'dapa_cells.h5')
    celldatabase.save_hdf(fulldb, fulldbFilename)





####################################################################################
####################################################################################
####################################################################################


# import os, sys
# from jaratoolbox import celldatabase
# from jaratoolbox import extraplots
# from jaratoolbox import spikesanalysis
# from jaratoolbox import spikesorting
# from jaratoolbox import behavioranalysis
# from jaratoolbox import loadbehavior
# from jaratoolbox import loadopenephys
# from jaratoolbox import ephyscore
# reload(loadopenephys)
# from jaratoolbox import settings
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
# import numpy as np
# from numpy import inf
# from scipy import optimize
# from scipy import stats
# import pdb

# subject = sys.argv[1]
# #subject = dapa011

# #Generate cell database
# inforec = '/home/jarauser/src/jaratest/common/inforecordings/{}_inforec.py'.format(subject)
# db = celldatabase.generate_cell_database(inforec)

# ####################################################################################

# def gaussian(x, a, x0, sigma, y0):
#     return a*np.exp(-(x-x0)**2/(2*sigma**2)) + y0

# ####################################################################################

# def generate_gaussian(cell):
#     coreCell = ephyscore.Cell(cell)
#     laserTuningSessionInds = coreCell.get_session_inds('laserTuningCurve')

#     if len(laserTuningSessionInds) == 0:
#         return np.nan, np.nan

#     #Init list to hold the optimized parameters for the gaussian for each intensity and laser
#     popts = []
#     Rsquareds = []

#     for sessionInd in laserTuningSessionInds:
#         bdata = coreCell.load_behavior_by_index(sessionInd)
#         ephysData = coreCell.load_ephys_by_index(sessionInd)
        
#         freqEachTrial = bdata['currentFreq']
#         laserEachTrial = bdata['laserOn']
#         intEachTrial = bdata['currentIntensity']
        
#         eventOnsetTimes = ephysData['events']['stimOn']
#         spikeTimeStamps = ephysData['spikeTimes']

#         timeRange = [-0.3, 0.6]
#         baseTimeRange = [0.0, 0.1]
#         alignmentRange = [baseTimeRange[0], timeRange[1]]   

#         possiblefreqs = np.unique(freqEachTrial)
#         freqLabels = [round(x/1000, 1) for x in possiblefreqs]
#         possiblelaser = np.unique(laserEachTrial)
#         possibleInts = np.unique(intEachTrial)

#         #Init arrays to hold the baseline and response spike counts per condition
#         allLaserIntenBase = np.array([])
#         allLaserIntenResp = np.empty((len(possiblelaser), len(possibleInts), len(possiblefreqs)))
#         allLaserIntenRespMedian = np.empty((len(possiblelaser), len(possibleInts), len(possiblefreqs)))

#         for indlaser, laser in enumerate(possiblelaser):
#             for indinten, inten in enumerate(possibleInts):
#                 spks = np.array([])
#                 freqs = np.array([])
#                 base = np.array([])
#                 for indfreq, freq in enumerate(possiblefreqs):
#                     selectinds = np.flatnonzero((freqEachTrial==freq)&(intEachTrial==inten)&(laserEachTrial==laser))
#                     try:
#                         selectedOnsetTimes = eventOnsetTimes[selectinds]
#                     except:
#                         print('index error')
#                         continue
#                     (spikeTimesFromEventOnset,
#                     trialIndexForEachSpike,
#                     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimeStamps,
#                                                                                 selectedOnsetTimes,
#                                                                                 alignmentRange)
#                     nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                                         indexLimitsEachTrial,
#                                                                         baseTimeRange)
#                     nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                                         indexLimitsEachTrial,
#                                                                         timeRange)
#                     base = np.concatenate([base, nspkBase.ravel()])
#                     spks = np.concatenate([spks, nspkResp.ravel()])
#                     # inds = np.concatenate([inds, np.ones(len(nspkResp.ravel()))*indfreq])
#                     freqs = np.concatenate([freqs, np.ones(len(nspkResp.ravel()))*freq])
#                     allLaserIntenBase = np.concatenate([allLaserIntenBase, nspkBase.ravel()])
#                     allLaserIntenResp[indlaser, indinten, indfreq] = np.mean(nspkResp)
#                     allLaserIntenRespMedian[indlaser, indinten, indfreq] = np.median(nspkResp)

#                 try:
#                     popt, pcov = optimize.curve_fit(gaussian, #Fit the curve for this intensity
#                                                     np.log2(freqs),
#                                                     spks,
#                                                     p0=[1, np.log2(possiblefreqs[7]), 1, allLaserIntenBase.mean()],
#                                                     #bounds=([0, np.log2(possiblefreqs[0]), 0, 0],
#                                                     #        [inf, np.log2(possiblefreqs[-1]), inf, inf])
#                                                     )
#                     popts.append(list(popt)) #Save the curve paramaters

#                     ## Calculate the R**2 value for the fit
#                     fittedSpks = gaussian(np.log2(freqs), *popt)
#                     residuals = spks - fittedSpks
#                     SSresidual = np.sum(residuals**2)
#                     SStotal = np.sum((spks-np.mean(spks))**2)
#                     Rsquared = 1-(SSresidual/SStotal)
#                     Rsquareds.append(Rsquared)

#                 except RuntimeError:
                    
#                     #failed=True
#                     #print "RUNTIME ERROR, Cell {}".format(cell)
#                     #runtimeErrorInds.append(indIter)
#                     #thresholds[indIter] = None
#                     #cfs[indIter] = None
#                     #lowerFreqs[indIter] = None
#                     #upperFreqs[indIter] = None
                    
#                     #print "RUNTIME ERROR, Cell {}".format(cell)
#                     popts.append([np.nan, np.nan, np.nan, np.nan])
#                     Rsquareds.append(np.nan)
#                     continue
                
#                 #plt.figure()
#                 #print(gaussian(popt[1], *popt))
#                 #plt.plot(np.log2(freqs), gaussian(np.log2(freqs), *popt))
#                 #plt.show()

#     #print(popts)
#     #print(Rsquareds)
#     return popts, Rsquareds

# ####################################################################################

# #Calculate shape quality
# allShapeQuality = np.empty(len(db))
# allGaussianVals = []
# allRsquareds = []
# for indCell, cell in db.iterrows():
#     print("Processing cell {}...".format(indCell))
#     peakAmplitudes = cell['spikePeakAmplitudes']
#     spikeShapeSD = cell['spikeShapeSD']
#     thisShapeQuality = abs(peakAmplitudes[1]/spikeShapeSD.mean())
#     allShapeQuality[indCell] = thisShapeQuality
#     gaussianVals, Rsquareds = generate_gaussian(cell)
#     #print(gaussianVals, Rsquareds)
#     allGaussianVals.append(gaussianVals)
#     allRsquareds.append(Rsquareds)
# allShapeQuality[allShapeQuality==np.inf]=0
# db['shapeQuality'] = allShapeQuality
# db['gaussianVals'] = allGaussianVals
# db['allRsquareds'] = allRsquareds

# filename = '/home/jarauser/data/databases/{}_clusterdatabase.h5'.format(subject)
# db.to_hdf(filename, key='database')


# ### Ask if people in the lab get the same Warning ###
# """
# In [34]: run generate_database.py
# /usr/lib/python2.7/dist-packages/pandas/io/pytables.py:2446: PerformanceWarning: 
# your performance may suffer as PyTables will pickle object types that it cannot
# map directly to c-types [inferred_type->mixed,key->block1_values] [items->['behavior', 'brainarea', 'clusterPeakAmplitudes', 'clusterPeakTimes', 'clusterSpikeSD', 'clusterSpikeShape', 'date', 'ephys', 'info', 'inforecPath', 'sessiontype', 'subject']]

#   warnings.warn(ws, PerformanceWarning)
# """