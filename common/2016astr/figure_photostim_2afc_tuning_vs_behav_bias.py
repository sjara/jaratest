import os
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.lines as mlines
import scipy.stats as stats
import figparams
reload(figparams)

STUDY_NAME = '2016astr'
FIGNAME = 'photostim_2afc'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1] # Which panels to plot

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_photostim_2afc_tuning_vs_behav_bias' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,4]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1
labelPosX = [0.02, 0.48]   # Horiz position for panel labels
labelPosY = [0.95, 0.95]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 2)
gs.update(left=0.1, right=0.95, top=0.95, bottom=0.12, wspace=0.25, hspace=0.15)

PHOTOSTIMCOLORS = {'no_laser':'k',
                   'laser_left':figparams.colp['stimLeft'],
                   'laser_right':figparams.colp['stimRight']}

# -- Panel A: medial to lateral distribution of tuning frequency in head-fixed astr -- #
ax1 = plt.subplot(gs[0, 0])

ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

# -- Load data about freq preference from bilaterally implanted mice -- #
FIGNAME_tuning = 'sound_freq_selectivity'
dataDir_tuning = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME_tuning)

summaryFilename_tuning = 'summary_bilateral_best_freq.npz'
summaryFullPath_tuning = os.path.join(dataDir_tuning,summaryFilename_tuning)
summary_tuning = np.load(summaryFullPath_tuning)

left014Freqs = summary_tuning['d1pi014_left']
left015Freqs = summary_tuning['d1pi015_left']
left016Freqs = summary_tuning['d1pi016_left']
right014Freqs = summary_tuning['d1pi014_right']
right015Freqs = summary_tuning['d1pi015_right']
right016Freqs = summary_tuning['d1pi016_right']
left014FreqsSessions = summary_tuning['d1pi014_left_sessions']
left015FreqsSessions = summary_tuning['d1pi015_left_sessions']
left016FreqsSessions = summary_tuning['d1pi016_left_sessions']
right014FreqsSessions = summary_tuning['d1pi014_right_sessions']
right015FreqsSessions = summary_tuning['d1pi015_right_sessions']
right016FreqsSessions = summary_tuning['d1pi016_right_sessions']

allLeftFreqs = np.concatenate([left014Freqs, left015Freqs])
allRightFreqs = np.concatenate([right015Freqs, right016Freqs])

plt.hold('True')
randOffset = 0.3*(np.random.rand(len(allLeftFreqs))-0.5)
ax1.plot(1+randOffset, allLeftFreqs, 'o', mec=PHOTOSTIMCOLORS['laser_left'], mfc='None')
randOffset = 0.3*(np.random.rand(len(allRightFreqs))-0.5)
ax1.plot(2+randOffset, allRightFreqs, 'o', mec=PHOTOSTIMCOLORS['laser_right'], mfc='None')

meanLeftFreq = np.mean(allLeftFreqs)
meanRightFreq = np.mean(allRightFreqs)
ax1.plot(0.3*np.array([-1,1])+1, 100*np.tile(meanLeftFreq,2), lw=3, color=PHOTOSTIMCOLORS['laser_left'])
ax1.plot(0.3*np.array([-1,1])+2, 100*np.tile(meanRightFreq,2), lw=3, color=PHOTOSTIMCOLORS['laser_right'])

xlim = [0, 3]
ylim = [-0.8, 1]
plt.xlim(xlim)
plt.ylim(ylim)
xticks = [1,2]
xticklabels = ['Left\nhemi', 'Right\nhemi']
plt.xticks(xticks, xticklabels, fontsize=fontSizeTicks)
plt.ylabel('Preferred frequency to boundary (octaves)', fontsize=fontSizeLabels) # labelpad=labelDis
extraplots.boxoff(ax1)
z,pVal = stats.ranksums(allLeftFreqs, allRightFreqs)
print 'Comparing frequencies encoded in left vs right hemi with ranksum test, p value is {}'.format(pVal)
ax1.text(0.7, 0.9, 'p = {}'.format(pVal))


