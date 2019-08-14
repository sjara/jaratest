''' 
Generates inputs to plot a raster and frequency tuning curve for example cells used to illustrate SS.
Inputs for each cell are saved as npz's

Can select which cells from the list to generate by index.
Not specifying which cells to generate will generate all of them.

To run:
run supplement_generate_example_frequency_tuning.py 0 2 (generate the first and third cell)
'''

import os
import sys
import pandas as pd
import numpy as np
from scipy import stats

from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import database_generation_funcs as funcs
import figparams

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'photoidentification_cells.h5')
dbase = celldatabase.load_hdf(dbPath)

figName = 'supplement_figure_gaussian_frequency_tuning_fit'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, figName)
#dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', figName)

# -- Example cells -- #
cellList = [{'subject' : 'band016',
            'date' : '2016-12-11',
            'depth' : 950,
            'tetrode' : 6,
            'cluster' : 6}, #example AC cell
            
            {'subject' : 'band029',
            'date' : '2017-05-25',
            'depth' : 1240,
            'tetrode' : 2,
            'cluster' : 2}, #another AC cell
            
            {'subject' : 'band031',
            'date' : '2017-06-29',
            'depth' : 1140,
            'tetrode' : 1,
            'cluster' : 3}, #another AC cell
            
            {'subject' : 'band044',
            'date' : '2018-01-16',
            'depth' : 975,
            'tetrode' : 7,
            'cluster' : 4}, #another AC cell
            
            {'subject' : 'band060',
            'date' : '2018-04-02',
            'depth' : 1275,
            'tetrode' : 4,
            'cluster' : 2}] #another AC cell

args = sys.argv[1:]
if len(args):
    cellsToGenerate = [int(x) for x in args]
else:
    cellsToGenerate = range(len(cellList))
print cellsToGenerate


for indCell in cellsToGenerate:
    # -- find the cell we want based on dictionary --
    cellInd, dbRow = celldatabase.find_cell(dbase, **cellList[indCell])
    cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
    
    # --- loads spike and event data for frequency tuning ephys sessions ---
    tuningEphysData, tuningBData = cell.load('tuningCurve')
    tuningEventOnsetTimes = tuningEphysData['events']['soundDetectorOn']
    if len(tuningEventOnsetTimes)==0: #some cells recorded before sound detector installed
        tuningEventOnsetTimes = tuningEphysData['events']['stimOn'] + 0.0095 #correction for bandwidth trials, determined by comparing sound detector onset to stim event onset
    tuningEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(tuningEventOnsetTimes, minEventOnsetDiff=0.2)
    tuningSpikeTimestamps = tuningEphysData['spikeTimes']
    
    freqEachTrial = tuningBData['currentFreq']
    numFreqs = np.unique(freqEachTrial)
    intEachTrial = tuningBData['currentIntensity']
    
    rasterTimeRange = [-0.3,0.5]
    tuningTimeRange = dbRow['tuningTimeRange']
    baselineTimeRange = [-0.5,-0.1]
    fullRange = [min(rasterTimeRange+tuningTimeRange+baselineTimeRange), max(rasterTimeRange+tuningTimeRange+baselineTimeRange)]
    
    trialsEachCond = behavioranalysis.find_trials_each_combination(freqEachTrial,
                                                                    numFreqs,
                                                                    intEachTrial,
                                                                    np.unique(intEachTrial))
    trialsHighInt = trialsEachCond[:,:,-1] #only interested in loudest tones as they correspond to high amp bandwidth trials
    
    # --- computes inputs to frequency tuning curve ---
    tuningSpikeTimesFromEventOnset, trialIndexForEachSpike, tuningIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        tuningSpikeTimestamps, 
                                                                                                        tuningEventOnsetTimes,
                                                                                                        fullRange)

    tuningSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(tuningSpikeTimesFromEventOnset, tuningIndexLimitsEachTrial, tuningTimeRange)
    responseArray, errorArray = funcs.calculate_tuning_curve_inputs(tuningSpikeCountMat, freqEachTrial, intEachTrial)
    responseArray = responseArray[:,-1]/(tuningTimeRange[1]-tuningTimeRange[0]) #just the high intensity freq trials
    errorArray = errorArray[:,-1]/(tuningTimeRange[1]-tuningTimeRange[0])
    
    # --- computes inputs to plot gaussian fit ---
    gaussFit = dbRow['gaussFit']
    x_fine = np.linspace(np.log2(numFreqs)[0], np.log2(numFreqs)[-1], 100)
    gaussCurve = funcs.gaussian(x_fine, gaussFit[0], gaussFit[1], gaussFit[2], gaussFit[3])
    R2 = dbRow['tuningFitR2']
    
    # --- computes baseline spike rate ---
    baselineSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(tuningSpikeTimesFromEventOnset, tuningIndexLimitsEachTrial, baselineTimeRange)
    baselineSpikeRate = np.mean(baselineSpikeCountMat.flatten())/(baselineTimeRange[1]-baselineTimeRange[0])
    
    # --- get estimated best frequency for cell ---
    prefFreq = dbRow['prefFreq']
    
    ### Save data ###    
    outputFile = 'example_frequency_tuning_{}_{}_{}um_T{}_c{}.npz'.format(dbRow['subject'], dbRow['date'],
                                                                         int(dbRow['depth']),dbRow['tetrode'],dbRow['cluster'])

    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath,
             responseArray=responseArray, 
             SEM=errorArray,
             possibleFreqs=numFreqs,
             spikeTimesFromEventOnset=tuningSpikeTimesFromEventOnset,
             indexLimitsEachTrial=tuningIndexLimitsEachTrial,
             trialsEachCond=trialsHighInt,
             tuningWindow=tuningTimeRange, rasterTimeRange=rasterTimeRange,
             baselineSpikeRate=baselineSpikeRate,
             fitXVals = x_fine, fitResponse = gaussCurve, R2 = R2, prefFreq = prefFreq)
    print outputFile + " saved"
    
    
