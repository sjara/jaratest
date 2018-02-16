'''
Lan Guo 20170323
OLD CELLDB.
Script to calculate modulation index for the reward change task for all cells in an animal.
Modulation index is calculated by comparing spike counts in a given window and alignment for trials with more reward on either the left or the right port. Use ONLY correct trials; only calculate mod index for 2 middle frequencies. 
Can choose different alignment options (sound, center-out, side-in) and calculate Mod Index for different time windows with aligned spikes.
Output is a pandas DataFrame.
'''

import time
zeroTime = time.time()

import numpy as np
import itertools
import sys, os
import importlib
import pandas as pd
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratest.nick.database import dataloader_v2 as dataloader
#from jaratest.lan import test055_load_n_plot_billy_data_one_cell as loader
#reload(loader)
  
# -- Global variables -- #
mouseNameList = ['adap005','adap012','adap013','adap015','adap017','gosi001','gosi004','gosi008','gosi010','adap067','adap071'] 
SAMPLING_RATE = 30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial    
processedDate = time.strftime("%d_%m_%Y")

dbKey = 'reward_change'

timeRange = [-0.5,0.5] # In seconds. Time range for to calculate spikeTimesFromEventOnset, this time window has to span all the possible count time ranges for generating spike count matrix

recalculate = False
CASE = 3
##############################################################

