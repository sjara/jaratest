import os
import numpy as np

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

controlChangeAccuracy = np.zeros(len(PV_CHR2_MICE))
expChangeAccuracy = np.zeros_like(controlChangeAccuracy)

controlChangeBias = np.zeros_like(controlChangeAccuracy)
expChangeBias = np.zeros_like(controlChangeAccuracy)

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

    return trialsEachCond, trialsEachLaser, valid, correct, toneChoice, noiseChoice, numBands

for indMouse, mouse in enumerate(PV_CHR2_MICE):

    trialsEachCond, trialsEachLaser, valid, correct, toneChoice, noiseChoice, numBands = load_data_for_this_stuff(mouse, '3mW control')

    # -- compute accuracies and bias for each bandwidth in control condition --
    for indBand in range(len(numBands)):
        trialsEachLaser = trialsEachCond[:, :, indBand]

        # -- sort trials by laser presentation, compute accuracy as percent correct trials out of all valid trials --
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

        # -- compute bias to a side as difference/sum --
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

    # -- compute overall change in accuracy and bias for control condition --
    laserValid = valid[trialsEachLaser[:, 1]]
    laserCorrect = correct[trialsEachLaser[:, 1]]
    controlValid = valid[trialsEachLaser[:, 0]]
    controlCorrect = correct[trialsEachLaser[:, 0]]
    controlChangeAccuracy[indMouse] = (100.0 * np.sum(laserCorrect) / np.sum(laserValid)) - (100.0 * np.sum(controlCorrect) / np.sum(controlValid))

    laserToneChoice = toneChoice[trialsEachLaser[:, 1]]
    laserNoiseChoice = noiseChoice[trialsEachLaser[:, 1]]
    controlToneChoice = toneChoice[trialsEachLaser[:, 0]]
    controlNoiseChoice = noiseChoice[trialsEachLaser[:, 0]]
    controlChangeBias[indMouse] = 1.0 * ((np.sum(laserToneChoice) - np.sum(laserNoiseChoice)) / (np.sum(laserToneChoice) + np.sum(laserNoiseChoice)))-((np.sum(controlToneChoice) - np.sum(controlNoiseChoice)) / (np.sum(controlToneChoice) + np.sum(controlNoiseChoice)))

    # -- compute overall change in accuracy and bias for experimental condition --
    trialsEachCond, trialsEachLaser, valid, correct, toneChoice, noiseChoice, numBands = load_data_for_this_stuff(mouse, '3mW laser')
    laserValid = valid[trialsEachLaser[:, 1]]
    laserCorrect = correct[trialsEachLaser[:, 1]]
    controlValid = valid[trialsEachLaser[:, 0]]
    controlCorrect = correct[trialsEachLaser[:, 0]]
    expChangeAccuracy[indMouse] = (100.0 * np.sum(laserCorrect) / np.sum(laserValid)) - (
                100.0 * np.sum(controlCorrect) / np.sum(controlValid))

    laserToneChoice = toneChoice[trialsEachLaser[:, 1]]
    laserNoiseChoice = noiseChoice[trialsEachLaser[:, 1]]
    controlToneChoice = toneChoice[trialsEachLaser[:, 0]]
    controlNoiseChoice = noiseChoice[trialsEachLaser[:, 0]]
    expChangeBias[indMouse] = 1.0 * ((np.sum(laserToneChoice) - np.sum(laserNoiseChoice)) / (
                np.sum(laserToneChoice) + np.sum(laserNoiseChoice))) - (
                                              (np.sum(controlToneChoice) - np.sum(controlNoiseChoice)) / (
                                                  np.sum(controlToneChoice) + np.sum(controlNoiseChoice)))

# -- save analysis of behav data --
outputFile = 'all_behaviour_ac_inactivation_control.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         laserAccuracy=laserAccuracy, controlAccuracy=controlAccuracy,
         laserBias=laserBias, controlBias=controlBias,
         controlChangeAccuracy=controlChangeAccuracy, expChangeAccuracy=expChangeAccuracy,
         controlChangeBias=controlChangeBias, expChangeBias=expChangeBias,
         possibleBands=numBands)
print(outputFile + " saved")
