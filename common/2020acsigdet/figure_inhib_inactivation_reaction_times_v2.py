import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots

import behaviour_analysis_funcs as bf
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
figSize = [6.92,4.2]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.001, 0.21, 0.49, 0.72]  # Horiz position for panel labels
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

gs = gridspec.GridSpec(2, 4, width_ratios=[0.77, 1.0, 0.77, 1.0])
gs.update(top=0.98, bottom=0.05, left=0.07, right=0.97, wspace=0.7, hspace=0.3)

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
    yLim = (0, 150)
    xTickLabels = ['no PV', 'no SOM']
    colours = [PVColour, SOMColour]

    for type in range(len(laserReactions)):
        axScatter = plt.subplot(gs[type, 0])
        laserReaction = 1000*laserReactions[type] # convert to ms
        controlReaction = 1000*controlReactions[type]
        thisxticklabels = ['baseline', xTickLabels[type]]

        bf.plot_laser_comparison(axScatter, [controlReaction, laserReaction], colours[type], 'white', yLim, thisxticklabels)

        axScatter.set_ylabel('Sampling time (ms)', fontsize=fontSizeLabels)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[0], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

        # -- compute effect size (% change, change in ms)
        changeReaction = np.mean(laserReaction - controlReaction)
        meanReaction = np.mean(controlReaction)

        print(f'{xTickLabels[type]} mean change in reaction times: {changeReaction} ms, {100*changeReaction/meanReaction}% change')


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

    # PVeffectpVals = pValData['PVcontrolvsexppValAllBands']
    # PVlaserpVals = pValData['PVexppValAllBand']
    # PVsigMice = (PVeffectpVals<0.05) & (PVlaserpVals<0.05)
    #
    # SOMeffectpVals = pValData['SOMcontrolvsexppValAllBands']
    # SOMlaserpVals = pValData['SOMexppValAllBand']
    # SOMsigMice = (SOMeffectpVals < 0.05) & (SOMlaserpVals < 0.05)
    #
    # PVfacecolours = [PVColour if val else 'none' for val in PVsigMice]
    # PVfacecolours = funcs.list_colours_to_rgba(PVfacecolours)
    # SOMfacecolours = [SOMColour if val else 'none' for val in SOMsigMice]
    # SOMfacecolours = funcs.list_colours_to_rgba(SOMfacecolours)

    expChange = [1000*PVexpChange, 1000*SOMexpChange] # convert to ms
    controlChange = [1000*PVcontrolChange, 1000*SOMcontrolChange]
    xLims = [(-10, 50), (-20, 20)]
    yLims = [(-20, 40), (-1, 40)]
    axisLabels = ['No PV', 'No SOM']
    panelLabels = ['B', 'F']
    colours = [PVColour, SOMColour]
    #facecolours = [PVfacecolours, SOMfacecolours]

    for type in range(len(expChange)):
        axScatter = plt.subplot(gs[type, 1])

        bf.plot_exp_vs_control_scatter(axScatter, controlChange[type], expChange[type], colours[type], xLims[type], yLims[type], 'none')

        axScatter.set_xlabel(r'Control $\Delta$ sampling time', fontsize=fontSizeLabels)
        axScatter.set_ylabel(f'{axisLabels[type]} ' r'$\Delta$ sampling time', fontsize=fontSizeLabels)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[1], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

        # -- linear regression --
        slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange[type], expChange[type])

        print(f'Laser in vs. out sampling time change for {axisLabels[type]}: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

        # -- compute Cohen's d --
        # cohensd = funcs.cohend(controlChange[type], expChange[type], independent=True)
        # print(f'Cohen\'s d: {cohensd}')

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
    yLim = [250, 550]
    xTickLabels = ['no PV', 'no SOM']
    colours = [PVColour, SOMColour]

    for type in range(len(laserDecisions)):
        axScatter = plt.subplot(gs[type, 2])
        laserDecision = 1000*laserDecisions[type]
        controlDecision = 1000*controlDecisions[type]
        thisxticklabels = ['baseline', xTickLabels[type]]

        bf.plot_laser_comparison(axScatter, [controlDecision, laserDecision], colours[type], 'white', yLim, thisxticklabels)
        axScatter.set_ylabel('Time to reward (ms)', fontsize=fontSizeLabels)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[2], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

        # -- compute effect size (% change, change in ms)
        changeDecision = np.mean(laserDecision - controlDecision)
        meanDecision = np.mean(controlDecision)

        print(f'{xTickLabels[type]} mean change in decision times: {changeDecision} ms, {100 * changeDecision / meanDecision}% change')

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

    # PVeffectpVals = pValData['PVcontrolvsexppValAllBands']
    # PVlaserpVals = pValData['PVexppValAllBand']
    # PVsigMice = (PVeffectpVals<0.05) & (PVlaserpVals<0.05)
    #
    # SOMeffectpVals = pValData['SOMcontrolvsexppValAllBands']
    # SOMlaserpVals = pValData['SOMexppValAllBand']
    # SOMsigMice = (SOMeffectpVals < 0.05) & (SOMlaserpVals < 0.05)
    #
    # PVfacecolours = [PVColour if val else 'none' for val in PVsigMice]
    # PVfacecolours = funcs.list_colours_to_rgba(PVfacecolours)
    # SOMfacecolours = [SOMColour if val else 'none' for val in SOMsigMice]
    # SOMfacecolours = funcs.list_colours_to_rgba(SOMfacecolours)

    expChange = [1000*PVexpChange, 1000*SOMexpChange]
    controlChange = [1000*PVcontrolChange, 1000*SOMcontrolChange]
    xLims = [(-10, 50), (-20, 30)]
    yLims = [(-10, 50), (-10, 40)]
    axisLabels = ['No PV', 'No SOM']
    panelLabels = ['D', 'H']
    colours = [PVColour, SOMColour]
    #facecolours = [PVfacecolours, SOMfacecolours]

    for type in range(len(expChange)):
        axScatter = plt.subplot(gs[type, 3])

        bf.plot_exp_vs_control_scatter(axScatter, controlChange[type], expChange[type], colours[type], xLims[type], yLims[type], 'none')

        axScatter.set_xlabel(r'Control $\Delta$ time to reward', fontsize=fontSizeLabels)
        axScatter.set_ylabel(f'{axisLabels[type]} ' r'$\Delta$ time to reward', fontsize=fontSizeLabels)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[3], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

        # -- linear regression --
        slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange[type], expChange[type])

        print(f'Laser in vs. out time to reward change for {axisLabels[type]}: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

        # -- compute Cohen's d --
        # cohensd = funcs.cohend(controlChange[type], expChange[type], independent=True)
        # print(f'Cohen\'s d: {cohensd}')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