# -- Panel B: relationship between tuning freq of a photostim site and the resulting contralateral behavioral bias -- #
ax2 = plt.subplot(gs[0, 1])
extraplots.boxoff(ax2)
ax2.annotate('B', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

# -- Load data about behavior bias in photostim 2afc from the same mice -- #
FIGNAME_behav = 'photostim_2afc'
dataDir_behav = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME_behav)

summaryFilename_behav = 'summary_photostim_percent_right_choice_change.npz'
summaryFullPath_behav = os.path.join(dataDir_behav,summaryFilename_behav)
summary_behav = np.load(summaryFullPath_behav)

# These numbers are percent change in rightward choice (stim - control) for each condition:
left014 = summary_behav['d1pi014leftHemiStim']
left015 = summary_behav['d1pi015leftHemiStim']
left016 = summary_behav['d1pi016leftHemiStim']
right014 = summary_behav['d1pi014rightHemiStim']
right015 = summary_behav['d1pi015rightHemiStim']
right016 = summary_behav['d1pi016rightHemiStim']

left014sessions = summary_behav['d1pi014leftHemiStimSessions']
left015sessions = summary_behav['d1pi015leftHemiStimSessions']
left016sessions = summary_behav['d1pi016leftHemiStimSessions']
right014sessions = summary_behav['d1pi014rightHemiStimSessions']
right015sessions = summary_behav['d1pi015rightHemiStimSessions']
right016sessions = summary_behav['d1pi016rightHemiStimSessions']

## checked and make sure the sessions for behavior and frequency data matched up
allFreqSessions = np.concatenate([left014FreqsSessions, left015FreqsSessions, left016FreqsSessions, right014FreqsSessions, right015FreqsSessions, right016FreqsSessions])
allBehavSessions = np.concatenate([left014sessions, left015sessions, left016sessions, right014sessions, right015sessions, right016sessions])
assert np.all(allFreqSessions==allBehavSessions), 'Sessions donot match up!'

# -- Plot relationship between tuning freq and rightward bias -- #
# !! Taking out stim sites that were near the border of str & cortex !!
#allFreqs = np.concatenate([left014Freqs, left015Freqs, left016Freqs, right014Freqs, right015Freqs, right016Freqs])
#allRightBias = 100*np.concatenate([left014, left015, left016, right014, right015, right016])

#ax2.scatter(xVal, yVal)
plt.hold('True')
allBiasLeftStim = 100*np.concatenate([left014, left015])
allBiasRightStim = 100*np.concatenate([right015, right016])
ax2.plot(allLeftFreqs, allBiasLeftStim, 'o', mec=PHOTOSTIMCOLORS['laser_left'], mfc='None')
ax2.plot(allRightFreqs, allBiasRightStim, 'o', mec=PHOTOSTIMCOLORS['laser_right'], mfc='None')
ax2.set_xlabel('Preferred frequency to boundary (octaves)')
ax2.set_ylabel('Bias to high freq (%)\nstim - control')

allFreqs = np.concatenate([allLeftFreqs, allRightFreqs])
allBias = np.concatenate([allBiasLeftStim, allBiasRightStim])
xVal = allFreqs[~np.isnan(allFreqs)]
yVal = allBias[~np.isnan(allFreqs)]
slope, intercept, rVal, pVal, stdError = stats.linregress(xVal, yVal)
print 'Using scipy.stats.linregress, the r value is {}, p value is {}'.format(rVal,pVal)
xl = np.linspace(min(xVal), max(xVal), 20)
yl = [slope*xx + intercept  for xx in xl]
ax2.plot(xl, yl, '-k')
rValsp, pValsp = stats.spearmanr(allFreqs[~np.isnan(allFreqs)], allBias[~np.isnan(allFreqs)])
print 'Using spearman correlation test, the r value is {}, p value is {}'.format(rValsp, pValsp)
ax2.set_xlim([-1, 1])
ax2.set_ylim([-50,55])
ax2.text(-0.5,48, 'r = {}\np = {}'.format(rValsp,pValsp))
#plt.show()
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

