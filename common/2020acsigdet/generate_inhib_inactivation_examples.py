import os
import numpy as np
from statsmodels.stats.proportion import proportion_confint

from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import studyparams

figName = 'figure_inhibitory_inactivation'
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

examples = [{'subject': 'band065',
             'sessions': '10mW laser',
             'bandwidth': 0.25},  # example SOM-ArchT psychometric

            {'subject': 'band081',
             'sessions': '10mW laser',
             'bandwidth': 0.25}]  # example PV-ArchT psychometric

for example in examples:
    sessions = studyparams.miceDict[example['subject']][example['sessions']]
    behavData = behavioranalysis.load_many_sessions(example['subject'], sessions)

    numLasers = np.unique(behavData['laserSide'])
    numBands = np.unique(behavData['currentBand'])
    numSNRs = np.unique(behavData['currentSNR'])

    trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['laserSide'], numLasers,
                                                                   behavData['currentBand'], numBands)
    trialsEachSNR = behavioranalysis.find_trials_each_type(behavData['currentSNR'], numSNRs)

    trialsEachCond3Params = np.zeros((len(behavData['laserSide']), len(numLasers), len(numBands), len(numSNRs)),
                                     dtype=bool)
    for ind in range(len(numSNRs)):
        trialsEachCond3Params[:, :, :, ind] = trialsEachCond & trialsEachSNR[:, ind][:, np.newaxis, np.newaxis]

    valid = behavData['valid'].astype(bool)
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

    band = np.argwhere(numBands == example['bandwidth']).flatten()[0]
    psyCurves = []
    upperErrors = []
    lowerErrors = []

    for laser in range(len(numLasers)):
        thisPsyCurve = np.zeros(len(numSNRs))
        upperErrorBar = np.zeros(len(numSNRs))
        lowerErrorBar = np.zeros(len(numSNRs))
        for snr in range(len(numSNRs)):
            validThisCond = valid[trialsEachCond3Params[:, laser, band, snr]]
            toneChoiceThisCond = toneChoice[trialsEachCond3Params[:, laser, band, snr]]
            thisPsyCurve[snr] = 100.0 * np.sum(toneChoiceThisCond) / np.sum(validThisCond)

            CIthisSNR = np.array(proportion_confint(np.sum(toneChoiceThisCond), np.sum(validThisCond), method='wilson'))
            upperErrorBar[snr] = 100.0 * CIthisSNR[1] - thisPsyCurve[snr]
            lowerErrorBar[snr] = thisPsyCurve[snr] - 100.0 * CIthisSNR[0]

        psyCurves.append(thisPsyCurve)
        upperErrors.append(upperErrorBar)
        lowerErrors.append(lowerErrorBar)

    # -- save data --
    outputFile = '{}_psycurve.npz'.format(example['subject'])
    outputFullPath = os.path.join(dataDir, outputFile)
    np.savez(outputFullPath,
             psyCurveControl=psyCurves[0], upperErrorControl=upperErrors[0], lowerErrorControl=lowerErrors[0],
             psyCurveLaser=psyCurves[1], upperErrorLaser=upperErrors[1], lowerErrorLaser=lowerErrors[1],
             possibleSNRs=numSNRs)
    print(outputFile + " saved")
