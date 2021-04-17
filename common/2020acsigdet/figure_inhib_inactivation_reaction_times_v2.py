import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots

import behaviour_analysis_funcs as funcs
import figparams
import studyparams

figName = 'figure_inhibitory_inactivation_reaction_times'
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

pValFigName = 'figure_inhibitory_inactivation' # get pVals from inactivation behaviour effect figure
# pValDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, pValFigName)
pValDataDir = os.path.join(settings.FIGURES_DATA_PATH, pValFigName)

PANELS = [1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
CORRECTED = 0
outputDir = '/tmp/'
if CORRECTED:
    figFilename = 'Fig5_inhib_inactivation_reaction_times_corrected_v2'  # Do not include extension
else:
    figFilename = 'Fig5_inhib_inactivation_reaction_times_v2'
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [6.9,4.2]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.001, 0.20, 0.51, 0.70]  # Horiz position for panel labels
labelPosY = [0.96, 0.45]  # Vert position for panel labels

summaryFileName = 'all_reaction_times_inhib_inactivation.npz'
pValFileName = 'all_behaviour_inhib_inactivation_v2.npz'

baseColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']
controlColour = figparams.colp['connectLine']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 4, width_ratios=[0.7, 1.0, 0.7, 1.0])
gs.update(top=0.98, bottom=0.05, left=0.1, right=0.98, wspace=0.7, hspace=0.3)

