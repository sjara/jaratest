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

FIGNAME = 'figure_inhibitory_inactivation'
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
CORRECTED = 0
outputDir = '/tmp/'
if CORRECTED:
    figFilename = 'Fig3_inhib_inactivation_corrected_new'
else:
    figFilename = 'Fig3_inhib_inactivation_new'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [11,9]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.003, 0.39, 0.675]  # Horiz position for panel labels
labelPosY = [0.98, 0.64, 0.3]  # Vert position for panel labels

PVInactExample = 'band081_psycurve.npz'
SOMInactExample = 'band065_psycurve.npz'
summaryFileName = 'all_behaviour_inhib_inactivation_v2.npz'

baseColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']
controlColour = figparams.colp['control']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(3, 4, width_ratios=[1.5, 1, 1, 1])
gs.update(top=0.98, bottom=0.05, left=0.07, right=0.94, wspace=0.5, hspace=0.4)

def bootstrap_median_CI(data, reps=1000, interval=95):
    medians = np.zeros(reps)
    for ind in range(reps):
        samples = np.random.choice(data, len(data), replace=True)
        medians[ind] = np.median(samples)
    low = np.percentile(medians,(100-interval)/2.0)
    high = np.percentile(medians,interval+(100-interval)/2.0)
    return [low, high]

