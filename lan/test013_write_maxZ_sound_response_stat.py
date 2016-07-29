'''
calculates max Z value for all frequencies (only uses valid trails in calculations) for all cells with good quality (score of 1 or 6).
Lan Guo, modified from script by Santiago Jaramillo and Billy Walker
Implemented: using santiago's methods to remove missing trials from behavior when ephys has skipped trials. -LG20160309
'''

from jaratoolbox import loadbehavior
from jaratoolbox import settings_2 as settings
reload (settings)
from jaratoolbox import ephyscore
import os
import numpy as np
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import celldatabase as cellDB
import matplotlib.pyplot as plt
import sys
import importlib
import re

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)
reload(allcells)

SAMPLING_RATE=30000.0

outputDir = '/home/languo/data/ephys/'+mouseName
nameOfFile = 'maxZVal_'+mouseName
finalOutputDir = outputDir+'/'+mouseName+'_stats'
if not os.path.exists(finalOutputDir):
    os.mkdir(finalOutputDir)

soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.010 # Size of each bin in histogram in seconds

timeRange = [-0.3,0.7] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes

ephysRootDir = settings.EPHYS_PATH

experimenter = 'lan'
#experimenter = 'billy'
paradigm = '2afc'

Zthreshold = 3

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
subject = allcells.cellDB[0].animalName
behavSession = ''
ephysSession = ''
tetrodeID = ''

################################################################################################
baseRange = [-0.050,-0.025]              # Baseline range (in seconds)
binTime = baseRange[1]-baseRange[0]         # Time-bin size
responseTimeRange = [-0.1,0.1]       #Time range to calculate z value for (should be divisible by binTime
responseTime = responseTimeRange[1]-responseTimeRange[0]
binEdges = np.arange(0,5)*binTime  # Edges of bins to calculate response (in seconds)
################################################################################################

class nestedDict(dict):#This is to create maxZDict
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value


maxZDict = nestedDict()
#ZscoreArray = np.array([])
maxZList = [] #List of behavior sessions that already have maxZ values calculated

try:
    text_file = open('%s/%s.txt' % (finalOutputDir,nameOfFile), 'r+') #open a text file to read and write in
    #text_file.readline()
    behavName = ''
    for line in text_file:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        behavLine = line.split(':')
        freqLine = line.split()
        if (behavLine[0] == 'Behavior Session'):
            behavName = behavLine[1][:-1]
            maxZList.append(behavName)
            

except:
    text_file = open('%s/%s.txt' % (finalOutputDir,nameOfFile), 'w') #open a text file to read and write in

badSessionList = []#Makes sure sessions that crash don't get ZValues printed

for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]
    tetrode = oneCell.tetrode
    cluster = oneCell.cluster
    quality = oneCell.quality

    if (oneCell.behavSession in maxZList): #checks to make sure the maxZ value is not recalculated
        continue
    if quality ==1 or quality ==6:
        try:
            if (behavSession != oneCell.behavSession):

                subject = oneCell.animalName
                behavSession = oneCell.behavSession
                ephysSession = oneCell.ephysSession
                ephysRoot = os.path.join(ephysRootDir,subject)

                print oneCell.behavSession

                # -- Load Behavior Data --
                behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
                bdata = loadbehavior.BehaviorData(behaviorFilename)
                numberOfTrials = len(bdata['choice'])
                print "number of behavior trials ",numberOfTrials

                # -- Load event data and convert event timestamps to ms --
                ephysDir = os.path.join(ephysRoot, ephysSession)
                eventFilename=os.path.join(ephysDir, 'all_channels.events')
                events = loadopenephys.Events(eventFilename) # Load events data
                eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 

                soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)
                # -- Check to see if ephys has skipped trials, if so remove trials from behav data 
                soundOnsetTimeEphys = eventTimes[soundOnsetEvents]
                soundOnsetTimeBehav = bdata['timeTarget']

                # Find missing trials
                missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
                # Remove missing trials
                bdata.remove_trials(missingTrials)
                soundOnsetTimeBehav = bdata['timeTarget']
                nTrialsBehav = len(soundOnsetTimeBehav)
                nTrialsEphys = len(soundOnsetTimeEphys)
                print 'N (behav) = {0}'.format(nTrialsBehav)
                print 'N (ephys) = {0}'.format(nTrialsEphys)

                eventOnsetTimes = eventTimes[soundOnsetEvents]
                #print "number of ephys trials ",len(eventOnsetTimes)

                possibleFreq = np.unique(bdata['targetFrequency'])
                numberOfFrequencies = len(possibleFreq)
                for possFreq in possibleFreq:
                    maxZDict[behavSession][possFreq] = np.zeros([clusNum*numTetrodes]) #initialize a list for storing maxZ with max length, only good clusters will be filled in so the rest of the entries will be zeros.
                #maxZArray = np.empty([clusNum*numTetrodes])

                validTrials = ((bdata['outcome'] == bdata.labels['outcome']['correct']) | (bdata['outcome'] == bdata.labels['outcome']['error']))

            # -- Load Spike Data From Certain Cluster --
            for Frequency in range(numberOfFrequencies):
                Freq = possibleFreq[Frequency]
                oneFreqTrials = bdata['targetFrequency'] == Freq  #only use a certain frequency
                trialsToUse = (oneFreqTrials & validTrials)

                oneFreqEventOnsetTimes = eventOnsetTimes[trialsToUse] #Choose only the trials with this frequency


                spkData = ephyscore.CellData(oneCell)
                spkTimeStamps = spkData.spikes.timestamps

                (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                    spikesanalysis.eventlocked_spiketimes(spkTimeStamps,oneFreqEventOnsetTimes,timeRange)


                [zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange,binEdges) #computes z score for each bin. zStat is array of z scores. maxZ is maximum value of z in timeRange

                clusterNumber = (tetrode-1)*clusNum+(cluster-1)
                #maxZArray[clusterNumber].append(maxZ)
                maxZDict[behavSession][Freq][clusterNumber] = maxZ
                #if abs(maxZ)=<Zthreshold & onecell.soundResponsive!=True:
                    #oneCell.soundResponsive=False
                #elif abs(maxZ)>Zthreshold:
                    #oneCell.soundResponsive=True

                #ZscoreArray[:,Frequency,cellID] = zStat
        except:
            #print "error with session "+oneCell.behavSession
            if (oneCell.behavSession not in badSessionList):
                badSessionList.append(oneCell.behavSession)

    else:
        continue

bSessionList = []
for bSession in maxZDict:
    if (bSession not in badSessionList):
        bSessionList.append(bSession)

bSessionList.sort()
for bSession in bSessionList:
    text_file.write("Behavior Session:%s" % bSession)
    for freq in maxZDict[bSession]:
        text_file.write("\n%s " % freq)
        for ZVal in maxZDict[bSession][freq]:
            text_file.write("%s," % ZVal)
    text_file.write("\n")

text_file.close()
print 'error with sessions: '
for badSes in badSessionList:
    print badSes
print 'finished max Z value check'
