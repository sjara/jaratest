'''
Tuning curve figure for 2019astrpi
'''
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import spikesorting
from jaratoolbox import ephyscore
from jaratoolbox import celldatabase
from jaratoolbox import behavioranalysis
from scipy import stats
import pandas as pd
import figparams
import studyparams
from jaratoolbox import settings
reload(extraplots)
reload(figparams)

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(ax, yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    ax.plot([start, end], [yval, yval], color=color, lw=linewidth)
#==========================parameters==========================================
FIGNAME = 'figure_frequency_tuning'

d1mice = studyparams.ASTR_D1_CHR2_MICE
nameDB = '_'.join(d1mice) + '.h5'
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
# os.path.join(studyparams.PATH_TO_TEST,nameDB)
db = pd.read_hdf(pathtoDB)
db = db.query('rsquaredFit>{}'.format(studyparams.R2_CUTOFF))
exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')

#=======================================================================

exData = np.load(exampleDataPath)
np.random.seed(8)

D1 = db.query('laserpulse_pVal<0.05 and noiseburst_pVal<0.05') #bothsoundlaser
nD1 = db.query('laserpulse_pVal>0.05 and noiseburst_pVal<0.05') #onlysoundnolaser

PANELS = [1, 1, 1, 1, 1, 1, 1, 1, 1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'figure_frequency_tuning' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [13, 6.5] # In inches

fontSizeLabels = figparams.fontSizeLabels*2
# fontSizeTicks = figparams.fontSizeTicks*2
fontSizeTicks = fontSizeLabels
fontSizePanel = figparams.fontSizePanel*2
fontSizeTitles = figparams.fontSizeTitles*2

#Params for extraplots significance stars
fontSizeNS = figparams.fontSizeNS
fontSizeStars = figparams.fontSizeStars
starHeightFactor = figparams.starHeightFactor
starGapFactor = figparams.starGapFactor
starYfactor = figparams.starYfactor

dotEdgeColor = figparams.dotEdgeColor
nd1ColorMap = 'Blues'
d1ColorMap = 'Reds'

colornD1 = figparams.cp.TangoPalette['SkyBlue2']
colorD1 = figparams.cp.TangoPalette['ScarletRed1']
markerAlpha = 1

labelPosX = [0.05, 0.24, 0.45, 0.64, 0.835]   # Horiz position for panel labels
labelPosY = [0.92, 0.42]                      # Vert position for panel labels

# Define colors, use figparams
laserColor = figparams.colp['blueLaser']
fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

#Define the layout
gs = gridspec.GridSpec(2, 5)
gs.update(left=0.02, right=0.98, top=0.95, bottom=0.125, wspace=0.7, hspace=0.5)

ndOne = plt.subplot(gs[0, 0:2])
dOne = plt.subplot(gs[1, 0:2])

axBW = plt.subplot(gs[0:2,2])
axThresh = plt.subplot(gs[0:2, 3])
axLatency = plt.subplot(gs[0:2, 4])

plt.text(-0.25, 1.03, 'A', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=ndOne.transAxes)
plt.text(-0.25, 1.03, 'B', ha='center', va='center',
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

messages = []
#============================================================================
lowFreq = 2
highFreq = 40
nFreqLabels = 3

freqTickLocations = np.linspace(0, 15, nFreqLabels)
freqs = np.logspace(np.log10(lowFreq),np.log10(highFreq),nFreqLabels)
freqs = np.round(freqs, decimals=1)

nIntenLabels = 3
intensities = np.linspace(15, 70, nIntenLabels)
intenTickLocations = np.linspace(0, 11, nIntenLabels)
#===========================Create and save figures=============================
                        ##### TC Heatmap example 1 #####
if PANELS[0]:#
    exampleKey = 'D1'
    exDataFR = exData[exampleKey]/0.1
    cax = dOne.imshow(np.flipud(exDataFR), interpolation='nearest', cmap=d1ColorMap)
    cbar = plt.colorbar(cax, ax=dOne, format='%d')
    maxFR = np.max(exDataFR.ravel())
    cbar.ax.set_ylabel('Firing rate\n(spk/s)', fontsize = fontSizeLabels, labelpad=-10)
    extraplots.set_ticks_fontsize(cbar.ax, fontSizeTicks)
    cbar.set_ticks([0, maxFR])
    cax.set_clim([0, maxFR])


    dOne.set_yticks(intenTickLocations)
    dOne.set_yticklabels(intensities[::-1])
    dOne.set_xticks(freqTickLocations)
    freqLabels = ['{0:.1f}'.format(freq) for freq in freqs]
    # dOne.set_xticklabels(freqLabels, rotation='vertical')
    dOne.set_xticklabels(freqLabels)
    dOne.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)
    dOne.set_ylabel('Intensity (dB SPL)', fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(dOne, fontSizeTicks)

title = 'Cluster{0}'.format(exampleKey)
plt.suptitle(title,fontsize = 15)

        ##### TC Heatmap example 2 #####
if PANELS[3]:
    exampleKey = 'nD1'
    exDataFR = exData[exampleKey]/0.1
    cax = ndOne.imshow(np.flipud(exDataFR), interpolation='nearest', cmap=nd1ColorMap)
    cbar = plt.colorbar(cax, ax=ndOne, format='%d')
    maxFR = np.max(exDataFR.ravel())
    cbar.ax.set_ylabel('Firing rate\n(spk/s)', fontsize = fontSizeLabels, labelpad=-10)
    extraplots.set_ticks_fontsize(cbar.ax, fontSizeTicks)
    cbar.set_ticks([0, maxFR])
    cax.set_clim([0, maxFR])


    ndOne.set_yticks(intenTickLocations)
    ndOne.set_yticklabels(intensities[::-1])
    ndOne.set_xticks(freqTickLocations)
    freqLabels = ['{0:.1f}'.format(freq) for freq in freqs]
    # dOne.set_xticklabels(freqLabels, rotation='vertical')
    ndOne.set_xticklabels(freqLabels)
    ndOne.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)
    ndOne.set_ylabel('Intensity (dB SPL)', fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(ndOne, fontSizeTicks)

title = 'Cluster{0}'.format(exampleKey)
plt.suptitle(title,fontsize = 15)

plt.hold(True)
if PANELS[8]:

    popStatCol = 'bw10'
    D1PopStat = D1.query('{} == {}'.format(popStatCol,popStatCol))[popStatCol]
    nD1PopStat = nD1.query('{} == {}'.format(popStatCol,popStatCol))[popStatCol]
    # D1PopStat = D1.query('bw10 == bw10').bw10
    # nD1PopStat = nD1.query('bw10 == bw10').bw10

    pos = jitter(np.ones(len(nD1PopStat))*0, 0.20)
    axBW.plot(pos, nD1PopStat, 'o', mec = colornD1, mfc = 'None', alpha=markerAlpha)
    medline(axBW, np.median(nD1PopStat), 0, 0.5)
    pos = jitter(np.ones(len(D1PopStat))*1, 0.20)
    axBW.plot(pos, D1PopStat, 'o', mec = colorD1, mfc = 'None', alpha=markerAlpha)
    medline(axBW, np.median(D1PopStat), 1, 0.5)
    axBW.set_ylabel('BW10', fontsize=fontSizeLabels)

    # tickLabels = ['nD1:Str', 'D1:Str']
    tickLabels = ['nD1:Str\nn={}'.format(len(nD1PopStat)), 'D1:Str\nn={}'.format(len(D1PopStat))]
    axBW.set_xticks(range(2))
    axBW.set_xlim([-0.5, 1.5])
    extraplots.boxoff(axBW)
    extraplots.set_ticks_fontsize(axBW, fontSizeTicks)
    axBW.set_xticklabels(tickLabels, fontsize=fontSizeLabels, rotation=45)

    zstat, pVal = stats.mannwhitneyu(nD1PopStat, D1PopStat) #Nick used stats.ranksum

    messages.append("{} p={}".format(popStatCol, pVal))

    yDataMax = max([max(D1PopStat), max(nD1PopStat)])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor
    plt.sca(axBW)
    starString = None if pVal<0.05 else 'n.s.'
    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                  starSize=fontSizeStars+2, starString=starString,
                                  gapFactor=starGapFactor)
    plt.hold(1)
#
plt.hold(True)
if PANELS[8]:

    popStatCol = 'thresholdFRA'
    nD1PopStat = D1.query('{} == {}'.format(popStatCol,popStatCol))[popStatCol]
    nD1PopStat= nD1.query('{} == {}'.format(popStatCol,popStatCol))[popStatCol]

    plt.sca(axThresh)

    spacing = 0.05

    markers = extraplots.spread_plot(0, nD1PopStat, spacing)
    plt.setp(markers, mec = colornD1, mfc = 'None')
    medline(axThresh, np.median(nD1PopStat), 0, 0.5)

    markers = extraplots.spread_plot(1, D1PopStat, spacing)
    plt.setp(markers, mec = colorD1, mfc = 'None')

    medline(axThresh, np.median(D1PopStat), 1, 0.5)
    axThresh.set_ylabel('Threshold (dB SPL)', fontsize=fontSizeLabels)
    # tickLabels = ['nD1:Str', 'D1:Str']
    tickLabels = ['nD1:Str\nn={}'.format(len(nD1PopStat)), 'D1:Str\nn={}'.format(len(D1PopStat))]
    axThresh.set_xticks(range(2))
    axThresh.set_xlim([-0.5, 1.5])
    extraplots.boxoff(axThresh)
    extraplots.set_ticks_fontsize(axThresh, fontSizeTicks)

    axThresh.set_xticklabels(tickLabels, fontsize=fontSizeLabels, rotation=45)

    zstat, pVal = stats.mannwhitneyu(D1PopStat, nD1PopStat)#Nick used stats.ranksum

    messages.append("{} p={}".format(popStatCol, pVal))

    '''
    if pVal<0.05:
        starMarker='*'
    else:
        starMarker='n.s.'
    extraplots.new_significance_stars([0, 1], yStars, yStarHeight, starMarker=starMarker,
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=axThresh)
    '''
    yDataMax = max([max(nD1PopStat), max(D1PopStat)])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor
    starString = None if pVal<0.05 else 'n.s.'
    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                  starSize=fontSizeStars, starString=starString,
                                  gapFactor=starGapFactor)
    plt.hold(1)


if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
