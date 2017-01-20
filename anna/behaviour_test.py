import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from jaratoolbox import extrafuncs
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import colorpalette
from jaratest.nick.database import dataloader_v2 as dataloader

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

def behav_stats(animalName, session, paradigm='2afc'):
    loader = dataloader.DataLoader(animalName)
    behavFile = loadbehavior.path_to_behavior_data(animalName,paradigm,session)
    behavData = loader.get_session_behavior(behavFile)
    correct = behavData['outcome']==behavData.labels['outcome']['correct']
    early = behavData['outcome']==behavData.labels['outcome']['invalid']
    valid = behavData['valid'].astype(bool)
    
    nValid = len(valid)
    nCorrect = len(correct[correct==True])
    #performance = nCorrect.astype(float)/nValid.astype(float)
    print 'Valid: ' + str(nValid)
    print 'Correct: ' + str(nCorrect)
    #print performance

def plot_dynamics(behavData,winsize=40,fontsize=12):
    '''
    Plot performance in time for one session.
    First argument is an object created by loadbehavior.BehaviorData (or subclasses)
    '''
    import pdb
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

def band_discrim_byside(behavData):
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
    
def band_SNR_laser_psychometric(animal, sessions, paradigm='2afc', xlabel=True, ylabel=True):
    loader = dataloader.DataLoader(animal)
    validPerSNR = None
    rightPerSNR = None
    for ind, session in enumerate(sessions):
        behavFile = loadbehavior.path_to_behavior_data(animal,paradigm,session)
        behavData = loader.get_session_behavior(behavFile)
        ax = plt.gca()
        ax.cla()
        possibleSNRs = np.unique(behavData['currentSNR'])
        laserTrialTypes = np.unique(behavData['laserSide'])
        trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['currentSNR'], possibleSNRs, 
                                                                        behavData['laserSide'], laserTrialTypes)
        valid = behavData['valid'].astype(bool)
        rightChoice = behavData['choice']==behavData.labels['choice']['right']
        if validPerSNR is None:
            validPerSNR = np.zeros((len(laserTrialTypes),len(possibleSNRs)))
            rightPerSNR = np.zeros((len(laserTrialTypes),len(possibleSNRs)))
        for las in range(len(laserTrialTypes)):
            trialsThisLaser = trialsEachCond[:,:,las]
            for inds in range(len(possibleSNRs)):
                trialsThisSNR = trialsThisLaser[:,inds]
                validThisSNR = np.sum(trialsThisSNR.astype(int)[valid])
                rightThisSNR = np.sum(trialsThisSNR.astype(int)[rightChoice])
                validPerSNR[las,inds] += validThisSNR
                rightPerSNR[las,inds] += rightThisSNR
    return validPerSNR, rightPerSNR, possibleSNRs
    
def plot_psychometric(validPerSNR, rightPerSNR, possibleSNRs, colour = 'k'):
    from statsmodels.stats.proportion import proportion_confint
    import pdb
    performance = []
    upper = []
    lower = []
    for inds in range(len(possibleSNRs)):
        #pdb.set_trace()
        CIthisSNR = np.array(proportion_confint(rightPerSNR[inds], validPerSNR[inds], method = 'wilson'))
        performance.append(100.0*rightPerSNR[inds]/validPerSNR[inds])
        upper.append(100.0*CIthisSNR[1]-performance[-1])
        lower.append(performance[-1]-100.0*CIthisSNR[0])
    plt.plot(np.arange(len(possibleSNRs)), performance, marker='o', color=colour, lw=3, ms=10)
    plt.errorbar(np.arange(len(possibleSNRs)), performance, yerr = [lower, upper],color=colour)
    plt.ylabel("% rightward")
    plt.xlabel('SNR (dB)')
    plt.xticks(np.arange(len(possibleSNRs)), possibleSNRs)
    plt.ylim((0,100))
    
