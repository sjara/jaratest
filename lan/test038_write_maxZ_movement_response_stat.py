'''
Calculates max Z value for for all cells with good quality (score of 1 or 6) for significant movement-related changes in activity (only uses valid trails in calculations).
*Time window for baseline is -0.050 to -0.025sec before sound-onset(when the mice are stationary in the center hole), time window for moving period is 0.15 to 0.3sec after sound-onset
Lan Guo 20160411 modified from script by Santiago Jaramillo and Billy Walker
Implemented: using santiago's methods to remove missing trials from behavior when ephys has skipped trials. 
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
nameOfFile = 'maxZVal_movement_150to300msAfterSound_'+mouseName
finalOutputDir = outputDir+'/'+mouseName+'_stats'
if not os.path.exists(finalOutputDir):
    os.mkdir(finalOutputDir)

soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.010 # Size of each bin in histogram in seconds

timeRange = [-0.3,0.7] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes

ephysRootDir = settings.EPHYS_PATH

if mouseName=='adap015' or mouseName=='adap013' or mouseName=='adap017':
    experimenter = 'billy'
else:
    experimenter = 'lan'

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
#responseTimeRange = [-0.1,0.1]       
#responseTime = responseTimeRange[1]-responseTimeRange[0]
binEdges = np.arange(6,13)*binTime  # Edges of bins to calculate response (in seconds), 150-300ms after sound-onset
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
        behavLine = line.split(':')
        freqLine = line.split()
        if (behavLine[0] == 'Behavior Session'):
            behavName = behavLine[1][:-1]
            maxZList.append(behavName)
        ###Added this, after maxZ file has been written once, next run will read all the calculated maxZ score and generate histogram
        else:
            maxZDict[behavName][freqLine[0]] = freqLine[1].split(',')[0:-1]

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


                #calculate eventOnsetTimes aligned to sound-onset
                eventOnsetTimes = eventTimes[soundOnsetEvents]
                 
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
                #print len(zStat)

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
    if (bSession not in badSessionList) and (bSession not in maxZList):
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
print 'finished max Z movement value check'


##########################THIS IS TO PLOT HISTOGRAM################################################
binWidth = 1 # Size of each bin in histogram in seconds
maxZBinVec = np.arange(-5,6,binWidth)
binmaxZArray = np.empty(len(maxZBinVec))
#binmaxZNonSig = np.empty(len(maxZBinVec))
maxZ=5
totalSigMaxZ=0
for binInd in range(len(maxZBinVec)-1):
    binTotalmaxZ = 0
    for bSession in maxZList:
        for (freq,maxZScores) in maxZDict[bSession].items():
            for maxZScore in maxZScores:
                if (float(maxZScore)!=0) and (float(maxZScore) >= maxZBinVec[binInd]) and (float(maxZScore) < maxZBinVec[binInd+1]):
                    binTotalmaxZ+=1
    print maxZBinVec[binInd],maxZBinVec[binInd+1], binTotalmaxZ    
    binmaxZArray[binInd] = binTotalmaxZ
    if maxZBinVec[binInd]>=3 or maxZBinVec[binInd+1]<=-3:
        totalSigMaxZ+=binTotalmaxZ

    #binModIndexArrayNonSig[binInd] = binTotalNonSig
#binModIndexArraySig[-1] = 0  #why is this??
#binModIndexArrayNonSig[-1] = 0 #why is this??
#sigNum=int(sum(binModIndexArraySig))
#comparisonNum=len(modIndexArray)
#print 'number of comparisons: ',comparisonNum

totalCellNum=sum(binmaxZArray)
plt.clf() 

plt.bar(maxZBinVec,binmaxZArray,width = binWidth, color = 'b')
#plt.bar(modIndBinVec,binModIndexArrayNonSig,width = binWidth, color = 'g',bottom = binModIndexArraySig)

plt.xlim((-(maxZ+binWidth),maxZ+binWidth))
ylim=plt.ylim()[1]
plt.xlabel('Movement Max Z score')
plt.ylabel('Number of Cells')
plt.text(-0.5*(maxZ+binWidth),0.5*ylim,'Plotting %s cells, %s Z score significant'%(totalCellNum, totalSigMaxZ))
plt.title('Movement max Z score')

plt.gcf().set_size_inches((8.5,11))
figformat = 'png'
filename = 'Movement_maxZ_%s.%s'%(subject,figformat)
fullFileName = os.path.join(finalOutputDir,filename)

print 'saving figure to %s'%fullFileName
plt.gcf().savefig(fullFileName,format=figformat)

plt.show()

