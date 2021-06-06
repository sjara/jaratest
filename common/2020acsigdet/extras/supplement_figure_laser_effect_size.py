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

ACFIGNAME = 'figure_ac_inactivation'
# acDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
acDataDir = os.path.join(settings.FIGURES_DATA_PATH, ACFIGNAME)

INACTFIGNAME = 'figure_inhibitory_inactivation'
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, INACTFIGNAME)

PANELS = [1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
CORRECTED = 0
outputDir = '/tmp/'
if CORRECTED:
    figFilename = 'FigX_correlations_of_laser_effect_corrected'  # Do not include extension
else:
    figFilename = 'FigX_correlations_of_laser_effect'
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [9,6]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.2, 0.55, 0.77, 0.25, 0.5, 0.77]  # Horiz position for panel labels
labelPosY = [0.97, 0.47]  # Vert position for panel labels

ACsummaryFileName = 'all_behaviour_ac_inactivation.npz'
ACcontrolFileName = 'all_behaviour_ac_inactivation_control.npz'
inactSummaryFileName = 'all_behaviour_inhib_inactivation.npz'
inactControlFileName = 'all_behaviour_inhib_inactivation_control.npz'

baseColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']
connectLineColour = figparams.colp['connectLine']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 2, wspace=0.3, hspace=0.4)
gs.update(top=0.97, bottom=0.08, left=0.03, right=0.98, wspace=0.5, hspace=0.3)