def band_SNR_psychometric(animal, sessions, paradigm = '2afc'):
    loader = dataloader.DataLoader(animal)
    validPerSNR = None
    rightPerSNR = None
    for ind,session in enumerate(sessions):
        behavFile = loadbehavior.path_to_behavior_data(animal,paradigm,session)
        behavData = loader.get_session_behavior(behavFile)
        possibleSNRs = np.unique(behavData['currentSNR'])
        trialsEachCond = behavioranalysis.find_trials_each_type(behavData['currentSNR'], possibleSNRs)
        valid = behavData['valid'].astype(bool)
        rightChoice = behavData['choice']==behavData.labels['choice']['right']
        if validPerSNR is None:
            validPerSNR = np.zeros(len(possibleSNRs))
            rightPerSNR = np.zeros(len(possibleSNRs))
        for inds in range(len(possibleSNRs)):
            trialsThisSNR = trialsEachCond[:,inds]
            validThisSNR = np.sum(trialsThisSNR.astype(int)[valid])
            rightThisSNR = np.sum(trialsThisSNR.astype(int)[rightChoice])
            validPerSNR[inds] += validThisSNR
            rightPerSNR[inds] += rightThisSNR
    return validPerSNR, rightPerSNR, possibleSNRs

''' 
Method for extracting differences in time between two events in mouse behaviour.
Can be used for withdrawal times, reaction times, etc.

Inputs: 
    - animal: name of animal (string)
    - sessions: list of sessions being analysed (list of strings)
    - paradigm: paradigm used (string)
    - triggers: list of two elements, indicating the names of the events/states that are the desired start and end points (list of two strings)
    
Outputs:
    - times: np.array containing the amount of time it took to get from each start event to each end event
'''
def time_differences(animal, sessions, paradigm = '2afc', triggers = ['Cin', 'Cout']):
    import pdb
    loader = dataloader.DataLoader(animal)
    timeDiff = None
    for ind,session in enumerate(sessions):
        behavFile = loadbehavior.path_to_behavior_data(animal,paradigm,session)
        behavData = loader.get_session_behavior(behavFile)
        eventCode = np.array(behavData.events['eventCode'])
        eventTime = behavData.events['eventTime']
        nextState = behavData.events['nextState']
        try:
            start = np.where(eventCode==behavData.stateMatrix['eventsNames'][triggers[0]])[0]
        except KeyError:
            start = np.where(nextState==behavData.stateMatrix['statesNames'][triggers[0]])[0]+1
        try:
            stop = np.where(eventCode==behavData.stateMatrix['eventsNames'][triggers[1]])[0]
        except KeyError:
            stop = np.where(nextState==behavData.stateMatrix['statesNames'][triggers[1]])[0]+1
        if len(start)>len(stop):
            startAll = start.copy()
            start = np.zeros(len(stop))
            for i in range(len(stop)):
                start[i] = max(j for j in startAll if j < stop[i])
            start = start.astype(int)
        if len(stop)>len(start):
            stopAll = stop.copy()
            stop = np.zeros(len(start))
            for i in range(len(start)):
                stop[i] = min(j for j in stopAll if j > start[i])
            stop = stop.astype(int)
        startTime = eventTime[start]
        stopTime = eventTime[stop]
        #pdb.set_trace()
        diffThisSess = stopTime-startTime
        if timeDiff is None:
            timeDiff = diffThisSess
        else:
            timeDiff = np.concatenate((timeDiff, diffThisSess))
    return timeDiff

def time_differences_by_trial(animal, sessions, sortBy, paradigm = '2afc', triggers = ['Cin', 'Cout']):
    loader = dataloader.DataLoader(animal)
    timeDiff = []
    for ind,session in enumerate(sessions):
        if len(sessions)>1:
            timeDiffThisSess = []
        behavFile = loadbehavior.path_to_behavior_data(animal,paradigm,session)
        behavData = loader.get_session_behavior(behavFile)
        possibleSort = np.unique(behavData[sortBy])
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
        for ind in range(len(possibleSort)):
            trialsThisCond = trialsEachCond[:,ind]
            if len(trialsThisCond) > len(trialEnd):
                trialsThisCond = trialsThisCond[:-1]
            trialEndThisCond = trialEnd[trialsThisCond]
            startThisCond = np.zeros(len(trialsThisCond))
            stopThisCond = np.zeros(len(trialsThisCond))
            for i in range(len(trialEndThisCond)):
                startThisCond[i] = max(j for j in start if j < trialEndThisCond[i])
                stopThisCond[i] = max(k for k in stop if k < trialEndThisCond[i])
            startThisCond = startThisCond.astype(int)
            stopThisCond = stopThisCond.astype(int)
            startTime = eventTime[startThisCond]
            stopTime = eventTime[stopThisCond]
            diffThisCond = stopTime - startTime
            if len(sessions) == 1:
                timeDiff.append(diffThisCond)
            else:
                timeDiffThisSess.append(diffThisCond)
        if len(sessions) > 1:
            timeDiff.append(timeDiffThisSess)
    return timeDiff, possibleSort

