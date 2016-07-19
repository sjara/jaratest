'''
For cells in head-fixed PINP experiments. calculates max Z value for noise burst and laser burst test for all cells with good quality (score of 1 or 6).
Lan Guo 2016-03-30
'''

from jaratoolbox import loadbehavior
from jaratoolbox import settings_2 as settings
reload (settings)
from jaratoolbox import ephyscore
import os
import numpy as np
from jaratoolbox import loadopenephys
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

SAMPLING_RATE=30000.0

outputDir = '/home/languo/data/ephys/'+mouseName
nameOfLaserFile = 'maxZVal_laser_'+mouseName
nameOfSoundFile= 'maxZVal_sound_'+mouseName
finalOutputDir = outputDir+'/'+mouseName+'_stats'
if not os.path.exists(finalOutputDir):
    os.mkdir(finalOutputDir)

laserTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
soundTriggerChannel = 0
binWidth = 0.010 # Size of each bin in histogram in seconds

timeRange = [-0.3,0.7] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

ephysRootDir = settings.EPHYS_PATH

experimenter = 'lan'

Zthreshold = 3

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
subject = allcells.cellDB[0].animalName
behavSession = ''
laserSession = ''
tetrodeID = ''

################################################################################################
baseRange = [-0.050,-0.025]              # Baseline range (in seconds)
binTime = baseRange[1]-baseRange[0]         # Time-bin size
#responseTimeRange = [-0.1,0.1]      
#responseTime = responseTimeRange[1]-responseTimeRange[0]
binEdges = np.arange(0,5)*binTime  # Edges of bins to calculate response (in seconds)
################################################################################################

class nestedDict(dict):#This is to create maxZDict
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value


maxZLaserDict = nestedDict()
maxZSoundDict = nestedDict()
#ZscoreArray = np.array([])
maxZList = [] #List of behavior sessions that already have maxZ values calculated

try:
    lasertext_file = open("%s/%s.txt" % (finalOutputDir,nameOfLaserFile), 'r+') #open a text file to read and write in
    lasertext_file.readline()
    behavName = ''
    for line in lasertext_file:
        behavLine = line.split(':')
        #freqLine = line.split()
        if (behavLine[0] == 'Behavior Session'):
            behavName = behavLine[1][:-1]
            maxZList.append(behavName)
            

except:
    lasertext_file = open("%s/%s.txt" % (finalOutputDir,nameOfLaserFile), 'w') #open a text file to read and write in

try:
    soundtext_file = open("%s/%s.txt" % (finalOutputDir,nameOfSoundFile), 'r+') 
except:
    soundtext_file = open("%s/%s.txt" % (finalOutputDir,nameOfSoundFile), 'w')


badSessionList = []#Makes sure sessions that crash don't get ZValues printed

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 4 #PINP experiments was done with head-stage with 4TTs

