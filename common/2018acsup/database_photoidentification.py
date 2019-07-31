'''
This script contains a function that computes new columns for a database of photoidentified cells.
'''

import os
import numpy as np
import imp

from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import histologyanalysis as ha

from jaratoolbox import settings

import database_generation_funcs as funcs
import database_bandwidth_tuning_fit_funcs as fitfuncs


def photoID_base_stats(db, filename = ''):
    '''
    This function takes as argument a pandas DataFrame and adds new columns.
    The filename should be the full path to where the database will be saved. If a filename is not specified, the database will not be saved.
    
    This function computed basic statistics for all clusters (e.g. laser responsiveness, sound responsiveness, preferred frequency).
    '''
    soundLoc = []
    NaKpeakLatency = np.empty(len(db))
    
    laserTestStatistic = np.empty(len(db))
    laserPVal = np.empty(len(db))
    laserTrainTestStatistic = np.empty(len(db))
    laserTrainPVal = np.empty(len(db))
    laserChangeFR = np.empty(len(db))
    
    soundResponseTestStatistic = np.empty(len(db))
    soundResponsePVal = np.empty(len(db))
    onsetSoundResponseTestStatistic = np.empty(len(db))
    onsetSoundResponsePVal = np.empty(len(db))
    sustainedSoundResponseTestStatistic = np.empty(len(db))
    sustainedSoundResponsePVal = np.empty(len(db))
    AMRate = np.empty(len(db))
    
    gaussFit = []
    tuningTimeRange = []
    Rsquared = np.empty(len(db))
    prefFreq = np.empty(len(db))
    octavesFromPrefFreq = np.empty(len(db))
    bestBandSession = np.empty(len(db))
    
    for indRow, (dbIndex, dbRow) in enumerate(db.iterrows()):
        cellObj = ephyscore.Cell(dbRow, useModifiedClusters=True)
        print "Now processing", dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster']
        
        # --- Determine if sound presentation was ipsi or contra to recording location ---
        soundSide = dbRow['info'][2]
        recordingSide = dbRow['brainArea']
        
        if (soundSide=='sound_left' and recordingSide=='left_AC') or (soundSide=='sound_right' and recordingSide=='right_AC'):
            soundLoc.append('ipsi')
        else:
            soundLoc.append('contra')
            
        # --- Determine time difference between Na and K peak (spike width) ---
        peakTimes = dbRow['spikePeakTimes']
        latency = peakTimes[2]-peakTimes[1]
        NaKpeakLatency[indRow] = latency
        
        # --- Determine laser responsiveness of each cell (using laser pulse) ---
        try:
            laserEphysData, noBehav = cellObj.load('laserPulse')
        except IndexError:
            print "No laser pulse session for this cell"
            testStatistic = np.nan
            pVal = np.nan
            changeFR = np.nan
        else:
            testStatistic, pVal, changeFR = funcs.laser_response(laserEphysData)
        laserTestStatistic[indRow] = testStatistic
        laserPVal[indRow] = pVal
        laserChangeFR[indRow] = changeFR
        
        # --- Determine laser responsiveness of each cell (using laser train) ---
        try:
            laserTrainEphysData, noBehav = cellObj.load('laserTrain')
        except IndexError:
            print "No laser train session for this cell"
            testStatistic = np.nan
            pVal = np.nan
        else:
            testStatistic, pVal, changeFR = funcs.laser_response(laserTrainEphysData)
        laserTrainTestStatistic[indRow] = testStatistic
        laserTrainPVal[indRow] = pVal
        
        # --- Determine sound responsiveness during bandwidth sessions and other statistics about bandwidth session---
        try:
            bandEphysData, bandBehavData = cellObj.load('bandwidth')
        except IndexError:
            print "No bandwidth session for this cell"
            testStatistic = np.nan
            pVal = np.nan
            onsetTestStatistic = np.nan
            onsetpVal = np.nan
            sustainedTestStatistic = np.nan
            sustainedpVal = np.nan
            AM = np.nan
        else:
            bandEventOnsetTimes = funcs.get_sound_onset_times(bandEphysData, 'bandwidth')
            bandSpikeTimestamps = bandEphysData['spikeTimes']
            bandEachTrial = bandBehavData['currentBand']
            secondSort = bandBehavData['currentAmp']
            numBands = np.unique(bandEachTrial)
            numSec = np.unique(secondSort)
            AM = np.unique(bandBehavData['modRate'])
            
            trialsEachComb = behavioranalysis.find_trials_each_combination(bandEachTrial, numBands, secondSort, numSec)
            trialsEachBaseCond = trialsEachComb[:,:,-1] #using high amp trials for photoidentified, no laser for inactivation
            testStatistic, pVal = funcs.sound_response_any_stimulus(bandEventOnsetTimes, bandSpikeTimestamps, trialsEachBaseCond, [0.0, 1.0], [-1.2,-0.2])
            onsetTestStatistic, onsetpVal = funcs.sound_response_any_stimulus(bandEventOnsetTimes, bandSpikeTimestamps, trialsEachBaseCond, [0.0,0.05], [-0.25,0.2])
            sustainedTestStatistic, sustainedpVal = funcs.sound_response_any_stimulus(bandEventOnsetTimes, bandSpikeTimestamps, trialsEachBaseCond, [0.2,1.0], [-1.0,0.2])
            pVal *= len(numSec) #correction for multiple comparisons
            onsetpVal *= len(numSec)
            sustainedpVal *= len(numSec)
        
        soundResponseTestStatistic[indRow] = testStatistic
        soundResponsePVal[indRow] = pVal
        onsetSoundResponseTestStatistic[indRow] = onsetTestStatistic
        onsetSoundResponsePVal[indRow] = onsetpVal
        sustainedSoundResponseTestStatistic[indRow] = sustainedTestStatistic
        sustainedSoundResponsePVal[indRow] = sustainedpVal
        AMRate[indRow] = AM
        
        # --- Determine frequency tuning of cells ---
        try:
            tuningEphysData, tuningBehavData = cellObj.load('tuningCurve')
        except IndexError:
            print "No tuning session for this cell"
            freqFit = np.full(4, np.nan)
            thisRsquared = np.nan
            bestFreq = np.nan
            tuningWindow = [np.nan,np.nan]
            octavesFromBest = np.nan
            bandIndex = np.nan
        else:
            tuningEventOnsetTimes = funcs.get_sound_onset_times(tuningEphysData, 'tuningCurve')
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
            tuningWindow = funcs.best_window_freq_tuning(spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachFreqHighInt)
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, tuningWindow)
            tuningSpikeRates = (spikeCountMat[trialsHighInt].flatten())/(tuningWindow[1]-tuningWindow[0])
            freqsThisIntensity = freqEachTrial[trialsHighInt]
            freqFit, thisRsquared = funcs.gaussian_tuning_fit(np.log2(freqsThisIntensity), tuningSpikeRates)
            if freqFit is not None:
                bestFreq = 2**freqFit[0]
                bandIndex, octavesFromBest = funcs.best_index(cellObj, bestFreq, 'bandwidth')
            else:
                freqFit = np.full(4, np.nan)
                bestFreq = np.nan
                bandIndex = np.nan
                octavesFromBest = np.nan
        gaussFit.append(freqFit)
        tuningTimeRange.append(tuningWindow)
        Rsquared[indRow] = thisRsquared
        prefFreq[indRow] = bestFreq
        octavesFromPrefFreq[indRow] = octavesFromBest
        bestBandSession[indRow] = bandIndex
        
    db['soundLocation'] = soundLoc
    db['spikeWidth'] = NaKpeakLatency
    db['AMRate'] = AMRate
            
    db['laserPVal'] = laserPVal
    db['laserUStat'] = laserTestStatistic
    db['laserTrainPVal'] = laserTrainPVal
    db['laserTrainUStat'] = laserTrainTestStatistic
    db['laserChangeFR'] = laserChangeFR
    
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
        
    if len(filename)!=0:        
        celldatabase.save_hdf(db, filename)
        print filename + " saved"
        
    return db
        
    
