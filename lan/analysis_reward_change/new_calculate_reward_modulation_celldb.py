'''
Lan Guo 20180212
UPDATED WITH NEW CELLDB METHODS FOR LOADING DATA
Script to calculate modulation index for the reward change task for all cells in an animal. 
Modulation index is calculated by comparing spike counts in a given window and alignment for trials with more reward on either the left or the right port. Use ONLY correct trials; only calculate mod index for 2 middle frequencies. 
Modulation direction is a rough estimate of whether the cells activity goes up and down in a block-wise manner in a session. NOTE: right now we are only implementing a check for those cells whose firing goes continuously up or down over the blocks of interest; we did not check if the activity actually goes up and down when block switches. Nonetheless this analysis can potentially rule out false positive 'modulated' cells (whose activity consistently decrease or increase throughout the session). Mod direction has to be 1 to be a good modulation.
Can choose different alignment options (sound, center-out, side-in) and calculate Mod Index for different time windows with aligned spikes.
Output is a pandas DataFrame.
'''

import time
zeroTime = time.time()
import argparse
import numpy as np
import itertools
import sys, os
import pandas as pd
from jaratoolbox import settings
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import ephyscore
  
# -- Global variables -- #
#mouseNameList = ['gosi010'] #['adap005','adap012','adap013','adap015','adap017','gosi001','gosi004','gosi008','gosi010','adap067','adap071'] 
soundChannelType = 'stim'

processedDate = time.strftime("%d_%m_%Y")

dbKey = 'reward_change'
NEW_DATABASE_FOLDER = 'new_celldb'

timeRange = [-0.5,0.5] # In seconds. Time range for to calculate spikeTimesFromEventOnset, this time window has to span all the possible count time ranges for generating spike count matrix

recalculate = False

# -- Takes command line arguments for script params -- #
parser = argparse.ArgumentParser()
parser.add_argument('--CASE', type=str, required=True, help="CASE can be 'calculate' or 'merge'")
parser.add_argument('-MICE', '--MOUSENAMELIST', type=str, nargs='*', help="Enter mouse names separated by space")
args = parser.parse_args()
CASE = args.CASE
mouseNameList = args.MOUSENAMELIST
##############################################################

