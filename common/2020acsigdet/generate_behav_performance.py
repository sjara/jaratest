import os
import numpy as np
from statsmodels.stats.proportion import proportion_confint
from scipy import stats

from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import behaviour_analysis_funcs as funcs
import studyparams

figName = 'figure_characterise_behaviour'
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

mouseDicts = [studyparams.unimplanted_PVCHR2, studyparams.unimplanted_PVARCHT, studyparams.unimplanted_SOMARCHT,
              studyparams.unimplanted_PVCRE, studyparams.unimplanted_SOMCRE]

BAND_TO_USE = [0,-1] # only use the extreme bandwidths for mice that had more than 2

percentToneDetectEachSNR = []
percentCorrectEachBand = []
dprimeEachBand = []
hitRateEachBand = []
FArateEachBand = []

for miceThisType in mouseDicts:

    percentToneDetectEachSNRThisType = None
    percentCorrectEachBandThisType = None
    dprimeEachBandThisType = None
    hitRateEachBandThisType = None
    FArateEachBandThisType = None

    for indMouse, mouse in enumerate(miceThisType.keys()):
        behavData = behavioranalysis.load_many_sessions(mouse, miceThisType[mouse])
        numMice = len(miceThisType.keys())

        bandEachTrial = behavData['currentBand']
        SNReachTrial = behavData['currentSNR']

        correct = behavData['outcome'] == behavData.labels['outcome']['correct']
        incorrect = behavData['outcome'] == behavData.labels['outcome']['error']
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

        # --- inputs to psychometric curve ---
        possibleSNRs = np.unique(SNReachTrial)
        trialsEachSNR = behavioranalysis.find_trials_each_type(SNReachTrial, possibleSNRs)
        if percentToneDetectEachSNRThisType is None:
            percentToneDetectEachSNRThisType = np.zeros((numMice, len(possibleSNRs)))

        for SNR in range(len(possibleSNRs)):
            trialsThisSNR = trialsEachSNR[:, SNR]
            toneChoiceThisSNR = toneChoice[trialsThisSNR]
            noiseChoiceThisSNR = noiseChoice[trialsThisSNR]
            percentToneDetectEachSNRThisType[indMouse, SNR] = 100.0 * np.sum(toneChoiceThisSNR) / (np.sum(toneChoiceThisSNR) + np.sum(noiseChoiceThisSNR))

        # --- comparisons by bandwidth ---
        possibleBands = np.unique(bandEachTrial)
        trialsEachBand = behavioranalysis.find_trials_each_type(bandEachTrial, possibleBands)

        if percentCorrectEachBandThisType is None:
            percentCorrectEachBandThisType = np.zeros((numMice, len(BAND_TO_USE)))
            dprimeEachBandThisType = np.zeros_like(percentCorrectEachBandThisType)
            hitRateEachBandThisType = np.zeros_like(percentCorrectEachBandThisType)
            FArateEachBandThisType = np.zeros_like(percentCorrectEachBandThisType)

        for band in BAND_TO_USE:
            trialsThisBand = trialsEachBand[:, band]
            correctThisBand = correct[trialsThisBand]
            incorrectThisBand = incorrect[trialsThisBand]
            toneChoiceThisBand = toneChoice[trialsThisBand]
            noiseChoiceThisBand = noiseChoice[trialsThisBand]

            toneTrialsThisBand = np.sum(correctThisBand & toneChoiceThisBand) + np.sum(incorrectThisBand & noiseChoiceThisBand)
            noiseTrialsThisBand = np.sum(correctThisBand & noiseChoiceThisBand) + np.sum(incorrectThisBand & toneChoiceThisBand)

            thisHitRate = np.sum(correctThisBand & toneChoiceThisBand) / toneTrialsThisBand
            thisFARate = np.sum(incorrectThisBand & toneChoiceThisBand) / noiseTrialsThisBand

            hitRateEachBandThisType[indMouse, band] = 100.0 * thisHitRate
            FArateEachBandThisType[indMouse, band] = 100.0 * thisFARate
            dprimeEachBandThisType[indMouse, band] = (stats.norm.ppf(thisHitRate) - stats.norm.ppf(thisFARate))

            percentCorrectEachBandThisType[indMouse, band] = 100.0 * np.sum(correctThisBand) / (np.sum(correctThisBand) + np.sum(incorrectThisBand))

    percentToneDetectEachSNR.append(percentToneDetectEachSNRThisType)
    percentCorrectEachBand.append(percentCorrectEachBandThisType)
    hitRateEachBand.append(hitRateEachBandThisType)
    FArateEachBand.append(FArateEachBandThisType)
    dprimeEachBand.append(dprimeEachBandThisType)