if CASE == 1:
    for mouseName in mouseNameList:
        #-- Calculate modulation index and significance with different onset and time window --#
        newTime=time.time(); print 'Elapsed time: {0:0.2f}  AFTER IMPORT'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER


        # -- Define the alignment and countTimeRange windows to use for calculating modulation -- #
        #allAlignments = ['sound','center-out', 'side-in'] #the first argument is alignment, choices are 'sound', 'center-out' and 'side-in'
        allAlignments = ['side-in']
        #allCountTimeRanges = ([0,0.1],[-0.1,0])
        allCountTimeRanges = ([-0.3,-0.2])
        # Generate conditions for calculating modulation in by taking all possible combinations from all alignments and countTimeRanges
        #conditions = list(itertools.product(allAlignments,allCountTimeRanges))
        conditions = [('side-in',[-0.3,0])]
        modulationDfAllMice = pd.DataFrame()

        #for mouseName in mouseNameList:
        databaseFullPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(mouseName))
        outFilename = '/var/tmp/{}_reward_change_modulation_{}.h5'.format(mouseName,processedDate)
        if os.path.isfile(outFilename):
            print 'Analysis for this mouse was saved before.'
            processed = pd.read_hdf(outFilename, key='reward_change')
            processedSessions = np.unique(processed['date'])
        else:
            processed = pd.DataFrame({'date':[]})
            processedSessions = []
        modulationDict = {'subject': [],
                          'date': [],
                          'tetrode': [],
                          'cluster': []}
        '''
        for (alignment, countTimeRange) in conditions:

            # Make names for count time range and alignment for labeling columns in output df
            window = str(countTimeRange[0])+'-'+str(countTimeRange[1])+'s_'+alignment
            modulationDict.update({'modInd_'+window:[],
                                   'modSig_'+window: []})
        '''
        #allcellsFileName = 'allcells_'+mouseName+'_quality'
        cellDb = pd.read_hdf(databaseFullPath, key=dbKey)
        #sys.path.append(settings.ALLCELLS_PATH)
        #allcells = importlib.import_module(allcellsFileName)
        #reload(allcells)

        newTime=time.time(); print 'Elapsed time: {0:0.2f}  ALLCELLS'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER

        # Process each mouse in chunks
        chunkSize = 20
        #chunks = [allcells.cellDB[ind:ind+chunkSize] for ind in range(0, len(allcells.cellDB), chunkSize)]
        chunks = [cellDb.iloc[ind:ind+chunkSize] for ind in range(0, len(cellDb), chunkSize)]

        for chunk in chunks:

            modulationDict = {'subject': [],
                              'date': [],
                              'tetrode': [],
                              'cluster': []}

            # Do this for each frequency
            for (alignment, countTimeRange) in conditions:
                # Make names for count time range and alignment for labeling columns in output df
                window = str(countTimeRange[0])+'-'+str(countTimeRange[1])+'s_'+alignment

                modulationDict.update({'modIndLow_'+window: [],
                                       'modSigLow_'+window: [],
                                       'modIndHigh_'+window: [],
                                       'modSigHigh_'+window: []})

            for ind,cell in chunk.iterrows():
                if len(processed):
                    processedThisSes = processed[processed['date']==cell.date]
                else:
                    processedThisSes = pd.DataFrame({'tetrode':[],'cluster':[]})
                if (cell.date in processedSessions) & (cell.tetrode in processedThisSes['tetrode']) & (cell.cluster in processedThisSes['cluster']):
                    print 'This cell has been checked for modulation.'
                    continue
                else:
                    loader = dataloader.DataLoader(cell['subject'])
                    sessiontype = 'behavior'  #2afc behavior
                    session = cell['ephys'][cell['sessiontype'].index(sessiontype)]
                    behavFile = cell['behavior'][cell['sessiontype'].index(sessiontype)]
                    eventData = loader.get_session_events(session)
                    try:
                        spikeData = loader.get_session_spikes(session, int(cell['tetrode']), cluster=int(cell['cluster']))
                    except AttributeError:
                        spikeData = (0, 0)
                        modulationDict['subject'].append(cell.subject)
                        modulationDict['date'].append(cell.date)
                        modulationDict['tetrode'].append(cell.tetrode)
                        modulationDict['cluster'].append(cell.cluster)
                        for key in modulationDict.keys():
                            if 'modInd' in key:
                                modulationDict[key].append(0.0)
                            elif 'modSig' in key:
                                modulationDict[key].append(1.0)

                        continue
                    spkTimeStamps = spikeData.timestamps
                    bdata = loader.get_session_behavior(behavFile)

                    soundOnsetTimeBehav = bdata['timeTarget']
                    newTime=time.time(); print 'Elapsed time: {0:0.2f} Loaded behavior and events'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER

                    ######check if ephys and behav miss-aligned, if so, remove skipped trials####
                    eventTimes = eventData.timestamps
                    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
                    soundOnsetTimeEphys = eventTimes[soundOnsetEvents]
                    # Find missing trials
                    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)

                    # Remove missing trials,all fields of bdata's results are modified after this
                    bdata.remove_trials(missingTrials) #This modifies bdata in place

                    soundOnsetTimeBehavNew = bdata['timeTarget'] #This is after removing trials from behav
                    if len(soundOnsetTimeBehavNew) != len(soundOnsetTimeEphys):
                        # if for some reason cannot make behav and ephys have same amount of trials, skip this cell
                        print 'Session {} behav and ephys length did not match, unknown error.'.format(cell.date)
                        modulationDict['subject'].append(cell.subject)
                        modulationDict['date'].append(cell.date)
                        modulationDict['tetrode'].append(cell.tetrode)
                        modulationDict['cluster'].append(cell.cluster) 
                        for key in modulationDict.keys():
                            if 'modInd' in key:
                                modulationDict[key].append(0.0)
                            elif 'modSig' in key:
                                modulationDict[key].append(1.0)

                        continue
                    newTime=time.time(); print 'Elapsed time: {0:0.2f} Removed missing trials'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER

                    currentBlock = bdata['currentBlock']
                    blockTypes = [bdata.labels['currentBlock']['same_reward'],bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
                    trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes) #trialsEachType is an array of dimension nTrials*nblockTypes where boolean vector (in a column) indicates which trials are in each type of block
                    #valid = (bdata['outcome']==bdata.labels['outcome']['correct'])|(bdata['outcome']==bdata.labels['outcome']['error'])
                    correct = bdata['outcome']==bdata.labels['outcome']['correct']

                    if (not sum(trialsEachType[:,1])) or (not sum(trialsEachType[:,2])): #This means there's no change in reward for this session
                        print 'Session {} has no change in reward.'.format(cell.date)
                        modulationDict['subject'].append(cell.subject)
                        modulationDict['date'].append(cell.date)
                        modulationDict['tetrode'].append(cell.tetrode)
                        modulationDict['cluster'].append(cell.cluster) 
                        for key in modulationDict.keys():
                            if 'modInd' in key:
                                modulationDict[key].append(0.0)
                            elif 'modSig' in key:
                                modulationDict[key].append(1.0)

                        continue

                    #correctRightward = rightward & correct
                    #correctLeftward = leftward & correct
                    possibleFreq = np.unique(bdata['targetFrequency'])
                    numFreqs = len(possibleFreq)
                    if numFreqs != 2:
                        print 'Warning: There are more than 2 frequencies used in behavior session. Calculation of modulation index not complete (only calculated for the lowest and highest freqs)!'
                    lowFreq = bdata['targetFrequency'] == possibleFreq[0]
                    highFreq = bdata['targetFrequency'] == possibleFreq[-1]

                    modulationDict['subject'].append(cell.subject)
                    modulationDict['date'].append(cell.date)
                    modulationDict['tetrode'].append(cell.tetrode)
                    modulationDict['cluster'].append(cell.cluster)

                    for (alignment, countTimeRange) in conditions:
                        # Make names for count time range and alignment for labeling columns in output df
                        window = str(countTimeRange[0])+'-'+str(countTimeRange[1])+'s_'+alignment
                        # -- Calculate event onset time based on what events to align spike data to -- #
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
                        #print len(EventOnsetTimes)

                        outputDir = '/var/tmp/processed_data'
                        outputFile = 'eventlocked_{0}_{1}_T{2}c{3}_{4}.npz'.format(cell.subject, cell.date, cell.tetrode, cell.cluster, alignment)
                        outputFullPath = os.path.join(outputDir,outputFile)
                        if os.path.isfile(outputFullPath) and not recalculate:
                            evlockdata = np.load(outputFullPath)
                            spikeTimesFromEventOnset = evlockdata['spikeTimesFromEventOnset']
                            trialIndexForEachSpike = evlockdata['trialIndexForEachSpike']
                            indexLimitsEachTrial = evlockdata['indexLimitsEachTrial']
                            timeRange = evlockdata['timeRange']

                            newTime=time.time(); print 'Elapsed time: {0:0.2f}  LOADED EVLOCKED DATA'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER

                        else:
                            newTime=time.time(); print 'Elapsed time: {0:0.2f}  LOADED EPHYS/BEHAV one cell'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER

                            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                                spikesanalysis.eventlocked_spiketimes(spkTimeStamps,EventOnsetTimes,timeRange)

                            #---- Save intermediate results somewhere, next time can just load it ----
                            np.savez(outputFullPath, spikeTimesFromEventOnset=spikeTimesFromEventOnset,
                                     trialIndexForEachSpike=trialIndexForEachSpike,
                                     indexLimitsEachTrial=indexLimitsEachTrial, timeRange=timeRange, alignment=alignment)
                            print 'Saved event-locked data to {0}'.format(outputFullPath)
                            newTime=time.time(); print 'Elapsed time: {0:0.2f}  Calculated EVLOCKED DATA'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER

                        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange)  #spike counts in the window of interest for modulation
                        spikeCountEachTrial = spikeCountMat.flatten() #spikeCountMat contains num of spikes in countTimeRange, each column is each trial, only one row because only given one time bin(countTimeRange)

                        freqLabels = ['Low','High']
                        for indf,freq in enumerate([lowFreq, highFreq]):
                            trialsMoreLeft = trialsEachType[:,1] & freq & correct 
                            trialsMoreRight = trialsEachType[:,2] & freq & correct 
                            trialsEachCond = [trialsMoreRight,trialsMoreLeft]

                            # -- Calculate modulation index and significance p value -- #
                            spikeAvgRight = np.average(spikeCountEachTrial[trialsMoreRight])
                            spikeAvgLeft = np.average(spikeCountEachTrial[trialsMoreLeft])
                            if ((spikeAvgRight + spikeAvgLeft) == 0):
                                modIndex = 0.0
                                modSig = 1.0
                            else:
                                modSig = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange,trialsEachCond)[1]
                                modIndex = (spikeAvgRight - spikeAvgLeft)/(spikeAvgRight + spikeAvgLeft)
                            newTime=time.time(); print 'Elapsed time: {0:0.2f}  Calculated MOD INDEX & SIG'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER
                            modulationDict['modInd{}_'.format(freqLabels[indf])+window].append(modIndex) 
                            modulationDict['modSig{}_'.format(freqLabels[indf])+window].append(modSig)


            # Open the hdf file for appending data
            #outFilename = '/var/tmp/{}_reward_change_modulation.h5'.format(mouseName)
            outFile = pd.HDFStore(outFilename, 'a')

            modulationDfThisChunk=pd.DataFrame(modulationDict)    
            modulationDfThisChunk.sort_values(['date','tetrode','cluster'],ascending=True,inplace=True)
            #modulationDfAllMice = pd.concat((modulationDfAllMice,modulationDfThisMouse), ignore_index=True)
            #modulationDfThisMouse.to_hdf('/home/languo/data/ephys/reward_change_summary_stats/{}_reward_change_modulation.h5'.format(cell.subject),key='reward_change')
            #modulationDfThisMouse.to_hdf('/var/tmp/{}_reward_change_modulation.h5'.format(cell.subject),key='reward_change')
            outFile.append('reward_change',modulationDfThisChunk, data_columns=True, index=True)
            outFile.close()
            newTime=time.time(); print 'Elapsed time: {0:0.2f} WROTE TO OUTFILE'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER

        #modulationDfAllMice.to_hdf('/home/languo/data/ephys/reward_change_summary_stats/all_mice_reward_change_modulation.h5',key='mod_swiching')