def photoID_indices(db, filename = ''):
    '''
    This function takes as argument a pandas DataFrame and adds new columns.
    The filename should be the full path to where the database will be saved. If a filename is not specified, the database will not be saved.
    
    This function computes indices like Suppression Index for all cells passing (generous) thresholds for good cells.
    The thresholds used here are more generous than the ones in studyparams, in case we want to relax our criteria in the future.
    '''
    
    bestCells = db.query("isiViolations<0.02 or modifiedISI<0.02")
    bestCells = bestCells.loc[bestCells['spikeShapeQuality']>2]
    bestCells = bestCells.query('soundResponsePVal<0.05 or onsetSoundResponsePVal<0.05 or sustainedSoundResponsePVal<0.05')
    bestCells = bestCells.loc[bestCells['tuningFitR2']>0.05]
    bestCells = bestCells.loc[bestCells['octavesFromPrefFreq']<0.5]
    
    #prepare arrays of NaNs for when we save arrays of data
    bandwidthSpikeArraysHighAmp = np.empty((len(db),7))
    bandwidthSpikeArraysHighAmp[:] = np.nan
    
    bandwidthSpikeArraysLowAmp = np.empty((len(db),7))
    bandwidthSpikeArraysLowAmp[:] = np.nan
    
    bandwidthSpikeArraysOnset = np.empty((len(db),6))
    bandwidthSpikeArraysOnset[:] = np.nan
    
    for dbIndex, dbRow in bestCells.iterrows():
        
        cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
        
        bandEphysData, bandBehavData = cell.load_by_index(int(dbRow['bestBandSession']))
        bandEventOnsetTimes = funcs.get_sound_onset_times(bandEphysData, 'bandwidth')
        bandSpikeTimestamps = bandEphysData['spikeTimes']
        
        bandEachTrial = bandBehavData['currentBand']
        secondSort = bandBehavData['currentAmp']
        
        propOnset, propSustained = funcs.onset_sustained_spike_proportion(bandSpikeTimestamps, bandEventOnsetTimes)
        
        db.at[dbIndex, 'proportionSpikesOnset'] = propOnset
        db.at[dbIndex, 'proportionSpikesSustained'] = propSustained       

        #by default: not subtracting baseline, but are replacing pure tone response with baseline for 0 bw condition
        onsetSupInds, onsetSupIndpVals, onsetFacInds, onsetFacIndpVals, onsetPeakInds, onsetSpikeArray = funcs.bandwidth_suppression_from_peak(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange=[0.0,0.05], baseRange=[-0.05,0.0])
        db.at[dbIndex, 'onsetSuppressionIndex'] = onsetSupInds[-1]
        db.at[dbIndex, 'onsetSuppressionpVal'] = onsetSupIndpVals[-1]
        db.at[dbIndex, 'onsetFacilitationIndex'] = onsetFacInds[-1]
        db.at[dbIndex, 'onsetFacilitationpVal'] = onsetFacIndpVals[-1]
        db.at[dbIndex, 'onsetPrefBandwidth'] = bandEachTrial[onsetPeakInds[-1]]
        
        sustainedSupInds, sustainedSupIndpVals, sustainedFacInds, sustainedFacIndpVals, sustainedPeakInds, sustainedSpikeArray = funcs.bandwidth_suppression_from_peak(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange=[0.2,1.0], baseRange=[-1.0,-0.2])
        db.at[dbIndex, 'sustainedSuppressionIndex'] = sustainedSupInds[-1]
        db.at[dbIndex, 'sustainedSuppressionpVal'] = sustainedSupIndpVals[-1]
        db.at[dbIndex, 'sustainedFacilitationIndex'] = sustainedFacInds[-1]
        db.at[dbIndex, 'sustainedFacilitationpVal'] = sustainedFacIndpVals[-1]
        db.at[dbIndex, 'sustainedPrefBandwidth'] = bandEachTrial[sustainedPeakInds[-1]]
        
        #only interested in high amp responses
        sustainedResponse = sustainedSpikeArray[:,-1]
        bandsForFit = np.unique(bandEachTrial)
        bandsForFit[-1] = 6
        mFixed = 1
        
        fitParams, R2 = fitfuncs.diff_of_gauss_fit(bandsForFit, sustainedResponse, mFixed=mFixed)
        
        #fit params
        db.at[dbIndex, 'R0'] = fitParams[0]
        db.at[dbIndex, 'RD'] = fitParams[3]
        db.at[dbIndex, 'RS'] = fitParams[4]
        db.at[dbIndex, 'm'] = mFixed
        db.at[dbIndex, 'sigmaD'] = fitParams[1]
        db.at[dbIndex, 'sigmaS'] = fitParams[2]
        db.at[dbIndex, 'bandwidthTuningR2'] = R2
        
        testBands = np.linspace(bandsForFit[0],bandsForFit[-1],500)
        allFitParams = [mFixed]
        allFitParams.extend(fitParams)
        suppInd, prefBW = fitfuncs.extract_stats_from_fit(allFitParams, testBands)
        
        db.at[dbIndex, 'fitSustainedSuppressionIndex'] = suppInd
        db.at[dbIndex, 'fitSustainedPrefBandwidth'] = prefBW
        
        #also calculating fits and suppression with pure tone being 0 bw condition
        toneSustainedSupInds, toneSustainedSupIndpVals, toneSustainedFacInds, toneSustainedFacIndpVals, toneSustainedPeakInds, toneSustainedSpikeArray = funcs.bandwidth_suppression_from_peak(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange=[0.2,1.0], baseRange=[-1.0,-0.2], zeroBWBaseline=False)
        db.at[dbIndex, 'sustainedSuppressionIndexPureTone'] = toneSustainedSupInds[-1]
        db.at[dbIndex, 'sustainedSuppressionpValPureTone'] = toneSustainedSupIndpVals[-1]
        db.at[dbIndex, 'sustainedFacilitationIndexPureTone'] = toneSustainedFacInds[-1]
        db.at[dbIndex, 'sustainedFacilitationpValPureTone'] = toneSustainedFacIndpVals[-1]
        db.at[dbIndex, 'sustainedPrefBandwidthPureTone'] = bandEachTrial[toneSustainedPeakInds[-1]]
        
        #only interested in high amp responses
        toneSustainedResponse = toneSustainedSpikeArray[:,-1]
        
        toneFitParams, toneR2 = fitfuncs.diff_of_gauss_fit(bandsForFit, toneSustainedResponse, mFixed=mFixed)
        
        #fit params
        db.at[dbIndex, 'R0PureTone'] = toneFitParams[0]
        db.at[dbIndex, 'RDPureTone'] = toneFitParams[3]
        db.at[dbIndex, 'RSPureTone'] = toneFitParams[4]
        db.at[dbIndex, 'mPureTone'] = mFixed
        db.at[dbIndex, 'sigmaDPureTone'] = toneFitParams[1]
        db.at[dbIndex, 'sigmaSPureTone'] = toneFitParams[2]
        db.at[dbIndex, 'bandwidthTuningR2PureTone'] = toneR2
        
        allFitParamsTone = [mFixed]
        allFitParamsTone.extend(toneFitParams)
        suppIndTone, prefBWTone = fitfuncs.extract_stats_from_fit(allFitParamsTone, testBands)
        
        db.at[dbIndex, 'fitSustainedSuppressionIndexPureTone'] = suppIndTone
        db.at[dbIndex, 'fitSustainedPrefBandwidthPureTone'] = prefBWTone
        
        #also calculating fits and suppression with nothing being fit for bw 0, want to do both intensities here
        #doing this for onset responses as well
        noZeroSustainedResponseHighAmp = sustainedSpikeArray[1:,-1]
        noZeroOnsetResponseHighAmp = onsetSpikeArray[1:,-1]
        bandsForFitNoZero = bandsForFit[1:]
        
        noZeroFitParamsHigh, noZeroR2High = fitfuncs.diff_of_gauss_fit(bandsForFitNoZero, noZeroSustainedResponseHighAmp, mFixed=mFixed)
        
        #fit params
        db.at[dbIndex, 'R0noZeroHighAmp'] = noZeroFitParamsHigh[0]
        db.at[dbIndex, 'RDnoZeroHighAmp'] = noZeroFitParamsHigh[3]
        db.at[dbIndex, 'RSnoZeroHighAmp'] = noZeroFitParamsHigh[4]
        db.at[dbIndex, 'mnoZeroHighAmp'] = mFixed
        db.at[dbIndex, 'sigmaDnoZeroHighAmp'] = noZeroFitParamsHigh[1]
        db.at[dbIndex, 'sigmaSnoZeroHighAmp'] = noZeroFitParamsHigh[2]
        db.at[dbIndex, 'bandwidthTuningR2noZeroHighAmp'] = noZeroR2High
        
        allFitParamsNoZeroHigh = [mFixed]
        allFitParamsNoZeroHigh.extend(noZeroFitParamsHigh)
        testBandsNoZero = np.linspace(bandsForFitNoZero[0],bandsForFitNoZero[-1],500)
        suppIndNoZero, prefBWNoZero = fitfuncs.extract_stats_from_fit(allFitParamsNoZeroHigh, testBandsNoZero)
        
        db.at[dbIndex, 'fitSustainedSuppressionIndexNoZeroHighAmp'] = suppIndNoZero
        db.at[dbIndex, 'fitSustainedPrefBandwidthNoZeroHighAmp'] = prefBWNoZero
        
        
        noZeroFitParamsOnset, noZeroR2Onset = fitfuncs.diff_of_gauss_fit(bandsForFitNoZero, noZeroOnsetResponseHighAmp, mFixed=mFixed)
        
        db.at[dbIndex, 'R0noZeroOnset'] = noZeroFitParamsOnset[0]
        db.at[dbIndex, 'RDnoZeroOnset'] = noZeroFitParamsOnset[3]
        db.at[dbIndex, 'RSnoZeroOnset'] = noZeroFitParamsOnset[4]
        db.at[dbIndex, 'mnoZeroOnset'] = mFixed
        db.at[dbIndex, 'sigmaDnoZeroOnset'] = noZeroFitParamsOnset[1]
        db.at[dbIndex, 'sigmaSnoZeroOnset'] = noZeroFitParamsOnset[2]
        db.at[dbIndex, 'bandwidthTuningR2noZeroOnset'] = noZeroR2Onset
        
        allFitParamsNoZeroOnset = [mFixed]
        allFitParamsNoZeroOnset.extend(noZeroFitParamsOnset)
        suppIndNoZero, prefBWNoZero = fitfuncs.extract_stats_from_fit(allFitParamsNoZeroOnset, testBandsNoZero)
        
        db.at[dbIndex, 'fitOnsetSuppressionIndexNoZero'] = suppIndNoZero
        db.at[dbIndex, 'fitOnsetPrefBandwidthNoZero'] = prefBWNoZero
        
        if sustainedSpikeArray.shape[1]>1: 
            noZeroSustainedResponseLowAmp = sustainedSpikeArray[1:,0]
            
            if all(noZeroSustainedResponseLowAmp):
                noZeroFitParamsLow, noZeroR2Low = fitfuncs.diff_of_gauss_fit(bandsForFitNoZero, noZeroSustainedResponseLowAmp, mFixed=mFixed)
                
                #fit params
                db.at[dbIndex, 'R0noZeroLowAmp'] = noZeroFitParamsLow[0]
                db.at[dbIndex, 'RDnoZeroLowAmp'] = noZeroFitParamsLow[3]
                db.at[dbIndex, 'RSnoZeroLowAmp'] = noZeroFitParamsLow[4]
                db.at[dbIndex, 'mnoZeroLowAmp'] = mFixed
                db.at[dbIndex, 'sigmaDnoZeroLowAmp'] = noZeroFitParamsLow[1]
                db.at[dbIndex, 'sigmaSnoZeroLowAmp'] = noZeroFitParamsLow[2]
                db.at[dbIndex, 'bandwidthTuningR2noZeroLowAmp'] = noZeroR2Low
                
                allFitParamsNoZeroLow = [mFixed]
                allFitParamsNoZeroLow.extend(noZeroFitParamsLow)
                suppIndNoZero, prefBWNoZero = fitfuncs.extract_stats_from_fit(allFitParamsNoZeroLow, testBandsNoZero)
                
                db.at[dbIndex, 'fitSustainedSuppressionIndexNoZeroLowAmp'] = suppIndNoZero
                db.at[dbIndex, 'fitSustainedPrefBandwidthNoZeroLowAmp'] = prefBWNoZero
        
        #save the spike array and baseline rate for each cell in case needed for future calculations
        bandwidthSpikeArraysHighAmp[dbIndex,:] = toneSustainedSpikeArray[:,-1]
        bandwidthSpikeArraysLowAmp[dbIndex,:] = toneSustainedSpikeArray[:,0]
        bandwidthSpikeArraysOnset[dbIndex,:] = noZeroOnsetResponseHighAmp
        db.at[dbIndex, 'bandwidthBaselineRate'] = sustainedResponse[0]
        
    
    db['bandwidthOnsetSpikeArrayHighAmp'] = list(bandwidthSpikeArraysOnset)
    db['bandwidthSustainedSpikeArrayHighAmp'] = list(bandwidthSpikeArraysHighAmp)
    db['bandwidthSustainedSpikeArrayLowAmp'] = list(bandwidthSpikeArraysLowAmp)
           
    if len(filename)!=0:        
        celldatabase.save_hdf(db, filename)
        print filename + " saved"
    
    return db


