import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import extrafuncs
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import colorpalette
from jaratest.nick.database import dataloader_v2 as dataloader

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
    #colorEachFreq = dict(zip(possibleFreq,possibleColors))

    #behavData.find_trials_each_block()

    '''nBlocks = behavData.blocks['nBlocks']
    trialsEachBlock = behavData.blocks['trialsEachBlock']
    validEachBlock = trialsEachBlock & (behavData['valid'][:,np.newaxis].astype(bool))
    nValidEachBlock = np.sum(validEachBlock,axis=0)
    lastValidEachBlock = np.cumsum(nValidEachBlock) # Actually, these values correspond to lastIndex+1
    firstValidEachBlock = np.concatenate(([0],lastValidEachBlock[:-1]))'''
    rightChoice = behavData['choice']==behavData.labels['choice']['right']

    hPlots = []
    plt.hold(True)
    #trialsThisBlock = trialsEachBlock[:,indb]
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
    animalNames = ['band006', 'band007', 'band008', 'band009','band010', 'band011','band012', 'band013']
    session = '20161018a'
    paradigm = '2afc'
    for ind,animal in enumerate(animalNames):
        plt.subplot(2,4,ind+1)
        loader = dataloader.DataLoader(animal)
        behavFile = loadbehavior.path_to_behavior_data(animal,paradigm,session)
        behavData = loader.get_session_behavior(behavFile)
        plot_dynamics(behavData)
        plt.title(animal)
    plt.suptitle(session)
    