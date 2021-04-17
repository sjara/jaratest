import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots

import behaviour_analysis_funcs as funcs
import figparams
import studyparams

FIGNAME = 'figure_inhibitory_inactivation'
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 0, 1, 1, 0, 1, 1, 0]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
CORRECTED = 0
SIG_CONTROL_REMOVED = 0
outputDir = '/tmp/'
figFilename = 'Fig4_inhib_inactivation_new2'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [6.9,6.5]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.003, 0.31, 0.51, 0.72]  # Horiz position for panel labels
labelPosY = [0.97, 0.69, 0.59, 0.25]  # Vert position for panel labels

PVInactExample = 'band081_psycurve.npz'
SOMInactExample = 'band065_psycurve.npz'
summaryFileName = 'all_behaviour_inhib_inactivation_v2.npz'

baseColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']
controlColour = figparams.colp['control']
connectLineColour = figparams.colp['connectLine']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(4, 4, width_ratios=[1.7, 1, 1, 1], height_ratios=[1,0.5,1,0.5])
gs.update(top=0.98, bottom=0.08, left=0.08, right=0.94, wspace=0.6, hspace=0.4)

def bootstrap_median_CI(data, reps=1000, interval=95):
    medians = np.zeros(reps)
    for ind in range(reps):
        samples = np.random.choice(data, len(data), replace=True)
        medians[ind] = np.median(samples)
    low = np.percentile(medians,(100-interval)/2.0)
    high = np.percentile(medians,interval+(100-interval)/2.0)
    return [low, high]

def plot_laser_comparison(axes, data, laserColour, yLim):
    barLoc = np.array([-0.24, 0.24])

    for indMouse in range(data[0].shape[0]):
        plt.plot(barLoc, [data[0][indMouse], data[1][indMouse]], '-', color=connectLineColour)

    plt.plot(np.tile(barLoc[0], data[0].shape[0]), data[0], 'o', color=baseColour)
    plt.plot(np.tile(barLoc[1], data[1].shape[0]), data[1], 'o', mec=laserColour, mfc='white')

    # median = np.median(accuracyData, axis=0)
    # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')

    axes.set_xlim(barLoc[0] - 0.3, barLoc[1] + 0.3)
    axes.set_xticks(barLoc)
    axes.set_ylim(yLim)

    extraplots.boxoff(axes)

    pVal = stats.wilcoxon(data[1], data[0])[1]
    print(f"Change in pVal: {pVal}")

    if pVal < 0.05:
        extraplots.significance_stars(barLoc, 0.98 * np.diff(yLim), 0.02 * np.diff(yLim), gapFactor=0.3)

def plot_cell_type_comparison(axes, data, colours, yLim, facecolours=None):
    width = 0.3
    barLoc = np.array([-0.18, 0.18])

    for indType in range(len(data)):
        if facecolours is None:
            facecolours = np.tile('white', len(data))
        jitter = 0.8 * width * (np.random.random(len(data[indType])) - 0.5)
        plt.scatter(np.tile(barLoc[indType], len(data[indType])) + jitter, data[indType], edgecolors=colours[indType], facecolors=facecolours[indType])

        plt.plot([barLoc[indType] - width / 2, barLoc[indType] + width / 2], [np.median(data[indType]), np.median(data[indType])],
                 color='k', linewidth=4, zorder=10)  # medians

        CI = bootstrap_median_CI(data[indType])
        # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
        plt.plot([barLoc[indType], barLoc[indType]], CI, color='k', linewidth=2)  # error bars
        plt.plot([barLoc[indType] - width / 8, barLoc[indType] + width / 8], [CI[0], CI[0]], color='k', linewidth=2)  # bottom caps
        plt.plot([barLoc[indType] - width / 8, barLoc[indType] + width / 8], [CI[1], CI[1]], color='k', linewidth=2)  # top caps

    pVal = stats.ranksums(data[0], data[1])[1]
    print(f'PV change vs SOM change p val: {pVal}')

    if pVal < 0.05:
        extraplots.significance_stars(xLocs[indBand], 0.98 * np.diff(yLim), 0.02 * np.diff(yLim), gapFactor=0.3)

    plt.plot([-10, 10], [0, 0], '--', color='0.5', zorder=0)  # line at 0 indicating direction of change

    axes.set_xlim(barLoc[0] - 0.3, barLoc[1] + 0.3)
    axes.set_xticks(barLoc)
    axes.set_ylim(yLim)

    extraplots.boxoff(axes)

