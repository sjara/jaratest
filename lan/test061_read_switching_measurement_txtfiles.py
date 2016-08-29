'''
To select cells to plot, we need to check cell quality as well as many computed measures we defined in analysis, such as sound responsiveness, and whether modulated when mice going left versus going right etc.
Script with methods to read txt files generated from analysis of switching animals (maxZ sound score, ISI violation, modulation index, movement modulation index, minimal performance, minimal trials) and store them in dictionaries. Also looks at all cells and gets cluster quality, depth info.

Lan Guo 20160818
'''

from jaratoolbox import settings
import os
import sys
import importlib
import re
import numpy as np
import pandas as pd

cellNumPerSession = 96


def read_sound_maxZ_file_switching(maxZFilename):
    '''
    File foramt: file starts with behavSession line ('Behavior Session:behavSession\n'), followed by one line for each frequency in the task, each frequency line starts with the frequency, followed by a space ' ', then the maxZ scores separated by comma ',' .
    '''
    maxZFile = open(maxZFilename, 'r')
    #maxZsoundDict = {'maxZSoundLow':[],'maxZSoundMid':[],'maxZSoundHigh':[],'behavSession':[]}
    maxZsoundDict = {}
    behavSessionCount=0 #for keeping track of how many behav session was processed
    for line in maxZFile:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        behavLine = line.split(':')
        freqLine = line.split()
        if (behavLine[0] == 'Behavior Session'):
            behavName = behavLine[1][:-1]
            behavSessionCount += 1
            
        else:
            maxZDict[behavName][freqLine[0]] = freqLine[1].split(',')[0:-1]
    maxZFile.close()
    #maxZsound=pd.DataFrame(maxZsoundDict) #col name will be specific freq will create extra cols when freq changes
    
    #print maxZsound[100:150]
    maxZsound.sort('behavSession',ascending=True,inplace=True)
    #maxZsound=maxZsound.reset_index(drop=True)
    maxZsound = maxZsound.values() #This gets a numpy matrix of the values
    
    return maxZsound


def read_ISI_violation_file(ISIFilename):
    '''
    File format: file starts with behavSession line ('Behavior Session:behavSession\n'), followed by one line for the ISI violation percentage for all possible clusters in this session, separated by comman ','.
    '''
    ISIFile = open(ISIFilename, 'r')
    behavSessionCount=0
    ISIDict = {}
    for line in ISIFile:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1] 
            behavSessionCount+=1
            ISIDict['behavSession'].extend([behavName]*cellNumPerSession)
        else:
            ISIDict['ISI'].extend([float(x) for x in line.split(',')[0:-1]])
    ISIFile.close()      
    ISI = pd.DataFrame(ISIDict)
    #print ISI[100:150]
    ISI.sort('behavSession',ascending=True,inplace=True)
    #ISI = ISI.reset_index(drop=True)
    ISI = ISI['ISI'].values()
    
    return ISI


def read_min_performance_file(minPerfFilename):
    '''
    File format: file starts with one line describing the minimal performance criterion/cut-off, followed by all the session names for sessions that passed the cut-off, each session name is one line.
    '''
    minPerfFile.readline()
    minPerfList=minPerfFile.read().split()



def read_min_trial_file(minTrialFile):
    '''
    File format: file starts with one line describing the minimal trial number criterion/cut-off. This line is followed by an empty line, then behavior sessions names (e.g. 20160229a) of all the sessions are listed, one on each line, along with the middle frequency presented in that session if it passed the min trial test (e.g. "20160412a: 11000") 
    '''
    minTrialFile.readline()
    minTrialFile.readline()
    minTrialDict= {}
    for lineCount,line in enumerate(minTrialFile):
        minTrialStr = line.split(':')
        trialFreq = minTrialStr[1].split()
        minTrialDict.update({minTrialStr[0][1:]:trialFreq})
        # if the session's middle frequency does not pass the minimum trial criteria, the sub dictionary of that session will be empty.



def read_mod_index_switching(modIndexFile):
    '''
    File format: each session's record starts with one line for the behavior session name (e.g. "Behavior Session:20160414a"). This is followed by a new line containing the modI values for every cluster for the middle frequency (start with 'modI:' modIndex separated by ','). Next is a new line containing the p value significance for the modulation of the middle frequency for every cluster (start with 'modSig:' mod significance separated by ','). Last new line is the modulation direction score ((start with 'modDir:' mod dir score separated by ',').  
    '''
    modIFile = open(modIFilename, 'r')
    modIDict = {} #stores all the modulation indices
    modSigDict = {} #stores the significance of the modulation of each cell
    modDirectionScoreDict = {} #stores the score of how often the direction of modulation changes
    behavName = ''
    behavName = ''
    for line in modIFile:
        splitLine = line.split(':')
        if (splitLine[0] == 'Behavior Session'):
            behavName = splitLine[1][:-1]
        elif (splitLine[0] == 'modI'):
            modIDict[behavName] = [float(x) for x in splitLine[1].split(',')[0:-1]]
        elif (splitLine[0] == 'modSig'):
            modSigDict[behavName] = [float(x) for x in splitLine[1].split(',')[0:-1]]
        elif (splitLine[0] == 'modDir'):
            modDirectionScoreDict[behavName] = [float(x) for x in splitLine[1].split(',')[0:-1]]




















if __name__ == '__main__':
    mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
    allcellsFileName = 'allcells_'+mouseName
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)


    # - Directory storing all computed measurements in txt files -- #
    processedDir = os.path.join(settings.EPHYS_PATH,mouseName,mouseName+'_stats')

    measurementFiles = [(os.path.join(processedDir, f) for f in os.listdir(processedDir) if os.path.isfile(os.path.join(processedDir, f))]

    for filename in measurementFiles:
        if filename.find('maxZVal'):
            maxZsound = read_sound_maxZ_file_switching(filename)

        if filename.find('ISI'):
            ISI = read_ISI_violation_file(filename)

        if filename.find('minTrial'):

        if filename.find('minPerformance'):

        if filename.find('modIndex'):


        if filename.find('movement'):
