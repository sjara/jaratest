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
    Returns a boolean 4D array of size [nTrials,nValues1,nValues2,nValues3]. True for each combination.
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


def band_psychometric(animal, sessions, trialTypes=['currentSNR']):
    ''' 
    Produces the number of valid trials and number of trials where animal went to the right for each condition.
    Can sort by up to three parameters.
    
    Input:
        animal = name of animal whose behaviour is to be used (string)
        sessions = file names of sessions to be used (list of strings)
        trialTypes = names of parameters in behavData to be used for sorting trials (list of strings, up to 3 parameters)
        
    Output:
        validPerCond = 1D to 3D array (depending on number of parameters given) giving number of valid trials for each condition
        rightPerCond = like validPerCond, only trials where animal went to the right
        possibleParams = possible values each parameter takes
    '''
    behavData = behavioranalysis.load_many_sessions(animal, sessions)
    
    firstSort = behavData[trialTypes[0]]
    possibleFirstSort = np.unique(firstSort)
    
    possibleSecondSort = None
    possibleThirdSort = None
    
    if len(trialTypes) > 1:
        secondSort = behavData[trialTypes[1]]
        possibleSecondSort = np.unique(secondSort)

    if len(trialTypes) > 2:
        thirdSort = behavData[trialTypes[2]]
        possibleThirdSort = np.unique(thirdSort)
        
    valid = behavData['valid'].astype(bool)
    rightChoice = behavData['choice']==behavData.labels['choice']['right']
    
    if len(trialTypes) == 3:
        trialsEachComb = find_trials_each_combination_three_params(firstSort, possibleFirstSort, secondSort, possibleSecondSort, thirdSort, possibleThirdSort)
    elif len(trialTypes) == 2:
        trialsEachComb = behavioranalysis.find_trials_each_combination(firstSort, possibleFirstSort, secondSort, possibleSecondSort)
    elif len(trialTypes) == 1:
        trialsEachComb = behavioranalysis.find_trials_each_type(firstSort, possibleFirstSort)
    
    validPerCond, rightPerCond = compute_psychometric_inputs(valid, rightChoice, trialsEachComb)
    
    possibleParams = [possibleFirstSort, possibleSecondSort, possibleThirdSort]
    possibleParams = [param for param in possibleParams if param is not None]
    return validPerCond, rightPerCond, possibleParams

def compute_psychometric_inputs(validTrials, rightChoiceTrials, trialsEachCond):
    '''
    Produces the number of valid trials and trials the animal went to the right for every combination of parameters.
    Shape of output array depends on shape of trialsEachCond parameter
    
    Input: 
        validTrials = 1D array of length nTrials, True for valid trials, False for invalid trials
        rightChoiceTrials = 1D array of length nTrials, True for right choice, False otherwise
        trialsEachCond = boolean array of dimension 1+nParameters, size [nTrials, nValues1, ...], True for every combination
    
    Output:
        validPerCond = nParameter-dimensional array, size [nValues1, ...], contains number of valid trials for every combination
        rightPerCond = array like validPerCond, contains number of right choices for every combination
    '''
    dim = trialsEachCond.shape[1:]
    validPerCond = np.zeros(dim)
    rightPerCond = np.zeros(dim)
    
    if len(dim)>1:
        for cond in range(trialsEachCond.shape[-1]):
            validThisCond, rightThisCond = compute_psychometric_inputs(validTrials, rightChoiceTrials, trialsEachCond[...,cond])
            validPerCond[...,cond] = validThisCond
            rightPerCond[...,cond] = rightThisCond
    else:
        for cond in range(trialsEachCond.shape[-1]):
            trialsThisSNR = trialsEachCond[:,cond]
            validThisCond = np.sum(trialsThisSNR.astype(int)[validTrials])
            rightThisCond = np.sum(trialsThisSNR.astype(int)[rightChoiceTrials])
            validPerCond[cond] += validThisCond
            rightPerCond[cond] += rightThisCond
    
    return validPerCond, rightPerCond

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
    plt.errorbar(np.arange(len(possibleSNRs)), performance, yerr = [lower, upper], color=colour, lw=2, ls=linestyle)
    if ylabel:
        plt.ylabel("% rightward", fontsize=16)
    if xlabel:
        plt.xlabel('SNR (dB)', fontsize=16)
    plt.xticks(np.arange(len(possibleSNRs)), possibleSNRs)
    plt.ylim((0,100))
    ax = plt.gca()
    extraplots.boxoff(ax)