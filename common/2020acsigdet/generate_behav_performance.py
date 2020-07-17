import os
import numpy as np
from statsmodels.stats.proportion import proportion_confint

from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import studyparams

figName = 'figure_characterise_behaviour'
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

mouseDicts = [studyparams.unimplanted_PVCHR2, studyparams.unimplanted_PVARCHT, studyparams.unimplanted_SOMARCHT, studyparams.unimplanted_wt]

percentToneDetectEachSNR = []
percentCorrectEachBand = []
biasEachBand = []

for miceThisType in mouseDicts:

    percentToneDetectEachSNRThisType = None
    percentCorrectEachBandThisType = None
    biasEachBandThisType = None

    for indMouse, mouse in enumerate(miceThisType.keys()):
        behavData = behavioranalysis.load_many_sessions(mouse, miceThisType[mouse])
        numMice = len(miceThisType.keys())

        bandEachTrial = behavData['currentBand']
        noiseAmpEachTrial = behavData['currentNoiseAmp']
        SNReachTrial = behavData['currentSNR']

        valid = behavData['valid'].astype(bool)
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

        # trialsEachComb = np.zeros((len(firstSort),len(possibleFirstSort),len(possibleSecondSort),len(possibleThirdSort)),dtype=bool)
        # trialsEachComb12 = behavioranalysis.find_trials_each_combination(firstSort, possibleFirstSort, secondSort, possibleSecondSort)
        # trialsEachType3 = behavioranalysis.find_trials_each_type(thirdSort,possibleThirdSort)
        # for ind3 in range(len(possibleThirdSort)):
        #     trialsEachComb[:,:,:,ind3] = trialsEachComb12 & trialsEachType3[:,ind3][:,np.newaxis,np.newaxis]

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
            percentCorrectEachBandThisType = np.zeros((numMice, len(possibleBands)))
        if biasEachBandThisType is None:
            biasEachBandThisType = np.zeros((numMice, len(possibleBands)))

        for band in range(len(possibleBands)):
            trialsThisBand = trialsEachBand[:, band]
            correctThisBand = correct[trialsThisBand]
            incorrectThisBand = incorrect[trialsThisBand]
            toneChoiceThisBand = toneChoice[trialsThisBand]
            noiseChoiceThisBand = noiseChoice[trialsThisBand]

            percentCorrectEachBandThisType[indMouse, band] = 100.0 * np.sum(correctThisBand) / (np.sum(correctThisBand) + np.sum(incorrectThisBand))
            biasEachBandThisType[indMouse, band] = (np.sum(toneChoiceThisBand) - np.sum(noiseChoiceThisBand)) / (
                        np.sum(toneChoiceThisBand) + np.sum(noiseChoiceThisBand))

    percentToneDetectEachSNR.append(percentToneDetectEachSNRThisType)
    percentCorrectEachBand.append(percentCorrectEachBandThisType)
    biasEachBand.append(biasEachBandThisType)

allToneDetect = np.concatenate(tuple(percentToneDetectEachSNR), axis=0)
allPercentCorrect = np.concatenate(tuple(percentCorrect[:,(0,-1)] for percentCorrect in percentCorrectEachBand), axis=0)
allBias = np.concatenate(tuple(bias[:,(0,-1)] for bias in biasEachBand), axis=0)

# # --- comparisons by noise amp ---
# possibleNoiseAmps = np.unique(noiseAmpEachTrial)
# trialsEachNoiseAmp = behavioranalysis.find_trials_each_type(noiseAmpEachTrial, possibleNoiseAmps)
# percentCorrectEachNoiseAmp = np.zeros(len(possibleNoiseAmps))
# biasEachNoiseAmp = np.zeros(len(possibleNoiseAmps))
#
# for amp in range(len(possibleNoiseAmps)):
#     trialsThisAmp = trialsEachBand[:, amp]
#     validThisAmp = valid[trialsThisAmp]
#     correctThisAmp = correct[trialsThisAmp]
#     toneChoiceThisAmp = toneChoice[trialsThisAmp]
#     noiseChoiceThisAmp = noiseChoice[trialsThisAmp]
#
#     percentCorrectEachNoiseAmp[amp] = 100.0 * np.sum(correctThisAmp) / np.sum(validThisAmp)
#     biasEachNoiseAmp[amp] = (np.sum(toneChoiceThisAmp) - np.sum(noiseChoiceThisAmp)) / (
#                 np.sum(toneChoiceThisAmp) + np.sum(noiseChoiceThisAmp))

# -- save data --
outputFile = 'unimplanted_behaviour.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         PVCHR2toneDetect = percentToneDetectEachSNR[0], PVCHR2correctByBand = percentCorrectEachBand[0], PVCHR2biasByBand = biasEachBand[0],
         PVARCHTtoneDetect = percentToneDetectEachSNR[1], PVARCHTcorrectByBand = percentCorrectEachBand[1], PVARCHTbiasByBand = biasEachBand[1],
         SOMARCHTtoneDetect = percentToneDetectEachSNR[2], SOMARCHTcorrectByBand = percentCorrectEachBand[2], SOMARCHTbiasByBand = biasEachBand[2],
         wtToneDetect = percentToneDetectEachSNR[3], wtCorrectByBand = percentCorrectEachBand[3], wtBiasByBand = biasEachBand[3],
         allToneDetect = allToneDetect, allPercentCorrect = allPercentCorrect, allBias = allBias,
         possibleSNRs = possibleSNRs, possibleBands = possibleBands)
print(outputFile + " saved")

# -- example psychometric curve for behav figure --
mouse = 'band068'
sessions = [studyparams.band068_unimplanted[-1]]
behavData = behavioranalysis.load_many_sessions(mouse, sessions)

numBands = np.unique(behavData['currentBand'])
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
         possibleSNRs = possibleSNRs, numTrials = np.sum(valid))
print(outputFile + " saved")