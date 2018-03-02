import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from jaratoolbox import extrafuncs
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import settings


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
        
        
        
    
    

if __name__ == '__main__':

    animalNames = ['band0'+str(number) for number in [46,47,48,49,50,51,52,53]]
    #animalNames = ['adap064', 'adap070']
    session = '20180301a'
    
    rsync_all_behaviour(animalNames)
    plt.figure()
    
    for ind,animal in enumerate(animalNames):
        plt.subplot(2,4,ind+1)
        behavFile = os.path.join(settings.BEHAVIOR_PATH,animal,animal+'_2afc_'+session+'.h5')
        behavData = loadbehavior.BehaviorData(behavFile,readmode='full')
        plot_dynamics(behavData)
        plt.title(animal)
    plt.suptitle(session)
    plt.show()
    
    plt.figure()
    for ind,animal in enumerate(animalNames):
        plt.subplot(2,4,ind+1)
        behavFile = os.path.join(settings.BEHAVIOR_PATH,animal,animal+'_2afc_'+session+'.h5')
        behavData = loadbehavior.BehaviorData(behavFile,readmode='full')
        plot_multibandwidth_psychometric(behavData)
        plt.title(animal)
    plt.suptitle(session)
    plt.show()
