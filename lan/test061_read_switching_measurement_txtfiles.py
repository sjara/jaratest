'''
To select cells to plot, we need to check cell quality as well as many computed measures we defined in analysis, such as sound responsiveness, and whether modulated when mice going left versus going right etc.
Script with methods to read txt files generated from analysis of switching animals (maxZ sound score, ISI violation, modulation index, movement modulation index, minimal performance, minimal trials) and store them in dictionaries. Also looks at all cells and gets cluster quality, depth info.

Lan Guo 20160818
'''
# -- TO DO -- #
# file-reading functions should output not a dict with behavSessions as keys but preferrably a dataframe with behavSession as a col (so can sort by behavSession)
 
from jaratoolbox import settings
import os
import sys
import importlib
import re
import numpy as np
import pandas as pd
import codecs
cellNumPerSession = 96

def read_nlines_from_txt_file(openedFile, n):
    '''
    Function to read n lines from a file given a file object.
    '''
    lines = [line for line in [openedFile.readline() for _ in range(n)] if len(line)]
    return lines


def read_sound_maxZ_file_switching_return_Df(maxZFilename):
    '''
    File foramt: file starts with behavSession line ('Behavior Session:behavSession\n'), followed by one line for each frequency (there are 3 frequencies in each session) in the task, each frequency line starts with the frequency, followed by a space ' ', then the maxZ scores separated by comma ',' .
    '''
    maxZFile = open(maxZFilename, 'r')
    maxZsoundDict = {'maxZSoundLow':[],'maxZSoundMid':[],'maxZSoundHigh':[],'behavSession':[]}
    #maxZsoundDict = {}
    behavSessionCount=0 #for keeping track of how many behav session was processed
    '''
    for line in maxZFile:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1]  
            #behavSessionList.append(behavName)
            behavSessionCount+=1
            maxZsoundDict['behavSession'].extend([behavName]*cellNumPerSession)
        else:
            freqLow = int(line.split()[0])
            maxZsoundDict['maxZSoundLow'].extend([float(x) for x in line.split()[1].split(',')[0:-1]])
            #maxZFile.readline()
            freqMid = int(line.split()[0])
            maxZsoundDict['maxZSoundMid'].extend([float(x) for x in line.split()[1].split(',')[0:-1]])
            #maxZFile.readline()
            freqHigh = int(line.split()[0])
            #maxZsoundDict['maxZSoundHigh'].extend([float(x) for x in line.split()[1].split(',')[0:-1]])
    '''
    while True:
        linesOneSession = read_nlines_from_txt_file(maxZFile, 4)
        if not linesOneSession:
            break
        behavLine = linesOneSession[0]
        if behavLine.startswith(codecs.BOM_UTF8):
            behavLine = line[3:]
        if (behavLine.split(':')[0] == 'Behavior Session'):
            behavName = behavLine.split(':')[1][:-1]  
            #behavSessionList.append(behavName)
            behavSessionCount+=1
            maxZsoundDict['behavSession'].extend([behavName]*cellNumPerSession)
        freqLowLine = linesOneSession[1]
        maxZsoundDict['maxZSoundLow'].extend([float(x) for x in freqLowLine.split()[1].split(',')[0:-1]])
        freqMidLine = linesOneSession[2]
        maxZsoundDict['maxZSoundMid'].extend([float(x) for x in freqMidLine.split()[1].split(',')[0:-1]])
        freqHighLine = linesOneSession[3]
        maxZsoundDict['maxZSoundHigh'].extend([float(x) for x in freqHighLine.split()[1].split(',')[0:-1]])

    maxZFile.close()
    maxZsoundDf = pd.DataFrame(maxZsoundDict)     
    #print maxZsound[100:150]
    maxZsoundDf.sort('behavSession',ascending=True,inplace=True)
    maxZsoundDf = maxZsoundDf.reset_index(drop=True)
    #maxZsound = maxZsound.values() #This gets a numpy matrix of the values
    
    return maxZsoundDf #This is a DataFrame with columns 'maxZSoundLow', 'maxZSoundMid', 'maxZSoundHigh', and 'behaveSession'


def read_ISI_violation_file_return_Df(ISIFilename):
    '''
    File format: file starts with behavSession line ('Behavior Session:behavSession\n'), followed by one line for the ISI violation percentage for all possible clusters in this session, separated by comman ','.
    '''
    ISIFile = open(ISIFilename, 'r')
    behavSessionCount=0
    ISIDict = {'behavSession':[],'ISI':[]}
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
    ISIDf = pd.DataFrame(ISIDict)
    #print ISI[100:150]
    ISIDf.sort('behavSession',ascending=True,inplace=True)
    ISIDf = ISIDf.reset_index(drop=True)
    #ISI = ISI['ISI'].values()
    
    return ISIDf #This is a Df two cols: 'behavSession' and 'ISI'


