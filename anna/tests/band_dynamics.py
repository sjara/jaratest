import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from jaratoolbox import extrafuncs
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

from jaratest.anna.analysis import band_behaviour_analysis
reload(band_behaviour_analysis)


def rsync_behavior(subject, server = 'jarauser@jarahub', serverBehavPath = '/data/behavior'):
    import subprocess
    fullRemotePath = os.path.join(serverBehavPath, subject)
    serverDataPath = '{}:{}'.format(server, fullRemotePath)
    localDataPath = os.path.join(settings.BEHAVIOR_PATH) + os.sep
    transferCommand = ['rsync', '-av', serverDataPath, localDataPath]
    subprocess.call(transferCommand)
    
def rsync_all_behaviour(subjects):
    for subject in subjects:
        rsync_behavior(subject)
        
def plot_dynamics(behavData,winsize=40,fontsize=12):
    '''
    Plot performance in time for one session.
    First argument is an object created by loadbehavior.BehaviorData (or subclasses)
    '''
    ax = plt.gca()
    ax.cla()
    lineWidth = 2
    possibleRewardSide = np.unique(behavData['rewardSide'])
    possibleColors = ['b','r']
    rightChoice = behavData['choice']==behavData.labels['choice']['right']

    hPlots = []
    plt.hold(True)
    valid = behavData['valid'].astype(bool)
    for indr,thisSide in enumerate(possibleRewardSide):
        thisColor = possibleColors[indr]
        trialsThisSide = (behavData['rewardSide']==thisSide)
        choiceVecThisSide = np.ma.masked_array(rightChoice[valid])
        choiceVecThisSide.mask = ~trialsThisSide[valid]
        movAvChoice = extrafuncs.moving_average_masked(choiceVecThisSide,winsize)
        hp, = plt.plot(range(0,len(movAvChoice)),100*movAvChoice,
                       lw=lineWidth,color=thisColor)
        hPlots.append(hp)
    plt.ylim([-5,105])
    plt.axhline(50,color='0.5',ls='--')
    plt.ylabel('% rightward',fontsize=fontsize)
    plt.xlabel('Trial',fontsize=fontsize)
    extraplots.set_ticks_fontsize(ax,fontsize)
    #plt.draw()
    #plt.show()
    return hPlots

def plot_multibandwidth_psychometric(behavData):
    ax = plt.gca()
    ax.cla()
    possibleRewardSide = np.unique(behavData['rewardSide'])
    possibleBands = np.unique(behavData['currentBand'])
    possibleColors = plt.cm.rainbow(np.linspace(0,1,len(possibleBands)))
    trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['currentBand'], 
                                                                   possibleBands, 
                                                                   behavData['rewardSide'], 
                                                                   possibleRewardSide)
    valid = behavData['valid'].astype(bool)
    rightChoice = behavData['choice']==behavData.labels['choice']['right']
    
    patches=[]
    for indb, thisBand in enumerate(possibleBands):
        thisColor = possibleColors[indb]
        trialsThisBand = trialsEachCond[:,indb,:]
        thisBandPerformance = []
        for indr in range(len(possibleRewardSide)):
            trialsThisSide = trialsThisBand[:,indr]
            validThisSide = np.sum(trialsThisSide.astype(int)[valid])
            rightThisSide = np.sum(trialsThisSide.astype(int)[rightChoice])
            #pdb.set_trace()
            thisBandPerformance.append(100.0*rightThisSide/validThisSide)
        plt.plot([0,1], thisBandPerformance, color=thisColor, marker='o', lw=3, ms=10)
        patches.append(mpatches.Patch(color=thisColor, label=str(thisBand)))
    plt.ylim((0,100))
    plt.xlim((-0.2,1.2))
    plt.ylabel("% rightward")
    labels = ['no tone','tone']
    plt.xticks([0,1], labels)
    plt.legend(handles=patches, borderaxespad=0.3,prop={'size':12}, loc='best')
        
