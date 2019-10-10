"""
[For all cells in DB] create cell reports include the following plots for three sessions:
noiseburst: raster, PSTH, ISI, waverform, sparks over time
laserpulse: raster, PSTH, ISI, waveform, sparks over time
TuningCurve: raster plot(for one intensity), waveform

You have to specify the name of the subject you want to generate the reports for,
and give answer to question which duplicated session do you want to use to plot in\
case you have more than one same sessions such as laserpulse
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import random
from jaratoolbox import settings
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import spikesorting
from jaratoolbox import ephyscore
from jaratoolbox import celldatabase
from jaratoolbox import behavioranalysis
import figparams
import studyparams

if sys.version_info[0] < 3:
    input_func = raw_input
elif sys.version_info[0] >= 3:
    input_func = input

# -----------parameters----------------
timeRange = [-0.5, 0.5]
binWidth = 0.010
timeVec = np.arange(timeRange[0], timeRange[-1], binWidth)
smoothWinSizePsth = 3  # smoothWinSizePsth2 = 3
lwPsth = 2
downsampleFactorPsth = 1
msRaster = 2
tuningcurve = studyparams.tuningcurve  # ['tuningCurve','tuningCurve(tc)']

# ---------subplot adjust------------
bottom = 0.05
top = 0.93
hspace = 0.4
wspace = 0.65
left = 0.1
right = 0.88
countreport = 0  # count the number of reports generated

# ---------------------------------------------------------------------------
fig = plt.gcf()
fig.clf()

studyname = studyparams.STUDY_NAME
outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyname, 'new_reports/')

d1mice = studyparams.ASTR_D1_CHR2_MICE
nameDB = '_'.join(d1mice) + '.h5'
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
db = celldatabase.load_hdf(pathtoDB)
celldb = db.query('rsquaredFit>{}'.format(studyparams.R2_CUTOFF))
celldb = celldb.query('subject=="d1pi041"')

# -------------------------------------------------------------------------------
for indRow, dbRow in celldb.iterrows():
    oneCell = ephyscore.Cell(dbRow, useModifiedClusters=False)

    rast1 = []
    rast2 = []
    spkMat = []
    spikeT = []
    waveF = []
    ax = []

    sessionCell = [con for (i, con) in enumerate(dbRow['sessionType'])]  # if con == 'sessiontype']
    sessionUC = pd.Series(sessionCell).unique()  # sessionUC = list(set(sessionCell)) even numpy changes the sequence
    sessionsOrig = [ss for ss in sessionUC if (ss == 'noiseburst') or (ss == 'laserpulse') or (ss == 'tuningCurve')]
    sessions = np.copy(sessionsOrig)

    # Establishing gridspecs
    gs = gridspec.GridSpec(4, 8, width_ratios=[1, 1, 1, 1, 1, 1, 6, 4])
    gs.update(left=0.04, right=0.98, top=0.90, bottom=0.175, wspace=1.1, hspace=0.5)

    axNoiseburstRaster = plt.subplot(gs[0, 0:2])
    axLaserpulseRaster = plt.subplot(gs[0, 2:4])

    axNoiseburstPSTH = plt.subplot(gs[1, 0:2])
    axLaserpulsePSTH = plt.subplot(gs[1, 2:4])

    axTuningCurveISI = plt.subplot(gs[3, 0:2])
    axLaserpulseISI = plt.subplot(gs[2, 0:2])
    axTuningCurveWaveform = plt.subplot(gs[3, 2:4])
    axLaserpulseWaveform = plt.subplot(gs[2, 2:4])
    axTuningCurveEvents = plt.subplot(gs[2, 0:2])

    axTuningCurveRaster = plt.subplot(gs[0:3, 4:7])
    axTuningCurveHeatmap = plt.subplot(gs[3, 4:6])

    for sessiontype in sessionsOrig:

        sessionInds = [ind for (ind, con) in enumerate(dbRow['sessionType']) if con == sessiontype]
        randomchoice = random.choice(sessionInds)
        sessionIndToUse = sessionInds[-1]
        ephysData, bdata = oneCell.load_by_index(sessionIndToUse)  # behavClass=behavClass you may need to include that while doing tuning curve

        spikeTimes = ephysData['spikeTimes']
        if sessiontype == 'laserpulse':
            eventOnsetTimes = ephysData['events']['stimOn']
        else:
            eventOnsetTimes = ephysData['events']['soundDetectorOn']

        # --------------------------Tuning curve-------------------------------
        # tuning curve variables
        if sessiontype == 'tuningCurve':
            currentFreq = bdata['currentFreq']
            trialsEachType = behavioranalysis.find_trials_each_type(currentFreq,
                                                                    np.unique(currentFreq))
            uniqFreq = np.unique(currentFreq)
            b = np.array(["%.0f" % i for i in uniqFreq])  # this is unique frequencies
            freqTicks = [str(b[i])+" ["+str(i)+"]" for i, con in enumerate(b)]
            nTrialsEachCond = [trialsEachType[:, i].sum() for i in range(trialsEachType.shape[1])]
            new_tick_locations = np.cumsum(nTrialsEachCond)

            # Heatmap calculations of tuning curve
            lowFreq = 2
            highFreq = 40
            nFreqLabels = 3

            freqTickLocations = np.linspace(0, 15, nFreqLabels)
            freqs = np.logspace(np.log10(lowFreq), np.log10(highFreq), nFreqLabels)
            freqs = np.round(freqs, decimals=1)

            baseRange = [-0.1, 0]
            responseRange = [0, 0.1]
            alignmentRange = [baseRange[0], responseRange[1]]

            currentIntensity = bdata['currentIntensity']
            possibleIntensity = np.unique(bdata['currentIntensity'])
            nIntenLabels = len(possibleIntensity)
            lowIntensity = min(possibleIntensity)
            highIntensity = max(possibleIntensity)
            intensities = np.linspace(lowIntensity, highIntensity, nIntenLabels)
            intensities = intensities.astype(np.int)
            intenTickLocations = np.linspace(0, nIntenLabels - 1, nIntenLabels)
            allIntenResp = np.empty((len(possibleIntensity), len(uniqFreq)))
            for indinten, inten in enumerate(possibleIntensity):

                for indfreq, freq in enumerate(uniqFreq):
                    selectinds = np.flatnonzero((currentFreq == freq) & (currentIntensity == inten))
                    # =====================index mismatch======================
                    while selectinds[-1] >= eventOnsetTimes.shape[0]:
                        selectinds = np.delete(selectinds, -1, 0)

                    # ---------------------------------------------------------
                    selectedOnsetTimes = eventOnsetTimes[selectinds]
                    (spikeTimesFromEventOnset, trialIndexForEachSpike,
                     indexLimitsEachTrial) = \
                        spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                              selectedOnsetTimes,
                                                              alignmentRange)

                    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial,
                                                                        responseRange)

                    allIntenResp[indinten, indfreq] = np.mean(nspkResp)
                    FR_data = allIntenResp/0.1

        (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)
        # -----------------------PSTH spikecountmatrix ------------------------
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                 indexLimitsEachTrial,
                                                                 timeVec)

        # -------------------------Getting ready for plotting------------------
        rast1.append(spikeTimesFromEventOnset)
        rast2.append(indexLimitsEachTrial)
        spkMat.append(spikeCountMat)
        spikeT.append(spikeTimes)
        waveF.append(ephysData['samples'])

    # -----------------------Plot variables-----------------------------
    tetnum = dbRow['tetrode']
    chanum = dbRow['cluster']

    # bestCells = celldb.query("isiViolations<0.02 or modifiedISI<0.02")
    # -------------------------end of set variable-----------------------------
    # -----------------------Raster,PSTH,ISI,WaveForm,EventTime----------------
    for sessInd, con in enumerate(sessions):
        if con not in tuningcurve:

            # Noiseburst plotting
            if con == 'noiseburst':
                # Raster plotting
                plt.sca(axNoiseburstRaster)
                pRaster, hcond, zline = extraplots.raster_plot(rast1[sessInd],
                                                               rast2[sessInd],
                                                               timeRange,
                                                               trialsEachCond=[],
                                                               colorEachCond='g')
                plt.setp(pRaster, ms=msRaster)
                plt.setp(hcond, zorder=3)
                plt.ylabel('Trial')
                axNoiseburstRaster.set_xlim(-0.3, 0.5)
                plt.title(con.title())

                # PSTH plotting
                plt.sca(axNoiseburstPSTH)
                pPSTH = extraplots.plot_psth(spkMat[sessInd] / binWidth,
                                             smoothWinSizePsth, timeVec,
                                             trialsEachCond=[],
                                             linestyle=None, linewidth=lwPsth,
                                             downsamplefactor=downsampleFactorPsth,
                                             colorEachCond='g')
                extraplots.boxoff(plt.gca())
                plt.ylabel('Firing rate\n(spk/s)')
                plt.xlabel('time from onset of the sound(s)')

            # Laserpulse plotting
            elif con == 'laserpulse':
                # Raster plotting
                plt.sca(axLaserpulseRaster)
                pRaster, hcond, zline = extraplots.raster_plot(rast1[sessInd],
                                                               rast2[sessInd],
                                                               timeRange,
                                                               trialsEachCond=[],
                                                               colorEachCond='r')
                plt.setp(pRaster, ms=msRaster)
                plt.setp(hcond, zorder=3)
                plt.ylabel('Trial')
                axLaserpulseRaster.set_xlim(-0.3, 0.5)
                plt.title(con.title())

                # PSTH plotting
                plt.sca(axLaserpulsePSTH)
                pPSTH = extraplots.plot_psth(spkMat[sessInd] / binWidth,
                                             smoothWinSizePsth, timeVec,
                                             trialsEachCond=[], linestyle=None,
                                             linewidth=lwPsth,
                                             downsamplefactor=downsampleFactorPsth,
                                             colorEachCond='r')
                extraplots.boxoff(plt.gca())
                plt.ylabel('Firing rate\n(spk/s)')
                plt.xlabel('time from onset of the sound(s)')

                # Plot waveforms
                plt.sca(axLaserpulseWaveform)
                if waveF[sessInd].any():
                    all_waves, mean_waves, scale_bar = spikesorting.plot_waveforms(waveF[sessInd])
                    plt.setp(mean_waves, color='r')
                plt.title(con.title())

        # Tuning Curve
        else:
            # ----------if the length doesn't match, abandon last one from trialsEachType
            while indexLimitsEachTrial.shape[1] < trialsEachType.shape[0]:
                trialsEachType = np.delete(trialsEachType, -1, 0)

            plt.sca(axTuningCurveRaster)
            pRaster, hcond, zline = extraplots.raster_plot(rast1[sessInd],
                                                           rast2[sessInd],
                                                           timeRange,
                                                           trialsEachCond=trialsEachType)

            plt.setp(pRaster, ms=msRaster)
            plt.setp(hcond, zorder=3)
            plt.ylabel('Trial')
            axTuningCurveRaster.set_yticks(new_tick_locations)
            axTuningCurveRaster.set_yticklabels(new_tick_locations)
            plt.xticks(np.arange(timeRange[0], timeRange[1], .02))
            plt.xlim([-0.05, 0.3])

            ylim = axTuningCurveRaster.get_ylim()
            plt.vlines(dbRow['latency'], ylim[0], ylim[1], colors='b')

            plt.title(con.title())
            # still raster plot, plotting frequency levels
            axTuningCurveRaster.set_yticks(new_tick_locations)
            axTuningCurveRaster.set_yticklabels(freqTicks)
            axTuningCurveRaster.set_ylabel('Frequency(Hz)')

            # Waveform
            plt.sca(axTuningCurveWaveform)
            if waveF[sessInd].any():
                all_waves, mean_waves, scale_bar = \
                    spikesorting.plot_waveforms(waveF[sessInd])
                plt.setp(mean_waves, color='b')
                plt.setp(all_waves, color='m')
            plt.axis('off')
            plt.title(con.title())

            # ISI plot
            plt.sca(axTuningCurveISI)
            hp_ISI, ISIhistogram, ISIbins = \
                spikesorting.plot_isi_loghist(spikeT[sessInd])
            plt.setp(hp_ISI, color='b')
            plt.title(con.title())

            # Plot events in time
            plt.sca(axTuningCurveEvents)
            if spikeT[sessInd].any():
                hp_Events = spikesorting.plot_events_in_time(spikeT[sessInd])
                plt.setp(hp_Events, color='b')
            plt.title(con.title())

            # ----------------------- Tuning Curve heatmap --------------------
            fontSizeLabels = figparams.fontSizeLabels * 2
            fontSizeTicks = fontSizeLabels

            cax = axTuningCurveHeatmap.imshow(np.flipud(FR_data),
                                              interpolation='nearest',
                                              cmap='Blues')
            cbar = plt.colorbar(cax, ax=axTuningCurveHeatmap, format='%d')
            maxFR = np.max(FR_data.ravel())
            cbar.ax.set_ylabel('Firing rate\n(spk/s)',
                               fontsize=fontSizeLabels, labelpad=-10)
            extraplots.set_ticks_fontsize(cbar.ax, fontSizeTicks)
            cbar.set_ticks([0, maxFR])
            cax.set_clim([0, maxFR])

            axTuningCurveHeatmap.set_yticks(intenTickLocations)
            axTuningCurveHeatmap.set_yticklabels(intensities[::-1])
            axTuningCurveHeatmap.set_xticks(freqTickLocations)
            freqLabels = ['{0:.1f}'.format(freq) for freq in freqs]
            axTuningCurveHeatmap.set_xticklabels(freqLabels)
            axTuningCurveHeatmap.set_xlabel('Frequency (kHz)',
                                            fontsize=fontSizeLabels)
            axTuningCurveHeatmap.set_ylabel('Intensity (dB SPL)',
                                            fontsize=fontSizeLabels)
            extraplots.set_ticks_fontsize(axTuningCurveHeatmap, fontSizeTicks)

    # ###############################################################################
    title = '[{5}]{0}, {1}, {2}um, T{3}c{4}, session ={6}'.format(
        dbRow['subject'], dbRow['date'], dbRow['depth'], tetnum, chanum,
        dbRow.name, sessionCell)
    plt.suptitle(title, fontsize=15, fontname="Times New Roman Bold")
    fig.set_size_inches([20, 10])
    # pathtoPng = os.path.join(outputDir, 'cellreport/')
    fig.savefig(outputDir + '[c#{0}] {1}_{2}_tetrode{3}_cluster{4}.png'.format(
        dbRow.name, dbRow['subject'], dbRow['depth'], tetnum, chanum))
    plt.clf()
    countreport += 1
    print("Report number {} generated!".format(countreport))
print("Total of {} reports have been generated".format(countreport))

plt.plot()
