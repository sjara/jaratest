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
figSize = [7,5]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1
labelPosX = [0.02, 0.54]   # Horiz position for panel labels
labelPosY = [0.95, 0.95]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 2)
gs.update(left=0.12, right=0.9, top=0.95, bottom=0.1, wspace=0.2, hspace=0.15)


# -- Panel A: medial to lateral distribution of tuning frequency in head-fixed astr -- #
ax1 = plt.subplot(gs[0, 0])
plt.axis('off')
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


# -- Panel B: relationship between tuning freq of a photostim site and the resulting contralateral behavioral bias -- #
ax2 = plt.subplot(gs[0,1])
extraplots.boxoff(ax2)
ax2.annotate('B', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

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
allFreqs = np.concatenate([left014Freqs, left015Freqs, left016Freqs, right014Freqs, right015Freqs, right016Freqs])
allRightBias = 100*np.concatenate([left014, left015, left016, right014, right015, right016])

ax2.scatter(allFreqs[~np.isnan(allFreqs)], allRightBias[~np.isnan(allFreqs)])
ax2.set_xlabel('Preferred frequency to boundary (octaves)')
ax2.set_ylabel('Bias to high freq: stim - control (%)')
ax2.set_xlim([-1.7, 1.7])

r, pVal = stats.spearmanr(allFreqs[~np.isnan(allFreqs)], allRightBias[~np.isnan(allFreqs)])
ax2.text(-1.0,50, 'p value for spearman correlation test is {}'.format(pVal))
#plt.show()
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

