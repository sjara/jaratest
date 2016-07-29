'''
Script to read all separately written measurements: BehavSession, CellQuality, Tetrode, Cluster, ISIviolation,maxZsound,maxZmovement,modulationIndex(for reward and movement) and modulationSignificance into one csv file.
Added waveform measures (the times and magnitudes of the capacitive peak, sodium peak, and potasium peak respectively). 

-Last updated 2016-05-18 LG

'''

import time
import pandas as pd
from jaratoolbox import settings_2 as settings
import sys
import importlib
import os
import codecs
import numpy as np

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes
cellNumPerSession=clusNum*numTetrodes
all_measures=pd.DataFrame()
#############################################################################
subject = sys.argv[1]
allcellsFileName = 'allcells_'+subject
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)
outputDir = '/home/languo/data/ephys/'+subject+'/'
processedDir = os.path.join(outputDir,subject+'_stats')
###########################################################################
#THIS IS ANIMAL SPECIFIC. some sessions have a mid freq in addition to high and low frequencies, don't want to include all three frequencies otherwise array will be of different size. Set boundaries so that all low frequencies and high frequencies in all experiments are included but the middle frequencies are left out from the database

if subject=='adap012':
    lowFreqBoundary= 9500 #in Hz 
    highFreqBoundary= 13400
elif subject=='adap005':
    lowFreqBoundary= 9000 #in Hz 
    highFreqBoundary= 10000
elif subject=='adap013':
    lowFreqBoundary= 9000 #in Hz 
    highFreqBoundary= 11000
elif subject=='adap015':
    lowFreqBoundary= 9000 #in Hz 
    highFreqBoundary= 10000
elif subject=='adap017':
    lowFreqBoundary= 9000 #in Hz 
    highFreqBoundary= 12000
elif subject=='d1pi003':
    lowFreqBoundary= 8000 #in Hz 
    highFreqBoundary= 13000

############################## Cell Quality #########################################
cellsThisAnimal=allcells.cellDB
cellQuality=[]
for oneCell in cellsThisAnimal:
    cellQuality.append(oneCell.quality)

all_measures['cellQuality']=pd.DataFrame(cellQuality)

##################################################################################

############################## ISI,Tetrode,Cluster,behavSession #########################################
ISIFilename = os.path.join(processedDir,'ISI_Violations_'+subject+'.txt')
ISIFile = open(ISIFilename, 'r')

behavSessionCount=0
#cellIndex=range(cellNumPerSession)
behavSessionList=[]
ISIDict={'ISI':[],'behavSession':[]}
#start1=time.clock()
for line in ISIFile:
    if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
    if (line.split(':')[0] == 'Behavior Session'):
        behavName = line.split(':')[1][:-1] 
        behavSessionList.append(behavName)
        behavSessionCount+=1
        ISIDict['behavSession'].extend([behavName]*cellNumPerSession)
    else:
        ISIDict['ISI'].extend([float(x) for x in line.split(',')[0:-1]])
ISIFile.close()      

behavSessionNum_ISI=behavSessionCount
ISI=pd.DataFrame(ISIDict)
#print ISI[100:150]
ISI.sort('behavSession',ascending=True,inplace=True)
ISI=ISI.reset_index(drop=True)
#print ISI[100:150]

all_measures['behavSession']=ISI['behavSession']
all_measures['Tetrode']=np.tile(np.repeat(range(1,9), 12),behavSessionCount)
all_measures['Cluster']=np.tile(np.tile(range(1,13), 8),behavSessionCount)
all_measures['ISI']=ISI['ISI']

#end1=time.clock()
#processTime1=end1-start1
#print processTime1,behavSessionList
print 'read-in ISI: ', behavSessionCount, 'sessions'
############################################################################

#################### maxZ for sound responsiveness #########################
maxZFilename = os.path.join(processedDir,'maxZVal_'+subject+'.txt')
maxZFile = open(maxZFilename, 'r')
maxZsoundDict = {'maxZSoundLeft':[],'maxZSoundRight':[],'behavSession':[]}
behavSessionCount=0
behavSessionList=[]
cellIndex=range(cellNumPerSession)
start=time.clock()
for line in maxZFile:
    if line.startswith(codecs.BOM_UTF8):
        line = line[3:]
    if (line.split(':')[0] == 'Behavior Session'):
        behavName = line.split(':')[1][:-1]  
        behavSessionList.append(behavName)
        behavSessionCount+=1
        maxZsoundDict['behavSession'].extend([behavName]*cellNumPerSession)
    else:
        freq=int(line.split()[0])
        if freq <= lowFreqBoundary:
            maxZsoundDict['maxZSoundLeft'].extend([float(x) for x in line.split()[1].split(',')[0:-1]])
        elif freq >= highFreqBoundary: #some sessions have a mid freq, don't want to include all three frequencies otherwise array will be of different size, THIS MIGHT BE ANIMAL SPECIFIC
            maxZsoundDict['maxZSoundRight'].extend([float(x) for x in line.split()[1].split(',')[0:-1]])

