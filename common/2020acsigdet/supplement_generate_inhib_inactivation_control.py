import os
import numpy as np

from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import studyparams

def load_data_for_this_stuff(mouse, sessionType):
    sessions = studyparams.miceDict[mouse][sessionType]
    behavData = behavioranalysis.load_many_sessions(mouse, sessions)

    numLasers = np.unique(behavData['laserSide'])
    numBands = np.unique(behavData['currentBand'])

    trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['laserSide'], numLasers,
                                                                   behavData['currentBand'], numBands)
    trialsEachLaser = behavioranalysis.find_trials_each_type(behavData['laserSide'], numLasers)

    valid = behavData['valid'].astype(bool)
    correct = behavData['outcome'] == behavData.labels['outcome']['correct']
    incorrect = behavData['outcome'] == behavData.labels['outcome']['error']

    leftChoice = behavData['choice'] == behavData.labels['choice']['left']
    rightChoice = behavData['choice'] == behavData.labels['choice']['right']

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

    return trialsEachCond, trialsEachLaser, valid, correct, incorrect, toneChoice, noiseChoice, numBands

FIGNAME = 'figure_inhibitory_inactivation'
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PV_ARCHT_MICE = studyparams.PV_ARCHT_MICE
SOM_ARCHT_MICE = studyparams.SOM_ARCHT_MICE

mouseTypes = [PV_ARCHT_MICE, SOM_ARCHT_MICE]

laserAccuracy = []
controlAccuracy = []

laserBias = []
controlBias = []

changeAccuracy = []
changeBias = []

