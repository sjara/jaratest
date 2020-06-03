import os
import numpy as np
from scipy import stats

from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import studyparams

figName = 'figure_ac_inactivation'
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

PV_CHR2_MICE = studyparams.PV_CHR2_MICE

laserAccuracy = None
controlAccuracy = None

laserBias = None
controlBias = None

rewardPVals = None
sideChoicePVals = None

for indMouse, mouse in enumerate(PV_CHR2_MICE):

    laserSessions = studyparams.miceDict[mouse]['3mW laser']
    laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

    numLasers = np.unique(laserBehavData['laserSide'])
    numBands = np.unique(laserBehavData['currentBand'])

    trialsEachCond = behavioranalysis.find_trials_each_combination(laserBehavData['laserSide'], numLasers,
                                                                   laserBehavData['currentBand'], numBands)

    # -- compute accuracies and bias for each bandwidth --

    for indBand in range(len(numBands)):
        trialsEachLaser = trialsEachCond[:, :, indBand]

        # -- sort trials by laser presentation, compute accuracy as percent correct trials out of all valid trials --
        valid = laserBehavData['valid'].astype(bool)
        correct = laserBehavData['outcome'] == laserBehavData.labels['outcome']['correct']

        laserValid = valid[trialsEachLaser[:, 1]]
        laserCorrect = correct[trialsEachLaser[:, 1]]

        if laserAccuracy is None:
            laserAccuracy = np.zeros((len(PV_CHR2_MICE), len(numBands)))
        laserAccuracy[indMouse, indBand] = 100.0 * np.sum(laserCorrect) / np.sum(laserValid)

        controlValid = valid[trialsEachLaser[:, 0]]
        controlCorrect = correct[trialsEachLaser[:, 0]]

        if controlAccuracy is None:
            controlAccuracy = np.zeros((len(PV_CHR2_MICE), len(numBands)))
        controlAccuracy[indMouse, indBand] = 100.0 * np.sum(controlCorrect) / np.sum(controlValid)

        if rewardPVals is None:
            rewardPVals = np.zeros((len(PV_CHR2_MICE), len(numBands)))
        rewardPVals[indMouse, indBand] = stats.ranksums(laserCorrect[laserValid], controlCorrect[controlValid])[1]

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

        if laserBias is None:
            laserBias = np.zeros((len(PV_CHR2_MICE), len(numBands)))
        laserBias[indMouse, indBand] = 1.0 * (np.sum(laserToneChoice) - np.sum(laserNoiseChoice)) / \
                                           (np.sum(laserToneChoice) + np.sum(laserNoiseChoice))

        controlToneChoice = toneChoice[trialsEachLaser[:, 0]]
        controlNoiseChoice = noiseChoice[trialsEachLaser[:, 0]]

        if controlBias is None:
            controlBias = np.zeros((len(PV_CHR2_MICE), len(numBands)))
        controlBias[indMouse, indBand] = 1.0 * (np.sum(controlToneChoice) - np.sum(controlNoiseChoice)) / \
                                    (np.sum(controlToneChoice) + np.sum(controlNoiseChoice))

        if sideChoicePVals is None:
            sideChoicePVals = np.zeros((len(PV_CHR2_MICE), len(numBands)))
        sideChoicePVals[indMouse, indBand] = stats.ranksums(laserToneChoice[laserValid], controlToneChoice[controlValid])[1]

# -- save responses of all sound responsive cells to 0.25 bandwidth sounds --
outputFile = 'all_behaviour_ac_inactivation.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         laserAccuracy=laserAccuracy, controlAccuracy=controlAccuracy,
         laserBias=laserBias, controlBias=controlBias,
         rewardPVals=rewardPVals, sideChoicePVals=sideChoicePVals,
         possibleBands=numBands)
print(outputFile + " saved")