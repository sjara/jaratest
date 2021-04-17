import sys
sys.path.append('..')
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.proportion import proportion_confint
from scipy import stats

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches

from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import extraplots

import behaviour_analysis_funcs as funcs
import studyparams

dbName = 'good_sessions.csv'
# dataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
dbPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
sessionDB = pd.read_csv(dbPath)

dbName = 'good_mice.csv'
# dataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
dbPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
mouseDB = pd.read_csv(dbPath)

mouseRow = mouseDB.query('strain=="PVArchT"')
PV_ARCHT_MICE = mouseRow['mice'].apply(eval).iloc[-1]
mouseRow = mouseDB.query('strain=="SOMArchT"')
SOM_ARCHT_MICE = mouseRow['mice'].apply(eval).iloc[-1]
mouseRow = mouseDB.query('strain=="PVChR2"')
PV_CHR2_MICE = mouseRow['mice'].apply(eval).iloc[-1]
mouseType = [PV_ARCHT_MICE, SOM_ARCHT_MICE, PV_CHR2_MICE]
trialType = ['laser', 'control']
mouseLabel = ['PV-ArchT', 'SOM-ArchT', 'PV-ChR2']
legendLabel = ['no PV', 'no SOM', 'PV activated']
laserColours = ['g', 'g', 'b']

ArchTlaserPower = 10
ChR2LaserPower = 3

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

    hitRates = np.zeros(trialsEachCond.shape[1:-1])
    FArates = np.zeros_like(hitRates)
    dprimes = np.zeros_like(hitRates)
    trialsEachCond = np.sum(trialsEachCond, axis=3).astype(bool)

    for band in range(trialsEachCond.shape[2]):
        for laser in range(trialsEachCond.shape[1]):
            trialsThisCond = trialsEachCond[:, laser, band]

            thisCorrect = correct[trialsThisCond]
            thisIncorrect = incorrect[trialsThisCond]
            thisToneChoice = toneChoice[trialsThisCond]
            thisNoiseChoice = noiseChoice[trialsThisCond]

            toneTrials = np.sum(thisCorrect & thisToneChoice) + np.sum(thisIncorrect & thisNoiseChoice)
            noiseTrials = np.sum(thisCorrect & thisNoiseChoice) + np.sum(thisIncorrect & thisToneChoice)

            thisHitRate = np.sum(thisCorrect & thisToneChoice) / toneTrials
            thisFARate = np.sum(thisIncorrect & thisToneChoice) / noiseTrials

            hitRates[laser, band] = thisHitRate
            FArates[laser, band] = thisFARate
            dprimes[laser, band] = (stats.norm.ppf(thisHitRate) - stats.norm.ppf(thisFARate)) / np.sqrt(2)

    return psyCurves, upperErrorBars, lowerErrorBars, hitRates, FArates, dprimes


