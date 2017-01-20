'''
Generate and store intermediate data for plot showing frequency-selectivity of astr sound-responsive neurons (using tuning curve data). Data for raster and psth are saved separately. 
For raster data, output contains spikeTimestamps, eventOnsetTimes, freqEachTrial.
For psth data, output contains spikeCountMat, timeVec, freqEachTrial.

Lan Guo20161220
'''

### To DO 

# In the filename of the npz should include tetrode and cluster e.g. T6_c2
# save the script name that generates the npz in the npz file, in the field called 'script' (using os.path.realpath(__file__)
# Save the manually set params such as timeRange in npz file

import os
import sys
import importlib
import numpy as np
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratest.lan import test055_load_n_plot_billy_data_one_cell as loader
import figparams

timeRange = [-0.5,1]
binWidth = 0.010
scriptFullPath = os.path.realpath(__file__)

# -- Access mounted behavior and ephys drives for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
EPHYS_PATH = settings.EPHYS_PATH_REMOTE

if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

if not os.path.ismount(EPHYS_PATH):
    os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ {}'.format(EPHYS_PATH))


# -- Select an example cell from allcells file -- #
cellParamsList = [{'firstParam':'adap020',
                   'behavSession':'20160420a',
                   'tetrode':3,
                   'cluster':5},
                  {'firstParam':'test089',
                   'behavSession':'20150804a',
                   'tetrode':7,
                   'cluster':9},
                  {'firstParam':'test089',
                   'behavSession':'20150911a',
                   'tetrode':7,
                   'cluster':7}]

for cellParams in cellParamsList:
    mouseName = cellParams['firstParam']

    allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)

    ### Using cellDB methode to find the index of this cell in the cellDB ###
    cellIndex = allcells.cellDB.findcell(**cellParams)
    thisCell = allcells.cellDB[cellIndex]

    ### Get events, spikes, and behav data from mounted drives ###
    (eventOnsetTimes, spikeTimestamps, bdata) = loader.load_remote_tuning_data(thisCell,BEHAVIOR_PATH,EPHYS_PATH)

    # -- Calculate and store intermediate data for tuning raster -- #
    freqEachTrial = bdata['currentFreq']
    intensityEachTrial = bdata['currentIntensity']
    possibleFreq = np.unique(freqEachTrial)
    possibleIntensity = np.unique(intensityEachTrial)
    if len(possibleIntensity) != 1:
        intensity = 50  # 50dB is the stimulus intensity used in 2afc task
        ###Just select the trials with a given intensity###
        trialsThisIntensity = [intensityEachTrial==intensity]
        freqEachTrial = freqEachTrial[trialsThisIntensity]
        #intensityEachTrial = intensityEachTrial[trialsThisIntensity]
        eventOnsetTimes = eventOnsetTimes[trialsThisIntensity]

    possibleFreq = np.unique(freqEachTrial)
    trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)
    timeRange = [-0.5,1]
    binWidth = 0.010
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimes,timeRange)

    ### Save raster data ###    
    outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
    outputFile = 'example_freq_tuning_raster_{}_{}_T{}_c{}.npz'.format(thisCell.animalName, thisCell.behavSession, thisCell.tetrode,thisCell.cluster)
    outputFullPath = os.path.join(outputDir,outputFile)
    np.savez(outputFullPath, spikeTimestamps=spikeTimestamps, eventOnsetTimes=eventOnsetTimes, possibleFreq=possibleFreq, spikeTimesFromEventOnset=spikeTimesFromEventOnset, indexLimitsEachTrial=indexLimitsEachTrial, timeRange=timeRange,trialsEachFreq=trialsEachFreq, script=scriptFullPath, **cellParams)

    # -- Calculate and store intermediate data for tuning psth -- #
    freqScaleFactor = 3 #factor to reduce number of frequencies plotted by
    possibleFreq = possibleFreq[1::freqScaleFactor] #select just a subset of frequencies to plot
    trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)

    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    ### Save psth data ###
    outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
    outputFile = 'example_freq_tuning_psth_{}_{}_T{}_c{}.npz'.format(thisCell.animalName, thisCell.behavSession,thisCell.tetrode,thisCell.cluster)
    outputFullPath = os.path.join(outputDir,outputFile)
    np.savez(outputFullPath, possibleFreq=possibleFreq, spikeCountMat=spikeCountMat, timeVec=timeVec, trialsEachFreq=trialsEachFreq, timeRange=timeRange, binWidth=binWidth, script=scriptFullPath, **cellParams)
