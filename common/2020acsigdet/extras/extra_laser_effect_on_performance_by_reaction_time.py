import sys
sys.path.append('..')
import os
import numpy as np
from statsmodels.stats.proportion import proportion_confint

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import extraplots

import studyparams
import figparams
import behaviour_analysis_funcs as bf

SOM_ARCHT_MICE = studyparams.SOM_ARCHT_MICE
PV_ARCHT_MICE = studyparams.PV_ARCHT_MICE
PV_CHR2_MICE = studyparams.PV_CHR2_MICE
mouseType = [PV_CHR2_MICE, PV_ARCHT_MICE, SOM_ARCHT_MICE]
typeLabels = ['PV-ChR2', 'PV-ArchT', 'SOM-ArchT']

SAVE_FIGURE = 1
CIS = 0
outputDir = '/tmp/'
figFilename = 'FigX_effect_by_sampling_time'
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [10,8]  # In inches

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(3, 2)
gs.update(top=0.90, bottom=0.15, left=0.07, right=0.98, wspace=0.5, hspace=0.3)

ExcColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']
colours = [PVColour, PVColour, SOMColour]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

for indType, mice in enumerate(mouseType):
    allAccsControl = None
    allAccsLaser = None
    allToneReportsControl = None
    allToneReportsLaser = None
    for indMouse, mouse in enumerate(mice):
        if indType == 0:
            laserSessions = studyparams.miceDict[mouse]['3mW laser']
        else:
            laserSessions = studyparams.miceDict[mouse]['10mW laser']
        laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

        numLasers = np.unique(laserBehavData['laserSide'])
        numBands = np.unique(laserBehavData['currentBand'])
        numSNRs = np.unique(laserBehavData['currentSNR'])

        correct = laserBehavData['outcome'] == laserBehavData.labels['outcome']['correct']
        incorrect = laserBehavData['outcome'] == laserBehavData.labels['outcome']['error']
        rightChoice = laserBehavData['choice'] == laserBehavData.labels['choice']['right']
        leftChoice = laserBehavData['choice'] == laserBehavData.labels['choice']['left']

        if 'toneSide' in laserBehavData.keys():
            if laserBehavData['toneSide'][-1] == laserBehavData.labels['toneSide']['right']:
                toneChoice = rightChoice
                noiseChoice = leftChoice
            elif laserBehavData['toneSide'][-1] == laserBehavData.labels['toneSide']['left']:
                toneChoice = leftChoice
                noiseChoice = rightChoice
        else:
            # all tones meant go to right before introduction of 'toneSide' key
            toneChoice = rightChoice
            noiseChoice = leftChoice

        reactionTimes, decisionTimes = bf.get_reaction_times(mouse, laserSessions)

        trialsEachLaser = behavioranalysis.find_trials_each_type(laserBehavData['laserSide'], numLasers)

        binslow = np.linspace(0, 0.06, 7)
        binshigh = np.linspace(0.08, 0.2, 7)
        bins = np.concatenate((binslow, binshigh))
        nBins = len(bins) - 1

        # -- average accuracy for each reaction time --
        controlCorrect = correct & trialsEachLaser[:,0]
        controlIncorrect = incorrect & trialsEachLaser[:,0]

        laserCorrect = correct & trialsEachLaser[:, 1]
        laserIncorrect = incorrect & trialsEachLaser[:, 1]

        correctReactionTimes = reactionTimes[controlCorrect]
        correctReactionTimes = correctReactionTimes[np.isfinite(correctReactionTimes)]
        incorrectReactionTimes = reactionTimes[controlIncorrect]
        incorrectReactionTimes = incorrectReactionTimes[np.isfinite(incorrectReactionTimes)]

        correctReactionTimesLaser = reactionTimes[laserCorrect]
        correctReactionTimesLaser = correctReactionTimesLaser[np.isfinite(correctReactionTimesLaser)]
        incorrectReactionTimesLaser = reactionTimes[laserIncorrect]
        incorrectReactionTimesLaser = incorrectReactionTimesLaser[np.isfinite(incorrectReactionTimesLaser)]

        binCountsControlCorrect, bins = np.histogram(correctReactionTimes, bins=bins)
        binCountsControlIncorrect, bins = np.histogram(incorrectReactionTimes, bins=bins)

        binCountsLaserCorrect, bins = np.histogram(correctReactionTimesLaser, bins=bins)
        binCountsLaserIncorrect, bins = np.histogram(incorrectReactionTimesLaser, bins=bins)

        if allAccsControl is None:
            allAccsControl = np.zeros((len(mice), nBins))
            allAccsLaser = np.zeros_like(allAccsControl)

        accuraciesControl = 100.0 * binCountsControlCorrect/(binCountsControlCorrect+binCountsControlIncorrect)
        accuraciesLaser = 100.0 * binCountsLaserCorrect/(binCountsLaserCorrect+binCountsLaserIncorrect)

        allAccsControl[indMouse, :] = accuraciesControl
        allAccsLaser[indMouse, :] = accuraciesLaser

        # -- average tone reported for each reaction time --
        controlToneChoice = toneChoice & trialsEachLaser[:, 0]
        controlNoiseChoice = noiseChoice & trialsEachLaser[:, 0]

        laserToneChoice = toneChoice & trialsEachLaser[:, 1]
        laserNoiseChoice = noiseChoice & trialsEachLaser[:, 1]

        toneReactionTimes = reactionTimes[controlToneChoice]
        toneReactionTimes = correctReactionTimes[np.isfinite(correctReactionTimes)]
        noiseReactionTimes = reactionTimes[controlNoiseChoice]
        noiseReactionTimes = incorrectReactionTimes[np.isfinite(incorrectReactionTimes)]

        toneReactionTimesLaser = reactionTimes[laserToneChoice]
        toneReactionTimesLaser = correctReactionTimesLaser[np.isfinite(correctReactionTimesLaser)]
        noiseReactionTimesLaser = reactionTimes[laserNoiseChoice]
        noiseReactionTimesLaser = incorrectReactionTimesLaser[np.isfinite(incorrectReactionTimesLaser)]

        binCountsControlTone, bins = np.histogram(toneReactionTimes, bins=bins)
        binCountsControlNoise, bins = np.histogram(noiseReactionTimes, bins=bins)

        binCountsLaserTone, bins = np.histogram(toneReactionTimesLaser, bins=bins)
        binCountsLaserNoise, bins = np.histogram(noiseReactionTimesLaser, bins=bins)

        if allToneReportsControl is None:
            allToneReportsLaser = np.zeros((len(mice), nBins))
            allToneReportsControl = np.zeros_like(allToneReportsLaser)

        toneChoiceControl = 100.0 * binCountsControlTone / (binCountsControlTone + binCountsControlNoise)
        toneChoiceLaser = 100.0 * binCountsLaserTone / (binCountsLaserTone + binCountsLaserNoise)

        allToneReportsControl[indMouse, :] = toneChoiceControl
        allToneReportsLaser[indMouse, :] = toneChoiceLaser

    # -- make plots --
    axAccuracy = plt.subplot(gs[indType, 0])

    xVals = bins[:-1]
    medianControl = np.median(allAccsControl, axis=0)
    medianLaser = np.median(allAccsLaser, axis=0)
    plt.plot(xVals, medianControl, 'o-', color=ExcColour, lw=3, ms=9)
    plt.plot(xVals, medianLaser, 'o-', color=colours[indType], lw=3, ms=9)

    if not CIS:
        for indMouse in range(allAccsControl.shape[0]):
            plt.plot(xVals, allAccsControl[indMouse, :], '-', color=ExcColour, alpha=0.3)
            plt.plot(xVals, allAccsLaser[indMouse, :], '-', color=colours[indType], alpha=0.3)
    else:
        for indBin in xVals:
            CI = bf.bootstrap_median_CI(allAccsControl[:, indBin])
            # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
            plt.plot([indBin, indBin], CI, color=colours[indType], linewidth=1.5)  # error bars
            plt.plot([indBin - 0.2, indBin + 0.2], [CI[0], CI[0]], color=colours[indType], linewidth=1.5)  # bottom caps
            plt.plot([indBin - 0.2, indBin + 0.2], [CI[1], CI[1]], color=colours[indType], linewidth=1.5)  # top caps

    plt.plot([-10, 10], [0, 0], '--', color='0.5')

    axAccuracy.set_xlim(xVals[0] - 0.01, xVals[-1] + 0.01)
    axAccuracy.set_xticks(xVals)
    #axAccuracy.set_xticklabels(xVals)
    axAccuracy.set_xlabel('Sampling time (s)', fontsize=fontSizeLabels)

    yLim = [45, 95]
    axAccuracy.set_ylim(yLim)
    axAccuracy.set_ylabel('Accuracy (%)', fontsize=fontSizeLabels)

    plt.title(f'{typeLabels[indType]}')
    print("?")

    axToneReport = plt.subplot(gs[indType, 1])

    xVals = bins[:-1]
    medianControl = np.median(allToneReportsControl, axis=0)
    medianLaser = np.median(allToneReportsLaser, axis=0)
    plt.plot(xVals, medianControl, 'o-', color=ExcColour, lw=3, ms=9)
    plt.plot(xVals, medianLaser, 'o-', color=colours[indType], lw=3, ms=9)

    if not CIS:
        for indMouse in range(allToneReportsControl.shape[0]):
            plt.plot(xVals, allToneReportsControl[indMouse, :], '-', color=ExcColour, alpha=0.3)
            plt.plot(xVals, allToneReportsLaser[indMouse, :], '-', color=colours[indType], alpha=0.3)
    else:
        for indBin in xVals:
            CI = bf.bootstrap_median_CI(allToneReportsControl[:, indBin])
            # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
            plt.plot([indBin, indBin], CI, color=colours[indType], linewidth=1.5)  # error bars
            plt.plot([indBin - 0.2, indBin + 0.2], [CI[0], CI[0]], color=colours[indType], linewidth=1.5)  # bottom caps
            plt.plot([indBin - 0.2, indBin + 0.2], [CI[1], CI[1]], color=colours[indType], linewidth=1.5)  # top caps

    plt.plot([-10, 10], [0, 0], '--', color='0.5')

    axToneReport.set_xlim(xVals[0] - 0.01, xVals[-1] + 0.01)
    axToneReport.set_xticks(xVals)
    # axToneReport.set_xticklabels(xVals)
    axToneReport.set_xlabel('Sampling time (s)', fontsize=fontSizeLabels)

    yLim = [0, 100]
    axToneReport.set_ylim(yLim)
    axToneReport.set_ylabel('Tone reported (%)', fontsize=fontSizeLabels)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

