# -*- coding: utf-8 -*-
"""
This script creates a basic database from an inforec using celldatabase.py and calculates statistics
useful for identifying and comapring D1 and nD1 cells. 

This script will:
1. Create a basic database (minimally selected for SSQ and ISIviolations)
2. select cells by spike shape quality interspike interval violations (threshold value held in studyparams.py)
3. Calculate statistics for D1/nD1 determination using laserpulse data
4. Calculate the response latency for each cell using tuning curve data 

Created on Fri Sep 18 14:19:55 2020
@author: Devin Henderling
"""

import os
import numpy as np
import pandas as pd
import studyparams
from scipy import stats
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
import database_generation_funcs as funcs

# ========================== Run Mode ==========================

TEST = 1


if TEST:
    d1mice = studyparams.SINGLE_MOUSE
    outputDirectory = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 
                                   '{}_lattetest.h5'.format(d1mice[0]))
    pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 
                            '{}_basic.h5'.format(d1mice[0]))
else:
    d1mice = studyparams.ASTR_D1_CHR2_MICE
    outputDirectory = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 
                                   '{}_test.h5'.format(studyparams.DATABASE_NAME))
    pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 
                            '{}_basic.h5'.format(studyparams.DATABASE_NAME))
# ========================== Basic Database Creation ==========================
        
# Generates basic database, minimally selected for SSQ and ISI
# basicDB = celldatabase.generate_cell_database_from_subjects(d1mice)

# Loads basic database for testing
db = celldatabase.load_hdf(pathtoDB)  
    
# Creates variables to see if various sessions ran for cluster 
hasAM = db['sessionType'].apply(lambda s: 'am' in s)
hasLP = db['sessionType'].apply(lambda s: 'laserpulse' in s)
hasLT = db['sessionType'].apply(lambda s: 'lasertrain' in s)
hasNB = db['sessionType'].apply(lambda s: 'noiseburst' in s)
hasTC = db['sessionType'].apply(lambda s: 'tuningCurve' in s)
hasTT = db['sessionType'].apply(lambda s: 'tuningTest' in s)

 
for indIter, (indRow, dbRow) in enumerate(db.iterrows()):
    oneCell = ephyscore.Cell(dbRow, useModifiedClusters=False)
                
    # Calculating tuning curve statistics 
    session = 'tuningCurve'
        
    tuningEphysData, tuningBehavData = oneCell.load(session)
        
    baseRange = [-0.1, 0]  # Time used for baseline spike counts.

    # Extracting information from ephys and behavior data to do calculations later with
    currentFreq = tuningBehavData['currentFreq']  # The frequency for each individual trial
    currentIntensity = tuningBehavData['currentIntensity']  # The intensity for each individual trial
    uniqFreq = np.unique(currentFreq)  # List of frequencies used for presentations, no repeats
    uniqueIntensity = np.unique(currentIntensity)  # List of intensities used for presentatiosn, no repeats       
    tuningTrialsEachCond = behavioranalysis.find_trials_each_combination(currentFreq, uniqFreq,
                                                                         currentIntensity, uniqueIntensity)
    
    allIntenBase = np.array([])  # A list to collect the baseline spikes across all intensities
    respSpikeMeanTuning = np.empty((len(uniqueIntensity), len(uniqFreq)))  # A list to collect the response spikes across all intensities
    Rsquareds = []  # Collection of rsquared values
    popts = []  # Collection of optimal fit parameters for the Gaussians
    
    tuningSpikeTimes = tuningEphysData['spikeTimes']
    tuningEventOnsetTimes = tuningEphysData['events']['soundDetectorOn']
    tuningEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(tuningEventOnsetTimes,
                                                                            minEventOnsetDiff=0.2)
    
    # Checking to see if the ephys data has one more trial than the behavior data and removing the last session if it does
    if len(tuningEventOnsetTimes) == (len(currentFreq) + 1):
        tuningEventOnsetTimes = tuningEventOnsetTimes[0:-1]
        print("Correcting ephys data to be same length as behavior data")
        calculate = True
    elif len(tuningEventOnsetTimes) == len(currentFreq):
        print("Data is already the same length")
        calculate = True
    else:
        print("Something is wrong with the length of these data")
        calculate = False
        
    # ========================== Latency ==========================
    
    if calculate:
        tuningZStat, tuningPVal = \
                    funcs.sound_response_any_stimulus(tuningEventOnsetTimes, tuningSpikeTimes,
                                                      tuningTrialsEachCond[:, :, -1], timeRange=[0.0, 0.05],
                                                      baseRange=[-0.05, 0])  # All trials at all frequencies at the highest intensity
        try:
            respLatency = funcs.calculate_latency(tuningEventOnsetTimes, currentFreq, uniqFreq, currentIntensity,
                                                  uniqueIntensity, tuningSpikeTimes)
        except IndexError:
            print("Index error for cell {}".format(indRow))  # If there are no spikes in the timeRangeForLatency
            respLatency = np.nan
    else:
        respLatency = np.nan
    # if respLatency <= 0:
    #     respLatency = np.nan
    db.at[indRow, 'latency'] = respLatency  # How long the cell takes to have an response after presentation             
        
# ========================== Saving ==========================

celldatabase.save_hdf(db, outputDirectory)
print("SAVED DATAFRAME to {}".format(outputDirectory))
print(u"\U0001F4A9" * 10)