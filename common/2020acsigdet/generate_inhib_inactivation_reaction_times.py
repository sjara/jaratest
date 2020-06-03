import os
import numpy as np

from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import studyparams

figName = 'figure_inhibitory_inactivation_reaction_times'
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

SOM_ARCHT_MICE = studyparams.SOM_ARCHT_MICE
PV_ARCHT_MICE = studyparams.PV_ARCHT_MICE
mouseType = [PV_ARCHT_MICE, SOM_ARCHT_MICE]

laserReaction = []
controlReaction = []

laserDecision = []
controlDecision = []

for indType, mice in enumerate(mouseType):

    thisLaserReaction = None
    thisControlReaction = None

    thisLaserDecision = None
    thisControlDecision = None

    for indMouse, mouse in enumerate(mice):

        laserSessions = studyparams.miceDict[mouse]['10mW laser']
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

        for indBand in range(len(numBands)):
            trialsEachLaser = trialsEachCond[:, :, indBand]

            # -- sort trials by laser presentation, compute reaction times as time diff between sound on and center out --
            if thisLaserReaction is None:
                thisLaserReaction = np.zeros((len(mice), len(numBands)))
            laserReactionTimes = reactionTimes[trialsEachLaser[:,1]]
            laserReactionTimes = laserReactionTimes[np.isfinite(laserReactionTimes)]
            thisLaserReaction[indMouse, indBand] = np.mean(laserReactionTimes)

            if thisControlReaction is None:
                thisControlReaction = np.zeros((len(mice), len(numBands)))
            controlReactionTimes = reactionTimes[trialsEachLaser[:, 0]]
            controlReactionTimes = controlReactionTimes[np.isfinite(controlReactionTimes)]
            thisControlReaction[indMouse, indBand] = np.mean(controlReactionTimes)

            # -- compute decision time as time diff between center out and side in --
            if thisLaserDecision is None:
                thisLaserDecision = np.zeros((len(mice), len(numBands)))
            laserDecisionTimes = decisionTimes[trialsEachLaser[:, 1]]
            laserDecisionTimes = laserDecisionTimes[np.isfinite(laserDecisionTimes)]
            thisLaserDecision[indMouse, indBand] = np.mean(laserDecisionTimes)

            if thisControlDecision is None:
                thisControlDecision = np.zeros((len(mice), len(numBands)))
            controlDecisionTimes = decisionTimes[trialsEachLaser[:,0]]
            controlDecisionTimes = controlDecisionTimes[np.isfinite(controlDecisionTimes)]
            thisControlDecision[indMouse, indBand] = np.mean(controlDecisionTimes)

    laserReaction.append(thisLaserReaction)
    controlReaction.append(thisControlReaction)

    laserDecision.append(thisLaserDecision)
    controlDecision.append(thisControlDecision)

# -- save responses of all sound responsive cells to 0.25 bandwidth sounds --
outputFile = 'all_reaction_times_inhib_inactivation.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         PVlaserReaction=laserReaction[0], PVcontrolReaction=controlReaction[0],
         PVlaserDecision=laserDecision[0], PVcontrolDecision=controlDecision[0],
         SOMlaserReaction=laserReaction[1], SOMcontrolReaction=controlReaction[1],
         SOMlaserDecision=laserDecision[1], SOMcontrolDecision=controlDecision[1],
         possibleBands=numBands)
print(outputFile + " saved")
