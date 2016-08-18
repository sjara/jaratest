'''
Lan Guo 20160812
Modified from Billy's modIndexCalcSwitching.py
Takes cellDB whose individual cells contain the property 'quality' to mark whether it's a good cell or not.
Finds modulation index for all cells (now not checking cell quality) for ALL frequencies for the psycometric task. Comparing response to one frequency going left versus going right.
Can choose different alignment options (sound, center-out, side-in) and calculate Mod Index for different time windows with aligned spikes. 
Using santiago's methods to remove missing trials from behavior when ephys has skipped trials. 
'''

from jaratoolbox import loadbehavior
from jaratoolbox import settings
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
import codecs

##################-- Usage of this script --################################
# Have to invoke this script with 4 extra system arguments(besides the filename)
 
alignment = sys.argv[1] #the first argument is alignment, choices are 'sound', 'center-out' and 'side-in'

# The second and third sys arguments are the beginning and end of the time window to calculate modulation index in.

if sys.argv[2]=='0':
    countTimeRange = [int(sys.argv[2]),float(sys.argv[3])]
elif sys.argv[3]=='0':
    countTimeRange = [float(sys.argv[2]),int(sys.argv[3])]
else:
    countTimeRange = [float(sys.argv[2]),float(sys.argv[3])]

# The fourth sys argument onwards should be mouse names
mouseNameList = sys.argv[4:] #the fourth argument onwards are the mouse names to tell the script which allcells file to use
#print alignment,countTimeRange,mouseNameList
############################################################################

SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.020 # Size of each bin in histogram in seconds

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes
timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

for mouseName in mouseNameList:
    allcellsFileName = 'allcells_'+mouseName
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)
    #from jaratest.lan.Allcells import allcellsFileName as allcells
    subject = allcells.cellDB[0].animalName
    ephysRootDir = settings.EPHYS_PATH
    outputDir = '/home/languo/data/ephys/'+mouseName
    finalOutputDir = outputDir+'/'+subject+'_stats'
    ###################Choose alignment and time window to calculate mod Index#######################
    #alignment = 'center-out'  #put here alignment choice!!choices are 'sound', 'center-out', 'side-in'.
    #countTimeRange = [0.1,0.2]
    window = str(countTimeRange[0])+'to'+str(countTimeRange[1])+'sec_window_'
    nameOfmodSFile = 'modSig_'+alignment+'_'+window+mouseName
    nameOfmodIFile = 'modIndex_'+alignment+'_'+window+mouseName

    #############################################################################

    '''
    #experimenter param is obsolete -LG 20160812
    if mouseName=='adap015' or mouseName=='adap013' or mouseName=='adap017':
        experimenter = 'billy'
    else:
        experimenter = 'lan'
    '''

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
    
    modI_filename = '%s/%s.txt' % (finalOutputDir,nameOfmodIFile)
    if os.path.isfile(modI_filename):
        modI_file = open(modI_filename, 'r+') #open a text file to read and write in
        behavName = ''
        for line in modI_file:
            if line.startswith(codecs.BOM_UTF8):
                line = line[3:]
            behavLine = line.split(':')
            if (behavLine[0] == 'Behavior Session'):
                behavName = behavLine[1][:-1]
                modIList.append(behavName)
        modI_file.close()
    else:
        modI_file = open(modI_filename, 'w') #when file dosenot exit then create it, but will truncate the existing file

    modS_filename = '%s/%s.txt' % (finalOutputDir,nameOfmodSFile)
    if os.path.isfile(modS_filename):
        modSig_file = open(modS_filename, 'r+') #open a text file to read and write in
        behavName = ''
        for line in modSig_file:
            if line.startswith(codecs.BOM_UTF8):
                line = line[3:]
            behavLine = line.split(':')
            if (behavLine[0] == 'Behavior Session'):
                behavName = behavLine[1][:-1]
                modSList.append(behavName)
        modSig_file.close()
    else:
        modSig_file = open(modS_filename, 'w') #when file dosenot exit then create it, but will truncate the existing file

