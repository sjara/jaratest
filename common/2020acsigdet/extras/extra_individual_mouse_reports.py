import os
import numpy as np
from statsmodels.stats.proportion import proportion_confint

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

# SOM_ARCHT_WT_MICE = studyparams.SOM_ARCHT_WT_MICE
# PV_ARCHT_MICE = studyparams.PV_ARCHT_MICE
# mouseType = [SOM_ARCHT_WT_MICE]
# mouseLabel = ['SOM-Cre']
# legendLabel = ['laser on']

# 'control' or 'laser'
sessionType = 'control'
#sessionType = 'laser'

for indType, mice in enumerate(mouseType):
    for mouse in mice:
        fig = plt.gcf()
        fig.clf()
        fig.set_facecolor('w')

        gs = gridspec.GridSpec(1, 3, width_ratios=[1.6, 1, 1])
        gs.update(top=0.90, bottom=0.15, left=0.07, right=0.98, wspace=0.5, hspace=0.3)

        if indType == 2:
            laserSessions = studyparams.miceDict[mouse][f'3mW {sessionType}']
        else:
            laserSessions = studyparams.miceDict[mouse][f'10mW {sessionType}']
        laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

        numLasers = np.unique(laserBehavData['laserSide'])
        numBands = np.unique(laserBehavData['currentBand'])
        numSNRs = np.unique(laserBehavData['currentSNR'])

        trialsEachCond = behavioranalysis.find_trials_each_combination(laserBehavData['laserSide'], numLasers,
                                                                       laserBehavData['currentBand'], numBands)
        trialsEachSNR = behavioranalysis.find_trials_each_type(laserBehavData['currentSNR'], numSNRs)

        trialsEachCond3Params = np.zeros(
            (len(laserBehavData['laserSide']), len(numLasers), len(numBands), len(numSNRs)), dtype=bool)
        for ind in range(len(numSNRs)):
            trialsEachCond3Params[:, :, :, ind] = trialsEachCond & trialsEachSNR[:, ind][:, np.newaxis, np.newaxis]

        valid = laserBehavData['valid'].astype(bool)
        correct = laserBehavData['outcome'] == laserBehavData.labels['outcome']['correct']
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

        # -- plot psychometric curves for each bandwidth and laser presentation --
        axPsyCurve = plt.subplot(gs[0, 0])

        bandColours = ['r', 'k', 'b']
        laserLines = ['-', '--']
        patches = []

        for band in range(len(numBands)):
            laserFill = [bandColours[band], 'white']
            for laser in range(len(numLasers)):
                thisPsyCurve = np.zeros(len(numSNRs))
                upperErrorBar = np.zeros(len(numSNRs))
                lowerErrorBar = np.zeros(len(numSNRs))
                for snr in range(len(numSNRs)):
                    toneChoiceThisCond = toneChoice[trialsEachCond3Params[:, laser, band, snr]]
                    noiseChoiceThisCond = noiseChoice[trialsEachCond3Params[:, laser, band, snr]]
                    thisPsyCurve[snr] = 100.0 * np.sum(toneChoiceThisCond) / (np.sum(toneChoiceThisCond) + np.sum(noiseChoiceThisCond))

                    CIthisSNR = np.array(
                        proportion_confint(np.sum(toneChoiceThisCond), (np.sum(toneChoiceThisCond) + np.sum(noiseChoiceThisCond)), method='wilson'))
                    upperErrorBar[snr] = 100.0 * CIthisSNR[1] - thisPsyCurve[snr]
                    lowerErrorBar[snr] = thisPsyCurve[snr] - 100.0 * CIthisSNR[0]

                plt.plot(range(len(numSNRs)), thisPsyCurve, color=bandColours[band], mec=bandColours[band], marker='o',
                         mfc=laserFill[laser], ls=laserLines[laser], lw=3, ms=10, zorder=-laser)
                plt.errorbar(range(len(numSNRs)), thisPsyCurve, yerr=[lowerErrorBar, upperErrorBar], fmt='none',
                             color=bandColours[band], lw=2, capsize=5, capthick=1)
            patches.append(mpatches.Patch(color=bandColours[band], label=numBands[band]))
        plt.legend(handles=patches, borderaxespad=0.3, prop={'size': 12}, loc='best')

        axPsyCurve.set_xticks(range(len(numSNRs)))
        axPsyCurve.set_xticklabels(numSNRs)
        axPsyCurve.set_xlabel('SNR (dB)')

        axPsyCurve.set_ylim(0, 100)
        axPsyCurve.set_ylabel('% trials tone reported')

        extraplots.boxoff(axPsyCurve)

        # -- plot accuracies for each bandwidth and laser presentation --
        axAccuracy = plt.subplot(gs[0, 1])

        barLoc = np.array([-0.24, 0.24])
        xLocs = np.arange(len(numBands))
        xTickLabels = numBands

        for band in range(len(numBands)):
            accuracy = np.zeros(len(numLasers))
            for laser in range(len(numLasers)):
                accuracy[laser] = 100.0 * np.sum(correct[trialsEachCond[:, laser, band]]) / np.sum(
                    valid[trialsEachCond[:, laser, band]])

            xVals = barLoc + xLocs[band]
            plt.plot(xVals, accuracy, 'k-', lw=2)
            l1, = plt.plot(xVals[0], accuracy[0], 'o', mec='k', mfc='k', ms=10)
            l2, = plt.plot(xVals[1], accuracy[1], 'o', mec='k', mfc='white', ms=10)

        axAccuracy.legend([l1, l2], ['control', legendLabel[indType]])

        axAccuracy.set_xlim(xLocs[0] - 0.5, xLocs[-1] + 0.5)
        axAccuracy.set_xticks(xLocs)
        axAccuracy.set_xticklabels(numBands)
        axAccuracy.set_xlabel('Masker bandwidth (oct)')

        yLims = axAccuracy.get_ylim()
        axAccuracy.set_ylim(yLims[0] - 10, yLims[1] + 10)
        axAccuracy.set_ylabel('Accuracy (%)')

        extraplots.boxoff(axAccuracy)

        # -- plot bias for each bandwidth and laser presentation --
        axBias = plt.subplot(gs[0, 2])

        barLoc = np.array([-0.24, 0.24])
        xLocs = np.arange(len(numBands))
        xTickLabels = numBands

        for band in range(len(numBands)):
            bias = np.zeros(len(numLasers))
            for laser in range(len(numLasers)):
                trialsThisCond = trialsEachCond[:, laser, band]
                bias[laser] = 1.0 * (np.sum(toneChoice[trialsThisCond]) - np.sum(noiseChoice[trialsThisCond])) / \
                              (np.sum(toneChoice[trialsThisCond]) + np.sum(noiseChoice[trialsThisCond]))

            xVals = barLoc + xLocs[band]
            plt.plot(xVals, bias, 'k-', lw=2)
            l1, = plt.plot(xVals[0], bias[0], 'o', mec='k', mfc='k', ms=10)
            l2, = plt.plot(xVals[1], bias[1], 'o', mec='k', mfc='white', ms=10)

        axBias.legend([l1, l2], ['control', legendLabel[indType]])

        axBias.set_xlim(xLocs[0] - 0.5, xLocs[-1] + 0.5)
        axBias.set_xticks(xLocs)
        axBias.set_xticklabels(numBands)
        axBias.set_xlabel('Masker bandwidth (oct)')

        yLims = axBias.get_ylim()
        axBias.set_ylim(yLims[0] - 0.1, yLims[1] + 0.1)
        axBias.set_ylabel('Bias')

        extraplots.boxoff(axBias)

        plt.suptitle(mouse + ' ({})'.format(mouseLabel[indType]))

        figFilename = f'{mouse}_behav_report_{sessionType}'
        extraplots.save_figure(figFilename, 'png', [9, 4], '/tmp/')
