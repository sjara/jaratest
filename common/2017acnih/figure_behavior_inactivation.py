'''
Figure showing performance in signal extraction task with inactivation (of AC or specific cells).
'''

import os
import sys
from statsmodels.stats.proportion import proportion_confint
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
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
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [8,4]

fontSizeLabels = 14 #12
fontSizeTicks = 12 #10
fontSizePanel = 16
labelDis = 0.1
labelPosX = [0.07, 0.45]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

dataFullPath = os.path.join(dataDir,filenameArchCaMKIIpsycurve)
data = np.load(dataFullPath)

#laserColor = [cp.TangoPalette['Butter3'],cp.TangoPalette['Butter1']]
colors = ['k', cp.TangoPalette['Butter3']]

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,2)
gs.update(top=0.9, left=0.05, bottom=0.15, right=0.98, wspace=0.25, hspace=0.25)

#axTask = plt.subplot(gs[0,0])

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
    plt.plot(np.arange(len(possibleSNRs)), performance, marker='o', color=color, mec='none', lw=3, ms=10, clip_on=False)
    plt.errorbar(np.arange(len(possibleSNRs)), performance, yerr = [lower, upper],color=color, clip_on=False)
    if ylabel:
        plt.ylabel("% rightward", fontsize=16)
    if xlabel:
        plt.xlabel('SNR (dB)', fontsize=16)
    plt.xticks(np.arange(len(possibleSNRs)), possibleSNRs)
    plt.ylim((0,100))
#validPerSNR, rightPerSNR, possibleSNRs, laserTrialTypes = band_SNR_laser_psychometric(animal, sessions)
'''

validPerSNReach = data['validPerSNR']
rightPerSNReach = data['rightPerSNR']
possibleSNRs = data['possibleSNRs']

ax1 = plt.subplot(gs[0,1])
pHandles = []
for las in range(len(validPerSNReach)):
    validPerSNR = validPerSNReach[las,:]
    rightPerSNR = rightPerSNReach[las,:]
    thisColor = colors[las]
    performance = []
    upper = []
    lower = []
    for inds in range(len(possibleSNRs)):
        CIthisSNR = np.array(proportion_confint(rightPerSNR[inds], validPerSNR[inds], method = 'wilson'))
        performance.append(100.0*rightPerSNR[inds]/validPerSNR[inds])
        upper.append(100.0*CIthisSNR[1]-performance[-1])
        lower.append(performance[-1]-100.0*CIthisSNR[0])
    thisPlot, = plt.plot(np.arange(len(possibleSNRs)), performance, marker='o', color=thisColor, mec='none', lw=3, ms=10, clip_on=False)
    pHandles.append(thisPlot)
    plt.errorbar(np.arange(len(possibleSNRs)), performance, yerr = [lower, upper], color=thisColor, clip_on=False)

plt.xticks(np.arange(len(possibleSNRs)), possibleSNRs)
plt.xlim([-0.2, len(possibleSNRs)-1+0.2])
plt.ylim((0,100))
plt.legend(pHandles,['Control','No E cells'], loc='upper left', numpoints=1, markerscale=1, handlelength=1.5, frameon=False)

extraplots.boxoff(ax1)
#plt.ylabel('Rightward choice (%)', fontsize=fontSizeLabels)
plt.ylabel('Signal detection rate (%)', fontsize=fontSizeLabels)
plt.xlabel('Signal to noise ratio (dB)', fontsize=fontSizeLabels)
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
