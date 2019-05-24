'''
Generate and store intermediate data for plot showing frequency-selectivity of astr sound-responsive neurons (using psychometric curve 2afc data). 
Lan Guo20161221
'''

import os
import numpy as np
import pandas as pd
from jaratoolbox import settings
import figparams

scriptFullPath = os.path.realpath(__file__)
goodQualityList = [1,6]
maxZthreshold = 3

# -- Access mounted ephys data for psycurve mice -- #
EPHYS_MOUNTED = settings.EPHYS_PATH_REMOTE

# if not os.path.ismount(EPHYS_MOUNTED):
#     os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ {}'.format(EPHYS_MOUNTED))

################ -- Function to read file containing maximal Z score for each frequency presented in the psychometric curve task, store data in a dataframe  -- #####################
### This function is modified from a function with the same name in test068_read_psychometric_measurement_txtfiles.py to include maxZ score for all frequencies. ###

class nestedDict(dict): 
    #This is for making a dict that it returns a new instance (of dict) whenever a key is accessed but missing
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def read_sound_maxZ_file_psychometric_return_Df(maxZFilename):
    '''
    Reads txt files containing maximal Z scores of sound responses calculated by each chord frequencies presented in the 2afc psychometric curve task. 
    Text File foramt: file starts with behavSession line ('Behavior Session:behavSession\n'), followed by one line for each frequency (there are 6 frequencies in each session) in the task, each frequency line starts with the frequency, followed by a space ' ', then the maxZ scores separated by comma ',' .
    '''
    import pandas as pd

    maxZFile = open(maxZFilename, 'r')
    
    behavSessionCount=0 #for keeping track of how many behav session was processed
    
    maxZDict = nestedDict()
    behavName = ''
    for line in maxZFile:
        behavLine = line.split(':')
        freqLine = line.split()
        if (behavLine[0] == 'Behavior Session'):
            behavName = behavLine[1][:-1]
        else:
            maxZDict[behavName][freqLine[0]] = freqLine[1].split(',')[0:-1]
    maxZFile.close()

    maxZDf = pd.DataFrame()
    numCellsPerSession = 96

    for behavSession in maxZDict.keys():
        thisSessionDf = pd.DataFrame({'behavSession':np.tile(behavSession,numCellsPerSession),'tetrode':np.repeat(range(1,9),12),'cluster':np.tile(range(1,13),8)})
        allFreqsSorted = sorted(int(freq) for freq in maxZDict[behavSession].keys()) #has to turn string (dic keys) to int for sorting by frequency!
        #thisSessionDf['freqs'] = allFreqsSorted,numCellsPerSession)
        #maxZAllFreqs = np.zeros((numCellsPerSession,len(allFreqsSorted))) #initialize ndarray for all cells and all 6 frequencies in the psychometric task, some sessions may not have all 6 so those values will be zero
        for indf,freq in enumerate(allFreqsSorted):
            maxZThisFreq = maxZDict[behavSession][str(freq)] #has to turn the freq back to str
            #maxZAllFreqs[:,indf] = maxZThisFreq
            thisSessionDf['maxZ_freq{}'.format(indf+1)] = maxZThisFreq
        maxZDf = maxZDf.append(thisSessionDf, ignore_index=True)
    return maxZDf
###############################################################################################

############ -- Function to read cell quality and depth from allcells files -- ###############
### This function is taken from test068_read_psychometric_measurement_txtfiles.py ###

def read_allcells_quality_depth(allcellsFilename):
    import sys
    import importlib
    import pandas as pd
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)
    cellsThisAnimal=allcells.cellDB
    cellQualityDf = pd.DataFrame(columns=['animalName','cellQuality','tetrode','cluster','behavSession','cellDepth'])
    #dtype=['str','int','int','int','str','float']
    for oneCell in cellsThisAnimal:
        cellQualityDf = cellQualityDf.append({'animalName':oneCell.animalName,'cellDepth':oneCell.depth,'cellQuality':oneCell.quality[oneCell.cluster-1],'tetrode':oneCell.tetrode,'cluster':oneCell.cluster,'behavSession':oneCell.behavSession}, ignore_index=True)
        
    return cellQualityDf
###############################################################################################


psychometricMice = ['adap013','adap017','adap015','test053','test055']
allMiceDfs = []

# -- Loop through all psychometric curve mice, get cell quality and maxZ score for all frequencies -- #
for mouseName in psychometricMice:
    allcellsFileName = 'allcells_'+mouseName+'_quality'
    cellQualityDf = read_allcells_quality_depth(allcellsFileName)

    # - Directory storing all computed measurements in txt files -- #
    processedDir = os.path.join(EPHYS_MOUNTED,mouseName+'_processed')
    #measurementFiles = [os.path.join(processedDir, f) for f in os.listdir(processedDir) if os.path.isfile(os.path.join(processedDir, f))]
    dfs = []
    dfs.append(cellQualityDf)
    
    maxZFilename = os.path.join(processedDir,'maxZVal.txt')
    maxZsoundDf = read_sound_maxZ_file_psychometric_return_Df(maxZFilename)
    dfs.append(maxZsoundDf)

    #--Joining both dataFrames on 'behavSession' column --#
    dfThisMouse = reduce(lambda left,right: pd.merge(left,right,on=['behavSession','tetrode','cluster'],how='inner'), dfs)
    allMiceDfs.append(dfThisMouse)

dfAllPsychometricMouseSound = pd.concat(allMiceDfs, ignore_index=True)
dfAllPsychometricMouseSound['script'] = scriptFullPath

### Save dataframe ###
outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
outputFile = 'all_freqs_maxZ_all_psycurve_mice.h5'
outputFullPath = os.path.join(outputDir,outputFile)
dfAllPsychometricMouseSound.to_hdf(outputFullPath,key='psychometric')


# -- Generate counts of 'responsive' cell (based on maxZ) of good quality for each frequency presented in the psychometric curve task. Do this separately for each mouse. -- #
maxNumOfFreqs = 6
allMiceFreqSelDict = {}
for thisMouseDf in allMiceDfs:
    goodCells = thisMouseDf.loc[thisMouseDf.cellQuality.isin(goodQualityList)]
    maxZcolnames = sorted([col for col in goodCells.columns if 'maxZ' in col]) #Get a list of column names containing maxZ scores, sorted so that lower frequencies come first
    numOfFreqs = len(maxZcolnames)
    if numOfFreqs > maxNumOfFreqs:
        maxNumOfFreqs = numOfFreqs
    numResponsiveCellsAllFreqs = []
    for colname in maxZcolnames:
        numResponsiveCells = sum(np.abs(goodCells[colname].astype('float')) > maxZthreshold)
        numResponsiveCellsAllFreqs.append(numResponsiveCells)
    allMiceFreqSelDict[thisMouseDf.animalName[0]] = numResponsiveCellsAllFreqs

### Save data ###
outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
outputFile = 'summary_freq_selectivity_all_psycurve_mice.npz'
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, script=scriptFullPath, maxZthreshold=maxZthreshold, goodCellQuality=goodQualityList, numOfFreqs=maxNumOfFreqs, psychometricMice=psychometricMice,  **allMiceFreqSelDict)
