'''
Generate and store intermediate data for plot showing movement-aligned firing activity of astr neurons recorded in reward change task.  
Spike counts are done separately for low vs high freq trials and left vs right movement trials (4 conditions total).
Lan Guo 2018-08-03
'''
import os
import sys
import numpy as np
import pandas as pd
from jaratoolbox import loadbehavior
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
import figparams
reload(figparams)

STUDY_NAME = figparams.STUDY_NAME
FIGNAME = 'movement_selectivity'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

if not os.path.exists(outputDir):
    os.mkdir(outputDir)

scriptFullPath = os.path.realpath(__file__)
timeRange = [-0.4,0.5]
binWidth = 0.010

colorsDict = {'left': figparams.colp['MoveLeft'],
              'right':figparams.colp['MoveRight']} 

# -- Access mounted behavior and ephys drives for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
EPHYS_PATH = settings.EPHYS_PATH_REMOTE

if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

if not os.path.ismount(EPHYS_PATH):
    os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ {}'.format(EPHYS_PATH))


# -- These example cells we picked manually  --#
cellParamsList = []

exampleCell = {'subject':'adap013',
              'date':'2016-03-30',
              'tetrode':8,
               'cluster':5,
               'brainRegion':'astr'}  # leftward very strong
cellParamsList.append(exampleCell) 

exampleCell = {'subject':'adap005',
              'date':'2015-12-24',
              'tetrode':6,
               'cluster':8,
               'brainRegion':'astr'} 
cellParamsList.append(exampleCell)

exampleCell = {'subject':'adap012',
              'date':'2016-03-09',
              'tetrode':3,
               'cluster':2,
               'brainRegion':'astr'} 
cellParamsList.append(exampleCell)
#
exampleCell = {'subject':'adap012',
              'date':'2016-03-24',
              'tetrode':4,
               'cluster':8,
               'brainRegion':'astr'} 
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-02-13',
              'tetrode':7,
               'cluster':8,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-03-11',
              'tetrode':4,
               'cluster':5,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)

#
exampleCell = {'subject':'gosi008',
              'date':'2017-03-07',
              'tetrode':1,
               'cluster':4,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)

#
exampleCell = {'subject':'gosi008',
              'date':'2017-03-10',
              'tetrode':1,
               'cluster':10,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)


exampleCell = {'subject':'gosi010',
              'date':'2017-05-02',
              'tetrode':4,
               'cluster':12,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)

# -- Here we can choose to generate data for a specific cell instead of every cell -- #
if len(sys.argv) == 1:
    print 'You can also provide the index of the cell you want to generate intermediate data for as an argument to this script. Generating data for all cells...'
    cellIndToGenerate = 'all'
elif len( sys.argv) == 2:
    cellIndToGenerate = int(sys.argv[1]) 
####################################################################################
dbFolder = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
celldbPath = os.path.join(dbFolder, 'rc_database.h5')
celldb = celldatabase.load_hdf(celldbPath)
sessionType = 'behavior'
behavClass = loadbehavior.FlexCategBehaviorData
evlockFolder = 'evlock_spktimes'
evlockDataPath = os.path.join(EPHYS_PATH, STUDY_NAME, evlockFolder)
soundChannelType = 'stim'
####################################################################################

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

    diffTimesSound = bdata['timeTarget'] - bdata['timeCenterOut'] 
    diffTimesSideIn = bdata['timeSideIn'] - bdata['timeCenterOut']

    # -- Select trials to plot from behavior file -- #
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    freqEachTrial = bdata['targetFrequency']
    lowFreq = freqEachTrial == bdata['lowFreq'][0]
    highFreq = freqEachTrial == bdata['highFreq'][0]

    trialsToUseLeftCorrct = leftward & lowFreq
    trialsToUseLeftError = leftward & highFreq
    trialsToUseRightCorrect = rightward & highFreq
    trialsToUseRightError = rightward & lowFreq

    condLabels = ['go left correct', 'go right correct', 'go left error', 'go right error']
    #condLabels = ['go left', 'go right']
    trialsEachCond = np.c_[trialsToUseLeftCorrct, trialsToUseRightCorrect, trialsToUseLeftError, trialsToUseRightError] 
    #trialsEachCond = np.c_[leftward, rightward]
    colorEachCond = [colorsDict['left'],colorsDict['right'],colorsDict['left'],colorsDict['right']]
    #colorEachCond = [colorsDict['left'],colorsDict['right']]
    
    alignment = 'center-out'
    evlockDataFilename = '{0}_{1}_{2}_T{3}_c{4}_{5}.npz'.format(animal, date, depth, tetrode, cluster, alignment)
    evlockDataFullpath = os.path.join(evlockDataPath, evlockDataFilename) 
    evlockSpktimes = np.load(evlockDataFullpath)
    spikeTimesFromEventOnset = evlockSpktimes['spikeTimesFromEventOnset']
    indexLimitsEachTrial = evlockSpktimes['indexLimitsEachTrial']
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    # -- Save raster intermediate data -- #    
    #outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
    outputFile = 'example_rc_movement_sel_{}_{}_T{}_c{}.npz'.format(animal, date, tetrode, cluster)
    outputFullPath = os.path.join(outputDir,outputFile)
    np.savez(outputFullPath, spikeTimesFromEventOnset=spikeTimesFromEventOnset, 
      soundTimesFromEventOnset=diffTimesSound, sideInTimesFromEventOnset=diffTimesSideIn,
      indexLimitsEachTrial=indexLimitsEachTrial, 
      spikeCountMat=spikeCountMat, timeVec=timeVec, binWidth=binWidth, 
      condLabels=condLabels, trialsEachCond=trialsEachCond, colorEachCond=colorEachCond, 
      script=scriptFullPath, colorLeftTrials=colorsDict['left'], colorRightTrials=colorsDict['right'], **cellParams) 


    
