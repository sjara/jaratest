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

BAND_TO_USE = 0.25 # just looking at data from 0.25 octaves as effects seem to be larger


def calculate_tone_diff(behavData):
    numLasers = np.unique(behavData['laserSide'])
    numBands = np.unique(behavData['currentBand'])
    numSNRs = np.unique(behavData['currentSNR'])

    trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['laserSide'], numLasers,
                                                                   behavData['currentBand'], numBands)
    trialsEachSNR = behavioranalysis.find_trials_each_type(behavData['currentSNR'], numSNRs)

    trialsEachCond3Params = np.zeros((len(behavData['laserSide']), len(numLasers), len(numBands), len(numSNRs)), dtype=bool)
    for ind in range(len(numSNRs)):
        trialsEachCond3Params[:, :, :, ind] = trialsEachCond & trialsEachSNR[:, ind][:, np.newaxis, np.newaxis]

    # valid = behavData['valid'].astype(bool)
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

    band = np.argwhere(numBands == BAND_TO_USE).flatten()[0]

    thisPsyCurve = np.zeros((len(numLasers), len(numSNRs)))
    for laser in range(len(numLasers)):
        for snr in range(len(numSNRs)):
            toneChoiceThisCond = toneChoice[trialsEachCond3Params[:, laser, band, snr]]
            noiseChoiceThisCond = noiseChoice[trialsEachCond3Params[:, laser, band, snr]]
            thisPsyCurve[laser, snr] = 100.0 * np.sum(toneChoiceThisCond) / (np.sum(noiseChoiceThisCond) + np.sum(toneChoiceThisCond))

    thisToneDetectDiff = np.diff(thisPsyCurve, axis=0)

    correctBySide = np.zeros((len(numLasers), 2, 2)) #laser, correct/incorrect, tone/noise
    for laser in range(len(numLasers)):
        toneChoiceThisCond = toneChoice[trialsEachCond[:, laser, band]]
        noiseChoiceThisCond = noiseChoice[trialsEachCond[:, laser, band]]
        correctThisCond = correct[trialsEachCond[:, laser, band]]
        incorrectThisCond = incorrect[trialsEachCond[:, laser, band]]

        correctBySide[laser, 0, 0] = np.sum(toneChoiceThisCond & correctThisCond)
        correctBySide[laser, 0, 1] = np.sum(noiseChoiceThisCond & correctThisCond)
        correctBySide[laser, 1, 0] = np.sum(toneChoiceThisCond & incorrectThisCond)
        correctBySide[laser, 1, 1] = np.sum(noiseChoiceThisCond & incorrectThisCond)

    return thisToneDetectDiff, correctBySide


diffToneDetectLaser = []
diffToneDetectControl = []
toneReportBySideLaser = []
toneReportBySideControl = []
correctBySideLaser = []
correctBySideControl = []

