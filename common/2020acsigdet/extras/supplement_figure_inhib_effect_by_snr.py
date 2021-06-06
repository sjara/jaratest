import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
import studyparams
import behaviour_analysis_funcs as bf

FIGNAME = 'figure_inhibitory_inactivation'
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 1]  # Plot panel i if PANELS[i]==1
#PANELS = [0, 1, 0, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
CORRECTED = 0
CIS = 1
outputDir = '/tmp/'
if CORRECTED:
    figFilename = 'FigX_inhib_inactivation_by_snr_corrected'  # Do not include extension
else:
    figFilename = 'FigX_inhib_inactivation_by_snr'
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [8,10]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.36, 0.66, 0.42]  # Horiz position for panel labels
labelPosY = [0.98, 0.78, 0.48, 0.28]  # Vert position for panel labels

summaryFileName = 'change_behaviour_by_snr_inhib_inactivation_v2.npz'

ExcColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(3, 3)
gs.update(top=0.95, bottom=0.15, left=0.17, right=0.94, wspace=0.5, hspace=0.3)

# --- summary of change in tone reported during PV or SOM inactivation by snr split by bw ---
if PANELS[0]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    possibleSNRs = summaryData['possibleSNRs']
    possibleBands = summaryData['possibleBands']
    PVpsyCurves = summaryData['PVpsyCurves']
    PVcontrolPsyCurves = summaryData['PVpsyCurvesControl']
    SOMpsyCurves = summaryData['SOMpsyCurves']
    SOMcontrolPsyCurves = summaryData['SOMpsyCurvesControl']

    PVshape = [PVpsyCurves.shape[0], len(possibleBands), len(possibleSNRs)]
    SOMshape = [SOMpsyCurves.shape[0], len(possibleBands), len(possibleSNRs)]

    PVdetectDiff = np.diff(PVpsyCurves, axis=1).reshape(PVshape)
    SOMdetectDiff = np.diff(SOMpsyCurves, axis=1).reshape(SOMshape)
    PVdetectDiffControl = np.diff(PVcontrolPsyCurves, axis=1).reshape(PVshape)
    SOMdetectDiffControl = np.diff(SOMcontrolPsyCurves, axis=1).reshape(SOMshape)

    if CORRECTED:
        correctedPVdetectDiff = PVdetectDiff - PVdetectDiffControl
        correctedSOMdetectDiff = SOMdetectDiff - SOMdetectDiffControl

        PVpsyCurves[:,1,:,:] = PVpsyCurves[:,1,:,:] + PVdetectDiffControl
        SOMpsyCurves[:,1,:,:] = SOMpsyCurves[:,1,:,:] + SOMdetectDiffControl
    else:
        correctedPVdetectDiff = PVdetectDiff
        correctedSOMdetectDiff = SOMdetectDiff

    colours = [PVColour, SOMColour]
    starSide = [1.0, -1.0]
    typeLabel = ['no PV', 'no SOM']
    changeData = [correctedPVdetectDiff, correctedSOMdetectDiff]

    xVals = range(len(possibleSNRs))

    for indBand, band in enumerate(possibleBands):
        axCurves = plt.subplot(gs[0, indBand])
        for indType, changes in enumerate(changeData):

            median = np.median(changes[:, indBand, :], axis=0)
            plt.plot(xVals, median, 'o-', color=colours[indType], lw=3, ms=9)

            if not CIS:
                for indMouse in range(changes.shape[0]):
                    plt.plot(xVals, changes[indMouse,indBand,:], '-', color=colours[indType], alpha=0.3)
            else:
                for indSNR in xVals:
                    CI = bf.bootstrap_median_CI(changes[:,indBand,indSNR])
                    # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
                    plt.plot([indSNR, indSNR], CI, color=colours[indType], linewidth=1.5)  # error bars
                    plt.plot([indSNR - 0.2, indSNR + 0.2], [CI[0], CI[0]], color=colours[indType], linewidth=1.5)  # bottom caps
                    plt.plot([indSNR - 0.2, indSNR + 0.2], [CI[1], CI[1]], color=colours[indType], linewidth=1.5)  # top caps

            plt.plot([-10, 10], [0, 0], '--', color='0.5')

            axCurves.set_xlim(xVals[0]-0.3, xVals[-1]+0.3)
            axCurves.set_xticks(xVals)
            axCurves.set_xticklabels(possibleSNRs)
            axCurves.set_xlabel('SNR (dB)', fontsize=fontSizeLabels)

            yLim = [-40, 25]
            axCurves.set_ylim(yLim)
            axCurves.set_ylabel('Change in tone reported (%)', fontsize=fontSizeLabels)

            plt.title(f'{band} octaves')

            # stats
            for indsnr, snr in enumerate(possibleSNRs):
                pVal = stats.wilcoxon(changes[:,indBand,indsnr])
                print(f'{typeLabel[indType]} change in tone detect at {band} octaves and {snr} SNR: {pVal}')

                if pVal[1] < 0.05:
                    hs, = axCurves.plot(xVals[indsnr], 0.9 * yLim[1-indType], '*', mfc=colours[indType], mec='None', clip_on=False)
                    hs.set_markersize(8)
                else:
                    axCurves.text(xVals[indsnr], 0.9 * yLim[1-indType], 'ns', fontsize=8, va='center', ha='center', color=colours[indType], clip_on=False)
                    #extraplots.significance_stars(xVals[indsnr], starSide[indType] * 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3, color=colours[indType])

                if indType==1: #just so this shit doesn't get printed twice
                    pVal = stats.ranksums(correctedPVdetectDiff[:, indBand, indsnr], correctedSOMdetectDiff[:, indBand, indsnr])
                    print(f'PV vs SOM diff in tone detect at {band} octaves and {snr} SNR: {pVal}')

                    if pVal[1] < 0.05:
                        hs, = axCurves.plot(xVals[indsnr], 0, '*', mfc='k', mec='None', clip_on=False)
                        hs.set_markersize(8)
                    else:
                        axCurves.text(xVals[indsnr], 0, 'ns', fontsize=8, va='center', ha='center', color='k', clip_on=False)

        extraplots.boxoff(axCurves)
        extraplots.set_ticks_fontsize(axCurves, fontSizeTicks)

