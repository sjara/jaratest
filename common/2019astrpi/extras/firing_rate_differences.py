"""
Look at the baseline and evoked firing rates compared between D1 and nD1 cells for laserpulse, noiseburst, tuningTest, tuningCurve, and AM. Graphically, then
numerically.
"""
import copy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.gridspec as gridspec
from scipy import stats
import studyparams
from jaratoolbox import behavioranalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
import database_generation_funcs as funcs
import figparams
from extras import figure_R2_comparison as histDraw

#%% Calculations of various data to plot
db = celldatabase.load_hdf("/var/tmp/figuresdata/2019astrpi/ttDBR2.h5")

D1DB = db.query(studyparams.D1_CELLS)
nD1DB = db.query(studyparams.nD1_CELLS)
emptyD1 = np.zeros(len(D1DB))
emptyND1 = np.zeros(len(nD1DB))
D1Results = pd.DataFrame({"noiseburstBase": emptyD1,
                          "noiseburstResp": emptyD1,
                          "tuningTestBase": emptyD1,
                          "tuningTestResp": emptyD1,
                          "tuningCurveBase": emptyD1,
                          "tuningCurveResp": emptyD1,
                          "amBase": emptyD1,
                          "amResp": emptyD1,
                          })
nD1Results = pd.DataFrame({"noiseburstBase": emptyND1,
                           "noiseburstResp": emptyND1,
                           "tuningTestBase": emptyND1,
                           "tuningTestResp": emptyND1,
                           "tuningCurveBase": emptyND1,
                           "tuningCurveResp": emptyND1,
                           "amBase": emptyND1,
                           "amResp": emptyND1,
                           })

for name_ind, database in enumerate([D1DB, nD1DB]):
    if name_ind == 0:
        df = D1Results
    elif name_ind == 1:
        df = nD1Results
    for indIter, (indRow, dbRow) in enumerate(database.iterrows()):
        sessions = dbRow['sessionType']
        oneCell = ephyscore.Cell(dbRow, useModifiedClusters=False)
        cenFreq = dbRow.cf
