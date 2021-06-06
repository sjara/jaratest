import os
import numpy as np
import pandas as pd

from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import studyparams

figName = 'figure_inhibitory_inactivation'
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

dbName = 'good_sessions.csv'
# dataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
dbPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
sessionDB = pd.read_csv(dbPath)

dbName = 'good_mice.csv'
# dataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
dbPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
mouseDB = pd.read_csv(dbPath)

mouseRow = mouseDB.query('strain=="PVArchT"')
PV_ARCHT_MICE = mouseRow['mice'].apply(eval).iloc[-1]
mouseRow = mouseDB.query('strain=="SOMArchT"')
SOM_ARCHT_MICE = mouseRow['mice'].apply(eval).iloc[-1]
mouseType = [PV_ARCHT_MICE, SOM_ARCHT_MICE]

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

    thisPsyCurve = np.zeros((len(numLasers), len(numBands), len(numSNRs)))
    thisAccuracy = np.zeros((len(numLasers), len(numBands), len(numSNRs)))
    thisTrialsByCond = np.zeros((len(numLasers), len(numBands), len(numSNRs), 2)) # final dim correct/incorrect
    for laser in range(len(numLasers)):
        for band in range(len(numBands)):
            for snr in range(len(numSNRs)):
                toneChoiceThisCond = toneChoice[trialsEachCond3Params[:, laser, band, snr]]
                noiseChoiceThisCond = noiseChoice[trialsEachCond3Params[:, laser, band, snr]]
                thisPsyCurve[laser, band, snr] = 100.0 * np.sum(toneChoiceThisCond) / (np.sum(noiseChoiceThisCond) + np.sum(toneChoiceThisCond))

                correctThisCond = correct[trialsEachCond3Params[:, laser, band, snr]]
                incorrectThisCond = incorrect[trialsEachCond3Params[:, laser, band, snr]]
                thisAccuracy[laser, band,snr] = 100.0 * np.sum(correctThisCond) / (np.sum(correctThisCond) + np.sum(incorrectThisCond))
                thisTrialsByCond[laser, band, snr, 0] = np.sum(correctThisCond)
                thisTrialsByCond[laser, band, snr, 1] = np.sum(incorrectThisCond)

    #thisToneDetectDiff = np.diff(thisPsyCurve, axis=0)

    return thisPsyCurve, thisAccuracy, thisTrialsByCond


diffToneDetectLaser = []
diffToneDetectControl = []
accuracyLaser = []
accuracyControl = []
trialCountsLaser = []
trialCountsControl = []

for indType, mice in enumerate(mouseType):

    thisToneDetectDiffLaser = None
    thisToneDetectDiffControl = None
    thisAccuracyLaser = None
    thisAccuracyControl = None
    thisTrialCountsLaser = None
    thisTrialCountsControl = None

    for indMouse, mouse in enumerate(mice):

        dbRow = sessionDB.query('mouse==@mouse and sessionType=="10mW laser"')
        laserSessions = dbRow['goodSessions'].apply(eval).iloc[-1]
        laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

        toneDetectDiff, accuraciesByCond, trialsByCond = calculate_tone_diff(laserBehavData)

        dbRow = sessionDB.query('mouse==@mouse and sessionType=="10mW control"')
        controlSessions = dbRow['goodSessions'].apply(eval).iloc[-1]
        controlBehavData = behavioranalysis.load_many_sessions(mouse, controlSessions)

        controlToneDetectDiff, controlAccuraciesByCond, trialsByCondControl = calculate_tone_diff(controlBehavData)

        if thisToneDetectDiffLaser is None:
            thisToneDetectDiffLaser = np.zeros(tuple([len(mice)]+list(toneDetectDiff.shape)))
            thisToneDetectDiffControl = np.zeros_like(thisToneDetectDiffLaser)
            thisAccuracyLaser = np.zeros_like(thisToneDetectDiffLaser)
            thisAccuracyControl = np.zeros_like(thisToneDetectDiffLaser)
            thisTrialCountsLaser = np.zeros(tuple([len(mice)] + list(trialsByCond.shape))) # mouse, laser, tone/noise
            thisTrialCountsControl = np.zeros_like(thisTrialCountsLaser)

        thisToneDetectDiffLaser[indMouse, :] = toneDetectDiff
        thisToneDetectDiffControl[indMouse, :] = controlToneDetectDiff
        thisAccuracyLaser[indMouse, :] = accuraciesByCond
        thisAccuracyControl[indMouse, :] = controlAccuraciesByCond
        thisTrialCountsLaser[indMouse,:] = trialsByCond
        thisTrialCountsControl[indMouse, :] = trialsByCondControl

    diffToneDetectLaser.append(thisToneDetectDiffLaser)
    diffToneDetectControl.append(thisToneDetectDiffControl)
    accuracyLaser.append(thisAccuracyLaser)
    accuracyControl.append(thisAccuracyControl)
    trialCountsLaser.append(thisTrialCountsLaser)
    trialCountsControl.append(thisTrialCountsControl)

# -- save responses of all sound responsive cells to 0.25 bandwidth sounds --
outputFile = 'change_behaviour_by_snr_inhib_inactivation_v2.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         PVpsyCurves=diffToneDetectLaser[0], SOMpsyCurves=diffToneDetectLaser[1],
         PVpsyCurvesControl=diffToneDetectControl[0], SOMpsyCurvesControl=diffToneDetectControl[1],
         PVaccuracies=accuracyLaser[0], SOMaccuracies=accuracyLaser[1],
         PVaccuraciesControl=accuracyControl[0], SOMaccuraciesControl=accuracyControl[1],
         PVtrialCounts=trialCountsLaser[0], SOMtrialCounts=trialCountsLaser[1],
         PVtrialCountsControl=trialCountsControl[0], SOMtrialCountsControl=trialCountsControl[1],
         possibleSNRs=np.unique(laserBehavData['currentSNR']), possibleBands=np.unique(np.unique(laserBehavData['currentBand'])))
print(outputFile + " saved")