for indType, mice in enumerate(mouseTypes):
    thisLaserAccuracy = None
    thisControlAccuracy = None

    thisLaserBias = None
    thisControlBias = None

    controlChangeAccuracy = np.zeros(len(mice))
    expChangeAccuracy = np.zeros_like(controlChangeAccuracy)

    controlChangeBias = np.zeros_like(controlChangeAccuracy)
    expChangeBias = np.zeros_like(controlChangeAccuracy)

    for indMouse, mouse in enumerate(mice):

        trialsEachCond, trialsEachLaser, valid, correct, incorrect, toneChoice, noiseChoice, numBands = load_data_for_this_stuff(mouse, '10mW control')

        # -- compute accuracies and bias for each bandwidth in control condition --
        for indBand in range(len(numBands)):
            trialsEachLaser = trialsEachCond[:, :, indBand]

            # -- sort trials by laser presentation, compute accuracy as percent correct trials out of all valid trials --
            laserCorrect = correct[trialsEachLaser[:, 1]]
            laserIncorrect = incorrect[trialsEachLaser[:, 1]]

            if thisLaserAccuracy is None:
                thisLaserAccuracy = np.zeros((len(mice), len(numBands)))
            thisLaserAccuracy[indMouse, indBand] = 100.0 * np.sum(laserCorrect) / (np.sum(laserCorrect) + np.sum(laserIncorrect))

            controlCorrect = correct[trialsEachLaser[:, 0]]
            controlIncorrect = incorrect[trialsEachLaser[:, 0]]

            if thisControlAccuracy is None:
                thisControlAccuracy = np.zeros((len(mice), len(numBands)))
            thisControlAccuracy[indMouse, indBand] = 100.0 * np.sum(controlCorrect) / (np.sum(controlCorrect) + np.sum(controlIncorrect))

            # -- compute bias to a side as difference/sum --
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

        # -- compute overall change in accuracy and bias for control condition --
        laserCorrect = correct[trialsEachLaser[:, 1]]
        laserIncorrect = incorrect[trialsEachLaser[:, 1]]
        controlCorrect = correct[trialsEachLaser[:, 0]]
        controlIncorrect = incorrect[trialsEachLaser[:, 0]]
        controlChangeAccuracy[indMouse] = (100.0 * np.sum(laserCorrect) / (np.sum(laserCorrect) + np.sum(laserIncorrect))) - (100.0 * np.sum(controlCorrect) / (np.sum(controlCorrect) + np.sum(controlIncorrect)))

        laserToneChoice = toneChoice[trialsEachLaser[:, 1]]
        laserNoiseChoice = noiseChoice[trialsEachLaser[:, 1]]
        controlToneChoice = toneChoice[trialsEachLaser[:, 0]]
        controlNoiseChoice = noiseChoice[trialsEachLaser[:, 0]]
        controlChangeBias[indMouse] = 1.0 * ((np.sum(laserToneChoice) - np.sum(laserNoiseChoice)) / (np.sum(laserToneChoice) + np.sum(laserNoiseChoice)))-((np.sum(controlToneChoice) - np.sum(controlNoiseChoice)) / (np.sum(controlToneChoice) + np.sum(controlNoiseChoice)))

        # -- compute overall change in accuracy and bias for experimental condition --
        trialsEachCond, trialsEachLaser, valid, correct, incorrect, toneChoice, noiseChoice, numBands = load_data_for_this_stuff(mouse, '10mW laser')
        laserCorrect = correct[trialsEachLaser[:, 1]]
        laserIncorrect = incorrect[trialsEachLaser[:, 1]]
        controlCorrect = correct[trialsEachLaser[:, 0]]
        controlIncorrect = incorrect[trialsEachLaser[:, 0]]
        expChangeAccuracy[indMouse] = (100.0 * np.sum(laserCorrect) / (np.sum(laserCorrect) + np.sum(laserIncorrect))) - (
                    100.0 * np.sum(controlCorrect) / (np.sum(controlCorrect) + np.sum(controlIncorrect)))

        laserToneChoice = toneChoice[trialsEachLaser[:, 1]]
        laserNoiseChoice = noiseChoice[trialsEachLaser[:, 1]]
        controlToneChoice = toneChoice[trialsEachLaser[:, 0]]
        controlNoiseChoice = noiseChoice[trialsEachLaser[:, 0]]
        expChangeBias[indMouse] = 1.0 * ((np.sum(laserToneChoice) - np.sum(laserNoiseChoice)) / (
                    np.sum(laserToneChoice) + np.sum(laserNoiseChoice))) - (
                                                  (np.sum(controlToneChoice) - np.sum(controlNoiseChoice)) / (
                                                      np.sum(controlToneChoice) + np.sum(controlNoiseChoice)))

    laserAccuracy.append(thisLaserAccuracy)
    controlAccuracy.append(thisControlAccuracy)

    laserBias.append(thisLaserBias)
    controlBias.append(thisControlBias)

    changeAccuracy.append([controlChangeAccuracy, expChangeAccuracy])
    changeBias.append([controlChangeBias, expChangeBias])


# -- save analysis of behav data --
outputFile = 'all_behaviour_inhib_inactivation_control.npz'
outputFullPath = os.path.join(inactDataDir, outputFile)
np.savez(outputFullPath,
         PVlaserAccuracy=laserAccuracy[0], PVcontrolAccuracy=controlAccuracy[0],
         PVlaserBias=laserBias[0], PVcontrolBias=controlBias[0],
         SOMlaserAccuracy=laserAccuracy[1], SOMcontrolAccuracy=controlAccuracy[1],
         SOMlaserBias=laserBias[1], SOMcontrolBias=controlBias[1],
         PVcontrolChangeAccuracy=changeAccuracy[0][0], PVexpChangeAccuracy=changeAccuracy[0][1],
         PVcontrolChangeBias=changeBias[0][0], PVexpChangeBias=changeBias[0][1],
         SOMcontrolChangeAccuracy=changeAccuracy[1][0], SOMexpChangeAccuracy=changeAccuracy[1][1],
         SOMcontrolChangeBias=changeBias[1][0], SOMexpChangeBias=changeBias[1][1],
         possibleBands=numBands)
print(outputFile + " saved")
