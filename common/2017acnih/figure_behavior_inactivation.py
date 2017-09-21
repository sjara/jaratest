'''
Figure showing performance in signal extraction task with inactivation (of AC or specific cells).
'''

import os
import sys
from statsmodels.stats.proportion import proportion_confint
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
from statsmodels.stats.proportion import proportion_confint
matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'


FIGNAME = 'ac_inactivation_behavior'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2017acnih', FIGNAME)

PANELS_TO_PLOT = [1,1]  # [Experimental, Model]

filenameArchCaMKIIpsycurve = 'band011_CaMKII_inactivation_psychometric.npz'

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

dataFullPath = os.path.join(dataDir,filenameArchCaMKIIpsycurve)
data = np.load(dataFullPath)

laserColor = [cp.TangoPalette['Butter3'],cp.TangoPalette['Butter1']]
colors = ['k','m']

'''
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
'''

# -- From jaratest/anna/behaviour_test.py --
def plot_psychometric(validPerSNR, rightPerSNR, possibleSNRs, color = 'k', xlabel=True, ylabel=True):
    performance = []
    upper = []
    lower = []
    for inds in range(len(possibleSNRs)):
        CIthisSNR = np.array(proportion_confint(rightPerSNR[inds], validPerSNR[inds], method = 'wilson'))
        performance.append(100.0*rightPerSNR[inds]/validPerSNR[inds])
        upper.append(100.0*CIthisSNR[1]-performance[-1])
        lower.append(performance[-1]-100.0*CIthisSNR[0])
    plt.plot(np.arange(len(possibleSNRs)), performance, marker='o', color=color, lw=3, ms=10, clip_on=False)
    plt.errorbar(np.arange(len(possibleSNRs)), performance, yerr = [lower, upper],color=color, clip_on=False)
    if ylabel:
        plt.ylabel("% rightward", fontsize=16)
    if xlabel:
        plt.xlabel('SNR (dB)', fontsize=16)
    plt.xticks(np.arange(len(possibleSNRs)), possibleSNRs)
    plt.ylim((0,100))

#validPerSNR, rightPerSNR, possibleSNRs, laserTrialTypes = band_SNR_laser_psychometric(animal, sessions)

validPerSNR = data['validPerSNR']
possibleSNRs = data['possibleSNRs']
rightPerSNR = data['rightPerSNR']


plt.clf()
ax1 = plt.gca()
for las in range(len(validPerSNR)):
    plot_psychometric(validPerSNR[las,:], rightPerSNR[las,:], possibleSNRs, color = colors[las])
extraplots.boxoff(ax1)
plt.ylabel('Rightward choice (%)', fontsize=fontSizeLabels)
plt.xlabel('Signal to noise ratio (dB)', fontsize=fontSizeLabels)
plt.show()

