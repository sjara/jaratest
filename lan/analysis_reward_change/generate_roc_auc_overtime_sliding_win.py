'''
Store intermediate data for calculate area under curve of ROC curves generated from firing rate and trial type(whether more or less reward) in non-overlapping 10ms bins, aligned to side-in. 

Lan Guo 20171127
'''
import os
import sys
import numpy as np
import pandas as pd
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
import sklearn.metrics

STUDY_NAME = '2017rc'

#FIGNAME = 'reward_modulation_movement_selective_cells'
FIGNAME = 'roc_auc_overtime'
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)
dataDir = os.path.join('/tmp/', STUDY_NAME, FIGNAME)

if not os.path.exists(dataDir):
    os.mkdir(dataDir)

# -- These example cells I picked manually  --#
cellParamsList = []

exampleCell = {'subject':'adap012',
              'date':'2016-02-04',
              'tetrode':3,
               'cluster':3,
               'brainRegion':'astr'} # low freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'adap012',
              'date':'2016-03-09',
              'tetrode':3,
               'cluster':2,
               'brainRegion':'astr'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'adap012',
              'date':'2016-03-24',
              'tetrode':6,
               'cluster':6,
               'brainRegion':'astr'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'adap013',
              'date':'2016-03-28',
              'tetrode':4,
               'cluster':5,
               'brainRegion':'astr'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'adap013',
              'date':'2016-03-28',
              'tetrode':8,
               'cluster':8,
               'brainRegion':'astr'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'adap013',
              'date':'2016-03-30',
              'tetrode':1,
               'cluster':3,
               'brainRegion':'astr'} # low freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi001',
              'date':'2017-05-06',
              'tetrode':3,
               'cluster':5,
               'brainRegion':'ac'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-02-13',
              'tetrode':7,
               'cluster':8,
               'brainRegion':'ac'} # low freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-03-15',
              'tetrode':6,
               'cluster':7,
               'brainRegion':'ac'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-03-18',
              'tetrode':3,
               'cluster':4,
               'brainRegion':'ac'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-04-06',
              'tetrode':7,
               'cluster':5,
               'brainRegion':'ac'} # high freq
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi008',
              'date':'2017-03-14',
              'tetrode':7,
               'cluster':8,
               'brainRegion':'ac'} # high freq
cellParamsList.append(exampleCell)

# -- Select an example cell or generate all cells based on sys argv -- #
if len(sys.argv) == 1:
    cellParamsList = cellParamsList
    print 'Generating roc auc over time for all cells'
elif len( sys.argv) == 2:
    cellIndToGenerate = int(sys.argv[1])
    cellParamsList = [cellParamsList[cellIndToGenerate]]

####################################################################################
scriptFullPath = os.path.realpath(__file__)
timeRange = [0,0.5] #[-0.5,0]
binWidth = 0.010  # 10ms bins
EPHYS_SAMPLING_RATE = 30000.0
soundTriggerChannel = 0
paradigm = '2afc'
minBlockSize = 30
freqsToPlot = ['low', 'high']
alignment = 'center-out' #'side-in' 

slidingWinSize = 5 # Use 5*binWidth sliding window 
numBootstrapResamples = 1000
bootstrapSampleSize = 100
###################################################################################

# -- Access mounted behavior and ephys drives for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
EPHYS_PATH = settings.EPHYS_PATH_REMOTE

if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

if not os.path.ismount(EPHYS_PATH):
    os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ {}'.format(EPHYS_PATH))

