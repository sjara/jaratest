'''
Quantify high vs low frequency selectivity fixing one movement direction at a time, using all good cells recorded in the 2afc psychometric task. For all the non-duplicated good cells that are in the striatum, look at their response each trial each frequency for trials either with right or left subsequent choice.
Lan Guo 20180125  
'''

import os
import sys
import numpy as np
import pandas as pd
import importlib
from jaratoolbox import settings
import figparams
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
import scipy.stats as stats
import pdb

FIGNAME = 'sound_freq_selectivity'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
dataDir = outputDir

paradigm = '2afc'
scriptFullPath = os.path.realpath(__file__)
'''
EPHYS_SAMPLING_RATE = 30000.0
soundTriggerChannel = 0
baseRange = [-0.1, 0] # time range of baseline period
responseRange = [0, 0.1] # time range of sound period
timeRange = [-0.2,0.2]
qualityList = [1,6]
ISIcutoff = 0.02
numOfFreqs = 6
maxNumOfTrials = 300 # a big number to make sure allocate enough space to store firing rate for all trials of each frequency
'''
# -- Access mounted behavior and ephys drives for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
EPHYS_PATH = settings.EPHYS_PATH_REMOTE

if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

if not os.path.ismount(EPHYS_PATH):
    os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ {}'.format(EPHYS_PATH))


# -- Read in databases storing all measurements from psycurve mice -- #
psychometricFilePath = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
psychometricFileName = 'all_cells_all_measures_waveform_psychometric.h5'
psychometricFullPath = os.path.join(psychometricFilePath,psychometricFileName)
allcells_psychometric = pd.read_hdf(psychometricFullPath,key='psychometric')

goodcells_psychometric = (allcells_psychometric.cellQuality.isin(qualityList)) & (allcells_psychometric.ISI <= ISIcutoff)
cellInStr =  (allcells_psychometric.cellInStr==1)
keepAfterDupTest = allcells_psychometric.keep_after_dup_test
cellSelector = goodcells_psychometric & cellInStr & keepAfterDupTest  #Boolean array
cellsToPlot = allcells_psychometric[cellSelector]

responseFilename = 'response_each_freq_each_cell_psycurve_2afc.npz'
responseFullPath = os.path.join(dataDir,responseFilename)
responseEachCellEachFreq = np.load(responseFullPath)

