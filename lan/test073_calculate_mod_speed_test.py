'''
Lan Guo 20161122
Script to calculate modulation index for the switching task for all cells in animals recorded during the switching 2afc task. 
Modulation index is calculated by comparing spike counts in a given window for trials in the high-block versus trials in the low-block. Only using correct trials; only calculate mod index for middle frequency. 
Modulation direction is a rough estimate of whether the cells activity goes up and down in a block-wise manner in a session; can potentially rule out cells whose activity consistently decrease or increase throughout the session.
Can choose different alignment options (sound, center-out, side-in) and calculate Mod Index for different time windows with aligned spikes.
Output is a pandas series
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
from jaratest.lan import test055_load_n_plot_billy_data_one_cell as loader
reload(loader)

newTime=time.time(); print 'Elapsed time: {0:0.2f}  AFTER IMPORT'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER


# -- Define the alignment and countTimeRange windows to use for calculating modulation -- #
allAlignments = ['sound','center-out'] #the first argument is alignment, choices are 'sound', 'center-out' and 'side-in'
allCountTimeRanges = ([0,0.1],[-0.1,0])
# Generate conditions for calculating modulation in by taking all possible combinations from all alignments and countTimeRanges
conditions = list(itertools.product(allAlignments,allCountTimeRanges))

#These are all the switching mice we recorded from
#mouseNameList = ['test059','test017'] 
mouseNameList = ['adap020','test059','test017'] 

# -- Global variables -- #
SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial


modulationDfAllMice = pd.DataFrame()

for mouseName in mouseNameList:
    outFilename = '/var/tmp/{}_switching_modulation.h5'.format(mouseName)
    if os.path.isfile(outFilename):
        print 'Analysis for this mouse was saved before.'
        processed = pd.read_hdf(outFilename, key='switching')
        processedSessions = np.unique(processed['behavSession'])
    else:
        processed = pd.DataFrame({'behavSession':[]})
        processedSessions = []
    modulationDict = {'animalName': [],
                      'behavSession': [],
                      'tetrode': [],
                      'cluster': []}

    for (alignment, countTimeRange) in conditions:
        # Make names for count time range and alignment for labeling columns in output df
        window = str(countTimeRange[0])+'-'+str(countTimeRange[1])+'s_'+alignment
        modulationDict.update({'modInd_'+window:[],
                               'modSig_'+window: [],
                               'modDir_'+window: []})

    allcellsFileName = 'allcells_'+mouseName+'_quality'
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)
    reload(allcells)

    newTime=time.time(); print 'Elapsed time: {0:0.2f}  ALLCELLS'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER
    
    # Process each mouse in chunks
    chunkSize = 20
    chunks = [allcells.cellDB[ind:ind+chunkSize] for ind in range(0, len(allcells.cellDB), chunkSize)]
        
    for chunk in chunks:

        modulationDict = {'animalName': [],
                      'behavSession': [],
                      'tetrode': [],
                      'cluster': []}

        for (alignment, countTimeRange) in conditions:
            # Make names for count time range and alignment for labeling columns in output df
            window = str(countTimeRange[0])+'-'+str(countTimeRange[1])+'s_'+alignment
            modulationDict.update({'modInd_'+window:[],
                                   'modSig_'+window: [],
                                   'modDir_'+window: []})

        for cell in chunk:
            if len(processed):
                processedThisSes = processed[processed['behavSession']==cell.behavSession]
            else:
                processedThisSes = pd.DataFrame({'tetrode':[],'cluster':[]})
            if (cell.behavSession in processedSessions) & (cell.tetrode in processedThisSes['tetrode']) & (cell.cluster in processedThisSes['cluster']):
                print 'This cell has been checked for modulation.'
                continue
            else:
                bdata = loader.load_remote_2afc_behav(cell)
                eventData = loader.load_remote_2afc_events(cell)
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
                    continue
                newTime=time.time(); print 'Elapsed time: {0:0.2f} Removed missing trials'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER


                rightward = bdata['choice']==bdata.labels['choice']['right']
                leftward = bdata['choice']==bdata.labels['choice']['left']
                valid = (bdata['outcome']==bdata.labels['outcome']['correct'])|(bdata['outcome']==bdata.labels['outcome']['error'])
                correct = bdata['outcome']==bdata.labels['outcome']['correct']
                correctRightward = rightward & correct
                correctLeftward = leftward & correct
                possibleFreq = np.unique(bdata['targetFrequency'])
                midFreq = bdata['targetFrequency'] == possibleFreq[len(possibleFreq)/2]

                # -- Select which trials to include -- #
                trialsToInclude = np.ones(len(bdata['currentBlock']), dtype=bool)

                ## -- Get rid of the any block if it's too short (don't have enough valid trials)-- ##
                ## NOTE 20161125 sometimes that last two blocks don't have enough valid trials!
                ## Changed this to iterate through all blocks and get rid of any block that doesn't have enough valid trials
                minLastBlockSize = 50 

                firstTrialsEachBlock = np.r_[0,np.flatnonzero(np.diff(bdata['currentBlock']))+1]
                lastTrialsEachBlock = np.r_[np.flatnonzero(np.diff(bdata['currentBlock'])),(len(bdata['currentBlock'])-1)]
                for (start,end) in zip(firstTrialsEachBlock,lastTrialsEachBlock):
                    #firstTrialLastBlock = indFirstTrialEachBlock[-1]
                    if sum(valid[start:end+1]) < minLastBlockSize:
                        trialsToInclude[start:end+1] = False
                        firstTrialsEachBlock = np.delete(firstTrialsEachBlock,np.where(firstTrialsEachBlock==start)[0])#remove this short block's first trial from record, so that won't look at this block again in the next steps
                newTime=time.time(); print 'Elapsed time: {0:0.2f} Removed blocks that were too short'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER

                ## -- Skip first 20 VALID trials of a block when calculating mod index -- ##
                numTrialsToExclude = 20 # how many trials to exclude at the beginning of each block from modulation index
                indTwentithValidTrialEachBlock = [(ind+np.where(valid[ind:]==1)[0][20]) for ind in firstTrialsEachBlock] #firstTrialsEachBlock should just contain blocks that have more than 50 valid trials from last step
                indTrialsToExcludeEachBlock = zip(firstTrialsEachBlock, indTwentithValidTrialEachBlock)
                for (indStart, indEnd) in indTrialsToExcludeEachBlock:
                    trialsToInclude[indStart:indEnd] = False
                newTime=time.time(); print 'Elapsed time: {0:0.2f} Removed first 20 valid trials from each block'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER

                # -- Calculate modulation index using only correct trials, trials not excluded in the last two steps, and using only middle frequency
                trialsToUse = trialsToInclude & midFreq 
                trialsToUseRight = correctRightward & trialsToUse
                trialsToUseLeft = correctLeftward & trialsToUse
                trialsEachCond = [trialsToUseRight,trialsToUseLeft]
                
                modulationDict['animalName'].append(cell.animalName)
                modulationDict['behavSession'].append(cell.behavSession)
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
                    outputFile = 'eventlocked_{0}_{1}_T{2}c{3}_{4}.npz'.format(cell.animalName, cell.behavSession, cell.tetrode, cell.cluster, alignment)
                    outputFullPath = os.path.join(outputDir,outputFile)
                    if os.path.isfile(outputFullPath):
                        evlockdata = np.load(outputFullPath)
                        spikeTimesFromEventOnset = evlockdata['spikeTimesFromEventOnset']
                        trialIndexForEachSpike = evlockdata['trialIndexForEachSpike']
                        indexLimitsEachTrial = evlockdata['indexLimitsEachTrial']
                        timeRange = evlockdata['timeRange']

                        newTime=time.time(); print 'Elapsed time: {0:0.2f}  LOADED EVLOCKED DATA'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER

                    else:
                        # -- Load ephys data for 2afc --
                        spikeData = loader.load_remote_2afc_spikes(cell)

                        newTime=time.time(); print 'Elapsed time: {0:0.2f}  LOADED EPHYS/BEHAV one cell'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER

                        spkTimeStamps = spikeData.timestamps
                        timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

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

                    # -- Calculate modulation index and significance p value -- #
                    spikeAvgRight = np.average(spikeCountEachTrial[trialsToUseRight])
                    spikeAvgLeft = np.average(spikeCountEachTrial[trialsToUseLeft])
                    if ((spikeAvgRight + spikeAvgLeft) == 0):
                        modIndex = 0.0
                        modSig = 1.0
                    else:
                        modSig = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange,trialsEachCond)[1]
                        modIndex = (spikeAvgRight - spikeAvgLeft)/(spikeAvgRight + spikeAvgLeft)
                    newTime=time.time(); print 'Elapsed time: {0:0.2f}  Calculated MOD INDEX & SIG'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER
                    # -- Calculate modulation direction score -- #
                    ###### Interpret results: modulation direction score of 0 is when activity either just goes up or just goes down during the session #############  
                    aveSpikesEachBlock = []
                    blockVec = np.zeros(len(bdata['currentBlock']))

                    for (start,end) in zip(firstTrialsEachBlock,lastTrialsEachBlock):
                        trialsThisBlock = np.zeros(len(bdata['currentBlock']), dtype=bool)
                        trialsThisBlock[start:end+1] = True
                        aveSpikesEachBlock.append(np.average(spikeCountEachTrial[trialsToUse&trialsThisBlock]))

                    rateChangeOverBlocks = np.diff(np.array(aveSpikesEachBlock))
                    rateChangeNonZero = np.array([i for i in rateChangeOverBlocks if i!=0])
                    if len(rateChangeNonZero)==0: #firing rate unchanged the whole session
                        modDir = 0
                    elif np.all(rateChangeNonZero>0) or np.all(rateChangeNonZero<0): #consistently go up or down, one direction for the whole session 
                        modDir = 0
                    else:
                        modDir = 1
                    newTime=time.time(); print 'Elapsed time: {0:0.2f}  Calculated MOD DIR'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER

                    modulationDict['modInd_'+window].append(modIndex) 
                    modulationDict['modSig_'+window].append(modSig)
                    modulationDict['modDir_'+window].append(modDir)

        # Open the hdf file for appending data
        outFilename = '/var/tmp/{}_switching_modulation.h5'.format(mouseName)
        outFile = pd.HDFStore(outFilename, 'a')

        modulationDfThisChunk=pd.DataFrame(modulationDict)    
        modulationDfThisChunk.sort(['behavSession','tetrode','cluster'],ascending=True,inplace=True)
        #modulationDfAllMice = pd.concat((modulationDfAllMice,modulationDfThisMouse), ignore_index=True)
        #modulationDfThisMouse.to_hdf('/home/languo/data/ephys/switching_summary_stats/{}_switching_modulation.h5'.format(cell.animalName),key='switching')
        #modulationDfThisMouse.to_hdf('/var/tmp/{}_switching_modulation.h5'.format(cell.animalName),key='switching')
        outFile.append('switching',modulationDfThisChunk, data_columns=True, index=True)
        outFile.close()
        newTime=time.time(); print 'Elapsed time: {0:0.2f} WROTE TO OUTFILE'.format(newTime-zeroTime); zeroTime=newTime; sys.stdout.flush()  ### PROFILER
        
#modulationDfAllMice.to_hdf('/home/languo/data/ephys/switching_summary_stats/all_mice_switching_modulation.h5',key='mod_swiching')
