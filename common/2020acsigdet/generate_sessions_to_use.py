import os
import numpy as np
import pandas as pd
from scipy import stats

from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import behaviour_analysis_funcs as funcs
import studyparams

figName = 'figure_inhibitory_inactivation'
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

SOM_ARCHT_MICE = studyparams.SOM_ARCHT_MICE
PV_ARCHT_MICE = studyparams.PV_ARCHT_MICE
PV_CHR2_MICE = studyparams.PV_CHR2_MICE
mouseType = [PV_ARCHT_MICE, SOM_ARCHT_MICE, PV_CHR2_MICE]
mouseTypeLabels = ['PVArchT', 'SOMArchT', 'PVChR2']
trialType = ['laser', 'control']
laserPower = ['10mW', '10mW', '3mW']

sessiondb = pd.DataFrame(dtype=object)
mousedb = pd.DataFrame(dtype=object)

for indCell, mice in enumerate(mouseType):
    miceToRemove = []
    for indMouse, mouse in enumerate(mice):
        for indType, type in enumerate(trialType):
            trialName = f'{laserPower[indCell]} {type}'
            sessions = studyparams.miceDict[mouse][trialName]
            sessionsToUse = None
            sessionsExcluded = 0
            for indSession, session in enumerate(sessions):
                if indSession == 0:
                    sessionsToUse = []

                behavData = behavioranalysis.load_many_sessions(mouse, [session])

                numLasers = np.unique(behavData['laserSide'])
                numBands = np.unique(behavData['currentBand'])

                trialsEachLaser = behavioranalysis.find_trials_each_type(behavData['laserSide'], numLasers)
                incorrect = behavData['outcome'] == behavData.labels['outcome']['error']
                correct = behavData['outcome'] == behavData.labels['outcome']['correct']

                controlIncorrect = incorrect[trialsEachLaser[:,0]]
                controlCorrect = correct[trialsEachLaser[:,0]]

                accuracy = np.sum(controlCorrect) / (np.sum(controlCorrect) + np.sum(controlIncorrect))

                # record which sessions have >60% accuracy
                if accuracy > 0.6:
                    sessionsToUse.append(session)
                else:
                    sessionsExcluded += 1

            entryDict = {'mouse': mouse,
                         'sessionType': trialName,
                         'goodSessions': sessionsToUse}
            sessiondb = sessiondb.append(entryDict, ignore_index=True)
            print(f'{mouse} {trialName}: {sessionsExcluded} sessions excluded')

            # don't include mice with very few good experimental sessions
            if len(sessionsToUse) < 3 and indType==0:
                miceToRemove.append(mouse)

    mice = [mouse for mouse in mice if mouse not in miceToRemove]
    entryDict = {'strain': mouseTypeLabels[indCell],
                 'mice': mice}
    mousedb = mousedb.append(entryDict, ignore_index=True)

dbName = 'good_sessions.csv'
# dataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
dataPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
sessiondb.to_csv(dataPath)

dbName = 'good_mice.csv'
# dataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
dataPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
mousedb.to_csv(dataPath)

