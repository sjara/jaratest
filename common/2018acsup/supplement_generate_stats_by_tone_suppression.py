''' 
Generates inputs to plot SIs of putative excitatory cells split into two groups: cells significantly suppressed by any pure tone, and cells not.

Inputs generated:
* SI for each cell
* p value for each cell denoting result of one-sided parametric test to determine if sound response is less than baseline
'''

import os
import pandas as pd
import numpy as np

from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

from scipy import stats

import studyparams

dbFilename = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 'photoidentification_cells.h5')
db = celldatabase.load_hdf(dbFilename)

figName = 'supplement_figure_gaussian_frequency_tuning_fit'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)

# -- find PV, SOM, and non-SOM cells that are tuned to frequency and with a good centre frequency selected and have sustained sound response
bestCells = db.query(studyparams.SINGLE_UNITS)
bestCells = bestCells.query(studyparams.GOOD_CELLS)

ExcCells = bestCells.query(studyparams.EXC_CELLS)

SIs = np.zeros(len(ExcCells))
pVals = np.zeros(len(ExcCells))

for indCell, (dbIndex, dbRow) in enumerate(ExcCells.iterrows()):
    
    cell = ephyscore.Cell(dbRow)
    
    tuningEphysData, tuningBData = cell.load('tuningCurve')
    tuningEventOnsetTimes = tuningEphysData['events']['soundDetectorOn']
    if len(tuningEventOnsetTimes)==0: #some cells recorded before sound detector installed
        tuningEventOnsetTimes = tuningEphysData['events']['stimOn'] + 0.0095 #correction for bandwidth trials, determined by comparing sound detector onset to stim event onset
    tuningEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(tuningEventOnsetTimes, minEventOnsetDiff=0.2)
    tuningSpikeTimestamps = tuningEphysData['spikeTimes']
     
    freqEachTrial = tuningBData['currentFreq']
    numFreqs = np.unique(freqEachTrial)
    intEachTrial = tuningBData['currentIntensity']
    timeRange = [-0.5,0.5]
     
    trialsEachCond = behavioranalysis.find_trials_each_combination(freqEachTrial,
                                                                    numFreqs,
                                                                    intEachTrial,
                                                                    np.unique(intEachTrial))
    trialsHighInt = trialsEachCond[:,:,-1] #only interested in loudest tones as they correspond to high amp bandwidth trials
     
    # --- computes spike counts for each trial ---
    tuningSpikeTimesFromEventOnset, trialIndexForEachSpike, tuningIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        tuningSpikeTimestamps, 
                                                                                                        tuningEventOnsetTimes,
                                                                                                        timeRange)
    tuningWindow = dbRow['tuningTimeRange']
    tuningSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(tuningSpikeTimesFromEventOnset, tuningIndexLimitsEachTrial, tuningWindow)
 
    tuningSpikeArray = np.zeros(len(numFreqs))
    for freq in range(len(numFreqs)):
        trialsThisFreq = trialsHighInt[:,freq]
        if tuningSpikeCountMat.shape[0] == len(trialsThisFreq)+1:
            tuningSpikeCountMat = tuningSpikeCountMat[:-1,:]
        spikeCountsThisFreq = tuningSpikeCountMat[trialsThisFreq].flatten()
        tuningSpikeArray[freq] = np.mean(spikeCountsThisFreq)/(tuningWindow[1]-tuningWindow[0])
         
    baselineTimeRange = [-tuningWindow[1],-tuningWindow[0]]
    baselineSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(tuningSpikeTimesFromEventOnset, tuningIndexLimitsEachTrial, baselineTimeRange)
    baselineSpikeRate = np.mean(baselineSpikeCountMat.flatten())/(baselineTimeRange[1]-baselineTimeRange[0])
   
    # --- determines if any response was significantly suppressed ---
        
    minpVal = np.inf
    maxzscore = -np.inf
    for freq in range(trialsHighInt.shape[1]):
        trialsThisCond = trialsHighInt[:,freq]
        if tuningSpikeCountMat.shape[0] == len(trialsThisCond)+1:
            tuningSpikeCountMat = tuningSpikeCountMat[:-1,:]
        if baselineSpikeCountMat.shape[0] == len(trialsThisCond)+1:
            baselineSpikeCountMat = baselineSpikeCountMat[:-1,:]
        if any(trialsThisCond):
            thisFirstStimCounts = tuningSpikeCountMat[trialsThisCond].flatten()
            thisStimBaseSpikeCounts = baselineSpikeCountMat[trialsThisCond].flatten()
            if all(thisFirstStimCounts==thisStimBaseSpikeCounts): #if counts are identical
                pValThisFirst = np.inf
            else:
                thiszscore, pValThisFirst = stats.mannwhitneyu(thisFirstStimCounts, thisStimBaseSpikeCounts, alternative='less')
            if pValThisFirst < minpVal:
                minpVal = pValThisFirst
                
    #minpVal = minpVal*len(numFreqs) #correction for multiple comparisons
    SIs[indCell] = dbRow['fitSustainedSuppressionIndexnoZero']
    pVals[indCell] = minpVal
    
# -- save data --
outputFile = 'pure_tone_suppression_stats.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         ExcCellSIs = SIs,
         toneSuppPVal = pVals)
print outputFile + " saved"