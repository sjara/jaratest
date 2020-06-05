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
SAVE_FIGURE = 1
outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'figure_frequency_tuning'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
figSize = [20, 5.75]

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
# fig = plt.gcf()
# fig.clf()
fig = plt.figure(figsize=figSize)
fig.set_facecolor('w')

# Define the layout
# gs = gridspec.GridSpec(2, 5)
# gs.update(left=0.02, right=0.98, top=0.95, bottom=0.125, wspace=0.7, hspace=0.5)
gs = gridspec.GridSpec(1, 8)
gs.update(left=0.04, right=0.98, top=0.95, bottom=0.175, wspace=1.1, hspace=0.5)

axOne = plt.subplot(gs[0, 0])
axTwo = plt.subplot(gs[0, 1])
axThree = plt.subplot(gs[0, 2])
axFour = plt.subplot(gs[0, 3])
axFive = plt.subplot(gs[0, 4])
axSix = plt.subplot(gs[0, 5])
axSeven = plt.subplot(gs[0, 6])
axEight = plt.subplot(gs[0, 7])

# for axis in [axBW, axLatency, axThresh, axOnsetivity, axMonotonicity]:
#     for side in axis.spines.keys():
#         axis.spines[side].linewidth = 200

# plt.text(-0.3, 1.03, 'A', ha='center', va='center',
#          fontsize=fontSizePanel, fontweight='bold',
#          transform=axTwo.transAxes)
# plt.text(-0.3, 1.03, 'B', ha='center', va='center',
#          fontsize=fontSizePanel, fontweight='bold',
#          transform=axOne.transAxes)
# plt.text(-0.41, 1.01, 'C', ha='center', va='center',
#          fontsize=fontSizePanel, fontweight='bold',
#          transform=axThree.transAxes)
# plt.text(-0.38, 1.01, 'D', ha='center', va='center',
#          fontsize=fontSizePanel, fontweight='bold',
#          transform=axFour.transAxes)
# plt.text(-0.38, 1.01, 'E', ha='center', va='center',
#          fontsize=fontSizePanel, fontweight='bold',
#          transform=axFive.transAxes)
# plt.text(-0.3, 1.01, 'F', ha='center', va='center',
#          fontsize=fontSizePanel, fontweight='bold',
#          transform=axSix.transAxes)
# plt.text(-0.3, 1.01, 'G', ha='center', va='center',
#          fontsize=fontSizePanel, fontweight='bold',
#          transform=axSeven.transAxes)

#%% Load in data
nameDB = studyparams.DATABASE_NAME + '.h5'
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
db = celldatabase.load_hdf(pathtoDB)
d1DB = db.query(studyparams.D1_CELLS)
nD1DB = db.query(studyparams.nD1_CELLS)

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
axFive.set_title("Tuning Curve R2 fit")

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

plt.show()
