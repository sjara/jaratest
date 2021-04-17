import sys
sys.path.append('..')
import numpy as np
from statsmodels.stats.proportion import proportion_confint
from scipy import stats

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches

from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import extraplots

import studyparams

SOM_ARCHT_MICE = studyparams.SOM_ARCHT_MICE
PV_ARCHT_MICE = studyparams.PV_ARCHT_MICE
PV_CHR2_MICE = studyparams.PV_CHR2_MICE
mouseType = [PV_ARCHT_MICE, SOM_ARCHT_MICE, PV_CHR2_MICE]
mouseLabel = ['PV-ArchT', 'SOM-ArchT', 'PV-ChR2']
legendLabel = ['no PV', 'no SOM', 'PV activated']
laserColours = ['g', 'g', 'b']

# SOM_ARCHT_WT_MICE = studyparams.SOM_ARCHT_WT_MICE
# PV_ARCHT_MICE = studyparams.PV_ARCHT_MICE
# mouseType = [SOM_ARCHT_WT_MICE]
# mouseLabel = ['SOM-Cre']
# legendLabel = ['laser on']

ArchTlaserPower = 10
ChR2LaserPower = 3

def get_trials(behavData):
    numLasers = np.unique(behavData['laserSide'])
    numBands = np.unique(behavData['currentBand'])
    numSNRs = np.unique(behavData['currentSNR'])

    trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['laserSide'], numLasers,
                                                                   behavData['currentBand'], numBands)
    trialsEachSNR = behavioranalysis.find_trials_each_type(behavData['currentSNR'], numSNRs)

    trialsEachCond3Params = np.zeros((len(behavData['laserSide']), len(numLasers), len(numBands), len(numSNRs)), dtype=bool)
    for ind in range(len(numSNRs)):
        trialsEachCond3Params[:, :, :, ind] = trialsEachCond & trialsEachSNR[:, ind][:, np.newaxis, np.newaxis]

    incorrect = behavData['outcome'] == behavData.labels['outcome']['error']
    correct = behavData['outcome'] == behavData.labels['outcome']['correct']
    rightChoice = behavData['choice'] == behavData.labels['choice']['right']
    leftChoice = behavData['choice'] == behavData.labels['choice']['left']

    if 'toneSide' in behavData.keys():
        if behavData['toneSide'][-1] == behavData.labels['toneSide']['right']:
            toneChoice = rightChoice
            noiseChoice = leftChoice
        elif behavData['toneSide'][-1] == behavData.labels['toneSide']['left']:
            toneChoice = leftChoice
            noiseChoice = rightChoice
    else:
        # all tones meant go to right before introduction of 'toneSide' key
        toneChoice = rightChoice
        noiseChoice = leftChoice

    return correct, incorrect, toneChoice, noiseChoice, trialsEachCond3Params, [numLasers, numBands, numSNRs]

def get_plot_inputs(correct, incorrect, toneChoice, noiseChoice, trialsEachCond):
    psyCurves = np.zeros(trialsEachCond.shape[1:])
    upperErrorBars = np.zeros_like(psyCurves)
    lowerErrorBars = np.zeros_like(psyCurves)

    for band in range(trialsEachCond.shape[2]):
        for laser in range(trialsEachCond.shape[1]):
            numSNRs = trialsEachCond.shape[3]
            thisPsyCurve = np.zeros(numSNRs)
            upperErrorBar = np.zeros(numSNRs)
            lowerErrorBar = np.zeros(numSNRs)
            for snr in range(numSNRs):
                toneChoiceThisCond = toneChoice[trialsEachCond[:, laser, band, snr]]
                noiseChoiceThisCond = noiseChoice[trialsEachCond[:, laser, band, snr]]
                thisPsyCurve[snr] = 100.0 * np.sum(toneChoiceThisCond) / (
                            np.sum(toneChoiceThisCond) + np.sum(noiseChoiceThisCond))

                CIthisSNR = np.array(proportion_confint(np.sum(toneChoiceThisCond),
                                       (np.sum(toneChoiceThisCond) + np.sum(noiseChoiceThisCond)), method='wilson'))
                upperErrorBar[snr] = 100.0 * CIthisSNR[1] - thisPsyCurve[snr]
                lowerErrorBar[snr] = thisPsyCurve[snr] - 100.0 * CIthisSNR[0]

            psyCurves[laser, band, :] = thisPsyCurve
            upperErrorBars[laser, band, :] = upperErrorBar
            lowerErrorBars[laser, band, :] = lowerErrorBar

    accuracies = np.zeros(trialsEachCond.shape[1:-1])
    biases = np.zeros_like(accuracies)
    trialsEachCond = np.sum(trialsEachCond, axis=3).astype(bool)

    for band in range(trialsEachCond.shape[2]):
        for laser in range(trialsEachCond.shape[1]):
            trialsThisCond = trialsEachCond[:, laser, band]
            accuracies[laser, band] = 100.0 * np.sum(correct[trialsThisCond]) / (np.sum(correct[trialsThisCond]) + np.sum(incorrect[trialsThisCond]))
            biases[laser, band] = 1.0 * (np.sum(toneChoice[trialsThisCond]) - np.sum(noiseChoice[trialsThisCond])) / \
                          (np.sum(toneChoice[trialsThisCond]) + np.sum(noiseChoice[trialsThisCond]))

    return psyCurves, upperErrorBars, lowerErrorBars, accuracies, biases


