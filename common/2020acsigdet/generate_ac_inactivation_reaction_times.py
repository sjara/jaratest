import os
import numpy as np
import pandas as pd

from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import behaviour_analysis_funcs as funcs
import studyparams

figName = 'figure_ac_inactivation'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

dbName = 'good_sessions.csv'
dataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
sessionDB = pd.read_csv(dbPath)

dbName = 'good_mice.csv'
dataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
mouseDB = pd.read_csv(dbPath)

mouseRow = mouseDB.query('strain=="PVChR2"')
PV_CHR2_MICE = mouseRow['mice'].apply(eval).iloc[-1]
sessionTypes = ['laser', 'control']
BANDS_TO_USE = [0, -1] # just use the first and last bandwidths for sessions that had more than 2

reactionTimes = None
decisionTimes = None

reactionTimesAllBand = None
decisionTimesAllBand = None


for indMouse, mouse in enumerate(PV_CHR2_MICE):
    for indSesType, sessionType in enumerate(sessionTypes):

        sessionTypeName = f'3mW {sessionType}'

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
        for indBand in BANDS_TO_USE:
            for indLaser in range(len(numLasers)):
                trialsThisCond = trialsEachCond[:, indLaser, indBand]

                if reactionTimes is None:
                    reactionTimes = np.zeros((len(sessionTypes), len(PV_CHR2_MICE), len(BANDS_TO_USE), len(numLasers)))
                    decisionTimes = np.zeros_like(reactionTimes)

                laserReactionTimes = mouseReactionTimes[trialsThisCond]
                laserReactionTimes = laserReactionTimes[np.isfinite(laserReactionTimes)]
                reactionTimes[indSesType, indMouse, indBand, indLaser] = np.median(laserReactionTimes)

                laserDecisionTimes = mouseDecisionTimes[trialsThisCond]
                laserDecisionTimes = laserDecisionTimes[np.isfinite(laserDecisionTimes)]
                decisionTimes[indSesType, indMouse, indBand, indLaser] = np.median(laserDecisionTimes)

        # -- also do it without splitting by bandwidth --
        for indLaser in range(len(numLasers)):
            trialsThisCond = trialsEachLaser[:, indLaser]

            if reactionTimesAllBand is None:
                reactionTimesAllBand = np.zeros((len(sessionTypes), len(PV_CHR2_MICE), len(numLasers)))
                decisionTimesAllBand = np.zeros_like(reactionTimesAllBand)

            laserReactionTimes = mouseReactionTimes[trialsThisCond]
            laserReactionTimes = laserReactionTimes[np.isfinite(laserReactionTimes)]
            reactionTimesAllBand[indSesType, indMouse, indLaser] = np.median(laserReactionTimes)

            laserDecisionTimes = mouseDecisionTimes[trialsThisCond]
            laserDecisionTimes = laserDecisionTimes[np.isfinite(laserDecisionTimes)]
            decisionTimesAllBand[indSesType, indMouse, indLaser] = np.median(laserDecisionTimes)

# -- save all reaction and decision times by bandwidth --
outputFile = 'all_reaction_times_ac_inactivation.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         expLaserReaction=reactionTimes[0,:,:,1], expNoLaserReaction=reactionTimes[0,:,:,0],
         controlLaserReaction=reactionTimes[1,:,:,1], controlNoLaserReaction=reactionTimes[1,:,:,0],
         expLaserDecision=decisionTimes[0,:,:,1], expNoLaserDecision=decisionTimes[0,:,:,0],
         controlLaserDecision=decisionTimes[1,:,:,1], controlNoLaserDecision=decisionTimes[1,:,:,0],

         expLaserReactionAllBand=reactionTimesAllBand[0,:,1], expNoLaserReactionAllBand=reactionTimesAllBand[0,:,0],
         controlLaserReactionAllBand=reactionTimesAllBand[1,:,1], controlNoLaserReactionAllBand=reactionTimesAllBand[1,:,0],
         expLaserDecisionAllBand=decisionTimesAllBand[0,:,1], expNoLaserDecisionAllBand=decisionTimesAllBand[0,:,0],
         controlLaserDecisionAllBand=decisionTimesAllBand[1,:,1], controlNoLaserDecisionAllBand=decisionTimesAllBand[1,:,0],
         possibleBands=numBands[BANDS_TO_USE])
print(outputFile + " saved")