# --- as above but condensing both bandwidths into one ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    possibleSNRs = summaryData['possibleSNRs']
    possibleBands = summaryData['possibleBands']
    PVshape = [summaryData['PVtrialCounts'].shape[0], len(possibleSNRs)]
    SOMshape = [summaryData['SOMtrialCounts'].shape[0], len(possibleSNRs)]

    PVtrialCounts = np.sum(summaryData['PVtrialCounts'], axis=2)
    SOMtrialCounts = np.sum(summaryData['SOMtrialCounts'], axis=2)

    PVpsyCurves = np.zeros((PVshape[0],2,len(possibleSNRs)))
    SOMpsyCurves = np.zeros((SOMshape[0], 2, len(possibleSNRs)))

    PVpsyCurves[:,:,0] = 100.0 * PVtrialCounts[:,:,0,1]/(PVtrialCounts[:,:,0,1] + PVtrialCounts[:,:,0,0])
    PVpsyCurves[:,:,1:] = 100.0 * PVtrialCounts[:,:,1:,0]/(PVtrialCounts[:,:,1:,1] + PVtrialCounts[:,:,1:,0])
    
    SOMpsyCurves[:,:,0] = 100.0 * SOMtrialCounts[:,:,0,1]/(SOMtrialCounts[:,:,0,1] + SOMtrialCounts[:,:,0,0])
    SOMpsyCurves[:,:,1:] = 100.0 * SOMtrialCounts[:,:,1:,0]/(SOMtrialCounts[:,:,1:,1] + SOMtrialCounts[:,:,1:,0])

    if CORRECTED:
        PVtrialCountsControl = np.sum(summaryData['PVtrialCountsControl'], axis=2)
        SOMtrialCountsControl = np.sum(summaryData['SOMtrialCountsControl'], axis=2)
    
        PVpsyCurvesControl = np.zeros((PVshape[0],2,len(possibleSNRs)))
        SOMpsyCurvesControl = np.zeros((SOMshape[0], 2, len(possibleSNRs)))
    
        PVpsyCurvesControl[:,:,0] = 100.0 * PVtrialCountsControl[:,:,0,1]/(PVtrialCountsControl[:,:,0,1] + PVtrialCountsControl[:,:,0,0])
        PVpsyCurvesControl[:,:,1:] = 100.0 * PVtrialCountsControl[:,:,1:,0]/(PVtrialCountsControl[:,:,1:,1] + PVtrialCountsControl[:,:,1:,0])
        
        SOMpsyCurvesControl[:,:,0] = 100.0 * SOMtrialCountsControl[:,:,0,1]/(SOMtrialCountsControl[:,:,0,1] + SOMtrialCountsControl[:,:,0,0])
        SOMpsyCurvesControl[:,:,1:] = 100.0 * SOMtrialCountsControl[:,:,1:,0]/(SOMtrialCountsControl[:,:,1:,1] + SOMtrialCountsControl[:,:,1:,0])
        
        PVchangeControl = np.diff(PVpsyCurvesControl, axis=1).reshape(PVshape)
        SOMchangeControl = np.diff(SOMpsyCurvesControl, axis=1).reshape(SOMshape)
        
        PVchange = np.diff(PVpsyCurves, axis=1).reshape(PVshape) - PVchangeControl
        SOMchange = np.diff(SOMpsyCurves, axis=1).reshape(SOMshape) - SOMchangeControl
    else:
        PVchange = np.diff(PVpsyCurves, axis=1).reshape(PVshape)
        SOMchange = np.diff(SOMpsyCurves, axis=1).reshape(SOMshape)

    changeData = [PVchange, SOMchange]
    axCurves = plt.subplot(gs[0, 2])
    colours = [PVColour, SOMColour]
    xVals = range(len(possibleSNRs))

    for indType, changes in enumerate(changeData):
        for indMouse in range(changes.shape[0]):
            plt.plot(xVals, changes[indMouse, :], '-', color=colours[indType], alpha=0.3)

        median = np.median(changes, axis=0)
        plt.plot(xVals, median, 'o-', color=colours[indType], lw=3, ms=9)

        plt.plot([-10, 10], [0, 0], '--', color='0.5')

    axCurves.set_xlim(xVals[0] - 0.3, xVals[-1] + 0.3)
    axCurves.set_xticks(xVals)
    axCurves.set_xticklabels(possibleSNRs)
    axCurves.set_xlabel('SNR (dB)', fontsize=fontSizeLabels)

    axCurves.set_ylim(-40, 25)
    axCurves.set_ylabel('Change in tone reported (%)', fontsize=fontSizeLabels)

    plt.title('bands combined')

    extraplots.boxoff(axCurves)
    extraplots.set_ticks_fontsize(axCurves, fontSizeTicks)

