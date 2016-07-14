'''
ephysBehaveDataAlignmentCheck.py
Checks if the Behavior data and Ephys data is aligned
author: Billy Walker
'''



from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
from jaratoolbox import settings
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import importlib


mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

SAMPLING_RATE=30000.0

outputDir = '/home/billywalker/data/ephys'
nameOfFile = 'dataAlignmentCheck'

subject = allcells.cellDB[0].animalName
behavSession = ''
ephysSession = ''

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'

ephysRoot = ephysRootDir+mouseName+'/'
eventID = 0

finalOutputDir = outputDir+'/'+subject+'_processed'
alignedCheckList = []

try:
    text_file = open("%s/%s.txt" % (finalOutputDir,nameOfFile), "r+") #open a text file to read and write in
    behavName = ''
    for line in text_file:
        behavLine = line.split(' ')
        behavName = behavLine[0]
        alignedCheckList.append(behavName)
except:
    text_file = open("%s/%s.txt" % (finalOutputDir,nameOfFile), "w") #open a text file to read and write in

thresDiff = 0.2 #The threshold in difference of times in seconds to flag a bad trial

for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]
    if (behavSession != oneCell.behavSession):


        subject = oneCell.animalName
        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        ephysRoot = os.path.join(ephysRootDir,subject)

        if (behavSession in alignedCheckList): #if it is already in the list, dont add it again
            continue

        # -- Load Behavior Data --
        behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
        bdata = loadbehavior.BehaviorData(behaviorFilename)
        numberOfTrials = len(bdata['choice'])

#experimenter = 'santiago'
#paradigm = '2afc'


        # -- Load event data and convert event timestamps to ms --
        ephysDir = os.path.join(ephysRoot, ephysSession)
        eventFilename=os.path.join(ephysDir, 'all_channels.events')
        events = loadopenephys.Events(eventFilename) # Load events data
        eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 
        multipleEventOnset=np.array(events.eventID)  #loads the onset times of all events (matches up with eventID to say if event 1 went on (1) or off (0)
        eventChannel = np.array(events.eventChannel) #loads the ID of the channel of the event. For example, 0 is sound event, 1 is trial event, 2 ...


        # -- Only use event onset times of one event --
        oneEvent = eventChannel==eventID #This picks out which channel you care about if there is more that one event
        eventOnset = multipleEventOnset*oneEvent #This keeps the correct size of the array to match eventTimes and picks out the onset of the channel you want
        eventOnsetTimes = eventTimes[eventOnset == 1] #This gives only the times of the onset of the channel you want

        behavTimes = np.empty(numberOfTrials)
        prevTimeCenter = bdata['timeCenterIn'][0]
        for trial,timeCenter in enumerate(bdata['timeCenterIn']):
            behavTimes[trial] = timeCenter - prevTimeCenter
            prevTimeCenter = timeCenter

        ephysTimes = np.empty(np.sum(eventOnset))
        prevTime = eventOnsetTimes[0]
        for etrial,timeSound in enumerate(eventOnsetTimes):
            ephysTimes[etrial] = timeSound - prevTime
            prevTime = timeSound

        numberToPlot = min(numberOfTrials,np.sum(eventOnset))
        differenceTimes = np.empty(numberToPlot)
        firstSkipped = False
        badTrial = 0
        for dtrial in range(0,numberToPlot):
            differenceTimes[dtrial] = ephysTimes[dtrial]-behavTimes[dtrial]
            if (abs(differenceTimes[dtrial])>thresDiff) and not firstSkipped:
                badTrial = dtrial
                firstSkipped = True

        '''
        #This will find the time differences if we throw out the skipped trial
        differenceTimesSkipped = np.empty(numberToPlot)
        for dstrial in range(0,badTrial):
            differenceTimesSkipped[dstrial] = ephysTimes[dstrial]-behavTimes[dstrial]
        for dstrial in range(badTrial,numberToPlot):
            differenceTimesSkipped[dstrial] = ephysTimes[dstrial]-behavTimes[dstrial+1]
        '''

        text_file.write("%s %s\n" % (behavSession, firstSkipped))

        '''
        plt.clf()
        differencePlt = plt.subplot2grid((1,2), (0, 0), colspan=1)
        plt.plot(differenceTimes)
        differenceSkippedPlt = plt.subplot2grid((1,2), (0, 1), colspan=1)
        plt.plot(differenceTimesSkipped)
        plt.show()
        '''
        



#print 'the number of behavior trials is {}'.format(numberOfTrials)
#print 'the number of ephys events trials is {}'.format(np.sum(eventOnset))
#print 'the skipped trial is {}'.format(badTrial)


text_file.close()
print 'finished data alignment check'