for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]
    tetrode = oneCell.tetrode
    cluster = oneCell.cluster
    quality = oneCell.quality
     
    print tetrode,cluster,quality
    #if (oneCell.behavSession in maxZList): #checks to make sure the maxZ value is not recalculated
        #continue
    if quality ==1 or quality ==6:
        try:
            if (behavSession != oneCell.behavSession):

                subject = oneCell.animalName
                behavSession = oneCell.behavSession
                ephysSession = oneCell.ephysSession
                laserSession = oneCell.laserSession
                ephysRoot = os.path.join(ephysRootDir,subject)
                tetrode=oneCell.tetrode
                cluster=oneCell.cluster

                print oneCell.behavSession,tetrode,cluster
                
                # -- Load laser event data and convert event timestamps to ms --
                laserephysDir = os.path.join(ephysRoot, laserSession)
                lasereventFilename=os.path.join(laserephysDir, 'all_channels.events')
                lasereventData = loadopenephys.Events(lasereventFilename) # Load events data
                lasereventTimes=np.array(lasereventData.timestamps)/SAMPLING_RATE 
                laserOnsetEvents = (lasereventData.eventID==1) & (lasereventData.eventChannel==laserTriggerChannel)
                laserOnsetTimes = lasereventTimes[laserOnsetEvents]

                # -- Load sound event data and convert event timestamps to ms --
                soundephysDir = os.path.join(ephysRoot, ephysSession)
                soundeventFilename=os.path.join(soundephysDir, 'all_channels.events')
                soundeventData = loadopenephys.Events(soundeventFilename) # Load events data
                soundeventTimes=np.array(soundeventData.timestamps)/SAMPLING_RATE 
                soundOnsetEvents = (soundeventData.eventID==1) & (soundeventData.eventChannel==soundTriggerChannel)
                soundOnsetTimes = soundeventTimes[soundOnsetEvents]
                print "number of laser trials ",len(laserOnsetTimes),"number of sound trials ",len(soundOnsetTimes)

                maxZLaserDict[behavSession] = np.zeros([clusNum*numTetrodes]) 
                maxZSoundDict[behavSession] = np.zeros([clusNum*numTetrodes])
                # -- Load Spike Data From Certain Cluster --
            soundSpkData = ephyscore.CellData(oneCell) #cannot use this methodfor laser data since it only loads ephys session not laser session
            soundSpkTimeStamps = soundSpkData.spikes.timestamps
            print len(soundSpkTimeStamps),len(soundOnsetTimes)
            laserSpkFullPath = os.path.join(laserephysDir,'Tetrode{0}.spikes'.format(tetrode))
            laserSpkData=loadopenephys.DataSpikes(laserSpkFullPath)
            laserSpkData.timestamps = laserSpkData.timestamps/SAMPLING_RATE
            kkDataDir= os.path.dirname(laserSpkFullPath)+'_kk'
            clusterFilename = 'Tetrode{0}.clu.1'.format(tetrode)
            clusterFullPath = os.path.join(kkDataDir,clusterFilename)
            clusters = np.fromfile(clusterFullPath,dtype='int32',sep=' ')[1:]
            spikesMaskThisCluster = clusters==cluster
            laserSpkTimeStamps = laserSpkData.timestamps[spikesMaskThisCluster]
            print len(laserSpkTimeStamps),len(laserOnsetTimes)

            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                spikesanalysis.eventlocked_spiketimes(laserSpkTimeStamps,laserOnsetTimes,timeRange)
            #print len(spikeTimesFromEventOnset)
            [zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange,binEdges) #computes z score for each bin. zStat is array of z scores. maxZ is maximum value of z in timeRange
            print zStat,maxZ
            ######clusterNumber different because usually named the 4TTs TT3,4,5,6, not starting from 1
            clusterNumber = (tetrode-3)*clusNum+(cluster-1)
            maxZLaserDict[behavSession][clusterNumber] = maxZ
            
            (soundspikeTimesFromEventOnset,soundtrialIndexForEachSpike,soundindexLimitsEachTrial) = \
                spikesanalysis.eventlocked_spiketimes(soundSpkTimeStamps,soundOnsetTimes,timeRange)
            #print len(spikeTimesFromEventOnset)
            [soundzStat,soundpValue,soundmaxZ] = spikesanalysis.response_score(soundspikeTimesFromEventOnset,soundindexLimitsEachTrial,baseRange,binEdges) #computes z score for each bin. zStat is array of z scores. maxZ is maximum value of z in timeRange
            print soundzStat,soundmaxZ
            
            maxZSoundDict[behavSession][clusterNumber] = soundmaxZ
            #ZscoreArray[:,Frequency,cellID] = zStat
        
        except:
            #print "error with session "+oneCell.behavSession
            if (oneCell.behavSession not in badSessionList):
                badSessionList.append(oneCell.behavSession)

    else:
        continue

bSessionList = []
for bSession in maxZLaserDict:
    if (bSession not in badSessionList):
        bSessionList.append(bSession)

bSessionList.sort()
for bSession in bSessionList:
    lasertext_file.write('Behavior Session:%s\n' %bSession)
    #text_file.write("\n")
    for ZVal in maxZLaserDict[bSession]:
        lasertext_file.write("%s," %ZVal)
    lasertext_file.write('\n')
lasertext_file.close()

for bSession in bSessionList:
    soundtext_file.write('Behavior Session:%s\n' %bSession)
    #text_file.write("\n")
    for ZVal in maxZLaserDict[bSession]:
        soundtext_file.write("%s," %ZVal)
    soundtext_file.write('\n')
soundtext_file.close()

print 'error with sessions: '
for badSes in badSessionList:
    print badSes
print 'finished laser response max Z value check'