if __name__ == '__main__':
    import pdb
    SAVE = 0
    CASE = 5
    paradigm = '2afc'
    if CASE < 3:
        animalNames = ['band011', 'band012']
        #animalNames = ['band017', 'band018', 'band019','band020']
        session = ['20170120a']
        for ind,animal in enumerate(animalNames):
            plt.subplot(2,2,ind+1)
            loader = dataloader.DataLoader(animal)
            behavFile = loadbehavior.path_to_behavior_data(animal,paradigm,session[0])
            behavData = loader.get_session_behavior(behavFile)
            if ind<2:
                xlabel = False
            else:
                xlabel = True
            if ind%2==0:
                ylabel = True
            else:
                ylabel = False
            if CASE==0:
                plot_dynamics(behavData)
            elif CASE==1:
                band_discrim_byside(behavData)
            elif CASE==2:
                validPerSNR, rightPerSNR, possibleSNRs = band_SNR_psychometric(animal, session)
                plot_psychometric(validPerSNR, rightPerSNR, possibleSNRs)
            plt.title(animal)
        plt.suptitle(session[0])
    if CASE == 3:
        animal = 'band006'
        #sessions = ['20161130a','20161201a','20161202a','20161203a','20161204a','20161205a', '20161206a', '20161207a']
        sessions = ['20161212a','20161213a']
        musWithdrawal = time_differences(animal, sessions[1::2], triggers = ['playNoiseStimulus','Cout'])
        salWithdrawal = time_differences(animal, sessions[::2], triggers = ['playNoiseStimulus','Cout'])
        data = [salWithdrawal, musWithdrawal]
        bins = np.linspace(0, 0.5, 50)
        plt.hist(data, bins, alpha=0.7, label=['saline', 'muscimol'])
        plt.legend(loc='upper right')
        plt.xlabel('withdrawal time from sound start (s)')
        plt.title(animal)
    if CASE == 4:
        animal = 'band007'
        #sessions = ['20161130a','20161201a','20161202a','20161203a','20161204a','20161205a', '20161206a', '20161207a']
        sessions = ['20161214a','20161216a']
        salValid, salRight, possibleSNRs = band_SNR_psychometric(animal, sessions[::2])
        musValid, musRight, possibleSNRs = band_SNR_psychometric(animal, sessions[1::2])
        salPerformance = 100.0*salRight/salValid
        musPerformance = 100.0*musRight/musValid
        from statsmodels.stats.proportion import proportion_confint
        salCI = np.array(proportion_confint(salRight, salValid, method = 'wilson'))
        musCI = np.array(proportion_confint(musRight, musValid, method = 'wilson'))
        salUpper = 100.0*salCI[1,:]-salPerformance
        salLower = salPerformance-100.0*salCI[0,:]
        plt.plot(np.arange(len(possibleSNRs)), salPerformance, marker='o', color = 'k', lw=3, ms=10)
        plt.errorbar(np.arange(len(possibleSNRs)), salPerformance, yerr = [salLower, salUpper],color='k')
        musUpper = 100.0*musCI[1,:]-musPerformance
        musLower = musPerformance-100.0*musCI[0,:]
        plt.plot(np.arange(len(possibleSNRs)), musPerformance, marker='o', color = 'r', lw=3, ms=10)
        plt.errorbar(np.arange(len(possibleSNRs)), musPerformance, yerr = [musLower, musUpper],color='r')
        plt.xticks(np.arange(len(possibleSNRs)), possibleSNRs)
        plt.ylim((0,100))
        plt.ylabel("% rightward")
        plt.xlabel('SNR (dB)')
        plt.title(animal)
    if CASE == 4.5:
        animal = 'band008'
        sessions = ['20161130a','20161201a','20161202a','20161203a','20161204a','20161205a', '20161206a', '20161207a']
        musDiff, possibleSNRs = time_differences_by_trial(animal, sessions[1::2], 'currentSNR', triggers = ['Cin','Cout'])
        salDiff, possibleSNRs = time_differences_by_trial(animal, sessions[::2], 'currentSNR', triggers = ['Cin','Cout'])
        meanReactionMus = np.zeros(len(possibleSNRs))
        meanReactionSal = np.zeros(len(possibleSNRs))
        for SNR in range(len(possibleSNRs)):
            reactionsThisSNRMus = [item[SNR] for item in musDiff]
            reactionsThisSNRSal = [item[SNR] for item in salDiff]
            reactionsThisSNRMus = tuple(reactionsThisSNRMus)
            reactionsThisSNRMus = np.concatenate(reactionsThisSNRMus)
            meanReactionMus[SNR] = np.mean(reactionsThisSNRMus)
            reactionsThisSNRSal = tuple(reactionsThisSNRSal)
            reactionsThisSNRSal = np.concatenate(reactionsThisSNRSal)
            meanReactionSal[SNR] = np.mean(reactionsThisSNRSal)
            pdb.set_trace()
        plt.plot(np.arange(len(possibleSNRs)), meanReactionSal, marker='o', color = 'k', lw=3, ms=10)
        plt.plot(np.arange(len(possibleSNRs)), meanReactionMus, marker='o', color = 'r', lw=3, ms=10)
        plt.ylabel('Reaction time (s)')
        plt.xlabel('SNR (dB)')
        plt.xticks(np.arange(len(possibleSNRs)), possibleSNRs)
        plt.ylim(bottom=0)
        plt.title(animal)
    if CASE == 5:
        animal = 'band013'
        #sessions = ['20170111a','20170112a', '20170115a']
        #sessions = ['20170113a', '20170116a']
        sessions = ['20170119a','20170120a']
        colours = ['k','r','y','b']
        sides = ['none', 'left', 'right', 'bilateral']
        patches = []
        validPerSNR, rightPerSNR, possibleSNRs = band_SNR_laser_psychometric(animal, sessions)
        for las in range(len(validPerSNR)):
            plot_psychometric(validPerSNR[las,:], rightPerSNR[las,:], possibleSNRs, colour = colours[las])
            patches.append(mpatches.Patch(color=colours[las], label=sides[las]))
        plt.legend(handles=patches, borderaxespad=0.3,prop={'size':12}, loc='best')
        plt.title(animal)
    if CASE == 6:
        animal = 'band013'
        session = ['20170111a']
        Withdrawal = time_differences(animal, session, triggers=['playNoiseStimulus', 'Cout'])
        bins = np.linspace(0, 0.8, 80)
        plt.hist(Withdrawal, bins, alpha=0.7)
        plt.legend(loc='upper right')
        plt.xlabel('withdrawal time (s)')
        plt.title(animal)
    if CASE == 7:
        animal = 'band013'
        sessions = ['20170111a','20170112a']
        diff, possibleSNRs = time_differences_by_trial(animal, sessions, 'currentSNR', triggers = ['playNoiseStimulus','Cout'])
        meanReaction = np.zeros(len(possibleSNRs))
        for SNR in range(len(possibleSNRs)):
            reactionsThisSNR = [item[SNR] for item in diff]
            reactionsThisSNR = tuple(reactionsThisSNR)
            reactionsThisSNR = np.concatenate(reactionsThisSNR)
            meanReaction[SNR] = np.mean(reactionsThisSNR)
        plt.plot(np.arange(len(possibleSNRs)), meanReaction, marker='o', lw=3, ms=10)
        plt.ylabel('Reaction time (s)')
        plt.xlabel('SNR (dB)')
        plt.xticks(np.arange(len(possibleSNRs)), possibleSNRs)
        plt.ylim(bottom=0)
    if SAVE:
        fig = plt.gcf()
        fig.set_size_inches(20, 10)
        fig_path = '/home/jarauser/Pictures/band_muscimol'
        if CASE==0:
            fig_name = '{0}_behaviour.png'.format(animal)
        elif CASE==3:
            fig_name = '{0}_withdrawal_times_sound_fluorescent.png'.format(animal)
        full_fig_path = os.path.join(fig_path, fig_name)
        fig.savefig(full_fig_path, format = 'png', bbox_inches='tight')
    