def plot_exp_vs_control_scatter(axes, xData, yData, colours, xLim, yLim, facecolours='none'):
    plt.scatter(xData, yData, edgecolors=colours, facecolors=facecolours)

    plt.plot([-100, 100], [0, 0], ':', c='0.5', zorder=-10)
    plt.plot([0, 0], [-100, 100], ':', c='0.5', zorder=-10)
    plt.plot([-100, 100], [-100, 100], ':', c='0.5', zorder=-10)

    axes.set_xlim(xLim)
    axes.set_ylim(yLim)
    axes.set(adjustable='box', aspect='equal')
    extraplots.boxoff(axes)
    extraplots.set_ticks_fontsize(axes, fontSizeTicks)

# --- example psychometric curves ---
if PANELS[0]:
    examples = [PVInactExample, SOMInactExample]
    cellTypeColours = [PVColour, SOMColour]
    labels = ['no PV', 'no SOM']
    panelLabels = ['A', 'E']

    for indType, exampleFileName in enumerate(examples):
        dataFullPath = os.path.join(inactDataDir, exampleFileName)
        data = np.load(dataFullPath)

        axCurve = plt.subplot(gs[indType*2:indType*2+2, 0])

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

    PVlaserdprime = summaryData['PVexpLaserdprimeAllBands']
    PVnoLaserdprime = summaryData['PVexpNoLaserdprimeAllBands']
    SOMlaserdprime = summaryData['SOMexpLaserdprimeAllBands']
    SOMnoLaserdprime = summaryData['SOMexpNoLaserdprimeAllBands']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        PVlaserdprimeControl = summaryData['PVcontrolLaserdprimeAllBands']
        PVnoLaserdprimeControl = summaryData['PVcontrolNoLaserdprimeAllBands']
        SOMlaserdprimeControl = summaryData['SOMcontrolLaserdprimeAllBands']
        SOMnoLaserdprimeControl = summaryData['SOMcontrolNoLaserdprimeAllBands']

        PVcontrolLaserdprimeCorrected = PVlaserdprime - (PVlaserdprimeControl - PVnoLaserdprimeControl)
        SOMlaserdprimeCorrected = SOMlaserdprime - (SOMlaserdprimeControl - SOMnoLaserdprimeControl)

        dprimeData = [[PVnoLaserdprime, PVcontrolLaserdprimeCorrected], [SOMnoLaserdprime, SOMlaserdprimeCorrected]]

    else:
        dprimeData = [[PVnoLaserdprime, PVlaserdprime], [SOMnoLaserdprime, SOMlaserdprime]]

    if SIG_CONTROL_REMOVED:
        PVcontrolpVal = summaryData['PVcontrolpValAllBand']
        SOMcontrolpVal = summaryData['SOMcontrolpValAllBand']

        dprimeData[0][0] = dprimeData[0][0][PVcontrolpVal > 0.05]
        dprimeData[0][1] = dprimeData[0][1][PVcontrolpVal > 0.05]
        dprimeData[1][0] = dprimeData[1][0][SOMcontrolpVal > 0.05]
        dprimeData[1][1] = dprimeData[1][1][SOMcontrolpVal > 0.05]

    panelLabels = ['B', 'F']
    colours = [PVColour, SOMColour]
    xTickLabels = ['no PV', 'no SOM']
    yLims = [[0,2.3], [0, 1.8]]

    for indType in range(2):
        axScatter = plt.subplot(gs[indType*2,1])
        plot_laser_comparison(axScatter, dprimeData[indType], colours[indType], yLims[indType])

        axScatter.set_xticklabels(['baseline', xTickLabels[indType]])
        axScatter.set_ylabel('d\'', fontsize=fontSizeLabels)

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[1], labelPosY[indLabel]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

