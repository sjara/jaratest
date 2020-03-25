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

import pdb

def rsync_behavior(subject, server = 'jarauser@jarahub', serverBehavPath = '/data/behavior', localDataPath = '/media/jarauser/redWD/2020acsigdet/data/behavior/'):
    import subprocess
    fullRemotePath = os.path.join(serverBehavPath, subject)
    serverDataPath = '{}:{}'.format(server, fullRemotePath)
    localDataPath = localDataPath + os.sep
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
        
def time_differences_by_trial(behavData, paradigm = '2afc', triggers = ['Cin', 'Cout']):
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

    startEvents = np.zeros(len(trialEnd))
    stopEvents = np.zeros(len(trialEnd))
    
    #pdb.set_trace()
    for i in range(len(trialEnd)):
        startEvents[i] = max(j for j in start if j < trialEnd[i])
        stopEvents[i] = min(k for k in stop if k > startEvents[i])
    startEvents = startEvents.astype(int)
    stopEvents = stopEvents.astype(int)
    startTime = eventTime[startEvents]
    stopTime = eventTime[stopEvents]
    timeDiff = stopTime - startTime
    
    return timeDiff
    
    

if __name__ == '__main__':
    

    CASE=0

    #animalNames = ['band'+str(number) for number in range(105,127)]
    animalNames = ['band091', 'band093']
    session = '20200323a'
    
    rsync_all_behaviour(animalNames)
    
    if CASE==0:
        plt.figure()
        
        for ind,animal in enumerate(animalNames):
            plt.subplot(5,4,ind+1)
            behavFile = os.path.join(settings.BEHAVIOR_PATH,animal,animal+'_2afc_'+session+'.h5')
            if os.path.exists(behavFile):
                behavData = loadbehavior.BehaviorData(behavFile,readmode='full')
                plot_dynamics(behavData)
                plt.title(animal)
            else:
                print("{} does not exist".format(behavFile))
        plt.suptitle(session)
        plt.show()
        
        plt.figure()
        for ind,animal in enumerate(animalNames):
            plt.subplot(5,4,ind+1)
            behavFile = os.path.join(settings.BEHAVIOR_PATH,animal,animal+'_2afc_'+session+'.h5')
            if os.path.exists(behavFile):
                behavData = loadbehavior.BehaviorData(behavFile,readmode='full')
                plot_multibandwidth_psychometric(behavData)
                plt.title(animal)
            else:
                print("{} does not exist".format(behavFile))
        plt.suptitle(session)
        plt.show()
        
    elif CASE==1:
        animals = ['band'+str(number) for number in [110, 111, 112]]#, 113, 114, 115, 116, 117, 118, 119, 120]]
        sessions = ['20200320a']
       
#         animals = ['band'+str(number) for number in [105, 107, 108, 109]]
#         sessions = ['20200229a', '20200301a', '20200302a']
        
        plt.figure()
        for ind, animal in enumerate(animals):
            plt.subplot(4,3,ind+1)
            validPerCond, rightPerCond, possibleConds = band_behaviour_analysis.band_psychometric(animal, sessions, trialTypes=['currentBand','currentSNR'])
            bandColours = ['k','r']
            patches = []
            for band in range(len(possibleConds[0])):
                band_behaviour_analysis.plot_band_psychometric(validPerCond[band,:], rightPerCond[band,:], possibleConds[1], colour = bandColours[band])
                patches.append(mpatches.Patch(color=bandColours[band], label=possibleConds[0][band]))
            plt.legend(handles=patches, borderaxespad=0.3,prop={'size':12}, loc='best')
            plt.title(animal)

        plt.show()
        
    elif CASE==2:
#         animal = 'band093'
#            
#         # -- laser --
#         #lasersessions = ['20200115a', '20200116a', '20200117a', '20200119a', '20200120a', '20200122a', '20200123a', '20200128a', '20200129a'] # 15 mW
#         lasersessions = ['20200131a', '20200201a', '20200203a', '20200204a', '20200206a', '20200207a', '20200209a', '20200210a']
#            
#         # -- control --
#         #controlsessions = ['20200118a', '20200121a', '20200124a', '20200130a']
#         controlsessions = ['20200202a', '20200205a', '20200208a', '20200211a']
         
#         lasersessions = ['20200212a', '20200213a', '20200214a', '20200216a', '20200217a', '20200218a', '20200220a', '20200221a', '20200222a']
#         controlsessions = ['20200215a', '20200219a', '20200223a']
        