def read_mod_index_switching_return_Df(modIndexFilename):
    '''
    File format: each session's record starts with one line for the behavior session name (e.g. "Behavior Session:20160414a"). This is followed by a new line containing the modI values for every cluster for the middle frequency (start with 'modI:' modIndex separated by ','). Next is a new line containing the p value significance for the modulation of the middle frequency for every cluster (start with 'modSig:' mod significance separated by ','). Last new line is the modulation direction score ((start with 'modDir:' mod dir score separated by ',').  
    '''
    modIFile = open(modIndexFilename, 'r')
    modulationDict = {'modIndex':[],'modSig':[],'behavSession':[]} #stores all the modulation indices for the middle frequency
    #modSigDict = {} #stores the significance of the modulation of each cell
    #modDirectionScoreDict = {} #stores the score of how often the direction of modulation changes
    behavName = ''
    behavName = ''
    for line in modIFile:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        splitLine = line.split(':')
        if (splitLine[0] == 'Behavior Session'):
            behavName = splitLine[1][:-1]
            modulationDict['behavSession'].extend([behavName]*cellNumPerSession)
        elif (splitLine[0] == 'modI'):
            modulationDict['modIndex'].extend([float(x) for x in splitLine[1].split(',')[0:-1]])
        elif (splitLine[0] == 'modSig'):
            modulationDict['modSig'].extend([float(x) for x in splitLine[1].split(',')[0:-1]])
        elif (splitLine[0] == 'modDir'):
            pass
            #modDirectionScoreDict[behavName] = [float(x) for x in splitLine[1].split(',')[0:-1]]

    modIFile.close()
    modulationDf = pd.DataFrame(modulationDict)
    modulationDf.sort('behavSession',ascending=True,inplace=True) #sort dataframe so that behavSessions are in ascending order
    modulationDf = modulationDf.reset_index(drop=True)
    return modulationDf

def read_movement_modI_return_Df(movementModIFilename):
    movementModIFile = open(movementModIFilename, 'r')
    movementModIDict = {'movementModI':[], 'behavSession':[]}
    
    for line in movementModIFile:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1]  
            #behavSessionList.append(behavName)
            #behavSessionCount+=1
            movementModIDict['behavSession'].extend([behavName]*cellNumPerSession)
        else:
            movementModIDict['movementModI'].extend([float(x) for x in line.split(',')[0:-1]])
    movementModIDf=pd.DataFrame(movementModIDict)
    movementModIDf.sort('behavSession',ascending=True,inplace=True)
    movementModIDf=movementModIDf.reset_index(drop=True)
    return movementModIDf


def read_movement_modS_return_Df(movementModSFilename):
    movementModSFile = open(movementModSFilename, 'r')
    movementModSDict = {'movementModS':[], 'behavSession':[]}
    
    for line in movementModSFile:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1]  
            #behavSessionList.append(behavName)
            #behavSessionCount+=1
            movementModSDict['behavSession'].extend([behavName]*cellNumPerSession)
        else:
            movementModSDict['movementModS'].extend([float(x) for x in line.split(',')[0:-1]])
    movementModSDf=pd.DataFrame(movementModSDict)
    movementModSDf.sort('behavSession',ascending=True,inplace=True)
    movementModSDf=movementModSDf.reset_index(drop=True)
    return movementModSDf


def read_min_performance_file_return_list(minPerfFilename):
    '''
    File format: file starts with one line describing the minimal performance criterion/cut-off, followed by all the session names for sessions that passed the cut-off, each session name is one line.
    '''
    minPerfFile = open(minPerfFilename, 'r')
    minPerfFile.readline()
    minPerfList=minPerfFile.read().split()
    minPerfFile.close()
    return minPerfList #This is a list of all sessions that passed the check (may not contain all behavSessions recorded in the all_cells file)


def read_min_trial_file_return_dict(minTrialFilename):
    '''
    File format: file starts with one line describing the minimal trial number criterion/cut-off. This line is followed by an empty line, then behavior sessions names (e.g. 20160229a) of all the sessions are listed, one on each line, along with the middle frequency presented in that session if it passed the min trial test (e.g. "20160412a: 11000") 
    '''
    minTrialFile = open(minTrialFilename, 'r')
    minTrialFile.readline()
    minTrialFile.readline()
    minTrialDict= {}
    for lineCount,line in enumerate(minTrialFile):
        minTrialStr = line.split(':')
        trialFreq = minTrialStr[1].split()
        minTrialDict.update({minTrialStr[0][1:]:trialFreq})
        # if the session's middle frequency does not pass the minimum trial criteria, the value of that session's key will be empty.
    minTrialFile.close()
    return minTrialDict #this is a dict with behav sessions as keys and mid freq as value if that session passed this check 




if __name__ == '__main__':
    mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
    allcellsFileName = 'allcells_'+mouseName
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)


    # - Directory storing all computed measurements in txt files -- #
    processedDir = os.path.join(settings.EPHYS_PATH,mouseName,mouseName+'_stats')

    measurementFiles = [os.path.join(processedDir, f) for f in os.listdir(processedDir) if os.path.isfile(os.path.join(processedDir, f))]
    dfs = []
    for filename in measurementFiles:
        if 'maxZVal' in filename:
            maxZsoundDf = read_sound_maxZ_file_switching_return_Df(filename)
            dfs.append(maxZsoundDf)
        elif 'ISI' in filename:
            ISIDf = read_ISI_violation_file_return_Df(filename)
            dfs.append(ISIDf)
        elif ('modIndex' in filename) & ('movement' not in filename):
            modulationDf = read_mod_index_switching_return_Df(filename)
            dfs.append(modulationDf)
        elif 'minTrial' in filename:
            minTrialDict = read_min_trial_file_return_dict(filename) 
            
        elif 'minPerformance' in filename:
            minPerfList = read_min_performance_file_return_list(filename)

        elif 'movement' in filename:
            if 'modIndex' in filename:
                movementIDf = read_movement_modI_return_Df(filename)
            elif 'modSig' in filename:
                movementSDf = read_movement_modS_return_Df(filename)
            dfs.append([movementIDf,movementSDf])

    #--Filter behavSessions by minPerformance --#
    maxZsoundDf = maxZsoundDf[maxZsoundDf['behavSession'].isin(minPerfList)]
    #--Joining all the resulting dataFrames on 'behavSession' column --#
    df_final = reduce(lambda left,right: pd.merge(left,right,on='behavSession',how='inner'), dfs)