# --- correlation between size of laser effect and initial accuracy ---
if PANELS[0]:
    summaryDataFullPath = os.path.join(acDataDir, ACsummaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserAccuracy = summaryData['laserAccuracy']
    controlAccuracy = summaryData['controlAccuracy']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        summaryControlDataFullPath = os.path.join(acDataDir, ACcontrolFileName)
        summaryControlData = np.load(summaryControlDataFullPath)

        laserAccuracyControl = summaryControlData['laserAccuracy']
        controlAccuracyControl = summaryControlData['controlAccuracy']

        laserAccuracyCorrected = laserAccuracy - (laserAccuracyControl - controlAccuracyControl)

    else:
        laserAccuracyCorrected = laserAccuracy

    summaryDataFullPath = os.path.join(inactDataDir, inactSummaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserAccuracy = summaryData['PVlaserAccuracy']
    PVcontrolAccuracy = summaryData['PVcontrolAccuracy']
    SOMlaserAccuracy = summaryData['SOMlaserAccuracy']
    SOMcontrolAccuracy = summaryData['SOMcontrolAccuracy']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        summaryControlDataFullPath = os.path.join(inactDataDir, inactControlFileName)
        summaryControlData = np.load(summaryControlDataFullPath)

        PVlaserAccuracyControl = summaryControlData['PVlaserAccuracy']
        PVcontrolAccuracyControl = summaryControlData['PVcontrolAccuracy']
        SOMlaserAccuracyControl = summaryControlData['SOMlaserAccuracy']
        SOMcontrolAccuracyControl = summaryControlData['SOMcontrolAccuracy']

        PVlaserAccuracyCorrected = PVlaserAccuracy - (PVlaserAccuracyControl - PVcontrolAccuracyControl)
        SOMlaserAccuracyCorrected = SOMlaserAccuracy - (SOMlaserAccuracyControl - SOMcontrolAccuracyControl)

    else:
        PVlaserAccuracyCorrected = PVlaserAccuracy
        SOMlaserAccuracyCorrected = SOMlaserAccuracy

    changes = [laserAccuracyCorrected-controlAccuracy, PVlaserAccuracyCorrected-PVcontrolAccuracy, SOMlaserAccuracyCorrected-SOMcontrolAccuracy]
    controlAccs = [controlAccuracy, PVcontrolAccuracy, SOMcontrolAccuracy]
    colours = [PVColour, PVColour, SOMColour]
    faceColours = [PVColour, 'none', 'none']
    lineType = ['-', '--', '--']
    typeLabel = ['PV activated', 'PV inactivated', 'SOM inactivated']

    xLim = [50,90]

    for indBand, band in enumerate(possibleBands):
        axScatter = plt.subplot(gs[indBand,0])
        points = []

        for indType in range(len(changes)):
            l1, = plt.plot(controlAccs[indType][:,indBand], changes[indType][:,indBand], 'o', mec=colours[indType], mfc=faceColours[indType])
            points.append(l1)

            slope, intercept, rVal, pVal, stdErr = stats.linregress(controlAccs[indType][:,indBand], changes[indType][:,indBand])
            xvals = np.linspace(xLim[0], xLim[1], 200)
            yvals = slope * xvals + intercept
            plt.plot(xvals, yvals, ls=lineType[indType], color=colours[indType], zorder=-1)

            print("Linear regression with {0} on accuracy: \ncorrelation coefficient (r): {1}\np Value: {2}".format(
                typeLabel[indType], rVal, pVal))

        axScatter.legend(points, typeLabel, loc='best')

        axScatter.set_xlim(xLim)
        axScatter.set_xlabel('Initial Accuracy (%)', fontsize=fontSizeLabels)

        axScatter.set_ylabel('Change in Accuracy (%)', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

# --- correlation between size of laser effect and initial bias ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(acDataDir, ACsummaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserBias = summaryData['laserBias']
    controlBias = summaryData['controlBias']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        summaryControlDataFullPath = os.path.join(acDataDir, ACcontrolFileName)
        summaryControlData = np.load(summaryControlDataFullPath)

        laserBiasControl = summaryControlData['laserBias']
        controlBiasControl = summaryControlData['controlBias']

        laserBiasCorrected = laserBias - (laserBiasControl - controlBiasControl)

    else:
        laserBiasCorrected = laserBias

    summaryDataFullPath = os.path.join(inactDataDir, inactSummaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserBias = summaryData['PVlaserBias']
    PVcontrolBias = summaryData['PVcontrolBias']
    SOMlaserBias = summaryData['SOMlaserBias']
    SOMcontrolBias = summaryData['SOMcontrolBias']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        summaryControlDataFullPath = os.path.join(inactDataDir, inactControlFileName)
        summaryControlData = np.load(summaryControlDataFullPath)

        PVlaserBiasControl = summaryControlData['PVlaserBias']
        PVcontrolBiasControl = summaryControlData['PVcontrolBias']
        SOMlaserBiasControl = summaryControlData['SOMlaserBias']
        SOMcontrolBiasControl = summaryControlData['SOMcontrolBias']

        PVlaserBiasCorrected = PVlaserBias - (PVlaserBiasControl - PVcontrolBiasControl)
        SOMlaserBiasCorrected = SOMlaserBias - (SOMlaserBiasControl - SOMcontrolBiasControl)

    else:
        PVlaserBiasCorrected = PVlaserBias
        SOMlaserBiasCorrected = SOMlaserBias

    changes = [laserBiasCorrected-controlBias, PVlaserBiasCorrected-PVcontrolBias, SOMlaserBiasCorrected-SOMcontrolBias]
    controlBiases = [controlBias, PVcontrolBias, SOMcontrolBias]
    colours = [PVColour, PVColour, SOMColour]
    faceColours = [PVColour, 'none', 'none']
    lineType = ['-', '--', '--']
    typeLabel = ['PV activated', 'PV inactivated', 'SOM inactivated']

    xLim = [-1,1]

    for indBand, band in enumerate(possibleBands):
        axScatter = plt.subplot(gs[indBand,1])
        points = []

        for indType in range(len(changes)):
            l1, = plt.plot(controlBiases[indType][:,indBand], changes[indType][:,indBand], 'o', mec=colours[indType], mfc=faceColours[indType])
            points.append(l1)

            slope, intercept, rVal, pVal, stdErr = stats.linregress(controlBiases[indType][:,indBand], changes[indType][:,indBand])
            xvals = np.linspace(xLim[0], xLim[1], 200)
            yvals = slope * xvals + intercept
            plt.plot(xvals, yvals, ls=lineType[indType], color=colours[indType], zorder=-1)

            print("Linear regression with {0} on bias: \ncorrelation coefficient (r): {1}\np Value: {2}".format(
                typeLabel[indType], rVal, pVal))

        axScatter.legend(points, typeLabel, loc='best')

        axScatter.set_xlim(xLim)
        axScatter.set_xlabel('Initial Bias', fontsize=fontSizeLabels)

        axScatter.set_ylabel('Change in Bias', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

if CORRECTED:
    plt.suptitle('LASER CORRECTED')
else:
    plt.suptitle('NO CORRECTION')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)