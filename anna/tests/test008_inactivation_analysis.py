''' THIS IS TO TEST Spearman coefficient and other methods of analysing inactivation data'''
import sys
import os
import pandas as pd
import numpy as np


from jaratoolbox import celldatabase
reload(celldatabase)
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

from scipy import stats

import subjects_info


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
                  'trialsEachCond':trialsEachCond,
                  'timeRange':timeRange}
    return tuningDict

def change_FR_by_bins(tuningDict, lowBandInds=[0,1,2], highBandInds=[4,5,6], timeRange=[0.2,1.0]):
    import pdb
    spikeCountMat = tuningDict['spikeCountMat']
    
    diffs = np.zeros(2)
    soundDuration = timeRange[1]-timeRange[0]
    
    lowBandCounts = []
    lowBandLaserCounts = []
    
    for ind in lowBandInds:
        trialsThisBand = tuningDict['trialsEachCond'][:,ind,:]
        thisBandCounts = spikeCountMat[trialsThisBand[:,0]].flatten()
        thisBandLaserCounts = spikeCountMat[trialsThisBand[:,1]].flatten()
        
        lowBandCounts.extend(thisBandCounts)
        lowBandLaserCounts.extend(thisBandLaserCounts)
    
    diffs[0] = (np.mean(lowBandLaserCounts) - np.mean(lowBandCounts))/soundDuration
    
    highBandCounts = []
    highBandLaserCounts = []
    
    for ind in highBandInds:
        trialsThisBand = tuningDict['trialsEachCond'][:,ind,:]
        thisBandCounts = spikeCountMat[trialsThisBand[:,0]].flatten()
        thisBandLaserCounts = spikeCountMat[trialsThisBand[:,1]].flatten()
        
        highBandCounts.extend(thisBandCounts)
        highBandLaserCounts.extend(thisBandLaserCounts)
    
    diffs[1] = (np.mean(highBandLaserCounts) - np.mean(highBandCounts))/soundDuration
    pdb.set_trace()
    
    return diffs


dbFilename = os.path.join(settings.DATABASE_PATH,'inactivation_cells2.h5')
db = celldatabase.load_hdf(dbFilename)

bestCells = db[db['sustainedSuppressionIndexLaser'].notnull()]
noPV = bestCells.loc[bestCells['subject'].isin(subjects_info.PV_ARCHT_MICE)]
noSOM = bestCells.loc[bestCells['subject'].isin(subjects_info.SOM_ARCHT_MICE)]

PVspearman = np.zeros(len(noPV))
PVbinDiff = np.zeros((len(noPV),2))

#plt.figure()
for indRow, (dbIndex, dbRow) in enumerate(noPV.iterrows()):
    
    cell = ephyscore.Cell(dbRow) #, useModifiedClusters=True)
        
    bandEphysData, bandBehavData = cell.load_by_index(int(dbRow['bestBandSession']))
        
    bandEventOnsetTimes = bandEphysData['events']['soundDetectorOn']
    bandSpikeTimestamps = bandEphysData['spikeTimes']

    bandEachTrial = bandBehavData['currentBand']
    numBands = np.unique(bandEachTrial)

    secondSort = bandBehavData['laserTrial']

    sustainedTuningDict = calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange=[0.2,1.0])
    laserDiff = np.diff(sustainedTuningDict['responseArray'])
    binDiffs = change_FR_by_bins(sustainedTuningDict)
    #plt.plot(laserDiff)
    spearman = stats.spearmanr(laserDiff, numBands)
    PVspearman[indRow] = spearman[0]
    PVbinDiff[indRow,:] = binDiffs

SOMspearman = np.zeros(len(noSOM))
SOMbinDiff = np.zeros((len(noSOM),2))

#plt.figure()  
for indRow, (dbIndex, dbRow) in enumerate(noSOM.iterrows()):
    
    cell = ephyscore.Cell(dbRow) #, useModifiedClusters=True)
        
    bandEphysData, bandBehavData = cell.load_by_index(int(dbRow['bestBandSession']))
        
    bandEventOnsetTimes = bandEphysData['events']['soundDetectorOn']
    bandSpikeTimestamps = bandEphysData['spikeTimes']
        
    bandEachTrial = bandBehavData['currentBand']
    numBands = np.unique(bandEachTrial)

    secondSort = bandBehavData['laserTrial']

    sustainedTuningDict = calculate_tuning_curve_inputs(bandSpikeTimestamps, bandEventOnsetTimes, bandEachTrial, secondSort, timeRange=[0.2,1.0])
    laserDiff = np.diff(sustainedTuningDict['responseArray'])
    binDiffs = change_FR_by_bins(sustainedTuningDict)
    #plt.plot(laserDiff)
    spearman = stats.spearmanr(laserDiff, numBands)
    SOMspearman[indRow] = spearman[0]
    SOMbinDiff[indRow,:] = binDiffs
    
    