'''
Given an allcells file, calculate and write ISI violation (ISI<2msec) percentage to a file.
LG 20160328
'''

from jaratoolbox import settings_2 as settings
from jaratoolbox import loadopenephys
import numpy as np
import os
from jaratoolbox import spikesorting
reload(spikesorting)
from jaratoolbox import loadbehavior
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
import matplotlib.pyplot as plt
import sys
import importlib
import codecs

mouseNameList = sys.argv[1:]

ISIcutoff = 0.002 #2msec, ISI unit is the same as Timestamps, in sec
clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes
SAMPLING_RATE=30000.0
#soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
ephysRootDir = settings.EPHYS_PATH

for mouseName in mouseNameList:
    allcellsFileName = 'allcells_'+mouseName
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)

    outputDir = '/home/languo/data/ephys/'+mouseName
    nameOfFile = 'ISI_Violations_'+mouseName
    finalOutputDir = outputDir+'/'+mouseName+'_stats'
    if not os.path.exists(finalOutputDir):
        os.mkdir(finalOutputDir)

    numOfCells = len(allcells.cellDB)

    behavSession = ''
    ephysSession = ''
    tetrodeID = ''


    class nestedDict(dict):#This is to create maxZDict
        def __getitem__(self, item):
            try:
                return super(nestedDict, self).__getitem__(item)
            except KeyError:
                value = self[item] = type(self)()
                return value


    ISIDict = nestedDict()
    #ZscoreArray = np.array([])
    ISIList = [] #List of behavior sessions that already have maxZ values calculated

    try:
        text_file = open('%s/%s.txt' % (finalOutputDir,nameOfFile), 'r+') #open a text file to read and write in
        behavName = ''
        for line in text_file:
            if line.startswith(codecs.BOM_UTF8):
                line = line[3:]
            behavLine = line.split(':')
            freqLine = line.split()
            if (behavLine[0] == 'Behavior Session'):
                behavName = behavLine[1][:-1]
                ISIList.append(behavName)            

    except:
        text_file = open('%s/%s.txt' % (finalOutputDir,nameOfFile), 'w') #open a text file to read and write in

    badSessionList = []#Makes sure sessions that crash don't get ZValues printed

    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]
        quality = oneCell.quality
        tetrode = oneCell.tetrode
        cluster = oneCell.cluster

        if (oneCell.behavSession in ISIList): #checks to make sure the ISI violation value is not recalculated
            continue
        if behavSession!=oneCell.behavSession:
            behavSession=oneCell.behavSession
            ISIDict[behavSession] = np.ones([clusNum*numTetrodes]) #initialize ISIDict for each behavior session once; ISI violation fraction of bad cells are set to 1(maximal)
        if quality ==1 or quality ==6:
            try:
                #if (behavSession != oneCell.behavSession):

                subject = oneCell.animalName
                #behavSession = oneCell.behavSession
                ephysSession = oneCell.ephysSession
                ephysRoot = os.path.join(ephysRootDir,subject)
                clusterNumber = (tetrode-1)*clusNum+(cluster-1)
                print oneCell.behavSession

                spkData = ephyscore.CellData(oneCell)
                spkTimeStamps = spkData.spikes.timestamps

                ISI = np.diff(spkTimeStamps)

                if np.any(ISI<0):
                    raise 'Times of events are not ordered (or there is at least one repeated).'
                if len(ISI)==0:  # Hack in case there is only one spike
                    ISI = np.array(10)

                ISIVioBool = ISI<ISIcutoff #ISI smaller than 2msec

                fractionViolation = np.mean(ISIVioBool) 
                ISIDict[behavSession][clusterNumber] = fractionViolation

                print 'ISI Violation less than ',ISIcutoff,' is ',fractionViolation

            except:
                #print "error with session "+oneCell.behavSession
                if (oneCell.behavSession not in badSessionList):
                    badSessionList.append(oneCell.behavSession)

        else:
            continue

    bSessionList = []
    for bSession in ISIDict:
        if (bSession not in badSessionList):
            bSessionList.append(bSession)

    bSessionList.sort()
    for bSession in bSessionList:
        if bSession not in ISIList:
            text_file.write("Behavior Session:%s\n" %bSession)
            for ISIfraction in ISIDict[bSession]:
                text_file.write("%s," %ISIfraction)
            text_file.write("\n")
    text_file.close()

    print 'error with sessions: '
    for badSes in badSessionList:
        print badSes
    print 'finished ISI violation check for', subject
