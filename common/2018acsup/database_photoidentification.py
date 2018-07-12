'''
This script takes as argument a pandas DataFrame or a path to a saved database and adds new columns.

Columns added are split into two groups: the basic stats computed for every cluster, and the more complex
ones computed only for cells that pass certain criteria based on these basic stats.

Either can be chosen to be run, the final database is saved regardless.

A name for the saved database can be passed if you want a separate database for whatever reason.

TO DO:
- Split up into smaller functions for each computation to make flow more clear
'''

import os
import pandas as pd
import numpy as np

from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis

from jaratoolbox import settings

import database_generation_funcs as funcs

R2CUTOFF = 0.1
OCTAVESCUTOFF = 0.3


def photoIDdatabase(db, baseStats = False, indices = True, filename = 'photoidentification_cells.h5'):
    if type(db) == str:
        dbPath = os.path.join(settings.DATABASE_PATH,db)
        db = celldatabase.load_hdf(dbPath)
        
    if baseStats:
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
    
            # --- Determine laser responsiveness of each cell (using laser pulse) ---
            try:
                laserEphysData, noBehav = cellObj.load('laserPulse')
            except IndexError:
                print "No laser pulse session for this cell"
                testStatistic = None
                pVal = None
            else:
                testStatistic, pVal = funcs.laser_response(laserEphysData)
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
                testStatistic, pVal = funcs.laser_response(laserTrainEphysData)
            laserTrainTestStatistic[indRow] = testStatistic
            laserTrainPVal[indRow] = pVal
            
            # --- Determine sound responsiveness during bandwidth sessions ---
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
            else:
                bandEventOnsetTimes = funcs.get_sound_onset_times(bandEphysData, 'bandwidth')
                bandSpikeTimestamps = bandEphysData['spikeTimes']
                bandEachTrial = bandBehavData['currentBand']
                secondSort = bandBehavData['currentAmp']
                numBands = np.unique(bandEachTrial)
                numSec = np.unique(secondSort)
                
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
        
    if indices:
        bestCells = db.query("isiViolations<0.02 and spikeShapeQuality>2.5")
        bestCells = bestCells.loc[bestCells['soundResponsePVal']<0.05]
        bestCells = bestCells.loc[bestCells['tuningFitR2']>R2CUTOFF]
        bestCells = bestCells.loc[bestCells['octavesFromPrefFreq']<OCTAVESCUTOFF]
        
        for dbIndex, dbRow in bestCells.iterrows():
            
            cell = ephyscore.Cell(dbRow) #, useModifiedClusters=True)
            
            bandEphysData, bandBehavData = cell.load_by_index(int(dbRow['bestBandSession']))
            bandEventOnsetTimes = funcs.get_sound_onset_times(bandEphysData, 'bandwidth')
            bandSpikeTimestamps = bandEphysData['spikeTimes']
            
            bandEachTrial = bandBehavData['currentBand']
            secondSort = bandBehavData['currentAmp']
            
            propOnset, propSustained = funcs.onset_sustained_spike_proportion(bandSpikeTimestamps, bandEventOnsetTimes)
            
            db.at[dbIndex, 'proportionSpikesOnset'] = propOnset
            db.at[dbIndex, 'proportionSpikesSustained'] = propSustained
            
            onsetTuningDict = funcs.calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange=[0.0,0.05])
            sustainedTuningDict = funcs.calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange=[0.2,1.0])        
    
            onsetStats = funcs.bandwidth_suppression_from_peak(onsetTuningDict)
            db.at[dbIndex, 'onsetSuppressionIndex'] = onsetStats['suppressionIndex'][-1]
            db.at[dbIndex, 'onsetSuppressionpVal'] = onsetStats['suppressionpVal'][-1]
            db.at[dbIndex, 'onsetFacilitationIndex'] = onsetStats['facilitationIndex'][-1]
            db.at[dbIndex, 'onsetFacilitationpVal'] = onsetStats['facilitationpVal'][-1]
            
            sustainedStats = funcs.bandwidth_suppression_from_peak(sustainedTuningDict)
            db.at[dbIndex, 'sustainedSuppressionIndex'] = sustainedStats['suppressionIndex'][-1]
            db.at[dbIndex, 'sustainedSuppressionpVal'] = sustainedStats['suppressionpVal'][-1]
            db.at[dbIndex, 'sustainedFacilitationIndex'] = sustainedStats['facilitationIndex'][-1]
            db.at[dbIndex, 'sustainedFacilitationpVal'] = sustainedStats['facilitationpVal'][-1]
            
    dbFilename = os.path.join(settings.DATABASE_PATH,filename)
    celldatabase.save_hdf(db, dbFilename)


