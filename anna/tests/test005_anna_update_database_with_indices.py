''' THIS IS TO TEST LOADING A FULL DATABASE AND COMPUTING INDICES'''
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

from scipy import stats

R2CUTOFF = 0.1
OCTAVESCUTOFF = 0.3

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

def calculate_tuning_curve_inputs(spikeTimeStamps, eventOnsetTimes, firstSort, secondSort, timeRange, baseRange=[-1.1,-0.1]):
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
    baselineError = stats.sem(baseSpikeCountMat)/(baseRange[1]-baseRange[0])
    
    for sec in range(len(numSec)):
        trialsThisSec = trialsEachCond[:,:,sec]
        for first in range(len(numFirst)):
            trialsThisFirst = trialsThisSec[:,first]
            if spikeCountMat.shape[0] != len(trialsThisFirst):
                spikeCountMat = spikeCountMat[:-1,:]
            if any(trialsThisFirst):
                thisFirstCounts = spikeCountMat[trialsThisFirst].flatten()
                spikeArray[first,sec] = np.mean(thisFirstCounts)/duration
                errorArray[first,sec] = stats.sem(thisFirstCounts)/duration
            else:
                spikeArray[first,sec] = np.nan
                errorArray[first,sec] = np.nan
    tuningDict = {'responseArray':spikeArray,
                  'errorArray':errorArray,
                  'baselineSpikeRate':baselineSpikeRate,
                  'baselineSpikeError':baselineError,
                  'spikeCountMat':spikeCountMat,
                  'trialsEachCond':trialsEachCond}
    return tuningDict

def bandwidth_suppression_from_peak(tuningDict, subtractBaseline=False):
    spikeArray = tuningDict['responseArray']
    baselineSpikeRate = tuningDict['baselineSpikeRate']
    spikeCountMat = tuningDict['spikeCountMat']
    
    suppressionIndex = np.zeros(spikeArray.shape[1])
    facilitationIndex = np.zeros_like(suppressionIndex)
    
    suppressionpVal = np.zeros_like(suppressionIndex)
    facilitationpVal = np.zeros_like(suppressionIndex)
            
    if not subtractBaseline:
        baselineSpikeRate = 0
    
    for ind in range(len(suppressionIndex)):    
        suppressionIndex[ind] = (max(spikeArray[:,ind])-spikeArray[:,ind][-1])/(max(spikeArray[:,ind])-baselineSpikeRate)
        facilitationIndex[ind] = (max(spikeArray[:,ind])-spikeArray[:,ind][0])/(max(spikeArray[:,ind])-baselineSpikeRate)

        trialsThisSeconsVal = tuningDict['trialsEachCond'][:,:,ind]
        peakInd = np.argmax(spikeArray[:,ind])
        
        peakSpikeCounts = spikeCountMat[trialsThisSeconsVal[:,peakInd]].flatten()
        whiteNoiseSpikeCounts = spikeCountMat[trialsThisSeconsVal[:,-1]].flatten()
        pureToneSpikeCounts = spikeCountMat[trialsThisSeconsVal[:,0]].flatten()
        
        suppressionpVal[ind] = stats.ranksums(peakSpikeCounts, whiteNoiseSpikeCounts)[1]
        facilitationpVal[ind] = stats.ranksums(peakSpikeCounts, pureToneSpikeCounts)[1]
        
    
    suppressionDict = {'suppressionIndex':suppressionIndex,
                       'suppressionpVal':suppressionpVal,
                       'facilitationIndex':facilitationIndex,
                       'facilitationpVal':facilitationpVal}
    
    return suppressionDict

def onset_sustained_spike_proportion(spikeTimeStamps, eventOnsetTimes, onsetTimeRange=[0.0,0.05], sustainedTimeRange=[0.2,1.0]):
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