behavSessionNum_maxZsound=behavSessionCount
maxZsound=pd.DataFrame(maxZsoundDict)
#print maxZsound[100:150]
maxZsound.sort('behavSession',ascending=True,inplace=True)
maxZsound=maxZsound.reset_index(drop=True)

all_measures['maxZSoundLeft']=maxZsound['maxZSoundLeft']
all_measures['maxZSoundRight']=maxZsound['maxZSoundRight']

#print maxZsound[100:150]
#end=time.clock()
maxZFile.close()
print 'read-in sound maxZ: ', behavSessionCount, 'sessions'
#################################################################################

#################### maxZ for movement responsiveness ################
nameOfmovementmaxZFile = 'maxZVal_movement_150to300msAfterSound_'+subject+'.txt'
movementmaxZFilename = os.path.join(processedDir,nameOfmovementmaxZFile)

movementmaxZFile = open(movementmaxZFilename, 'r')
maxZmovementDict = {'maxZMovementLeft':[],'maxZMovementRight':[],'behavSession':[]}
behavSessionCount=0
behavSessionList=[]
cellIndex=range(cellNumPerSession)
#start=time.clock()
for line in movementmaxZFile:
    if line.startswith(codecs.BOM_UTF8):
        line = line[3:]
    if (line.split(':')[0] == 'Behavior Session'):
        behavName = line.split(':')[1][:-1]  
        behavSessionList.append(behavName)
        behavSessionCount+=1
        maxZmovementDict['behavSession'].extend([behavName]*cellNumPerSession)
    else:
        freq=int(line.split()[0])
        if freq <= lowFreqBoundary:
            maxZmovementDict['maxZMovementLeft'].extend([float(x) for x in line.split()[1].split(',')[0:-1]])
        elif freq >= highFreqBoundary: #some sessions have a mid freq
            maxZmovementDict['maxZMovementRight'].extend([float(x) for x in line.split()[1].split(',')[0:-1]])
behavSessionNum_maxZmovement=behavSessionCount
maxZmovement=pd.DataFrame(maxZmovementDict)

maxZmovement.sort('behavSession',ascending=True,inplace=True)
maxZmovement=maxZmovement.reset_index(drop=True)

all_measures['maxZMovementLeft']=maxZmovement['maxZMovementLeft']
all_measures['maxZMovementRight']=maxZmovement['maxZMovementRight']
#end=time.clock()

movementmaxZFile.close()
#print end-start, behavSessionList
print 'read-in movement maxZ: ', behavSessionCount, 'sessions'
######################################################################

#################### maxZ for laser responsiveness ################
if subject == 'd1pi003':
    nameOflasermaxZFile = 'maxZVal_laser_'+subject+'.txt'
    lasermaxZFilename = os.path.join(processedDir,nameOflasermaxZFile)

    lasermaxZFile = open(lasermaxZFilename, 'r')
    maxZlaserDict = {'maxZLaser':[],'behavSession':[]}
    behavSessionCount=0
    behavSessionList=[]
    cellIndex=range(cellNumPerSession)
    #start=time.clock()
    for line in lasermaxZFile:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1]  
            behavSessionList.append(behavName)
            behavSessionCount+=1
            maxZlaserDict['behavSession'].extend([behavName]*cellNumPerSession)
        else:
            maxZlaserDict['maxZLaser'].extend([float(x) for x in line.split(',')[0:-1]])
           
    behavSessionNum_maxZmovement=behavSessionCount
    maxZlaser=pd.DataFrame(maxZlaserDict)

    maxZlaser.sort('behavSession',ascending=True,inplace=True)
    maxZlaser=maxZlaser.reset_index(drop=True)

    all_measures['maxZLaser']=maxZlaser['maxZLaser']
    #end=time.clock()

    lasermaxZFile.close()
    #print end-start, behavSessionList
    print 'read-in laser maxZ: ', behavSessionCount, 'sessions'
###############################################################################

