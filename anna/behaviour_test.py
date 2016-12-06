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

def band_discrim_totals(behavData):
    import pdb
    ax = plt.gca()
    ax.cla()
    possibleBands = np.unique(behavData['currentBand'])
    trialsEachCond = behavioranalysis.find_trials_each_type(behavData['currentBand'], possibleBands)
    valid = behavData['valid'].astype(bool)
    correct = behavData['outcome']==behavData.labels['outcome']['correct']
    index = np.arange(len(possibleBands))
    performance = []
    for indb in range(len(possibleBands)):
        trialsThisBand = trialsEachCond[:,indb]
        validThisBand = np.sum(trialsThisBand.astype(int)[valid])
        correctThisBand = np.sum(trialsThisBand.astype(int)[correct])
        #pdb.set_trace()
        performance.append(100.0*correctThisBand/validThisBand)
    plt.plot(index, performance)
    plt.ylim((0,100))
    plt.ylabel('% correct')
    plt.xlabel('bandwidths')
    ax.set_xticks(index + 0.5)
    ax.set_xticklabels(possibleBands)
    
def band_SNR_psychometric(behavData, xlabel=True, ylabel=True):
    import pdb
    ax = plt.gca()
    ax.cla()
    possibleSNRs = np.unique(behavData['currentSNR'])
    trialsEachCond = behavioranalysis.find_trials_each_type(behavData['currentSNR'], possibleSNRs)
    valid = behavData['valid'].astype(bool)
    rightChoice = behavData['choice']==behavData.labels['choice']['right']
    performance = []
    for inds in range(len(possibleSNRs)):
        trialsThisSNR = trialsEachCond[:,inds]
        validThisBand = np.sum(trialsThisSNR.astype(int)[valid])
        rightThisBand = np.sum(trialsThisSNR.astype(int)[rightChoice])
        #pdb.set_trace()
        performance.append(100.0*rightThisBand/validThisBand)
    plt.plot(np.arange(len(possibleSNRs)), performance, marker='o', lw=3, ms=10)
    if ylabel:
        plt.ylabel("% rightward")
    if xlabel:
        plt.xlabel('SNR (dB)')
    plt.xticks(np.arange(len(possibleSNRs)), possibleSNRs)
    plt.ylim((0,100))

if __name__ == '__main__':
    SAVE = 1
    CASE = 3
    #animalNames = ['band006', 'band007', 'band008', 'band009','band010', 'band011','band012', 'band013']
    #animalNames = ['band006', 'band007', 'band008', 'band009', 'band010', 'band011', 'band012']
    #animalNames = ['band011', 'band012', 'band013']
    animal = 'band006'
    sessions = ['20161130a','20161201a','20161202a','20161203a','20161204a','20161205a']
    paradigm = '2afc'
    for ind,session in enumerate(sessions):
        plt.subplot(3,2,ind+1)
        loader = dataloader.DataLoader(animal)
        behavFile = loadbehavior.path_to_behavior_data(animal,paradigm,session)
        behavData = loader.get_session_behavior(behavFile)
        if ind<4:
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
            band_discrim_totals(behavData)
        elif CASE==3:
            band_SNR_psychometric(behavData, xlabel=xlabel, ylabel=ylabel)
        plt.title(session)
    plt.suptitle(animal)
    if SAVE:
        fig = plt.gcf()
        fig.set_size_inches(20, 10)
        fig_path = '/home/jarauser/Pictures'
        if CASE==0:
            fig_name = '{0}_behaviour.png'.format(animal)
        elif CASE==3:
            fig_name = '{0}_band_psychometric.png'.format(animal)
        full_fig_path = os.path.join(fig_path, fig_name)
        fig.savefig(full_fig_path, format = 'png', bbox_inches='tight')
    