# --- example psychometric curves ---
if PANELS[0]:
    examples = [PVInactExample, SOMInactExample]
    cellTypeColours = [PVColour, SOMColour]
    labels = ['no PV', 'no SOM']
    panelLabels = ['A', 'D']

    for indType, exampleFileName in enumerate(examples):
        dataFullPath = os.path.join(inactDataDir, exampleFileName)
        data = np.load(dataFullPath)

        axCurve = plt.subplot(gs[indType, 0])

        psyCurveControl = data['psyCurveLaserInControl']
        upperErrorControl = data['upperErrorLaserInControl']
        lowerErrorControl = data['lowerErrorLaserInControl']
        possibleSNRs = data['possibleSNRs']

        xVals = range(len(possibleSNRs))
        plt.plot(xVals[:2], psyCurveControl[:2], 'o--', color=baseColour, lw=3, ms=8, zorder=10)
        l1, = plt.plot(xVals[1:], psyCurveControl[1:], 'o-', color=baseColour, lw=3, ms=8, zorder=10)
        #l1, = plt.plot(range(len(possibleSNRs)), psyCurveControl, 'o-', color=ExcColour, lw=3, ms=8)
        plt.errorbar(range(len(possibleSNRs)), psyCurveControl, yerr=[lowerErrorControl, upperErrorControl], fmt='none',
                     color=baseColour, lw=2, capsize=5, capthick=1)

        psyCurveLaser = data['psyCurveLaserIn']
        upperErrorLaser = data['upperErrorLaserIn']
        lowerErrorLaser = data['lowerErrorLaserIn']

        plt.plot(xVals[:2], psyCurveLaser[:2], 'o--', color=cellTypeColours[indType], mfc='white', lw=3, ms=8, zorder=10)
        l2, = plt.plot(xVals[1:], psyCurveLaser[1:], 'o-', color=cellTypeColours[indType], mfc='white', lw=3, ms=8, zorder=10)
        #l2, = plt.plot(range(len(possibleSNRs)), psyCurveLaser, 'o--', color=cellTypeColours[indType], mfc='white', lw=3, ms=8)
        plt.errorbar(range(len(possibleSNRs)), psyCurveLaser, yerr=[lowerErrorLaser, upperErrorLaser], fmt='none',
                     color=cellTypeColours[indType], lw=2, capsize=5, capthick=1, zorder=-10)

        psyCurveLaserOut = data['psyCurveLaserOut']
        upperErrorLaserOut = data['upperErrorLaserOut']
        lowerErrorLaserOut = data['lowerErrorLaserOut']

        plt.plot(xVals[:2], psyCurveLaserOut[:2], 'o--', color=controlColour, mfc='white', lw=3, ms=8, zorder=10)
        l3, = plt.plot(xVals[1:], psyCurveLaserOut[1:], 'o-', color=controlColour, mfc='white', lw=3, ms=8, zorder=10)
        # l2, = plt.plot(range(len(possibleSNRs)), psyCurveLaser, 'o--', color=cellTypeColours[indType], mfc='white', lw=3, ms=8)
        plt.errorbar(range(len(possibleSNRs)), psyCurveLaserOut, yerr=[lowerErrorLaserOut, upperErrorLaserOut], fmt='none',
                     color=controlColour, lw=2, capsize=5, capthick=1, zorder=-10)

        axCurve.legend([l1, l2, l3], ['no laser', labels[indType], 'laser out'])

        axCurve.set_xlim(-0.2, len(possibleSNRs) - 0.8)
        axCurve.set_xticks(range(len(possibleSNRs)))
        xTickLabels = ['-inf']
        xTickLabels.extend([int(x) for x in possibleSNRs.tolist()[1:]])
        axCurve.set_xticklabels(xTickLabels)
        axCurve.set_xlabel('SNR (dB)', fontsize=fontSizeLabels)

        axCurve.set_ylim(0, 100)
        axCurve.set_ylabel('Trials with tone reported (%)', fontsize=fontSizeLabels)

        extraplots.boxoff(axCurve)
        extraplots.breakaxis(0.5, 0, 0.15, 5, gap=0.5)
        extraplots.set_ticks_fontsize(axCurve, fontSizeTicks)

    for indLabel, label in enumerate(panelLabels):
        axCurve.annotate(label, xy=(labelPosX[0], labelPosY[indLabel]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

# --- summary of change in d prime during PV or SOM inactivation ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserdprime = summaryData['PVexpLaserdprime']
    PVnoLaserdprime = summaryData['PVexpNoLaserdprime']
    SOMlaserdprime = summaryData['SOMexpLaserdprime']
    SOMnoLaserdprime = summaryData['SOMexpNoLaserdprime']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        PVlaserdprimeControl = summaryData['PVcontrolLaserdprime']
        PVnoLaserdprimeControl = summaryData['PVcontrolNoLaserdprime']
        SOMlaserdprimeControl = summaryData['SOMcontrolLaserdprime']
        SOMnoLaserdprimeControl = summaryData['SOMcontrolNoLaserdprime']

        PVcontrolLaserdprimeCorrected = PVlaserdprime - (PVlaserdprimeControl - PVnoLaserdprimeControl)
        SOMlaserdprimeCorrected = SOMlaserdprime - (SOMlaserdprimeControl - SOMnoLaserdprimeControl)

        dprimeData = [[PVnoLaserdprime, PVcontrolLaserdprimeCorrected], [SOMnoLaserdprime, SOMlaserdprimeCorrected]]

    else:
        dprimeData = [[PVnoLaserdprime, PVlaserdprime], [SOMnoLaserdprime, SOMlaserdprime]]

    panelLabels = ['B', 'E']
    colours = [PVColour, SOMColour]
    yLim = [0,2]

    for indType, dprimes in enumerate(dprimeData):
        axScatter = plt.subplot(gs[indType,1])

        barLoc = np.array([-0.24, 0.24])
        xLocs = np.arange(2)
        xTickLabels = possibleBands

        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(dprimes[0].shape[0]):
                plt.plot(thisxLocs, [dprimes[0][indMouse, indBand], dprimes[1][indMouse, indBand]], '-', color=baseColour)

            plt.plot(np.tile(thisxLocs[0],dprimes[0].shape[0]), dprimes[0][:,indBand], 'o', color=baseColour)
            plt.plot(np.tile(thisxLocs[1],dprimes[1].shape[0]), dprimes[1][:,indBand], 'o', mec=colours[indType], mfc='white')

            #median = np.median(accuracyData, axis=0)
            #plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')

            pVal = stats.wilcoxon(dprimes[1][:,indBand], dprimes[0][:,indBand])[1]
            print(f"Change in d\' pVal at {possibleBands[indBand]} octaves: {pVal}")

            if pVal < 0.05:
                extraplots.significance_stars(thisxLocs, 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3)

        axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axScatter.set_xticks(xLocs)
        xTickLabels = possibleBands.tolist()
        xTickLabels[-1] = 'WN'
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(xTickLabels)
        axScatter.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

        axScatter.set_ylim(yLim)
        axScatter.set_ylabel('d\'', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[1], labelPosY[indLabel]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

# --- comparison in change in d prime with PV and SOM inactivation ---
if PANELS[2]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserdprime = summaryData['PVexpLaserdprime']
    PVnoLaserdprime = summaryData['PVexpNoLaserdprime']
    SOMlaserdprime = summaryData['SOMexpLaserdprime']
    SOMnoLaserdprime = summaryData['SOMexpNoLaserdprime']
    possibleBands = summaryData['possibleBands']

    PVchange = PVlaserdprime - PVnoLaserdprime
    SOMchange = SOMlaserdprime - SOMnoLaserdprime

    if CORRECTED:
        PVlaserdprimeControl = summaryData['PVcontrolLaserdprime']
        PVnoLaserdprimeControl = summaryData['PVcontrolNoLaserdprime']
        SOMlaserdprimeControl = summaryData['SOMcontrolLaserdprime']
        SOMnoLaserdprimeControl = summaryData['SOMcontrolNoLaserdprime']

        controlPVchange = PVlaserdprimeControl - PVnoLaserdprimeControl
        controlSOMchange = SOMlaserdprimeControl - SOMnoLaserdprimeControl

        correctedPVchange = PVchange - controlPVchange
        correctedSOMchange = SOMchange - controlSOMchange

        changedprime = [correctedPVchange, correctedSOMchange]
        medianChangedprime = [np.median(correctedPVchange, axis=0), np.median(correctedSOMchange, axis=0)]
    else:
        changedprime = [PVchange, SOMchange]
        medianChangedprime = [np.median(PVchange, axis=0), np.median(SOMchange, axis=0)]

    axBar = plt.subplot(gs[2,1])
    cartoonLabel = 'G'
    panelLabel = 'H'

    cellTypeColours = [PVColour, SOMColour]

    width = 0.3
    barLoc = np.array([-0.18, 0.18])
    xLocs = np.arange(2)
    xTickLabels = possibleBands
    yLims = (-0.6, 0.2)

    #changeCIs = [bootstrap_median_CI(PVchange), bootstrap_median_CI(SOMchange)]
    for indBand in range(len(possibleBands)):
        for indType in range(len(medianChangedprime)):
            jitter = 0.8 * width * (np.random.random(len(changedprime[indType])) - 0.5)
            plt.plot(np.tile(xLocs[indBand] + barLoc[indType], len(changedprime[indType])) + jitter,
                     changedprime[indType][:, indBand], 'o', mec=cellTypeColours[indType], mfc='white')

            plt.plot([xLocs[indBand] + barLoc[indType] - width / 2, xLocs[indBand] + barLoc[indType] + width / 2],
                     [medianChangedprime[indType][indBand], medianChangedprime[indType][indBand]],
                     color='k', linewidth=3, zorder=10)  # medians

            dprimeCI = bootstrap_median_CI(changedprime[indType][:,indBand])
            # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
            plt.plot([xLocs[indBand] + barLoc[indType], xLocs[indBand] + barLoc[indType]], dprimeCI,
                     color='k', linewidth=1.5)  # error bars
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                     [dprimeCI[0], dprimeCI[0]], color='k', linewidth=1.5)  # bottom caps
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                     [dprimeCI[1], dprimeCI[1]], color='k', linewidth=1.5)  # top caps

        pVal = stats.ranksums(changedprime[0][:, indBand], changedprime[1][:, indBand])[1]
        print(f'PV d\' change vs SOM d\' change for bw {possibleBands[indBand]} p val: {pVal}')

        if pVal < 0.05:
            extraplots.significance_stars(xLocs[indBand], 0.98 * yLims[1], 0.02 * np.diff(yLims), gapFactor=0.3)

    plt.plot([-10, 10], [0, 0], '--', color='0.5', zorder=0)  # line at 0 indicating direction of change

    axBar.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[1] + barLoc[1] + 0.3)
    axBar.set_xticks(xLocs)
    xTickLabels = possibleBands.tolist()
    xTickLabels[-1] = 'WN'
    axBar.set_xticks(xLocs)
    axBar.set_xticklabels(xTickLabels)
    axBar.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

    axBar.set_ylim(yLims)
    axBar.set_ylabel('Change in d\'', fontsize=fontSizeLabels)

    extraplots.boxoff(axBar)
    extraplots.set_ticks_fontsize(axBar, fontSizeTicks)

    axBar.annotate(panelLabel, xy=(labelPosX[1], labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel,
                     fontweight='bold')
    axBar.annotate(cartoonLabel, xy=(labelPosX[0], labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel,
                   fontweight='bold')

# --- comparison in change in hits with PV and SOM inactivation ---
if PANELS[3]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserHits = summaryData['PVexpLaserHits']
    PVnoLaserHits = summaryData['PVexpNoLaserHits']
    SOMlaserHits = summaryData['SOMexpLaserHits']
    SOMnoLaserHits = summaryData['SOMexpNoLaserHits']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        PVlaserHitsControl = summaryData['PVcontrolLaserHits']
        PVnoLaserHitsControl = summaryData['PVcontrolNoLaserHits']
        SOMlaserHitsControl = summaryData['SOMcontrolLaserHits']
        SOMnoLaserHitsControl = summaryData['SOMcontrolNoLaserHits']

        PVlaserHitsCorrected = PVlaserHits - (PVlaserHitsControl - PVnoLaserHitsControl)
        SOMlaserHitsCorrected = SOMlaserHits - (SOMlaserHitsControl - SOMnoLaserHitsControl)

        hitsData = [[PVnoLaserHits, PVlaserHitsCorrected], [SOMnoLaserHits, SOMlaserHitsCorrected]]

    else:
        hitsData = [[PVnoLaserHits, PVlaserHits], [SOMnoLaserHits, SOMlaserHits]]

    panelLabels = ['C', 'F']
    colours = [PVColour, SOMColour]
    yLims = [(0,1.0),(0,1.0)]
    legendLabels = ['no PV', 'no SOM']

    for indType, hits in enumerate(hitsData):
        axScatter = plt.subplot(gs[indType, 2])

        barLoc = np.array([-0.24, 0.24])
        xLocs = np.arange(2)
        xTickLabels = possibleBands

        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(hits[0].shape[0]):
                plt.plot(thisxLocs, [hits[0][indMouse, indBand], hits[1][indMouse, indBand]], '-',
                         color=baseColour)

            plt.plot(np.tile(thisxLocs[0], hits[0].shape[0]), hits[0][:, indBand], 'o', color=baseColour)
            plt.plot(np.tile(thisxLocs[1], hits[1].shape[0]), hits[1][:, indBand], 'o',
                     mec=colours[indType], mfc='white')

            # median = np.median(accuracyData, axis=0)
            # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')

            # calculate those stats!
            pVal = stats.wilcoxon(hits[0][:, indBand], hits[1][:, indBand])
            print(f'{legendLabels[indType]} hit rate change for bw {possibleBands[indBand]} p val: {pVal}')

            if pVal[1] < 0.05:
                extraplots.significance_stars(thisxLocs, yLims[indType][1] * 1.03, yLims[indType][1] * 0.02, gapFactor=0.25)

        axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axScatter.set_xticks(xLocs)
        xTickLabels = possibleBands.tolist()
        xTickLabels[-1] = 'WN'
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(xTickLabels)
        axScatter.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

        axScatter.set_ylim(yLims[indType])
        axScatter.set_ylabel('Hit Rate', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[2], labelPosY[indLabel]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

# --- summary of change in bias towards one side during PV or SOM inactivation ---
if PANELS[4]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserHits = summaryData['PVexpLaserHits']
    PVnoLaserHits = summaryData['PVexpNoLaserHits']
    SOMlaserHits = summaryData['SOMexpLaserHits']
    SOMnoLaserHits = summaryData['SOMexpNoLaserHits']
    possibleBands = summaryData['possibleBands']

    PVchange = PVlaserHits - PVnoLaserHits
    SOMchange = SOMlaserHits - SOMnoLaserHits

    if CORRECTED:
        PVlaserHitsControl = summaryData['PVcontrolLaserHits']
        PVnoLaserHitsControl = summaryData['PVcontrolNoLaserHits']
        SOMlaserHitsControl = summaryData['SOMcontrolLaserHits']
        SOMnoLaserHitsControl = summaryData['SOMcontrolNoLaserHits']

        controlPVchange = PVlaserHitsControl - PVnoLaserHitsControl
        controlSOMchange = SOMlaserHitsControl - SOMnoLaserHitsControl

        correctedPVchange = PVchange - controlPVchange
        correctedSOMchange = SOMchange - controlSOMchange

        changeHits = [correctedPVchange, correctedSOMchange]
        medianChangeHits = [np.median(correctedPVchange, axis=0), np.median(correctedSOMchange, axis=0)]

    else:
        changeHits = [PVchange, SOMchange]
        medianChangeHits = [np.median(PVchange, axis=0), np.median(SOMchange, axis=0)]

    axBar = plt.subplot(gs[2,2])

    cellTypeColours = [PVColour, SOMColour]
    panelLabel = 'I'
    width = 0.3
    barLoc = np.array([-0.18, 0.18])
    xLocs = np.arange(2)

    for indBand in range(len(possibleBands)):
        for indType in range(len(medianChangeHits)):
            jitter = 0.8*width*(np.random.random(len(changeHits[indType]))-0.5)
            plt.plot(np.tile(xLocs[indBand]+barLoc[indType], len(changeHits[indType]))+jitter, changeHits[indType][:,indBand],
                     'o', mec=cellTypeColours[indType], mfc='white')
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 2, xLocs[indBand] + barLoc[indType] + width / 2],
                     [medianChangeHits[indType][indBand], medianChangeHits[indType][indBand]],
                     color='k', linewidth=3, zorder=10)  # medians

            hitsCI = bootstrap_median_CI(changeHits[indType][:, indBand])
            # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
            plt.plot([xLocs[indBand] + barLoc[indType], xLocs[indBand] + barLoc[indType]], hitsCI,
                     color='k', linewidth=1.5)  # error bars
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                     [hitsCI[0], hitsCI[0]], color='k', linewidth=1.5)  # bottom caps
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                     [hitsCI[1], hitsCI[1]], color='k', linewidth=1.5)  # top caps
    plt.plot([-10,10], [0,0], '--', color='0.5', zorder=0) # line at 0 indicating direction of change

    axBar.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[1] + barLoc[1] + 0.3)
    axBar.set_xticks(xLocs)
    xTickLabels = possibleBands.tolist()
    xTickLabels[-1] = 'WN'
    axBar.set_xticks(xLocs)
    axBar.set_xticklabels(xTickLabels)
    axBar.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

    yLims = (-0.5, 0.1)
    axBar.set_ylim(yLims)
    axBar.set_ylabel('Change in Hit Rate', fontsize=fontSizeLabels)

    extraplots.boxoff(axBar)
    extraplots.set_ticks_fontsize(axBar, fontSizeTicks)

    axBar.annotate(panelLabel, xy=(labelPosX[2], labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel,
                   fontweight='bold')

    # calculate those stats!
    for band in range(len(possibleBands)):
        pVal = stats.ranksums(changeHits[0][:,band], changeHits[1][:,band])
        print(f'PV hit rate change vs SOM hit rate change for bw {possibleBands[band]} p val: {pVal}')

        if pVal[1] < 0.05:
            extraplots.significance_stars(barLoc + xLocs[band], yLims[1] * 1.03, yLims[1] * 0.02, gapFactor=0.25)

# --- comparison in change in false alarms with PV and SOM inactivation ---
if PANELS[5]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserFAs = summaryData['PVexpLaserFA']
    PVnoLaserFAs = summaryData['PVexpNoLaserFA']
    SOMlaserFAs = summaryData['SOMexpLaserFA']
    SOMnoLaserFAs = summaryData['SOMexpNoLaserFA']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        controlPVlaserFAs = summaryData['PVcontrolLaserFA']
        controlPVnoLaserFAs = summaryData['PVcontrolNoLaserFA']
        controlSOMlaserFAs = summaryData['SOMcontrolLaserFA']
        controlSOMnoLaserFAs = summaryData['SOMcontrolNoLaserFA']

        PVlaserFAsCorrected = PVlaserFAs - (controlPVlaserFAs - controlPVnoLaserFAs)
        SOMlaserFAsCorrected = SOMlaserFAs - (controlSOMlaserFAs - controlSOMnoLaserFAs)

        FAdata = [[PVnoLaserFAs, PVlaserFAsCorrected], [SOMnoLaserFAs, SOMlaserFAsCorrected]]

    else:
        FAdata = [[PVnoLaserFAs, PVlaserFAs], [SOMnoLaserFAs, SOMlaserFAs]]

    panelLabels = ['C', 'F']
    colours = [PVColour, SOMColour]
    yLims = [(0,1.0),(0,1.0)]
    legendLabels = ['no PV', 'no SOM']

    for indType, FAs in enumerate(FAdata):
        axScatter = plt.subplot(gs[indType, 3])

        barLoc = np.array([-0.24, 0.24])
        xLocs = np.arange(2)
        xTickLabels = possibleBands

        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(FAs[0].shape[0]):
                plt.plot(thisxLocs, [FAs[0][indMouse, indBand], FAs[1][indMouse, indBand]], '-',
                         color=baseColour)

            plt.plot(np.tile(thisxLocs[0], FAs[0].shape[0]), FAs[0][:, indBand], 'o', color=baseColour)
            plt.plot(np.tile(thisxLocs[1], FAs[1].shape[0]), FAs[1][:, indBand], 'o',
                     mec=colours[indType], mfc='white')

            # median = np.median(accuracyData, axis=0)
            # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')

            # calculate those stats!
            pVal = stats.wilcoxon(FAs[0][:, indBand], FAs[1][:, indBand])
            print(f'{legendLabels[indType]} false alarm rate change for bw {possibleBands[indBand]} p val: {pVal}')

            if pVal[1] < 0.05:
                extraplots.significance_stars(thisxLocs, yLims[indType][1] * 1.03, yLims[indType][1] * 0.02, gapFactor=0.25)

        axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axScatter.set_xticks(xLocs)
        xTickLabels = possibleBands.tolist()
        xTickLabels[-1] = 'WN'
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(xTickLabels)
        axScatter.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

        axScatter.set_ylim(yLims[indType])
        axScatter.set_ylabel('False Alarm Rate', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[2], labelPosY[indLabel]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

# --- summary of change in false alarms during PV or SOM inactivation ---
if PANELS[6]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserFAs = summaryData['PVexpLaserFA']
    PVnoLaserFAs = summaryData['PVexpNoLaserFA']
    SOMlaserFAs = summaryData['SOMexpLaserFA']
    SOMnoLaserFAs = summaryData['SOMexpNoLaserFA']
    possibleBands = summaryData['possibleBands']

    PVchange = PVlaserFAs - PVnoLaserFAs
    SOMchange = SOMlaserFAs - SOMnoLaserFAs

    if CORRECTED:
        controlPVlaserFAs = summaryData['PVcontrolLaserFA']
        controlPVnoLaserFAs = summaryData['PVcontrolNoLaserFA']
        controlSOMlaserFAs = summaryData['SOMcontrolLaserFA']
        controlSOMnoLaserFAs = summaryData['SOMcontrolNoLaserFA']

        controlPVchange = controlPVlaserFAs - controlPVnoLaserFAs
        controlSOMchange = controlSOMlaserFAs - controlSOMnoLaserFAs

        correctedPVchange = PVchange - controlPVchange
        correctedSOMchange = SOMchange - controlSOMchange

        changeFAs = [correctedPVchange, correctedSOMchange]
        medianChangeFAs = [np.median(correctedPVchange, axis=0), np.median(correctedSOMchange, axis=0)]

    else:
        changeFAs = [PVchange, SOMchange]
        medianChangeFAs = [np.median(PVchange, axis=0), np.median(SOMchange, axis=0)]

    axBar = plt.subplot(gs[2,3])

    cellTypeColours = [PVColour, SOMColour]
    panelLabel = 'I'
    width = 0.3
    barLoc = np.array([-0.18, 0.18])
    xLocs = np.arange(2)

    for indBand in range(len(possibleBands)):
        for indType in range(len(medianChangeFAs)):
            jitter = 0.8*width*(np.random.random(len(changeFAs[indType]))-0.5)
            plt.plot(np.tile(xLocs[indBand]+barLoc[indType], len(changeFAs[indType]))+jitter, changeFAs[indType][:,indBand],
                     'o', mec=cellTypeColours[indType], mfc='white')
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 2, xLocs[indBand] + barLoc[indType] + width / 2],
                     [medianChangeFAs[indType][indBand], medianChangeFAs[indType][indBand]],
                     color='k', linewidth=3, zorder=10)  # medians

            FACI = bootstrap_median_CI(changeFAs[indType][:, indBand])
            # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
            plt.plot([xLocs[indBand] + barLoc[indType], xLocs[indBand] + barLoc[indType]], FACI,
                     color='k', linewidth=1.5)  # error bars
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                     [FACI[0], FACI[0]], color='k', linewidth=1.5)  # bottom caps
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                     [FACI[1], FACI[1]], color='k', linewidth=1.5)  # top caps
    plt.plot([-10,10], [0,0], '--', color='0.5', zorder=0) # line at 0 indicating direction of change

    axBar.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[1] + barLoc[1] + 0.3)
    axBar.set_xticks(xLocs)
    xTickLabels = possibleBands.tolist()
    xTickLabels[-1] = 'WN'
    axBar.set_xticks(xLocs)
    axBar.set_xticklabels(xTickLabels)
    axBar.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

    yLims = (-0.5, 0.1)
    axBar.set_ylim(yLims)
    axBar.set_ylabel('Change in False Alarm Rate', fontsize=fontSizeLabels)

    extraplots.boxoff(axBar)
    extraplots.set_ticks_fontsize(axBar, fontSizeTicks)

    axBar.annotate(panelLabel, xy=(labelPosX[2], labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel,
                   fontweight='bold')

    # calculate those stats!
    for band in range(len(possibleBands)):
        pVal = stats.ranksums(changeFAs[0][:,band], changeFAs[1][:,band])
        print(f'PV vs SOM false alarm rate change for bw {possibleBands[band]} p val: {pVal}')

        if pVal[1] < 0.05:
            extraplots.significance_stars(barLoc + xLocs[band], yLims[1] * 1.03, yLims[1] * 0.02, gapFactor=0.25)

if CORRECTED:
    plt.suptitle('LASER EFFECT CORRECTION')
else:
    plt.suptitle('NO CORRECTION')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