if __name__=='__main__':
    if len(sys.argv[1:]):
        if sys.argv[1] == 'archt':
            dbFilename = os.path.join(settings.DATABASE_PATH,'inactivation_cells.h5')
            db = celldatabase.load_hdf(dbFilename)
            subType = 'archt'
        elif sys.argv[1] == 'chr2':
            dbFilename = os.path.join(settings.DATABASE_PATH,'photoidentification_cells.h5')
            db = celldatabase.load_hdf(dbFilename)
            subType = 'chr2'
    else:
        sys.exit("Please input database to process:\n\"archt\" for inactivation experiments\n\"chr2\" for photoidentification experiments")
    
    bestCells = db.query("isiViolations<0.02 and spikeShapeQuality>2.5")
    bestCells = bestCells.loc[bestCells['soundResponsePVal']<0.05]
    bestCells = bestCells.loc[bestCells['tuningFitR2']>R2CUTOFF]
    bestCells = bestCells.loc[bestCells['octavesFromPrefFreq']<OCTAVESCUTOFF]
    
    for dbIndex, dbRow in bestCells.iterrows():
        
        cell = ephyscore.Cell(dbRow) #, useModifiedClusters=True)
        
        bandEphysData, bandBehavData = cell.load_by_index(int(dbRow['bestBandSession']))
        if subType == 'archt':
            sessionType = 'laserBandwidth'
        elif subType == 'chr2':
            sessionType = 'bandwidth'
        
        bandEventOnsetTimes = get_sound_onset_times(bandEphysData, sessionType)
        bandSpikeTimestamps = bandEphysData['spikeTimes']
        
        bandEachTrial = bandBehavData['currentBand']
        if subType == 'archt':
            secondSort = bandBehavData['laserTrial']
        if subType == 'chr2':
            secondSort = bandBehavData['currentAmp']
        
        propOnset, propSustained = onset_sustained_spike_proportion(bandSpikeTimestamps, bandEventOnsetTimes)
        
        db.at[dbIndex, 'proportionSpikesOnset'] = propOnset
        db.at[dbIndex, 'proportionSpikesSustained'] = propSustained
        
        onsetTuningDict = calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange=[0.0,0.05])
        sustainedTuningDict = calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange=[0.2,1.0])        

        if subType == 'chr2':
            onsetStats = bandwidth_suppression_from_peak(onsetTuningDict)
            db.at[dbIndex, 'onsetSuppressionIndex'] = onsetStats['suppressionIndex'][-1]
            db.at[dbIndex, 'onsetSuppressionpVal'] = onsetStats['suppressionpVal'][-1]
            db.at[dbIndex, 'onsetFacilitationIndex'] = onsetStats['facilitationIndex'][-1]
            db.at[dbIndex, 'onsetFacilitationpVal'] = onsetStats['facilitationpVal'][-1]
            
            sustainedStats = bandwidth_suppression_from_peak(sustainedTuningDict)
            db.at[dbIndex, 'sustainedSuppressionIndex'] = sustainedStats['suppressionIndex'][-1]
            db.at[dbIndex, 'sustainedSuppressionpVal'] = sustainedStats['suppressionpVal'][-1]
            db.at[dbIndex, 'sustainedFacilitationIndex'] = sustainedStats['facilitationIndex'][-1]
            db.at[dbIndex, 'sustainedFacilitationpVal'] = sustainedStats['facilitationpVal'][-1]

        elif subType == 'archt':
            onsetStats = bandwidth_suppression_from_peak(onsetTuningDict)
            db.at[dbIndex, 'onsetSuppressionIndexLaser'] = onsetStats['suppressionIndex'][-1]
            db.at[dbIndex, 'onsetSuppressionpValLaser'] = onsetStats['suppressionpVal'][-1]
            db.at[dbIndex, 'onsetFacilitationIndexLaser'] = onsetStats['facilitationIndex'][-1]
            db.at[dbIndex, 'onsetFacilitationpValLaser'] = onsetStats['facilitationpVal'][-1]
             
            db.at[dbIndex, 'onsetSuppressionIndexNoLaser'] = onsetStats['suppressionIndex'][0]
            db.at[dbIndex, 'onsetSuppressionpValNoLaser'] = onsetStats['suppressionpVal'][0]
            db.at[dbIndex, 'onsetFacilitationIndexNoLaser'] = onsetStats['facilitationIndex'][0]
            db.at[dbIndex, 'onsetFacilitationpValNoLaser'] = onsetStats['facilitationpVal'][0]
             
            sustainedStats = bandwidth_suppression_from_peak(sustainedTuningDict)
            db.at[dbIndex, 'sustainedSuppressionIndexLaser'] = sustainedStats['suppressionIndex'][-1]
            db.at[dbIndex, 'sustainedSuppressionpValLaser'] = sustainedStats['suppressionpVal'][-1]
            db.at[dbIndex, 'sustainedFacilitationIndexLaser'] = sustainedStats['facilitationIndex'][-1]
            db.at[dbIndex, 'sustainedFacilitationpValLaser'] = sustainedStats['facilitationpVal'][-1]
             
            db.at[dbIndex, 'sustainedSuppressionIndexNoLaser'] = sustainedStats['suppressionIndex'][0]
            db.at[dbIndex, 'sustainedSuppressionpValNoLaser'] = sustainedStats['suppressionpVal'][0]
            db.at[dbIndex, 'sustainedFacilitationIndexNoLaser'] = sustainedStats['facilitationIndex'][0]
            db.at[dbIndex, 'sustainedFacilitationpValNoLaser'] = sustainedStats['facilitationpVal'][0]
    
    if subType == 'chr2':
        outputName = 'photoidentification_cells2.h5'
    elif subType == 'archt':
        outputName = 'inactivation_cells2.h5'
    dbFilename = os.path.join(settings.DATABASE_PATH,outputName)
    celldatabase.save_hdf(db, dbFilename)
    print('Saved database to: {}'.format(dbFilename))

