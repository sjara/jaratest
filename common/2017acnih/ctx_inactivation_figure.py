from statsmodels.stats.proportion import proportion_confint
import numpy as np
import pandas as pd
from jaratest.nick.database import dataloader_v2 as dataloader
from jaratest.anna import bandwidths_analysis_v2 as bandan
from jaratest.anna import behaviour_test as bt
reload(bt)
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
import matplotlib.gridspec as gridspec
import matplotlib


PRINT_FIGURE = 1

gs = gridspec.GridSpec(2,2)
gs.update(left=0.15, right=0.85, wspace=0.4, hspace=0.4)
labelPosX = [0.08, 0.48]
labelPosY = [0.92, 0.46]

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'


fontSizeLabels = 14
fontSizeTicks = 12
fontSizePanel = 16

muscimolColor = cp.TangoPalette['Orange2']
laserColor = cp.TangoPalette['Plum1']


animal = 'band008'
sessions = ['20161130a','20161201a','20161202a','20161203a','20161204a','20161205a', '20161206a', '20161207a']
plt.subplot(gs[0,0])
validPerSNR, rightPerSNR, possibleSNRs = bt.band_SNR_psychometric(animal, sessions[::2])
bt.plot_psychometric(validPerSNR, rightPerSNR, possibleSNRs)
validPerSNR, rightPerSNR, possibleSNRs = bt.band_SNR_psychometric(animal, sessions[1::2])
bt.plot_psychometric(validPerSNR, rightPerSNR, possibleSNRs, colour=muscimolColor)
plt.ylabel('% rightward choice', fontsize=fontSizeLabels)
plt.xlabel('Signal to noise ratio (dB)', fontsize=fontSizeLabels)

animals = ['band006','band008','band010']
plt.subplot(gs[0,1])
for animal in animals:
    salValid, salCorrect = bt.behav_stats(animal, sessions[::2])
    musValid, musCorrect = bt.behav_stats(animal, sessions[1::2])
    salAccuracy = 100.0*salCorrect/salValid
    musAccuracy = 100.0*musCorrect/musValid
    plt.plot([1,2],[salAccuracy,musAccuracy], '-o', color='k', lw=2)
    salCI = np.array(proportion_confint(salCorrect, salValid, method = 'wilson'))
    musCI = np.array(proportion_confint(musCorrect, musValid, method = 'wilson'))
    upper = [(100.0*salCI[1]-salAccuracy),(100.0*musCI[1]-musAccuracy)]
    lower = [(salAccuracy-100.0*salCI[0]), (musAccuracy-100.0*musCI[0])]
    plt.errorbar([1,2], [salAccuracy, musAccuracy], yerr = [lower, upper],color='k')
plt.xlim([0.5,2.5])
plt.ylim([50,100])
ax = plt.gca()
ax.set_xticks([1,2])
ax.set_xticklabels(['saline', 'muscimol'],fontsize=fontSizeLabels)
plt.ylabel('Accuracy (%)',fontsize=fontSizeLabels)
    
animal = 'band017'
sessions = ['20170228a','20170226a','20170224a','20170222a']
plt.subplot(gs[1,0])
validPerSNR, rightPerSNR, possibleSNRs, laserTrialTypes = bt.band_SNR_laser_psychometric(animal, sessions)
colours = ['k',laserColor]
for las in range(len(validPerSNR)):
    bt.plot_psychometric(validPerSNR[las,:], rightPerSNR[las,:], possibleSNRs, colour = colours[las])
plt.ylabel('% rightward choice', fontsize=fontSizeLabels)
plt.xlabel('Signal to noise ratio (dB)', fontsize=fontSizeLabels)
   
animals = ['band017', 'band020']
plt.subplot(gs[1,1])
for animal in animals:
    valid, correct = bt.behav_laser_stats(animal, sessions[::2])
    conAccuracy = 100.0*correct[0]/valid[0]
    lasAccuracy = 100.0*correct[1]/valid[1]
    plt.plot([1,2],[conAccuracy,lasAccuracy], '-o', color='k', lw=2)
    conCI = np.array(proportion_confint(correct[0], valid[0], method = 'wilson'))
    lasCI = np.array(proportion_confint(correct[1], valid[1], method = 'wilson'))
    upper = [(100.0*conCI[1]-conAccuracy),(100.0*lasCI[1]-lasAccuracy)]
    lower = [(conAccuracy-100.0*conCI[0]), (lasAccuracy-100.0*lasCI[0])]
    plt.errorbar([1,2], [conAccuracy, lasAccuracy], yerr = [lower, upper],color='k')
plt.xlim([0.5,2.5])
plt.ylim([50,100])
ax = plt.gca()
ax.set_xticks([1,2])
ax.set_xticklabels(['no laser', 'laser'],fontsize=fontSizeLabels)
plt.ylabel('Accuracy (%)',fontsize=fontSizeLabels)

plt.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.annotate('D', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()


figFormat = 'svg'#'pdf' #'svg' 
figFilename = 'ac_inactivation' # Do not include extension
outputDir = '/tmp/'
if PRINT_FIGURE:
    extraplots.save_figure(figFilename, figFormat, [10,8], outputDir)

