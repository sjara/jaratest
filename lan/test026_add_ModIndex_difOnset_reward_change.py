'''
Lan Guo 20160111
Modified from Billy's modIndexCalcSwitching.py
New version, now takes cellDB whose individual cells contain the property 'quality' to mark whether it's a good cell or not.
Finds modulation index for all good cells (based on oneCell.quality, score of 1 or 6) for reward_change task. Comparing response to one frequency under less or more reward conditions using only correct trials.
NEW: can choose different alignment options (sound, center-out, side-in) and calculate Mod Index for different time windows with aligned spikes. 
Implemented: using santiago's methods to remove missing trials from behavior when ephys has skipped trials. -LG20160307
Implemented 'trialLimit' constraint to exclude blocks with few trials at the end of a behav session. -LG 20160324
'''

from jaratoolbox import loadbehavior
from jaratoolbox import settings_2 as settings
from jaratoolbox import ephyscore
import os
import numpy as np
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt
import sys
import importlib

alignment = sys.argv[1] #the first argument is alignment, choices are 'sound', 'center-out' and 'side-in'
if sys.argv[2]=='0':
    countTimeRange = [int(sys.argv[2]),float(sys.argv[3])]
elif sys.argv[3]=='0':
    countTimeRange = [float(sys.argv[2]),int(sys.argv[3])]
else:
    countTimeRange = [float(sys.argv[2]),float(sys.argv[3])]
mouseNameList = sys.argv[4:] #the fourth argument onwards are the mouse names to tell the script which allcells file to use
#print alignment,countTimeRange,mouseNameList

SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.020 # Size of each bin in histogram in seconds
#Frequency = 1 #This chooses which frequency to look at, numbered out of possible frequencies starting with the lowest frequency as number 0
#countTimeRange = [0,0.1] #time range in which to count spikes for modulation index and modulation significance tests
#stimulusRange = [0.0,0.1] # The time range that the stimulus is being played, used in statistic test for modulation significance

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes
timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