cellsToPlot = cellsToPlot.reset_index()
for ind,cell in cellsToPlot.iterrows(): 
    print 'retrieving data for cell', ind
    animalName = cell['animalName']
   
    behavSession = cell['behavSession']
    tetrode = cell['tetrode']
    cluster = cell['cluster']
   
    ## Get behavior data associated with 2afc session ###
    behavFileName = '{0}_{1}_{2}.h5'.format(animalName,paradigm,behavSession)
    behavFile = os.path.join(BEHAVIOR_PATH,animalName,behavFileName)
    bdata = loadbehavior.BehaviorData(behavFile,readmode='full')

    ### Get events data ###
    fullEventFilename=os.path.join(EPHYS_PATH, animalName, ephysSession, 'all_channels.events')
    eventData = loadopenephys.Events(fullEventFilename)
    ##### Get event onset times #####
    eventData.timestamps = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE #hard-coded ephys sampling rate!!

    eventOnsetTimes=np.array(eventData.timestamps)
    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
    soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]
    soundOnsetTimeBehav = bdata['timeTarget']
    # -- Check to see if ephys and behav recordings have same number of trials, remove missing trials from behav file -- #
    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimes,soundOnsetTimeBehav)
    # Remove missing trials
    bdata.remove_trials(missingTrials)
    
    for indf, freq in enumerate(possibleFreq):
        # -- Only use valid trials of one frequency to estimate response index -- #
        rightward = bdata['choice']==bdata.labels['choice']['right']
        leftward = bdata['choice']==bdata.labels['choice']['left'] 
        oneFreqTrials = (bdata['targetFrequency'] == freq) & bdata['valid'].astype('bool')
        oneFreqTrialsLeft = oneFreqTrials & leftward
        oneFreqTrialsRight = oneFreqTrials & rightward
        # need to figure out which trials of the oneFreqTrials are left, which are right
        responseEachFreqEachCell[ind,:,indf] # These are all the trials 
        oneFreqSoundOnsetTimes = soundOnsetTimes[oneFreqTrials]
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimestamps,oneFreqSoundOnsetTimes,timeRange)
        # Generate the spkCountMatrix where each row is one trial, each column is a time bin to count spikes in, in this case one time bin for baseline and one time bin for sound period
        
        nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange) 
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange)
        print nspkBase.shape, nspkResp.shape
                
        # Calculate response index (S-B)/(S+B) where S and B are ave response during the sound window and baseline window, respectively
        responseIndex = (np.mean(nspkResp) - np.mean(nspkBase))/(np.mean(nspkResp) + np.mean(nspkBase))
        responseInds.append(responseIndex)
        responseEachFreq.append(np.squeeze(nspkResp)) #Store response rate to each stim frequency(for all trials) 
        baselineEachFreq.append(np.squeeze(nspkBase))
        print 'ave firing rate for baseline and sound periods are', np.mean(nspkBase), np.mean(nspkResp), 'response index is', responseIndex

        #[zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange,responseRange) #computes z score for each bin. zStat is array of z scores. maxZ is maximum value of z in timeRange; in this case only one bin so only one Z score
        # Calculate statistic using ranksums test 
        zStat,pValue = stats.ranksums(nspkResp, nspkBase)
        print zStat, pValue
        zScores.append(zStat)
        pVals.append(pValue)
        
    #?? Use correction for multiple comparisons(n comparisons where n=number of frequencies presented) here, then store whether a cell is significantly 'responsive' or not ??
    
    indMaxZ = np.argmax(np.abs(zScores))
    maxZscore = zScores[indMaxZ] 
    bestFreq = possibleFreq[indMaxZ]
    pVal = pVals[indMaxZ]
    responseIndMaxZ = responseInds[indMaxZ] #Take the response index for the freq with the biggest absolute response
    bestFreqEachCell[ind] = bestFreq
    maxZscoreEachCell[ind] = maxZscore
    maxZresponseIndEachCell[ind] = responseIndMaxZ
    pValSoundResponseEachCell[ind] = pVal
    zScoresEachFreqEachCell[ind,:] = zScores
    pValEachFreqEachCell[ind,:] = pVals
    responseIndEachFreqEachCell[ind,:] = responseInds
    for indf in range(numOfFreqs):
        numOfTrials = len(responseEachFreq[indf])
        responseEachFreqEachCell[ind,:numOfTrials,indf] = responseEachFreq[indf] #[np.mean(response) for response in responseEachFreq]
        responseEachFreqEachCell.mask[ind,numOfTrials:,indf] = True #Mask the extra trials not occupied by data
        baselineEachFreqEachCell[ind,:numOfTrials,indf] = baselineEachFreq[indf]
        baselineEachFreqEachCell.mask[ind,numOfTrials:,indf] = True

    # freqSelectivityEachCell contain the p value of the ANOVA test comparing evoked responses from all frequencies
    statistics, freqSelectivityEachCell[ind] = stats.f_oneway(*responseEachFreq) # Use one-way ANOVA to compare responses from all frequencies to see if significantly different -> if so quantify cell as freq selective
    #pdb.set_trace()

# -- Save psth intermediate data -- #
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

outputFile = 'summary_2afc_best_freq_maxZ_psychometric.npz'
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, bestFreqEachCell=bestFreqEachCell, maxZscoreEachCell=maxZscoreEachCell, pValSoundResponseEachCell=pValSoundResponseEachCell, maxZresponseIndEachCell=maxZresponseIndEachCell, freqSelectivityEachCell=freqSelectivityEachCell, zScoresEachFreqEachCell=zScoresEachFreqEachCell, pValEachFreqEachCell=pValEachFreqEachCell, responseIndEachFreqEachCell=responseIndEachFreqEachCell, cellSelectorBoolArray=cellSelector, baselineWindow=baseRange, soundWindow=responseRange, paradigm=paradigm, script=scriptFullPath)
# Have to save the two masked arrays individually because:
# NotImplementedError: MaskedArray.tofile() not implemented yet.
# Cannot directly save masked arrays in npz
# responseEachFreqEachCell=responseEachFreqEachCell, baselineEachFreqEachCell=baselineEachFreqEachCell,
responseEachFreqEachCellFile = 'response_each_freq_each_cell_psycurve_2afc.npz'
baselineEachFreqEachCellFile = 'baseline_each_freq_each_cell_psycurve_2afc.npz'

responseEachFreqEachCell.dump(os.path.join(outputDir,responseEachFreqEachCellFile))
baselineEachFreqEachCell.dump(os.path.join(outputDir,baselineEachFreqEachCellFile))