def time_differences_by_trial(animal, sessions, sortBy, paradigm = '2afc', triggers = ['Cin', 'Cout']):
    timeDiff = []
    import pdb
    for ind,session in enumerate(sessions):
        behavFile = os.path.join(settings.BEHAVIOR_PATH,animal,animal+'_2afc_'+session+'.h5')
        behavData = loadbehavior.BehaviorData(behavFile,readmode='full')
        possibleSort = np.unique(behavData[sortBy])
        while len(possibleSort)>len(timeDiff):
            timeDiff.append([])
            print len(timeDiff)
        trialsEachCond = behavioranalysis.find_trials_each_type(behavData[sortBy], possibleSort)
        eventCode = np.array(behavData.events['eventCode'])
        eventTime = behavData.events['eventTime']
        nextState = behavData.events['nextState']
        trialEnd = np.where(nextState==behavData.stateMatrix['statesNames']['startTrial'])[0][1:]
        try:
            start = np.where(eventCode==behavData.stateMatrix['eventsNames'][triggers[0]])[0]
        except KeyError:
            start = np.where(nextState==behavData.stateMatrix['statesNames'][triggers[0]])[0]+1
        try:
            stop = np.where(eventCode==behavData.stateMatrix['eventsNames'][triggers[1]])[0]
        except KeyError:
            stop = np.where(nextState==behavData.stateMatrix['statesNames'][triggers[1]])[0]+1
        for ind2 in range(len(possibleSort)):
            trialsThisCond = trialsEachCond[:,ind2]
            if len(trialsThisCond) > len(trialEnd):
                trialsThisCond = trialsThisCond[:-1]
            trialEndThisCond = trialEnd[trialsThisCond]
            startThisCond = np.zeros(sum(trialsThisCond))
            stopThisCond = np.zeros(sum(trialsThisCond))
            #pdb.set_trace()
            for i in range(len(trialEndThisCond)):
                startThisCond[i] = max(j for j in start if j < trialEndThisCond[i])
                stopThisCond[i] = min(k for k in stop if k > startThisCond[i])
            startThisCond = startThisCond.astype(int)
            stopThisCond = stopThisCond.astype(int)
            startTime = eventTime[startThisCond]
            stopTime = eventTime[stopThisCond]
            diffThisCond = stopTime - startTime
            #pdb.set_trace()
            timeDiff[ind2].extend(diffThisCond)
    return timeDiff, possibleSort
        
    
    

if __name__ == '__main__':
    

    CASE=2

    animalNames = ['band0'+str(number) for number in [78,79,80,82,83,84,85,86]]
    #animalNames = ['adap064', 'adap070']
    session = '20190409a'
    
    #rsync_all_behaviour(animalNames)
    
    if CASE==0:
        plt.figure()
        
        for ind,animal in enumerate(animalNames):
            plt.subplot(2,5,ind+1)
            behavFile = os.path.join(settings.BEHAVIOR_PATH,animal,animal+'_2afc_'+session+'.h5')
            behavData = loadbehavior.BehaviorData(behavFile,readmode='full')
            plot_dynamics(behavData)
            plt.title(animal)
        plt.suptitle(session)
        plt.show()
        
        plt.figure()
        for ind,animal in enumerate(animalNames):
            plt.subplot(2,5,ind+1)
            behavFile = os.path.join(settings.BEHAVIOR_PATH,animal,animal+'_2afc_'+session+'.h5')
            behavData = loadbehavior.BehaviorData(behavFile,readmode='full')
            plot_multibandwidth_psychometric(behavData)
            plt.title(animal)
        plt.suptitle(session)
        plt.show()
        
    elif CASE==1:
        animals = ['band0'+str(number) for number in [81,87]]
        #sessions = ['20180929a','20180930a', '20181001a','20181002a','20181003a','20181004a']
        sessions = ['20190214a']
        rsync_all_behaviour(animalNames)
        
        plt.figure()
        for ind, animal in enumerate(animals):
            plt.subplot(2,3,ind+1)
            validPerCond, rightPerCond, possibleConds = band_behaviour_analysis.band_psychometric(animal, sessions, trialTypes=['currentBand','currentSNR'])
            bandColours = ['k','r']
            patches = []
            for band in range(len(possibleConds[0])):
                band_behaviour_analysis.plot_band_psychometric(validPerCond[band,:], rightPerCond[band,:], possibleConds[1], colour = bandColours[band])
                patches.append(mpatches.Patch(color=bandColours[band], label=possibleConds[0][band]))
            plt.legend(handles=patches, borderaxespad=0.3,prop={'size':12}, loc='best')
            plt.title(animal)

        plt.show()