if CASE == 'calculate':
    #-- Calculate modulation index and significance with different onset and time window --#
    for mouseName in mouseNameList:
        newTime=time.time(); print 'Elapsed time: {0:0.2f}  AFTER IMPORT'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER


        # -- Define the alignment and countTimeRange windows to use for calculating modulation -- #
        #allAlignments = ['sound','center-out','side-in'] #the first argument is alignment, choices are 'sound', 'center-out' and 'side-in'
        #allCountTimeRanges = ([0,0.1],[-0.1,0])
        #allCountTimeRanges = ([0.05,0.15],[0.05,0.25],[0.05,0.35],[0.15,0.25],[0.05,0.2])

        # -- Generate conditions for calculating modulation in by taking all possible combinations from all alignments and countTimeRanges -- #
        #conditions = list(itertools.product(allAlignments,allCountTimeRanges))
        conditions = [('sound', [-0.1,0]), 
                      ('sound', [0,0.1]), 
                      ('center-out', [-0.1,0]), 
                      ('center-out', [0.05,0.15]), 
                      ('center-out', [0.15,0.25]),
                      ('center-out', [0.05,0.2]),
                      ('center-out', [0.05,0.25]),
                      ('center-out', [0.05,0.35]),
                      ('side-in',[-0.1,0]),
                      ('side-in',[-0.15,0]),
                      ('side-in',[-0.2,0]),
                      ('side-in',[0,0.1])
        ]
        modulationDfAllMice = pd.DataFrame()

        #for mouseName in mouseNameList:
        #databaseFullPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(mouseName))
        databaseFullPath = os.path.join(settings.DATABASE_PATH, NEW_DATABASE_FOLDER, '{}_database.h5'.format(mouseName))
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

        cellDb = pd.read_hdf(databaseFullPath, key=dbKey)
   
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
                                       'modDirLow_'+window: [],
                                       'modIndHigh_'+window: [],
                                       'modSigHigh_'+window: [],
                                       'modDirHigh_'+window: []})

            for ind,cell in chunk.iterrows():
                if len(processed):
                    processedThisSes = processed[processed['date']==cell.date]
                else:
                    processedThisSes = pd.DataFrame({'tetrode':[],'cluster':[]})
                if (cell.date in processedSessions) & (cell.tetrode in processedThisSes['tetrode']) & (cell.cluster in processedThisSes['cluster']):
                    print 'This cell has been checked for modulation.'
                    continue
                else:
                    # -- Load behavior and ephys data for this cell -- #
                    cellObj = ephyscore.Cell(cell)
                    sessiontype = 'behavior' #2afc behavior
                    sessionInd = cellObj.get_session_inds(sessiontype)[0]
                    bdata = cellObj.load_behavior_by_index(sessionInd)
                    try:
                        ephysData = cellObj.load_ephys_by_index(sessionInd)
                    except ValueError:
                        #spikeData = (0, 0)
                        modulationDict['subject'].append(cell.subject)
                        modulationDict['date'].append(cell.date)
                        modulationDict['tetrode'].append(cell.tetrode)
                        modulationDict['cluster'].append(cell.cluster)
                        for key in modulationDict.keys():
                            if 'modInd' in key:
                                modulationDict[key].append(0.0)
                            elif 'modSig' in key:
                                modulationDict[key].append(1.0)
                            elif 'modDir' in key:
                                modulationDict[key].append(0)
                        continue

                    eventsDict = ephysData['events']
                    spikeTimestamps = ephysData['spikeTimes']
                    
                    soundOnsetTimeBehav = bdata['timeTarget']
                    newTime=time.time(); print 'Elapsed time: {0:0.2f} Loaded behavior and events'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER

                    ######check if ephys and behav miss-aligned, if so, remove skipped trials####
                    #eventTimes = eventData.timestamps
                    #soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
                    #soundOnsetTimeEphys = eventTimes[soundOnsetEvents]

                    soundOnsetTimeEphys = eventsDict['{}On'.format(soundChannelType)]
                    # -- Find missing trials -- #
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
                            elif 'modDir' in key:
                                modulationDict[key].append(0)
                        continue
                    newTime=time.time(); print 'Elapsed time: {0:0.2f} Removed missing trials'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER

                    currentBlock = bdata['currentBlock']
                    blockTypes = [bdata.labels['currentBlock']['same_reward'],bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
                    trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes) # trialsEachType is an ndarray of dimension nTrials*nblockTypes where boolean vector (in a column) indicates which trials are in each type of block
                    # -- Find trials each type each block to evaluate Modulation Direction -- #
                    nTrials = len(bdata['currentBlock'])
                    blockBoundaries = np.flatnonzero(np.diff(bdata['currentBlock']))
                    lastTrialEachBlock = np.hstack((blockBoundaries,nTrials))
                    firstTrialEachBlock = np.hstack((0,lastTrialEachBlock[:-1]+1))
                    nRcBlocks = 0 # Number of blocks with unequal reward on left and right port
                    blockNumEachTrial = np.zeros(nTrials)
                    for indBlock,firstTrial in enumerate(firstTrialEachBlock):
                        typeThisBlock = bdata['currentBlock'][firstTrial]
                        if (typeThisBlock == bdata.labels['currentBlock']['more_left']) | (typeThisBlock ==bdata.labels['currentBlock']['more_right']):
                            nRcBlocks += 1
                            lastTrial = lastTrialEachBlock[indBlock]
                            blockNumEachTrial[firstTrial:lastTrial] = nRcBlocks # possible values of blockNumEachTrial start at 1
                    
                    trialsEachBlockLeftOrRightMore = behavioranalysis.find_trials_each_type(blockNumEachTrial, range(1, nRcBlocks+1))  # trialsEachBlock is an ndarray of dimension nTrials*nRcBlocks where nRcBlocks is the number of left_more or right_more blocks
                
                    ####################################################################
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
                            elif 'modDir' in key:
                                modulationDict[key].append(0)
                        continue

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
                            EventOnsetTimes = soundOnsetTimeEphys
                        elif alignment == 'center-out':
                            diffTimes=bdata['timeCenterOut']-bdata['timeTarget']
                            EventOnsetTimes = soundOnsetTimeEphys + diffTimes
                        elif alignment == 'side-in':
                            diffTimes=bdata['timeSideIn']-bdata['timeTarget']
                            EventOnsetTimes = soundOnsetTimeEphys + diffTimes
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
                                spikesanalysis.eventlocked_spiketimes(spikeTimestamps,EventOnsetTimes,timeRange)

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
                            spikeAvgMoreRight = np.average(spikeCountEachTrial[trialsMoreRight])
                            spikeAvgMoreLeft = np.average(spikeCountEachTrial[trialsMoreLeft])
                            if ((spikeAvgMoreRight + spikeAvgMoreLeft) == 0):
                                modIndex = 0.0
                                modSig = 1.0
                            else:
                                modSig = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange,trialsEachCond)[1]
                                modIndex = (spikeAvgMoreRight - spikeAvgMoreLeft)/(spikeAvgMoreRight + spikeAvgMoreLeft)

                            # -- Evaluate modulation direction -- #
                            aveSpikeEachBlock = np.zeros(nRcBlocks)
                            for block in range(nRcBlocks):
                                trialsThisBlock = trialsEachBlockLeftOrRightMore[:, block] & freq & correct
                                aveSpikeThisBlock = np.average(spikeCountEachTrial[trialsThisBlock])
                                aveSpikeEachBlock[block] = aveSpikeThisBlock
                            aveSpikeDiffEachBlock = np.diff(aveSpikeEachBlock)
                            if len(np.unique(np.sign(aveSpikeDiffEachBlock))) == 1:
                                # All spike differences of the same sign, that means firing rate keeps going up or going down throughout session
                                modDir = 0
                            else:
                                # At least one block firing rate changes in opposite direction; cannot tell if firing rate flip-flops per block 
                                modDir = 1
                            ##############################################################    
                            newTime=time.time(); print 'Elapsed time: {0:0.2f}  Calculated MOD INDEX & SIG'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER
                            modulationDict['modInd{}_'.format(freqLabels[indf])+window].append(modIndex) 
                            modulationDict['modSig{}_'.format(freqLabels[indf])+window].append(modSig)
                            modulationDict['modDir{}_'.format(freqLabels[indf])+window].append(modDir)

            # Open the hdf file for appending data
            #outFilename = '/var/tmp/{}_reward_change_modulation.h5'.format(mouseName)
            outFile = pd.HDFStore(outFilename, 'a')

            modulationDfThisChunk=pd.DataFrame(modulationDict)    
            modulationDfThisChunk.sort_values(['date','tetrode','cluster'],ascending=True,inplace=True)
            outFile.append('reward_change',modulationDfThisChunk, data_columns=True, index=True)
            outFile.close()
            newTime=time.time(); print 'Elapsed time: {0:0.2f} WROTE TO OUTFILE'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER


if CASE == 'merge':
    # -- Merge newly calculated modulation index from dif windows with all cells all measures --#
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    for mouseName in mouseNameList:
        databaseFullPath = os.path.join(settings.DATABASE_PATH, NEW_DATABASE_FOLDER, '{}_database.h5'.format(mouseName))
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
            dfAllThisMouse.drop('level_0', 1, inplace=True)
        dfAllThisMouse.reset_index(inplace=True)
        if 'level_0' in dfAllThisMouse.columns:
            dfAllThisMouse.drop('level_0', 1, inplace=True)
        dfAllThisMouse.to_hdf(databaseFullPath, key='reward_change')
        
        #when saving to hdf, using (format='table',data_columns=True) is slower but enable on disk queries

