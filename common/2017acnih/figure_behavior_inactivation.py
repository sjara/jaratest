'''
Figure showing performance in signal extraction task with inactivation (of AC or specific cells).
'''

import os
import sys
from statsmodels.stats.proportion import proportion_confint
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from jaratoolbox import extraplots
from jaratoolbox import settings
matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'





####### NO NEED TO RELOAD DATA, it is saved by generate_bandwidth... ###########







FIGNAME = 'behavior_inactivation'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2017acnih', FIGNAME)

PANELS_TO_PLOT = [1,1]  # [Experimental, Model]

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'behavior_inactivation' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [14,6]

fontSizeLabels = 14 #12
fontSizeTicks = 12 #10
fontSizePanel = 16
labelDis = 0.1
labelPosX = [0.07, 0.45]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels


animal = 'band011'
sessions = ['20170314a','20170315a','20170324a']
colours = ['k','m']

# -- From jaratest/anna/behaviour_test.py --
def band_SNR_laser_psychometric(animal, sessions, trialTypes='laserSide', paradigm='2afc', xlabel=True, ylabel=True):
    loader = dataloader.DataLoader(animal)
    validPerSNR = None
    rightPerSNR = None
    for ind, session in enumerate(sessions):
        behavFile = loadbehavior.path_to_behavior_data(animal,paradigm,session)
        behavData = loader.get_session_behavior(behavFile)
        ax = plt.gca()
        ax.cla()
        possibleSNRs = np.unique(behavData['currentSNR'])
        laserTrialTypes = np.unique(behavData[trialTypes])
        trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['currentSNR'], possibleSNRs, 
                                                                        behavData[trialTypes], laserTrialTypes)
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
    return validPerSNR, rightPerSNR, possibleSNRs, laserTrialTypes

# -- From jaratest/anna/behaviour_test.py --
def plot_psychometric(validPerSNR, rightPerSNR, possibleSNRs, colour = 'k', xlabel=True, ylabel=True):
    from statsmodels.stats.proportion import proportion_confint
    performance = []
    upper = []
    lower = []
    for inds in range(len(possibleSNRs)):
        CIthisSNR = np.array(proportion_confint(rightPerSNR[inds], validPerSNR[inds], method = 'wilson'))
        performance.append(100.0*rightPerSNR[inds]/validPerSNR[inds])
        upper.append(100.0*CIthisSNR[1]-performance[-1])
        lower.append(performance[-1]-100.0*CIthisSNR[0])
    plt.plot(np.arange(len(possibleSNRs)), performance, marker='o', color=colour, lw=3, ms=10)
    plt.errorbar(np.arange(len(possibleSNRs)), performance, yerr = [lower, upper],color=colour)
    if ylabel:
        plt.ylabel("% rightward", fontsize=16)
    if xlabel:
        plt.xlabel('SNR (dB)', fontsize=16)
    plt.xticks(np.arange(len(possibleSNRs)), possibleSNRs)
    plt.ylim((0,100))

validPerSNR, rightPerSNR, possibleSNRs, laserTrialTypes = band_SNR_laser_psychometric(animal, sessions)
plt.clf()
for las in range(len(validPerSNR)):
    plot_psychometric(validPerSNR[las,:], rightPerSNR[las,:], possibleSNRs, colour = colours[las])
plt.ylabel('% rightward choice', fontsize=fontSizeLabels)
plt.xlabel('Signal to noise ratio (dB)', fontsize=fontSizeLabels)
plt.show()