for mouseName in mouseNameList:
    allcellsFileName = 'allcells_'+mouseName
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)
    #from jaratoolbox.test.lan.Allcells import allcellsFileName as allcells
    subject = allcells.cellDB[0].animalName
    ephysRootDir = settings.EPHYS_PATH
    outputDir = '/home/languo/data/ephys/'+mouseName
    
    ###################Choose alignment and time window to calculate mod Index#######################
    #alignment = 'center-out'  #put here alignment choice!!choices are 'sound', 'center-out', 'side-in'.
    #countTimeRange = [0.1,0.2]
    window = str(countTimeRange[0])+'to'+str(countTimeRange[1])+'sec_window_'
    nameOfmodSFile = 'modSig_'+alignment+'_'+window+mouseName
    nameOfmodIFile = 'modIndex_'+alignment+'_'+window+mouseName

    #############################################################################

    finalOutputDir = outputDir+'/'+subject+'_stats'
    
    if mouseName=='adap015' or mouseName=='adap013' or mouseName=='adap017':
        experimenter = 'billy'
    else:
        experimenter = 'lan'
    
    paradigm = '2afc'
    numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
    print numOfCells

    behavSession = ''
    #processedDir = os.path.join(settings.EPHYS_PATH,subject+'_processed')

    ###############FOR USING MODIDICT WITH ALL FREQS############################################
    class nestedDict(dict):
        def __getitem__(self, item):
            try:
                return super(nestedDict, self).__getitem__(item)
            except KeyError:
                value = self[item] = type(self)()
                return value
    #############################################################################################


    modIList = []#List of behavior sessions that already have modI values calculated
    modSList = []
    try:
        modI_file = open('%s/%s.txt' % (finalOutputDir,nameOfmodIFile), 'r+') #open a text file to read and write in
        behavName = ''
        for line in modI_file:
            if line.startswith(codecs.BOM_UTF8):
                line = line[3:]
            behavLine = line.split(':')
            if (behavLine[0] == 'Behavior Session'):
                behavName = behavLine[1][:-1]
                modIList.append(behavName)

    except:
        modI_file = open('%s/%s.txt' % (finalOutputDir,nameOfmodIFile), 'w') #when file dosenot exit then create it, but will truncate the existing file


    #No need to initialize modIList again since all behav sessions in modI file should be the same as the ones in modSig file.
    try:
        modSig_file = open('%s/%s.txt' % (finalOutputDir,nameOfmodSFile), 'r+') #open a text file to read and write in
        behavName = ''
        for line in modSig_file:
            if line.startswith(codecs.BOM_UTF8):
                line = line[3:]
            behavLine = line.split(':')
            if (behavLine[0] == 'Behavior Session'):
                behavName = behavLine[1][:-1]
                modSList.append(behavName)
    except:
        modSig_file = open('%s/%s.txt' % (finalOutputDir,nameOfmodSFile), 'w') #when file dosenot exit then create it, but will truncate the existing file


    badSessionList = [] #Makes sure sessions that crash don't get modI values printed
    behavSession = ''
    modIndexArray = []
    modIDict = nestedDict() #stores all the modulation indices
    modSigDict = nestedDict()

    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]

        if oneCell.quality==1 or oneCell.quality==6:

            if (oneCell.behavSession in modIList and oneCell.behavSession in modSList): #checks to make sure the modI value is not recalculated
                continue
            try:

                if (behavSession != oneCell.behavSession):

                    subject = oneCell.animalName
                    behavSession = oneCell.behavSession
                    ephysSession = oneCell.ephysSession
                    ephysRoot = os.path.join(ephysRootDir,subject)
                    trialLimit = oneCell.trialLimit

                    print behavSession

                    # -- Load Behavior Data --
                    behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
                    bdata = loadbehavior.BehaviorData(behaviorFilename)
                    soundOnsetTimeBehav = bdata['timeTarget']

                    print behaviorFilename
                    # -- Load event data and convert event timestamps to ms --
                    ephysDir = os.path.join(ephysRoot, ephysSession)
                    eventFilename=os.path.join(ephysDir, 'all_channels.events')
                    events = loadopenephys.Events(eventFilename) # Load events data
                    eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 

                    soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)
                    soundOnsetTimeEphys = eventTimes[soundOnsetEvents]
                    ######check if ephys and behav miss-aligned, if so, remove skipped trials####

                    # Find missing trials
                    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)

                    # Remove missing trials,all fields of bdata's results are modified after this
                    bdata.remove_trials(missingTrials)
                    print 'behav length',len(soundOnsetTimeBehav),'ephys length',len(soundOnsetTimeEphys)

                    ######do the analysis based on what events to align spike data to#####
                    if alignment == 'sound':
                        EventOnsetTimes = eventTimes[soundOnsetEvents]
                    elif alignment == 'center-out':
                        EventOnsetTimes = eventTimes[soundOnsetEvents]
                        diffTimes=bdata['timeCenterOut']-bdata['timeTarget']
                        EventOnsetTimes+=diffTimes
                    elif alignment == 'side-in':
                        EventOnsetTimes = eventTimes[soundOnsetEvents]
                        diffTimes=bdata['timeSideIn']-bdata['timeTarget']
                        EventOnsetTimes+=diffTimes
                    print len(EventOnsetTimes)

                    rightward = bdata['choice']==bdata.labels['choice']['right']
                    leftward = bdata['choice']==bdata.labels['choice']['left']
                    #valid = (bdata['outcome']==bdata.labels['outcome']['correct'])|(bdata['outcome']==bdata.labels['outcome']['error'])
                    correct = bdata['outcome']==bdata.labels['outcome']['correct']
                    #correctRightward = rightward & correct
                    #correctLeftward = leftward & correct

                    possibleFreq = np.unique(bdata['targetFrequency'])
                    print possibleFreq
                    numberOfFrequencies = len(possibleFreq)
                    numberOfTrials = len(bdata['choice'])
                    targetFreqs = bdata['targetFrequency']
                    currentBlock = bdata['currentBlock']

                    #######20160324 Implemented trialLimit constraint to exclude blocks with few trials at the end of a behav session 
                    if(not len(trialLimit)):
                        validTrials = np.ones(len(currentBlock),dtype=bool)
                    else:
                        validTrials = np.zeros(len(currentBlock),dtype=bool)
                        validTrials[trialLimit[0]:trialLimit[1]] = 1

                    blockTypes = [bdata.labels['currentBlock']['same_reward'],bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
                    #blockLabels = ['same_reward','more_left', 'more_right']
                    trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes) #trialsEachType is an array of dimension nTrials*nblockTypes where boolean vector (in a column) indicates which trials are in each type of block

                    for possFreq in possibleFreq:
                        modIDict[behavSession][possFreq] = np.zeros([clusNum*numTetrodes]) #0 being no modIndex
                        modSigDict[behavSession][possFreq] = np.ones([clusNum*numTetrodes]) #1 being no significance test

                # -- Load Spike Data From Certain Cluster --
                spkData = ephyscore.CellData(oneCell)
                spkTimeStamps = spkData.spikes.timestamps

                clusterNumber = (oneCell.tetrode-1)*clusNum+(oneCell.cluster-1)
                for Freq in possibleFreq:
                    oneFreq = targetFreqs == Freq
                    if Freq <= 9500:  #Arbitrary boundary based on behavior sessions so far. This is a 'low' freq - going left trial 
                        trialsToUseMoreReward = trialsEachType[:,1]&oneFreq&correct&validTrials #trialsEachType[:,1] are all the 'more_left' trials.

                        #trialsToUseLessReward = trialsEachType[:,2] & oneFreq & correct&validTrials
                        trialsToUseLessReward = (trialsEachType[:,0]+trialsEachType[:,2])&oneFreq&correct&validTrials #'same_reward' block is also 'less reward'
                        #FIX ME: add a checkpoint to stop calculating modIndex if too few trials(<10) can be used for a given condition
                        print Freq,'left',len(np.nonzero(trialsToUseMoreReward)[0]),len(np.nonzero(trialsToUseLessReward)[0])
                    else:
                        trialsToUseMoreReward = trialsEachType[:,2]&oneFreq&correct&validTrials
                        #trialsEachType[:,2] are all the 'more_right' trials.
                        #trialsToUseLessReward = trialsEachType[:,1] & oneFreq & correct
                        trialsToUseLessReward = (trialsEachType[:,0]+trialsEachType[:,1])&oneFreq&correct&validTrials
                        print Freq,'right',len(np.nonzero(trialsToUseMoreReward)[0])

                    trialsEachCond = [trialsToUseMoreReward,trialsToUseLessReward]
                    #print trialEachCond[1][0:10] #trialsEachCond[0][0:10]
                    #print 'behavior ',behavSession,' tetrode ',oneCell.tetrode,' cluster ',oneCell.cluster,'freq',Freq,  

                    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                        spikesanalysis.eventlocked_spiketimes(spkTimeStamps,EventOnsetTimes,timeRange)
                    print len(spikeTimesFromEventOnset)

                    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange)

                    spikeCountEachTrial = spikeCountMat.flatten()
                    spikeAvgMoreReward = sum(spikeCountEachTrial[trialsToUseMoreReward])/float(sum(trialsToUseMoreReward))
                    spikeAvgLessReward = sum(spikeCountEachTrial[trialsToUseLessReward])/float(sum(trialsToUseLessReward))
                    print 'cluster', clusterNumber, spikeAvgMoreReward, spikeAvgLessReward

                    if ((spikeAvgMoreReward + spikeAvgLessReward) == 0):
                        modIDict[behavSession][Freq][clusterNumber]=0.0
                        modSigDict[behavSession][Freq][clusterNumber]=1.0
                    else:
                        modIDict[behavSession][Freq][clusterNumber]=((spikeAvgMoreReward - spikeAvgLessReward)/(spikeAvgMoreReward + spikeAvgLessReward))  
                        modSig = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange,trialsEachCond)
                        modSigDict[behavSession][Freq][clusterNumber]=modSig[1]
                        print modIDict[behavSession][Freq][clusterNumber]
                #print modIDict
                    #print spikeAvgMoreReward,' ', spikeAvgLessReward, ' ',modIDict[behavSession][Freq][clusterNumber]

            except:
                if (oneCell.behavSession not in badSessionList):
                    badSessionList.append(oneCell.behavSession)

        else:
            continue

    #########################################################################################
    #This is the save all the values in a text file
    #########################################################################################
    bSessionList = []
    for bSession in modIDict:
        if (bSession not in badSessionList):
            bSessionList.append(bSession)

    bSessionList.sort()
    for bSession in bSessionList:
        if bSession not in modIList:
            modI_file.write("Behavior Session:%s" % bSession)
            for freq in modIDict[bSession]:
                modI_file.write("\n%s " % freq)
                for modInd in modIDict[bSession][freq]:
                    modI_file.write("%s," % modInd)
            modI_file.write("\n")
        if bSession not in modSList:
            modSig_file.write("Behavior Session:%s" % bSession)
            for freq in modSigDict[bSession]:
                modSig_file.write("\n%s " % freq) 
                for modSig in modSigDict[bSession][freq]:
                    modSig_file.write("%s," % modSig)
            modSig_file.write("\n")

    #Important for data read out: the format of the modI and modSig files are very similar to maxZ files. one line for behav session starting with 'Behavior Session:'; one line for modInd/modSig starting with the frequency followed by space, then modIndex/modSig for each cell separated by ','

    modI_file.close()
    modSig_file.close()
    #########################################################################################

    print 'error with sessions: '
    for badSes in badSessionList:
        print badSes
    print 'finished modI value check'


