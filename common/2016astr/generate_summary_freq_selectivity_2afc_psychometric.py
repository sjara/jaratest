'''
Quantify 2afc sound response data in psychometric mice. For all the non-duplicated good cells that are in the striatum, look at their psychometric 2afc data, calculate a Z score and response index for each frequency comparing baseline (100-0ms window before sound) and sound-evoked response (0-100ms window from sound-onset). Store the Z scores, p values, ave response rates for each frequency for each cell; as well as the Z score that is largest in absolute value, the response index of that frequency, and the frequency that generates it. 
Use one-way ANOVA to compare whether evoked-responses for all frequencies were significantly different as a measure of 'frequency-selectivity'. 
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

paradigm = '2afc'
scriptFullPath = os.path.realpath(__file__)
EPHYS_SAMPLING_RATE = 30000.0
soundTriggerChannel = 0
baseRange = [-0.1, 0] # time range of baseline period
responseRange = [0, 0.1] # time range of sound period
timeRange = [-0.2,0.2]
qualityList = [1,6]
ISIcutoff = 0.02
numOfFreqs = 6
maxNumOfTrials = 300 # a big number to make sure allocate enough space to store firing rate for all trials of each frequency

# -- Access mounted behavior and ephys drives for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
EPHYS_PATH = settings.EPHYS_PATH_REMOTE

# if not os.path.ismount(BEHAVIOR_PATH):
#     os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

# if not os.path.ismount(EPHYS_PATH):
#     os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ {}'.format(EPHYS_PATH))


# -- Read in databases storing all measurements from psycurve mice -- #
psychometricFilePath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME)
psychometricFileName = 'all_cells_all_measures_waveform_psychometric.h5'
psychometricFullPath = os.path.join(psychometricFilePath,psychometricFileName)
allcells_psychometric = pd.read_hdf(psychometricFullPath,key='psychometric')

goodcells_psychometric = (allcells_psychometric.cellQuality.isin(qualityList)) & (allcells_psychometric.ISI <= ISIcutoff)
cellInStr =  (allcells_psychometric.cellInStr==1)
keepAfterDupTest = allcells_psychometric.keep_after_dup_test
cellSelector = goodcells_psychometric & cellInStr & keepAfterDupTest  #Boolean array
cellsToPlot = allcells_psychometric[cellSelector]

# For cells that do not pass the cell selection criteria, the best freq, maxZ score, and response index are set to zero and the p value for sound responsiveness and frequency selectivity are set to one.
bestFreqEachCell = np.zeros(len(cellsToPlot))
maxZscoreEachCell = np.zeros(len(cellsToPlot))
pValSoundResponseEachCell = np.ones(len(cellsToPlot))
maxZresponseIndEachCell = np.zeros(len(cellsToPlot))
freqSelectivityEachCell = np.ones(len(cellsToPlot))
zScoresEachFreqEachCell = np.zeros((len(cellsToPlot),numOfFreqs))
pValEachFreqEachCell = np.ones((len(cellsToPlot),numOfFreqs))
responseEachFreqEachCell = np.ma.masked_array(np.empty((len(cellsToPlot),maxNumOfTrials,numOfFreqs)),mask=np.zeros((len(cellsToPlot),maxNumOfTrials,numOfFreqs)))
baselineEachFreqEachCell = np.ma.masked_array(np.empty((len(cellsToPlot),maxNumOfTrials,numOfFreqs)),mask=np.zeros((len(cellsToPlot),maxNumOfTrials,numOfFreqs)))
responseIndEachFreqEachCell = np.zeros((len(cellsToPlot),numOfFreqs))

cellsToPlot = cellsToPlot.reset_index()
for ind,cell in cellsToPlot.iterrows(): 
    print 'retrieving data for cell', ind
    animalName = cell['animalName']
    allcellsFileName = 'allcells_'+animalName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)
    
    behavSession = cell['behavSession']
    tetrode = cell['tetrode']
    cluster = cell['cluster']
    ### Using cellDB methode to find the index of this cell in the cellDB ###
    cellIndex = allcells.cellDB.findcell(animalName, behavSession, tetrode, cluster)
    oneCell = allcells.cellDB[cellIndex]
    
    ephysSession = oneCell.ephysSession

    ## Get behavior data associated with 2afc session ###
    behavFileName = '{0}_{1}_{2}.h5'.format(animalName,paradigm,behavSession)
    behavFile = os.path.join(BEHAVIOR_PATH,animalName,behavFileName)
    bdata = loadbehavior.BehaviorData(behavFile,readmode='full')

    ### Get events data ###
    fullEventFilename=os.path.join(EPHYS_PATH, animalName, ephysSession, 'all_channels.events')
    eventData = loadopenephys.Events(fullEventFilename)
    ##### Get event onset times #####
    eventData.timestamps = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE #hard-coded ephys sampling rate!!

    ### GEt spike data of just this cluster ###
    spikeFilename = os.path.join(EPHYS_PATH,oneCell.animalName,oneCell.ephysSession, 'Tetrode{}.spikes'.format(oneCell.tetrode))
    spikeData = loadopenephys.DataSpikes(spikeFilename)
    spikeData.timestamps = spikeData.timestamps/EPHYS_SAMPLING_RATE
    clustersDir = os.path.join(EPHYS_PATH,oneCell.animalName,oneCell.ephysSession)+'_kk'
    clusterFilename = os.path.join(clustersDir, 'Tetrode{}.clu.1'.format(oneCell.tetrode))
    clusters = np.fromfile(clusterFilename, dtype='int32', sep=' ')[1:]
    spikeData.timestamps = spikeData.timestamps[clusters==oneCell.cluster]
    spikeData.samples = spikeData.samples[clusters==oneCell.cluster, :, :]
    spikeData.samples = spikeData.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
    # FIXME: This assumes the gain is the same for all channels and records
    spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
    #spikeData = ephyscore.CellData(oneCell) #This defaults to settings ephys path
    spikeTimestamps = spikeData.timestamps

    eventOnsetTimes=np.array(eventData.timestamps)
    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
    soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]
    soundOnsetTimeBehav = bdata['timeTarget']
    # -- Check to see if ephys and behav recordings have same number of trials, remove missing trials from behav file -- #
    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimes,soundOnsetTimeBehav)
    # Remove missing trials
    bdata.remove_trials(missingTrials)
    
    print 'calculating z scores for cell', ind
    possibleFreq = np.unique(bdata['targetFrequency'])
    numFreqs = len(possibleFreq)
    # -- Calculate Z score of sound response for each frequency -- #
    zScores = []
    pVals = []
    responseEachFreq = [] #store sound-evoked response (0-100ms) for each trial
    baselineEachFreq = [] #store baseline rate (-100-0ms) for each trial
    responseInds = []
    for freq in possibleFreq:
        # -- Only use valid trials of one frequency to estimate response index -- #
        oneFreqTrials = (bdata['targetFrequency'] == freq) & bdata['valid'].astype('bool')
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
