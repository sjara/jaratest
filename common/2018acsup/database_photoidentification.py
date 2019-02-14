'''
This script contains a function that computes new columns for a database of photoidentified cells.
'''

import os
import pandas as pd
import numpy as np
import time

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

R2CUTOFF = 0.1
OCTAVESCUTOFF = 0.3


def photoIDdatabase(db, clusterRescue=False, baseStats = False, computeIndices = True, filename = 'photoidentification_cells.h5'):
    '''
    This function takes as argument a pandas DataFrame and adds new columns.
    If you need to pass a path to a database instead, uncomment first three lines in photoIDdatabase to allow the function to take a path as an argument.
    
    Columns added are split into two groups: the basic stats computed for every cluster, and the more complex
    ones computed only for cells that pass certain criteria based on these basic stats and additional criteria based on cell quality.
    
    Either can be chosen to be run, the final database is saved regardless.
    
    A name for the saved database can be passed if you want a database different from the default.
    If you don't want to save the database, you can pass an empty filename.
    '''
#     if type(db) == str:
#         dbPath = os.path.join(settings.DATABASE_PATH,db)
#         db = celldatabase.load_hdf(dbPath)
    
    if clusterRescue:
        from sklearn import neighbors
        cellsToRescue = db.query('isiViolations>0.02')
        for indRow, dbRow in cellsToRescue.iterrows():
            cell = ephyscore.Cell(dbRow)
            print dbRow['subject'], dbRow['date'], dbRow['depth']
            timestamps, samples, recordingNumber = cell.load_all_spikedata()
            tetrode = dbRow['tetrode']
            cluster = dbRow['cluster']

            isiViolations = spikesorting.calculate_ISI_violations(timestamps)
            print "isi violations: %{}".format(isiViolations*100)
            print "nSpikes: {}".format(len(timestamps))
            if len(timestamps)!=0:
                featuresMat = spikesorting.calculate_features(samples, ['peakFirstHalf', 'valleyFirstHalf', 'energy'])
            
                #To sort by nearest-neighbor distance
                print "Calculating NN distance"
                tic = time.time()
                #This will use all the processors
                nbrs = neighbors.NearestNeighbors(n_neighbors=2, algorithm='auto', n_jobs=-1).fit(featuresMat)
                distances, indices = nbrs.kneighbors(featuresMat)
                toc = time.time()
                elapsed = toc-tic
                print "NN done, elapsed time: {}".format(elapsed/60.)
                sortArray = np.argsort(distances[:,1]) #Take second neighbor distance because first is self (0)
            
                #To sort by mahalanobis distance to the cluster centroid
                # centroid = featuresMat.mean(axis=0)
            
                spikesToRemove = 0
                thisISIviolation = isiViolations #The isi violations including all the spikes
                jumpBy = int(len(timestamps)*0.01) #Jump by 1% of spikes each time
                if jumpBy == 0:
                    jumpBy = 1 #remove at least 1 spike
                while thisISIviolation>0.02:
                    spikesToRemove+=jumpBy
                    #We start to throw spikes at the end of the sort array away
                    includeBool = sortArray < (len(sortArray)-spikesToRemove)
                    # timestampsToInclude = sortedTimestamps[:-1*spikesToRemove]
                    timestampsToInclude = timestamps[includeBool]
                    thisISIviolation = spikesorting.calculate_ISI_violations(np.sort(timestampsToInclude))
                    print "Removing {} spikes, ISI violations: {}".format(spikesToRemove, thisISIviolation)
                print "Final included spikes: {} out of {}".format(len(timestampsToInclude), len(timestamps))
            
                #The inds of all the spikes that get to stay (have to have a low number in sort array)
                #Sort array is in chronological order, so this include bool array is also chronological
                # includeBool = sortArray < (len(sortArray)-spikesToRemove)
            
                try:
                    for thisRecordingNum in np.unique(recordingNumber):
                        #Which spikes in the total come from this recording
                        indsThisRecording = np.flatnonzero(recordingNumber == thisRecordingNum)
                        #What are the values in includeBool for those inds?
                        includeThisRecording = includeBool[indsThisRecording]
                
                        #load the .clu file
                        #Need the recording info
                        subject = cell.dbRow['subject']
                        date = cell.dbRow['date']
                        ephysTimeThisRecording = cell.dbRow['ephysTime'][thisRecordingNum]
                        clusterDir = "{}_kk".format("_".join([date, ephysTimeThisRecording]))
                        clusterFullPath = os.path.join(settings.EPHYS_PATH, subject, clusterDir)
                        clusterFile = os.path.join(clusterFullPath,'Tetrode{}.clu.1'.format(tetrode))
                
                        allClustersThisTetrode = np.fromfile(clusterFile,dtype='int32',sep=' ')[1:]
                
                        nClusters = len(np.unique(allClustersThisTetrode))
                
                        #The inds of the spikes from the cluster we are working on
                        indsThisCluster = np.flatnonzero(allClustersThisTetrode == cluster)
                
                        #For each spike from this cluster we have a bool value to include it or not
                        assert len(indsThisCluster) == len(includeThisRecording)
                
                        #For every spike in the cluster, we determine whether to keep or remove
                        for indIter, indThisSpike in enumerate(indsThisCluster):
                            includeThisSpike = includeThisRecording[indIter]
                            if includeThisSpike == 0: #If we remove, just set the value in allClustersThisTetrode to 0
                                allClustersThisTetrode[indThisSpike] = 0
                
                        #Then just re-save the allClustersThisTetrode as a modified clu file
                        modifiedClusterFile = os.path.join(clusterFullPath,'Tetrode{}.clu.modified'.format(tetrode))
                
                        # FIXME: Make sure that adding cluster 0 does not mess up creating databases or
                        #        other processes where we need to read the clu file
                        fid = open(modifiedClusterFile,'w')
                        #We added a new garbage cluster (0)
                        fid.write('{0}\n'.format(nClusters+1))
                        print "Writing .clu.modified file for session {}".format(ephysTimeThisRecording)
                        for cn in allClustersThisTetrode:
                            fid.write('{0}\n'.format(cn))
                        fid.close()
                    
                        #Save the new ISI violation
                        db.loc[indRow, 'modifiedISI'] = thisISIviolation
                    
                except:
                    print "Could not save modified .clu files"
    
    if baseStats:
        soundLoc = []
        
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
        
    if computeIndices:
        bestCells = db.query("isiViolations<0.02 or modifiedISI<0.02")
        bestCells = bestCells.loc[bestCells['spikeShapeQuality']>2]
        bestCells = bestCells.query('soundResponsePVal<0.05 or onsetSoundResponsePVal<0.05 or sustainedSoundResponsePVal<0.05')
        bestCells = bestCells.loc[bestCells['tuningFitR2']>R2CUTOFF]
        bestCells = bestCells.loc[bestCells['octavesFromPrefFreq']<OCTAVESCUTOFF]
        
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
            
            #also calculating fits and suppression with nothing being fit for bw 0
            noZeroSustainedResponse = sustainedResponse[1:]
            bandsForFitNoZero = bandsForFit[1:]
            
            noZeroFitParams, noZeroR2 = fitfuncs.diff_of_gauss_fit(bandsForFitNoZero, noZeroSustainedResponse, mFixed=mFixed)
            
            #fit params
            db.at[dbIndex, 'R0noZero'] = noZeroFitParams[0]
            db.at[dbIndex, 'RDnoZero'] = noZeroFitParams[3]
            db.at[dbIndex, 'RSnoZero'] = noZeroFitParams[4]
            db.at[dbIndex, 'mnoZero'] = mFixed
            db.at[dbIndex, 'sigmaDnoZero'] = noZeroFitParams[1]
            db.at[dbIndex, 'sigmaSnoZero'] = noZeroFitParams[2]
            db.at[dbIndex, 'bandwidthTuningR2noZero'] = noZeroR2
            
            allFitParamsNoZero = [mFixed]
            allFitParamsNoZero.extend(noZeroFitParams)
            testBandsNoZero = np.linspace(bandsForFitNoZero[0],bandsForFitNoZero[-1],500)
            suppIndNoZero, prefBWNoZero = fitfuncs.extract_stats_from_fit(allFitParamsNoZero, testBandsNoZero)
            
            db.at[dbIndex, 'fitSustainedSuppressionIndexnoZero'] = suppIndNoZero
            db.at[dbIndex, 'fitSustainedPrefBandwidthnoZero'] = prefBWNoZero
            
    if len(filename)!=0:        
        celldatabase.save_hdf(db, filename)
        print filename + " saved"
    
    return db