# --- comparison in change in d prime with laser in vs laser out
if PANELS[2]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserdprime = summaryData['PVexpLaserdprimeAllBands']
    PVnoLaserdprime = summaryData['PVexpNoLaserdprimeAllBands']
    SOMlaserdprime = summaryData['SOMexpLaserdprimeAllBands']
    SOMnoLaserdprime = summaryData['SOMexpNoLaserdprimeAllBands']

    PVchange = PVlaserdprime - PVnoLaserdprime
    SOMchange = SOMlaserdprime - SOMnoLaserdprime

    PVlaserdprimeControl = summaryData['PVcontrolLaserdprimeAllBands']
    PVnoLaserdprimeControl = summaryData['PVcontrolNoLaserdprimeAllBands']
    SOMlaserdprimeControl = summaryData['SOMcontrolLaserdprimeAllBands']
    SOMnoLaserdprimeControl = summaryData['SOMcontrolNoLaserdprimeAllBands']

    controlPVchange = PVlaserdprimeControl - PVnoLaserdprimeControl
    controlSOMchange = SOMlaserdprimeControl - SOMnoLaserdprimeControl

    PVeffectpVals = summaryData['PVcontrolvsexppValAllBands']
    PVlaserpVals = summaryData['PVexppValAllBand']
    PVsigMice = (PVeffectpVals<0.05) & (PVlaserpVals<0.05)

    SOMeffectpVals = summaryData['SOMcontrolvsexppValAllBands']
    SOMlaserpVals = summaryData['SOMexppValAllBand']
    SOMsigMice = (SOMeffectpVals < 0.05) & (SOMlaserpVals < 0.05)

    PVfacecolours = [PVColour if val else 'none' for val in PVsigMice]
    PVfacecolours = funcs.list_colours_to_rgba(PVfacecolours)
    SOMfacecolours = [SOMColour if val else 'none' for val in SOMsigMice]
    SOMfacecolours = funcs.list_colours_to_rgba(SOMfacecolours)

    panelLabels = ['B', 'F']
    colours = [PVColour, SOMColour]
    facecolours = [PVfacecolours, SOMfacecolours]
    xTickLabels = ['no PV', 'no SOM']
    xLims = [[-0.5, 0.5], [-0.5, 0.3]]
    yLims = [[-0.7, 0.3], [-0.7, 0.1]]

    expChange = [PVchange, SOMchange]
    controlChange = [controlPVchange, controlSOMchange]

    for indType in range(2):
        axScatter = plt.subplot(gs[indType*2+1, 1])
        plot_exp_vs_control_scatter(axScatter, controlChange[indType], expChange[indType], colours[indType], xLims[indType], yLims[indType], facecolours[indType])

        axScatter.set_xlabel(r'laser-out $\Delta$ d$^\prime$', fontsize=fontSizeLabels)
        axScatter.set_ylabel(r'laser-in $\Delta$ d$^\prime$', fontsize=fontSizeLabels)

        # -- linear regression --
        slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange[indType], expChange[indType])

        print(f'Laser in vs. out d\' change for {xTickLabels[indType]}: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[1], labelPosY[indLabel]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

# --- comparison in change in d prime with PV and SOM inactivation ---
if PANELS[3]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserdprime = summaryData['PVexpLaserdprimeAllBands']
    PVnoLaserdprime = summaryData['PVexpNoLaserdprimeAllBands']
    SOMlaserdprime = summaryData['SOMexpLaserdprimeAllBands']
    SOMnoLaserdprime = summaryData['SOMexpNoLaserdprimeAllBands']
    possibleBands = summaryData['possibleBands']

    PVeffectpVals = summaryData['PVcontrolvsexppValAllBands']
    PVlaserpVals = summaryData['PVexppValAllBand']
    PVsigMice = (PVeffectpVals < 0.05) & (PVlaserpVals < 0.05)

    SOMeffectpVals = summaryData['SOMcontrolvsexppValAllBands']
    SOMlaserpVals = summaryData['SOMexppValAllBand']
    SOMsigMice = (SOMeffectpVals < 0.05) & (SOMlaserpVals < 0.05)

    PVchange = PVlaserdprime - PVnoLaserdprime
    SOMchange = SOMlaserdprime - SOMnoLaserdprime

    if CORRECTED:
        PVlaserdprimeControl = summaryData['PVcontrolLaserdprimeAllBands']
        PVnoLaserdprimeControl = summaryData['PVcontrolNoLaserdprimeAllBands']
        SOMlaserdprimeControl = summaryData['SOMcontrolLaserdprimeAllBands']
        SOMnoLaserdprimeControl = summaryData['SOMcontrolNoLaserdprimeAllBands']

        controlPVchange = PVlaserdprimeControl - PVnoLaserdprimeControl
        controlSOMchange = SOMlaserdprimeControl - SOMnoLaserdprimeControl

        correctedPVchange = PVchange - controlPVchange
        correctedSOMchange = SOMchange - controlSOMchange

        changedprime = [correctedPVchange, correctedSOMchange]
    else:
        changedprime = [PVchange, SOMchange]

    if SIG_CONTROL_REMOVED:
        PVcontrolpVal = summaryData['PVcontrolpValAllBand']
        SOMcontrolpVal = summaryData['SOMcontrolpValAllBand']

        changedprime[0] = changedprime[0][PVcontrolpVal > 0.05]
        changedprime[1] = changedprime[1][SOMcontrolpVal > 0.05]

    axBar = plt.subplot(gs[4,1])
    cartoonLabel = 'I'
    panelLabel = 'J'

    cellTypeColours = [PVColour, SOMColour]
    xTickLabels = ['no PV', 'no SOM']
    yLims = (-0.6, 0.2)

    # PVfacecolours = [PVColour if val else 'white' for val in PVsigMice]
    # PVfacecolours = funcs.list_colours_to_rgba(PVfacecolours)
    # SOMfacecolours = [SOMColour if val else 'white' for val in SOMsigMice]
    # SOMfacecolours = funcs.list_colours_to_rgba(SOMfacecolours)
    # facecolours = [PVfacecolours, SOMfacecolours]

    facecolours = [PVColour, SOMColour]

    plot_cell_type_comparison(axBar, changedprime, cellTypeColours, yLims, facecolours)

    axBar.set_xticklabels(xTickLabels)
    axBar.set_ylabel(r'$\Delta$ d$^\prime$', fontsize=fontSizeLabels)

    axBar.annotate(panelLabel, xy=(labelPosX[1], labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel,
                     fontweight='bold')
    axBar.annotate(cartoonLabel, xy=(labelPosX[0], labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel,
                   fontweight='bold')

# --- comparison in change in hits with PV and SOM inactivation ---
if PANELS[4]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserHits = summaryData['PVexpLaserHitsAllBands']
    PVnoLaserHits = summaryData['PVexpNoLaserHitsAllBands']
    SOMlaserHits = summaryData['SOMexpLaserHitsAllBands']
    SOMnoLaserHits = summaryData['SOMexpNoLaserHitsAllBands']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        PVlaserHitsControl = summaryData['PVcontrolLaserHitsAllBands']
        PVnoLaserHitsControl = summaryData['PVcontrolNoLaserHitsAllBands']
        SOMlaserHitsControl = summaryData['SOMcontrolLaserHitsAllBands']
        SOMnoLaserHitsControl = summaryData['SOMcontrolNoLaserHitsAllBands']

        PVlaserHitsCorrected = PVlaserHits - (PVlaserHitsControl - PVnoLaserHitsControl)
        SOMlaserHitsCorrected = SOMlaserHits - (SOMlaserHitsControl - SOMnoLaserHitsControl)

        hitsData = [[PVnoLaserHits, PVlaserHitsCorrected], [SOMnoLaserHits, SOMlaserHitsCorrected]]

    else:
        hitsData = [[PVnoLaserHits, PVlaserHits], [SOMnoLaserHits, SOMlaserHits]]

    if SIG_CONTROL_REMOVED:
        PVcontrolpVal = summaryData['PVcontrolpValAllBand']
        SOMcontrolpVal = summaryData['SOMcontrolpValAllBand']

        hitsData[0][0] = hitsData[0][0][PVcontrolpVal > 0.05]
        hitsData[0][1] = hitsData[0][1][PVcontrolpVal > 0.05]
        hitsData[1][0] = hitsData[1][0][SOMcontrolpVal > 0.05]
        hitsData[1][1] = hitsData[1][1][SOMcontrolpVal > 0.05]

    panelLabels = ['C', 'G']
    colours = [PVColour, SOMColour]
    yLims = [(0,100),(0,100)]
    xTickLabels = ['no PV', 'no SOM']

    for indType in range(2):
        axScatter = plt.subplot(gs[indType*2, 2])
        plot_laser_comparison(axScatter, hitsData[indType], colours[indType], yLims[indType])

        axScatter.set_xticklabels(['baseline', xTickLabels[indType]])
        axScatter.set_ylabel('Hit Rate (%)', fontsize=fontSizeLabels)

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[2], labelPosY[indLabel]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

# --- comparison in change in hit rate with laser in vs laser out
if PANELS[5]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserHits = summaryData['PVexpLaserHitsAllBands']
    PVnoLaserHits = summaryData['PVexpNoLaserHitsAllBands']
    SOMlaserHits = summaryData['SOMexpLaserHitsAllBands']
    SOMnoLaserHits = summaryData['SOMexpNoLaserHitsAllBands']

    PVchange = PVlaserHits - PVnoLaserHits
    SOMchange = SOMlaserHits - SOMnoLaserHits

    PVlaserHitsControl = summaryData['PVcontrolLaserHitsAllBands']
    PVnoLaserHitsControl = summaryData['PVcontrolNoLaserHitsAllBands']
    SOMlaserHitsControl = summaryData['SOMcontrolLaserHitsAllBands']
    SOMnoLaserHitsControl = summaryData['SOMcontrolNoLaserHitsAllBands']

    controlPVchange = PVlaserHitsControl - PVnoLaserHitsControl
    controlSOMchange = SOMlaserHitsControl - SOMnoLaserHitsControl

    PVeffectpVals = summaryData['PVcontrolvsexppValAllBands']
    PVlaserpVals = summaryData['PVexppValAllBand']
    PVsigMice = (PVeffectpVals<0.05) & (PVlaserpVals<0.05)

    SOMeffectpVals = summaryData['SOMcontrolvsexppValAllBands']
    SOMlaserpVals = summaryData['SOMexppValAllBand']
    SOMsigMice = (SOMeffectpVals < 0.05) & (SOMlaserpVals < 0.05)

    PVfacecolours = [PVColour if val else 'none' for val in PVsigMice]
    PVfacecolours = funcs.list_colours_to_rgba(PVfacecolours)
    SOMfacecolours = [SOMColour if val else 'none' for val in SOMsigMice]
    SOMfacecolours = funcs.list_colours_to_rgba(SOMfacecolours)

    panelLabels = ['B', 'F']
    colours = [PVColour, SOMColour]
    facecolours = [PVfacecolours, SOMfacecolours]
    xTickLabels = ['no PV', 'no SOM']
    xLims = [[-25, 10], [-25, 15]]
    yLims = [[-30, 5], [-30, 10]]

    expChange = [PVchange, SOMchange]
    controlChange = [controlPVchange, controlSOMchange]

    for indType in range(2):
        axScatter = plt.subplot(gs[indType*2+1, 2])
        plot_exp_vs_control_scatter(axScatter, controlChange[indType], expChange[indType], colours[indType], xLims[indType], yLims[indType], facecolours[indType])

        axScatter.set_xlabel(r'laser-out $\Delta$ HR', fontsize=fontSizeLabels)
        axScatter.set_ylabel(r'laser-in $\Delta$ HR', fontsize=fontSizeLabels)

        # -- linear regression --
        slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange[indType], expChange[indType])

        print(f'Laser in vs. out hit rate change for {xTickLabels[indType]}: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[1], labelPosY[indLabel]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

# --- summary of change in false alarm rate during PV or SOM inactivation ---
if PANELS[6]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserHits = summaryData['PVexpLaserHitsAllBands']
    PVnoLaserHits = summaryData['PVexpNoLaserHitsAllBands']
    SOMlaserHits = summaryData['SOMexpLaserHitsAllBands']
    SOMnoLaserHits = summaryData['SOMexpNoLaserHitsAllBands']
    possibleBands = summaryData['possibleBands']

    PVeffectpVals = summaryData['PVcontrolvsexppValAllBands']
    PVlaserpVals = summaryData['PVexppValAllBand']
    PVsigMice = (PVeffectpVals<0.05) & (PVlaserpVals<0.05)

    SOMeffectpVals = summaryData['SOMcontrolvsexppValAllBands']
    SOMlaserpVals = summaryData['SOMexppValAllBand']
    SOMsigMice = (SOMeffectpVals < 0.05) & (SOMlaserpVals < 0.05)

    PVchange = PVlaserHits - PVnoLaserHits
    SOMchange = SOMlaserHits - SOMnoLaserHits

    if CORRECTED:
        PVlaserHitsControl = summaryData['PVcontrolLaserHitsAllBands']
        PVnoLaserHitsControl = summaryData['PVcontrolNoLaserHitsAllBands']
        SOMlaserHitsControl = summaryData['SOMcontrolLaserHitsAllBands']
        SOMnoLaserHitsControl = summaryData['SOMcontrolNoLaserHitsAllBands']

        controlPVchange = PVlaserHitsControl - PVnoLaserHitsControl
        controlSOMchange = SOMlaserHitsControl - SOMnoLaserHitsControl

        correctedPVchange = PVchange - controlPVchange
        correctedSOMchange = SOMchange - controlSOMchange

        changeHits = [correctedPVchange, correctedSOMchange]

    else:
        changeHits = [PVchange, SOMchange]

    if SIG_CONTROL_REMOVED:
        PVcontrolpVal = summaryData['PVcontrolpValAllBand']
        SOMcontrolpVal = summaryData['SOMcontrolpValAllBand']

        changeHits[0] = changeHits[0][PVcontrolpVal > 0.05]
        changeHits[1] = changeHits[1][SOMcontrolpVal > 0.05]

    axBar = plt.subplot(gs[4,2])

    cellTypeColours = [PVColour, SOMColour]
    panelLabel = 'K'

    xTickLabels = ['no PV', 'no SOM']
    yLims = (-30, 10)

    # PVfacecolours = [PVColour if val else 'white' for val in PVsigMice]
    # PVfacecolours = funcs.list_colours_to_rgba(PVfacecolours)
    # SOMfacecolours = [SOMColour if val else 'white' for val in SOMsigMice]
    # SOMfacecolours = funcs.list_colours_to_rgba(SOMfacecolours)
    # facecolours = [PVfacecolours, SOMfacecolours]

    facecolours = [PVColour, SOMColour]

    plot_cell_type_comparison(axBar, changeHits, cellTypeColours, yLims, facecolours)

    axBar.set_xticklabels(xTickLabels)
    axBar.set_ylabel(r'$\Delta$ Hit Rate (%)', fontsize=fontSizeLabels)

    axBar.annotate(panelLabel, xy=(labelPosX[2], labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel,
                   fontweight='bold')

# --- comparison in change in false alarms with PV and SOM inactivation ---
if PANELS[7]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserFAs = summaryData['PVexpLaserFAallBands']
    PVnoLaserFAs = summaryData['PVexpNoLaserFAallBands']
    SOMlaserFAs = summaryData['SOMexpLaserFAallBands']
    SOMnoLaserFAs = summaryData['SOMexpNoLaserFAallBands']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        controlPVlaserFAs = summaryData['PVcontrolLaserFAallBands']
        controlPVnoLaserFAs = summaryData['PVcontrolNoLaserFAallBands']
        controlSOMlaserFAs = summaryData['SOMcontrolLaserFAallBands']
        controlSOMnoLaserFAs = summaryData['SOMcontrolNoLaserFAallBands']

        PVlaserFAsCorrected = PVlaserFAs - (controlPVlaserFAs - controlPVnoLaserFAs)
        SOMlaserFAsCorrected = SOMlaserFAs - (controlSOMlaserFAs - controlSOMnoLaserFAs)

        FAdata = [[PVnoLaserFAs, PVlaserFAsCorrected], [SOMnoLaserFAs, SOMlaserFAsCorrected]]

    else:
        FAdata = [[PVnoLaserFAs, PVlaserFAs], [SOMnoLaserFAs, SOMlaserFAs]]

    if SIG_CONTROL_REMOVED:
        PVcontrolpVal = summaryData['PVcontrolpValAllBand']
        SOMcontrolpVal = summaryData['SOMcontrolpValAllBand']

        FAdata[0][0] = FAdata[0][0][PVcontrolpVal > 0.05]
        FAdata[0][1] = FAdata[0][1][PVcontrolpVal > 0.05]
        FAdata[1][0] = FAdata[1][0][SOMcontrolpVal > 0.05]
        FAdata[1][1] = FAdata[1][1][SOMcontrolpVal > 0.05]

    panelLabels = ['D', 'H']
    colours = [PVColour, SOMColour]
    yLims = [(0,50),(0,70)]
    xTickLabels = ['no PV', 'no SOM']

    for indType in range(2):
        axScatter = plt.subplot(gs[indType*2, 3])
        plot_laser_comparison(axScatter, FAdata[indType], colours[indType], yLims[indType])

        axScatter.set_xticklabels(['baseline', xTickLabels[indType]])
        axScatter.set_ylabel('False Alarm Rate (%)', fontsize=fontSizeLabels)

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[3], labelPosY[indLabel]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

# --- comparison in change in false alarm rate with laser in vs laser out
if PANELS[8]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserFAs = summaryData['PVexpLaserFAallBands']
    PVnoLaserFAs = summaryData['PVexpNoLaserFAallBands']
    SOMlaserFAs = summaryData['SOMexpLaserFAallBands']
    SOMnoLaserFAs = summaryData['SOMexpNoLaserFAallBands']

    PVchange = PVlaserFAs - PVnoLaserFAs
    SOMchange = SOMlaserFAs - SOMnoLaserFAs

    controlPVlaserFAs = summaryData['PVcontrolLaserFAallBands']
    controlPVnoLaserFAs = summaryData['PVcontrolNoLaserFAallBands']
    controlSOMlaserFAs = summaryData['SOMcontrolLaserFAallBands']
    controlSOMnoLaserFAs = summaryData['SOMcontrolNoLaserFAallBands']

    controlPVchange = controlPVlaserFAs - controlPVnoLaserFAs
    controlSOMchange = controlSOMlaserFAs - controlSOMnoLaserFAs

    PVeffectpVals = summaryData['PVcontrolvsexppValAllBands']
    PVlaserpVals = summaryData['PVexppValAllBand']
    PVsigMice = (PVeffectpVals<0.05) & (PVlaserpVals<0.05)

    SOMeffectpVals = summaryData['SOMcontrolvsexppValAllBands']
    SOMlaserpVals = summaryData['SOMexppValAllBand']
    SOMsigMice = (SOMeffectpVals < 0.05) & (SOMlaserpVals < 0.05)

    PVfacecolours = [PVColour if val else 'none' for val in PVsigMice]
    PVfacecolours = funcs.list_colours_to_rgba(PVfacecolours)
    SOMfacecolours = [SOMColour if val else 'none' for val in SOMsigMice]
    SOMfacecolours = funcs.list_colours_to_rgba(SOMfacecolours)

    panelLabels = ['B', 'F']
    colours = [PVColour, SOMColour]
    facecolours = [PVfacecolours, SOMfacecolours]
    xTickLabels = ['no PV', 'no SOM']
    xLims = [[-20, 20], [-20, 15]]
    yLims = [[-20, 20], [-20, 15]]

    expChange = [PVchange, SOMchange]
    controlChange = [controlPVchange, controlSOMchange]

    for indType in range(2):
        axScatter = plt.subplot(gs[indType*2+1, 3])
        plot_exp_vs_control_scatter(axScatter, controlChange[indType], expChange[indType], colours[indType], xLims[indType], yLims[indType], facecolours[indType])

        axScatter.set_xlabel(r'laser-out $\Delta$ FAR', fontsize=fontSizeLabels)
        axScatter.set_ylabel(r'laser-in $\Delta$ FAR', fontsize=fontSizeLabels)

        # -- linear regression --
        slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange[indType], expChange[indType])

        print(f'Laser in vs. out false alarm rate change for {xTickLabels[indType]}: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[1], labelPosY[indLabel]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

    print(f'Significant PV mice: {np.sum(PVsigMice)} out of {len(PVsigMice)}')
    print(f'Significant SOM mice: {np.sum(SOMsigMice)} out of {len(SOMsigMice)}')

# --- summary of change in false alarms during PV or SOM inactivation ---
if PANELS[9]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserFAs = summaryData['PVexpLaserFAallBands']
    PVnoLaserFAs = summaryData['PVexpNoLaserFAallBands']
    SOMlaserFAs = summaryData['SOMexpLaserFAallBands']
    SOMnoLaserFAs = summaryData['SOMexpNoLaserFAallBands']
    possibleBands = summaryData['possibleBands']

    PVeffectpVals = summaryData['PVcontrolvsexppValAllBands']
    PVlaserpVals = summaryData['PVexppValAllBand']
    PVsigMice = (PVeffectpVals<0.05) & (PVlaserpVals<0.05)

    SOMeffectpVals = summaryData['SOMcontrolvsexppValAllBands']
    SOMlaserpVals = summaryData['SOMexppValAllBand']
    SOMsigMice = (SOMeffectpVals < 0.05) & (SOMlaserpVals < 0.05)

    PVchange = PVlaserFAs - PVnoLaserFAs
    SOMchange = SOMlaserFAs - SOMnoLaserFAs

    if CORRECTED:
        controlPVlaserFAs = summaryData['PVcontrolLaserFAallBands']
        controlPVnoLaserFAs = summaryData['PVcontrolNoLaserFAallBands']
        controlSOMlaserFAs = summaryData['SOMcontrolLaserFAallBands']
        controlSOMnoLaserFAs = summaryData['SOMcontrolNoLaserFAallBands']

        controlPVchange = controlPVlaserFAs - controlPVnoLaserFAs
        controlSOMchange = controlSOMlaserFAs - controlSOMnoLaserFAs

        correctedPVchange = PVchange - controlPVchange
        correctedSOMchange = SOMchange - controlSOMchange

        changeFAs = [correctedPVchange, correctedSOMchange]

    else:
        changeFAs = [PVchange, SOMchange]

    if SIG_CONTROL_REMOVED:
        PVcontrolpVal = summaryData['PVcontrolpValAllBand']
        SOMcontrolpVal = summaryData['SOMcontrolpValAllBand']

        changeFAs[0] = changeFAs[0][PVcontrolpVal > 0.05]
        changeFAs[1] = changeFAs[1][SOMcontrolpVal > 0.05]

    axBar = plt.subplot(gs[4,3])

    cellTypeColours = [PVColour, SOMColour]
    panelLabel = 'K'

    xTickLabels = ['no PV', 'no SOM']
    yLims = (-20, 10)

    # PVfacecolours = [PVColour if val else 'white' for val in PVsigMice]
    # PVfacecolours = funcs.list_colours_to_rgba(PVfacecolours)
    # SOMfacecolours = [SOMColour if val else 'white' for val in SOMsigMice]
    # SOMfacecolours = funcs.list_colours_to_rgba(SOMfacecolours)
    # facecolours = [PVfacecolours, SOMfacecolours]

    facecolours = [PVColour, SOMColour]

    plot_cell_type_comparison(axBar, changeFAs, cellTypeColours, yLims, facecolours)

    axBar.set_xticklabels(xTickLabels)
    axBar.set_ylabel(r'$\Delta$ False Alarm Rate (%)', fontsize=fontSizeLabels)

    axBar.annotate(panelLabel, xy=(labelPosX[3], labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel,
                   fontweight='bold')

    print(f'Significant PV mice: {np.sum(PVsigMice)} out of {len(PVsigMice)}')
    print(f'Significant SOM mice: {np.sum(SOMsigMice)} out of {len(SOMsigMice)}')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