# --- summary of change in accuracy during PV or SOM inactivation by snr split by bw ---
if PANELS[2]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    possibleSNRs = summaryData['possibleSNRs']
    possibleBands = summaryData['possibleBands']
    PVaccuracies = summaryData['PVaccuracies']
    PVaccuraciesControl = summaryData['PVaccuraciesControl']
    SOMaccuracies = summaryData['SOMaccuracies']
    SOMaccuraciesControl = summaryData['SOMaccuraciesControl']

    PVshape = [PVaccuracies.shape[0], len(possibleBands), len(possibleSNRs)]
    SOMshape = [SOMaccuracies.shape[0], len(possibleBands), len(possibleSNRs)]

    PVaccuracyDiff = np.diff(PVaccuracies, axis=1).reshape(PVshape)
    SOMaccuracyDiff = np.diff(SOMaccuracies, axis=1).reshape(SOMshape)
    PVaccuracyDiffControl = np.diff(PVaccuraciesControl, axis=1).reshape(PVshape)
    SOMaccuracyDiffControl = np.diff(SOMaccuraciesControl, axis=1).reshape(SOMshape)

    if CORRECTED:
        correctedPVaccuraciesDiff = PVaccuracyDiff - PVaccuracyDiffControl
        correctedSOMaccuraciesDiff = SOMaccuracyDiff - SOMaccuracyDiffControl
        #
        # PVaccuracyDiff[:,1,:,:] = PVaccuracyDiff[:,1,:,:] + PVaccuracyDiffControl
        # SOMaccuracyDiff[:,1,:,:] = SOMaccuracyDiff[:,1,:,:] + SOMaccuracyDiffControl
    else:
        correctedPVaccuraciesDiff = PVaccuracyDiff
        correctedSOMaccuraciesDiff = SOMaccuracyDiff

    colours = [PVColour, SOMColour]
    starSide = [1.0, -1.0]
    typeLabel = ['no PV', 'no SOM']
    changeData = [correctedPVaccuraciesDiff, correctedSOMaccuraciesDiff]

    xVals = range(len(possibleSNRs))

    for indBand, band in enumerate(possibleBands):
        axCurves = plt.subplot(gs[1, indBand])
        for indType, changes in enumerate(changeData):

            median = np.median(changes[:,indBand,:], axis=0)
            plt.plot(xVals, median, 'o-', color=colours[indType], lw=3, ms=9)

            if not CIS:
                for indMouse in range(changes.shape[0]):
                    plt.plot(xVals, changes[indMouse,indBand,:], '-', color=colours[indType], alpha=0.3)
            else:
                for indSNR in xVals:
                    CI = bf.bootstrap_median_CI(changes[:,indBand,indSNR])
                    # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
                    plt.plot([indSNR, indSNR], CI, color=colours[indType], linewidth=1.5)  # error bars
                    plt.plot([indSNR - 0.2, indSNR + 0.2], [CI[0], CI[0]], color=colours[indType], linewidth=1.5)  # bottom caps
                    plt.plot([indSNR - 0.2, indSNR + 0.2], [CI[1], CI[1]], color=colours[indType], linewidth=1.5)  # top caps

            plt.plot([-10, 10], [0, 0], '--', color='0.5')

            axCurves.set_xlim(xVals[0]-0.3, xVals[-1]+0.3)
            axCurves.set_xticks(xVals)
            axCurves.set_xticklabels(possibleSNRs)
            axCurves.set_xlabel('SNR (dB)', fontsize=fontSizeLabels)

            yLim = [-40, 25]
            axCurves.set_ylim(yLim)
            axCurves.set_ylabel('Change in accuracy (%)', fontsize=fontSizeLabels)

            plt.title(f'{band} octaves')

            # stats
            for indsnr, snr in enumerate(possibleSNRs):
                pVal = stats.wilcoxon(changes[:,indBand,indsnr])
                print(f'{typeLabel[indType]} change in accuracy at {band} octaves and {snr} SNR: {pVal}')

                if pVal[1] < 0.05:
                    hs, = axCurves.plot(xVals[indsnr], 0.9 * yLim[1-indType], '*', mfc=colours[indType], mec='None', clip_on=False)
                    hs.set_markersize(8)
                else:
                    axCurves.text(xVals[indsnr], 0.9 * yLim[1-indType], 'ns', fontsize=8, va='center', ha='center', color=colours[indType], clip_on=False)
                    #extraplots.significance_stars(xVals[indsnr], starSide[indType] * 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3, color=colours[indType])

                if indType==1: #just so this shit doesn't get printed twice
                    pVal = stats.ranksums(correctedPVaccuraciesDiff[:, indBand, indsnr], correctedSOMaccuraciesDiff[:, indBand, indsnr])
                    print(f'PV vs SOM diff in accuracy at {band} octaves and {snr} SNR: {pVal}')

                    if pVal[1] < 0.05:
                        hs, = axCurves.plot(xVals[indsnr], 0, '*', mfc='k', mec='None', clip_on=False)
                        hs.set_markersize(8)
                    else:
                        axCurves.text(xVals[indsnr], 0, 'ns', fontsize=8, va='center', ha='center', color='k', clip_on=False)

        extraplots.boxoff(axCurves)
        extraplots.set_ticks_fontsize(axCurves, fontSizeTicks)

