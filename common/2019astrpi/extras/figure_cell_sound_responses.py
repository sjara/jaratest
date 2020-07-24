"""
Generates a figures used to explore all aspects of sound responses for the
various stimuli we presented to the mice. Panels from here may or may not make
it into the final paper.
"""
import os
import sys
sys.path.append('..')
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

#%% Functions
def jitter(arr, frac):
    jitter_value = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter_value
    return jitteredArr


def medline(ax, yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    ax.plot([start, end], [yval, yval], color=color, lw=linewidth)


#%% Figure parameters
STRIATUM_ONLY = True

SAVE_FIGURE = 1
np.random.seed(1)
outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'sound_responses'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
figSize = [20, 18]

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
markerSpacing = 0.05

labelPosX = [0.02, 0.24, 0.45, 0.64, 0.835]   # Horiz position for panel labels
labelPosY = [0.92, 0.42]    # Vert position for panel labels

# Define colors, use figparams
laserColor = figparams.colp['blueLaser']
fig = plt.figure(figsize=figSize)
fig.set_facecolor('w')

# Define the layout
gs = gridspec.GridSpec(4, 8)
gs.update(left=0.04, right=0.98, top=0.95, bottom=0.05, wspace=.75, hspace=0.3)

axOne = plt.subplot(gs[0, 0])
axTwo = plt.subplot(gs[0, 1])
axThree = plt.subplot(gs[0, 2])
axFour = plt.subplot(gs[0, 3])
axFive = plt.subplot(gs[0, 4])
axSix = plt.subplot(gs[0, 5])
axSeven = plt.subplot(gs[0, 6])
axEight = plt.subplot(gs[0, 7])
axNine = plt.subplot(gs[1, 0])  # Noiseburst RI
axTen = plt.subplot(gs[1, 1])  # Pure tone RI
axEleven = plt.subplot(gs[1, 2])  # AM Onset RI
axTwelve = plt.subplot(gs[1, 3])  # AM Sustained RI
axThirteen = plt.subplot(gs[1, 4])  # Pure tone FR
axFourteen = plt.subplot(gs[1, 5])  # Pure tone FR limited y-axis
axFifteen = plt.subplot(gs[1, 6])  # Pure tone FR limited y-axis
axSixteen = plt.subplot(gs[1, 7])  # Tuned Cell FR
axSeventeen = plt.subplot(gs[2, 0])  # Noiseburst RI limited by FR
axEighteen = plt.subplot(gs[2, 1])  # Pure tone RI limited by FR
axNineteen = plt.subplot(gs[2, 2])  # AM Onset RI limited by FR
axTwenty = plt.subplot(gs[2, 3])  # AM Sustained RI limited by FR
axTwentyOne = plt.subplot(gs[2, 4])  # Tuned Cell Onset FR
axTwentyTwo = plt.subplot(gs[2, 5])  # Tuned Cell sustained FR
axTwentyThree = plt.subplot(gs[2, 6])  # AM Onset FR
axTwentyFour = plt.subplot(gs[2, 7])  # AM Sustained FR
axTwentyFive = plt.subplot(gs[3, 0])  # Noiseburst base
axTwentySix = plt.subplot(gs[3, 1])  # Base for Onset TC
axTwentySeven = plt.subplot(gs[3, 2])  # Base for Sustained TC
axTwentyEight = plt.subplot(gs[3, 3])  # Base for overall response TC
axTwentyNine = plt.subplot(gs[3, 4])  # Base for Onset AM
axThirty = plt.subplot(gs[3, 5])  # Base for Sustained AM

#%% Load in data
nameDB = studyparams.DATABASE_NAME + '.h5'
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
db = celldatabase.load_hdf(pathtoDB)
if STRIATUM_ONLY:
    db = db.query(studyparams.BRAIN_REGION_QUERY_STRIATUM_ONLY)
elif not STRIATUM_ONLY:
    pass
d1DB = db.query(studyparams.D1_CELLS)
nD1DB = db.query(studyparams.nD1_CELLS)
d1DB = d1DB.query(studyparams.FIRST_FLTRD_CELLS)
nD1DB = nD1DB.query(studyparams.FIRST_FLTRD_CELLS)

messages = []
#%% Sorting data and plotting
#FIXME: I realized that I can't plot any values for this since it is a comparison of multiple values.
# Percentage comparisons are still the best I could do so I am not plotting these for now.

# --------- sound repsonsive cells ------------
# D1DBResponse = d1DB.query("(noiseburst_pVal < 0.05 or tuning_pVal < 0.05 or am_response_pVal < 0.05)")
# nD1DBResponse = nD1DB.query("(noiseburst_pVal < 0.05 or tuning_pVal < 0.05 or am_response_pVal < 0.05)")
# D1DBNoResponse = d1DB.query("~(noiseburst_pVal < 0.05 or tuning_pVal < 0.05 or am_response_pVal < 0.05)")
# nD1DBNoResponse = nD1DB.query("~(noiseburst_pVal < 0.05 or tuning_pVal < 0.05 or am_response_pVal < 0.05)")
#
# plt.sca(axOne)
# markersD1Sound = extraplots.spread_plot(0, D1DBResponse, markerSpacing)
# markersD1NoSound = extraplots.spread_plot(1, D1DBNoResponse, markerSpacing)
#
# plt.sca(axTwo)
# markersnD1Sound = extraplots.spread_plot(0, nD1DBResponse, markerSpacing)
# markersnD1NoSound = extraplots.spread_plot(1, nD1DBNoResponse, markerSpacing)
#
# plt.show()

# ---------- noiseburst response ----------
D1Noise = d1DB.noiseburst_pVal[pd.notnull(d1DB.noiseburst_pVal)]
nD1Noise = nD1DB.noiseburst_pVal[pd.notnull(nD1DB.noiseburst_pVal)]
D1NoiseX = jitter(np.ones(len(D1Noise))*0, 0.20)
nD1NoiseX = jitter(np.ones(len(nD1Noise))*1, 0.20)

plt.sca(axOne)
axOne.plot(D1NoiseX, D1Noise, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axOne.plot(nD1NoiseX, nD1Noise, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axOne, np.median(D1Noise), 0, 0.5)
medline(axOne, np.median(nD1Noise), 1, 0.5)

axOne.set_xlim([-0.5, 1.5])
axOne.set_xticks(range(2))
axOne.set_xticklabels(["D1", "nD1"])
axOne.set_ylabel("p-value")
axOne.set_title("Noiseburst p-values")

# ---------- tuningCurve response p-value ----------
D1Pure = d1DB.tuning_pVal[pd.notnull(d1DB.tuning_pVal)]
nD1Pure = nD1DB.tuning_pVal[pd.notnull(nD1DB.tuning_pVal)]
D1PureX = jitter(np.ones(len(D1Pure))*0, 0.20)
nD1PureX = jitter(np.ones(len(nD1Pure))*1, 0.20)

plt.sca(axTwo)
axTwo.plot(D1PureX, D1Pure, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axTwo.plot(nD1PureX, nD1Pure, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axTwo, np.median(D1Pure), 0, 0.5)
medline(axTwo, np.median(nD1Pure), 1, 0.5)

axTwo.set_xlim([-0.5, 1.5])
axTwo.set_xticks(range(2))
axTwo.set_xticklabels(["D1", "nD1"])
axTwo.set_ylabel("p-value")
axTwo.set_title("Tuning Curve p-values")

# ---------- tuningCurve response Z-stat ----------
D1Z = d1DB.tuning_ZStat[pd.notnull(d1DB.tuning_ZStat)]
nD1Z = nD1DB.tuning_ZStat[pd.notnull(nD1DB.tuning_ZStat)]
D1ZX = jitter(np.ones(len(D1Z))*0, 0.20)
nD1ZX = jitter(np.ones(len(nD1Z))*1, 0.20)

plt.sca(axThree)
axThree.plot(D1ZX, D1Z, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axThree.plot(nD1ZX, nD1Z, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axThree, np.median(D1Z), 0, 0.5)
medline(axThree, np.median(nD1Z), 1, 0.5)

axThree.set_xlim([-0.5, 1.5])
axThree.set_xticks(range(2))
axThree.set_xticklabels(["D1", "nD1"])
axThree.set_ylabel("Z-Statistic")
axThree.set_title("Tuning Curve Z-values")

# ---------- tuningCurve response Z-stat (reduced y-axis) ----------
D1Z = d1DB.tuning_ZStat[pd.notnull(d1DB.tuning_ZStat)]
nD1Z = nD1DB.tuning_ZStat[pd.notnull(nD1DB.tuning_ZStat)]
D1ZX = jitter(np.ones(len(D1Z))*0, 0.20)
nD1ZX = jitter(np.ones(len(nD1Z))*1, 0.20)

plt.sca(axFour)
axFour.plot(D1ZX, D1Z, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axFour.plot(nD1ZX, nD1Z, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axFour, np.median(D1Z), 0, 0.5)
medline(axFour, np.median(nD1Z), 1, 0.5)

axFour.set_xlim([-0.5, 1.5])
axFour.set_ylim([0, 500])
axFour.set_xticks(range(2))
axFour.set_xticklabels(["D1", "nD1"])
axFour.set_ylabel("Z-Statistic")
axFour.set_title("Tuning Curve Z-values (limited y-axis)")

# ---------- tuningCurve R2 values ----------
# Assuming that all infinities that come up are from miscalculations, so changing them to NaNs so they can be excluded later
d1DB.rsquaredFit.replace([np.inf, -np.inf], np.nan, inplace=True)
nD1DB.rsquaredFit.replace([np.inf, -np.inf], np.nan, inplace=True)
D1DBPure = d1DB[d1DB.rsquaredFit.notnull()]
nD1DBPure = nD1DB[nD1DB.rsquaredFit.notnull()]
D1DBPure = D1DBPure.query("tuning_pVal < 0.05")
nD1DBPure = nD1DBPure.query("tuning_pVal < 0.05")
D1Tuned = D1DBPure.rsquaredFit
nD1Tuned = nD1DBPure.rsquaredFit
D1TunedX = jitter(np.ones(len(D1Tuned))*0, 0.20)
nD1TunedX = jitter(np.ones(len(nD1Tuned))*1, 0.20)

plt.sca(axFive)
axFive.plot(D1TunedX, D1Tuned, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axFive.plot(nD1TunedX, nD1Tuned, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axFive, np.median(D1Tuned), 0, 0.5)
medline(axFive, np.median(nD1Tuned), 1, 0.5)

axFive.set_xlim([-0.5, 1.5])
axFive.set_xticks(range(2))
axFive.set_xticklabels(["D1", "nD1"])
axFive.set_ylabel("R2 value")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1Tuned, nD1Tuned, alternative='two-sided')
messages.append("tc R2 = {}".format(pVals))
axFive.set_title("Tuning Curve R2 fit\np-value = {:.4}".format(pVals))

# ---------- AM Response p-values ----------
D1AMR = d1DB.am_response_pVal[pd.notnull(d1DB.am_response_pVal)]
nD1AMR = nD1DB.am_response_pVal[pd.notnull(nD1DB.am_response_pVal)]
D1AMRX = jitter(np.ones(len(D1AMR))*0, 0.20)
nD1AMRX = jitter(np.ones(len(nD1AMR))*1, 0.20)

plt.sca(axSix)
axSix.plot(D1AMRX, D1AMR, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axSix.plot(nD1AMRX, nD1AMR, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axSix, np.median(D1AMR), 0, 0.5)
medline(axSix, np.median(nD1AMR), 1, 0.5)

axSix.set_xlim([-0.5, 1.5])
axSix.set_xticks(range(2))
axSix.set_xticklabels(["D1", "nD1"])
axSix.set_ylabel("p-value")
axSix.set_title("AM Response p-values")

# ---------- AM Response Z-values ----------
D1AMRZ = d1DB.am_response_ZStat[pd.notnull(d1DB.am_response_ZStat)]
nD1AMRZ = nD1DB.am_response_ZStat[pd.notnull(nD1DB.am_response_ZStat)]
D1AMRZX = jitter(np.ones(len(D1AMRZ))*0, 0.20)
nD1AMRZX = jitter(np.ones(len(nD1AMRZ))*1, 0.20)

plt.sca(axSeven)
axSeven.plot(D1AMRZX, D1AMRZ, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axSeven.plot(nD1AMRZX, nD1AMRZ, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axSeven, np.median(D1AMRZ), 0, 0.5)
medline(axSeven, np.median(nD1AMRZ), 1, 0.5)

axSeven.set_xlim([-0.5, 1.5])
axSeven.set_xticks(range(2))
axSeven.set_xticklabels(["D1", "nD1"])
axSeven.set_ylabel("Z-statistic")
axSeven.set_title("AM Response Z-values")

# ---------- AM Sync p-values ----------
D1AMS = d1DB.am_synchronization_pVal[pd.notnull(d1DB.am_synchronization_pVal)]
nD1AMS = nD1DB.am_synchronization_pVal[pd.notnull(nD1DB.am_synchronization_pVal)]
D1AMSX = jitter(np.ones(len(D1AMS))*0, 0.20)
nD1AMSX = jitter(np.ones(len(nD1AMS))*1, 0.20)

plt.sca(axEight)
axEight.plot(D1AMSX, D1AMS, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axEight.plot(nD1AMSX, nD1AMS, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axEight, np.median(D1AMS), 0, 0.5)
medline(axEight, np.median(nD1AMS), 1, 0.5)

axEight.set_xlim([-0.5, 1.5])
axEight.set_xticks(range(2))
axEight.set_xticklabels(["D1", "nD1"])
axEight.set_ylabel("p-value")
axEight.set_title("AM Synchronization p-values")

# ############# RESPONSE INDEX PLOTS #################
# ----------- Noiseburst Response Index --------------
D1NoiseIndex = (d1DB.noiseburst_responseFR - d1DB.noiseburst_baselineFR) /\
               (d1DB.noiseburst_responseFR + d1DB.noiseburst_baselineFR)
nD1NoiseIndex = (nD1DB.noiseburst_responseFR - nD1DB.noiseburst_baselineFR) /\
                (nD1DB.noiseburst_responseFR + nD1DB.noiseburst_baselineFR)
# Dropping NaNs and then converting from a series to a list
D1NoiseIndex = D1NoiseIndex.dropna()
nD1NoiseIndex = nD1NoiseIndex.dropna()
D1NoiseIndex = D1NoiseIndex.to_list()
nD1NoiseIndex = nD1NoiseIndex.to_list()
D1NoiseIndexX = jitter(np.ones(len(D1NoiseIndex))*0, 0.20)
nD1NoiseIndexX = jitter(np.ones(len(nD1NoiseIndex))*1, 0.20)

plt.sca(axNine)
axNine.plot(D1NoiseIndexX, D1NoiseIndex, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axNine.plot(nD1NoiseIndexX, nD1NoiseIndex, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axNine, np.median(D1NoiseIndex), 0, 0.5)
medline(axNine, np.median(nD1NoiseIndex), 1, 0.5)

axNine.set_xticks(range(2))
axNine.set_xticklabels(["D1", "nD1"])
axNine.set_ylabel("RI")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1NoiseIndex, nD1NoiseIndex, alternative='two-sided')
messages.append("Whitenoise index = {}".format(pVals))
axNine.set_title("Noiseburst Response Index\n\u00B1[0.0 s, 0.1 s]\np-value = {:.4}".format(pVals))

# ---------- Pure Tone Response Index --------------
D1PureToneIndex = (d1DB.tuningRespFRBestFreqMaxInt - d1DB.tuningBaseFRBestFreqMaxInt) /\
                  (d1DB.tuningRespFRBestFreqMaxInt + d1DB.tuningBaseFRBestFreqMaxInt)
nD1PureToneIndex = (nD1DB.tuningRespFRBestFreqMaxInt - nD1DB.tuningBaseFRBestFreqMaxInt) /\
                   (nD1DB.tuningRespFRBestFreqMaxInt + nD1DB.tuningBaseFRBestFreqMaxInt)

# Dropping NaNs and then converting from a series to a list
D1PureToneIndex = D1PureToneIndex.dropna()
nD1PureToneIndex = nD1PureToneIndex.dropna()
D1PureToneIndex = D1PureToneIndex.to_list()
nD1PureToneIndex = nD1PureToneIndex.to_list()
D1PureToneIndexX = jitter(np.ones(len(D1PureToneIndex))*0, 0.20)
nD1PureToneIndexX = jitter(np.ones(len(nD1PureToneIndex))*1, 0.20)

plt.sca(axTen)
axTen.plot(D1PureToneIndexX, D1PureToneIndex, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axTen.plot(nD1PureToneIndexX, nD1PureToneIndex, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axTen, np.median(D1PureToneIndex), 0, 0.5)
medline(axTen, np.median(nD1PureToneIndex), 1, 0.5)

axTen.set_xticks(range(2))
axTen.set_xticklabels(["D1", "nD1"])
axTen.set_ylabel("RI")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1PureToneIndex, nD1PureToneIndex, alternative='two-sided')
messages.append("Pure tone index = {}".format(pVals))
axTen.set_title("Pure Tone Response Index\n\u00B1[0.0 s, 0.1 s]\np-value = {:.4}".format(pVals))

# ---------- Onset Response Index --------------
D1OnsetIndex = (d1DB.AMRespFROnset - d1DB.AMBaseFROnset) /\
              (d1DB.AMRespFROnset + d1DB.AMBaseFROnset)
nD1OnsetIndex = (nD1DB.AMRespFROnset - nD1DB.AMBaseFROnset) /\
               (nD1DB.AMRespFROnset + nD1DB.AMBaseFROnset)

# Dropping NaNs and then converting from a series to a list
D1OnsetIndex = D1OnsetIndex.dropna()
nD1OnsetIndex = nD1OnsetIndex.dropna()
D1OnsetIndex = D1OnsetIndex.to_list()
nD1OnsetIndex = nD1OnsetIndex.to_list()
D1OnsetIndexX = jitter(np.ones(len(D1OnsetIndex))*0, 0.20)
nD1OnsetIndexX = jitter(np.ones(len(nD1OnsetIndex))*1, 0.20)

plt.sca(axEleven)
axEleven.plot(D1OnsetIndexX, D1OnsetIndex, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axEleven.plot(nD1OnsetIndexX, nD1OnsetIndex, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axEleven, np.median(D1OnsetIndex), 0, 0.5)
medline(axEleven, np.median(nD1OnsetIndex), 1, 0.5)

axEleven.set_xticks(range(2))
axEleven.set_xticklabels(["D1", "nD1"])
axEleven.set_ylabel("RI")


# Statistics
zStats, pVals = stats.mannwhitneyu(D1OnsetIndex, nD1OnsetIndex, alternative='two-sided')
messages.append("AM onset index = {}".format(pVals))
axEleven.set_title("AM Onset Response Index\n\u00B1[0.0 s, 0.1 s]\np-value = {:.4}".format(pVals))

# ---------- Sustained Response Index --------------
D1SustainedIndex = (d1DB.AMRespFRSustained - d1DB.AMBaseFRSustained) /\
                   (d1DB.AMRespFRSustained + d1DB.AMBaseFRSustained)
nD1SustainedIndex = (nD1DB.AMRespFRSustained - nD1DB.AMBaseFRSustained) /\
                    (nD1DB.AMRespFRSustained + nD1DB.AMBaseFRSustained)

# Dropping NaNs and then converting from a series to a list
D1SustainedIndex = D1SustainedIndex.dropna()
nD1SustainedIndex = nD1SustainedIndex.dropna()
D1SustainedIndex = D1SustainedIndex.to_list()
nD1SustainedIndex = nD1SustainedIndex.to_list()
D1SustainedIndexX = jitter(np.ones(len(D1SustainedIndex))*0, 0.20)
nD1SustainedIndexX = jitter(np.ones(len(nD1SustainedIndex))*1, 0.20)

plt.sca(axTwelve)
axTwelve.plot(D1SustainedIndexX, D1SustainedIndex, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axTwelve.plot(nD1SustainedIndexX, nD1SustainedIndex, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axTwelve, np.median(D1SustainedIndex), 0, 0.5)
medline(axTwelve, np.median(nD1SustainedIndex), 1, 0.5)

axTwelve.set_xticks(range(2))
axTwelve.set_xticklabels(["D1", "nD1"])
axTwelve.set_ylabel("RI")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1SustainedIndex, nD1SustainedIndex, alternative='two-sided')
messages.append("AM sustained index = {}".format(pVals))
axTwelve.set_title("AM Sustained Response Index\n\u00B1[0.1 s, 0.5 s]\np-value = {:.4}".format(pVals))

# ------------ Pure Tone Firing Rate -------------
D1PureToneFR = d1DB.tuningRespFRBestFreqMaxInt.dropna().to_list()
nD1PureToneFR = nD1DB.tuningRespFRBestFreqMaxInt.dropna().to_list()
D1PureToneFRX = jitter(np.ones(len(D1PureToneFR))*0, 0.20)
nD1PureToneFRX = jitter(np.ones(len(nD1PureToneFR))*1, 0.20)

plt.sca(axThirteen)
axThirteen.plot(D1PureToneFRX, D1PureToneFR, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axThirteen.plot(nD1PureToneFRX, nD1PureToneFR, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axThirteen, np.median(D1PureToneFR), 0, 0.5)
medline(axThirteen, np.median(nD1PureToneFR), 1, 0.5)

axThirteen.set_xticks(range(2))
axThirteen.set_xticklabels(["D1", "nD1"])
axThirteen.set_ylabel("Mean FR (spks/s)")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1PureToneFR, nD1PureToneFR, alternative='two-sided')
messages.append("Pure tone firing rates = {}".format(pVals))
axThirteen.set_title("Pure Tone Firing Rates\n[0.0 s, 0.1 s]\np-value = {:.4}".format(pVals))

# ------------ Pure Tone Firing Rate (limited y-axis) -------------
D1PureToneFR = d1DB.tuningRespFRBestFreqMaxInt.dropna().to_list()
nD1PureToneFR = nD1DB.tuningRespFRBestFreqMaxInt.dropna().to_list()
D1PureToneFRX = jitter(np.ones(len(D1PureToneFR))*0, 0.20)
nD1PureToneFRX = jitter(np.ones(len(nD1PureToneFR))*1, 0.20)

plt.sca(axFourteen)
axFourteen.plot(D1PureToneFRX, D1PureToneFR, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axFourteen.plot(nD1PureToneFRX, nD1PureToneFR, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axFourteen, np.median(D1PureToneFR), 0, 0.5)
medline(axFourteen, np.median(nD1PureToneFR), 1, 0.5)

axFourteen.set_xticks(range(2))
axFourteen.set_xticklabels(["D1", "nD1"])
axFourteen.set_ylabel("Mean FR (spks/s)")
axFourteen.set_ylim([0, 5])
axFourteen.set_title("Pure Tone Firing Rates\n[0.0 s, 0.1 s]\nLimited y-axis")

# ------------ Pure Tone Firing Rate (even more restricted axis) -------------
D1PureToneFR = d1DB.tuningRespFRBestFreqMaxInt.dropna().to_list()
nD1PureToneFR = nD1DB.tuningRespFRBestFreqMaxInt.dropna().to_list()
D1PureToneFRX = jitter(np.ones(len(D1PureToneFR))*0, 0.20)
nD1PureToneFRX = jitter(np.ones(len(nD1PureToneFR))*1, 0.20)

plt.sca(axFifteen)
axFifteen.plot(D1PureToneFRX, D1PureToneFR, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axFifteen.plot(nD1PureToneFRX, nD1PureToneFR, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axFifteen, np.median(D1PureToneFR), 0, 0.5)
medline(axFifteen, np.median(nD1PureToneFR), 1, 0.5)

axFifteen.set_xticks(range(2))
axFifteen.set_xticklabels(["D1", "nD1"])
axFifteen.set_ylabel("Mean FR (spks/s)")
axFifteen.set_ylim([0, 1])
axFifteen.set_title("Pure Tone Firing Rates\n[0.0 s, 0.1 s]\nLimited y-axis")

# ------------ Tuned Cell Firing Rate -------------
D1DBTuned = d1DB.query(studyparams.TUNING_FILTER)
nD1DBTuned = nD1DB.query(studyparams.TUNING_FILTER)
D1TunedFR = D1DBTuned.tuningRespFRBestFreqMaxInt.dropna().to_list()
nD1TunedFR = nD1DBTuned.tuningRespFRBestFreqMaxInt.dropna().to_list()
D1TunedFRX = jitter(np.ones(len(D1TunedFR))*0, 0.20)
nD1TunedFRX = jitter(np.ones(len(nD1TunedFR))*1, 0.20)

plt.sca(axSixteen)
axSixteen.plot(D1TunedFRX, D1TunedFR, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axSixteen.plot(nD1TunedFRX, nD1TunedFR, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axSixteen, np.median(D1TunedFR), 0, 0.5)
medline(axSixteen, np.median(nD1TunedFR), 1, 0.5)

axSixteen.set_xticks(range(2))
axSixteen.set_xticklabels(["D1", "nD1"])
axSixteen.set_ylabel("Mean FR (spks/s)")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1TunedFR, nD1TunedFR, alternative='two-sided')
messages.append("Tuned cell FR = {}".format(pVals))
axSixteen.set_title("Tuned Cell Firing Rates\n[0.0 s, 0.1 s]\np-value = {:.4}".format(pVals))

# ############# MORE FIRING RATE PLOTS ###############
# ------------- Onset FR for pure tones --------------
# For plotting only tuned cells
D1DBTuned = d1DB.query(studyparams.TUNING_FILTER)
nD1DBTuned = nD1DB.query(studyparams.TUNING_FILTER)
D1OnsetFR = D1DBTuned.tuningRespOnsetFRBestFreqMaxInt.dropna().to_list()
nD1OnsetFR = nD1DBTuned.tuningRespOnsetFRBestFreqMaxInt.dropna().to_list()

# For plotting all pure tone responses, not just tuned cells
# D1OnsetFR = d1DB.tuningRespOnsetFRBestFreqMaxInt.dropna().to_list()
# nD1OnsetFR = nD1DB.tuningRespOnsetFRBestFreqMaxInt.dropna().to_list()

D1OnsetFRX = jitter(np.ones(len(D1OnsetFR))*0, 0.20)
nD1OnsetFRX = jitter(np.ones(len(nD1OnsetFR))*1, 0.20)

plt.sca(axTwentyOne)
axTwentyOne.plot(D1OnsetFRX, D1OnsetFR, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axTwentyOne.plot(nD1OnsetFRX, nD1OnsetFR, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axTwentyOne, np.median(D1OnsetFR), 0, 0.5)
medline(axTwentyOne, np.median(nD1OnsetFR), 1, 0.5)

axTwentyOne.set_xticks(range(2))
axTwentyOne.set_xticklabels(["D1", "nD1"])
axTwentyOne.set_ylabel("Mean FR (spks/s)")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1OnsetFR, nD1OnsetFR, alternative='two-sided')
messages.append("Pure tone onset FR = {}".format(pVals))
axTwentyOne.set_title("TC\nOnset Firing Rates \n[0 s, 0.05 s]\np-value = {:.4}".format(pVals))

# ------------- Sustained FR for pure tones --------------
# For plotting only tuned cells
D1DBTuned = d1DB.query(studyparams.TUNING_FILTER)
nD1DBTuned = nD1DB.query(studyparams.TUNING_FILTER)
D1SustainedFR = D1DBTuned.tuningRespSustainedFRBestFreqMaxInt.dropna().to_list()
nD1SustainedFR = nD1DBTuned.tuningRespSustainedFRBestFreqMaxInt.dropna().to_list()

# For plotting all pure tone responses, not just tuned cells
# D1SustainedFR = d1DB.tuningRespSustainedFRBestFreqMaxInt.dropna().to_list()
# nD1SustainedFR = nD1DB.tuningRespSustainedFRBestFreqMaxInt.dropna().to_list()

D1SustainedFRX = jitter(np.ones(len(D1SustainedFR))*0, 0.20)
nD1SustainedFRX = jitter(np.ones(len(nD1SustainedFR))*1, 0.20)

plt.sca(axTwentyTwo)
axTwentyTwo.plot(D1SustainedFRX, D1SustainedFR, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axTwentyTwo.plot(nD1SustainedFRX, nD1SustainedFR, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axTwentyTwo, np.median(D1SustainedFR), 0, 0.5)
medline(axTwentyTwo, np.median(nD1SustainedFR), 1, 0.5)

axTwentyTwo.set_xticks(range(2))
axTwentyTwo.set_xticklabels(["D1", "nD1"])
axTwentyTwo.set_ylabel("Mean FR (spks/s)")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1SustainedFR, nD1SustainedFR, alternative='two-sided')
messages.append("Pure tone sustained FR = {}".format(pVals))
axTwentyTwo.set_title("TC\nSustained Firing Rates\n[0.05 s, 0.1 s]\np-value = {:.4}".format(pVals))


# ----------- Onset FR for AM ------------------
# Only AM responsive cells
d1DBAMResp = d1DB.query(studyparams.AM_FILTER)
nD1DBAMResp = nD1DB.query(studyparams.AM_FILTER)
D1DBAMOnset = d1DBAMResp.AMRespFROnset.dropna().to_list()
nD1DBAMOnset = nD1DBAMResp.AMRespFROnset.dropna().to_list()

# All cells AM data was collected for
# D1DBAMOnset = d1DB.AMRespFROnset.dropna().to_list()
# nD1DBAMOnset = nD1DB.AMRespFROnset.dropna().to_list()

D1DBAMOnsetX = jitter(np.ones(len(D1DBAMOnset))*0, 0.20)
nD1DBAMOnsetX = jitter(np.ones(len(nD1DBAMOnset))*1, 0.20)

plt.sca(axTwentyThree)
axTwentyThree.plot(D1DBAMOnsetX, D1DBAMOnset, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axTwentyThree.plot(nD1DBAMOnsetX, nD1DBAMOnset, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axTwentyThree, np.median(D1DBAMOnset), 0, 0.5)
medline(axTwentyThree, np.median(nD1DBAMOnset), 1, 0.5)

axTwentyThree.set_xticks(range(2))
axTwentyThree.set_xticklabels(["D1", "nD1"])
axTwentyThree.set_ylabel("Mean FR (spks/s)")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1DBAMOnset, nD1DBAMOnset, alternative='two-sided')
messages.append("AM Onset FR = {}".format(pVals))
axTwentyThree.set_title("AM\nOnset Firing Rates \n[0 s, 0.1 s]\np-value = {:.4}".format(pVals))

# ----------- Sustained FR for AM ------------------
# Only AM responsive cells
d1DBAMResp = d1DB.query(studyparams.AM_FILTER)
nD1DBAMResp = nD1DB.query(studyparams.AM_FILTER)
D1DBAMSustained = d1DBAMResp.AMRespFRSustained.dropna().to_list()
nD1DBAMSustained = nD1DBAMResp.AMRespFRSustained.dropna().to_list()

# All cells AM data was collected for
# D1DBAMSustained = d1DB.AMRespFRSustained.dropna().to_list()
# nD1DBAMSustained = nD1DB.AMRespFRSustained.dropna().to_list()

D1DBAMSustainedX = jitter(np.ones(len(D1DBAMSustained))*0, 0.20)
nD1DBAMSustainedX = jitter(np.ones(len(nD1DBAMSustained))*1, 0.20)

plt.sca(axTwentyFour)
axTwentyFour.plot(D1DBAMSustainedX, D1DBAMSustained, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axTwentyFour.plot(nD1DBAMSustainedX, nD1DBAMSustained, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axTwentyFour, np.median(D1DBAMSustained), 0, 0.5)
medline(axTwentyFour, np.median(nD1DBAMSustained), 1, 0.5)

axTwentyFour.set_xticks(range(2))
axTwentyFour.set_xticklabels(["D1", "nD1"])
axTwentyFour.set_ylabel("Mean FR (spks/s)")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1DBAMSustained, nD1DBAMSustained, alternative='two-sided')
messages.append("AM Sustained FR = {}".format(pVals))
axTwentyFour.set_title("AM\nSustained Firing Rates \n[0.1 s, 0.5 s]\np-value = {:.4}".format(pVals))

# ------------- Response indices selected by FR thresholds -------------
# ------------ Pure tones ----------
# Filtering by some arbitrary FR
FRThreshold = 5
D1DBPureToneLimited = d1DB.query("(tuningOnsetRate > {0} or tuningSustainedRate > {0} or tuningBaseRate > {0})".format(FRThreshold))
nD1DBPureToneLimited = nD1DB.query("(tuningOnsetRate > {0} or tuningSustainedRate > {0} or tuningBaseRate > {0})".format(FRThreshold))

# Index calculation
D1PureToneIndexFiltered = (D1DBPureToneLimited.tuningRespFRBestFreqMaxInt - D1DBPureToneLimited.tuningBaseFRBestFreqMaxInt) / \
                          (D1DBPureToneLimited.tuningRespFRBestFreqMaxInt + D1DBPureToneLimited.tuningBaseFRBestFreqMaxInt)
nD1PureToneIndexFiltered = (nD1DBPureToneLimited.tuningRespFRBestFreqMaxInt - nD1DBPureToneLimited.tuningBaseFRBestFreqMaxInt) / \
                           (nD1DBPureToneLimited.tuningRespFRBestFreqMaxInt + nD1DBPureToneLimited.tuningBaseFRBestFreqMaxInt)

# Dropping NaNs and converting from a series to a list
D1PureToneIndexFiltered = D1PureToneIndexFiltered.dropna()
nD1PureToneIndexFiltered = nD1PureToneIndexFiltered.dropna()
D1PureToneIndexFiltered = D1PureToneIndexFiltered.to_list()
nD1PureToneIndexFiltered = nD1PureToneIndexFiltered.to_list()

# Generating x-coords
D1PureToneIndexFilteredX = jitter(np.ones(len(D1PureToneIndexFiltered))*0, 0.20)
nD1PureToneIndexFilteredX = jitter(np.ones(len(nD1PureToneIndexFiltered))*1, 0.20)

plt.sca(axEighteen)
axEighteen.plot(D1PureToneIndexFilteredX, D1PureToneIndexFiltered, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axEighteen.plot(nD1PureToneIndexFilteredX, nD1PureToneIndexFiltered, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axEighteen, np.median(D1PureToneIndexFiltered), 0, 0.5)
medline(axEighteen, np.median(nD1PureToneIndexFiltered), 1, 0.5)

axEighteen.set_xticks(range(2))
axEighteen.set_xticklabels(["D1", "nD1"])
axEighteen.set_ylabel("Response Index (spks/s)")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1PureToneIndexFiltered, nD1PureToneIndexFiltered, alternative='two-sided')
messages.append("Pure Tone RI limited by FR = {}".format(pVals))
axEighteen.set_title("Response Index pure tones\nLimited by FR > {0}\np-value = {1:.4}".format(FRThreshold, pVals))

# ------------- AM Onset --------------
FRThreshold = 2
D1DBAMOnsetLimited = d1DB.query("(AMBaseFROnset > {0} or AMRespFROnset > {0})".format(FRThreshold))
nD1DBAMOnsetLimited = nD1DB.query("(AMBaseFROnset > {0} or AMRespFROnset > {0})".format(FRThreshold))

D1OnsetIndexFiltered = (D1DBAMOnsetLimited.AMRespFROnset - D1DBAMOnsetLimited.AMBaseFROnset) /\
              (D1DBAMOnsetLimited.AMRespFROnset + D1DBAMOnsetLimited.AMBaseFROnset)
nD1OnsetIndexFiltered = (nD1DBAMOnsetLimited.AMRespFROnset - nD1DBAMOnsetLimited.AMBaseFROnset) /\
               (nD1DBAMOnsetLimited.AMRespFROnset + nD1DBAMOnsetLimited.AMBaseFROnset)

# Dropping NaNs and then converting from a series to a list
D1OnsetIndexFiltered = D1OnsetIndexFiltered.dropna()
nD1OnsetIndexFiltered = nD1OnsetIndexFiltered.dropna()
D1OnsetIndexFiltered = D1OnsetIndexFiltered.to_list()
nD1OnsetIndexFiltered = nD1OnsetIndexFiltered.to_list()
D1OnsetIndexFilteredX = jitter(np.ones(len(D1OnsetIndexFiltered))*0, 0.20)
nD1OnsetIndexFilteredX = jitter(np.ones(len(nD1OnsetIndexFiltered))*1, 0.20)

plt.sca(axNineteen)
axNineteen.plot(D1OnsetIndexFilteredX, D1OnsetIndexFiltered, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axNineteen.plot(nD1OnsetIndexFilteredX, nD1OnsetIndexFiltered, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axNineteen, np.median(D1OnsetIndexFiltered), 0, 0.5)
medline(axNineteen, np.median(nD1OnsetIndexFiltered), 1, 0.5)

axNineteen.set_xticks(range(2))
axNineteen.set_xticklabels(["D1", "nD1"])
axNineteen.set_ylabel("RI")


# Statistics
zStats, pVals = stats.mannwhitneyu(D1OnsetIndexFiltered, nD1OnsetIndexFiltered, alternative='two-sided')
messages.append("AM onset index = {}".format(pVals))
axNineteen.set_title("AM Onset Response Index\nLimited by FR > {0}\np-value = {1:.4}".format(FRThreshold, pVals))

# ------------- AM Sustained --------------
FRThreshold = 2
D1DBAMSustainedLimited = d1DB.query("(AMBaseFRSustained > {0} or AMRespFRSustained > {0})".format(FRThreshold))
nD1DBAMSustainedLimited = nD1DB.query("(AMBaseFRSustained > {0} or AMRespFRSustained > {0})".format(FRThreshold))

D1SustainedIndexFiltered = (D1DBAMSustainedLimited.AMRespFRSustained - D1DBAMSustainedLimited.AMBaseFRSustained) /\
              (D1DBAMSustainedLimited.AMRespFRSustained + D1DBAMSustainedLimited.AMBaseFRSustained)
nD1SustainedIndexFiltered = (nD1DBAMSustainedLimited.AMRespFRSustained - nD1DBAMSustainedLimited.AMBaseFRSustained) /\
               (nD1DBAMSustainedLimited.AMRespFRSustained + nD1DBAMSustainedLimited.AMBaseFRSustained)

# Dropping NaNs and then converting from a series to a list
D1SustainedIndexFiltered = D1SustainedIndexFiltered.dropna()
nD1SustainedIndexFiltered = nD1SustainedIndexFiltered.dropna()
D1SustainedIndexFiltered = D1SustainedIndexFiltered.to_list()
nD1SustainedIndexFiltered = nD1SustainedIndexFiltered.to_list()
D1SustainedIndexFilteredX = jitter(np.ones(len(D1SustainedIndexFiltered))*0, 0.20)
nD1SustainedIndexFilteredX = jitter(np.ones(len(nD1SustainedIndexFiltered))*1, 0.20)

plt.sca(axTwenty)
axTwenty.plot(D1SustainedIndexFilteredX, D1SustainedIndexFiltered, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axTwenty.plot(nD1SustainedIndexFilteredX, nD1SustainedIndexFiltered, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axTwenty, np.median(D1SustainedIndexFiltered), 0, 0.5)
medline(axTwenty, np.median(nD1SustainedIndexFiltered), 1, 0.5)

axTwenty.set_xticks(range(2))
axTwenty.set_xticklabels(["D1", "nD1"])
axTwenty.set_ylabel("RI")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1SustainedIndexFiltered, nD1SustainedIndexFiltered, alternative='two-sided')
messages.append("AM sustained index = {}".format(pVals))
axTwenty.set_title("AM Sustained Response Index\nLimited by FR > {0}\np-value = {1:.4}".format(FRThreshold, pVals))

# ---------- Noiseburst Response Index -----------
FRThreshold = 3
D1DBNoiseburstLimited = d1DB.query("(noiseburst_baselineFR > {0} or noiseburst_responseFR > {0})".format(FRThreshold))
nD1DBNoiseburstLimited = nD1DB.query("(noiseburst_baselineFR > {0} or noiseburst_responseFR > {0})".format(FRThreshold))

D1NoiseFilteredIndex = (D1DBNoiseburstLimited.noiseburst_responseFR - D1DBNoiseburstLimited.noiseburst_baselineFR) /\
               (D1DBNoiseburstLimited.noiseburst_responseFR + D1DBNoiseburstLimited.noiseburst_baselineFR)
nD1NoiseFilteredIndex = (nD1DBNoiseburstLimited.noiseburst_responseFR - nD1DBNoiseburstLimited.noiseburst_baselineFR) /\
                (nD1DBNoiseburstLimited.noiseburst_responseFR + nD1DBNoiseburstLimited.noiseburst_baselineFR)
# Dropping NaNs and then converting from a series to a list
D1NoiseFilteredIndex = D1NoiseFilteredIndex.dropna()
nD1NoiseFilteredIndex = nD1NoiseFilteredIndex.dropna()
D1NoiseFilteredIndex = D1NoiseFilteredIndex.to_list()
nD1NoiseFilteredIndex = nD1NoiseFilteredIndex.to_list()
D1NoiseFilteredIndexX = jitter(np.ones(len(D1NoiseFilteredIndex))*0, 0.20)
nD1NoiseFilteredIndexX = jitter(np.ones(len(nD1NoiseFilteredIndex))*1, 0.20)

plt.sca(axSeventeen)
axSeventeen.plot(D1NoiseFilteredIndexX, D1NoiseFilteredIndex, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axSeventeen.plot(nD1NoiseFilteredIndexX, nD1NoiseFilteredIndex, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axSeventeen, np.median(D1NoiseFilteredIndex), 0, 0.5)
medline(axSeventeen, np.median(nD1NoiseFilteredIndex), 1, 0.5)

axSeventeen.set_xticks(range(2))
axSeventeen.set_xticklabels(["D1", "nD1"])
axSeventeen.set_ylabel("RI")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1NoiseFilteredIndex, nD1NoiseFilteredIndex, alternative='two-sided')
messages.append("Whitenoise index = {}".format(pVals))
axSeventeen.set_title("Noiseburst Response Index\nLimited by FR > {0}\np-value = {1:.4}".format(FRThreshold, pVals))

# ------------------- Baseline Firing Rate plots ------------------
# ----- Noiseburst baseline FR -------
D1NoiseBaseFR = d1DB.noiseburst_baselineFR.dropna().to_list()
nD1NoiseBaseFR = nD1DB.noiseburst_baselineFR.dropna().to_list()
D1NoiseBaseFRX = jitter(np.ones(len(D1NoiseBaseFR))*0, 0.20)
nD1NoiseBaseFRX = jitter(np.ones(len(nD1NoiseBaseFR))*1, 0.20)

plt.sca(axTwentyFive)
axTwentyFive.plot(D1NoiseBaseFRX, D1NoiseBaseFR, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axTwentyFive.plot(nD1NoiseBaseFRX, nD1NoiseBaseFR, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axTwentyFive, np.median(D1NoiseBaseFR), 0, 0.5)
medline(axTwentyFive, np.median(nD1NoiseBaseFR), 1, 0.5)

axTwentyFive.set_xticks(range(2))
axTwentyFive.set_xticklabels(["D1", "nD1"])
axTwentyFive.set_ylabel("Mean FR (spks/s)")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1NoiseBaseFR, nD1NoiseBaseFR, alternative='two-sided')
messages.append("Noiseburst baseline p-value = {}".format(pVals))
axTwentyFive.set_title("Noiseburst baseline FR\n[-0.1 s, 0.0 s]\np-value = {0:.4}".format(pVals))

# ----- Pure tone Onset baseline FR -------
D1PureToneOnsetBaseFR = d1DB.tuningBaseOnsetFRBestFreqMaxInt.dropna().to_list()
nD1PureToneOnsetBaseFR = nD1DB.tuningBaseOnsetFRBestFreqMaxInt.dropna().to_list()
D1PureToneOnsetBaseFRX = jitter(np.ones(len(D1PureToneOnsetBaseFR))*0, 0.20)
nD1PureToneOnsetBaseFRX = jitter(np.ones(len(nD1PureToneOnsetBaseFR))*1, 0.20)

plt.sca(axTwentySix)
axTwentySix.plot(D1PureToneOnsetBaseFRX, D1PureToneOnsetBaseFR, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axTwentySix.plot(nD1PureToneOnsetBaseFRX, nD1PureToneOnsetBaseFR, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axTwentySix, np.median(D1PureToneOnsetBaseFR), 0, 0.5)
medline(axTwentySix, np.median(nD1PureToneOnsetBaseFR), 1, 0.5)

axTwentySix.set_xticks(range(2))
axTwentySix.set_xticklabels(["D1", "nD1"])
axTwentySix.set_ylabel("Mean FR (spks/s)")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1PureToneOnsetBaseFR, nD1PureToneOnsetBaseFR, alternative='two-sided')
messages.append("Pure tone onset baseline p-value = {}".format(pVals))
axTwentySix.set_title("PT Onset baseline FR\n[-0.05 s, 0.0 s]\np-value = {0:.4}".format(pVals))

# ----- Pure tone Sustained baseline FR -------
D1PureToneSustainedBaseFR = d1DB.tuningBaseSustainedFRBestFreqMaxInt.dropna().to_list()
nD1PureToneSustainedBaseFR = nD1DB.tuningBaseSustainedFRBestFreqMaxInt.dropna().to_list()
D1PureToneSustainedBaseFRX = jitter(np.ones(len(D1PureToneSustainedBaseFR))*0, 0.20)
nD1PureToneSustainedBaseFRX = jitter(np.ones(len(nD1PureToneSustainedBaseFR))*1, 0.20)

plt.sca(axTwentySeven)
axTwentySeven.plot(D1PureToneSustainedBaseFRX, D1PureToneSustainedBaseFR, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axTwentySeven.plot(nD1PureToneSustainedBaseFRX, nD1PureToneSustainedBaseFR, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axTwentySeven, np.median(D1PureToneSustainedBaseFR), 0, 0.5)
medline(axTwentySeven, np.median(nD1PureToneSustainedBaseFR), 1, 0.5)

axTwentySeven.set_xticks(range(2))
axTwentySeven.set_xticklabels(["D1", "nD1"])
axTwentySeven.set_ylabel("Mean FR (spks/s)")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1PureToneSustainedBaseFR, nD1PureToneSustainedBaseFR, alternative='two-sided')
messages.append("Pure tone sustained baseline p-value = {}".format(pVals))
axTwentySeven.set_title("PT Sustained baseline FR\n[-0.1 s, -0.05 s]\np-value = {0:.4}".format(pVals))

# ----- Pure tone baseline FR -------
D1PureToneBaseFR = d1DB.tuningBaseFRBestFreqMaxInt.dropna().to_list()
nD1PureToneBaseFR = nD1DB.tuningBaseFRBestFreqMaxInt.dropna().to_list()
D1PureToneBaseFRX = jitter(np.ones(len(D1PureToneBaseFR))*0, 0.20)
nD1PureToneBaseFRX = jitter(np.ones(len(nD1PureToneBaseFR))*1, 0.20)

plt.sca(axTwentyEight)
axTwentyEight.plot(D1PureToneBaseFRX, D1PureToneBaseFR, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axTwentyEight.plot(nD1PureToneBaseFRX, nD1PureToneBaseFR, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axTwentyEight, np.median(D1PureToneBaseFR), 0, 0.5)
medline(axTwentyEight, np.median(nD1PureToneBaseFR), 1, 0.5)

axTwentyEight.set_xticks(range(2))
axTwentyEight.set_xticklabels(["D1", "nD1"])
axTwentyEight.set_ylabel("Mean FR (spks/s)")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1PureToneBaseFR, nD1PureToneBaseFR, alternative='two-sided')
messages.append("Pure tone baseline p-value = {}".format(pVals))
axTwentyEight.set_title("PT baseline FR at max int\n[-0.1 s, 0.0 s]\np-value = {0:.4}".format(pVals))

# ----- AM Onset baseline FR -------
D1AMOnsetBaseFR = d1DB.AMBaseFROnset.dropna().to_list()
nD1AMOnsetBaseFR = nD1DB.AMBaseFROnset.dropna().to_list()
D1AMOnsetBaseFRX = jitter(np.ones(len(D1AMOnsetBaseFR))*0, 0.20)
nD1AMOnsetBaseFRX = jitter(np.ones(len(nD1AMOnsetBaseFR))*1, 0.20)

plt.sca(axTwentyNine)
axTwentyNine.plot(D1AMOnsetBaseFRX, D1AMOnsetBaseFR, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axTwentyNine.plot(nD1AMOnsetBaseFRX, nD1AMOnsetBaseFR, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axTwentyNine, np.median(D1AMOnsetBaseFR), 0, 0.5)
medline(axTwentyNine, np.median(nD1AMOnsetBaseFR), 1, 0.5)

axTwentyNine.set_xticks(range(2))
axTwentyNine.set_xticklabels(["D1", "nD1"])
axTwentyNine.set_ylabel("Mean FR (spks/s)")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1AMOnsetBaseFR, nD1AMOnsetBaseFR, alternative='two-sided')
messages.append("AM Onset baseline p-value = {}".format(pVals))
axTwentyNine.set_title("AM Onset baseline FR\n[-0.1 s, 0.0 s]\np-value = {0:.4}".format(pVals))

# ----- AM Sustained baseline FR -------
D1AMSustainedBaseFR = d1DB.AMBaseFRSustained.dropna().to_list()
nD1AMSustainedBaseFR = nD1DB.AMBaseFRSustained.dropna().to_list()
D1AMSustainedBaseFRX = jitter(np.ones(len(D1AMSustainedBaseFR))*0, 0.20)
nD1AMSustainedBaseFRX = jitter(np.ones(len(nD1AMSustainedBaseFR))*1, 0.20)

plt.sca(axThirty)
axThirty.plot(D1AMSustainedBaseFRX, D1AMSustainedBaseFR, 'o', mec=colorD1, mfc='None', alpha=markerAlpha)
axThirty.plot(nD1AMSustainedBaseFRX, nD1AMSustainedBaseFR, 'o', mec=colornD1, mfc='None', alpha=markerAlpha)

medline(axThirty, np.median(D1AMSustainedBaseFR), 0, 0.5)
medline(axThirty, np.median(nD1AMSustainedBaseFR), 1, 0.5)

axThirty.set_xticks(range(2))
axThirty.set_xticklabels(["D1", "nD1"])
axThirty.set_ylabel("Mean FR (spks/s)")

# Statistics
zStats, pVals = stats.mannwhitneyu(D1AMSustainedBaseFR, nD1AMSustainedBaseFR, alternative='two-sided')
messages.append("AM Sustained baseline p-value = {}".format(pVals))
axThirty.set_title("AM Sustained baseline FR\n[-0.5 s, -0.1 s]\np-value = {0:.4}".format(pVals))

extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
plt.show()

for message in messages:
    print(message, end="\n")
