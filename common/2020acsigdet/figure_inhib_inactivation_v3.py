import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots

import behaviour_analysis_funcs as bf
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
figSize = [6.82,6.5]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.003, 0.32, 0.525, 0.74]  # Horiz position for panel labels
labelPosY = [0.97, 0.84, 0.49, 0.36,
             0.705, 0.47, 0.21]  # Vert position for panel labels

PVInactExample = 'band137_psycurve.npz'
SOMInactExample = 'band065_psycurve.npz'
summaryFileName = 'all_behaviour_inhib_inactivation_v2.npz'

baseColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']
controlColour = figparams.colp['control']
connectLineColour = figparams.colp['connectLine']

lineWidth = figparams.lineWidth
markerSize = figparams.markerSize

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(5, 4, width_ratios=[1.7, 1, 1, 1], height_ratios=[1,0.5,0.001,1,0.5])
gs.update(top=0.98, bottom=0.08, left=0.08, right=0.94, wspace=0.6, hspace=0.4)


# --- example psychometric curves ---
if PANELS[0]:
    examples = [PVInactExample, SOMInactExample]
    cellTypeColours = [PVColour, SOMColour]
    labels = ['no PV', 'no SOM']
    cartoonLabels = ['A', 'I']
    panelLabels = ['B', 'J']

    axPsyCurves = gs[:, 0]
    gs2 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=axPsyCurves, wspace=0.3, hspace=0.4, height_ratios=[0.3,1.0,0.3,1.0])

    for indType, exampleFileName in enumerate(examples):
        dataFullPath = os.path.join(inactDataDir, exampleFileName)
        data = np.load(dataFullPath)

        axCurve = plt.subplot(gs2[indType*2+1, 0])

        psyCurveControl = data['psyCurveLaserInControl']
        upperErrorControl = data['upperErrorLaserInControl']
        lowerErrorControl = data['lowerErrorLaserInControl']
        possibleSNRs = data['possibleSNRs']

        xVals = range(len(possibleSNRs))
        plt.plot(xVals[:2], psyCurveControl[:2], 'o--', color=baseColour, lw=lineWidth, ms=markerSize, zorder=10)
        l1, = plt.plot(xVals[1:], psyCurveControl[1:], 'o-', color=baseColour, lw=lineWidth, ms=markerSize, zorder=10)
        #l1, = plt.plot(range(len(possibleSNRs)), psyCurveControl, 'o-', color=ExcColour, lw=3, ms=8)
        plt.errorbar(range(len(possibleSNRs)), psyCurveControl, yerr=[lowerErrorControl, upperErrorControl], fmt='none',
                     color=baseColour, lw=lineWidth, capsize=5, capthick=1)

        psyCurveLaser = data['psyCurveLaserIn']
        upperErrorLaser = data['upperErrorLaserIn']
        lowerErrorLaser = data['lowerErrorLaserIn']

        plt.plot(xVals[:2], psyCurveLaser[:2], 'o--', color=cellTypeColours[indType], mfc='white', lw=lineWidth, ms=markerSize, zorder=10)
        l2, = plt.plot(xVals[1:], psyCurveLaser[1:], 'o-', color=cellTypeColours[indType], mfc='white', lw=lineWidth, ms=markerSize, zorder=10)
        #l2, = plt.plot(range(len(possibleSNRs)), psyCurveLaser, 'o--', color=cellTypeColours[indType], mfc='white', lw=3, ms=8)
        plt.errorbar(range(len(possibleSNRs)), psyCurveLaser, yerr=[lowerErrorLaser, upperErrorLaser], fmt='none',
                     color=cellTypeColours[indType], lw=lineWidth, capsize=5, capthick=1, zorder=-10)

        psyCurveLaserOut = data['psyCurveLaserOut']
        upperErrorLaserOut = data['upperErrorLaserOut']
        lowerErrorLaserOut = data['lowerErrorLaserOut']

        # plt.plot(xVals[:2], psyCurveLaserOut[:2], 'o--', color=controlColour, mfc='white', lw=3, ms=8, zorder=10)
        # l3, = plt.plot(xVals[1:], psyCurveLaserOut[1:], 'o-', color=controlColour, mfc='white', lw=3, ms=8, zorder=10)
        # # l2, = plt.plot(range(len(possibleSNRs)), psyCurveLaser, 'o--', color=cellTypeColours[indType], mfc='white', lw=3, ms=8)
        # plt.errorbar(range(len(possibleSNRs)), psyCurveLaserOut, yerr=[lowerErrorLaserOut, upperErrorLaserOut], fmt='none',
        #              color=controlColour, lw=2, capsize=5, capthick=1, zorder=-10)

        axCurve.legend([l1, l2], ['baseline', labels[indType]], fontsize=fontSizeLegend, frameon=False, handlelength=1.0)

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
        axCurve.annotate(label, xy=(labelPosX[0], labelPosY[indLabel*2+1]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
        axCurve.annotate(cartoonLabels[indLabel], xy=(labelPosX[0], labelPosY[indLabel*2]), xycoords='figure fraction',
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

    panelLabels = ['C', 'K']
    colours = [PVColour, SOMColour]
    xTickLabels = ['no PV', 'no SOM']
    yLim = [0,2.3]

    for indType in range(2):
        axScatter = plt.subplot(gs[indType*3,1])
        thisxticklabels = ['baseline', xTickLabels[indType]]
        bf.plot_laser_comparison(axScatter, dprimeData[indType], colours[indType], 'white', yLim, thisxticklabels)
        axScatter.set_ylabel('d\'', fontsize=fontSizeLabels)

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[1], labelPosY[indLabel*5]), xycoords='figure fraction',
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

    # PVeffectpVals = summaryData['PVcontrolvsexppValAllBands']
    # PVlaserpVals = summaryData['PVexppValAllBand']
    # PVsigMice = (PVeffectpVals<0.05) & (PVlaserpVals<0.05)
    #
    # SOMeffectpVals = summaryData['SOMcontrolvsexppValAllBands']
    # SOMlaserpVals = summaryData['SOMexppValAllBand']
    # SOMsigMice = (SOMeffectpVals < 0.05) & (SOMlaserpVals < 0.05)
    #
    # PVfacecolours = [PVColour if val else 'none' for val in PVsigMice]
    # PVfacecolours = funcs.list_colours_to_rgba(PVfacecolours)
    # SOMfacecolours = [SOMColour if val else 'none' for val in SOMsigMice]
    # SOMfacecolours = funcs.list_colours_to_rgba(SOMfacecolours)

    panelLabels = ['F', 'N']
    colours = [PVColour, SOMColour]
    # facecolours = [PVfacecolours, SOMfacecolours]
    xTickLabels = ['No PV', 'No SOM']
    xLims = [[-0.5, 0.5], [-0.5, 0.3]]
    yLims = [[-0.7, 0.3], [-0.7, 0.1]]

    expChange = [PVchange, SOMchange]
    controlChange = [controlPVchange, controlSOMchange]

    for indType in range(2):
        axScatter = plt.subplot(gs[indType*3+1, 1])
        bf.plot_exp_vs_control_scatter(axScatter, controlChange[indType], expChange[indType], colours[indType], xLims[indType], yLims[indType], 'none')

        axScatter.set_xlabel(r'Control $\Delta$ d$^\prime$', fontsize=fontSizeLabels)
        axScatter.set_ylabel(f'{xTickLabels[indType]} ' r'$\Delta$ d$^\prime$', fontsize=fontSizeLabels, labelpad=0)

        # -- linear regression --
        slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange[indType], expChange[indType])

        print(f'Laser in vs. out d\' change for {xTickLabels[indType]}: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

        # -- compare change in d' between laser in and out --
        pVal = stats.wilcoxon(controlChange[indType], expChange[indType])[1]
        print(f'Laser in vs. out direction of effect d\' pVal {xTickLabels[indType]}: {pVal}')

        percentBiggerLaserIn = 100.0*np.sum((controlChange[indType]-expChange[indType])>0)/len(controlChange[indType])
        print(f'Percent of {xTickLabels[indType]} mice with bigger laser in effect: {percentBiggerLaserIn}')


    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[1], labelPosY[indLabel*2+4]), xycoords='figure fraction',
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

    bf.plot_cell_type_comparison(axBar, changedprime, cellTypeColours, yLims, facecolours)

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

    panelLabels = ['D', 'L']
    colours = [PVColour, SOMColour]
    yLim = (0,100)
    xTickLabels = ['no PV', 'no SOM']

    for indType in range(2):
        axScatter = plt.subplot(gs[indType*3, 2])
        thisxticklabels = ['baseline', xTickLabels[indType]]
        bf.plot_laser_comparison(axScatter, hitsData[indType], colours[indType], 'white', yLim, thisxticklabels)

        axScatter.set_ylabel('Hit Rate (%)', fontsize=fontSizeLabels, labelpad=0)

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[2], labelPosY[indLabel*5]), xycoords='figure fraction',
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

    # PVeffectpVals = summaryData['PVcontrolvsexppValAllBands']
    # PVlaserpVals = summaryData['PVexppValAllBand']
    # PVsigMice = (PVeffectpVals<0.05) & (PVlaserpVals<0.05)
    #
    # SOMeffectpVals = summaryData['SOMcontrolvsexppValAllBands']
    # SOMlaserpVals = summaryData['SOMexppValAllBand']
    # SOMsigMice = (SOMeffectpVals < 0.05) & (SOMlaserpVals < 0.05)
    #
    # PVfacecolours = [PVColour if val else 'none' for val in PVsigMice]
    # PVfacecolours = funcs.list_colours_to_rgba(PVfacecolours)
    # SOMfacecolours = [SOMColour if val else 'none' for val in SOMsigMice]
    # SOMfacecolours = funcs.list_colours_to_rgba(SOMfacecolours)

    panelLabels = ['G', 'O']
    colours = [PVColour, SOMColour]
    # facecolours = [PVfacecolours, SOMfacecolours]
    xTickLabels = ['No PV', 'No SOM']
    xLims = [[-25, 10], [-25, 15]]
    yLims = [[-30, 5], [-30, 10]]

    expChange = [PVchange, SOMchange]
    controlChange = [controlPVchange, controlSOMchange]

    for indType in range(2):
        axScatter = plt.subplot(gs[indType*3+1, 2])
        bf.plot_exp_vs_control_scatter(axScatter, controlChange[indType], expChange[indType], colours[indType], xLims[indType], yLims[indType], 'none')

        axScatter.set_xlabel(r'Control $\Delta$ HR', fontsize=fontSizeLabels)
        axScatter.set_ylabel(f'{xTickLabels[indType]} ' r'$\Delta$ HR', fontsize=fontSizeLabels, labelpad=0)

        # -- linear regression --
        slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange[indType], expChange[indType])

        print(f'Laser in vs. out hit rate change for {xTickLabels[indType]}: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

        # -- compare change in hit rate between laser in and out --
        pVal = stats.wilcoxon(controlChange[indType], expChange[indType])[1]
        print(f'Laser in vs. out direction of effect hit rate pVal {xTickLabels[indType]}: {pVal}')

        percentBiggerLaserIn = 100.0 * np.sum((controlChange[indType] - expChange[indType]) > 0) / len(controlChange[indType])
        print(f'Percent of {xTickLabels[indType]} mice with bigger laser in effect: {percentBiggerLaserIn}')

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[2], labelPosY[indLabel*2+4]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

# --- summary of change in hit rate during PV or SOM inactivation ---
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

    bf.plot_cell_type_comparison(axBar, changeHits, cellTypeColours, yLims, facecolours)

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

    panelLabels = ['E', 'M']
    colours = [PVColour, SOMColour]
    yLim = (0,70)
    xTickLabels = ['no PV', 'no SOM']

    for indType in range(2):
        axScatter = plt.subplot(gs[indType*3, 3])
        thisxticklabels = ['baseline', xTickLabels[indType]]
        bf.plot_laser_comparison(axScatter, FAdata[indType], colours[indType], 'white', yLim, thisxticklabels)

        axScatter.set_ylabel('False Alarm Rate (%)', fontsize=fontSizeLabels, labelpad=3)

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[3], labelPosY[indLabel*5]), xycoords='figure fraction',
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

    # PVeffectpVals = summaryData['PVcontrolvsexppValAllBands']
    # PVlaserpVals = summaryData['PVexppValAllBand']
    # PVsigMice = (PVeffectpVals<0.05) & (PVlaserpVals<0.05)
    #
    # SOMeffectpVals = summaryData['SOMcontrolvsexppValAllBands']
    # SOMlaserpVals = summaryData['SOMexppValAllBand']
    # SOMsigMice = (SOMeffectpVals < 0.05) & (SOMlaserpVals < 0.05)
    #
    # PVfacecolours = [PVColour if val else 'none' for val in PVsigMice]
    # PVfacecolours = funcs.list_colours_to_rgba(PVfacecolours)
    # SOMfacecolours = [SOMColour if val else 'none' for val in SOMsigMice]
    # SOMfacecolours = funcs.list_colours_to_rgba(SOMfacecolours)

    panelLabels = ['H', 'P']
    colours = [PVColour, SOMColour]
    # facecolours = [PVfacecolours, SOMfacecolours]
    xTickLabels = ['No PV', 'No SOM']
    xLims = [[-20, 20], [-20, 15]]
    yLims = [[-20, 20], [-20, 15]]

    expChange = [PVchange, SOMchange]
    controlChange = [controlPVchange, controlSOMchange]

    for indType in range(2):
        axScatter = plt.subplot(gs[indType*3+1, 3])
        bf.plot_exp_vs_control_scatter(axScatter, controlChange[indType], expChange[indType], colours[indType], xLims[indType], yLims[indType], 'none')

        axScatter.set_xlabel(r'Control $\Delta$ FAR', fontsize=fontSizeLabels)
        axScatter.set_ylabel(f'{xTickLabels[indType]} ' r'$\Delta$ FAR', fontsize=fontSizeLabels, labelpad=0)

        # -- linear regression --
        slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange[indType], expChange[indType])

        print(f'Laser in vs. out false alarm rate change for {xTickLabels[indType]}: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

        # -- compare change in FA rate between laser in and out --
        pVal = stats.wilcoxon(controlChange[indType], expChange[indType])[1]
        print(f'Laser in vs. out direction of effect FA pVal {xTickLabels[indType]}: {pVal}')

        percentBiggerLaserIn = 100.0 * np.sum((controlChange[indType] - expChange[indType]) > 0) / len(
            controlChange[indType])
        print(f'Percent of {xTickLabels[indType]} mice with bigger laser in effect: {percentBiggerLaserIn}')

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[3], labelPosY[indLabel*2+4]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

    # print(f'Significant PV mice: {np.sum(PVsigMice)} out of {len(PVsigMice)}')
    # print(f'Significant SOM mice: {np.sum(SOMsigMice)} out of {len(SOMsigMice)}')

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
