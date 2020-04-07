import os
import numpy as np

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
            validThisSNR = valid[trialsThisSNR]
            toneChoiceThisSNR = toneChoice[trialsThisSNR]
            percentToneDetectEachSNRThisType[indMouse, SNR] = 100.0 * np.sum(toneChoiceThisSNR) / np.sum(validThisSNR)

        # --- comparisons by bandwidth ---
        possibleBands = np.unique(bandEachTrial)
        trialsEachBand = behavioranalysis.find_trials_each_type(bandEachTrial, possibleBands)

        if percentCorrectEachBandThisType is None:
            percentCorrectEachBandThisType = np.zeros((numMice, len(possibleBands)))
        if biasEachBandThisType is None:
            biasEachBandThisType = np.zeros((numMice, len(possibleBands)))

        for band in range(len(possibleBands)):
            trialsThisBand = trialsEachBand[:, band]
            validThisBand = valid[trialsThisBand]
            correctThisBand = correct[trialsThisBand]
            toneChoiceThisBand = toneChoice[trialsThisBand]
            noiseChoiceThisBand = noiseChoice[trialsThisBand]

            percentCorrectEachBandThisType[indMouse, band] = 100.0 * np.sum(correctThisBand) / np.sum(validThisBand)
            biasEachBandThisType[indMouse, band] = (np.sum(toneChoiceThisBand) - np.sum(noiseChoiceThisBand)) / (
                        np.sum(toneChoiceThisBand) + np.sum(noiseChoiceThisBand))

    percentToneDetectEachSNR.append(percentToneDetectEachSNRThisType)
    percentCorrectEachBand.append(percentCorrectEachBandThisType)
    biasEachBand.append(biasEachBandThisType)

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
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         PVCHR2toneDetect = percentToneDetectEachSNR[0], PVCHR2correctByBand = percentCorrectEachBand[0], PVCHR2biasByBand = biasEachBand[0],
         PVARCHTtoneDetect = percentToneDetectEachSNR[1], PVARCHTcorrectByBand = percentCorrectEachBand[1], PVARCHTbiasByBand = biasEachBand[1],
         SOMARCHTtoneDetect = percentToneDetectEachSNR[2], SOMARCHTcorrectByBand = percentCorrectEachBand[2], SOMARCHTbiasByBand = biasEachBand[2],
         wtToneDetect = percentToneDetectEachSNR[3], wtCorrectByBand = percentCorrectEachBand[3], wtBiasByBand = biasEachBand[3],
         possibleSNRs = possibleSNRs, possibleBands = possibleBands)
print(outputFile + " saved")