# --- comparison in change in sampling times with inactivation ---
if PANELS[0]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserReaction = summaryData['PVexpLaserReactionAllBand']
    PVcontrolReaction = summaryData['PVexpNoLaserReactionAllBand']
    SOMlaserReaction = summaryData['SOMexpLaserReactionAllBand']
    SOMcontrolReaction = summaryData['SOMexpNoLaserReactionAllBand']

    if CORRECTED:
        PVlaserReactionControl = summaryData['PVcontrolLaserReactionAllBand']
        PVcontrolReactionControl = summaryData['PVcontrolNoLaserReactionAllBand']
        SOMlaserReactionControl = summaryData['SOMcontrolLaserReactionAllBand']
        SOMcontrolReactionControl = summaryData['SOMcontrolNoLaserReactionAllBand']

        PVlaserReactionCorrected = PVlaserReaction - (PVlaserReactionControl - PVcontrolReactionControl)
        SOMlaserReactionCorrected = SOMlaserReaction - (SOMlaserReactionControl - SOMcontrolReactionControl)

    else:
        PVlaserReactionCorrected = PVlaserReaction
        SOMlaserReactionCorrected = SOMlaserReaction

    laserReactions = [PVlaserReactionCorrected, SOMlaserReactionCorrected]
    controlReactions = [PVcontrolReaction, SOMcontrolReaction]

    panelLabels = ['A', 'E']

    barLoc = np.array([-0.24, 0.24])
    yLim = (0, 0.15)
    legendLabels = ['no PV', 'no SOM']
    colours = [PVColour, SOMColour]

    for type in range(len(laserReactions)):
        axScatter = plt.subplot(gs[type, 0])
        laserReaction = laserReactions[type]
        controlReaction = controlReactions[type]

        for indMouse in range(laserReaction.shape[0]):
            plt.plot(barLoc, [controlReaction[indMouse], laserReaction[indMouse]], '-', color=controlColour)

        l1, = plt.plot(np.tile(barLoc[1], laserReaction.shape[0]), laserReaction, 'o', mec=colours[type], mfc='white')
        l2, = plt.plot(np.tile(barLoc[0], controlReaction.shape[0]), controlReaction, 'o', mec=baseColour, mfc=baseColour)

        axScatter.legend([l2, l1], ['control', legendLabels[type]], loc='best')

        axScatter.set_xlim(barLoc[0] - 0.3, barLoc[1] + 0.3)
        axScatter.set_xticks([])

        axScatter.set_ylim(yLim)
        axScatter.set_ylabel('Sampling time (s)', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[0], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

        # -- stats!! --
        pVal = stats.wilcoxon(laserReaction, controlReaction)[1]
        if pVal < 0.05:
            extraplots.significance_stars(barLoc, 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3)
        print(f"Change in reaction time with {legendLabels[type]} pVal: {pVal}")

# --- laser in vs out reaction times ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    pValDataFullPath = os.path.join(pValDataDir, pValFileName)
    pValData = np.load(pValDataFullPath)

    PVlaserReaction = summaryData['PVexpLaserReactionAllBand']
    PVcontrolReaction = summaryData['PVexpNoLaserReactionAllBand']
    SOMlaserReaction = summaryData['SOMexpLaserReactionAllBand']
    SOMcontrolReaction = summaryData['SOMexpNoLaserReactionAllBand']
    PVexpChange = PVlaserReaction - PVcontrolReaction
    SOMexpChange = SOMlaserReaction - SOMcontrolReaction

    PVlaserReactionControl = summaryData['PVcontrolLaserReactionAllBand']
    PVcontrolReactionControl = summaryData['PVcontrolNoLaserReactionAllBand']
    SOMlaserReactionControl = summaryData['SOMcontrolLaserReactionAllBand']
    SOMcontrolReactionControl = summaryData['SOMcontrolNoLaserReactionAllBand']
    PVcontrolChange = PVlaserReactionControl - PVcontrolReactionControl
    SOMcontrolChange = SOMlaserReactionControl - SOMcontrolReactionControl

    PVeffectpVals = pValData['PVcontrolvsexppValAllBands']
    PVlaserpVals = pValData['PVexppValAllBand']
    PVsigMice = (PVeffectpVals<0.05) & (PVlaserpVals<0.05)

    SOMeffectpVals = pValData['SOMcontrolvsexppValAllBands']
    SOMlaserpVals = pValData['SOMexppValAllBand']
    SOMsigMice = (SOMeffectpVals < 0.05) & (SOMlaserpVals < 0.05)

    PVfacecolours = [PVColour if val else 'none' for val in PVsigMice]
    PVfacecolours = funcs.list_colours_to_rgba(PVfacecolours)
    SOMfacecolours = [SOMColour if val else 'none' for val in SOMsigMice]
    SOMfacecolours = funcs.list_colours_to_rgba(SOMfacecolours)

    expChange = [PVexpChange, SOMexpChange]
    controlChange = [PVcontrolChange, SOMcontrolChange]
    xLims = [(-0.01, 0.05), (-0.02, 0.02)]
    yLims = [(-0.02, 0.04), (-0.001, 0.04)]
    legendLabels = ['no PV', 'no SOM']
    panelLabels = ['B', 'F']
    colours = [PVColour, SOMColour]
    facecolours = [PVfacecolours, SOMfacecolours]

    for type in range(len(expChange)):
        axScatter = plt.subplot(gs[type, 1])
        plt.scatter(controlChange[type], expChange[type], edgecolors=colours[type], facecolors=facecolours[type])

        plt.plot([-100, 100], [0, 0], ':', c='0.5', zorder=-10)
        plt.plot([0, 0], [-100, 100], ':', c='0.5', zorder=-10)
        plt.plot([-100, 100], [-100, 100], ':', c='0.5', zorder=-10)

        axScatter.set_xlim(xLims[type])
        axScatter.set_ylim(yLims[type])

        axScatter.set_xlabel(r'laser-out $\Delta$ sampling time', fontsize=fontSizeLabels)
        axScatter.set_ylabel(r'laser-in $\Delta$ sampling time', fontsize=fontSizeLabels)
        axScatter.set(adjustable='box', aspect='equal')

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[1], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

        # -- linear regression --
        slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange[type], expChange[type])

        print(f'Laser in vs. out sampling time change for {legendLabels[type]}: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

        # -- compute Cohen's d --
        cohensd = funcs.cohend(controlChange[type], expChange[type], independent=True)
        #print(np.mean(controlChange[type]), np.mean(expChange[type]), np.var(controlChange[type]), np.var(expChange[type]))
        print(f'Cohen\'s d: {cohensd}')

# --- comparison in change in decision times with inactivation ---
if PANELS[2]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserDecision = summaryData['PVexpLaserDecisionAllBand']
    PVcontrolDecision = summaryData['PVexpNoLaserDecisionAllBand']
    SOMlaserDecision = summaryData['SOMexpLaserDecisionAllBand']
    SOMcontrolDecision = summaryData['SOMexpNoLaserDecisionAllBand']

    if CORRECTED:
        PVlaserDecisionControl = summaryData['PVcontrolLaserDecisionAllBand']
        PVcontrolDecisionControl = summaryData['PVcontrolNoLaserDecisionAllBand']
        SOMlaserDecisionControl = summaryData['SOMcontrolLaserDecisionAllBand']
        SOMcontrolDecisionControl = summaryData['SOMcontrolNoLaserDecisionAllBand']

        PVlaserDecisionCorrected = PVlaserDecision - (PVlaserDecisionControl - PVcontrolDecisionControl)
        SOMlaserDecisionCorrected = SOMlaserDecision - (SOMlaserDecisionControl - SOMcontrolDecisionControl)

    else:
        PVlaserDecisionCorrected = PVlaserDecision
        SOMlaserDecisionCorrected = SOMlaserDecision

    laserDecisions = [PVlaserDecisionCorrected, SOMlaserDecisionCorrected]
    controlDecisions = [PVcontrolDecision, SOMcontrolDecision]

    panelLabels = ['C', 'G']

    barLoc = np.array([-0.24, 0.24])
    yLims = [(0.25, 0.55), (0.25, 0.55)]
    legendLabels = ['no PV', 'no SOM']
    colours = [PVColour, SOMColour]

    for type in range(len(laserDecisions)):
        axScatter = plt.subplot(gs[type, 2])
        laserDecision = laserDecisions[type]
        controlDecision = controlDecisions[type]

        for indMouse in range(laserDecision.shape[0]):
            plt.plot(barLoc, [controlDecision[indMouse], laserDecision[indMouse]], '-', color=controlColour)

        l1, = plt.plot(np.tile(barLoc[1], laserDecision.shape[0]), laserDecision, 'o', mec=colours[type], mfc='white')
        l2, = plt.plot(np.tile(barLoc[0], controlDecision.shape[0]), controlDecision, 'o', mec=baseColour, mfc=baseColour)

        # median = np.median(accuracyData, axis=0)
        # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
        axScatter.legend([l2, l1], ['control', legendLabels[type]], loc='best')

        axScatter.set_xlim(barLoc[0] - 0.3, barLoc[1] + 0.3)
        axScatter.set_xticklabels([])

        axScatter.set_ylim(yLims[type])
        axScatter.set_ylabel('Time to reward (s)', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[2], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

        # -- stats!! --
        pVal = stats.wilcoxon(laserDecision, controlDecision)[1]
        if pVal < 0.05:
            extraplots.significance_stars(barLoc, 0.98 * yLims[type][1], 0.02 * np.diff(yLims[type]),
                                          gapFactor=0.3)
        print(f"Change in decision time with {legendLabels[type]} pVal: {pVal}")

# --- laser in vs out decision times ---
if PANELS[3]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    pValDataFullPath = os.path.join(pValDataDir, pValFileName)
    pValData = np.load(pValDataFullPath)

    PVlaserDecision = summaryData['PVexpLaserDecisionAllBand']
    PVcontrolDecision = summaryData['PVexpNoLaserDecisionAllBand']
    SOMlaserDecision = summaryData['SOMexpLaserDecisionAllBand']
    SOMcontrolDecision = summaryData['SOMexpNoLaserDecisionAllBand']
    PVexpChange = PVlaserDecision - PVcontrolDecision
    SOMexpChange = SOMlaserDecision - SOMcontrolDecision

    PVlaserDecisionControl = summaryData['PVcontrolLaserDecisionAllBand']
    PVcontrolDecisionControl = summaryData['PVcontrolNoLaserDecisionAllBand']
    SOMlaserDecisionControl = summaryData['SOMcontrolLaserDecisionAllBand']
    SOMcontrolDecisionControl = summaryData['SOMcontrolNoLaserDecisionAllBand']
    PVcontrolChange = PVlaserDecisionControl - PVcontrolDecisionControl
    SOMcontrolChange = SOMlaserDecisionControl - SOMcontrolDecisionControl

    PVeffectpVals = pValData['PVcontrolvsexppValAllBands']
    PVlaserpVals = pValData['PVexppValAllBand']
    PVsigMice = (PVeffectpVals<0.05) & (PVlaserpVals<0.05)

    SOMeffectpVals = pValData['SOMcontrolvsexppValAllBands']
    SOMlaserpVals = pValData['SOMexppValAllBand']
    SOMsigMice = (SOMeffectpVals < 0.05) & (SOMlaserpVals < 0.05)

    PVfacecolours = [PVColour if val else 'none' for val in PVsigMice]
    PVfacecolours = funcs.list_colours_to_rgba(PVfacecolours)
    SOMfacecolours = [SOMColour if val else 'none' for val in SOMsigMice]
    SOMfacecolours = funcs.list_colours_to_rgba(SOMfacecolours)

    expChange = [PVexpChange, SOMexpChange]
    controlChange = [PVcontrolChange, SOMcontrolChange]
    xLims = [(-0.01, 0.05), (-0.02, 0.03)]
    yLims = [(-0.01, 0.05), (-0.01, 0.04)]
    legendLabels = ['no PV', 'no SOM']
    panelLabels = ['D', 'H']
    colours = [PVColour, SOMColour]
    facecolours = [PVfacecolours, SOMfacecolours]

    for type in range(len(expChange)):
        axScatter = plt.subplot(gs[type, 3])
        plt.scatter(controlChange[type], expChange[type], edgecolors=colours[type], facecolors=facecolours[type])

        plt.plot([-100, 100], [0, 0], ':', c='0.5', zorder=-10)
        plt.plot([0, 0], [-100, 100], ':', c='0.5', zorder=-10)
        plt.plot([-100, 100], [-100, 100], ':', c='0.5', zorder=-10)

        axScatter.set_xlim(xLims[type])
        axScatter.set_ylim(yLims[type])

        axScatter.set_xlabel(r'laser-out $\Delta$ time to reward', fontsize=fontSizeLabels)
        axScatter.set_ylabel(r'laser-in $\Delta$ time to reward', fontsize=fontSizeLabels)
        axScatter.set(adjustable='box', aspect='equal')

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[3], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

        # -- linear regression --
        slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange[type], expChange[type])

        print(f'Laser in vs. out time to reward change for {legendLabels[type]}: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

        # -- compute Cohen's d --
        cohensd = funcs.cohend(controlChange[type], expChange[type], independent=True)
        print(f'Cohen\'s d: {cohensd}')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
