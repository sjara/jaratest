''' 
Generate the intermediate ephys and behaviour data to plot psychometric curves for bandwidth behaviour sessions.

All mice trained on bandwidth task where left=no tone, right=tone
Right trials came in multiple SNRs, but total trials are balanced 50-50 for left and right
Mice trained on multiple noise amplitudes, but for testing we only used noise whose average power level was 40dB
Tone was at 8kHz (as middle of mouse hearing range), AM rate used was 8Hz, sound lasted 500ms
For laser experiments, 25% of trials had bilateral laser, laser came on with sound and lasted 100ms after
'''

import os
import sys
import importlib
import numpy as np
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from scipy import stats

figName = 'ac_inactivation_behaviour'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2017acnih', figName)

muscimolAnimals = ['band006', 'band008', 'band010']
salineSessions = ['20161130a', '20161202a', '20161204a', '20161206a']
muscimolSessions = ['20161201a', '20161203a', '20161205a', '20161207a']

PVAnimals = ['band017', 'band020']
laserPVSessions = ['20170228a','20170226a','20170224a','20170222a']

archAnimals = ['band011']
archSessions = ['20170314a','20170315a','20170324a']

# --- computes valid and right trials across all sessions for muscimol animals ---
for animal in muscimolAnimals:
    musValidPerSNR = None
    musRightPerSNR = None
    musCorrect = 0
    for ind,session in enumerate(muscimolSessions):
        behavFile = os.path.join(settings.BEHAVIOR_PATH,animal,animal+'_2afc_'+session+'.h5')
        behavData = loadbehavior.BehaviorData(behavFile,readmode='full')
        possibleSNRs = np.unique(behavData['currentSNR'])
        trialsEachCond = behavioranalysis.find_trials_each_type(behavData['currentSNR'], possibleSNRs)
        valid = behavData['valid'].astype(bool)
        rightChoice = behavData['choice']==behavData.labels['choice']['right']
        correct = behavData['outcome']==behavData.labels['outcome']['correct']
        musCorrect += len(correct[correct==True])
        if musValidPerSNR is None:
            musValidPerSNR = np.zeros(len(possibleSNRs))
            musRightPerSNR = np.zeros(len(possibleSNRs))
        for inds in range(len(possibleSNRs)):
            trialsThisSNR = trialsEachCond[:,inds]
            validThisSNR = np.sum(trialsThisSNR.astype(int)[valid]) 
            rightThisSNR = np.sum(trialsThisSNR.astype(int)[rightChoice])
            musValidPerSNR[inds] += validThisSNR
            musRightPerSNR[inds] += rightThisSNR
    
    salValidPerSNR = None
    salRightPerSNR = None
    salCorrect = 0
    for ind,session in enumerate(salineSessions):
        behavFile = os.path.join(settings.BEHAVIOR_PATH,animal,animal+'_2afc_'+session+'.h5')
        behavData = loadbehavior.BehaviorData(behavFile,readmode='full')
        possibleSNRs = np.unique(behavData['currentSNR'])
        trialsEachCond = behavioranalysis.find_trials_each_type(behavData['currentSNR'], possibleSNRs)
        valid = behavData['valid'].astype(bool)
        rightChoice = behavData['choice']==behavData.labels['choice']['right']
        correct = behavData['outcome']==behavData.labels['outcome']['correct']
        salCorrect += len(correct[correct==True])
        if salValidPerSNR is None:
            salValidPerSNR = np.zeros(len(possibleSNRs))
            salRightPerSNR = np.zeros(len(possibleSNRs))
        for inds in range(len(possibleSNRs)):
            trialsThisSNR = trialsEachCond[:,inds]
            validThisSNR = np.sum(trialsThisSNR.astype(int)[valid]) 
            rightThisSNR = np.sum(trialsThisSNR.astype(int)[rightChoice])
            salValidPerSNR[inds] += validThisSNR
            salRightPerSNR[inds] += rightThisSNR
            
    validPerSNR = np.array([salValidPerSNR, musValidPerSNR])
    rightPerSNR = np.array([salRightPerSNR, musRightPerSNR])
    nCorrect = [salCorrect, musCorrect]
    
    # saves relevant data for plotting psychometric curve
    outputFile = '{}_muscimol_inactivation_psychometric.npz'.format(animal)
    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath, validPerSNR=validPerSNR, rightPerSNR=rightPerSNR, nCorrect=nCorrect, possibleSNRs=possibleSNRs)
    print outputFile + " saved"
    
# --- computes valid and right trials across all sesions for PV animals ---
for animal in PVAnimals:
    validPerSNR = None
    rightPerSNR = None
    nCorrect = [0,0]
    for ind, session in enumerate(laserPVSessions):
        behavFile = os.path.join(settings.BEHAVIOR_PATH,animal,animal+'_2afc_'+session+'.h5')
        behavData = loadbehavior.BehaviorData(behavFile,readmode='full')
        possibleSNRs = np.unique(behavData['currentSNR'])
        laserTrialTypes = np.unique(behavData['laserSide'])
        trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['currentSNR'], possibleSNRs, 
                                                                        behavData['laserSide'], laserTrialTypes)
        valid = behavData['valid'].astype(bool)
        rightChoice = behavData['choice']==behavData.labels['choice']['right']
        correct = behavData['outcome']==behavData.labels['outcome']['correct']
        laserTrials = np.where(behavData['laserSide']!=0)
        conTrials = np.where(behavData['laserSide']==0)
        nCorrect[0] += np.sum(correct[conTrials])
        nCorrect[1] += np.sum(correct[laserTrials])
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
                
    # saves relevant data for plotting psychometric curve
    outputFile = '{}_PV_activation_psychometric.npz'.format(animal)
    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath, validPerSNR=validPerSNR, rightPerSNR=rightPerSNR, nCorrect=nCorrect, possibleSNRs=possibleSNRs)
    print outputFile + " saved"

# --- computes valid and right trials across all sesions for Arch animals ---
for animal in archAnimals:
    validPerSNR = None
    rightPerSNR = None
    nCorrect = [0,0]
    for ind, session in enumerate(archSessions):
        behavFile = os.path.join(settings.BEHAVIOR_PATH,animal,animal+'_2afc_'+session+'.h5')
        behavData = loadbehavior.BehaviorData(behavFile,readmode='full')
        possibleSNRs = np.unique(behavData['currentSNR'])
        laserTrialTypes = np.unique(behavData['laserSide'])
        trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['currentSNR'], possibleSNRs, 
                                                                        behavData['laserSide'], laserTrialTypes)
        valid = behavData['valid'].astype(bool)
        rightChoice = behavData['choice']==behavData.labels['choice']['right']
        correct = behavData['outcome']==behavData.labels['outcome']['correct']
        laserTrials = np.where(behavData['laserSide']!=0)
        conTrials = np.where(behavData['laserSide']==0)
        nCorrect[0] += np.sum(correct[conTrials])
        nCorrect[1] += np.sum(correct[laserTrials])
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
                
    # saves relevant data for plotting psychometric curve
    outputFile = '{}_CamKII_inactivation_psychometric.npz'.format(animal)
    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath, validPerSNR=validPerSNR, rightPerSNR=rightPerSNR, nCorrect=nCorrect, possibleSNRs=possibleSNRs)
    print outputFile + " saved"
