from statsmodels.stats.proportion import proportion_confint
import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
import matplotlib.gridspec as gridspec
import matplotlib


PRINT_FIGURE = 1

FIGNAME = 'ac_inactivation_behaviour'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2017acnih', FIGNAME)

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

# subplot showing example psychometric curve during signal extraction task with and without muscimol
animal = 'band008'
filename = 'band008_muscimol_inactivation_psychometric.npz'
dataFullPath = os.path.join(dataDir,filename)
data = np.load(dataFullPath)

plt.subplot(gs[0,0])
condition_colours = ['k', muscimolColor]
possibleSNRs = data['possibleSNRs']
allValidPerSNR = data['validPerSNR']
allRightPerSNR = data['rightPerSNR']
plt.hold(True)
for condition in range(allValidPerSNR.shape[0]):
    performance = []
    upper = []
    lower = []
    validPerSNR = allValidPerSNR[condition,:]
    rightPerSNR = allRightPerSNR[condition,:]
    for inds in range(len(possibleSNRs)):
        CIthisSNR = np.array(proportion_confint(rightPerSNR[inds], validPerSNR[inds], method = 'wilson'))
        performance.append(100.0*rightPerSNR[inds]/validPerSNR[inds])
        upper.append(100.0*CIthisSNR[1]-performance[-1])
        lower.append(performance[-1]-100.0*CIthisSNR[0])
    plt.plot(np.arange(len(possibleSNRs)), performance, marker='o', color=condition_colours[condition], mec=condition_colours[condition], lw=2, ms=5)
    plt.errorbar(np.arange(len(possibleSNRs)), performance, yerr = [lower, upper],color=condition_colours[condition])
plt.xticks(np.arange(len(possibleSNRs)), possibleSNRs)
plt.ylim((0,100))
plt.ylabel('% rightward choice', fontsize=fontSizeLabels)
plt.xlabel('Signal to noise ratio (dB)', fontsize=fontSizeLabels)

# subplot showing decrease in accuracy on muscimol
animals = ['band006','band008','band010']
plt.subplot(gs[0,1])
for animal in animals:
    filename = animal+'_muscimol_inactivation_psychometric.npz'
    dataFullPath = os.path.join(dataDir,filename)
    data = np.load(dataFullPath)
    validPerSNR = data['validPerSNR']
    nCorrect = data['nCorrect']
    salValid = sum(validPerSNR[0,:])
    salCorrect = nCorrect[0]
    musValid = sum(validPerSNR[1,:])
    musCorrect = nCorrect[1]
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


# subplot showing example psychometric curve during signal extraction task during laser inactivation of AC
animal = 'band017'
filename = 'band017_PV_activation_psychometric.npz'
dataFullPath = os.path.join(dataDir,filename)
data = np.load(dataFullPath)
plt.subplot(gs[1,0])

condition_colours = ['k', laserColor]
possibleSNRs = data['possibleSNRs']
allValidPerSNR = data['validPerSNR']
allRightPerSNR = data['rightPerSNR']
plt.hold(True)
for condition in range(allValidPerSNR.shape[0]):
    performance = []
    upper = []
    lower = []
    validPerSNR = allValidPerSNR[condition,:]
    rightPerSNR = allRightPerSNR[condition,:]
    for inds in range(len(possibleSNRs)):
        CIthisSNR = np.array(proportion_confint(rightPerSNR[inds], validPerSNR[inds], method = 'wilson'))
        performance.append(100.0*rightPerSNR[inds]/validPerSNR[inds])
        upper.append(100.0*CIthisSNR[1]-performance[-1])
        lower.append(performance[-1]-100.0*CIthisSNR[0])
    plt.plot(np.arange(len(possibleSNRs)), performance, marker='o', color=condition_colours[condition], mec=condition_colours[condition], lw=2, ms=5)
    plt.errorbar(np.arange(len(possibleSNRs)), performance, yerr = [lower, upper],color=condition_colours[condition])
plt.xticks(np.arange(len(possibleSNRs)), possibleSNRs)
plt.ylim((0,100))
plt.ylabel('% rightward choice', fontsize=fontSizeLabels)
plt.xlabel('Signal to noise ratio (dB)', fontsize=fontSizeLabels)
   
animals = ['band017', 'band020']
plt.subplot(gs[1,1])
for animal in animals:
    filename = animal+'_PV_activation_psychometric.npz'
    dataFullPath = os.path.join(dataDir,filename)
    data = np.load(dataFullPath)
    validPerSNR = data['validPerSNR']
    nCorrect = data['nCorrect']
    conValid = sum(validPerSNR[0,:])
    conCorrect = nCorrect[0]
    lasValid = sum(validPerSNR[1,:])
    lasCorrect = nCorrect[1]
    conAccuracy = 100.0*conCorrect/conValid
    lasAccuracy = 100.0*lasCorrect/lasValid
    plt.plot([1,2],[conAccuracy,lasAccuracy], '-o', color='k', lw=2)
    conCI = np.array(proportion_confint(conCorrect, conValid, method = 'wilson'))
    lasCI = np.array(proportion_confint(lasCorrect, lasValid, method = 'wilson'))
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