######################### L-R movement Modulation Index ###########################
nameOfmovementmodIFile_1 = 'modIndex_'+'LvsR_movement_0to0.1sec_window_'+subject+'.txt'
movementmodIFilename_1 = os.path.join(processedDir,nameOfmovementmodIFile_1)
nameOfmovementmodIFile_2 = 'modIndex_'+'LvsR_movement_0to0.2sec_window_'+subject+'.txt'
movementmodIFilename_2 = os.path.join(processedDir,nameOfmovementmodIFile_2)

movementmodIFile_1=open(movementmodIFilename_1, 'r')
movementmodIFile_2=open(movementmodIFilename_2, 'r')

#movementmodIDict = {}
movementmodI=pd.DataFrame()
#cellIndex=range(cellNumPerSession)
#start2=time.clock()
movementmodIMeasures={'movementmodI0-0.1':movementmodIFile_1, 'movementmodI0-0.2':movementmodIFile_2}
listOfmovementmodIMeasures=['movementmodI0-0.1','movementmodI0-0.2']
listOfmovementmodIFiles=[movementmodIFile_1,movementmodIFile_2]

for (key,filename) in movementmodIMeasures.items(): #zip(listOfmovementmodIMeasures,listOfmovementmodIFiles):
    behavSessionCount=0
    behavSessionList=[]
    movementmodIDict = {}
    movementmodIDict.update({key:[],'behavSession':[]})
    for line in filename:
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1]  
            behavSessionList.append(behavName)
            behavSessionCount+=1
            movementmodIDict['behavSession'].extend([behavName]*cellNumPerSession)
        else:
            movementmodIDict[key].extend([float(x) for x in line.split(',')[0:-1]])
    movementmodI_current=pd.DataFrame(movementmodIDict)
    movementmodI_current.sort('behavSession',ascending=True,inplace=True)
    movementmodI_current=movementmodI_current.reset_index(drop=True)
    
    all_measures[key]=movementmodI_current[key]
    #behavSessionNum_movementmodI=behavSessionCount
    print 'read in', key, behavSessionCount

movementmodIFile_1.close()
movementmodIFile_2.close()
#end2=time.clock()
#processTime2=end2-start2
#print processTime2, behavSessionList
######################################################################################

######################## L-R movement Modulation Significance ########################

nameOfmovementmodSFile_1 = 'modSig_'+'LvsR_movement_0to0.1sec_window_'+subject+'.txt'
movementmodSFilename_1 = os.path.join(processedDir,nameOfmovementmodSFile_1)
nameOfmovementmodSFile_2 = 'modSig_'+'LvsR_movement_0to0.2sec_window_'+subject+'.txt'
movementmodSFilename_2 = os.path.join(processedDir,nameOfmovementmodSFile_2)
movementmodSFile_1=open(movementmodSFilename_1, 'r')
movementmodSFile_2=open(movementmodSFilename_2, 'r')

movementmodSDict = {}
behavSessionCount=0
behavSessionList=[]
#cellIndex=range(cellNumPerSession)
#start2=time.clock()

movementmodSMeasures={'movementmodS0-0.1':movementmodSFile_1, 'movementmodS0-0.2':movementmodSFile_2}

for (key,filename) in movementmodSMeasures.items(): #zip(listOfmovementmodIMeasures,listOfmovementmodIFiles):
    behavSessionCount=0
    behavSessionList=[]
    movementmodSDict = {}
    movementmodSDict.update({key:[],'behavSession':[]})
    for line in filename:
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1]  
            behavSessionList.append(behavName)
            behavSessionCount+=1
            movementmodSDict['behavSession'].extend([behavName]*cellNumPerSession)
        else:
            movementmodSDict[key].extend([float(x) for x in line.split(',')[0:-1]])
    movementmodS_current=pd.DataFrame(movementmodSDict)
    movementmodS_current.sort('behavSession',ascending=True,inplace=True)
    movementmodS_current=movementmodS_current.reset_index(drop=True)
    
    all_measures[key]=movementmodS_current[key]
    #behavSessionNum_movementmodI=behavSessionCount
    print 'read in', key, behavSessionCount

movementmodSFile_1.close()
movementmodSFile_2.close()

#end2=time.clock()
#processTime2=end2-start2
#print processTime2, behavSessionList
################################################################################


##################### Reward Modulation Index #################################
listOfmodIMeasures = ['sound_0to0.1sec','sound_0to0.15sec','center-out_-0.1to0sec','center-out_0to0.1sec', 'center-out_0to0.2sec','side-in_-0.1to0sec', 'side-in_0to0.1sec', 'side-in_0to0.2sec']
listOfmodIFilenames = ['modIndex_'+i+'_window_'+subject+'.txt' for i in listOfmodIMeasures]
listOfmodIFullFilenames = [os.path.join(processedDir,file) for file in listOfmodIFilenames]
listOfmodIFiles = [open(i, 'r') for i in listOfmodIFullFilenames]

