'''
Generate and store intermediate data for plots showing soundonset-aligned or center-out-aligned firing activity of astr/ac neurons recorded in reward-change task (for trials using the low and high frequency separately). 
For raster data, output contains spikeTimestamps, eventOnsetTimes, spikeTimesFromEventOnset, condEachTrial, labelEachTrial, as well as meta params.
For psth data, output contains spikeCountMat, timeVec, condEachTrial, as well as meta params.

Lan Guo 20171006
'''
import os
import sys
import numpy as np
import pandas as pd
from jaratoolbox import ephyscore
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import celldatabase
import figparams
reload(figparams)

STUDY_NAME = figparams.STUDY_NAME

FIGNAME = 'sound_responses'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

if not os.path.exists(dataDir):
    os.mkdir(dataDir)
'''
colorsDict = {'leftMoreLowFreq':'g',
             'rightMoreLowFreq':'m',
             'leftMoreHighFreq':'r',
             'rightMoreHighFreq':'b'}
'''
colorsDict = {'left': figparams.colp['MoveLeft'],
              'right':figparams.colp['MoveRight']} 

# -- These example cells I picked manually  --#
cellParamsList = []

exampleCell = {'subject':'gosi004',
               'date':'2017-03-15',
               'tetrode':6,
               'cluster':4,
               'brainRegion':'ac'} # low freq, not modulated
cellParamsList.append(exampleCell)

exampleCell = {'subject':'adap017',
               'date':'2016-04-06',
               'tetrode':4,
               'cluster':3,
               'brainRegion':'astr'} # high freq, not modulated
cellParamsList.append(exampleCell)

# # sustained sound response
# exampleCell = {'subject':'adap015',
#                'date':'2016-03-18',
#                'tetrode':3,
#                'cluster':9,
#                'brainRegion':'astr'} # low freq, sound modulated
# cellParamsList.append(exampleCell)

# # strong onset sound response 
# exampleCell = {'subject':'adap012',
#                'date':'2016-04-05',
#                'tetrode':4,
#                'cluster':6,
#                'brainRegion':'astr'} # high freq, sound modulated
# cellParamsList.append(exampleCell)

# # best example for astr
# exampleCell = {'subject':'adap017',
#                'date':'2016-04-21',
#                'tetrode':5,
#                'cluster':9,
#                'brainRegion':'astr'} # high freq, sound modulated
# cellParamsList.append(exampleCell)

# exampleCell = {'subject':'adap067',
#                'date':'2017-10-04',
#                'tetrode':1,
#                'cluster':2,
#                'brainRegion':'ac'} # low freq, sound modulated
# cellParamsList.append(exampleCell)

# # best example for ac
# exampleCell = {'subject':'gosi004',
#                'date':'2017-03-19',
#                'tetrode':6,
#                'cluster':4,
#                'brainRegion':'ac'} # low freq, sound modulated
# cellParamsList.append(exampleCell)

# -- Here we can choose to generate data for a specific cell instead of every cell -- #
if len(sys.argv) == 1:
    print 'You can also provide the index of the cell you want to generate intermediate data for as an argument to this script. Generating data for all cells...'
    cellIndToGenerate = 'all'
elif len( sys.argv) == 2:
    cellIndToGenerate = int(sys.argv[1]) 

####################################################################################
scriptFullPath = os.path.realpath(__file__)
timeRange = [-0.5,1]
binWidth = 0.010
EPHYS_SAMPLING_RATE = 30000.0
soundTriggerChannel = 0
paradigm = '2afc'
minBlockSize = 30
freqsToPlot = ['low', 'high']
alignmentsToPlot = ['sound']#, 'center-out']
###################################################################################

# -- Access mounted behavior and ephys drives for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
EPHYS_PATH = settings.EPHYS_PATH_REMOTE

if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

if not os.path.ismount(EPHYS_PATH):
    os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ {}'.format(EPHYS_PATH))

dbFolder = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
celldbPath = os.path.join(dbFolder, 'rc_database.h5')
celldb = celldatabase.load_hdf(celldbPath)
sessionType = 'behavior'
behavClass = loadbehavior.FlexCategBehaviorData
evlockFolder = 'evlock_spktimes'
evlockDataPath = os.path.join(EPHYS_PATH, STUDY_NAME, evlockFolder)
soundChannelType = 'stim'
# -- Select an example cell from allcells file -- #
if cellIndToGenerate != 'all':
    cellParamsList = [cellParamsList[cellIndToGenerate]]

for cellParams in cellParamsList:
    animal = cellParams['subject']
    date = cellParams['date']
    tetrode = cellParams['tetrode']
    cluster = cellParams['cluster']
    brainRegion = cellParams['brainRegion']
    
    ### Using cellDB methode to find this cell in the cellDB ###
    cell = celldb.loc[(celldb.subject==animal) & (celldb.date==date) & (celldb.tetrode==tetrode) & (celldb.cluster==cluster)].iloc[0]
    cellObj = ephyscore.Cell(cell)
    depth = cellObj.dbRow['depth']
    sessionInd = cellObj.get_session_inds(sessionType)[0]
    #bdata = cellObj.load_behavior_by_index(sessionInd, behavClass=behavClass)
    ephysData, bdata = cellObj.load_by_index(sessionInd, behavClass=behavClass)
    
    eventsDict = ephysData['events']
    spikeTimestamps = ephysData['spikeTimes']
    soundOnsetTimeEphys = eventsDict['{}On'.format(soundChannelType)]
    soundOnsetTimeBehav = bdata['timeTarget']
    
    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    # Remove missing trials
    bdata.remove_trials(missingTrials)
    diffTimes = bdata['timeCenterOut'] - bdata['timeTarget']
    # -- Select trials to plot from behavior file -- #
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    possibleFreq = np.unique(bdata['targetFrequency'])
    numFreqs = len(possibleFreq)
    freqsEachTrial = bdata['targetFrequency']
    lowFreqTrials = (freqsEachTrial == possibleFreq[0]) & correct
    highFreqTrials = freqsEachTrial == possibleFreq[-1] & correct
    trialsEachCond = np.column_stack((lowFreqTrials, highFreqTrials))
    colorEachCond = [colorsDict['left'], colorsDict['right']]
    labelEachCond = ['low freq', 'high freq']

    for alignment in alignmentsToPlot:
        evlockDataFilename = '{0}_{1}_{2}_T{3}_c{4}_{5}.npz'.format(animal, date, depth, tetrode, cluster, alignment)
        evlockDataFullpath = os.path.join(evlockDataPath, evlockDataFilename) 
        evlockSpktimes = np.load(evlockDataFullpath)
        spikeTimesFromEventOnset = evlockSpktimes['spikeTimesFromEventOnset']
        indexLimitsEachTrial = evlockSpktimes['indexLimitsEachTrial']
        timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

        # -- Save raster and psth intermediate data -- #    
        #outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
        outputFile = 'example_sound_resp_{}aligned_{}_{}_T{}_c{}.npz'.format(alignment, animal, date, tetrode, cluster)
        outputFullPath = os.path.join(dataDir,outputFile)
        np.savez(outputFullPath, spikeTimesFromEventOnset=spikeTimesFromEventOnset, 
            movementTimesFromEventOnset=diffTimes,
            indexLimitsEachTrial=indexLimitsEachTrial, spikeCountMat=spikeCountMat, 
            timeVec=timeVec, binWidth=binWidth, condLabels=labelEachCond, 
            trialsEachCond=trialsEachCond, colorEachCond=colorEachCond, 
            script=scriptFullPath, alignedTo=alignment, **cellParams)