# -------noiseburst----------
        session = 'noiseburst'
        try:
            noiseEphysData, noBData = oneCell.load(session)
        except IndexError:
            print("No {} in this site".format(session))
            df.at[indIter, "noiseburstBase"] = np.NaN
            df.at[indIter, "noiseburstResp"] = np.NaN
        else:
            noiseBaseRange = [-0.1, 0]
            noiseEventOnsetTimes = noiseEphysData['events']['soundDetectorOn']
            noiseSpikeTimes = noiseEphysData['spikeTimes']
            nspkBaseNoise, nspkRespNoise = funcs.calculate_firing_rate(noiseEventOnsetTimes, noiseSpikeTimes, noiseBaseRange)
            meanNoiseburstBase = np.mean(nspkBaseNoise)
            meanNoiseburstResp = np.mean(nspkRespNoise)
            df.at[indIter, "noiseburstBase"] = meanNoiseburstBase
            df.at[indIter, "noiseburstResp"] = meanNoiseburstResp

        session = 'tuningTest'
        try:
            ttEphysData, ttBehavData = oneCell.load(session)
        except IndexError:
            print("No {} in this site".format(session))
        except ValueError:
            print("No spikes in this site")
            df.at[indIter, "tuningTestBase"] = np.NaN
            df.at[indIter, "tuningTestResp"] = np.NaN
        else:
            ttBaseRange = [-0.1, 0]

            # Extracting information from ephys and behavior data to do calculations later with
            currentFreq = ttBehavData['currentFreq']
            currentIntensity = ttBehavData['currentIntensity']
            uniqFreq = np.unique(currentFreq)
            uniqueIntensity = np.unique(currentIntensity)
            ttTrialsEachCond = behavioranalysis.find_trials_each_combination(currentFreq, uniqFreq, currentIntensity, uniqueIntensity)

            ttSpikeTimes = ttEphysData['spikeTimes']
            ttEventOnsetTimes = ttEphysData['events']['soundDetectorOn']
            ttEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(ttEventOnsetTimes, minEventOnsetDiff=0.2)

            if len(ttEventOnsetTimes) == (len(currentFreq) + 1):
                ttEventOnsetTimes = ttEventOnsetTimes[0:-1]
                print("Correcting ephys data to be same length as behavior data")
                toCalculate = True
            elif len(ttEventOnsetTimes) == len(currentFreq):
                print("Data is already the same length")
                toCalculate = True
            else:
                print("Something is wrong with the length of these data")
                toCalculate = False
                # Instead of generating an error I made it just not calculate statistics. I should possibly have it log all mice
                # and sites where it failed to calculate so someone can review later
            if toCalculate:
                if cenFreq > 0:
                    freqIndex, = np.where(uniqFreq == cenFreq)
                    trialsCF = ttTrialsEachCond[:, freqIndex, :]
                    baseSpikesAtCF = np.array([])
                    respSpikesAtCF = np.array([])
                    nspkBaseTT, nspkRespTT = funcs.calculate_firing_rate(ttEventOnsetTimes, ttSpikeTimes, ttBaseRange)
                    for inten_cond in range(trialsCF.shape[1]):
                        trialsThisCond = trialsCF[:, 0, inten_cond]
                        if nspkBaseTT.shape[0] == len(trialsThisCond) + 1:
                            nspkBaseTT = nspkBaseTT[:-1, :]
                            nspkRespTT = nspkRespTT[:-1, :]
                        if any(trialsThisCond):
                            nspkBaseTTCond = nspkBaseTT[trialsThisCond].flatten()
                            nspkRespTTCond = nspkRespTT[trialsThisCond].flatten()
                            baseSpikesAtCF = np.concatenate((baseSpikesAtCF, nspkBaseTTCond))
                            respSpikesAtCF = np.concatenate((respSpikesAtCF, nspkRespTTCond))
                    meanTTBase = np.mean(baseSpikesAtCF)
                    meanTTResp = np.mean(respSpikesAtCF)
                    df.at[indIter, "tuningTestBase"] = meanTTBase
                    df.at[indIter, "tuningTestResp"] = meanTTResp
                else:
                    df.at[indIter, "tuningTestBase"] = np.NaN
                    df.at[indIter, "tuningTestResp"] = np.NaN

        session = 'tuningCurve'
        try:
            tuningEphysData, tuningBehavData = oneCell.load(session)
        except IndexError:
            print("No {} in this site".format(session))
            df.at[indIter, "tuningCurveBase"] = np.NaN
            df.at[indIter, "tuningCurveResp"] = np.NaN
        else:
            tuningBaseRange = [-0.1, 0]

            # Extracting information from ephys and behavior data to do calculations later with
            currentFreq = tuningBehavData['currentFreq']
            currentIntensity = tuningBehavData['currentIntensity']
            uniqFreq = np.unique(currentFreq)
            uniqueIntensity = np.unique(currentIntensity)
            tuningTrialsEachCond = behavioranalysis.find_trials_each_combination(currentFreq, uniqFreq, currentIntensity, uniqueIntensity)

            tuningSpikeTimes = tuningEphysData['spikeTimes']
            tuningEventOnsetTimes = tuningEphysData['events']['soundDetectorOn']
            tuningEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(tuningEventOnsetTimes, minEventOnsetDiff=0.2)

            if len(tuningEventOnsetTimes) == (len(currentFreq) + 1):
                tuningEventOnsetTimes = tuningEventOnsetTimes[0:-1]
                print("Correcting ephys data to be same length as behavior data")
                toCalculate = True
            elif len(tuningEventOnsetTimes) == len(currentFreq):
                print("Data is already the same length")
                toCalculate = True
            else:
                print("Something is wrong with the length of these data")
                toCalculate = False
                # Instead of generating an error I made it just not calculate statistics. I should posisbly have it log all mice
                # and sites where it failed to calculate so someone can review later
            if toCalculate:
                if cenFreq > 0:
                    freqIndex, = np.where(uniqFreq == cenFreq)
                    trialsCF = tuningTrialsEachCond[:, freqIndex, :]
                    baseSpikesAtCF = np.array([])
                    respSpikesAtCF = np.array([])
                    nspkBaseTuning, nspkRespTuning = funcs.calculate_firing_rate(tuningEventOnsetTimes, tuningSpikeTimes, tuningBaseRange)
                    for inten_cond in range(trialsCF.shape[2]):
                        trialsThisCond = trialsCF[:, 0, inten_cond]
                        if nspkBaseTuning.shape[0] == len(trialsThisCond) + 1:
                            nspkBaseTuning = nspkBaseTuning[:-1, :]
                            nspkRespTuning = nspkRespTuning[:-1, :]
                        if any(trialsThisCond):
                            nspkBaseTuningCond = nspkBaseTuning[trialsThisCond].flatten()
                            nspkRespTuningCond = nspkRespTuning[trialsThisCond].flatten()
                            baseSpikesAtCF = np.concatenate((baseSpikesAtCF, nspkBaseTuningCond))
                            respSpikesAtCF = np.concatenate((respSpikesAtCF, nspkRespTuningCond))
                    meanTuningBase = np.mean(baseSpikesAtCF)
                    meanTuningResp = np.mean(respSpikesAtCF)
                    df.at[indIter, "tuningCurveBase"] = meanTuningBase
                    df.at[indIter, "tuningCurveResp"] = meanTuningResp
                else:
                    df.at[indIter, "tuningCurveBase"] = np.NaN
                    df.at[indIter, "tuningCurveResp"] = np.NaN


        session = 'am'
        try:
            amEphysData, amBehavData = oneCell.load(session)
        except IndexError:
            print("No {} session in this site".format(session))
            df.at[indIter, "amBase"] = np.NaN
            df.at[indIter, "amResp"] = np.NaN
        else:
            amBaseRange = [-0.5, -0.1]
            amSpikeTimes = amEphysData['spikeTimes']
            amEventOnsetTimes = amEphysData['events']['soundDetectorOn']
            amCurrentFreq = amBehavData['currentFreq']
            amUniqFreq = np.unique(amCurrentFreq)
            amTrialsEachCond = behavioranalysis.find_trials_each_type(amCurrentFreq, amUniqFreq)

            if len(amCurrentFreq) != len(amEventOnsetTimes):
                amEventOnsetTimes = amEventOnsetTimes[:-1]
            if len(amCurrentFreq) != len(amEventOnsetTimes):
                print('Removing one does not align events and behavior. Skipping AM for cell')
            else:
                nspkBaseAM, nspkRespAM = funcs.calculate_firing_rate(amEventOnsetTimes, amSpikeTimes, amBaseRange)
                meanAMBase = np.mean(nspkBaseAM)
                meanAMResp = np.mean(nspkRespAM)
                df.at[indIter, "amBase"] = meanAMBase
                df.at[indIter, "amResp"] = meanAMResp

