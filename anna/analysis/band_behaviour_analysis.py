import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import extrafuncs
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import colorpalette

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
        
def find_trials_each_combination_three_params(parameter1,parameterPossibleValues1,parameter2,parameterPossibleValues2,parameter3,parameterPossibleValues3):
    '''
    Returns a boolean 3D array of size [nTrials,nValues1,nValues2]. True for each combination.
    '''
    if len(parameter1)!=len(parameter2):
        raise ValueError('parameters must be vectors of same size.')
    nTrials = len(parameter1)
    nValues1 = len(parameterPossibleValues1)
    nValues2 = len(parameterPossibleValues2)
    nValues3 = len(parameterPossibleValues3)
    trialsEachComb = np.zeros((nTrials,nValues1,nValues2,nValues3),dtype=bool)
    trialsEachComb12 = behavioranalysis.find_trials_each_combination(parameter1, parameterPossibleValues1, parameter2, parameterPossibleValues2)
    trialsEachType3 = behavioranalysis.find_trials_each_type(parameter3,parameterPossibleValues3)
    for ind3 in range(nValues3):
        trialsEachComb[:,:,:,ind3] = trialsEachComb12 & trialsEachType3[:,ind3][:,np.newaxis,np.newaxis]
    return trialsEachComb


def band_psychometric(animal, sessions, trialTypes=['currentSNR'], paradigm='2afc'):
    ''' 
    Produces the number of valid trials and number of trials where animal went to the right for each condition.
    Can sort by up to three parameters.
    
    Input:
        animal = name of animal whose behaviour is to be used (string)
        sessions = file names of sessions to be used (list of strings)
        trialTypes = names of parameters in behavData to be used for sorting trials (list of strings)
        paradigm = name of paradigm (string) (ONLY 2afc USED FOR NOW)
        
    Output:
        validPerCond = 1D to 3D array (depending on number of parameters given) giving number of valid trials for each condition
        rightPerCond = like validPerCond, only trials where animal went to the right
        possibleParams = possible values each parameter takes
    '''
    behavData = behavioranalysis.load_many_sessions(animal, sessions)
    validPerCond = None
    rightPerCond = None
    
    firstSort = behavData[trialTypes[0]]
    possibleFirstSort = np.unique(firstSort)
    trialsEachFirstCond = behavioranalysis.find_trials_each_type(firstSort, possibleFirstSort)
    
    possibleSecondSort = []
    possibleThirdSort = []
    
    if len(trialTypes) > 1:
        secondSort = behavData[trialTypes[1]]
        possibleSecondSort = np.unique(secondSort)
        trialsEachSecondCond = behavioranalysis.find_trials_each_type(secondSort, possibleSecondSort)

    if len(trialTypes) > 2:
        thirdSort = behavData[trialTypes[2]]
        possibleThirdSort = np.unique(thirdSort)
        trialsEachThirdCond = behavioranalysis.find_trials_each_type(thirdSort, possibleThirdSort)
        
    dim = [x for x in [len(possibleFirstSort),len(possibleSecondSort),len(possibleThirdSort)] if x>0]
    validPerCond = np.zeros(dim)
    rightPerCond = np.zeros(dim)
    valid = behavData['valid'].astype(bool)
    rightChoice = behavData['choice']==behavData.labels['choice']['right']
    
    trialsEachComb = find_trials_each_combination_three_params(firstSort, possibleFirstSort, secondSort, possibleSecondSort, thirdSort, possibleThirdSort)
    for first in range(len(possibleFirstSort)):
        for second in range(len(possibleSecondSort)):
            for third in range(len(possibleThirdSort)):
                trialsThisSNR = trialsEachComb[:,first,second,third]
                validThisCond = np.sum(trialsThisSNR.astype(int)[valid])
                rightThisCond = np.sum(trialsThisSNR.astype(int)[rightChoice])
                validPerCond[first,second,third] += validThisCond
                rightPerCond[first,second,third] += rightThisCond
    possibleParams = [possibleFirstSort, possibleSecondSort, possibleThirdSort]
    #possibleParams = filter(None, possibleParams)
    return validPerCond, rightPerCond, possibleParams

def plot_band_psychometric(validPerSNR, rightPerSNR, possibleSNRs, colour = 'k', linestyle='-', xlabel=True, ylabel=True):
    from statsmodels.stats.proportion import proportion_confint
    performance = []
    upper = []
    lower = []
    for inds in range(len(possibleSNRs)):
        CIthisSNR = np.array(proportion_confint(rightPerSNR[inds], validPerSNR[inds], method = 'wilson'))
        performance.append(100.0*rightPerSNR[inds]/validPerSNR[inds])
        upper.append(100.0*CIthisSNR[1]-performance[-1])
        lower.append(performance[-1]-100.0*CIthisSNR[0])
    plt.plot(np.arange(len(possibleSNRs)), performance, linestyle, marker='o', color=colour, mec=colour, lw=3, ms=10)
    plt.errorbar(np.arange(len(possibleSNRs)), performance, yerr = [lower, upper],color=colour)
    if ylabel:
        plt.ylabel("% rightward", fontsize=16)
    if xlabel:
        plt.xlabel('SNR (dB)', fontsize=16)
    plt.xticks(np.arange(len(possibleSNRs)), possibleSNRs)
    plt.ylim((0,100))