def plot_report(mouse, laserPower, indType):
    fig = plt.gcf()
    fig.clf()
    fig.set_facecolor('w')

    gs = gridspec.GridSpec(1, 2, width_ratios=[1.5, 1])
    gs.update(top=0.90, bottom=0.08, left=0.12, right=0.99, wspace=0.5, hspace=0.3)

    sessionTypeName = f'{laserPower}mW laser'
    dbRow = sessionDB.query('mouse==@mouse and sessionType==@sessionTypeName')
    laserSessions = dbRow['goodSessions'].apply(eval).iloc[-1]
    laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

    sessionTypeName = f'{laserPower}mW control'
    controlSessions = studyparams.miceDict[mouse][f'{laserPower}mW control']
    dbRow = sessionDB.query('mouse==@mouse and sessionType==@sessionTypeName')
    controlSessions = dbRow['goodSessions'].apply(eval).iloc[-1]
    controlBehavData = behavioranalysis.load_many_sessions(mouse, controlSessions)

    laserCorrect, laserIncorrect, laserToneChoice, laserNoiseChoice, laserTrialsEachCond3Params, labels = funcs.get_trials(laserBehavData)
    laserPsyCurves, laserUE, laserLE, laserHits, laserFAs, laserdprimes = get_plot_inputs(laserCorrect, laserIncorrect, laserToneChoice,
                                                                            laserNoiseChoice, laserTrialsEachCond3Params)
    laserTrialsEachCond = behavioranalysis.find_trials_each_combination(laserBehavData['laserSide'], np.unique(laserBehavData['laserSide']),
                                                                        laserBehavData['currentBand'], np.unique(laserBehavData['currentBand']))

    controlCorrect, controlIncorrect, controlToneChoice, controlNoiseChoice, controlTrialsEachCond3Params, labels = funcs.get_trials(controlBehavData)
    controlPsyCurves, controlUE, controlLE, controlHits, controlFAs, controldprimes = get_plot_inputs(controlCorrect, controlIncorrect,
                                                                            controlToneChoice, controlNoiseChoice,
                                                                            controlTrialsEachCond3Params)
    controlTrialsEachCond = behavioranalysis.find_trials_each_combination(controlBehavData['laserSide'], np.unique(controlBehavData['laserSide']),
                                                                    controlBehavData['currentBand'], np.unique(controlBehavData['currentBand']))

    numLasers = len(labels[0])
    numBands = len(labels[1])
    numSNRs = len(labels[2])

    psyCurves = np.concatenate((laserPsyCurves, controlPsyCurves), axis=0)
    upperErrors = np.concatenate((laserUE, controlUE), axis=0)
    lowerErrors = np.concatenate((laserLE, controlLE), axis=0)

    hits = np.concatenate((laserHits, controlHits), axis=0)
    FAs = np.concatenate((laserFAs, controlFAs), axis=0)
    dprimes = np.concatenate((laserdprimes, controldprimes), axis=0)

    # -- plot psychometric curves for each bandwidth and laser presentation --
    axPsyCurves = gs[0,0]
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

        # -- stats --
        conTable = np.zeros((2, 2, 2))  # laser off/on, tone/noise choice, exp/control session
        conTable[0, 0, 0] = np.sum(laserToneChoice[laserTrialsEachCond[:, 0, band]])
        conTable[0, 1, 0] = np.sum(laserNoiseChoice[laserTrialsEachCond[:, 0, band]])
        conTable[1, 0, 0] = np.sum(laserToneChoice[laserTrialsEachCond[:, 1, band]])
        conTable[1, 1, 0] = np.sum(laserNoiseChoice[laserTrialsEachCond[:, 1, band]])
        conTable[0, 0, 1] = np.sum(controlToneChoice[controlTrialsEachCond[:, 0, band]])
        conTable[0, 1, 1] = np.sum(controlNoiseChoice[controlTrialsEachCond[:, 0, band]])
        conTable[1, 0, 1] = np.sum(controlToneChoice[controlTrialsEachCond[:, 1, band]])
        conTable[1, 1, 1] = np.sum(controlNoiseChoice[controlTrialsEachCond[:, 1, band]])

        conTableAnalysis = sm.stats.StratifiedTable(conTable)
        pVal = conTableAnalysis.test_null_odds(correction=True).pvalue
        pVal2 = stats.mannwhitneyu(laserToneChoice[laserTrialsEachCond[:, 0, band]], laserToneChoice[laserTrialsEachCond[:, 1, band]])[1]
        pVal3 = stats.mannwhitneyu(controlToneChoice[controlTrialsEachCond[:, 0, band]], controlToneChoice[controlTrialsEachCond[:, 1, band]])[1]

        axThisPsyCurve.annotate(f'laser in vs. out pval = {pVal:.3f}', xy=(0.14, 0.89 - band*0.48), xycoords='figure fraction', fontsize=8)
        axThisPsyCurve.annotate(f'laser in on vs. off pval = {pVal2:.3f}', xy=(0.14, 0.875 - band * 0.48), xycoords='figure fraction', fontsize=8)
        axThisPsyCurve.annotate(f'laser out on vs. off pval = {pVal3:.3f}', xy=(0.14, 0.86 - band * 0.48), xycoords='figure fraction', fontsize=8)


    axThisPsyCurve.set_xlabel('SNR (dB)')

    legendLabels = ['baseline', legendLabel[indType], 'laser outside', 'laser outside baseline']
    axThisPsyCurve.legend(lines, legendLabels)
    # for indColor, colour in enumerate(colours):
    #     patches.append(mpatches.Patch(color=colour, label=legendLabels[indColor]))
    # plt.legend(handles=patches, borderaxespad=0.3, prop={'size': 12}, loc='best')

    axSummaries = gs[0,1]
    gs3 = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=axSummaries, wspace=0.3, hspace=0.4)

    # -- plot hit rates for each bandwidth and laser presentation --
    axHits = plt.subplot(gs3[0, 0])
    laserTrialsEachCond = np.sum(laserTrialsEachCond3Params, axis=3).astype(bool)
    controlTrialsEachCond = np.sum(controlTrialsEachCond3Params, axis=3).astype(bool)

    barLoc = np.array([-0.3, -0.1, 0.1, 0.3])
    xLocs = np.arange(numBands)
    xTickLabels = labels[1]

    for band in range(numBands):
        xVals = barLoc + xLocs[band]
        plt.plot(xVals, hits[:,band], 'k-', lw=2)
        l1, = plt.plot(xVals[0], hits[0,band], 'o', mec='k', mfc='k', ms=10)
        l2, = plt.plot(xVals[1], hits[1,band], 'o', mec=edgeColours[indType], mfc='white', ms=10)
        l3, = plt.plot(xVals[2], hits[2,band], 'o', mec='orange', mfc='orange', ms=10)
        l4, = plt.plot(xVals[3], hits[3, band], 'o', mec='orange', mfc='k', ms=10)

    axHits.set_xlim(xLocs[0] - 0.5, xLocs[-1] + 0.5)
    axHits.set_xticks(xLocs)
    axHits.set_xticklabels(labels[1])
    axHits.set_xlabel('Masker bandwidth (oct)')

    yLims = axHits.get_ylim()
    yLims = [yLims[0] - 0.1, yLims[1] + 0.1]
    axHits.set_ylim(yLims)
    axHits.set_ylabel('Hit Rate')

    # for band in range(numBands):
    #     xVals = barLoc + xLocs[band]
    #     pValLasers = stats.mannwhitneyu(laserCorrect[laserTrialsEachCond[:, 1, band]],
    #                                     controlCorrect[controlTrialsEachCond[:, 1, band]])[1]
    #     if pValLasers < 0.05:
    #         extraplots.significance_stars(xVals[1:3], yLims[1] * 0.96, yLims[1] * 0.01, gapFactor=0.35, starSize=7)
    #     else:
    #         extraplots.significance_stars(xVals[1:3], yLims[1] * 0.96, yLims[1] * 0.01, gapFactor=0.35, starSize=7,
    #                                       starString='ns')
    #     # axAccuracy.text(xLocs[band], 0.8 * yLim[1], f'p = {pValLasers:.3f}', fontsize=8, va='center', ha='center',
    #     #                 color='k', clip_on=False)
    #
    #     pValControls = stats.mannwhitneyu(laserCorrect[laserTrialsEachCond[:, 0, band]],
    #                                     controlCorrect[controlTrialsEachCond[:, 0, band]])[1]
    #     if pValControls < 0.05:
    #         extraplots.significance_stars([xVals[0],xVals[3]], yLims[1] * 0.99, yLims[1] * 0.01, gapFactor=0.2, starSize=7)
    #     else:
    #         extraplots.significance_stars([xVals[0],xVals[3]], yLims[1] * 0.99, yLims[1] * 0.01, gapFactor=0.2, starSize=7,
    #                                       starString='ns')

    extraplots.boxoff(axHits)

    # -- plot FA rate for each bandwidth and laser presentation --
    axFA = plt.subplot(gs3[1, 0])

    barLoc = np.array([-0.3, -0.1, 0.1, 0.3])
    xLocs = np.arange(numBands)
    xTickLabels = labels[1]

    for band in range(numBands):
        xVals = barLoc + xLocs[band]
        plt.plot(xVals, FAs[:,band], 'k-', lw=2)
        l1, = plt.plot(xVals[0], FAs[0,band], 'o', mec='k', mfc='k', ms=10)
        l2, = plt.plot(xVals[1], FAs[1,band], 'o', mec=edgeColours[indType], mfc='white', ms=10)
        l3, = plt.plot(xVals[2], FAs[2,band], 'o', mec='orange', mfc='orange', ms=10)
        l4, = plt.plot(xVals[3], FAs[3, band], 'o', mec='orange', mfc='k', ms=10)

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

    axFA.set_xlim(xLocs[0] - 0.5, xLocs[-1] + 0.5)
    axFA.set_xticks(xLocs)
    axFA.set_xticklabels(labels[1])
    axFA.set_xlabel('Masker bandwidth (oct)')

    yLims = axFA.get_ylim()
    yLims = [yLims[0] - 0.1, yLims[1] + 0.1]
    axFA.set_ylim(yLims)
    axFA.set_ylabel('False Alarm Rate')

    extraplots.boxoff(axFA)

    # for band in range(numBands):
    #     xVals = barLoc + xLocs[band]
    #     pValLasers = stats.mannwhitneyu(laserToneChoice[laserTrialsEachCond[:, 1, band]],
    #                                     controlToneChoice[controlTrialsEachCond[:, 1, band]])[1]
    #     if pValLasers < 0.05:
    #         extraplots.significance_stars(xVals[1:3], yLims[1] * 0.87, yLims[1] * 0.05, gapFactor=0.35, starSize=7)
    #     else:
    #         extraplots.significance_stars(xVals[1:3], yLims[1] * 0.87, yLims[1] * 0.05, gapFactor=0.35, starSize=7,
    #                                       starString='ns')
    #     # axAccuracy.text(xLocs[band], 0.8 * yLim[1], f'p = {pValLasers:.3f}', fontsize=8, va='center', ha='center',
    #     #                 color='k', clip_on=False)
    #
    #     pValControls = stats.mannwhitneyu(laserToneChoice[laserTrialsEachCond[:, 0, band]],
    #                                     controlToneChoice[controlTrialsEachCond[:, 0, band]])[1]
    #     if pValControls < 0.05:
    #         extraplots.significance_stars([xVals[0],xVals[3]], yLims[1] * 0.99, yLims[1] * 0.05, gapFactor=0.2, starSize=7)
    #     else:
    #         extraplots.significance_stars([xVals[0],xVals[3]], yLims[1] * 0.99, yLims[1] * 0.05, gapFactor=0.2, starSize=7,
    #                                       starString='ns')

    # -- plot d prime for each bandwidth and laser presentation --
    axdprime = plt.subplot(gs3[2, 0])

    barLoc = np.array([-0.3, -0.1, 0.1, 0.3])
    xLocs = np.arange(numBands)
    xTickLabels = labels[1]

    for band in range(numBands):
        xVals = barLoc + xLocs[band]
        plt.plot(xVals, dprimes[:,band], 'k-', lw=2)
        l1, = plt.plot(xVals[0], dprimes[0,band], 'o', mec='k', mfc='k', ms=10)
        l2, = plt.plot(xVals[1], dprimes[1,band], 'o', mec=edgeColours[indType], mfc='white', ms=10)
        l3, = plt.plot(xVals[2], dprimes[2,band], 'o', mec='orange', mfc='orange', ms=10)
        l4, = plt.plot(xVals[3], dprimes[3, band], 'o', mec='orange', mfc='k', ms=10)

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

    axdprime.set_xlim(xLocs[0] - 0.5, xLocs[-1] + 0.5)
    axdprime.set_xticks(xLocs)
    axdprime.set_xticklabels(labels[1])
    axdprime.set_xlabel('Masker bandwidth (oct)')

    yLims = axdprime.get_ylim()
    yLims = [yLims[0] - 0.1, yLims[1] + 0.1]
    axdprime.set_ylim(yLims)
    axdprime.set_ylabel('d\'')

    extraplots.boxoff(axdprime)

    if indType == 2:
        plt.suptitle(mouse + ' {}mW ({})'.format(ChR2LaserPower, mouseLabel[indType]))
        figFilename = f'{mouse}_behav_report_{ChR2LaserPower}mW_v2'
    else:
        plt.suptitle(mouse + ' {}mW ({})'.format(ArchTlaserPower, mouseLabel[indType]))
        figFilename = f'{mouse}_behav_report_{ArchTlaserPower}mW_v2'

    extraplots.save_figure(figFilename, 'png', [7, 8], '/tmp/', facecolor='w')
    #plt.show()

for indType, mice in enumerate(mouseType):
    for mouse in mice:
        if indType == 2:
            plot_report(mouse, ChR2LaserPower, indType)
        else:
            plot_report(mouse, ArchTlaserPower, indType)

    #     break
    # break