#%% ---Backups of dataframes while testing ---
D1ResultsCopy = copy.deepcopy(D1Results)
nD1ResultsCopy = copy.deepcopy((nD1Results))

#%% ------------ Transforming data to plot --------------
D1Results = D1Results.replace([np.inf, -np.inf], np.nan)
nD1Results = nD1Results.replace([np.inf, -np.inf], np.nan)

# --- Noise data ---
# Remove NaNs
D1NoiseBase = D1Results.noiseburstBase[D1Results.noiseburstBase.notnull()]
D1NoiseResp = D1Results.noiseburstResp[D1Results.noiseburstResp.notnull()]
nD1NoiseBase = nD1Results.noiseburstBase[nD1Results.noiseburstBase.notnull()]
nD1NoiseResp = nD1Results.noiseburstResp[nD1Results.noiseburstResp.notnull()]
# Remove zeros
D1NoiseBase = D1NoiseBase.iloc[D1NoiseBase.to_numpy().nonzero()]
D1NoiseResp = D1NoiseResp.iloc[D1NoiseResp.to_numpy().nonzero()]
nD1NoiseBase = nD1NoiseBase.iloc[nD1NoiseBase.to_numpy().nonzero()]
nD1NoiseResp = nD1NoiseResp.iloc[nD1NoiseResp.to_numpy().nonzero()]

# --- TuningTest data ---
# Remove NaNs
D1TuningTestBase = D1Results.tuningTestBase[D1Results.tuningTestBase.notnull()]
D1TuningTestResp = D1Results.tuningTestResp[D1Results.tuningTestResp.notnull()]
nD1TuningTestBase = nD1Results.tuningTestBase[nD1Results.tuningTestBase.notnull()]
nD1TuningTestResp = nD1Results.tuningTestResp[nD1Results.tuningTestResp.notnull()]
# Remove zeros
D1TuningTestBase = D1TuningTestBase.iloc[D1TuningTestBase.to_numpy().nonzero()]
D1TuningTestResp = D1TuningTestResp.iloc[D1TuningTestResp.to_numpy().nonzero()]
nD1TuningTestBase = nD1TuningTestBase.iloc[nD1TuningTestBase.to_numpy().nonzero()]
nD1TuningTestResp = nD1TuningTestResp.iloc[nD1TuningTestResp.to_numpy().nonzero()]

