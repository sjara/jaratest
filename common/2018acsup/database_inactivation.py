'''
This script takes as argument a pandas DataFrame or a path to a saved database and adds new columns.

Columns added are split into two groups: the basic stats computed for every cluster, and the more complex
ones computed only for cells that pass certain criteria based on these basic stats.

Either can be chosen to be run, the final database is saved regardless.

A name for the saved database can be passed if you want a separate database for whatever reason.

TO DO:
- Split up into smaller functions for each computation to make flow more clear
'''

import pandas as pd
import numpy as np
import os

from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import database_generation_funcs as funcs
import database_bandwidth_tuning_fit_funcs as fitfuncs
reload(funcs)
reload(fitfuncs)

import pdb

R2CUTOFF = 0.1
OCTAVESCUTOFF = 0.3



def inactivation_database(db, baseStats = False, computeIndices = True, filename = 'inactivation_cells.h5'):
    if type(db) == str:
        dbPath = os.path.join(settings.DATABASE_PATH,db)
        db = celldatabase.load_hdf(dbPath)
        
    if baseStats:
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
            
            # --- Determine sound responsiveness during bandwidth sessions ---
            try:
                bandEphysData, bandBehavData = cellObj.load('laserBandwidth')
            except IndexError:
                print "No bandwidth session for this cell"
                testStatistic = np.nan
                pVal = np.nan
                onsetTestStatistic = np.nan
                onsetpVal = np.nan
                sustainedTestStatistic = np.nan
                sustainedpVal = np.nan
                #pdb.set_trace()
            else:
                bandEventOnsetTimes = funcs.get_sound_onset_times(bandEphysData, 'bandwidth')
                bandSpikeTimestamps = bandEphysData['spikeTimes']
                bandEachTrial = bandBehavData['currentBand']
                secondSort = bandBehavData['laserTrial']
                numBands = np.unique(bandEachTrial)
                numSec = np.unique(secondSort)
                
                trialsEachComb = behavioranalysis.find_trials_each_combination(bandEachTrial, numBands, secondSort, numSec)
                trialsEachBaseCond = trialsEachComb[:,:,0] #using no laser trials to determine sound responsiveness
                testStatistic, pVal = funcs.sound_response_any_stimulus(bandEventOnsetTimes, bandSpikeTimestamps, trialsEachBaseCond, [0.0, 1.0], [-1.2,-0.2])
                onsetTestStatistic, onsetpVal = funcs.sound_response_any_stimulus(bandEventOnsetTimes, bandSpikeTimestamps, trialsEachBaseCond, [0.0,0.05], [-0.25,0.2])
                sustainedTestStatistic, sustainedpVal = funcs.sound_response_any_stimulus(bandEventOnsetTimes, bandSpikeTimestamps, trialsEachBaseCond, [0.2,1.0], [-1.0,0.2])
                pVal *= len(numBands) #correction for multiple comparisons
                onsetpVal *= len(numBands)
                sustainedpVal *= len(numBands)
                #pdb.set_trace()
            
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
                tuningWindow = np.full(2, np.nan)
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
                tuningWindow = np.array(tuningWindow)
                spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, tuningWindow)
                tuningSpikeRates = (spikeCountMat[trialsHighInt].flatten())/(tuningWindow[1]-tuningWindow[0])
                freqsThisIntensity = freqEachTrial[trialsHighInt]
                freqFit, thisRsquared = funcs.gaussian_tuning_fit(np.log2(freqsThisIntensity), tuningSpikeRates)
                if freqFit is not None:
                    bestFreq = 2**freqFit[0]
                    bandIndex, octavesFromBest = funcs.best_index(cellObj, bestFreq, 'laserBandwidth')
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
        
    if computeIndices:
        bestCells = db.query("isiViolations<0.02")# or modifiedISI<0.02")
        bestCells = bestCells.loc[bestCells['spikeShapeQuality']>2]
        bestCells = bestCells.query('soundResponsePVal<0.05 or onsetSoundResponsePVal<0.05 or sustainedSoundResponsePVal<0.05')
        bestCells = bestCells.loc[bestCells['tuningFitR2']>R2CUTOFF]
        bestCells = bestCells.loc[bestCells['octavesFromPrefFreq']<OCTAVESCUTOFF]
        
        for dbIndex, dbRow in bestCells.iterrows():
            
            cell = ephyscore.Cell(dbRow)
            
            bandEphysData, bandBehavData = cell.load_by_index(int(dbRow['bestBandSession']))
            bandEventOnsetTimes = funcs.get_sound_onset_times(bandEphysData, 'laserBandwidth')
            bandSpikeTimestamps = bandEphysData['spikeTimes']
            
            bandEachTrial = bandBehavData['currentBand']
            secondSort = bandBehavData['laserTrial']
            
            propOnset, propSustained = funcs.onset_sustained_spike_proportion(bandSpikeTimestamps, bandEventOnsetTimes)
            
            db.at[dbIndex, 'proportionSpikesOnset'] = propOnset
            db.at[dbIndex, 'proportionSpikesSustained'] = propSustained
            
            onsetTuningDict = funcs.calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange=[0.0,0.05])
            sustainedTuningDict = funcs.calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange=[0.2,1.0])        
    
            onsetStats = funcs.bandwidth_suppression_from_peak(onsetTuningDict)
            db.at[dbIndex, 'onsetSuppressionIndexLaser'] = onsetStats['suppressionIndex'][-1]
            db.at[dbIndex, 'onsetSuppressionpValLaser'] = onsetStats['suppressionpVal'][-1]
            db.at[dbIndex, 'onsetFacilitationIndexLaser'] = onsetStats['facilitationIndex'][-1]
            db.at[dbIndex, 'onsetFacilitationpValLaser'] = onsetStats['facilitationpVal'][-1]
             
            db.at[dbIndex, 'onsetSuppressionIndexNoLaser'] = onsetStats['suppressionIndex'][0]
            db.at[dbIndex, 'onsetSuppressionpValNoLaser'] = onsetStats['suppressionpVal'][0]
            db.at[dbIndex, 'onsetFacilitationIndexNoLaser'] = onsetStats['facilitationIndex'][0]
            db.at[dbIndex, 'onsetFacilitationpValNoLaser'] = onsetStats['facilitationpVal'][0]
             
            sustainedStats = funcs.bandwidth_suppression_from_peak(sustainedTuningDict)
            db.at[dbIndex, 'sustainedSuppressionIndexLaser'] = sustainedStats['suppressionIndex'][-1]
            db.at[dbIndex, 'sustainedSuppressionpValLaser'] = sustainedStats['suppressionpVal'][-1]
            db.at[dbIndex, 'sustainedFacilitationIndexLaser'] = sustainedStats['facilitationIndex'][-1]
            db.at[dbIndex, 'sustainedFacilitationpValLaser'] = sustainedStats['facilitationpVal'][-1]
             
            db.at[dbIndex, 'sustainedSuppressionIndexNoLaser'] = sustainedStats['suppressionIndex'][0]
            db.at[dbIndex, 'sustainedSuppressionpValNoLaser'] = sustainedStats['suppressionpVal'][0]
            db.at[dbIndex, 'sustainedFacilitationIndexNoLaser'] = sustainedStats['facilitationIndex'][0]
            db.at[dbIndex, 'sustainedFacilitationpValNoLaser'] = sustainedStats['facilitationpVal'][0]
            
            #find baselines with and without laser
            baselineRange = [-0.05, 0.0]
            baselineRates, baselineSEMs = funcs.inactivated_cells_baselines(bandSpikeTimestamps, bandEventOnsetTimes, secondSort, baselineRange)
            db.at[dbIndex, 'baselineFRnoLaser'] = baselineRates[0]
            db.at[dbIndex, 'baselineFRLaser'] = baselineRates[1]
            db.at[dbIndex, 'baselineFRnoLaserSEM'] = baselineSEMs[0]
            db.at[dbIndex, 'baselineFRLaserSEM'] = baselineSEMs[1]
            
            #no laser fit
            sustainedResponseNoLaser = sustainedTuningDict['responseArray'][:,0]
            
            #replace pure tone with baseline
            sustainedResponseNoLaser[0] = baselineRates[0]
            bandsForFit = np.unique(bandEachTrial)
            bandsForFit[-1] = 6
            mFixed = 1
            
            fitParams, R2 = fitfuncs.diff_of_gauss_fit(bandsForFit, sustainedResponseNoLaser, mFixed=mFixed)
            print fitParams
            
            #fit params
            db.at[dbIndex, 'R0noLaser'] = fitParams[0]
            db.at[dbIndex, 'RDnoLaser'] = fitParams[3]
            db.at[dbIndex, 'RSnoLaser'] = fitParams[4]
            db.at[dbIndex, 'mnoLaser'] = mFixed
            db.at[dbIndex, 'sigmaDnoLaser'] = fitParams[1]
            db.at[dbIndex, 'sigmaSnoLaser'] = fitParams[2]
            db.at[dbIndex, 'bandwidthTuningR2noLaser'] = R2
            
            testBands = np.linspace(bandsForFit[0],bandsForFit[-1],50)
            allFitParams = [mFixed]
            allFitParams.extend(fitParams)
            suppInd, prefBW = fitfuncs.extract_stats_from_fit(allFitParams, testBands)
            
            db.at[dbIndex, 'fitSustainedSuppressionIndexNoLaser'] = suppInd
            db.at[dbIndex, 'fitSustainedPrefBandwidthNoLaser'] = prefBW
            
            #laser fit
            sustainedResponseLaser = sustainedTuningDict['responseArray'][:,1]
            
            #replace pure tone with baseline
            sustainedResponseLaser[0] = baselineRates[1]
            
            fitParams, R2 = fitfuncs.diff_of_gauss_fit(bandsForFit, sustainedResponseLaser, mFixed=mFixed)
            print fitParams
            
            #fit params
            db.at[dbIndex, 'R0laser'] = fitParams[0]
            db.at[dbIndex, 'RDlaser'] = fitParams[3]
            db.at[dbIndex, 'RSlaser'] = fitParams[4]
            db.at[dbIndex, 'mlaser'] = mFixed
            db.at[dbIndex, 'sigmaDlaser'] = fitParams[1]
            db.at[dbIndex, 'sigmaSlaser'] = fitParams[2]
            db.at[dbIndex, 'bandwidthTuningR2laser'] = R2
            
            testBands = np.linspace(bandsForFit[0],bandsForFit[-1],50)
            allFitParams = [mFixed]
            allFitParams.extend(fitParams)
            suppInd, prefBW = fitfuncs.extract_stats_from_fit(allFitParams, testBands)
            
            db.at[dbIndex, 'fitSustainedSuppressionIndexLaser'] = suppInd
            db.at[dbIndex, 'fitSustainedPrefBandwidthLaser'] = prefBW
            
    dbFilename = os.path.join(settings.DATABASE_PATH,filename)
    celldatabase.save_hdf(db, dbFilename)


