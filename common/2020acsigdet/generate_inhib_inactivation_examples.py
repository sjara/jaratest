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
             'sessions': '10mW'},  # example SOM-ArchT psychometric

            {'subject': 'band081',
             'sessions': '10mW'},  # example PV-ArchT psychometric with increase in FAR

            {'subject': 'band137',
             'sessions': '10mW'}]  # example PV-ArchT psychometric with decrease in HR

sessionTypes = ['laser', 'control']

for example in examples:
    psyCurvesLaser = []
    upperErrorsLaser = []
    lowerErrorsLaser = []
    psyCurvesNoLaser = []
    upperErrorsNoLaser = []
    lowerErrorsNoLaser = []
    for type in sessionTypes:
        sessions = studyparams.miceDict[example['subject']][f"{example['sessions']} {type}"]
        behavData = behavioranalysis.load_many_sessions(example['subject'], sessions)

        numLasers = np.unique(behavData['laserSide'])
        numSNRs = np.unique(behavData['currentSNR'])

        trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['laserSide'], numLasers,
                                                                       behavData['currentSNR'], numSNRs)
        # trialsEachSNR = behavioranalysis.find_trials_each_type(behavData['currentSNR'], numSNRs)
        #
        # trialsEachCond3Params = np.zeros((len(behavData['laserSide']), len(numLasers), len(numBands), len(numSNRs)),
        #                                  dtype=bool)
        # for ind in range(len(numSNRs)):
        #     trialsEachCond3Params[:, :, :, ind] = trialsEachCond & trialsEachSNR[:, ind][:, np.newaxis, np.newaxis]

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

        # band = np.argwhere(numBands == example['bandwidth']).flatten()[0]

        for laser in range(len(numLasers)):
            thisPsyCurve = np.zeros(len(numSNRs))
            upperErrorBar = np.zeros(len(numSNRs))
            lowerErrorBar = np.zeros(len(numSNRs))
            for snr in range(len(numSNRs)):
                toneChoiceThisCond = toneChoice[trialsEachCond[:, laser, snr]]
                noiseChoiceThisCond = noiseChoice[trialsEachCond[:, laser, snr]]
                thisPsyCurve[snr] = 100.0 * np.sum(toneChoiceThisCond) / (np.sum(toneChoiceThisCond) + np.sum(noiseChoiceThisCond))

                CIthisSNR = np.array(proportion_confint(np.sum(toneChoiceThisCond), (np.sum(toneChoiceThisCond) + np.sum(noiseChoiceThisCond)), method='wilson'))
                upperErrorBar[snr] = 100.0 * CIthisSNR[1] - thisPsyCurve[snr]
                lowerErrorBar[snr] = thisPsyCurve[snr] - 100.0 * CIthisSNR[0]

            if laser:
                psyCurvesLaser.append(thisPsyCurve)
                upperErrorsLaser.append(upperErrorBar)
                lowerErrorsLaser.append(lowerErrorBar)
            else:
                psyCurvesNoLaser.append(thisPsyCurve)
                upperErrorsNoLaser.append(upperErrorBar)
                lowerErrorsNoLaser.append(lowerErrorBar)

    # -- save data --
    outputFile = '{}_psycurve.npz'.format(example['subject'])
    outputFullPath = os.path.join(dataDir, outputFile)
    np.savez(outputFullPath,
             psyCurveLaserInControl=psyCurvesNoLaser[0], upperErrorLaserInControl=upperErrorsNoLaser[0], lowerErrorLaserInControl=lowerErrorsNoLaser[0],
             psyCurveLaserIn=psyCurvesLaser[0], upperErrorLaserIn=upperErrorsLaser[0], lowerErrorLaserIn=lowerErrorsLaser[0],
             psyCurveLaserOutControl=psyCurvesNoLaser[1], upperErrorLaserOutControl=upperErrorsNoLaser[1], lowerErrorLaserOutControl=lowerErrorsNoLaser[1],
             psyCurveLaserOut=psyCurvesLaser[1], upperErrorLaserOut=upperErrorsLaser[1], lowerErrorLaserOut=lowerErrorsLaser[1],
             possibleSNRs=numSNRs)
    print(outputFile + " saved")