# --- TuningCurve data ---
# Remove NaNs
D1TuningCurveBase = D1Results.tuningCurveBase[D1Results.tuningCurveBase.notnull()]
D1TuningCurveResp = D1Results.tuningCurveResp[D1Results.tuningCurveResp.notnull()]
nD1TuningCurveBase = nD1Results.tuningCurveBase[nD1Results.tuningCurveBase.notnull()]
nD1TuningCurveResp = nD1Results.tuningCurveResp[nD1Results.tuningCurveResp.notnull()]
# Remove zeros
D1TuningCurveBase = D1TuningCurveBase.iloc[D1TuningCurveBase.to_numpy().nonzero()]
D1TuningCurveResp = D1TuningCurveResp.iloc[D1TuningCurveResp.to_numpy().nonzero()]
nD1TuningCurveBase = nD1TuningCurveBase.iloc[nD1TuningCurveBase.to_numpy().nonzero()]
nD1TuningCurveResp = nD1TuningCurveResp.iloc[nD1TuningCurveResp.to_numpy().nonzero()]

# --- AM data ---
# Remove NaNs
D1AMBase = D1Results.amBase[D1Results.amBase.notnull()]
D1AMResp = D1Results.amResp[D1Results.amResp.notnull()]
nD1AMBase = nD1Results.amBase[nD1Results.amBase.notnull()]
nD1AMResp = nD1Results.amResp[nD1Results.amResp.notnull()]
# Remove zeros
D1AMBase = D1AMBase.iloc[D1AMBase.to_numpy().nonzero()]
D1AMResp = D1AMResp.iloc[D1AMResp.to_numpy().nonzero()]
nD1AMBase = nD1AMBase.iloc[nD1AMBase.to_numpy().nonzero()]
nD1AMResp = nD1AMResp.iloc[nD1AMResp.to_numpy().nonzero()]

#%% ------------ Statistical calculations -------------
baseNoiseZStat, baseNoisePVal = stats.mannwhitneyu(D1NoiseBase, nD1NoiseBase, alternative='two-sided')
respNoseZStat, respNoisePVal = stats.mannwhitneyu(D1NoiseResp, nD1NoiseResp, alternative='two-sided')

baseTTZStat, baseTTPVal = stats.mannwhitneyu(D1TuningTestBase, nD1TuningTestBase, alternative='two-sided')
respTTZStat, respTTPVal = stats.mannwhitneyu(D1TuningTestResp, nD1TuningTestResp, alternative='two-sided')

baseTuningZStat, baseTuningPVal = stats.mannwhitneyu(D1TuningCurveBase, nD1TuningCurveBase, alternative='two-sided')
respTuningZStat, respTuningPVal = stats.mannwhitneyu(D1TuningCurveResp, nD1TuningCurveResp, alternative='two-sided')

baseAMZStat, baseAMPVal = stats.mannwhitneyu(D1AMBase, nD1AMBase, alternative='two-sided')
respAMZStat, respAMPVal = stats.mannwhitneyu(D1AMResp, nD1AMResp, alternative='two-sided')

#%% ------------ Evoked Plotting -------------
outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'FR_Comparisons_Evoked_no_zeros'  # Do not include extension
figFormat = 'png'  # 'pdf' or 'svg'
figSize = [15, 10]

fontSizeLabels = figparams.fontSizeLabels*2
# fontSizeTicks = figparams.fontSizeTicks*2
fontSizeTicks = fontSizeLabels
fontSizePanel = figparams.fontSizePanel*2
fontSizeTitles = figparams.fontSizeTitles

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

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

# Define the layout
gs = gridspec.GridSpec(2, 2)
gs.update(left=0.04, right=0.97, top=0.94, bottom=0.05, wspace=0.3, hspace=0.3)

axNoise = plt.subplot(gs[0, 0])
axTT = plt.subplot(gs[0, 1])
axTuning = plt.subplot(gs[1, 0])
axAM = plt.subplot(gs[1, 1])

plt.text(0, 1.1, 'Noise', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axNoise.transAxes)
plt.text(0, 1.1, 'TT', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axTT.transAxes)
plt.text(0, 1.1, 'TC', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axTuning.transAxes)
plt.text(0, 1.1, 'AM', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axAM.transAxes)

# --- Noiseburst plotting ---
plt.sca(axNoise)

histDraw.normalized_hist(D1NoiseResp, nD1NoiseResp, axNoise, colorD1, colornD1, bin_number=300)
axNoise.set_xlabel("Firing Rate")
axNoise.set_ylabel("Frequency")
axNoise.set_title("Noiseburst evoked FRs\np-value={}".format(round(respNoisePVal, 4)))
axNoise.set_xlim([0, 1])