# --- merging all the tones together to compare no tone vs tone conditions ---
if PANELS[3]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    possibleSNRs = summaryData['possibleSNRs']
    possibleBands = summaryData['possibleBands']
    PVshape = [summaryData['PVtrialCounts'].shape[0], len(possibleBands), 2]
    SOMshape = [summaryData['SOMtrialCounts'].shape[0], len(possibleBands), 2]

    PVtrialCounts = summaryData['PVtrialCounts']
    SOMtrialCounts = summaryData['SOMtrialCounts']

    PVpsyCurves2 = np.zeros((PVshape[0], 2, len(possibleBands), 2))
    SOMpsyCurves2 = np.zeros((SOMshape[0], 2, len(possibleBands), 2))

    PVpsyCurves2[:, :, :, 0] = 100.0 * PVtrialCounts[:, :, :, 0, 1] / (PVtrialCounts[:, :, :, 0, 1] + PVtrialCounts[:, :, :, 0, 0])
    PVpsyCurves2[:, :, :, 1] = 100.0 * np.sum(PVtrialCounts[:, :, :, 1:, 0], axis=3) / (np.sum(PVtrialCounts[:, :, :, 1:, 1], axis=3) + np.sum(PVtrialCounts[:, :, :, 1:, 0], axis=3))

    SOMpsyCurves2[:, :, :, 0] = 100.0 * SOMtrialCounts[:, :, :, 0, 1] / (SOMtrialCounts[:, :, :, 0, 1] + SOMtrialCounts[:, :, :, 0, 0])
    SOMpsyCurves2[:, :, :, 1] = 100.0 * np.sum(SOMtrialCounts[:, :, :, 1:, 0], axis=3) / (np.sum(SOMtrialCounts[:, :, :, 1:, 1], axis=3) + np.sum(SOMtrialCounts[:, :, :, 1:, 0], axis=3))

    if CORRECTED:
        PVtrialCountsControl = summaryData['PVtrialCountsControl']
        SOMtrialCountsControl = summaryData['SOMtrialCountsControl']

        PVpsyCurvesControl = np.zeros((PVshape[0], 2, len(possibleBands), 2))
        SOMpsyCurvesControl = np.zeros((SOMshape[0], 2, len(possibleBands), 2))

        PVpsyCurvesControl[:, :, :, 0] = 100.0 * PVtrialCountsControl[:, :, :, 0, 1] / (PVtrialCountsControl[:, :, :, 0, 1] + PVtrialCountsControl[:, :, :, 0, 0])
        PVpsyCurvesControl[:, :, :, 1] = 100.0 * np.sum(PVtrialCountsControl[:, :, :, 1:, 0], axis=3) / (
                    np.sum(PVtrialCountsControl[:, :, :, 1:, 1], axis=3) + np.sum(PVtrialCountsControl[:, :, :, 1:, 0], axis=3))

        SOMpsyCurvesControl[:, :, :, 0] = 100.0 * SOMtrialCountsControl[:, :, :, 0, 1] / (SOMtrialCountsControl[:, :, :, 0, 1] + SOMtrialCountsControl[:, :, :, 0, 0])
        SOMpsyCurvesControl[:, :, :, 1] = 100.0 * np.sum(SOMtrialCountsControl[:, :, :, 1:, 0], axis=3) / (
                    np.sum(SOMtrialCountsControl[:, :, :, 1:, 1], axis=3) + np.sum(SOMtrialCountsControl[:, :, :, 1:, 0], axis=3))

        PVchangeControl = np.diff(PVpsyCurvesControl, axis=1).reshape(PVshape)
        SOMchangeControl = np.diff(SOMpsyCurvesControl, axis=1).reshape(SOMshape)

        PVchange = np.diff(PVpsyCurves2, axis=1).reshape(PVshape) - PVchangeControl
        SOMchange = np.diff(SOMpsyCurves2, axis=1).reshape(SOMshape) - SOMchangeControl
    else:
        PVchange = np.diff(PVpsyCurves2, axis=1).reshape(PVshape)
        SOMchange = np.diff(SOMpsyCurves2, axis=1).reshape(SOMshape)

    axCurves = gs[1, 2]
    gs2 = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=axCurves, wspace=0.3, hspace=0.4)

    changeData = [PVchange, SOMchange]
    colours = [PVColour, SOMColour]
    starSide = [1.0, -1.0]
    typeLabel = ['no PV', 'no SOM']

    xVals = range(2)
    xLabels = ['noise', 'tone']

    for indBand, band in enumerate(possibleBands):
        axChange = plt.subplot(gs[2, indBand])
        for indType, changes in enumerate(changeData):

            median = np.median(changes[:, indBand, :], axis=0)
            plt.plot(xVals, median, 'o-', color=colours[indType], lw=3, ms=9)

            if not CIS:
                for indMouse in range(changes.shape[0]):
                    plt.plot(xVals, changes[indMouse, indBand, :], '-', color=colours[indType], alpha=0.3)
            else:
                for indSNR in xVals:
                    CI = bf.bootstrap_median_CI(changes[:, indBand, indSNR])
                    # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
                    plt.plot([indSNR, indSNR], CI, color=colours[indType], linewidth=1.5)  # error bars
                    plt.plot([indSNR - 0.2, indSNR + 0.2], [CI[0], CI[0]], color=colours[indType],
                             linewidth=1.5)  # bottom caps
                    plt.plot([indSNR - 0.2, indSNR + 0.2], [CI[1], CI[1]], color=colours[indType],
                             linewidth=1.5)  # top caps

            plt.plot([-10, 10], [0, 0], '--', color='0.5')

            axChange.set_xlim(xVals[0] - 0.3, xVals[-1] + 0.3)
            axChange.set_xticks(xVals)
            axChange.set_xticklabels(xLabels)
            axChange.set_xlabel('SNR (dB)', fontsize=fontSizeLabels)

            yLim = [-40, 25]
            axChange.set_ylim(yLim)
            axChange.set_ylabel('Change in tone reported (%)', fontsize=fontSizeLabels)

            plt.title(f'{band} octaves')

            # stats
            for snr in xVals:
                pVal = stats.wilcoxon(changes[:, indBand, snr])
                print(f'{typeLabel[indType]} change in tone detect at {band} octaves and {xLabels[snr]} trials: {pVal}')

                if pVal[1] < 0.05:
                    hs, = axChange.plot(snr, 0.9 * yLim[1 - indType], '*', mfc=colours[indType], mec='None',
                                        clip_on=False)
                    hs.set_markersize(8)
                else:
                    axChange.text(snr, 0.9 * yLim[1 - indType], 'ns', fontsize=8, va='center', ha='center',
                                  color=colours[indType], clip_on=False)
                    # extraplots.significance_stars(xVals[indsnr], starSide[indType] * 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3, color=colours[indType])

                if indType == 1:  # just so this shit doesn't get printed twice
                    pVal = stats.ranksums(PVchange[:, indBand, snr],
                                          SOMchange[:, indBand, snr])
                    print(f'PV vs SOM diff in tone detect at {band} octaves and {xLabels[snr]} trials: {pVal}')

                    if pVal[1] < 0.05:
                        hs, = axChange.plot(snr, 0, '*', mfc='k', mec='None', clip_on=False)
                        hs.set_markersize(8)
                    else:
                        axChange.text(snr, 0, 'ns', fontsize=8, va='center', ha='center', color='k',
                                      clip_on=False)

        extraplots.boxoff(axChange)
        extraplots.set_ticks_fontsize(axChange, fontSizeTicks)





if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