allToneDetect = np.concatenate(tuple(percentToneDetectEachSNR), axis=0)
allPercentCorrect = np.concatenate(tuple(percentCorrectEachBand), axis=0)
allHitRate = np.concatenate(tuple(hitRateEachBand), axis=0)
allFArate = np.concatenate(tuple(FArateEachBand), axis=0)
alldprime = np.concatenate(tuple(dprimeEachBand), axis=0)

# -- save data --
outputFile = 'unimplanted_behaviour_v2.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         PVCHR2toneDetect = percentToneDetectEachSNR[0], PVCHR2correctByBand = percentCorrectEachBand[0],
         PVCHR2dprimeByBand = dprimeEachBand[0], PVCHR2hitRateByBand = hitRateEachBand[0], PVCHR2FArateByBand = FArateEachBand[0],

         PVArchTtoneDetect = percentToneDetectEachSNR[1], PVArchTcorrectByBand = percentCorrectEachBand[1],
         PVArchTdprimeByBand = dprimeEachBand[1], PVArchThitRateByBand = hitRateEachBand[1], PVArchTFArateByBand = FArateEachBand[1],

         SOMArchTtoneDetect = percentToneDetectEachSNR[2], SOMArchTcorrectByBand = percentCorrectEachBand[2],
         SOMArchTdprimeByBand = dprimeEachBand[2], SOMArchThitRateByBand = hitRateEachBand[2], SOMArchTFArateByBand = FArateEachBand[2],

         PVCretoneDetect = percentToneDetectEachSNR[3], PVCrecorrectByBand = percentCorrectEachBand[3],
         PVCredprimeByBand = dprimeEachBand[3], PVCrehitRateByBand = hitRateEachBand[3], PVCreFArateByBand = FArateEachBand[3],

         SOMCretoneDetect = percentToneDetectEachSNR[4], SOMCrecorrectByBand = percentCorrectEachBand[4],
         SOMCredprimeByBand = dprimeEachBand[4], SOMCrehitRateByBand = hitRateEachBand[4], SOMCreFArateByBand = FArateEachBand[4],

         allToneDetect = allToneDetect, allPercentCorrect = allPercentCorrect, alldprimes = alldprime,
         allHitRate = allHitRate, allFArate = allFArate,

         possibleSNRs = possibleSNRs, possibleBands = possibleBands)
print(outputFile + " saved")

# -- example psychometric curve for behav figure --
mouse = 'band068'
sessions = [studyparams.band068_unimplanted[-1]]
behavData = behavioranalysis.load_many_sessions(mouse, sessions)

numSNRs = np.unique(behavData['currentSNR'])
trialsEachSNR = behavioranalysis.find_trials_each_type(behavData['currentSNR'], numSNRs)

toneChoice = behavData['choice'] == behavData.labels['choice']['right']
noiseChoice = behavData['choice'] == behavData.labels['choice']['left']

thisPsyCurve = np.zeros(len(numSNRs))
upperErrorBar = np.zeros(len(numSNRs))
lowerErrorBar = np.zeros(len(numSNRs))
for snr in range(len(numSNRs)):
    toneChoiceThisCond = toneChoice[trialsEachSNR[:, snr]]
    noiseChoiceThisCond = noiseChoice[trialsEachSNR[:, snr]]
    thisPsyCurve[snr] = 100.0 * np.sum(toneChoiceThisCond) / (np.sum(toneChoiceThisCond) + np.sum(noiseChoiceThisCond))

    CIthisSNR = np.array(proportion_confint(np.sum(toneChoiceThisCond), (np.sum(toneChoiceThisCond) + np.sum(noiseChoiceThisCond)), method='wilson'))
    upperErrorBar[snr] = 100.0 * CIthisSNR[1] - thisPsyCurve[snr]
    lowerErrorBar[snr] = thisPsyCurve[snr] - 100.0 * CIthisSNR[0]

# -- save data --
outputFile = 'band068_unimplanted_psycurve.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         psyCurve = thisPsyCurve, upperError = upperErrorBar, lowerError = lowerErrorBar,
         possibleSNRs = possibleSNRs, numTrials = (np.sum(toneChoiceThisCond) + np.sum(noiseChoiceThisCond)))
print(outputFile + " saved")