def photoDB_cell_locations(db, filename = ''):
    '''
    This function takes as argument a pandas DataFrame and adds new columns.
    The filename should be the full path to where the database will be saved. If a filename is not specified, the database will not be saved.
    
    This function computes the depths and cortical locations of all cells with suppression indices computed.
    This function should be run in a virtual environment because the allensdk has weird dependencies that we don't want tainting our computers.
    '''
    import nrrd
    from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache
    
    # lapPath = os.path.join(settings.ATLAS_PATH, 'AllenCCF_25/coronal_laplacian_25.nrrd')
    lapPath = '/mnt/jarahubdata/tmp/coronal_laplacian_25.nrrd'
    lapData = nrrd.read(lapPath)
    lap = lapData[0]
    
    mcc = MouseConnectivityCache(resolution=25)
    rsp = mcc.get_reference_space()
    rspAnnotationVolumeRotated = np.rot90(rsp.annotation, 1, axes=(2, 0))
    
    tetrodetoshank = {1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4} #hardcoded dictionary of tetrode to shank mapping for probe geometry used in this study
    
    bestCells = db[db['sustainedSuppressionIndex'].notnull()] #calculate depths for all the cells that we calculated SIs for
    
    db['recordingSiteName'] = '' #prefill will empty strings so whole column is strings (no NaNs)
    
    for dbIndex, dbRow in bestCells.iterrows():
        subject = dbRow['subject']
        
        try:
            fileNameInfohist = os.path.join(settings.INFOHIST_PATH,'{}_tracks.py'.format(subject))
            tracks = imp.load_source('tracks_module',fileNameInfohist).tracks
        except IOError:
            print("No such tracks file: {}".format(fileNameInfohist))
        else:
            brainArea = dbRow['brainArea']
            if brainArea == 'left_AC':
                brainArea = 'LeftAC'
            elif brainArea == 'right_AC':
                brainArea = 'RightAC'
            tetrode = dbRow['tetrode']
            shank = tetrodetoshank[tetrode]
            recordingTrack = dbRow['info'][0]
            
            track = next((track for track in tracks if (track['brainArea'] == brainArea) and (track['shank']==shank) and (track['recordingTrack']==recordingTrack)),None)
            
            if track is not None:
                histImage = track['histImage']
                
                filenameSVG = ha.get_filename_registered_svg(subject, brainArea, histImage, recordingTrack, shank)
                
                if tetrode%2==0:
                    depth = dbRow['depth']
                else:
                    depth = dbRow['depth'] - 150.0 #odd tetrodes are higher
                
                brainSurfCoords, tipCoords, siteCoords = ha.get_coords_from_svg(filenameSVG, [depth], dbRow['maxDepth'])
                
                siteCoords = siteCoords[0]
                
                atlasZ = track['atlasZ']
                cortexDepthData = np.rot90(lap[:,:,atlasZ], -1)
                 
                # We consider the points with depth > 0.95 to be the bottom surface of cortex
                bottomData = np.where(cortexDepthData>0.95)
                 
                # Top of cortex is less than 0.02 but greater than 0
                topData = np.where((cortexDepthData<0.02) & (cortexDepthData>0))

                # Distance between the cell and each point on the surface of the brain
                dXTop = topData[1] - siteCoords[0]
                dYTop = topData[0] - siteCoords[1]
                distanceTop = np.sqrt(dXTop**2 + dYTop**2)
                
                # The index and distance to the closest point on the top surface
                indMinTop = np.argmin(distanceTop)
                minDistanceTop = distanceTop.min()
            
                # Same for the distance from the cell to the bottom surface of cortex
                dXBottom = bottomData[1] - siteCoords[0]
                dYBottom = bottomData[0] - siteCoords[1]
                distanceBottom = np.sqrt(dXBottom**2 + dYBottom**2)
                minDistanceBottom = distanceBottom.min()
            
                # The metric we want is the relative distance from the top surface
                cellRatio = minDistanceTop / (minDistanceBottom + minDistanceTop)
                db.at[dbIndex, 'cortexRatioDepth'] = cellRatio
                
                # use allen annotated atlas to figure out where recording site is
                thisCoordID = rspAnnotationVolumeRotated[int(siteCoords[0]), int(siteCoords[1]), atlasZ]
                structDict = rsp.structure_tree.get_structures_by_id([thisCoordID])
                print "This is {}".format(str(structDict[0]['name']))
                db.at[dbIndex, 'recordingSiteName'] = structDict[0]['name']
                
            else:
                print subject, brainArea, shank, recordingTrack
                
    if len(filename)!=0:        
        celldatabase.save_hdf(db, filename)
        print filename + " saved"
    
    return db


