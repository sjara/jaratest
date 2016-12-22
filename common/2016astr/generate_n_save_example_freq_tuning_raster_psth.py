'''
Generate and store intermediate data for plot showing frequency-selectivity of astr sound-responsive neurons (using tuning curve data). Includes data for raster and psth.
Lan Guo20161220
'''

import os
import sys
import importlib
import numpy as np
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratest.lan import test055_load_n_plot_billy_data_one_cell as loader

# -- Mount behavior and ephys data for psycurve and switching mice -- #
BEHAVDIR_MOUNTED = '/home/languo/data/mnt/jarahubdata'
EPHYSDIR_MOUNTED = '/home/languo/data/jarastorephys'

if not os.path.ismount(BEHAVDIR_MOUNTED):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ /home/languo/data/mnt/jarahubdata')

if not os.path.ismount(EPHYSDIR_MOUNTED):
    os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ /home/languo/data/jarastorephys')


# -- Select an example cell -- #
cellParams = {'firstParam':'test059',
              'behavSession':'20150624a',
              'tetrode':1,
              'cluster':4}

mouseName = cellParams['firstParam']
    
allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

### Using cellDB methode to find the index of this cell in the cellDB ###
cellIndex = allcells.cellDB.findcell(**cellParams)
thisCell = allcells.cellDB[cellIndex]

### Get events, spikes, and behav data from mounted drives ###
(eventOnsetTimes, spikeTimestamps, bdata) = loader.load_remote_tuning_data(thisCell,BEHAVDIR_MOUNTED,EPHYSDIR_MOUNTED)

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

### Save data ###    
outputDir = '/home/languo/data/mnt/figuresdata'
outputFile = 'example_freq_tuning_raster_{}_{}.npz'.format(thisCell.animalName, thisCell.behavSession)
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, spikeTimestamps=spikeTimestamps, eventOnsetTimes=eventOnsetTimes,
    freqEachTrial=freqEachTrial)


# -- Calculate and store intermediate data for tuning psth -- #
possibleFreq = np.unique(freqEachTrial)
trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)
timeRange = [-0.5,1]
binWidth = 0.010
(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimes,timeRange)
timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

### Save data ###
outputDir = '/home/languo/data/mnt/figuresdata'
outputFile = 'example_freq_tuning_psth_{}_{}.npz'.format(thisCell.animalName, thisCell.behavSession)
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, spikeCountMat=spikeCountMat, timeVec=timeVec, trialsEachFreq=trialsEachFreq)
