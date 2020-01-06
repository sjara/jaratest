"""
Tuning curve figure for 2019astrpi
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import celldatabase
from scipy import stats
import pandas as pd
import figparams
import studyparams


if sys.version_info[0] < 3:
    inputFunc = raw_input
elif sys.version_info[0] >= 3:
    inputFunc = input


def jitter(arr, frac):
    jitter_value = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter_value
    return jitteredArr


def medline(ax, yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    ax.plot([start, end], [yval, yval], color=color, lw=linewidth)
# ==========================parameters==========================================


FIGNAME = 'figure_frequency_tuning'

d1mice = studyparams.ASTR_D1_CHR2_MICE
nameDB = '_'.join(d1mice) + '.h5'
# pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, '{}.h5'.format('temp'))
# os.path.join(studyparams.PATH_TO_TEST,nameDB)
db = celldatabase.load_hdf(pathtoDB)
db = db.query('rsquaredFit>{}'.format(studyparams.R2_CUTOFF))
exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')

# =======================================================================

exData = np.load(exampleDataPath)  # npz data generated from generate_example_freq_tuning
np.random.seed(8)

D1 = db.query('laserpulse_pVal<0.05')  # bothsoundlaser
nD1 = db.query('laserpulse_pVal>0.05')  # onlysoundnolaser

PANELS = [1, 1, 1, 1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'figure_frequency_tuning'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
figSize = [17.25, 5.75]  # In inches (originally [13, 6.5]. Matt changed to current values based off Nick's paper)

fontSizeLabels = figparams.fontSizeLabels*2
# fontSizeTicks = figparams.fontSizeTicks*2
fontSizeTicks = fontSizeLabels
fontSizePanel = figparams.fontSizePanel*2
fontSizeTitles = figparams.fontSizeTitles*2

# Params for extraplots significance stars
fontSizeNS = figparams.fontSizeNS
fontSizeStars = figparams.fontSizeStars
starHeightFactor = figparams.starHeightFactor
starGapFactor = figparams.starGapFactor
starYfactor = figparams.starYfactor

dotEdgeColor = figparams.dotEdgeColor
nd1ColorMap = 'Reds'
d1ColorMap = 'Blues'

colornD1 = figparams.cp.TangoPalette['ScarletRed1']
colorD1 = figparams.cp.TangoPalette['SkyBlue2']
markerAlpha = 1

# labelPosX = [0.05, 0.24, 0.45, 0.64, 0.835]   Old sizes from Allison. Updated below to match Nick's
# labelPosY = [0.92, 0.42]
labelPosX = [0.02, 0.24, 0.45, 0.64, 0.835]   # Horiz position for panel labels
labelPosY = [0.92, 0.42]    # Vert position for panel labels


# Define colors, use figparams
laserColor = figparams.colp['blueLaser']
fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

# Define the layout
# gs = gridspec.GridSpec(2, 5)
# gs.update(left=0.02, right=0.98, top=0.95, bottom=0.125, wspace=0.7, hspace=0.5)
gs = gridspec.GridSpec(2, 7)
gs.update(left=0.04, right=0.98, top=0.95, bottom=0.175, wspace=1.1, hspace=0.5)

ndOne = plt.subplot(gs[0, 0:2])
dOne = plt.subplot(gs[1, 0:2])

axBW = plt.subplot(gs[0:2, 2])
axThresh = plt.subplot(gs[0:2, 3])
axLatency = plt.subplot(gs[0:2, 4])

axOnsetivity = plt.subplot(gs[0:2, 5])
axMonotonicity = plt.subplot(gs[0:2, 6])

plt.text(-0.3, 1.03, 'A', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=ndOne.transAxes)
plt.text(-0.3, 1.03, 'B', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=dOne.transAxes)
plt.text(-0.3, 1.01, 'C', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axBW.transAxes)
plt.text(-0.3, 1.01, 'D', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axThresh.transAxes)
plt.text(-0.3, 1.01, 'E', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axLatency.transAxes)
plt.text(-0.3, 1.01, 'F', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axOnsetivity.transAxes)
plt.text(-0.3, 1.01, 'G', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axMonotonicity.transAxes)

messages = []
# ============================================================================
lowFreq = 2
highFreq = 40
nFreqLabels = 3

freqTickLocations = np.linspace(0, 15, nFreqLabels)
freqs = np.logspace(np.log10(lowFreq), np.log10(highFreq), nFreqLabels)
freqs = np.round(freqs, decimals=1)

nIntenLabels = 3
intensities = np.linspace(15, 70, nIntenLabels)
intenTickLocations = np.linspace(0, 11, nIntenLabels)

# ===========================Create and save figures=============================
# ---- TC Heatmap example 1 ----
if PANELS[0]:
    exampleKey = 'D1'
    exDataFR = exData[exampleKey]/0.1
    cax = dOne.imshow(np.flipud(exDataFR), interpolation='nearest', cmap=d1ColorMap)
    cbar = plt.colorbar(cax, ax=dOne, format='%d')
    maxFR = np.max(exDataFR.ravel())
    cbar.set_label('Firing rate\n(spk/s)', fontsize=fontSizeLabels, labelpad=-10)
    extraplots.set_ticks_fontsize(cbar.ax, fontSizeTicks)
    cbar.set_ticks([0, maxFR])
    cax.set_clim([0, maxFR])

    dOne.set_yticks(intenTickLocations)
    dOne.set_yticklabels(intensities[::-1])
    dOne.set_xticks(freqTickLocations)
    freqLabels = ['{0:.1f}'.format(freq) for freq in freqs]
    dOne.set_xticklabels(freqLabels)
    dOne.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)
    dOne.set_ylabel('Intensity (dB SPL)', fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(dOne, fontSizeTicks)

# ---- TC Heatmap example 2 ----
if PANELS[1]:
    exampleKey = 'nD1'
    exDataFR = exData[exampleKey]/0.1

    cax = ndOne.imshow(np.flipud(exDataFR), interpolation='nearest', cmap=nd1ColorMap)
    cbar = plt.colorbar(cax, ax=ndOne, format='%d')
    maxFR = np.max(exDataFR.ravel())
    cbar.set_label('Firing rate\n(spk/s)', fontsize=fontSizeLabels, labelpad=-10)
    extraplots.set_ticks_fontsize(cbar.ax, fontSizeTicks)
    cbar.set_ticks([0, maxFR])
    cax.set_clim([0, maxFR])

    ndOne.set_yticks(intenTickLocations)
    ndOne.set_yticklabels(intensities[::-1])
    ndOne.set_xticks(freqTickLocations)
    freqLabels = ['{0:.1f}'.format(freq) for freq in freqs]
    ndOne.set_xticklabels(freqLabels)
    ndOne.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)
    ndOne.set_ylabel('Intensity (dB SPL)', fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(ndOne, fontSizeTicks)

# plt.hold(True)

# ======================= Beginning of plotting for BW10 ================================

if PANELS[2]:

    popStatCol = 'bw10'
    D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
    nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]

    pos = jitter(np.ones(len(nD1PopStat))*0, 0.20)
    axBW.plot(pos, nD1PopStat, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)
    medline(axBW, np.median(nD1PopStat), 0, 0.5)
    pos = jitter(np.ones(len(D1PopStat))*1, 0.20)
    axBW.plot(pos, D1PopStat, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
    medline(axBW, np.median(D1PopStat), 1, 0.5)
    axBW.set_ylabel('BW10', fontsize=fontSizeLabels)

    tickLabels = ['nD1:Str\nn={}'.format(len(nD1PopStat)), 'D1:Str\nn={}'.format(len(D1PopStat))]
    axBW.set_xticks(range(2))
    axBW.set_xlim([-0.5, 1.5])
    extraplots.boxoff(axBW)
    extraplots.set_ticks_fontsize(axBW, fontSizeTicks)
    axBW.set_xticklabels(tickLabels, fontsize=fontSizeLabels, rotation=45)

    zstat, pVal = stats.mannwhitneyu(nD1PopStat, D1PopStat)  # Nick used stats.ranksum

    messages.append("{} p={}".format(popStatCol, pVal))

    yDataMax = max([max(D1PopStat), max(nD1PopStat)])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor
    plt.sca(axBW)
    starString = None if pVal < 0.05 else 'n.s.'
    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                  starSize=fontSizeStars+2, starString=starString,
                                  gapFactor=starGapFactor)
    #plt.hold(1)
#
#plt.hold(True)

# ======================= Beginning of plotting for threshold ================================
if PANELS[3]:

    popStatCol = 'thresholdFRA'
    D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
    nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]

    plt.sca(axThresh)

    spacing = 0.05

    markers = extraplots.spread_plot(0, nD1PopStat, spacing)
    plt.setp(markers, mec=colornD1, mfc='None')
    medline(axThresh, np.median(nD1PopStat), 0, 0.5)

    markers = extraplots.spread_plot(1, D1PopStat, spacing)
    plt.setp(markers, mec=colorD1, mfc='None')

    medline(axThresh, np.median(D1PopStat), 1, 0.5)
    axThresh.set_ylabel('Threshold (dB SPL)', fontsize=fontSizeLabels)
    tickLabels = ['nD1:Str\nn={}'.format(len(nD1PopStat)), 'D1:Str\nn={}'.format(len(D1PopStat))]
    axThresh.set_xticks(range(2))
    axThresh.set_xlim([-0.5, 1.5])
    extraplots.boxoff(axThresh)
    extraplots.set_ticks_fontsize(axThresh, fontSizeTicks)

    axThresh.set_xticklabels(tickLabels, fontsize=fontSizeLabels, rotation=45)

    zstat, pVal = stats.mannwhitneyu(D1PopStat, nD1PopStat)  # Nick used stats.ranksum

    messages.append("{} p={}".format(popStatCol, pVal))

    yDataMax = max([max(nD1PopStat), max(D1PopStat)])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor
    starString = None if pVal < 0.05 else 'n.s.'
    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                  starSize=fontSizeStars, starString=starString,
                                  gapFactor=starGapFactor)
    #plt.hold(1)

# ======================= Beginning of plotting for latency ================================
if PANELS[4]:

    popStatCol = 'latency'
    D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
    nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]

    pos = jitter(np.ones(len(nD1PopStat))*0, 0.20)
    axLatency.plot(pos, nD1PopStat*1000, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)
    medline(axLatency, np.median(nD1PopStat)*1000, 0, 0.5)
    pos = jitter(np.ones(len(D1PopStat))*1, 0.20)
    axLatency.plot(pos, D1PopStat*1000, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
    medline(axLatency, np.median(D1PopStat)*1000, 1, 0.5)
    axLatency.set_ylabel('Latency (ms)', fontsize=fontSizeTicks)
    # tickLabels = ['ATh:Str', 'AC:Str']
    tickLabels = ['nD1:Str\nn={}'.format(len(nD1PopStat)), 'D1:Str\nn={}'.format(len(D1PopStat))]
    axLatency.set_xticks(range(2))
    axLatency.set_xlim([-0.5, 1.5])
    extraplots.boxoff(axLatency)
    axLatency.set_ylim([-0.001, 18])

    extraplots.set_ticks_fontsize(axLatency, fontSizeTicks)
    axLatency.set_xticklabels(tickLabels, fontsize=fontSizeLabels, rotation=45)

    zstat, pVal = stats.ranksums(nD1PopStat, D1PopStat)

    # print "Ranksums test between thalamus and AC population stat ({}) vals: p={}".format(popStatCol, pVal) Remove Matt
    messages.append("{} p={}".format(popStatCol, pVal))

    yDataMax = max([max(D1PopStat*700), max(nD1PopStat*700)])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor
    starString = None if pVal < 0.05 else 'n.s.'
    plt.sca(axLatency)
    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                  starSize=fontSizeStars, starString=starString,
                                  gapFactor=starGapFactor)
    #plt.hold(1)

# ======================= Beginning of plotting for Onset to sustained ratio ================================

if PANELS[5]:

    popStatCol = 'cfOnsetivityIndex'
    D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
    nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]

    pos = jitter(np.ones(len(nD1PopStat))*0, 0.20)
    axOnsetivity.plot(pos, nD1PopStat, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)
    medline(axOnsetivity, np.median(nD1PopStat), 0, 0.5)
    pos = jitter(np.ones(len(D1PopStat))*1, 0.20)
    axOnsetivity.plot(pos, D1PopStat, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
    medline(axOnsetivity, np.median(D1PopStat), 1, 0.5)
    # axOnsetivity.set_ylabel('Onsetivity index', fontsize=fontSizeTicks)
    axOnsetivity.set_ylabel('Onset to sustained ratio', fontsize=fontSizeLabels)
    # tickLabels = ['ATh:Str', 'AC:Str']
    tickLabels = ['nD1:Str\nn={}'.format(len(nD1PopStat)), 'D1:Str\nn={}'.format(len(D1PopStat))]
    axOnsetivity.set_xticks(range(2))
    axOnsetivity.set_xlim([-0.5, 1.5])
    axOnsetivity.set_ylim([-0.51, 1.1])
    extraplots.boxoff(axOnsetivity)

    extraplots.set_ticks_fontsize(axOnsetivity, fontSizeTicks)
    axOnsetivity.set_xticklabels(tickLabels, fontsize=fontSizeLabels, rotation=45)

    zstat, pVal = stats.ranksums(nD1PopStat, D1PopStat)

    # print "Ranksums test between thalamus and AC population stat ({}) vals: p={}".format(popStatCol, pVal)
    messages.append("{} p={}".format(popStatCol, pVal))

    yDataMax = max([max(D1PopStat), max(nD1PopStat)])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor
    # starString = None if pVal<0.05 else 'n.s.'
    plt.sca(axOnsetivity)
    if pVal < 0.05:
        starString = None
        starSize = fontSizeStars
    else:
        starString = 'n.s.'
        starSize = fontSizeNS

    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                  starSize=starSize, starString=starString,
                                  gapFactor=starGapFactor)
    #plt.hold(1)

# ======================= Beginning of plotting for monotonicity index ================================
if PANELS[6]:

    popStatCol = 'monotonicityIndex'
    D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
    nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]

    pos = jitter(np.ones(len(nD1PopStat))*0, 0.20)
    axMonotonicity.plot(pos, nD1PopStat, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)
    medline(axMonotonicity, np.median(nD1PopStat), 0, 0.5)
    pos = jitter(np.ones(len(D1PopStat))*1, 0.20)
    axMonotonicity.plot(pos, D1PopStat, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
    medline(axMonotonicity, np.median(D1PopStat), 1, 0.5)
    axMonotonicity.set_ylabel('Monotonicity index', fontsize=fontSizeLabels)
    tickLabels = ['nD1:Str\nn={}'.format(len(nD1PopStat)), 'D1:Str\nn={}'.format(len(D1PopStat))]
    axMonotonicity.set_xticks(range(2))
    axMonotonicity.set_xlim([-0.5, 1.5])
    axMonotonicity.set_ylim([0, 1.1])
    extraplots.boxoff(axMonotonicity)

    extraplots.set_ticks_fontsize(axMonotonicity, fontSizeTicks)
    axMonotonicity.set_xticklabels(tickLabels, fontsize=fontSizeLabels, rotation=45)

    zstat, pVal = stats.ranksums(nD1PopStat, D1PopStat)

    # print "Ranksums test between thalamus and AC population stat ({}) vals: p={}".format(popStatCol, pVal)
    messages.append("{} p={}".format(popStatCol, pVal))

    yDataMax = max([max(D1PopStat), max(nD1PopStat)])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor
    # starString = None if pVal<0.05 else 'n.s.'
    plt.sca(axMonotonicity)
    if pVal < 0.05:
        starString = None
        starSize = fontSizeStars
    else:
        starString = 'n.s.'
        starSize = fontSizeNS

    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                  starSize=starSize, starString=starString,
                                  gapFactor=starGapFactor)
    #plt.hold(1)
fig1 = plt.gcf()

print("\nSTATISTICS:\n")
for message in messages:
    print(message)
print("\n")

if SAVE_FIGURE:
    if os.path.isdir(figparams.FIGURE_OUTPUT_DIR):
        pass
        extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
        print('{} saved to {}'.format(figFilename, figparams.FIGURE_OUTPUT_DIR))
    elif not os.path.isdir(os.path.join(figparams.FIGURE_OUTPUT_DIR)):
        answer = inputFunc(
                            "Save folder is not present. Would you like to make the desired directory now? (y/n) ")
        if answer in ['y', 'Y', 'Yes', 'YES']:
            os.mkdir(
                os.path.join(figparams.FIGURE_OUTPUT_DIR))
            extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
            print('{} saved to {}'.format(figFilename, figparams.FIGURE_OUTPUT_DIR))

plt.show()
