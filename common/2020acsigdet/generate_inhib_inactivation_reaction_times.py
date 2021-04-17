import os
import numpy as np
import pandas as pd

from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import behaviour_analysis_funcs as funcs
import studyparams

figName = 'figure_inhibitory_inactivation_reaction_times'
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
sessionTypes = ['laser', 'control']

reactionTimes = []
decisionTimes = []

reactionTimesAllBand = []
decisionTimesAllBand = []

for indCellType, mice in enumerate(mouseType):
    thisReactionTimes = None
    thisDecisionTimes = None

    thisReactionTimesAllBand = None
    thisDecisionTimesAllBand = None

    for indMouse, mouse in enumerate(mice):
        for indSesType, sessionType in enumerate(sessionTypes):

            sessionTypeName = f'10mW {sessionType}'

            dbRow = sessionDB.query('mouse==@mouse and sessionType==@sessionTypeName')
            laserSessions = dbRow['goodSessions'].apply(eval).iloc[-1]
            laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

            mouseReactionTimes, mouseDecisionTimes = funcs.get_reaction_times(mouse, laserSessions)

            numLasers = np.unique(laserBehavData['laserSide'])
            numBands = np.unique(laserBehavData['currentBand'])

            trialsEachCond = behavioranalysis.find_trials_each_combination(laserBehavData['laserSide'], numLasers,
                                                                           laserBehavData['currentBand'], numBands)
            trialsEachLaser = behavioranalysis.find_trials_each_type(laserBehavData['laserSide'], numLasers)

            # -- compute reaction and decision times for each bandwidth and laser presentation --
            for indBand in range(len(numBands)):
                for indLaser in range(len(numLasers)):
                    trialsThisCond = trialsEachCond[:, indLaser, indBand]

                    if thisReactionTimes is None:
                        thisReactionTimes = np.zeros((len(sessionTypes), len(mice), len(numBands), len(numLasers)))
                        thisDecisionTimes = np.zeros_like(thisReactionTimes)

                    laserReactionTimes = mouseReactionTimes[trialsThisCond]
                    laserReactionTimes = laserReactionTimes[np.isfinite(laserReactionTimes)]
                    thisReactionTimes[indSesType, indMouse, indBand, indLaser] = np.median(laserReactionTimes)

                    laserDecisionTimes = mouseDecisionTimes[trialsThisCond]
                    laserDecisionTimes = laserDecisionTimes[np.isfinite(laserDecisionTimes)]
                    thisDecisionTimes[indSesType, indMouse, indBand, indLaser] = np.median(laserDecisionTimes)

            # -- also do it without splitting by bandwidth --
            for indLaser in range(len(numLasers)):
                trialsThisCond = trialsEachLaser[:, indLaser]

                if thisReactionTimesAllBand is None:
                    thisReactionTimesAllBand = np.zeros((len(sessionTypes), len(mice), len(numLasers)))
                    thisDecisionTimesAllBand = np.zeros_like(thisReactionTimesAllBand)

                laserReactionTimes = mouseReactionTimes[trialsThisCond]
                laserReactionTimes = laserReactionTimes[np.isfinite(laserReactionTimes)]
                thisReactionTimesAllBand[indSesType, indMouse, indLaser] = np.median(laserReactionTimes)

                laserDecisionTimes = mouseDecisionTimes[trialsThisCond]
                laserDecisionTimes = laserDecisionTimes[np.isfinite(laserDecisionTimes)]
                thisDecisionTimesAllBand[indSesType, indMouse, indLaser] = np.median(laserDecisionTimes)

    reactionTimes.append(thisReactionTimes)
    decisionTimes.append(thisDecisionTimes)

    reactionTimesAllBand.append(thisReactionTimesAllBand)
    decisionTimesAllBand.append(thisDecisionTimesAllBand)


# -- save responses of all sound responsive cells to 0.25 bandwidth sounds --
outputFile = 'all_reaction_times_inhib_inactivation.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         PVexpLaserReaction=reactionTimes[0][0,:,:,1], PVexpNoLaserReaction=reactionTimes[0][0,:,:,0],
         PVcontrolLaserReaction=reactionTimes[0][1,:,:,1], PVcontrolNoLaserReaction=reactionTimes[0][1,:,:,0],
         PVexpLaserDecision=decisionTimes[0][0,:,:,1], PVexpNoLaserDecision=decisionTimes[0][0,:,:,0],
         PVcontrolLaserDecision=decisionTimes[0][1,:,:,1], PVcontrolNoLaserDecision=decisionTimes[0][1,:,:,0],

         SOMexpLaserReaction=reactionTimes[1][0,:,:,1], SOMexpNoLaserReaction=reactionTimes[1][0,:,:,0],
         SOMcontrolLaserReaction=reactionTimes[1][1,:,:,1], SOMcontrolNoLaserReaction=reactionTimes[1][1,:,:,0],
         SOMexpLaserDecision=decisionTimes[1][0,:,:,1], SOMexpNoLaserDecision=decisionTimes[1][0,:,:,0],
         SOMcontrolLaserDecision=decisionTimes[1][1,:,:,1], SOMcontrolNoLaserDecision=decisionTimes[1][1,:,:,0],

         PVexpLaserReactionAllBand=reactionTimesAllBand[0][0,:,1], PVexpNoLaserReactionAllBand=reactionTimesAllBand[0][0,:,0],
         PVcontrolLaserReactionAllBand=reactionTimesAllBand[0][1,:,1], PVcontrolNoLaserReactionAllBand=reactionTimesAllBand[0][1,:,0],
         PVexpLaserDecisionAllBand=decisionTimesAllBand[0][0,:,1], PVexpNoLaserDecisionAllBand=decisionTimesAllBand[0][0,:,0],
         PVcontrolLaserDecisionAllBand=decisionTimesAllBand[0][1,:,1], PVcontrolNoLaserDecisionAllBand=decisionTimesAllBand[0][1,:,0],

         SOMexpLaserReactionAllBand=reactionTimesAllBand[1][0,:,1], SOMexpNoLaserReactionAllBand=reactionTimesAllBand[1][0,:,0],
         SOMcontrolLaserReactionAllBand=reactionTimesAllBand[1][1,:,1], SOMcontrolNoLaserReactionAllBand=reactionTimesAllBand[1][1,:,0],
         SOMexpLaserDecisionAllBand=decisionTimesAllBand[1][0,:,1], SOMexpNoLaserDecisionAllBand=decisionTimesAllBand[1][0,:,0],
         SOMcontrolLaserDecisionAllBand=decisionTimesAllBand[1][1,:,1], SOMcontrolNoLaserDecisionAllBand=decisionTimesAllBand[1][1,:,0],
         possibleBands=numBands)
print(outputFile + " saved")
