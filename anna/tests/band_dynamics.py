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

import pdb

def rsync_behavior(subject, server = 'jarauser@jarahub', serverBehavPath = '/data/behavior', localDataPath = '/media/martushka/redWD/2020acsigdet/data/behavior/'):
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
    

    CASE=1
    
    if CASE==0:
        # animalNames = ['band' + str(number) for number in range(110, 127)]
        animalNames = ['band' + str(number) for number in range(145, 151)]
        session = '20210305a'

        #rsync_all_behaviour(animalNames)
        plt.figure()
        
        for ind,animal in enumerate(animalNames):
            plt.subplot(2,4,ind+1)
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
            plt.subplot(2,4,ind+1)
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
        animals = ['band'+str(number) for number in [147, 149, 150]]
        sessions = ['20210415a']

        # animals = ['band' + str(number) for number in [127, 128, 129, 130, 131, 132]]
        # sessions = ['20201027a', '20201028a', '20201029a', '20201030a','20201031a']

        #rsync_all_behaviour(animals)
       
#         animals = ['band'+str(number) for number in [105, 107, 108, 109]]
#         sessions = ['20200229a', '20200301a', '20200302a']
        
        plt.figure()
        for ind, animal in enumerate(animals):
            plt.subplot(1,3,ind+1)
            validPerCond, rightPerCond, possibleConds = band_behaviour_analysis.band_psychometric(animal, sessions, trialTypes=['currentBand','currentSNR'])
            bandColours = ['k','r']
            patches = []
            for band in range(len(possibleConds[0])):
                band_behaviour_analysis.plot_band_psychometric(validPerCond[band,:], rightPerCond[band,:], possibleConds[1], colour = bandColours[band])
                patches.append(mpatches.Patch(color=bandColours[band], label=possibleConds[0][band]))
            plt.legend(handles=patches, borderaxespad=0.3,prop={'size':12}, loc='best')

            # behavFile = os.path.join(settings.BEHAVIOR_PATH, animal, animal + '_2afc_' + session + '.h5')
            # if os.path.exists(behavFile):
            #     behavData = loadbehavior.BehaviorData(behavFile, readmode='full')
            behavData = behavioranalysis.load_many_sessions(animal, sessions)
            correct = behavData['outcome'] == behavData.labels['outcome']['correct']
            incorrect = behavData['outcome'] == behavData.labels['outcome']['error']

            accuracy = 100.0 * np.sum(correct) / (np.sum(correct) + np.sum(incorrect))
            plt.title(f'{animal}, Acc: {accuracy:.1f}%')

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

        # animal = 'band110'
        # lasersessions = ['20200615a','20200616a','20200618a','20200619a','20200621a','20200622a','20200625a','20200626a']
        # controlsessions = ['20200617a','20200620a','20200624a','20200627a']

        # lasersessions = ['20200628a','20200629a','20200701a','20200717a','20200719a','20200720a','20200722a','20200723a'] # 15mW
        # controlsessions = ['20200630a','20200718a','20200721a','20200724a']

        # lasersessions = ['20200725a','20200726a','20200728a','20200729a','20200731a','20200801a','20200803a','20200804a'] # 5mW
        # controlsessions = ['20200727a','20200730a','20200802a','20200805a']

        # animal = 'band111'
        # lasersessions = ['20200613a','20200614a','20200616a','20200617a','20200619a','20200620a','20200622a','20200623a'] # 10mW
        # controlsessions = ['20200615a','20200618a','20200621a','20200624a']

        # lasersessions = ['20200625a','20200626a','20200628a','20200629a','20200701a','20200713a','20200715a','20200716a'] # 15mW
        # controlsessions = ['20200627a','20200630a','20200714a','20200717a']

        # lasersessions = ['20200718a','20200719a','20200721a','20200722a','20200724a','20200725a','20200727a','20200728a'] # 5mW
        # controlsessions = ['20200720a','20200723a','20200726a','20200729a']
        
        # animal = 'band112'
        # lasersessions = ['20200608a','20200609a','20200611a','20200612a','20200614a','20200615a','20200617a','20200618a'] # 10mW
        # controlsessions = ['20200610a', '20200613a', '20200616a','20200619a']

        # lasersessions = ['20200620a','20200621a','20200623a','20200624a','20200626a','20200627a','20200629a','20200630a'] # 15mW
        # controlsessions = ['20200622a','20200625a','20200628a','20200701a']

        # lasersessions = ['20200713a','20200714a','20200716a','20200717a','20200719a','20200720a','20200722a','20200723a'] # 5mW
        # controlsessions = ['20200715a','20200718a','20200721a','20200724a']

        # animal = 'band121'
        # lasersessions = ['20200717a', '20200718a', '20200720a','20200721a','20200723a','20200724a','20200726a','20200727a'] # 5mW
        # controlsessions = ['20200719a','20200722a','20200725a','20200728a']

        # lasersessions = ['20200729a','20200730a','20200801a','20200802a','20200804a','20200805a','20200807a','20200808a'] # 10 mW
        # controlsessions = ['20200731a','20200803a','20200806a','20200809a']

        # lasersessions = ['20200810a','20200811a','20200813a','20200814a','20200816a','20200817a','20200819a','20200820a'] # 15 mW
        # controlsessions = ['20200812a','20200815a','20200818a','20200821a']

        # animal = 'band122'
        # lasersessions = ['20200808a','20200810a','20200811a','20200813a','20200816a','20200818a','20200822a','20200823a'] # 5 mW
        # controlsessions = ['20200809a','20200812a','20200815a','20200819a']
        # lasersessions = [] # 10 mW
        # controlsessions = ['20200824a']

        # animal = 'band113'
        # lasersessions = ['20200823a','20200824a','20200826a','20200827a','20200829a','20200830a','20200906a','20200907a'] # 5 mW
        # controlsessions = ['20200822a','20200825a','20200828a','20200831a']
        # lasersessions = ['20200923a', '20200924a', '20200926a', '20200927a', '20200929a', '20200930a', '20201002a', '20201003a'] # 10 mW
        # controlsessions = ['20200922a', '20200925a', '20200928a', '20201001a']

        # animal = 'band126'
        # # lasersessions = ['20200908a'] # 5 mW
        # # controlsessions = ['20200906a']
        # lasersessions = ['20201020a', '20201023a', '20201025a', '20201028a', '20201030a', '20201101a', '20201102a', '20201104a']
        # controlsessions = ['20201024a', '20201029a', '20201031a', '20201103a']

        # animal = 'band133'
        # lasersessions = ['20201002a', '20201003a', '20201005a', '20201006a'] # 3 mW
        # controlsessions = ['20201001a', '20201004a']

        # animal = 'band135'
        # lasersessions = ['20201025a', '20201028a', '20201029a', '20201031a', '20201101a', '20201103a', '20201104a'] # 3 mW
        # controlsessions = ['20201027a', '20201030a', '20201102a', '20201105a']

        # animal = 'band120'
        # lasersessions = ['20201023a', '20201024a', '20201026a', '20201027a', '20201029a', '20201030a', '20201101a', '20201102a']  # 10 mW
        # controlsessions = ['20201025a', '20201028a', '20201031a', '20201103a']

        animal = 'band150'
        lasersessions = ['20210404a', '20210405a','20210407a','20210408a','20210410a','20210411a']
        controlsessions = ['20210406a','20210409a']
        
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

    # unilateral plots
    elif CASE==3:
        from statsmodels.stats.proportion import proportion_confint

        # animal = 'band091'
        # sessions = ['20200220a', '20200221a', '20200222a', '20200223a', '20200224a', '20200226a', '20200227a', '20200228a', '20200229a']

        # animal = 'band093'
        # sessions = ['20200224a', '20200226a', '20200228a', '20200229a', '20200301a', '20200302a', '20200303a', '20200304a', '20200305a']

        # animal = 'band124'
        # sessions = ['20200823a','20200824a','20200825a','20200826a','20200827a','20200828a','20200829a','20200830a','20200831a']

        # animal = 'band125'
        # sessions = ['20200822a','20200823a','20200824a','20200825a','20200826a','20200827a','20200828a','20200829a','20200830a','20200831a']

        animal = 'band135'
        sessions = ['20201113a', '20201115a', '20201116a', '20201117a']

        plt.figure()

        validPerCond, rightPerCond, possibleConds = band_behaviour_analysis.band_psychometric(animal, sessions, trialTypes=['currentBand','laserSide','currentSNR'])
        for indBand, band in enumerate(possibleConds[0]):
            plt.subplot(1, 2, indBand + 1)
            bandColours = ['k', 'r']
            laserLines = ['-', '--', '-.', ':']
            lines = []
            for laser in range(len(possibleConds[1])):
                performance = []
                upper = []
                lower = []
                for SNR in range(len(possibleConds[2])):
                    CIthisSNR = np.array(proportion_confint(rightPerCond[indBand,laser,SNR], validPerCond[indBand,laser,SNR], method='wilson'))
                    performance.append(100.0 * rightPerCond[indBand,laser,SNR] / validPerCond[indBand,laser,SNR])
                    upper.append(100.0 * CIthisSNR[1] - performance[-1])
                    lower.append(performance[-1] - 100.0 * CIthisSNR[0])

                line, = plt.plot(np.arange(len(possibleConds[2])), performance, ls=laserLines[laser], marker='o', color=bandColours[indBand], mec=bandColours[indBand], lw=3, ms=10)
                #plt.errorbar(np.arange(len(possibleConds[2])), performance, yerr = [lower, upper], color=bandColours[indBand], lw=2, fmt='none', capsize=10)
                lines.append(line)
            plt.legend(handles=lines, labels=['no laser','left','right','bilateral'], borderaxespad=0.3, prop={'size': 12}, loc='best', handlelength=4, markerscale=0)
            if indBand==0:
                plt.ylabel("% rightward", fontsize=16)
            plt.xlabel('SNR (dB)', fontsize=16)
            plt.xticks(np.arange(len(possibleConds[2])), possibleConds[2])
            plt.ylim((0, 100))
            plt.title(band)
        plt.suptitle(animal)

        plt.show()

    # session by session plots (to see change in performance over time)
    elif CASE==4:

        # animal = 'band081'
        # animal = 'band087'
        # lasersessions = ['20190307a', '20190308a', '20190310a', '20190311a', '20190313a', '20190314a', '20190316a', '20190317a']

        animal = 'band110'
        lasersessions = ['20200615a','20200616a','20200618a','20200619a','20200621a','20200622a','20200625a','20200626a']

        # animal = 'band112'
        # lasersessions = ['20200608a','20200609a','20200611a','20200612a','20200614a','20200615a','20200617a','20200618a']

        plt.figure()
        for ind, session in enumerate(lasersessions):
            plt.subplot(2,4,ind+1)
            sessions = [session]
            validPerCond, rightPerCond, possibleConds = band_behaviour_analysis.band_psychometric(animal, sessions, trialTypes=['currentBand','laserSide','currentSNR'])
            bandColours = ['k','r']
            laserLines = ['-', '--']
            patches = []
            for band in range(len(possibleConds[0])):
                for laser in range(len(possibleConds[1])):
                    band_behaviour_analysis.plot_band_psychometric(validPerCond[band,laser,:], rightPerCond[band,laser,:], possibleConds[2], colour=bandColours[band], linestyle=laserLines[laser])
                patches.append(mpatches.Patch(color=bandColours[band], label=possibleConds[0][band]))
            plt.legend(handles=patches, borderaxespad=0.3,prop={'size':12}, loc='best')
            plt.title(session)
        plt.suptitle(animal)

        plt.show()
        
        
        
        
