import os
import numpy as np

from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import studyparams

figName = 'figure_ac_inactivation'
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

PV_CHR2_MICE = studyparams.PV_CHR2_MICE
BANDS_TO_USE = [0, -1] # ignore intermediate bandwidth for mice it was done

sessionTypes = ['3mW laser', '3mW control']

laserReaction = []
controlReaction = []

laserDecision = []
controlDecision = []

for sessionType in sessionTypes:

    thisLaserReaction = None
    thisControlReaction = None
    thisLaserDecision = None
    thisControlDecision = None

    for indMouse, mouse in enumerate(PV_CHR2_MICE):

        laserSessions = studyparams.miceDict[mouse][sessionType]
        laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

        if all(~np.isnan(laserBehavData['timeCenterOut'])):
            reactionTimes = laserBehavData['timeCenterOut'] - laserBehavData['timeTarget']
            decisionTimes = laserBehavData['timeSideIn'] - laserBehavData['timeCenterOut']
        else:
            reactionTimes = []
            decisionTimes = []
            for session in laserSessions:
                thisBehavFile = os.path.join(settings.BEHAVIOR_PATH, mouse, mouse + '_2afc_' + session + '.h5')
                if os.path.exists(thisBehavFile):
                    thisBehavData = loadbehavior.BehaviorData(thisBehavFile, readmode='full')
                timeSound = thisBehavData['timeTarget']
                timeCenterOut = np.zeros(len(timeSound))
                timeSideIn = thisBehavData['timeSideIn']

                eventCode = np.array(thisBehavData.events['eventCode'])
                eventTime = thisBehavData.events['eventTime']
                CoutInds = np.where(eventCode == laserBehavData.stateMatrix['eventsNames']['Cout'])[0]

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

        numLasers = np.unique(laserBehavData['laserSide'])
        numBands = np.unique(laserBehavData['currentBand'])

        trialsEachCond = behavioranalysis.find_trials_each_combination(laserBehavData['laserSide'], numLasers,
                                                                       laserBehavData['currentBand'], numBands)

        # -- compute reaction and decision times for each bandwidth --

        for indBand in BANDS_TO_USE:
            trialsEachLaser = trialsEachCond[:, :, indBand]

            # -- sort trials by laser presentation, compute reaction times as time diff between sound on and center out --
            if thisLaserReaction is None:
                thisLaserReaction = np.zeros((len(PV_CHR2_MICE), len(BANDS_TO_USE)))
            laserReactionTimes = reactionTimes[trialsEachLaser[:,1]]
            laserReactionTimes = laserReactionTimes[np.isfinite(laserReactionTimes)]
            thisLaserReaction[indMouse, indBand] = np.mean(laserReactionTimes)

            if thisControlReaction is None:
                thisControlReaction = np.zeros((len(PV_CHR2_MICE), len(BANDS_TO_USE)))
            controlReactionTimes = reactionTimes[trialsEachLaser[:, 0]]
            controlReactionTimes = controlReactionTimes[np.isfinite(controlReactionTimes)]
            thisControlReaction[indMouse, indBand] = np.mean(controlReactionTimes)

            # -- compute decision time as time diff between center out and side in --
            if thisLaserDecision is None:
                thisLaserDecision = np.zeros((len(PV_CHR2_MICE), len(BANDS_TO_USE)))
            laserDecisionTimes = decisionTimes[trialsEachLaser[:, 1]]
            laserDecisionTimes = laserDecisionTimes[np.isfinite(laserDecisionTimes)]
            thisLaserDecision[indMouse, indBand] = np.mean(laserDecisionTimes)

            if thisControlDecision is None:
                thisControlDecision = np.zeros((len(PV_CHR2_MICE), len(BANDS_TO_USE)))
            controlDecisionTimes = decisionTimes[trialsEachLaser[:,0]]
            controlDecisionTimes = controlDecisionTimes[np.isfinite(controlDecisionTimes)]
            thisControlDecision[indMouse, indBand] = np.mean(controlDecisionTimes)

    laserReaction.append(thisLaserReaction)
    controlReaction.append(thisControlReaction)
    laserDecision.append(thisLaserDecision)
    controlDecision.append(thisControlDecision)

# -- save all reaction and decision times by bandwidth --
outputFile = 'all_reaction_times_ac_inactivation.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         expLaserReaction=laserReaction[0], expNoLaserReaction=controlReaction[0],
         expLaserDecision=laserDecision[0], expNoLaserDecision=controlDecision[0],
         controlLaserReaction=laserReaction[1], controlNoLaserReaction=controlReaction[1],
         controlLaserDecision=laserDecision[1], controlNoLaserDecision=controlDecision[1],
         possibleBands=numBands[BANDS_TO_USE])
print(outputFile + " saved")
