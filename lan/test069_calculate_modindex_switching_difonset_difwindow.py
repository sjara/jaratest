'''
Lan Guo 20161122
Script to calculate modulation index for the switching task for all cells in animals recorded during the switching 2afc task. 
Modulation index is calculated by comparing spike counts in a given window for trials in the high-block versus trials in the low-block. Only using correct trials; only calculate mod index for middle frequency. 
Modulation direction is a rough estimate of whether the cells activity goes up and down in a block-wise manner in a session; can potentially rule out cells whose activity consistently decrease or increase throughout the session.
Can choose different alignment options (sound, center-out, side-in) and calculate Mod Index for different time windows with aligned spikes.
Output is a pandas series
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


# -- Usage: run test069 with alignment, start, and end of count time range(3 separate arguments) -- #
alignment = sys.argv[1] #the first argument is alignment, choices are 'sound', 'center-out' and 'side-in'
if sys.argv[2]=='0':
    countTimeRange = [int(sys.argv[2]),float(sys.argv[3])]
elif sys.argv[3]=='0':
    countTimeRange = [float(sys.argv[2]),int(sys.argv[3])]
else:
    countTimeRange = [float(sys.argv[2]),float(sys.argv[3])]

SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.020 # Size of each bin in histogram in secondsfor mouseName in mouseNameList:
ephysRootDir = '/home/languo/data/jarastorephys' #All swiching mice are on jarastore

mouseNameList = [] #These are all the switching mice we recorded from

for mouseName in mouseNameList:
    allcellsFileName = 'allcells_'+mouseName+'_quality'
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)
    
    #from jaratest.lan.Allcells import allcellsFileName as allcells
    subject = allcells.cellDB[0].animalName
    ephysRootDir = settings.EPHYS_PATH
    outputDir = '/home/languo/data/ephys/'+mouseName
 
    # Calculate count time range(window)
    window = str(countTimeRange[0])+'to'+str(countTimeRange[1])+'sec_window_'
    
    #nameOfmodSFile = 'modSig_'+alignment+'_'+window+mouseName
    #nameOfmodIFile = 'modIndex_'+alignment+'_'+window+mouseName
    behavSession = ''
    numOfCells = len(allcells.cellDB)
    for cell in range(numOfCells):
        if (behavSession != oneCell.behavSession):
        subject = oneCell.animalName
        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        ephysRoot = os.path.join(ephysRootDir,subject)
        # -- Load Behavior Data --
        behaviorFilename = loadbehavior.path_to_behavior_data(subject,paradigm,behavSession)
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
