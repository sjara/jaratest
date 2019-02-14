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
OCTAVESCUTOFF = 0.5



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
            
            # --- Determine sound responsiveness during bandwidth sessions and calculate baseline firing rates with and without laser---
            #done in a kind of stupid way because regular and control sessions are handled the same way
            if any(session in dbRow['sessionType'] for session in ['laserBandwidth', 'laserBandwidthControl']):
                if 'laserBandwidth' in dbRow['sessionType']:
                    bandEphysData, bandBehavData = cellObj.load('laserBandwidth')
                    behavSession = 'laserBandwidth'
                    db.at[dbIndex, 'controlSession'] = 0
                elif 'laserBandwidthControl' in dbRow['sessionType']:
                    bandEphysData, bandBehavData = cellObj.load('laserBandwidthControl')
                    behavSession = 'laserBandwidthControl'
                    db.at[dbIndex, 'controlSession'] = 1
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
                
                #find baselines with and without laser
                baselineRange = [-0.05, 0.0]
                baselineRates, baselineSEMs = funcs.inactivated_cells_baselines(bandSpikeTimestamps, bandEventOnsetTimes, secondSort, baselineRange)
                db.at[dbIndex, 'baselineFRnoLaser'] = baselineRates[0]
                db.at[dbIndex, 'baselineFRLaser'] = baselineRates[1]
                db.at[dbIndex, 'baselineFRnoLaserSEM'] = baselineSEMs[0]
                db.at[dbIndex, 'baselineFRLaserSEM'] = baselineSEMs[1]
                db.at[dbIndex, 'baselineChangeFR'] = baselineRates[1] - baselineRates[0]
            else:
                print "No bandwidth session for this cell"
                testStatistic = np.nan
                pVal = np.nan
                onsetTestStatistic = np.nan
                onsetpVal = np.nan
                sustainedTestStatistic = np.nan
                sustainedpVal = np.nan
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
                    bandIndex, octavesFromBest = funcs.best_index(cellObj, bestFreq, behavSession)
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
            bandEventOnsetTimes = funcs.get_sound_onset_times(bandEphysData, 'bandwidth')
            bandSpikeTimestamps = bandEphysData['spikeTimes']
            
            bandEachTrial = bandBehavData['currentBand']
            secondSort = bandBehavData['laserTrial']
            
            propOnset, propSustained = funcs.onset_sustained_spike_proportion(bandSpikeTimestamps, bandEventOnsetTimes)
            
            db.at[dbIndex, 'proportionSpikesOnset'] = propOnset
            db.at[dbIndex, 'proportionSpikesSustained'] = propSustained
            
            #by default: not subtracting baseline, but are replacing pure tone response with baseline for 0 bw condition
            onsetSupInds, onsetSupIndpVals, onsetFacInds, onsetFacIndpVals, onsetPeakInds, onsetSpikeArray = funcs.bandwidth_suppression_from_peak(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange=[0.0,0.05], baseRange=[-0.05,0.0])
            db.at[dbIndex, 'onsetSuppressionIndexLaser'] = onsetSupInds[-1]
            db.at[dbIndex, 'onsetSuppressionpValLaser'] = onsetSupIndpVals[-1]
            db.at[dbIndex, 'onsetFacilitationIndexLaser'] = onsetFacInds[-1]
            db.at[dbIndex, 'onsetFacilitationpValLaser'] = onsetFacIndpVals[-1]
            db.at[dbIndex, 'onsetPrefBandwidthLaser'] = bandEachTrial[onsetPeakInds[-1]]
             
            db.at[dbIndex, 'onsetSuppressionIndexNoLaser'] = onsetSupInds[0]
            db.at[dbIndex, 'onsetSuppressionpValNoLaser'] = onsetSupIndpVals[0]
            db.at[dbIndex, 'onsetFacilitationIndexNoLaser'] = onsetFacInds[0]
            db.at[dbIndex, 'onsetFacilitationpValNoLaser'] = onsetFacIndpVals[0]
            db.at[dbIndex, 'onsetPrefBandwidthNoLaser'] = bandEachTrial[onsetPeakInds[0]]
             
            #base range is right before sound onset so we get estimate for laser baseline
            sustainedSupInds, sustainedSupIndpVals, sustainedFacInds, sustainedFacIndpVals, sustainedPeakInds, sustainedSpikeArray = funcs.bandwidth_suppression_from_peak(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange=[0.2,1.0], baseRange=[-0.05,0.0])
            db.at[dbIndex, 'sustainedSuppressionIndexLaser'] = sustainedSupInds[-1]
            db.at[dbIndex, 'sustainedSuppressionpValLaser'] = sustainedSupIndpVals[-1]
            db.at[dbIndex, 'sustainedFacilitationIndexLaser'] = sustainedFacInds[-1]
            db.at[dbIndex, 'sustainedFacilitationpValLaser'] = sustainedFacIndpVals[-1]
            db.at[dbIndex, 'sustainedPrefBandwidthLaser'] = bandEachTrial[sustainedPeakInds[-1]]
             
            db.at[dbIndex, 'sustainedSuppressionIndexNoLaser'] = sustainedSupInds[0]
            db.at[dbIndex, 'sustainedSuppressionpValNoLaser'] = sustainedSupIndpVals[0]
            db.at[dbIndex, 'sustainedFacilitationIndexNoLaser'] = sustainedFacInds[0]
            db.at[dbIndex, 'sustainedFacilitationpValNoLaser'] = sustainedFacIndpVals[0]
            db.at[dbIndex, 'sustainedPrefBandwidthNoLaser'] = bandEachTrial[sustainedPeakInds[0]]
            
            #no laser fit
            sustainedResponseNoLaser = sustainedSpikeArray[:,0]

            bandsForFit = np.unique(bandEachTrial)
            bandsForFit[-1] = 6
            mFixed = 1
            
            fitParams, R2 = fitfuncs.diff_of_gauss_fit(bandsForFit, sustainedResponseNoLaser, mFixed=mFixed)
            
            #fit params
            db.at[dbIndex, 'R0noLaser'] = fitParams[0]
            db.at[dbIndex, 'RDnoLaser'] = fitParams[3]
            db.at[dbIndex, 'RSnoLaser'] = fitParams[4]
            db.at[dbIndex, 'mnoLaser'] = mFixed
            db.at[dbIndex, 'sigmaDnoLaser'] = fitParams[1]
            db.at[dbIndex, 'sigmaSnoLaser'] = fitParams[2]
            db.at[dbIndex, 'bandwidthTuningR2noLaser'] = R2
            
            testBands = np.linspace(bandsForFit[0],bandsForFit[-1],500)
            allFitParams = [mFixed]
            allFitParams.extend(fitParams)
            suppInd, prefBW = fitfuncs.extract_stats_from_fit(allFitParams, testBands)
            
            db.at[dbIndex, 'fitSustainedSuppressionIndexNoLaser'] = suppInd
            db.at[dbIndex, 'fitSustainedPrefBandwidthNoLaser'] = prefBW
            
            #laser fit
            sustainedResponseLaser = sustainedSpikeArray[:,1]
            
            fitParamsLaser, R2Laser = fitfuncs.diff_of_gauss_fit(bandsForFit, sustainedResponseLaser, mFixed=mFixed)
            
            #fit params
            db.at[dbIndex, 'R0laser'] = fitParamsLaser[0]
            db.at[dbIndex, 'RDlaser'] = fitParamsLaser[3]
            db.at[dbIndex, 'RSlaser'] = fitParamsLaser[4]
            db.at[dbIndex, 'mlaser'] = mFixed
            db.at[dbIndex, 'sigmaDlaser'] = fitParamsLaser[1]
            db.at[dbIndex, 'sigmaSlaser'] = fitParamsLaser[2]
            db.at[dbIndex, 'bandwidthTuningR2laser'] = R2Laser
            
            allFitParamsLaser = [mFixed]
            allFitParamsLaser.extend(fitParamsLaser)
            suppIndLaser, prefBWLaser = fitfuncs.extract_stats_from_fit(allFitParamsLaser, testBands)
            
            db.at[dbIndex, 'fitSustainedSuppressionIndexLaser'] = suppIndLaser
            db.at[dbIndex, 'fitSustainedPrefBandwidthLaser'] = prefBWLaser
            
            meanLaserDiff = np.mean(sustainedResponseLaser-sustainedResponseNoLaser)
            db.at[dbIndex, 'laserChangeResponse'] = meanLaserDiff
            
            laserDiff = sustainedResponseLaser-sustainedResponseNoLaser
            peakInd = np.argmax(sustainedResponseNoLaser)
            
            db.at[dbIndex, 'peakChangeFR'] = laserDiff[peakInd]
            db.at[dbIndex, 'WNChangeFR'] = laserDiff[-1]
            
            testRespsNoLaser = fitfuncs.diff_gauss_form(testBands, *allFitParams)
            testRespsLaser = fitfuncs.diff_gauss_form(testBands, *allFitParamsLaser)
    
            laserDiffModel = testRespsLaser-testRespsNoLaser
            peakIndModel = np.argmax(testRespsNoLaser)
            
            db.at[dbIndex, 'fitPeakChangeFR'] = laserDiffModel[peakIndModel]
            db.at[dbIndex, 'fitWNChangeFR'] = laserDiffModel[-1]
            
            #also calculating fits and suppression with pure tone being 0 bw condition
            toneSustainedSupInds, toneSustainedSupIndpVals, toneSustainedFacInds, toneSustainedFacIndpVals, toneSustainedPeakInds, toneSustainedSpikeArray = funcs.bandwidth_suppression_from_peak(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange=[0.2,1.0], baseRange=[-0.05,0.0], zeroBWBaseline=False)
            db.at[dbIndex, 'sustainedSuppressionIndexNoLaserPureTone'] = toneSustainedSupInds[0]
            db.at[dbIndex, 'sustainedSuppressionpValNoLaserPureTone'] = toneSustainedSupIndpVals[0]
            db.at[dbIndex, 'sustainedFacilitationIndexNoLaserPureTone'] = toneSustainedFacInds[0]
            db.at[dbIndex, 'sustainedFacilitationpValNoLaserPureTone'] = toneSustainedFacIndpVals[0]
            db.at[dbIndex, 'sustainedPrefBandwidthNoLaserPureTone'] = bandEachTrial[toneSustainedPeakInds[0]]
            
            db.at[dbIndex, 'sustainedSuppressionIndexLaserPureTone'] = toneSustainedSupInds[-1]
            db.at[dbIndex, 'sustainedSuppressionpValLaserPureTone'] = toneSustainedSupIndpVals[-1]
            db.at[dbIndex, 'sustainedFacilitationIndexLaserPureTone'] = toneSustainedFacInds[-1]
            db.at[dbIndex, 'sustainedFacilitationpValLaserPureTone'] = toneSustainedFacIndpVals[-1]
            db.at[dbIndex, 'sustainedPrefBandwidthLaserPureTone'] = bandEachTrial[toneSustainedPeakInds[-1]]
            
            toneSustainedResponseNoLaser = toneSustainedSpikeArray[:,0]
            
            toneFitParamsNoLaser, toneR2 = fitfuncs.diff_of_gauss_fit(bandsForFit, toneSustainedResponseNoLaser, mFixed=mFixed)
            
            #fit params
            db.at[dbIndex, 'R0PureToneNoLaser'] = toneFitParamsNoLaser[0]
            db.at[dbIndex, 'RDPureToneNoLaser'] = toneFitParamsNoLaser[3]
            db.at[dbIndex, 'RSPureToneNoLaser'] = toneFitParamsNoLaser[4]
            db.at[dbIndex, 'mPureToneNoLaser'] = mFixed
            db.at[dbIndex, 'sigmaDPureToneNoLaser'] = toneFitParamsNoLaser[1]
            db.at[dbIndex, 'sigmaSPureToneNoLaser'] = toneFitParamsNoLaser[2]
            db.at[dbIndex, 'bandwidthTuningR2PureToneNoLaser'] = toneR2
            
            allFitParamsToneNoLaser = [mFixed]
            allFitParamsToneNoLaser.extend(toneFitParamsNoLaser)
            suppIndTone, prefBWTone = fitfuncs.extract_stats_from_fit(allFitParamsToneNoLaser, testBands)
            
            db.at[dbIndex, 'fitSustainedSuppressionIndexPureToneNoLaser'] = suppIndTone
            db.at[dbIndex, 'fitSustainedPrefBandwidthPureToneNoLaser'] = prefBWTone
            
            
            toneSustainedResponseLaser = toneSustainedSpikeArray[:,1]
            
            toneFitParamsLaser, toneR2Laser = fitfuncs.diff_of_gauss_fit(bandsForFit, toneSustainedResponseLaser, mFixed=mFixed)
            
            #fit params
            db.at[dbIndex, 'R0PureToneLaser'] = toneFitParamsLaser[0]
            db.at[dbIndex, 'RDPureToneLaser'] = toneFitParamsLaser[3]
            db.at[dbIndex, 'RSPureToneLaser'] = toneFitParamsLaser[4]
            db.at[dbIndex, 'mPureToneLaser'] = mFixed
            db.at[dbIndex, 'sigmaDPureToneLaser'] = toneFitParamsLaser[1]
            db.at[dbIndex, 'sigmaSPureToneLaser'] = toneFitParamsLaser[2]
            db.at[dbIndex, 'bandwidthTuningR2PureToneLaser'] = toneR2Laser
            
            allFitParamsToneLaser = [mFixed]
            allFitParamsToneLaser.extend(toneFitParamsLaser)
            suppIndToneLaser, prefBWToneLaser = fitfuncs.extract_stats_from_fit(allFitParamsToneLaser, testBands)
            
            db.at[dbIndex, 'fitSustainedSuppressionIndexPureToneLaser'] = suppIndToneLaser
            db.at[dbIndex, 'fitSustainedPrefBandwidthPureToneLaser'] = prefBWToneLaser
            
            testRespsNoLaser = fitfuncs.diff_gauss_form(testBands, *allFitParamsToneNoLaser)
            testRespsLaser = fitfuncs.diff_gauss_form(testBands, *allFitParamsToneLaser)
    
            laserDiffModel = testRespsLaser-testRespsNoLaser
            peakIndModel = np.argmax(testRespsNoLaser)
            
            db.at[dbIndex, 'fitPeakChangeFRPureTone'] = laserDiffModel[peakIndModel]
            db.at[dbIndex, 'fitWNChangeFRPureTone'] = laserDiffModel[-1]
            
            #also calculating fits and suppression with nothing being fit for bw 0
            noZeroSustainedResponseNoLaser = sustainedSpikeArray[1:,0]
            bandsForFitNoZero = bandsForFit[1:]
            
            noZeroFitParamsNoLaser, noZeroR2 = fitfuncs.diff_of_gauss_fit(bandsForFitNoZero, noZeroSustainedResponseNoLaser, mFixed=mFixed)
            
            #fit params
            db.at[dbIndex, 'R0noZeroNoLaser'] = noZeroFitParamsNoLaser[0]
            db.at[dbIndex, 'RDnoZeroNoLaser'] = noZeroFitParamsNoLaser[3]
            db.at[dbIndex, 'RSnoZeroNoLaser'] = noZeroFitParamsNoLaser[4]
            db.at[dbIndex, 'mnoZeroNoLaser'] = mFixed
            db.at[dbIndex, 'sigmaDnoZeroNoLaser'] = noZeroFitParamsNoLaser[1]
            db.at[dbIndex, 'sigmaSnoZeroNoLaser'] = noZeroFitParamsNoLaser[2]
            db.at[dbIndex, 'bandwidthTuningR2noZeroNoLaser'] = noZeroR2
            
            allFitParamsNoZero = [mFixed]
            allFitParamsNoZero.extend(noZeroFitParamsNoLaser)
            testBandsNoZero = np.linspace(bandsForFitNoZero[0],bandsForFitNoZero[-1],500)
            suppIndNoZero, prefBWNoZero = fitfuncs.extract_stats_from_fit(allFitParamsNoZero, testBandsNoZero)
            
            db.at[dbIndex, 'fitSustainedSuppressionIndexNoZeroNoLaser'] = suppIndNoZero
            db.at[dbIndex, 'fitSustainedPrefBandwidthNoZeroNoLaser'] = prefBWNoZero
            
            noZeroSustainedResponseLaser = sustainedSpikeArray[1:,1]
            bandsForFitNoZero = bandsForFit[1:]
            
            noZeroFitParamsLaser, noZeroR2Laser = fitfuncs.diff_of_gauss_fit(bandsForFitNoZero, noZeroSustainedResponseLaser, mFixed=mFixed)
            
            #fit params
            db.at[dbIndex, 'R0noZeroLaser'] = noZeroFitParamsLaser[0]
            db.at[dbIndex, 'RDnoZeroLaser'] = noZeroFitParamsLaser[3]
            db.at[dbIndex, 'RSnoZeroLaser'] = noZeroFitParamsLaser[4]
            db.at[dbIndex, 'mnoZeroLaser'] = mFixed
            db.at[dbIndex, 'sigmaDnoZeroLaser'] = noZeroFitParamsLaser[1]
            db.at[dbIndex, 'sigmaSnoZeroLaser'] = noZeroFitParamsLaser[2]
            db.at[dbIndex, 'bandwidthTuningR2noZeroLaser'] = noZeroR2Laser
            
            allFitParamsNoZeroLaser = [mFixed]
            allFitParamsNoZeroLaser.extend(noZeroFitParamsLaser)
            suppIndNoZeroLaser, prefBWNoZeroLaser = fitfuncs.extract_stats_from_fit(allFitParamsNoZeroLaser, testBandsNoZero)
            
            db.at[dbIndex, 'fitSustainedSuppressionIndexNoZeroLaser'] = suppIndNoZeroLaser
            db.at[dbIndex, 'fitSustainedPrefBandwidthNoZeroLaser'] = prefBWNoZeroLaser
            
            testRespsNoLaser = fitfuncs.diff_gauss_form(testBandsNoZero, *allFitParamsNoZero)
            testRespsLaser = fitfuncs.diff_gauss_form(testBandsNoZero, *allFitParamsNoZeroLaser)
    
            laserDiffModel = testRespsLaser-testRespsNoLaser
            peakIndModel = np.argmax(testRespsNoLaser)
            
            db.at[dbIndex, 'fitPeakChangeFRNoZero'] = laserDiffModel[peakIndModel]
            db.at[dbIndex, 'fitWNChangeFRNoZero'] = laserDiffModel[-1]
    
    if len(filename)!=0:        
        celldatabase.save_hdf(db, filename)
        print filename + " saved"
        
    return db


