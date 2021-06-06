import os
import numpy as np

from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import studyparams

figName = 'figure_ac_inactivation'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

examples = [{'subject': 'band046',
             'sessions': '3mW laser',
             'bandwidth': 0.25}]  # example PV-ChR2 psychometric

for example in examples:
    sessions = studyparams.miceDict[example['subject']][example['sessions']]
    behavData = behavioranalysis.load_many_sessions(example['subject'], sessions)

    numLasers = np.unique(behavData['laserSide'])
    numBands = np.unique(behavData['currentBand'])
    numSNRs = np.unique(behavData['currentSNR'])

    trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['laserSide'], numLasers,
                                                                   behavData['currentBand'], numBands)

    if all(~np.isnan(behavData['timeCenterOut'])):
        reactionTimes = behavData['timeCenterOut'] - behavData['timeTarget']
        decisionTimes = behavData['timeSideIn'] - behavData['timeCenterOut']
    else:
        reactionTimes = []
        decisionTimes = []
        for session in sessions:
            thisBehavFile = os.path.join(settings.BEHAVIOR_PATH, example['subject'], example['subject'] + '_2afc_' + session + '.h5')
            if os.path.exists(thisBehavFile):
                thisBehavData = loadbehavior.BehaviorData(thisBehavFile, readmode='full')
            timeSound = thisBehavData['timeTarget']
            timeCenterOut = np.zeros(len(timeSound))
            timeSideIn = thisBehavData['timeSideIn']

            eventCode = np.array(thisBehavData.events['eventCode'])
            eventTime = thisBehavData.events['eventTime']
            CoutInds = np.where(eventCode == behavData.stateMatrix['eventsNames']['Cout'])[0]

            for trial in range(len(timeSound)):
                soundEventInd = np.where(eventTime == timeSound[trial])[0][0]
                CoutInd = CoutInds[np.argmax(CoutInds > soundEventInd)]
                timeCenterOut[trial] = eventTime[CoutInd]

            thisReactionTimes = timeCenterOut - timeSound
            thisDecisionTimes = timeSideIn - timeCenterOut

            reactionTimes.extend(thisReactionTimes)
            decisionTimes.extend(thisDecisionTimes)

        reactionTimes = np.array(reactionTimes)
        decisionTimes = np.array(decisionTimes)

    band = np.argwhere(numBands == example['bandwidth']).flatten()[0]
    trialsEachLaser = trialsEachCond[:,:,band]

    controlReactionTimes = reactionTimes[trialsEachLaser[:,0]]
    controlReactionTimes = controlReactionTimes[np.isfinite(controlReactionTimes)]
    laserReactionTimes = reactionTimes[trialsEachLaser[:,1]]
    laserReactionTimes = laserReactionTimes[np.isfinite(laserReactionTimes)]

    controlDecisionTimes = decisionTimes[trialsEachLaser[:,0]]
    controlDecisionTimes = controlDecisionTimes[np.isfinite(controlDecisionTimes)]
    laserDecisionTimes = decisionTimes[trialsEachLaser[:,1]]
    laserDecisionTimes = laserDecisionTimes[np.isfinite(laserDecisionTimes)]

    # -- save data --
    outputFile = '{}_reaction_times.npz'.format(example['subject'])
    outputFullPath = os.path.join(dataDir, outputFile)
    np.savez(outputFullPath,
             controlReactionTimes=controlReactionTimes, laserReactionTimes=laserReactionTimes,
             controlDecisionTimes=controlDecisionTimes, laserDecisionTimes=laserDecisionTimes)
    print(outputFile + " saved")