for indType, mice in enumerate(mouseType):

    thisToneDetectDiffLaser = None
    thisToneDetectDiffControl = None
    thisToneReportBySideLaser = None
    thisToneReportBySideControl = None
    thisCorrectBySideLaser = None
    thisCorrectBySideControl = None

    for indMouse, mouse in enumerate(mice):

        laserSessions = studyparams.miceDict[mouse]['10mW laser']
        laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

        laserToneDetectDiff, thisCorrectNumsLaser = calculate_tone_diff(laserBehavData)

        controlSessions = studyparams.miceDict[mouse]['10mW control']
        controlBehavData = behavioranalysis.load_many_sessions(mouse, controlSessions)

        controlToneDetectDiff, thisCorrectNumsControl = calculate_tone_diff(controlBehavData)

        if thisToneDetectDiffLaser is None:
            thisToneDetectDiffLaser = np.zeros((len(mice),laserToneDetectDiff.shape[1]))
            thisToneDetectDiffControl = np.zeros_like(thisToneDetectDiffLaser)
            thisCorrectBySideLaser = np.zeros((len(mice), 2, 2)) # mouse, laser, tone/noise
            thisCorrectBySideControl = np.zeros((len(mice), 2, 2))
            thisToneReportBySideLaser = np.zeros_like(thisCorrectBySideLaser)
            thisToneReportBySideControl = np.zeros_like(thisToneReportBySideLaser)

        thisToneDetectDiffLaser[indMouse, :] = laserToneDetectDiff
        thisToneDetectDiffControl[indMouse, :] = controlToneDetectDiff

        thisCorrectBySideLaser[indMouse, 0, 0] = 100.0 * thisCorrectNumsLaser[0, 0, 0]/(thisCorrectNumsLaser[0, 0, 0] + thisCorrectNumsLaser[0, 1, 0])
        thisCorrectBySideLaser[indMouse, 1, 0] = 100.0 * thisCorrectNumsLaser[1, 0, 0] / (thisCorrectNumsLaser[1, 0, 0] + thisCorrectNumsLaser[1, 1, 0])
        thisCorrectBySideLaser[indMouse, 0, 1] = 100.0 * thisCorrectNumsLaser[0, 0, 1] / (thisCorrectNumsLaser[0, 0, 1] + thisCorrectNumsLaser[0, 1, 1])
        thisCorrectBySideLaser[indMouse, 1, 1] = 100.0 * thisCorrectNumsLaser[1, 0, 1] / (thisCorrectNumsLaser[1, 0, 1] + thisCorrectNumsLaser[1, 1, 1])

        thisCorrectBySideControl[indMouse, 0, 0] = 100.0 * thisCorrectNumsControl[0, 0, 0] / (thisCorrectNumsControl[0, 0, 0] + thisCorrectNumsControl[0, 1, 0])
        thisCorrectBySideControl[indMouse, 1, 0] = 100.0 * thisCorrectNumsControl[1, 0, 0] / (thisCorrectNumsControl[1, 0, 0] + thisCorrectNumsControl[1, 1, 0])
        thisCorrectBySideControl[indMouse, 0, 1] = 100.0 * thisCorrectNumsControl[0, 0, 1] / (thisCorrectNumsControl[0, 0, 1] + thisCorrectNumsControl[0, 1, 1])
        thisCorrectBySideControl[indMouse, 1, 1] = 100.0 * thisCorrectNumsControl[1, 0, 1] / (thisCorrectNumsControl[1, 0, 1] + thisCorrectNumsControl[1, 1, 1])

        thisToneReportBySideLaser[indMouse, 0, 0] = 100.0 * thisCorrectNumsLaser[0, 0, 0] / (thisCorrectNumsLaser[0, 0, 0] + thisCorrectNumsLaser[0, 1, 1])
        thisToneReportBySideLaser[indMouse, 1, 0] = 100.0 * thisCorrectNumsLaser[1, 0, 0] / (thisCorrectNumsLaser[1, 0, 0] + thisCorrectNumsLaser[1, 1, 1])
        thisToneReportBySideLaser[indMouse, 0, 1] = 100.0 * thisCorrectNumsLaser[0, 1, 0] / (thisCorrectNumsLaser[0, 0, 1] + thisCorrectNumsLaser[0, 1, 0])
        thisToneReportBySideLaser[indMouse, 1, 1] = 100.0 * thisCorrectNumsLaser[1, 1, 0] / (thisCorrectNumsLaser[1, 0, 1] + thisCorrectNumsLaser[1, 1, 0])

        thisToneReportBySideControl[indMouse, 0, 0] = 100.0 * thisCorrectNumsControl[0, 0, 0] / (thisCorrectNumsControl[0, 0, 0] + thisCorrectNumsControl[0, 1, 1])
        thisToneReportBySideControl[indMouse, 1, 0] = 100.0 * thisCorrectNumsControl[1, 0, 0] / (thisCorrectNumsControl[1, 0, 0] + thisCorrectNumsControl[1, 1, 1])
        thisToneReportBySideControl[indMouse, 0, 1] = 100.0 * thisCorrectNumsControl[0, 1, 0] / (thisCorrectNumsControl[0, 0, 1] + thisCorrectNumsControl[0, 1, 0])
        thisToneReportBySideControl[indMouse, 1, 1] = 100.0 * thisCorrectNumsControl[1, 1, 0] / (thisCorrectNumsControl[1, 0, 1] + thisCorrectNumsControl[1, 1, 0])

    diffToneDetectLaser.append(thisToneDetectDiffLaser)
    diffToneDetectControl.append(thisToneDetectDiffControl)
    correctBySideLaser.append(thisCorrectBySideLaser)
    correctBySideControl.append(thisCorrectBySideControl)
    toneReportBySideLaser.append(thisToneReportBySideLaser)
    toneReportBySideControl.append(thisToneReportBySideControl)

# -- save responses of all sound responsive cells to 0.25 bandwidth sounds --
outputFile = 'change_behaviour_by_snr_inhib_inactivation.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         PVchangeToneDetect=diffToneDetectLaser[0], SOMchangeToneDetect=diffToneDetectLaser[1],
         PVchangeToneDetectControl=diffToneDetectControl[0], SOMchangeToneDetectControl=diffToneDetectControl[1],
         PVtoneReportBySide=toneReportBySideLaser[0], SOMtoneReportBySide=toneReportBySideLaser[1],
         PVtoneReportBySideControl=toneReportBySideControl[0], SOMtoneReportBySideControl=toneReportBySideControl[1],
         PVcorrectBySide=correctBySideLaser[0], SOMcorrectBySide=correctBySideLaser[1],
         PVcorrectBySideControl=correctBySideControl[0], SOMcorrectBySideControl=correctBySideControl[1],
         possibleSNRs=np.unique(laserBehavData['currentSNR']))
print(outputFile + " saved")