#########################################################################################
    badSessionList = [] #Makes sure sessions that crash don't get modI values printed
    behavSession = ''
    modIndexArray = []
    modIDict = nestedDict() #stores all the modulation indices
    modSigDict = nestedDict()

    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]

        #if oneCell.quality==1 or oneCell.quality==6: #commented out to calculate modI for all cells

        if (oneCell.behavSession in modIList and oneCell.behavSession in modSList): #checks to make sure the modI value is not recalculated
            continue
        #try:

        if (behavSession != oneCell.behavSession):

            # -- Write modIndex and modSig to file as have finished calculating last session--
            if behavSession != '':
                modI_file = open(modI_filename, 'a')
                modI_file.write("Behavior Session:%s" % behavSession)
                for Freq in modIDict[behavSession]:
                    modI_file.write("\n%s " % Freq)
                    for modInd in modIDict[behavSession][Freq]:
                        modI_file.write("%s," % modInd)
                modI_file.write("\n")
                modI_file.close()
                modSig_file = open(modSig_filename, 'a')
                modSig_file.write("Behavior Session:%s" % behavSession)
                for freq in modSigDict[behavSession]:
                    modSig_file.write("\n%s " % freq) 
                    for modSig in modSigDict[behavSession][freq]:
                        modSig_file.write("%s," % modSig)
                modSig_file.write("\n")
                modI_file.close()
            #Important for data read out: the format of the modI and modSig files are very similar to maxZ files. one line for behav session starting with 'Behavior Session:'; one line for modInd/modSig starting with the frequency followed by space, then modIndex/modSig for each cell separated by ','
            
            # -- Start to process this session --
            subject = oneCell.animalName
            behavSession = oneCell.behavSession
            ephysSession = oneCell.ephysSession
            ephysRoot = os.path.join(ephysRootDir,subject)
            #trialLimit = oneCell.trialLimit #billy's allcells don't have this param

            print behavSession

            # -- Load Behavior Data --
            behaviorFilename = loadbehavior.path_to_behavior_data(subject,paradigm,behavSession) #get rid of experimenter
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



            #######20160324 Implemented trialLimit constraint to exclude blocks with few trials at the end of a behav session 
            #if(not len(trialLimit)):
                #validTrials = np.ones(len(currentBlock),dtype=bool)
            #else:
                #validTrials = np.zeros(len(currentBlock),dtype=bool)
                #validTrials[trialLimit[0]:trialLimit[1]] = 1
            

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

            for possFreq in possibleFreq:
                modIDict[behavSession][possFreq] = np.zeros([clusNum*numTetrodes]) #0 being no modIndex
                modSigDict[behavSession][possFreq] = np.ones([clusNum*numTetrodes]) #1 being no significance test

        # -- Load Spike Data From Certain Cluster --
        spkData = ephyscore.CellData(oneCell)
        spkTimeStamps = spkData.spikes.timestamps

        clusterNumber = (oneCell.tetrode-1)*clusNum+(oneCell.cluster-1)

        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                spikesanalysis.eventlocked_spiketimes(spkTimeStamps,EventOnsetTimes,timeRange)
        #print len(spikeTimesFromEventOnset)

        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange)

        spikeCountEachTrial = spikeCountMat.flatten()

        # -- Calculate modulation index for each frequency presented in task --
        for Freq in possibleFreq:
            oneFreq = targetFreqs == Freq
            trialsToUseRight = rightward & oneFreq
            trialsToUseLeft = leftward & oneFreq
            trialsEachCond = [trialsToUseRight,trialsToUseLeft]

            #print 'behavior ',behavSession,' tetrode ',oneCell.tetrode,' cluster ',oneCell.cluster,'freq',Freq,  

            if ((sum(trialsToUseRight)==0) or (sum(trialsToUseLeft)==0)): #If there are no trials on one side
                modIDict[behavSession][Freq][clusterNumber] = 0.0
                modSigDict[behavSession][Freq][clusterNumber] = 1.0
                continue

            spikeAvgRight = sum(spikeCountEachTrial[trialsToUseRight])/float(sum(trialsToUseRight))
            spikeAvgLeft = sum(spikeCountEachTrial[trialsToUseLeft])/float(sum(trialsToUseLeft))

            #print 'cluster', clusterNumber, spikeAvgMoreReward, spikeAvgLessReward
            if ((spikeAvgRight + spikeAvgLeft) == 0):
                modIDict[behavSession][Freq][clusterNumber] = 0.0
                modSigDict[behavSession][Freq][clusterNumber] = 1.0
            else:
                mod_sig = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange,trialsEachCond)
                modIDict[behavSession][Freq][clusterNumber] =((spikeAvgRight - spikeAvgLeft)/(spikeAvgRight + spikeAvgLeft))
                modSigDict[behavSession][Freq][clusterNumber] = mod_sig[1]


    

        #print modIDict
            #print spikeAvgMoreReward,' ', spikeAvgLessReward, ' ',modIDict[behavSession][Freq][clusterNumber]

        #except:
            #if (oneCell.behavSession not in badSessionList):
                #badSessionList.append(oneCell.behavSession)

        #else:
            #continue
    
    # -- write the last session's modI and modS to file. -- 
    if behavSession != '':
        modI_file=open(modI_filename, 'a')
        modI_file.write("Behavior Session:%s" % behavSession)
        for Freq in modIDict[behavSession]:
            modI_file.write("\n%s " % Freq)
            for modInd in modIDict[behavSession][Freq]:
                modI_file.write("%s," % modInd)
        modI_file.write("\n")
        modI_file.close()
        
        modSig_file = open(modSig_filename, 'a')
        modSig_file.write("Behavior Session:%s" % behavSession)
        for freq in modSigDict[behavSession]:
            modSig_file.write("\n%s " % freq) 
            for modSig in modSigDict[behavSession][freq]:
                modSig_file.write("%s," % modSig)
        modSig_file.write("\n")
        modSig_file.close()
    #########################################################################################

    #print 'error with sessions: '
    #for badSes in badSessionList:
        #print badSes
    print 'finished modI value check'


