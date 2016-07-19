import time
import pandas as pd
from jaratoolbox import settings_2 as settings
import sys
import importlib
import os
import codecs
from subprocess import call 

#call("python test026_add_ModIndex_difOnset_reward_change.py side-in 0 0.1 adap012".split())
call("python test026_add_ModIndex_difOnset_reward_change.py side-in -0.1 0 adap012".split())
#call("python test026_add_ModIndex_difOnset_reward_change.py sound 0 0.1 adap012".split())

#call("python test026_add_ModIndex_difOnset_reward_change.py sound 0 0.15 adap012".split())

#call("python test026_add_ModIndex_difOnset_reward_change.py side-in 0 0.2 adap012".split())
#call("python test026_add_ModIndex_difOnset_reward_change.py center-out 0 0.2 adap012".split())

#call("python test026_add_ModIndex_difOnset_reward_change.py center-out 0 0.2 adap012".split())

'''
clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes
cellNumPerSession=clusNum*numTetrodes
subject = sys.argv[1]
allcellsFileName = 'allcells_'+subject
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)
outputDir = '/home/languo/data/ephys/'+subject+'/'
processedDir = os.path.join(outputDir,subject+'_stats')

listOfmodSMeasures = ['sound_0to0.1sec','sound_0to0.15sec','center-out_-0.1to0sec','center-out_0to0.1sec', 'center-out_0to0.2sec','side-in_-0.1to0sec', 'side-in_0to0.1sec', 'side-in_0to0.2sec']
listOfmodSFilenames = ['modSig_'+i+'_window_'+subject+'.txt' for i in listOfmodSMeasures]
listOfmodSFullFilenames = [os.path.join(processedDir,file) for file in listOfmodSFilenames]
listOfmodSFiles = [open(i, 'r') for i in listOfmodSFullFilenames]

modS=pd.DataFrame()
for (key,filename) in zip(listOfmodSMeasures,listOfmodSFiles):
    behavSessionCount=0
    behavSessionList=[]
    modSDict = {}
    modSDict.update({('modS'+key+'Left'):[],('modS'+key+'Right'):[],'behavSession':[]})
 
    for line in filename:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1]  
            behavSessionList.append(behavName)
            behavSessionCount+=1
            modSDict['behavSession'].extend([behavName]*cellNumPerSession)
        else:
            freq=int(line.split()[0])
            if freq < 9500:
                modSDict['modS'+key+'Left'].extend([float(x) for x in line.split()[1].split(',')[0:-1]])
            elif freq > 13400: #some sessions have a mid freq
                modSDict['modS'+key+'Right'].extend([float(x) for x in line.split()[1].split(',')[0:-1]])
    modS_current=pd.DataFrame(modSDict)
    modS_current.sort('behavSession',ascending=True,inplace=True)
    modS_current=modS_current.reset_index(drop=True)

    modS=pd.concat([modS,modS_current],axis=1)
    #modS[key+'Right']=modS_current[key+'Right']
    #behavSessionNum_movementmodI=behavSessionCount
    print 'read in', key, behavSessionCount, behavSessionList
    
#modS=pd.DataFrame(modSDict)
for f in listOfmodSFiles:
    f.close() 
'''
