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
    
    CASE=3

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
    
    elif CASE==2:
#         animal = 'band051'
#         laserSessions = ['20180330a','20180401a','20180403a','20180405a','20180407a','20180418a','20180420a','20180422a','20180424a','20180426a','20180428a','20180430a','20180502a']
#         controlSessions = ['20180331a', '20180329a', '20180402a', '20180404a','20180406a','20180411a','20180417a','20180419a','20180421a','20180425a','20180427a','20180429a','20180501a']

#         animal= 'band052'
#         laserSessions = ['20180516a', '20180519a', '20180521a','20180523a','20180525a','20180528a']
#         controlSessions = ['20180513a', '20180515a', '20180517a','20180518a','20180520a','20180522a','20180524a','20180526a']
#         
        # after box improvements
#         animal = 'band052'
#         laserSessions = ['20180530a', '20180601a', '20180603a','20180605a']
#         controlSessions = ['20180529a', '20180531a', '20180602a','20180604a']
#          
#         animal = 'band046'
#         laserSessions = ['20180523a', '20180525a', '20180528a']
#         controlSessions = ['20180522a', '20180524a', '20180526a']
        
        # after box improvements
#         animal = 'band046'
#         laserSessions = ['20180530a', '20180601a', '20180603a','20180605a']
#         controlSessions = ['20180529a', '20180531a', '20180602a','20180604a']

#         animal = 'band065'
#         laserSessions = ['20181018a','20181020a','20181021a','20181023a','20181024a','20181026a','20181027a','20181029a']
#         controlSessions = ['20181019a','20181022a','20181025a','20181028a','20181105a']
#         rsync_behavior(animal)
        
#         animal = 'band070'
#         laserSessions = ['20181020a','20181021a','20181023a','20181024a','20181026a','20181027a','20181029a','20181030a']
#         controlSessions = ['20181019a','20181022a','20181025a','20181028a','20181105a']
#         rsync_behavior(animal)

#         animal = 'band066'
#         laserSessions = ['20190123a','20190124a','20190126a','20190127a','20190129a','20190130a','20190201a','20190202a']
#         controlSessions = ['20190125a','20190128a','20190131a','20190203a']
#         rsync_behavior(animal)
        
#         animal = 'band066'
#         laserSessions = ['20190218a','20190219a','20190221a','20190222a','20190224a','20190225a','20190227a','20190228a']
#         controlSessions = ['20190220a','20190223a','20190226a','20190301a']
        
#         animal = 'band069'
#         laserSessions = ['20190123a','20190124a','20190126a','20190127a','20190129a','20190130a','20190201a','20190202a']
#         controlSessions = ['20190125a','20190128a','20190131a','20190203a']
#         rsync_behavior(animal)

#         animal = 'band069'
#         laserSessions = ['20190218a','20190219a','20190221a','20190222a','20190224a','20190225a','20190227a','20190228a']
#         controlSessions = ['20190220a','20190223a','20190226a','20190301a']
#         rsync_behavior(animal)
        
        animal = 'band081'
        laserSessions = ['20190307a','20190308a','20190310a','20190311a','20190313a','20190314a','20190316a','20190317a']
        controlSessions = ['20190309a','20190312a','20190315a','20190318a']
        rsync_behavior(animal)

#         animal = 'band087'
#         laserSessions = ['20190307a','20190308a','20190310a','20190311a','20190313a','20190314a','20190316a','20190317a']
#         controlSessions = ['20190309a','20190312a','20190315a','20190318a']
#         rsync_behavior(animal)

#         animal = 'band081'
#         laserSessions = ['20190310a'] #day anna trained
#         controlSessions = ['20190309a','20190312a','20190315a','20190318a']
#         rsync_behavior(animal)

#         animal = 'band065'
#         laserSessions = ['20181116a','20181118a','20181120a','20181122a']
#         
#         sessionTypes = [laserSessions]#, controlSessions]

        sessionTypes = [laserSessions, controlSessions]

        sessionTitles = ['Laser', 'Control']
        
        plt.figure()
        plt.hold(True)
        for ind, sessions in enumerate(sessionTypes):
            plt.subplot(1,2,ind+1)
            validPerCond, rightPerCond, possibleConds = band_behaviour_analysis.band_psychometric(animal, sessions, trialTypes=['laserSide','currentBand','currentSNR'])
            bandColours = ['k','#ef2929']
            laserLines = ['-','--']
            patches = []
            ylabel = True if ind==0 else False
            for laser in range(len(possibleConds[0])):
                for band in range(len(possibleConds[1])):
                    band_behaviour_analysis.plot_band_psychometric(validPerCond[laser,band,:], rightPerCond[laser,band,:], possibleConds[2], colour = bandColours[band], linestyle = laserLines[laser], ylabel=ylabel)
                    if laser==0:
                        patches.append(mpatches.Patch(color=bandColours[band], label=possibleConds[1][band]))
            plt.legend(handles=patches, borderaxespad=0.3,prop={'size':12}, loc='best')
            plt.title(sessionTitles[ind], fontsize=16)
            plt.xlim(-0.5, len(possibleConds[1])+1.5)
        plt.suptitle(animal, fontsize=16)

        plt.show()
        
    elif CASE==3:
        plt.figure()