for cellParams in cellParamsList:
    animal = cellParams['subject']
    date = cellParams['date']
    tetrode = cellParams['tetrode']
    cluster = cellParams['cluster']
    brainRegion = cellParams['brainRegion']
    celldbPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(animal))
    celldb = pd.read_hdf(celldbPath, key='reward_change')
    
    ### Using cellDB methode to find this cell in the cellDB ###
    oneCell = celldb.loc[(celldb.subject==animal) & (celldb.date==date) & (celldb.tetrode==tetrode) & (celldb.cluster==cluster)]
    sessionsThisCell = oneCell.iloc[0].sessiontype
    rcInd = sessionsThisCell.index('behavior')
    rcEphysThisCell = oneCell['ephys'].iloc[0][rcInd]
    rcBehavThisCell = oneCell['behavior'].iloc[0][rcInd]

    ## Get behavior data associated with 2afc session ###
    behavFileName = rcBehavThisCell
    behavFile = os.path.join(BEHAVIOR_PATH,animal,behavFileName)
    bdata = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')


    ### Get events data ###
    fullEventFilename=os.path.join(EPHYS_PATH, animal, rcEphysThisCell, 'all_channels.events')
    eventData = loadopenephys.Events(fullEventFilename)
    ##### Get event onset times #####
    eventData.timestamps = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE #hard-coded ephys sampling rate!!


    ### GEt spike data of just this cluster ###
    spikeFilename = os.path.join(EPHYS_PATH, animal, rcEphysThisCell, 'Tetrode{}.spikes'.format(tetrode))
    spikeData = loadopenephys.DataSpikes(spikeFilename)
    spikeData.timestamps = spikeData.timestamps/EPHYS_SAMPLING_RATE
    clustersDir = os.path.join(EPHYS_PATH, animal, rcEphysThisCell)+'_kk'
    clusterFilename = os.path.join(clustersDir, 'Tetrode{}.clu.1'.format(tetrode))
    clusters = np.fromfile(clusterFilename, dtype='int32', sep=' ')[1:]
    spikeData.timestamps = spikeData.timestamps[clusters==cluster]
    spikeData.samples = spikeData.samples[clusters==cluster, :, :]
    spikeData.samples = spikeData.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
    # FIXME: This assumes the gain is the same for all channels and records
    spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
    #spikeData = ephyscore.CellData(oneCell) #This defaults to settings ephys path
    spikeTimestamps = spikeData.timestamps

    # -- Check to see if ephys has skipped trials, if so remove trials from behav data -- #
    eventOnsetTimes=np.array(eventData.timestamps)
    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
    soundOnsetTimeEphys = eventOnsetTimes[soundOnsetEvents]
    soundOnsetTimeBehav = bdata['timeTarget']

    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    # Remove missing trials
    bdata.remove_trials(missingTrials)

    # -- calculate response and reaction time, as well as trials each type -- #
    currentBlock = bdata['currentBlock']
    blockTypeLabels = ['more_left', 'more_right']
    blockTypes = [bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
    trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
    freqsEachTrial = bdata['targetFrequency']
    possibleFreq = np.unique(freqsEachTrial)
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    
    # -- Calculate eventOnsetTimes aligned to center-out/side-in -- #
    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
    EventOnsetTimes = eventOnsetTimes[soundOnsetEvents]
    diffTimes=bdata['timeCenterOut']-bdata['timeTarget']
    #diffTimes=bdata['timeSideIn']-bdata['timeTarget']
    EventOnsetTimes+=diffTimes

    # -- Calculate spike times aligned to alignment for each trial -- #
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimestamps,EventOnsetTimes,timeRange)

    # -- Calculate spike counts for each time bin -- #
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    # -- Save intermediate data -- #
    outputFile = 'spike_count_by_bin_{}_aligned_{}_{}_T{}_c{}.npz'.format(alignment, animal, date, tetrode, cluster)
    outputFullPath = os.path.join(dataDir,outputFile)
    print 'Saving {0} ...'.format(outputFullPath)
    np.savez(outputFullPath, spikeCountMat=spikeCountMat, timeVec=timeVec, trialsEachType=trialsEachType, freqsEachTrial=freqsEachTrial, timeRange=timeRange, binWidth=binWidth, EPHYS_SAMPLING_RATE=EPHYS_SAMPLING_RATE, soundTriggerChannel=soundTriggerChannel, script=scriptFullPath, alignedTo=alignment, **cellParams)

    # -- For each freq, calculate ROC based on firing rate of correct trials and trial label (reward amount) -- #
    for freq in freqsToPlot:       
        # -- Keep only those correct trials of this freq to calculate ROC -- #
        if freq == 'low':
            oneFreqCorrectTrials = (bdata['targetFrequency'] == possibleFreq[0]) & correct 
            leftMoreTrialsOneFreq = trialsEachType[:,0]
            rewardLabelsTrialsThisFreq = leftMoreTrialsOneFreq[oneFreqCorrectTrials]
        elif freq == 'high':
            oneFreqCorrectTrials = (bdata['targetFrequency'] == possibleFreq[-1]) & correct 
            rightMoreTrialsOneFreq = trialsEachType[:,1] 
            rewardLabelsTrialsThisFreq = rightMoreTrialsOneFreq[oneFreqCorrectTrials]

        spikeCountMatThisFreq = spikeCountMat[oneFreqCorrectTrials, :]
        # -- Calculate and store roc_auc for each sliding window -- #
        yTrueLabel = rewardLabelsTrialsThisFreq
        df = pd.DataFrame(spikeCountMatThisFreq.transpose()) # Make time bin dimension as dataframe columns
        slidingSumDf = df.rolling(slidingWinSize).sum()
        slidingSums = slidingSumDf.values.transpose()[:,(slidingWinSize-1):] # Convert to original direction, get rid of trialing NaN values generated from sliding sum
        numSlidingWins = slidingSums.shape[1]
        aucEachSlidingWin = np.zeros(numSlidingWins)
        slidingWinEdges = np.zeros((numSlidingWins, 2))
        # Calculate roc auc for each sliding window
        for timeBin in range(numSlidingWins):
             yScore = slidingSums[:, timeBin]  #spikeCountMatThisFreq[:,timeBin]
             aucEachSlidingWin[timeBin] = sklearn.metrics.roc_auc_score(yTrueLabel, yScore)
             slidingWinEdges[timeBin, :] = np.array((timeVec[timeBin], timeVec[timeBin]+binWidth*slidingWinSize))
        
        nTrials = slidingSums.shape[0]
        auc95ConfidenceInterval = np.zeros((numBootstrapResamples, numSlidingWins))
        # Calculate 95% confidence interval using bootstrap resample
        for ind in range(numBootstrapResamples):
            bootstrapInds = np.random.choice(nTrials, bootstrapSampleSize) # random resample with replacement
            bsSlidingSums = slidingSums[bootstrapInds, :]
            bsYTrueLabel = yTrueLabel[bootstrapInds]
            bsAucEachSlidingWin = np.zeros(numSlidingWins)
            for timeBin in range(numSlidingWins):
                bsYScore = bsSlidingSums[:, timeBin]
                bsAucEachSlidingWin[timeBin] = sklearn.metrics.roc_auc_score(bsYTrueLabel, bsYScore)
            auc95ConfidenceInterval[ind, :] =  bsAucEachSlidingWin
   
        outputFile = 'binned_auc_roc_{}aligned_{}freq_{}_{}_T{}_c{}.npz'.format(alignment, freq, animal, date, tetrode, cluster)
        outputFullPath = os.path.join(dataDir,outputFile)
        print 'Saving {0} ...'.format(outputFullPath)
        np.savez(outputFullPath, spikeCountMatThisFreq=spikeCountMatThisFreq, rewardLabelsTrialsThisFreq=rewardLabelsTrialsThisFreq, timeVec=timeVec, slidingWinSize=slidingWinSize, slidingWinEdges=slidingWinEdges, aucEachSlidingWin=aucEachSlidingWin, auc95ConfidenceInterval=auc95ConfidenceInterval, script=scriptFullPath, frequencyPloted=freq, alignedTo=alignment, **cellParams) 
