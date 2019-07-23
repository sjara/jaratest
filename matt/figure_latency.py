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
reload(extraplots)
reload(figparams)

if sys.version_info[0] < 3:
    input_func = raw_input
elif sys.version_info[0] >= 3:
    input_func = input

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(ax, yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    ax.plot([start, end], [yval, yval], color=color, lw=linewidth)
#==========================parameters==========================================
FIGNAME = 'figure_frequency_tuning_test_latency'

d1mice = studyparams.ASTR_D1_CHR2_MICE
nameDB = '_'.join(d1mice) + '.h5'
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
# os.path.join(studyparams.PATH_TO_TEST,nameDB)
db = celldatabase.load_hdf(pathtoDB)
db = db.query('rsquaredFit>{}'.format(studyparams.R2_CUTOFF))
# exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')

#=======================================================================

# exData = np.load(exampleDataPath) This is never used in the code Santiago
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

# ======================= Beginning of plotting for latency ================================
if PANELS[8]:

    popStatCol = 'latency'
    D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
    nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]

    pos = jitter(np.ones(len(nD1PopStat))*0, 0.20)
    axLatency.plot(pos, nD1PopStat*1000, 'o', mec = colornD1, mfc = 'None', alpha=markerAlpha)
    medline(axLatency, np.median(nD1PopStat)*1000, 0, 0.5)
    pos = jitter(np.ones(len(D1PopStat))*1, 0.20)
    axLatency.plot(pos, D1PopStat*1000, 'o', mec = colorD1, mfc = 'None', alpha=markerAlpha)
    medline(axLatency, np.median(D1PopStat)*1000, 1, 0.5)
    axLatency.set_ylabel('Latency (ms)', fontsize=fontSizeTicks)
    # tickLabels = ['ATh:Str', 'AC:Str']
    tickLabels = ['nD1:Str\nn={}'.format(len(nD1PopStat)), 'D1:Str\nn={}'.format(len(D1PopStat))]
    axLatency.set_xticks(range(2))
    axLatency.set_xlim([-0.5, 1.5])
    extraplots.boxoff(axLatency)
    axLatency.set_ylim([-0.001, 65])

    extraplots.set_ticks_fontsize(axLatency, fontSizeTicks)
    axLatency.set_xticklabels(tickLabels, fontsize=fontSizeLabels, rotation=45)

    zstat, pVal = stats.ranksums(nD1PopStat, D1PopStat)

    # print "Ranksums test between thalamus and AC population stat ({}) vals: p={}".format(popStatCol, pVal) Remove Matt
    messages.append("{} p={}".format(popStatCol, pVal))

    '''
    if pVal<0.05:
        starMarker='*'
    else:
        starMarker='n.s.'
    extraplots.new_significance_stars([0, 1], yStars, yStarHeight, starMarker=starMarker,
                                        fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=axLatency)
    '''
    yDataMax = max([max(D1PopStat*2500), max(nD1PopStat*2500)])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor
    starString = None if pVal<0.05 else 'n.s.'
    plt.sca(axLatency)
    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                  starSize=fontSizeStars, starString=starString,
                                  gapFactor=starGapFactor)
    plt.hold(1)
plt.show()