# --- TuningTest plotting ---
plt.sca(axTT)

histDraw.normalized_hist(D1TuningTestResp, nD1TuningTestResp, axTT, colorD1,
                         colornD1, bin_number=60)
axTT.set_xlabel("Firing Rate")
axTT.set_ylabel("Frequency")
axTT.set_title("Tuning Test evoked FRs\np-value={}".format(round(respTTPVal, 4)))
axTT.set_xlim([0, 2])

# --- TuningCurve plotting ---
plt.sca(axTuning)

histDraw.normalized_hist(D1TuningCurveResp, nD1TuningCurveResp, axTuning, colorD1,
                         colornD1, bin_number=80)
axTuning.set_xlabel("Firing Rate")
axTuning.set_ylabel("Frequency")
axTuning.set_title("Tuning Curve evoked FRs\np-value={}".format(round(respTuningPVal, 4)))
axTuning.set_xlim([0, 1])

# --- AM plotting ---
plt.sca(axAM)

histDraw.normalized_hist(D1AMResp, nD1AMResp, axAM, colorD1, colornD1, bin_number=100)
axAM.set_xlabel("Firing Rate")
axAM.set_ylabel("Frequency")
axAM.set_title("AM evoked FRs\np-value={}".format(round(respAMPVal, 4)))
axAM.set_xlim([0, 2])


extraplots.save_figure(figFilename, figFormat, figSize, outputDir, 'w')
print('{} saved to {}'.format(figFilename, figparams.FIGURE_OUTPUT_DIR))

plt.show()

# ------------  Baseline Plotting -------------
fig.clf()
fig.set_facecolor('w')
figFilename = 'FR_Comparisons_Baseline_no_zeros'

# Define the layout
gs = gridspec.GridSpec(2, 2)
gs.update(left=0.04, right=0.97, top=0.94, bottom=0.05, wspace=0.3, hspace=0.3)

axNoise = plt.subplot(gs[0, 0])
axTT = plt.subplot(gs[0, 1])
axTuning = plt.subplot(gs[1, 0])
axAM = plt.subplot(gs[1, 1])

plt.text(0, 1.1, 'Noise', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axNoise.transAxes)
plt.text(0, 1.1, 'TT', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axTT.transAxes)
plt.text(0, 1.1, 'TC', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axTuning.transAxes)
plt.text(0, 1.1, 'AM', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axAM.transAxes)

# --- Noiseburst plotting ---
plt.sca(axNoise)

histDraw.normalized_hist(D1NoiseBase, nD1NoiseBase, axNoise, colorD1, colornD1, bin_number=300)
axNoise.set_xlabel("Firing Rate")
axNoise.set_ylabel("Frequency")
axNoise.set_title("Noiseburst baseline FRs\np-value={}".format(round(baseNoisePVal, 4)))
axNoise.set_xlim([0, 1])

# --- TuningTest plotting ---
plt.sca(axTT)

histDraw.normalized_hist(D1TuningTestBase, nD1TuningTestBase, axTT, colorD1,
                         colornD1, bin_number=60)
axTT.set_xlabel("Firing Rate")
axTT.set_ylabel("Frequency")
axTT.set_title("Tuning Test baseline FRs\np-value={}".format(round(baseTTPVal, 4)))
axTT.set_xlim([0, 1.5])

# --- TuningCurve plotting ---
plt.sca(axTuning)

histDraw.normalized_hist(D1TuningCurveBase, nD1TuningCurveBase, axTuning, colorD1,
                         colornD1, bin_number=80)
axTuning.set_xlabel("Firing Rate")
axTuning.set_ylabel("Frequency")
axTuning.set_title("Tuning Curve baseline FRs\np-value={}".format(round(baseTuningPVal, 4)))
axTuning.set_xlim([0, 1.5])

# --- AM plotting ---
plt.sca(axAM)

histDraw.normalized_hist(D1AMBase, nD1AMBase, axAM, colorD1, colornD1, bin_number=100)
axAM.set_xlabel("Firing Rate")
axAM.set_ylabel("Frequency")
axAM.set_title("AM baseline FRs\np-value={}".format(round(baseAMPVal, 4)))
axAM.set_xlim([0, 2])


extraplots.save_figure(figFilename, figFormat, figSize, outputDir, 'w')
print('{} saved to {}'.format(figFilename, figparams.FIGURE_OUTPUT_DIR))

plt.show()

