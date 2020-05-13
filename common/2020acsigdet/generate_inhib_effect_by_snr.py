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

diffToneDetect = []

for indType, mice in enumerate(mouseType):

    thisToneDetectDiff = None

    for indMouse, mouse in enumerate(mice):

        laserSessions = studyparams.miceDict[mouse]['10mW laser']
        laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

        numLasers = np.unique(laserBehavData['laserSide'])
        numBands = np.unique(laserBehavData['currentBand'])
        numSNRs = np.unique(laserBehavData['currentSNR'])

        trialsEachCond = behavioranalysis.find_trials_each_combination(laserBehavData['laserSide'], numLasers,
                                                                       laserBehavData['currentBand'], numBands)
        trialsEachSNR = behavioranalysis.find_trials_each_type(laserBehavData['currentSNR'], numSNRs)

        trialsEachCond3Params = np.zeros(
            (len(laserBehavData['laserSide']), len(numLasers), len(numBands), len(numSNRs)), dtype=bool)
        for ind in range(len(numSNRs)):
            trialsEachCond3Params[:, :, :, ind] = trialsEachCond & trialsEachSNR[:, ind][:, np.newaxis, np.newaxis]

        valid = laserBehavData['valid'].astype(bool)
        correct = laserBehavData['outcome'] == laserBehavData.labels['outcome']['correct']
        rightChoice = laserBehavData['choice'] == laserBehavData.labels['choice']['right']
        leftChoice = laserBehavData['choice'] == laserBehavData.labels['choice']['left']

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

        band = np.argwhere(numBands == BAND_TO_USE).flatten()[0]

        if thisToneDetectDiff is None:
            thisToneDetectDiff = np.zeros((len(mice), len(numSNRs)))

        thisPsyCurve = np.zeros((len(numLasers), len(numSNRs)))
        for laser in range(len(numLasers)):
            for snr in range(len(numSNRs)):
                validThisCond = valid[trialsEachCond3Params[:, laser, band, snr]]
                toneChoiceThisCond = toneChoice[trialsEachCond3Params[:, laser, band, snr]]
                thisPsyCurve[laser, snr] = 100.0 * np.sum(toneChoiceThisCond) / np.sum(validThisCond)

        thisToneDetectDiff[indMouse,:] = np.diff(thisPsyCurve, axis=0)

    diffToneDetect.append(thisToneDetectDiff)

# -- save responses of all sound responsive cells to 0.25 bandwidth sounds --
outputFile = 'change_behaviour_by_snr_inhib_inactivation.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         PVchangeToneDetect=diffToneDetect[0], SOMchangeToneDetect=diffToneDetect[1],
         possibleSNRs=numSNRs)
print(outputFile + " saved")