modI=pd.DataFrame()

for (key,filename) in zip(listOfmodIMeasures,listOfmodIFiles):
    behavSessionCount=0
    behavSessionList=[]
    modIDict = {}
    modIDict.update({('modI'+key+'Left'):[],('modI'+key+'Right'):[],'behavSession':[]})
    
    for line in filename:
        if line.startswith(codecs.BOM_UTF8):
            line = line[3:]
        if (line.split(':')[0] == 'Behavior Session'):
            behavName = line.split(':')[1][:-1]  
            behavSessionList.append(behavName)
            behavSessionCount+=1
            modIDict['behavSession'].extend([behavName]*cellNumPerSession)
        else:
            freq=int(line.split()[0])
            if freq <= lowFreqBoundary:
                modIDict['modI'+key+'Left'].extend([float(x) for x in line.split()[1].split(',')[0:-1]])
            elif freq >= highFreqBoundary: #some sessions have a mid freq
                modIDict['modI'+key+'Right'].extend([float(x) for x in line.split()[1].split(',')[0:-1]])
    modI_current=pd.DataFrame(modIDict)
    modI_current.sort('behavSession',ascending=True,inplace=True) #sort dataframe so that behavSessions are in ascending order
    modI_current=modI_current.reset_index(drop=True) #sort function somehow doesn't change index so have to reset it manually before merging
    
    all_measures['modI'+key+'Left']=modI_current['modI'+key+'Left']
    all_measures['modI'+key+'Right']=modI_current['modI'+key+'Right']
    #behavSessionNum_movementmodI=behavSessionCount
    print 'read in', key, behavSessionCount, behavSessionList

for f in listOfmodIFiles:
    f.close() 
##################################################################################


#################### Reward Modulation Significance #################################
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
            if freq <= lowFreqBoundary:
                modSDict['modS'+key+'Left'].extend([float(x) for x in line.split()[1].split(',')[0:-1]])
            elif freq >= highFreqBoundary: #some sessions have a mid freq
                modSDict['modS'+key+'Right'].extend([float(x) for x in line.split()[1].split(',')[0:-1]])
    modS_current=pd.DataFrame(modSDict)
    modS_current.sort(['behavSession'],ascending=True,inplace=True)
    modS_current=modS_current.reset_index(drop=True)
    all_measures['modS'+key+'Left']=modS_current['modS'+key+'Left']
    all_measures['modS'+key+'Right']=modS_current['modS'+key+'Right']
    #behavSessionNum_movementmodI=behavSessionCount
    print 'read in', key, behavSessionCount, behavSessionList

#modS=pd.DataFrame(modSDict)
for f in listOfmodSFiles:
    f.close() 
###################################################################################

############## Waveform #####################################################################

waveformData = pd.DataFrame(index=range(0,len(cellsThisAnimal)), columns=['peakCapAmp','peakNaAmp','peakKAmp','peakCapTime','peakNaTime','peakKTime','widthWaveform'])

for index,oneCell in enumerate(cellsThisAnimal):
    
    if oneCell.quality!=1 and oneCell.quality!=6:
        waveformDataThis=[0,0,0,0,0,0,0]
    else:
        spkData = ephyscore.CellData(oneCell)
        #waveforms = spkData.spikes.samples
        waveforms = spkData.spikes.samples.astype(float) - 2**15 # FIXME: this is specific to OpenEphys
        # FIXME: This assumes the gain is the same for all channels and records
        waveforms = (1000.0/spkData.spikes.gain[0,0]) * waveforms #this converts waveforms's unit to uV
        samplingRate = spkData.spikes.samplingRate

        (peakTimes, peakAmplitudes, avWaveform) = spikesorting.estimate_spike_peaks(waveforms,samplingRate)
        peakCapAmp,peakNaAmp,peakKAmp=peakAmplitudes
        peakCapTime,peakNaTime,peakKTime=peakTimes
        widthWaveform=peakKTime-peakCapTime
        waveformDataThis=[peakCapAmp,peakNaAmp,peakKAmp,peakCapTime,peakNaTime,peakKTime,widthWaveform]
    waveformData.ix[index,:]=waveformDataThis

all_measures=pd.concat((all_measures,waveformData), axis=1)
##############################################################################################

############### Write to csv file###########################################
all_measuresFilename=processedDir+'/all_measures_'+subject+'.csv'
all_measures.to_csv(all_measuresFilename)


 

   
