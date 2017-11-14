import os
import sys
import importlib
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratest.anna.analysis import band_behaviour_analysis as bb
reload(bb)
from scipy import stats

def plot_psychometric(validPerSNR, rightPerSNR, possibleSNRs, colour = 'k', linestyle='-', xlabel=True, ylabel=True):
    from statsmodels.stats.proportion import proportion_confint
    import pdb
    performance = []
    upper = []
    lower = []
    for inds in range(len(possibleSNRs)):
        #pdb.set_trace()
        CIthisSNR = np.array(proportion_confint(rightPerSNR[inds], validPerSNR[inds], method = 'wilson'))
        performance.append(100.0*rightPerSNR[inds]/validPerSNR[inds])
        upper.append(100.0*CIthisSNR[1]-performance[-1])
        lower.append(performance[-1]-100.0*CIthisSNR[0])
    plt.plot(np.arange(len(possibleSNRs)), performance, linestyle, marker='o', color=colour, lw=3, ms=10)
    plt.errorbar(np.arange(len(possibleSNRs)), performance, yerr = [lower, upper],color=colour)
    if ylabel:
        plt.ylabel("% rightward", fontsize=16)
    if xlabel:
        plt.xlabel('SNR (dB)', fontsize=16)
    plt.xticks(np.arange(len(possibleSNRs)), possibleSNRs)
    plt.ylim((0,100))

PVAnimals = ['band017', 'band020']
laserPVSessions = ['20170422a','20170423a','20170424a','20170426a','20170427a','20170428a','20170429a','20170430a','20170501a','20170502a','20170503a','20170504a','20170505a','20170506a','20170507a','20170508a']

bdata = behavioranalysis.load_many_sessions('band017', laserPVSessions)
valid, right, pos = bb.band_psychometric('band017', laserPVSessions, trialTypes = ['currentSNR', 'currentBand', 'laserSide'])

colours = ['b','r','k']
linestyle = ['-','--']
for band in range(len(pos[1])):
    for las in range(len(pos[2])):
        plot_psychometric(valid[:,band,las], right[:,band,las], pos[0], colour = colours[band], linestyle=linestyle[las])
plt.show()