import os
import numpy as np
import matplotlib.pyplot as plt

from jaratoolbox import extrafuncs
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
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

if __name__ == '__main__':

    animalNames = ['band0'+str(number) for number in [46,47,48,49,50,51,52,53]]
    #animalNames = ['adap064', 'adap070']
    session = '20180215a'
    
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