#         animals = ['band0'+str(number) for number in [65,66,67,68,69,70,71]]
#         sessions = ['20180929a','20180930a', '20181001a','20181002a','20181003a']
        animals = ['band081', 'band087']
        sessions = ['20190307a','20190308a','20190310a','20190311a','20190313a','20190314a','20190316a','20190317a']
        for ind, animal in enumerate(animals):
            plt.subplot(1,2,ind+1)
            timeDiff, possibleBands = time_differences_by_trial(animal, sessions, 'laserSide', triggers = ['playNoiseStimulus','Cout'])
            bins = np.linspace(0, 0.5, 50)
            plt.hold(True)
            plt.hist([timeDiff[0],timeDiff[1]], bins, alpha=0.7, label=np.unique(possibleBands), histtype='step', lw=3, color=['k','r'], normed=True)
            plt.legend(loc='upper right')
            plt.xlabel('withdrawal time from sound start (s)')
            plt.title(animal)
            ax = plt.gca()
            ax.axvline(np.median(timeDiff[0]), linestyle='--', color='k')
            ax.axvline(np.median(timeDiff[1]), linestyle='--', color='r')
        plt.show()
        
        plt.figure()
        for ind, animal in enumerate(animals):
            plt.subplot(1,2,ind+1)
            timeDiff, possibleOutcomes = time_differences_by_trial(animal, sessions, 'outcome', triggers = ['playNoiseStimulus','Cout'])
            bins = np.linspace(0, 0.5, 50)
            plt.hold(True)
            plt.hist([timeDiff[0],timeDiff[1]], bins, alpha=0.7, label=['incorrect','correct'], histtype='step', lw=3, color=['b','g'])
            plt.legend(loc='upper right')
            plt.xlabel('withdrawal time from sound start (s)')
            plt.title(animal)
            ax = plt.gca()
            ax.axvline(np.median(timeDiff[0]), linestyle='--', color='b')
            ax.axvline(np.median(timeDiff[1]), linestyle='--', color='g')
        plt.show()
        
    elif CASE==4:
        animals = ['band065', 'band070']
        sessions = ['20181106a','20181107a','20181108a','20181109a','20181110a','20181111a','20181112a','20181113a']

        
        plt.figure()
        for ind, animal in enumerate(animals):
            plt.subplot(1,2,ind+1)
            plt.hold(True)
            validPerCond, rightPerCond, possibleConds = band_behaviour_analysis.band_psychometric(animal, sessions, trialTypes=['laserSide','currentNoiseAmp','currentSNR'])
            bandColours = ['k','#ef2929']
            laserLines = ['-','--']
            patches = []
            for laser in range(len(possibleConds[0])):
                for band in range(len(possibleConds[1])):
                    band_behaviour_analysis.plot_band_psychometric(validPerCond[laser,band,:], rightPerCond[laser,band,:], possibleConds[2], colour = bandColours[band], linestyle = laserLines[laser])
                    if laser==0:
                        patches.append(mpatches.Patch(color=bandColours[band], label=possibleConds[1][band]))
            plt.legend(handles=patches, borderaxespad=0.3,prop={'size':12}, loc='best')
            plt.title(animal)
            plt.xlim(-0.5, len(possibleConds[1])+1.5)
        plt.suptitle('Noise amp modulation')
        
        plt.show()
        
    elif CASE==5:
        animals = ['band065', 'band070']
        sessions = ['20181106a','20181107a','20181108a','20181109a','20181110a','20181111a','20181112a','20181113a']

        
        plt.figure()
        for ind, animal in enumerate(animals):
            plt.subplot(1,2,ind+1)
            plt.hold(True)
            validPerCond, rightPerCond, possibleConds = band_behaviour_analysis.band_psychometric(animal, sessions, trialTypes=['laserSide','currentNoiseAmp','currentSNR'])
            bandColours = ['k','#ef2929']
            laserLines = ['-','--']
            patches = []
            for laser in range(len(possibleConds[0])):
                for band in range(len(possibleConds[1])):
                    band_behaviour_analysis.plot_band_psychometric(validPerCond[laser,band,:], rightPerCond[laser,band,:], possibleConds[2], colour = bandColours[band], linestyle = laserLines[laser])
                    if laser==0:
                        patches.append(mpatches.Patch(color=bandColours[band], label=possibleConds[1][band]))
            plt.legend(handles=patches, borderaxespad=0.3,prop={'size':12}, loc='best')
            plt.title(animal)
            plt.xlim(-0.5, len(possibleConds[1])+1.5)
        plt.suptitle('Noise amp modulation')

        plt.show()
