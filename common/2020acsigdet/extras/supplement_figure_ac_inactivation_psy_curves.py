import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from statsmodels.stats.proportion import proportion_confint

from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots
from jaratoolbox import settings

import studyparams
import figparams

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'SuppFig_ac_inactivation_psychometric_curves'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [6,3]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

baseColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
connectLineColour = figparams.colp['connectLine']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 2, wspace=0.3, hspace=0.4)
gs.update(top=0.97, bottom=0.15, left=0.12, right=0.98, wspace=0.5, hspace=0.3)

examples = [{'subject': 'band046',
             'sessions': '3mW laser',
             'bandwidth': 0.25}, # example tone-right PV-ChR2 psychometric

            {'subject': 'band134',
             'sessions': '3mW laser',
             'bandwidth': 0.25} # example tone-left PV-ChR2 psychometric
            ]

for indExample, example in enumerate(examples):
    # -- generate the curves --
    sessions = studyparams.miceDict[example['subject']][example['sessions']]
    behavData = behavioranalysis.load_many_sessions(example['subject'], sessions)

    numLasers = np.unique(behavData['laserSide'])
    numBands = np.unique(behavData['currentBand'])
    numSNRs = np.unique(behavData['currentSNR'])

    trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['laserSide'], numLasers,
                                                                   behavData['currentBand'], numBands)
    trialsEachSNR = behavioranalysis.find_trials_each_type(behavData['currentSNR'], numSNRs)

    trialsEachCond3Params = np.zeros((len(behavData['laserSide']), len(numLasers), len(numBands), len(numSNRs)),
                                     dtype=bool)
    for ind in range(len(numSNRs)):
        trialsEachCond3Params[:, :, :, ind] = trialsEachCond & trialsEachSNR[:, ind][:, np.newaxis, np.newaxis]

    valid = behavData['valid'].astype(bool)
    rightChoice = behavData['choice'] == behavData.labels['choice']['right']
    leftChoice = behavData['choice'] == behavData.labels['choice']['left']

    band = np.argwhere(numBands == example['bandwidth']).flatten()[0]
    psyCurves = []
    upperErrors = []
    lowerErrors = []

    for laser in range(len(numLasers)):
        thisPsyCurve = np.zeros(len(numSNRs))
        upperErrorBar = np.zeros(len(numSNRs))
        lowerErrorBar = np.zeros(len(numSNRs))
        for snr in range(len(numSNRs)):
            rightChoiceThisCond = rightChoice[trialsEachCond3Params[:, laser, band, snr]]
            leftChoiceThisCond = leftChoice[trialsEachCond3Params[:, laser, band, snr]]
            thisPsyCurve[snr] = 100.0 * np.sum(rightChoiceThisCond) / (np.sum(rightChoiceThisCond) + np.sum(leftChoiceThisCond))

            CIthisSNR = np.array(proportion_confint(np.sum(rightChoiceThisCond), (np.sum(rightChoiceThisCond) + np.sum(leftChoiceThisCond)), method='wilson'))
            upperErrorBar[snr] = 100.0 * CIthisSNR[1] - thisPsyCurve[snr]
            lowerErrorBar[snr] = thisPsyCurve[snr] - 100.0 * CIthisSNR[0]

        psyCurves.append(thisPsyCurve)
        upperErrors.append(upperErrorBar)
        lowerErrors.append(lowerErrorBar)

    # -- plot the curves --
    axCurve = plt.subplot(gs[0, indExample])
    xTickLabels = ['-inf']
    xTickLabels.extend([int(x) for x in numSNRs.tolist()[1:]])

    xVals = range(len(numSNRs))
    plt.plot(xVals[:2], psyCurves[0][:2], 'o--', color=baseColour, lw=3, ms=8, zorder=10)
    l1, = plt.plot(xVals[1:], psyCurves[0][1:], 'o-', color=baseColour, lw=3, ms=8, zorder=10)
    # l1, = plt.plot(range(len(possibleSNRs)), psyCurveControl, 'o-', color=baseColour, lw=3, ms=8)
    plt.errorbar(range(len(numSNRs)), psyCurves[0], yerr=[lowerErrors[0], upperErrors[0]], fmt='none',
                 color=baseColour, lw=2, capsize=5, capthick=1)


    plt.plot(xVals[:2], psyCurves[1][:2], 'o--', color=PVColour, lw=3, ms=8, zorder=10)
    l2, = plt.plot(xVals[1:], psyCurves[1][1:], 'o-', color=PVColour, lw=3, ms=8, zorder=10)
    # l2, = plt.plot(range(len(possibleSNRs)), psyCurveLaser, 'o-', color=PVColour, lw=3, ms=8)
    plt.errorbar(range(len(numSNRs)), psyCurves[1], yerr=[lowerErrors[0], upperErrors[0]], fmt='none',
                 color=PVColour, lw=2, capsize=5, capthick=1, zorder=-10)

    axCurve.legend([l1, l2], ['control', 'PV activated'])

    axCurve.set_xlim(-0.2, len(numSNRs) - 0.8)
    axCurve.set_xticks(range(len(numSNRs)))
    axCurve.set_xticklabels(xTickLabels)
    axCurve.set_xlabel('SNR (dB)', fontsize=fontSizeLabels)

    axCurve.set_ylim(0, 100)
    axCurve.set_ylabel('Trials with rightward choice (%)', fontsize=fontSizeLabels)

    extraplots.boxoff(axCurve)
    extraplots.breakaxis(0.5, 0, 0.15, 5, gap=0.5)
    extraplots.set_ticks_fontsize(axCurve, fontSizeTicks)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)