'''
if CASE == 2:
    # -- Add script field -- #
    import os
    import pandas as pd

    #mouseName = 'gosi008'
    outFilename = '/var/tmp/{}_reward_change_modulation.h5'.format(mouseName)
    #processedDir = '/home/languo/data/ephys/reward_change_summary_stats/newMod/'
    #for file in os.listdir(processedDir):
    modulationDf = pd.read_hdf(outFilename, key='reward_change')
    scriptFullPath = os.path.realpath(__file__)
    modulationDf['script'] = scriptFullPath
    modulationDf.drop_duplicates(inplace=True)
    modulationDf.to_hdf(outFilename, key='reward_change')
'''

if CASE == 3:
    # -- Merge newly calculated modulation index from dif windows with all cells all measures --#
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    for mouseName in mouseNameList:
        #mouseName = 'gosi008'        
        databaseFullPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(mouseName))
        #outFilename = '/var/tmp/{}_reward_change_modulation_{}.h5'.format(mouseName, processedDate)
        outFilePath = '/var/tmp/'
        outFilenames = [os.path.join(outFilePath,filename) for filename in os.listdir(outFilePath) if mouseName in filename]
        
        dfThisMouse = pd.read_hdf(databaseFullPath,key='reward_change')
        # -- replacing certain columns -- #
        #colsToDrop = [col for col in dfThisMouse.columns if '-0.2-0s' in col]
        #dfThisMouse = dfThisMouse.drop(columns=colsToDrop)
        #################################
        dfs = [dfThisMouse]
        #allMiceDfs = []
        #for mouseName in np.unique(dfAllMeasures['subject']):
        #dfThisMouse = dfAllMeasures.loc[dfAllMeasures['subject'] == mouseName].reset_index()
        for outFilename in outFilenames:    
            dfModThisMouse = pd.read_hdf(outFilename, key='reward_change')
            dfs.append(dfModThisMouse)

        dfAllThisMouse = reduce(lambda left,right: pd.merge(left,right,on=['subject','date','tetrode','cluster'],how='inner'), dfs)
        dfAllThisMouse.drop_duplicates(['subject','date','tetrode','cluster','depth'],inplace=True)
        if 'level_0' in dfAllThisMouse.columns:
            dfAllThisMouse = dfAllThisMouse.drop(columns=['level_0'])
        dfAllThisMouse.reset_index(inplace=True)
        dfAllThisMouse.drop('level_0', 1, inplace=True)
        dfAllThisMouse.to_hdf(databaseFullPath, key='reward_change')
        
        #when saving to hdf, using (format='table',data_columns=True) is slower but enable on disk queries

