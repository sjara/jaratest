import os
import numpy as np

from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import studyparams

figName = 'figure_inhibitory_inactivation'
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

SOM_ARCHT_MICE = studyparams.SOM_ARCHT_MICE
PV_ARCHT_MICE = studyparams.PV_ARCHT_MICE
mouseType = [PV_ARCHT_MICE, SOM_ARCHT_MICE]

laserAccuracy = []
controlAccuracy = []

laserBias = []
controlBias = []

for indType, mice in enumerate(mouseType):

    thisLaserAccuracy = None
    thisControlAccuracy = None

    thisLaserBias = None
    thisControlBias = None

    for indMouse, mouse in enumerate(mice):

        laserSessions = studyparams.miceDict[mouse]['10mW laser']
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

            if thisLaserAccuracy is None:
                thisLaserAccuracy = np.zeros((len(mice), len(numBands)))
            thisLaserAccuracy[indMouse, indBand] = 100.0 * np.sum(laserCorrect) / np.sum(laserValid)

            controlValid = valid[trialsEachLaser[:, 0]]
            controlCorrect = correct[trialsEachLaser[:, 0]]

            if thisControlAccuracy is None:
                thisControlAccuracy = np.zeros((len(mice), len(numBands)))
            thisControlAccuracy[indMouse, indBand] = 100.0 * np.sum(controlCorrect) / np.sum(controlValid)

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

            if thisLaserBias is None:
                thisLaserBias = np.zeros((len(mice), len(numBands)))
            thisLaserBias[indMouse, indBand] = 1.0 * (np.sum(laserToneChoice) - np.sum(laserNoiseChoice)) / \
                                               (np.sum(laserToneChoice) + np.sum(laserNoiseChoice))

            controlToneChoice = toneChoice[trialsEachLaser[:, 0]]
            controlNoiseChoice = noiseChoice[trialsEachLaser[:, 0]]

            if thisControlBias is None:
                thisControlBias = np.zeros((len(mice), len(numBands)))
            thisControlBias[indMouse, indBand] = 1.0 * (np.sum(controlToneChoice) - np.sum(controlNoiseChoice)) / \
                                        (np.sum(controlToneChoice) + np.sum(controlNoiseChoice))

    laserAccuracy.append(thisLaserAccuracy)
    controlAccuracy.append(thisControlAccuracy)

    laserBias.append(thisLaserBias)
    controlBias.append(thisControlBias)

# -- save responses of all sound responsive cells to 0.25 bandwidth sounds --
outputFile = 'all_behaviour_inhib_inactivation.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         PVlaserAccuracy=laserAccuracy[0], PVcontrolAccuracy=controlAccuracy[0],
         PVlaserBias=laserBias[0], PVcontrolBias=controlBias[0],
         SOMlaserAccuracy=laserAccuracy[1], SOMcontrolAccuracy=controlAccuracy[1],
         SOMlaserBias=laserBias[1], SOMcontrolBias=controlBias[1],
         possibleBands=numBands)
print(outputFile + " saved")
