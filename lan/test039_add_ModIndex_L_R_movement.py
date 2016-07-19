'''
Lan Guo 20160411

Calculates modulation index for all good cells (based on oneCell.quality, score of 1 or 6) in an allcells file. Comparing activity during movement in leftward trials versus in rightward trials, using only correct trials.
Spikes are aligned to 'center-out'. 
Used santiago's methods to remove missing trials from behavior when ephys has skipped trials.
Implemented 'trialLimit' constraint to exclude blocks with few trials at the end of a behav session. 
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

########---Input system arguments after python file name: start of countTimeRange, end of countTimeRange, subjects---#############
if sys.argv[1]=='0':
    countTimeRange = [int(sys.argv[1]),float(sys.argv[2])]
elif sys.argv[2]=='0':
    countTimeRange = [float(sys.argv[1]),int(sys.argv[2])]
else:
    countTimeRange = [float(sys.argv[1]),float(sys.argv[2])]
mouseNameList = sys.argv[3:] #the fourth argument onwards are the mouse names to tell the script which allcells file to use
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
    
    window = str(countTimeRange[0])+'to'+str(countTimeRange[1])+'sec_window_'
   #################################################################################
    nameOfmodSFile = 'modSig_LvsR_movement_'+window+mouseName
    nameOfmodIFile = 'modIndex_LvsR_movement_'+window+mouseName

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
    try:
        modI_file = open('%s/%s.txt' % (finalOutputDir,nameOfmodIFile), 'r+') #open a text file to read and write in
        behavName = ''
        for line in modI_file:
            behavLine = line.split(':')
            if (behavLine[0] == 'Behavior Session'):
                behavName = behavLine[1][:-1]
                modIList.append(behavName)

    except:
        modI_file = open('%s/%s.txt' % (finalOutputDir,nameOfmodIFile), 'w') #when file dosenot exit then create it, but will truncate the existing file


    #No need to initialize modIList again since all behav sessions in modI file should be the same as the ones in modSig file.
    try:
        modSig_file = open('%s/%s.txt' % (finalOutputDir,nameOfmodSFile), 'r+') #open a text file to read and write in

    except:
        modSig_file = open('%s/%s.txt' % (finalOutputDir,nameOfmodSFile), 'w') #when file dosenot exit then create it, but will truncate the existing file


    badSessionList = [] #Makes sure sessions that crash don't get modI values printed
    behavSession = ''
    modIndexArray = []
    modIDict =nestedDict() #stores all the modulation indices
    modSigDict =nestedDict()

    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]

        if oneCell.quality==1 or oneCell.quality==6:

            if (oneCell.behavSession in modIList): #checks to make sure the modI value is not recalculated
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

                    ##########Spike data will be aligned to center-out movement onset########                    
                    EventOnsetTimes = eventTimes[soundOnsetEvents]
                    diffTimes=bdata['timeCenterOut']-bdata['timeTarget']
                    EventOnsetTimes+=diffTimes

                    rightward = bdata['choice']==bdata.labels['choice']['right']
                    leftward = bdata['choice']==bdata.labels['choice']['left']
                    #valid = (bdata['outcome']==bdata.labels['outcome']['correct'])|(bdata['outcome']==bdata.labels['outcome']['error'])
                    correct = bdata['outcome']==bdata.labels['outcome']['correct']

                    ####### Implemented trialLimit constraint to exclude blocks with few trials at the end of a behav session 
                    if(not len(trialLimit)):
                        validTrials = np.ones(len(correct),dtype=bool)
                    else:
                        validTrials = np.zeros(len(correct),dtype=bool)
                        validTrials[trialLimit[0]:trialLimit[1]] = 1

                    correctRightward = rightward & correct & validTrials
                    correctLeftward = leftward & correct & validTrials

                    modIDict[behavSession] = np.zeros([clusNum*numTetrodes]) #0 being no modIndex
                    modSigDict[behavSession] = np.ones([clusNum*numTetrodes]) #1 being no significance test

                # -- Load Spike Data From Certain Cluster --
                spkData = ephyscore.CellData(oneCell)
                spkTimeStamps = spkData.spikes.timestamps

                clusterNumber = (oneCell.tetrode-1)*clusNum+(oneCell.cluster-1)

                trialsEachCond = [correctRightward,correctLeftward]

                (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                    spikesanalysis.eventlocked_spiketimes(spkTimeStamps,EventOnsetTimes,timeRange)
                print len(spikeTimesFromEventOnset)

                spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange)

                spikeCountEachTrial = spikeCountMat.flatten()
                spikeAvgLeftward = sum(spikeCountEachTrial[correctLeftward])/float(sum(correctLeftward))
                spikeAvgRightward = sum(spikeCountEachTrial[correctRightward])/float(sum(correctRightward))
                print 'cluster', clusterNumber, spikeAvgRightward, spikeAvgLeftward

                if ((spikeAvgRightward + spikeAvgLeftward) == 0):
                    modIDict[behavSession][clusterNumber]=0.0
                    modSigDict[behavSession][clusterNumber]=1.0
                else:
                    modIDict[behavSession][clusterNumber]=((spikeAvgRightward - spikeAvgLeftward)/(spikeAvgRightward + spikeAvgLeftward))  
                    modSig = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange,trialsEachCond)
                    modSigDict[behavSession][clusterNumber]=modSig[1]
                    print modIDict[behavSession][clusterNumber],modSigDict[behavSession][clusterNumber]

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
        modI_file.write("Behavior Session:%s\n" % bSession)
        for modInd in modIDict[bSession]:
            modI_file.write("%s," % modInd)
        modI_file.write("\n")
        modSig_file.write("Behavior Session:%s\n" % bSession)
        for modSig in modSigDict[bSession]:
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