#         animal = 'band091'
#           
#         # -- laser --
#         #lasersessions = ['20200206a', '20200207a', '20200209a', '20200210a', '20200213a', '20200214a', '20200216a', '20200217a']
#         lasersessions = ['20200301a', '20200302a', '20200303a', '20200305a', '20200306a', '20200308a', '20200311a', '20200312a'] # 15 mW
#           
#         # -- control --
#         #controlsessions = ['20200208a', '20200212a', '20200215a', '20200218a']
#         controlsessions = ['20200304a', '20200307a', '20200309a', '20200310a'] # 15 mW

#         animal = 'band108'
#         
#         lasersessions = ['20200305a', '20200306a', '20200308a']
#         controlsessions = ['20200307a']

#         animal = 'band066'
#          
#         lasersessions = ['20190123a', '20190124a', '20190126a', '20190127a', '20190129a', '20190130a', '20190201a', '20190202a']
#         controlsessions = ['20190125a', '20190128a', '20190131a', '20190203a']
        
#         animal = 'band065'
#         
#         lasersessions = ['20181018a', '20181020a', '20181021a', '20181023a', '20181024a', '20181026a', '20181027a', '20181029a']
#         controlsessions = ['20181019a', '20181022a', '20181025a', '20181028a', '20181105a']
        
#         animal = 'band069'
#         lasersessions = ['20190123a', '20190124a', '20190126a', '20190127a', '20190129a', '20190130a', '20190201a', '20190202a']
#         controlsessions = ['20190125a', '20190128a', '20190131a', '20190203a']
        
#         animal = 'band070'
#         lasersessions = ['20181020a', '20181021a', '20181023a', '20181024a', '20181026a', '20181027a', '20181029a', '20181030a']
#         controlsessions = ['20181019a', '20181022a', '20181025a', '20181028a', '20181105a']

        #animal = 'band081'
#         animal = 'band087'
#         lasersessions = ['20190307a', '20190308a', '20190310a', '20190311a', '20190313a', '20190314a', '20190316a', '20190317a']
#         controlsessions = ['20190309a', '20190312a', '20190315a', '20190318a']

#         animal = 'band110'
#         lasersessions = ['20200321a', '20200322a']
#         controlsessions = ['20200323a']
        
        animal = 'band105'
        lasersessions = ['20200305a', '20200306a', '20200308a', '20200309a', '20200311a', '20200312a', '20200317a', '20200318a']
        controlsessions = ['20200307a', '20200310a', '20200313a', '20200319a']
        
        sessionTypes = [lasersessions, controlsessions]
        sessionLabels = ['laser', 'control']
        
        plt.figure()
        for ind, sessions in enumerate(sessionTypes):
            plt.subplot(1,2,ind+1)
            validPerCond, rightPerCond, possibleConds = band_behaviour_analysis.band_psychometric(animal, sessions, trialTypes=['currentBand','laserSide','currentSNR'])
            bandColours = ['k','r']
            laserLines = ['-', '--','-.', ':']
            patches = []
            for band in range(len(possibleConds[0])):
                for laser in range(len(possibleConds[1])):
                    band_behaviour_analysis.plot_band_psychometric(validPerCond[band,laser,:], rightPerCond[band,laser,:], possibleConds[2], colour=bandColours[band], linestyle=laserLines[laser])
                patches.append(mpatches.Patch(color=bandColours[band], label=possibleConds[0][band]))
            plt.legend(handles=patches, borderaxespad=0.3,prop={'size':12}, loc='best')
            plt.title(sessionLabels[ind])
        plt.suptitle(animal)

        plt.show()
        
    elif CASE==3:
        animal = 'band093'
        lasersessions = ['20200115a', '20200116a', '20200117a', '20200119a', '20200120a', '20200122a', '20200123a', '20200128a', '20200129a']
        
        waitTimes = [[],[]]
        
        for session in lasersessions:
            behavFile = os.path.join(settings.BEHAVIOR_PATH,animal,animal+'_2afc_'+session+'.h5')
            behavData = loadbehavior.BehaviorData(behavFile,readmode='full')
            timeDiffs = time_differences_by_trial(behavData, triggers=['playNoiseStimulus','Cout'])
            
            trialsEachLaser = behavioranalysis.find_trials_each_type(behavData['laserSide'], np.unique(behavData['laserSide']))
            
            #pdb.set_trace()
            
            for laser in range(trialsEachLaser.shape[1]):
                trialsThisLaser = trialsEachLaser[:,laser]
                if (len(trialsThisLaser)==len(timeDiffs)) or (len(trialsThisLaser)+1==len(timeDiffs)):
                    timeDiffsThisLaser = timeDiffs[trialsThisLaser]
                    waitTimes[laser].extend(timeDiffsThisLaser)
                
        
        plt.hist(waitTimes, bins=np.linspace(0,0.5,21), normed=True, color=['k', 'r'])
        
        plt.show()
        
    elif CASE==4:
        animal = 'band093'
        
        
        
        
