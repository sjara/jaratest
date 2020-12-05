import os
import numpy as np
from scipy import stats

from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import studyparams

figName = 'figure_ac_inactivation'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

PV_CHR2_MICE = studyparams.PV_CHR2_MICE
BANDS_TO_USE = [0,-1] #ignore intermetiate bandwidth for the mice it was done for

laserCorrectSum = None
laserIncorrectSum = None
controlCorrectSum = None
controlIncorrectSum = None

laserToneSum = None
laserNoiseSum = None
controlToneSum = None
controlNoiseSum = None

for indMouse, mouse in enumerate(PV_CHR2_MICE):

    laserSessions = studyparams.miceDict[mouse]['3mW laser']
    laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

    numLasers = np.unique(laserBehavData['laserSide'])
    numBands = np.unique(laserBehavData['currentBand'])

    trialsEachCond = behavioranalysis.find_trials_each_combination(laserBehavData['laserSide'], numLasers,
                                                                   laserBehavData['currentBand'], numBands)

    # -- compute accuracies and bias for each bandwidth --

    for indBand in BANDS_TO_USE:
        trialsEachLaser = trialsEachCond[:, :, indBand]

        # -- sort trials by laser presentation, compute accuracy as percent correct trials out of all valid trials --
        correct = laserBehavData['outcome'] == laserBehavData.labels['outcome']['correct']
        incorrect = laserBehavData['outcome'] == laserBehavData.labels['outcome']['error']

        laserIncorrect = incorrect[trialsEachLaser[:, 1]]
        laserCorrect = correct[trialsEachLaser[:, 1]]

        controlIncorrect = incorrect[trialsEachLaser[:, 0]]
        controlCorrect = correct[trialsEachLaser[:, 0]]

        if laserCorrectSum is None:
            laserCorrectSum = np.zeros((len(PV_CHR2_MICE), len(BANDS_TO_USE)))
            laserIncorrectSum = np.zeros_like(laserCorrectSum)
            controlCorrectSum = np.zeros_like(laserCorrectSum)
            controlIncorrectSum = np.zeros_like(laserCorrectSum)

        laserCorrectSum[indMouse, indBand] = np.sum(laserCorrect)
        laserIncorrectSum[indMouse, indBand] = np.sum(laserIncorrect)
        controlCorrectSum[indMouse, indBand] = np.sum(controlCorrect)
        controlIncorrectSum[indMouse, indBand] = np.sum(controlIncorrect)

        # -- compute bias to a side as difference/sum --
        leftChoice = laserBehavData['choice'] == laserBehavData.labels['choice']['left']
        rightChoice = laserBehavData['choice'] == laserBehavData.labels['choice']['right']

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

        laserToneChoice = toneChoice[trialsEachLaser[:, 1]]
        laserNoiseChoice = noiseChoice[trialsEachLaser[:, 1]]

        controlToneChoice = toneChoice[trialsEachLaser[:, 0]]
        controlNoiseChoice = noiseChoice[trialsEachLaser[:, 0]]

        if laserToneSum is None:
            laserToneSum = np.zeros((len(PV_CHR2_MICE), len(BANDS_TO_USE)))
            laserNoiseSum = np.zeros_like(laserCorrectSum)
            controlToneSum = np.zeros_like(laserCorrectSum)
            controlNoiseSum = np.zeros_like(laserCorrectSum)

        laserToneSum[indMouse, indBand] = np.sum(laserToneChoice)
        laserNoiseSum[indMouse, indBand] = np.sum(laserNoiseChoice)
        controlToneSum[indMouse, indBand] = np.sum(controlToneChoice)
        controlNoiseSum[indMouse, indBand] = np.sum(controlNoiseChoice)

laserAccuracy = 100.0 * laserCorrectSum / (laserCorrectSum + laserIncorrectSum)
controlAccuracy = 100.0 * controlCorrectSum / (controlCorrectSum + controlIncorrectSum)

laserBias = 1.0 * (laserToneSum - laserNoiseSum) / (laserToneSum + laserNoiseSum)
controlBias = 1.0 * (controlToneSum - controlNoiseSum) / (controlToneSum + controlNoiseSum)

laserAccuracyAllBands = 100.0 * np.sum(laserCorrectSum, axis=1) / (np.sum(laserCorrectSum, axis=1) + np.sum(laserIncorrectSum, axis=1))
controlAccuracyAllBands = 100.0 * np.sum(controlCorrectSum, axis=1) / (np.sum(controlCorrectSum, axis=1) + np.sum(controlIncorrectSum, axis=1))

laserBiasAllBands = 1.0 * (np.sum(laserToneSum, axis=1) - np.sum(laserNoiseSum, axis=1)) / (np.sum(laserToneSum, axis=1) + np.sum(laserNoiseSum, axis=1))
controlBiasAllBands = 1.0 * (np.sum(controlToneSum, axis=1) - np.sum(controlNoiseSum, axis=1)) / (np.sum(controlToneSum, axis=1) + np.sum(controlNoiseSum, axis=1))

# -- save responses of all sound responsive cells to 0.25 bandwidth sounds --
outputFile = 'all_behaviour_ac_inactivation.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         laserAccuracy=laserAccuracy, controlAccuracy=controlAccuracy,
         laserAccuracyAllBands=laserAccuracyAllBands, controlAccuracyAllBands=controlAccuracyAllBands,
         laserBias=laserBias, controlBias=controlBias,
         laserBiasAllBands=laserBiasAllBands, controlBiasAllBands=controlBiasAllBands,
         possibleBands=numBands[BANDS_TO_USE])
print(outputFile + " saved")