def plot_report(mouse, laserPower, indType):
    fig = plt.gcf()
    fig.clf()
    fig.set_facecolor('w')

    gs = gridspec.GridSpec(2, 2, width_ratios=[1.5, 1])
    gs.update(top=0.90, bottom=0.08, left=0.12, right=0.99, wspace=0.5, hspace=0.3)

    laserSessions = studyparams.miceDict[mouse][f'{laserPower}mW laser']
    laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

    controlSessions = studyparams.miceDict[mouse][f'{laserPower}mW control']
    controlBehavData = behavioranalysis.load_many_sessions(mouse, controlSessions)

    laserCorrect, laserIncorrect, laserToneChoice, laserNoiseChoice, laserTrialsEachCond3Params, labels = get_trials(laserBehavData)
    laserPsyCurves, laserUE, laserLE, laserAcc, laserBias = get_plot_inputs(laserCorrect, laserIncorrect, laserToneChoice,
                                                                            laserNoiseChoice, laserTrialsEachCond3Params)

    controlCorrect, controlIncorrect, controlToneChoice, controlNoiseChoice, controlTrialsEachCond3Params, labels = get_trials(controlBehavData)
    controlPsyCurves, controlUE, controlLE, controlAcc, controlBias = get_plot_inputs(controlCorrect, controlIncorrect,
                                                                            controlToneChoice, controlNoiseChoice,
                                                                            controlTrialsEachCond3Params)

    numLasers = len(labels[0])
    numBands = len(labels[1])
    numSNRs = len(labels[2])

    psyCurves = np.concatenate((laserPsyCurves, controlPsyCurves), axis=0)
    upperErrors = np.concatenate((laserUE, controlUE), axis=0)
    lowerErrors = np.concatenate((laserLE, controlLE), axis=0)

    accuracy = np.concatenate((laserAcc, controlAcc), axis=0)
    bias = np.concatenate((laserBias, controlBias), axis=0)

    # -- plot psychometric curves for each bandwidth and laser presentation --
    axPsyCurves = gs[:,0]
    gs2 = gridspec.GridSpecFromSubplotSpec(numBands, 1, subplot_spec=axPsyCurves, wspace=0.3, hspace=0.4)

    lineColours = ['k', laserColours[indType], 'orange', '0.3']
    edgeColours = ['k', laserColours[indType], 'orange', 'orange']
    fillColours = ['k', 'white', 'orange', 'k']
    lineStyles = ['-', '--', '-', '-']
    lines = []

    for band in range(numBands):
        axThisPsyCurve = plt.subplot(gs2[band,0])
        for laser in range(numLasers+2):
            line, = plt.plot(range(numSNRs), psyCurves[laser,band,:], color=lineColours[laser], mec=edgeColours[laser], marker='o',
                     mfc=fillColours[laser], ls=lineStyles[laser], lw=3, ms=10, zorder=-laser)
            plt.errorbar(range(numSNRs), psyCurves[laser,band,:], yerr=[lowerErrors[laser,band,:], upperErrors[laser,band,:]], fmt='none',
                         color=lineColours[laser], lw=2, capsize=5, capthick=1)
            plt.title(f'{labels[1][band]} octaves')

            lines.append(line)

        axThisPsyCurve.set_ylim(0, 100)
        axThisPsyCurve.set_ylabel('% trials tone reported')
        extraplots.boxoff(axThisPsyCurve)

        axThisPsyCurve.set_xticks(range(numSNRs))
        axThisPsyCurve.set_xticklabels(labels[2])
    axThisPsyCurve.set_xlabel('SNR (dB)')

    legendLabels = ['baseline', legendLabel[indType], 'laser outside', 'laser outside baseline']
    axThisPsyCurve.legend(lines, legendLabels)
    # for indColor, colour in enumerate(colours):
    #     patches.append(mpatches.Patch(color=colour, label=legendLabels[indColor]))
    # plt.legend(handles=patches, borderaxespad=0.3, prop={'size': 12}, loc='best')

    # -- plot accuracies for each bandwidth and laser presentation --
    axAccuracy = plt.subplot(gs[0, 1])
    laserTrialsEachCond = np.sum(laserTrialsEachCond3Params, axis=3).astype(bool)
    controlTrialsEachCond = np.sum(controlTrialsEachCond3Params, axis=3).astype(bool)

    barLoc = np.array([-0.3, -0.1, 0.1, 0.3])
    xLocs = np.arange(numBands)
    xTickLabels = labels[1]

    for band in range(numBands):
        xVals = barLoc + xLocs[band]
        plt.plot(xVals, accuracy[:,band], 'k-', lw=2)
        l1, = plt.plot(xVals[0], accuracy[0,band], 'o', mec='k', mfc='k', ms=10)
        l2, = plt.plot(xVals[1], accuracy[1,band], 'o', mec=edgeColours[indType], mfc='white', ms=10)
        l3, = plt.plot(xVals[2], accuracy[2,band], 'o', mec='orange', mfc='orange', ms=10)
        l4, = plt.plot(xVals[3], accuracy[3, band], 'o', mec='orange', mfc='k', ms=10)

    axAccuracy.set_xlim(xLocs[0] - 0.5, xLocs[-1] + 0.5)
    axAccuracy.set_xticks(xLocs)
    axAccuracy.set_xticklabels(labels[0])
    axAccuracy.set_xlabel('Masker bandwidth (oct)')

    yLims = axAccuracy.get_ylim()
    yLims = [yLims[0] - 10, yLims[1] + 10]
    axAccuracy.set_ylim(yLims)
    axAccuracy.set_ylabel('Accuracy (%)')

    for band in range(numBands):
        xVals = barLoc + xLocs[band]
        pValLasers = stats.mannwhitneyu(laserCorrect[laserTrialsEachCond[:, 1, band]],
                                        controlCorrect[controlTrialsEachCond[:, 1, band]])[1]
        if pValLasers < 0.05:
            extraplots.significance_stars(xVals[1:3], yLims[1] * 0.96, yLims[1] * 0.01, gapFactor=0.35, starSize=7)
        else:
            extraplots.significance_stars(xVals[1:3], yLims[1] * 0.96, yLims[1] * 0.01, gapFactor=0.35, starSize=7,
                                          starString='ns')
        # axAccuracy.text(xLocs[band], 0.8 * yLim[1], f'p = {pValLasers:.3f}', fontsize=8, va='center', ha='center',
        #                 color='k', clip_on=False)

        pValControls = stats.mannwhitneyu(laserCorrect[laserTrialsEachCond[:, 0, band]],
                                        controlCorrect[controlTrialsEachCond[:, 0, band]])[1]
        if pValControls < 0.05:
            extraplots.significance_stars([xVals[0],xVals[3]], yLims[1] * 0.99, yLims[1] * 0.01, gapFactor=0.2, starSize=7)
        else:
            extraplots.significance_stars([xVals[0],xVals[3]], yLims[1] * 0.99, yLims[1] * 0.01, gapFactor=0.2, starSize=7,
                                          starString='ns')

    extraplots.boxoff(axAccuracy)

    # -- plot bias for each bandwidth and laser presentation --
    axBias = plt.subplot(gs[1, 1])

    barLoc = np.array([-0.3, -0.1, 0.1, 0.3])
    xLocs = np.arange(numBands)
    xTickLabels = labels[1]

    for band in range(numBands):
        xVals = barLoc + xLocs[band]
        plt.plot(xVals, bias[:,band], 'k-', lw=2)
        l1, = plt.plot(xVals[0], bias[0,band], 'o', mec='k', mfc='k', ms=10)
        l2, = plt.plot(xVals[1], bias[1,band], 'o', mec=edgeColours[indType], mfc='white', ms=10)
        l3, = plt.plot(xVals[2], bias[2,band], 'o', mec='orange', mfc='orange', ms=10)
        l4, = plt.plot(xVals[3], bias[3, band], 'o', mec='orange', mfc='k', ms=10)

        # pVal = stats.ranksums(toneChoice[trialsEachCond[:, 0, band]], toneChoice[trialsEachCond[:, 1, band]])[1]
        # yLim = axBias.get_ylim()
        # if pVal < 0.05:
        #     hs, = axBias.plot(xLocs[band], 0.9 * yLim[1], '*', mfc='k', mec='None', clip_on=False)
        #     hs.set_markersize(8)
        # else:
        #     axBias.text(xLocs[band], 0.9 * yLim[1], 'ns', fontsize=8, va='center', ha='center', color='k',
        #                 clip_on=False)
        # axBias.text(xLocs[band], 0.8 * yLim[1], f'p = {pVal:.3f}', fontsize=8, va='center', ha='center', color='k',
        #             clip_on=False)

    axBias.set_xlim(xLocs[0] - 0.5, xLocs[-1] + 0.5)
    axBias.set_xticks(xLocs)
    axBias.set_xticklabels(labels[1])
    axBias.set_xlabel('Masker bandwidth (oct)')

    yLims = axBias.get_ylim()
    yLims = [yLims[0] - 0.1, yLims[1] + 0.1]
    axBias.set_ylim(yLims)
    axBias.set_ylabel('Bias')

    for band in range(numBands):
        xVals = barLoc + xLocs[band]
        pValLasers = stats.mannwhitneyu(laserToneChoice[laserTrialsEachCond[:, 1, band]],
                                        controlToneChoice[controlTrialsEachCond[:, 1, band]])[1]
        if pValLasers < 0.05:
            extraplots.significance_stars(xVals[1:3], yLims[1] * 0.87, yLims[1] * 0.05, gapFactor=0.35, starSize=7)
        else:
            extraplots.significance_stars(xVals[1:3], yLims[1] * 0.87, yLims[1] * 0.05, gapFactor=0.35, starSize=7,
                                          starString='ns')
        # axAccuracy.text(xLocs[band], 0.8 * yLim[1], f'p = {pValLasers:.3f}', fontsize=8, va='center', ha='center',
        #                 color='k', clip_on=False)

        pValControls = stats.mannwhitneyu(laserToneChoice[laserTrialsEachCond[:, 0, band]],
                                        controlToneChoice[controlTrialsEachCond[:, 0, band]])[1]
        if pValControls < 0.05:
            extraplots.significance_stars([xVals[0],xVals[3]], yLims[1] * 0.99, yLims[1] * 0.05, gapFactor=0.2, starSize=7)
        else:
            extraplots.significance_stars([xVals[0],xVals[3]], yLims[1] * 0.99, yLims[1] * 0.05, gapFactor=0.2, starSize=7,
                                          starString='ns')

    # -- stats --
    # for band in range(numBands):
    #     for laser in range(trialsEachCond.shape[1]):
    #         trialsThisCond = trialsEachCond[:, laser, band]
    #         accuracies[laser, band] = 100.0 * np.sum(correct[trialsThisCond]) / (np.sum(correct[trialsThisCond]) + np.sum(incorrect[trialsThisCond]))
    #         biases[laser, band] = 1.0 * (np.sum(toneChoice[trialsThisCond]) - np.sum(noiseChoice[trialsThisCond])) / \
    #                       (np.sum(toneChoice[trialsThisCond]) + np.sum(noiseChoice[trialsThisCond]))

    extraplots.boxoff(axBias)
    if indType == 2:
        plt.suptitle(mouse + ' {}mW ({})'.format(ChR2LaserPower, mouseLabel[indType]))
        figFilename = f'{mouse}_behav_report_{ChR2LaserPower}mW'
    else:
        plt.suptitle(mouse + ' {}mW ({})'.format(ArchTlaserPower, mouseLabel[indType]))
        figFilename = f'{mouse}_behav_report_{ArchTlaserPower}mW'

    extraplots.save_figure(figFilename, 'png', [7, 8], '/tmp/', facecolor='w')
    #plt.show()

for indType, mice in enumerate(mouseType):
    for mouse in mice:
        if indType == 2:
            laserSessions = studyparams.miceDict[mouse][f'{ChR2LaserPower}mW laser']
            plot_report(mouse, ChR2LaserPower, indType)
        else:
            try:
                laserSessions = studyparams.miceDict[mouse][f'{ArchTlaserPower}mW laser']
            except(KeyError):
                pass
            else:
                plot_report(mouse, ArchTlaserPower, indType)

    #     break
    # break
