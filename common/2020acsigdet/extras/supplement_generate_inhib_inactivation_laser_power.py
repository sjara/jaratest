import os
import numpy as np

from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import behaviour_analysis_funcs as funcs
import studyparams

figName = 'figure_inhibitory_inactivation'
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

SOM_ARCHT_MICE = studyparams.SOM_ARCHT_MICE
PV_ARCHT_MICE = studyparams.PV_ARCHT_MICE
mouseType = [PV_ARCHT_MICE, SOM_ARCHT_MICE]
laserPowers = ['5mW', '10mW', '15mW']

REACTION_TIME_CUTOFF = studyparams.REACTION_TIME_CUTOFF

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

        for indPower, power in enumerate(laserPowers):

            try:
                laserSessions = studyparams.miceDict[mouse][f'{power} laser']
            except(KeyError):
                print(f'No {power} for {mouse}')
            else:
                laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

                numLasers = np.unique(laserBehavData['laserSide'])
                numBands = np.unique(laserBehavData['currentBand'])

                trialsEachCond = behavioranalysis.find_trials_each_combination(laserBehavData['laserSide'], numLasers,
                                                                               laserBehavData['currentBand'], numBands)

                reactionTimes, decisionTimes = funcs.get_reaction_times(mouse, laserSessions)
                trialsToUse = reactionTimes>REACTION_TIME_CUTOFF

                # -- compute accuracies and bias for each bandwidth --

                for indBand in range(len(numBands)):
                    trialsEachLaser = trialsEachCond[:, :, indBand]

                    # -- sort trials by laser presentation, compute accuracy as percent correct trials out of all valid trials --
                    valid = laserBehavData['valid'].astype(bool)
                    correct = laserBehavData['outcome'] == laserBehavData.labels['outcome']['correct']
                    incorrect = laserBehavData['outcome'] == laserBehavData.labels['outcome']['error']

                    laserValid = valid[trialsEachLaser[:, 1] & trialsToUse]
                    laserCorrect = correct[trialsEachLaser[:, 1] & trialsToUse]
                    laserIncorrect = incorrect[trialsEachLaser[:, 1] & trialsToUse]

                    if thisLaserAccuracy is None:
                        thisLaserAccuracy = np.empty((len(mice), len(laserPowers), len(numBands)))
                        thisLaserAccuracy[:] = np.nan
                    thisLaserAccuracy[indMouse, indPower, indBand] = 100.0 * np.sum(laserCorrect) / (np.sum(laserCorrect) + np.sum(laserIncorrect))

                    controlValid = valid[trialsEachLaser[:, 0] & trialsToUse]
                    controlCorrect = correct[trialsEachLaser[:, 0] & trialsToUse]
                    controlIncorrect = incorrect[trialsEachLaser[:, 0] & trialsToUse]

                    if thisControlAccuracy is None:
                        thisControlAccuracy = np.empty((len(mice), len(laserPowers), len(numBands)))
                        thisControlAccuracy[:] = np.nan
                    thisControlAccuracy[indMouse, indPower, indBand] = 100.0 * np.sum(controlCorrect) / (np.sum(controlCorrect) + np.sum(controlIncorrect))

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

                    laserToneChoice = toneChoice[trialsEachLaser[:, 1] & trialsToUse]
                    laserNoiseChoice = noiseChoice[trialsEachLaser[:, 1] & trialsToUse]

                    if thisLaserBias is None:
                        thisLaserBias = np.empty((len(mice), len(laserPowers), len(numBands)))
                        thisLaserBias[:] = np.nan
                    thisLaserBias[indMouse, indPower, indBand] = 1.0 * (np.sum(laserToneChoice) - np.sum(laserNoiseChoice)) / \
                                                       (np.sum(laserToneChoice) + np.sum(laserNoiseChoice))

                    controlToneChoice = toneChoice[trialsEachLaser[:, 0] & trialsToUse]
                    controlNoiseChoice = noiseChoice[trialsEachLaser[:, 0] & trialsToUse]

                    if thisControlBias is None:
                        thisControlBias = np.empty((len(mice), len(laserPowers), len(numBands)))
                        thisControlBias[:] = np.nan
                    thisControlBias[indMouse, indPower, indBand] = 1.0 * (np.sum(controlToneChoice) - np.sum(controlNoiseChoice)) / \
                                                (np.sum(controlToneChoice) + np.sum(controlNoiseChoice))

    laserAccuracy.append(thisLaserAccuracy)
    controlAccuracy.append(thisControlAccuracy)

    laserBias.append(thisLaserBias)
    controlBias.append(thisControlBias)

# -- save responses of all sound responsive cells to 0.25 bandwidth sounds --
outputFile = 'all_behaviour_inhib_inactivation_different_powers.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         PVlaserAccuracy=laserAccuracy[0], PVcontrolAccuracy=controlAccuracy[0],
         PVlaserBias=laserBias[0], PVcontrolBias=controlBias[0],
         SOMlaserAccuracy=laserAccuracy[1], SOMcontrolAccuracy=controlAccuracy[1],
         SOMlaserBias=laserBias[1], SOMcontrolBias=controlBias[1],
         possibleBands=numBands)
print(outputFile + " saved")
