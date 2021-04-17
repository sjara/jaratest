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

BANDS_TO_USE = [0, -1] # don't use intermediate bandwidths in mice that had them
CORRECTED = 0

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

for indType, mice in enumerate(mouseType):
    allHits = None
    hitsBySNR = None
    falseAlarms = None

    allHitsControl = None
    hitsBySNRControl = None
    falseAlarmsControl = None

    for indMouse, mouse in enumerate(mice):
        if indType == 2:
            laserSessions = studyparams.miceDict[mouse][f'{ChR2LaserPower}mW laser']
            laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)
            laserCorrect, laserIncorrect, laserToneChoice, laserNoiseChoice, laserTrialsEachCond, labels = get_trials(laserBehavData)

            controlSessions = studyparams.miceDict[mouse][f'{ChR2LaserPower}mW control']
            controlBehavData = behavioranalysis.load_many_sessions(mouse, controlSessions)
            controlCorrect, controlIncorrect, controlToneChoice, controlNoiseChoice, controlTrialsEachCond, labels = get_trials(laserBehavData)

            if len(labels[1])>len(BANDS_TO_USE):
                labels[1] = labels[1][BANDS_TO_USE]
        else:
            try:
                laserSessions = studyparams.miceDict[mouse][f'{ArchTlaserPower}mW laser']
                controlSessions = studyparams.miceDict[mouse][f'{ArchTlaserPower}mW control']
            except(KeyError):
                pass
            else:
                laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)
                laserCorrect, laserIncorrect, laserToneChoice, laserNoiseChoice, laserTrialsEachCond, labels = get_trials(laserBehavData)

                controlBehavData = behavioranalysis.load_many_sessions(mouse, controlSessions)
                controlCorrect, controlIncorrect, controlToneChoice, controlNoiseChoice, controlTrialsEachCond, labels = get_trials(laserBehavData)

        if hitsBySNR is None:
            hitsBySNR = np.zeros((len(mice), len(labels[0]), len(labels[1]), len(labels[2])-1))

        # -- compute each outcome as percentage of total trials --
        for band in BANDS_TO_USE:
            for laser in range(len(labels[0])):
                for snr in range(1,len(labels[2])):
                    trialsThisCond = laserTrialsEachCond[:, laser, band, snr]
                    toneChoiceThisCond = laserToneChoice[trialsThisCond]
                    noiseChoiceThisCond = laserNoiseChoice[trialsThisCond]
                    correctThisCond = laserCorrect[trialsThisCond]
                    incorrectThisCond = laserIncorrect[trialsThisCond]
                    totalToneTrialsThisCond = np.sum(correctThisCond & toneChoiceThisCond) + np.sum(
                        incorrectThisCond & noiseChoiceThisCond)
                    totalNoiseTrialsThisCond = np.sum(correctThisCond & noiseChoiceThisCond) + np.sum(
                        incorrectThisCond & toneChoiceThisCond)

                    hitsBySNR[indMouse, laser, band, snr-1] = np.sum(toneChoiceThisCond & correctThisCond) / totalToneTrialsThisCond

        if allHits is None:
            allHits = np.zeros((len(mice),len(labels[0]),len(labels[1])))
            falseAlarms = np.zeros_like(allHits)

        laserTrialsEachCond = np.sum(laserTrialsEachCond, axis=3).astype(bool)

        # -- compute each outcome as percentage of total trials --
        for band in BANDS_TO_USE:
            for laser in range(len(labels[0])):
                trialsThisCond = laserTrialsEachCond[:, laser, band]
                toneChoiceThisCond = laserToneChoice[trialsThisCond]
                noiseChoiceThisCond = laserNoiseChoice[trialsThisCond]
                correctThisCond = laserCorrect[trialsThisCond]
                incorrectThisCond = laserIncorrect[trialsThisCond]
                totalToneTrialsThisCond = np.sum(correctThisCond & toneChoiceThisCond) + np.sum(incorrectThisCond & noiseChoiceThisCond)
                totalNoiseTrialsThisCond = np.sum(correctThisCond & noiseChoiceThisCond) + np.sum(incorrectThisCond & toneChoiceThisCond)

                allHits[indMouse, laser, band] = np.sum(toneChoiceThisCond & correctThisCond) / totalToneTrialsThisCond
                falseAlarms[indMouse, laser, band] = np.sum(toneChoiceThisCond & incorrectThisCond) / totalToneTrialsThisCond

    # -- summary plot for each mouse type --
    fig = plt.gcf()
    fig.clf()
    fig.set_facecolor('w')

    gs = gridspec.GridSpec(2, 2)
    gs.update(top=0.90, bottom=0.15, left=0.09, right=0.99, wspace=0.5, hspace=0.3)

    colours = ['k', laserColours[indType]]
    width = 0.25
    barLoc = np.array([-0.2, 0.2])
    xLocs = np.arange(2)

    responses = [allHits, falseAlarms]
    xlabels = ['hit', 'FA']

    # -- plot all hits and FA --
    for indBand in BANDS_TO_USE:
        axBar = plt.subplot(gs[indBand,0])

        for indLaser in range(len(labels[0])):
            for indResponse in range(len(responses)):
                jitter = 0.8*width*(np.random.random(responses[indResponse].shape[0]))
                plt.plot(np.tile(xLocs[indResponse]+barLoc[indLaser], responses[indResponse].shape[0])+jitter,
                         100.0 * responses[indResponse][:,indLaser,indBand], 'o', mec=colours[indLaser], mfc='white')

                median = 100.0 * np.median(responses[indResponse][:,indLaser,indBand])
                plt.plot([xLocs[indResponse] + barLoc[indLaser] - width / 2, xLocs[indResponse] + barLoc[indLaser] + width / 2],
                         [median, median], color='k', linewidth=3, zorder=10)  # medians

                # biasCI = bootstrap_median_CI(changeBias[indType][:, indBand])
                # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
                # plt.plot([xLocs[indBand] + barLoc[indType], xLocs[indBand] + barLoc[indType]], biasCI,
                #          color='k', linewidth=1.5)  # error bars
                # plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                #          [biasCI[0], biasCI[0]], color='k', linewidth=1.5)  # bottom caps
                # plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                #          [biasCI[1], biasCI[1]], color='k', linewidth=1.5)  # top caps

        plt.title(f'{labels[1][indBand]} octaves')
        axBar.set_xticks(xLocs)
        axBar.set_xticklabels(xlabels)

        axBar.set_ylabel('Rate (%)')

        extraplots.boxoff(axBar)

        # -- plot hits by SNR --
        xLocs = np.arange(3)

        for indBand in BANDS_TO_USE:
            axBar = plt.subplot(gs[indBand, 1])

            for indLaser in range(len(labels[0])):
                for indSNR in range(hitsBySNR.shape[-1]):
                    jitter = 0.8 * width * (np.random.random(hitsBySNR.shape[0]))
                    plt.plot(np.tile(xLocs[indSNR] + barLoc[indLaser], hitsBySNR.shape[0]) + jitter,
                             100.0 * hitsBySNR[:, indLaser, indBand, indSNR], 'o', mec=colours[indLaser], mfc='white')

                    median = 100.0 * np.median(hitsBySNR[:, indLaser, indBand, indSNR])
                    plt.plot([xLocs[indSNR] + barLoc[indLaser] - width / 2,
                              xLocs[indSNR] + barLoc[indLaser] + width / 2],
                             [median, median], color='k', linewidth=3, zorder=10)  # medians

                    # biasCI = bootstrap_median_CI(changeBias[indType][:, indBand])
                    # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
                    # plt.plot([xLocs[indBand] + barLoc[indType], xLocs[indBand] + barLoc[indType]], biasCI,
                    #          color='k', linewidth=1.5)  # error bars
                    # plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                    #          [biasCI[0], biasCI[0]], color='k', linewidth=1.5)  # bottom caps
                    # plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                    #          [biasCI[1], biasCI[1]], color='k', linewidth=1.5)  # top caps

            plt.title(f'{labels[1][indBand]} octaves')
            axBar.set_xticks(xLocs)
            axBar.set_xticklabels(labels[2][1:])

            axBar.set_ylabel('Hit Rate (%)')

            extraplots.boxoff(axBar)

    plt.suptitle(f'{mouseLabel[indType]} effect')
    figFilename = f'{mouseLabel[indType]}_effect_on_signal_detection'

    extraplots.save_figure(figFilename, 'png', [6, 4], '/tmp/', facecolor='w')
