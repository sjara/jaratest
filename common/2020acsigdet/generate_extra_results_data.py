import os
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import settings

import studyparams
import behaviour_analysis_funcs as funcs

# --- laser-induced change in behavior by SNR in PV::ChR2 mice ---
dbName = 'good_sessions.csv'
dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
sessionDB = pd.read_csv(dbPath)

dbName = 'good_mice.csv'
dataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
# dataPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
mouseDB = pd.read_csv(dataPath)

mouseRow = mouseDB.query('strain=="PVChR2"')
PV_CHR2_MICE = mouseRow['mice'].apply(eval).iloc[-1]

psyCurves = None
for indMouse, mouse in enumerate(PV_CHR2_MICE):
    sessionTypeName = '3mW laser'
    dbRow = sessionDB.query('mouse==@mouse and sessionType==@sessionTypeName')
    laserSessions = dbRow['goodSessions'].apply(eval).iloc[-1]
    laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

    correct, incorrect, toneChoice, noiseChoice, trialsEachCond3Params, labels = funcs.get_trials(laserBehavData)

    numLasers = np.unique(laserBehavData['laserSide'])
    numSNRs = np.unique(laserBehavData['currentSNR'])

    trialsEachCond = behavioranalysis.find_trials_each_combination(laserBehavData['laserSide'], numLasers,
                                                                   laserBehavData['currentSNR'], numSNRs)

    if psyCurves is None:
        psyCurves = np.zeros((len(PV_CHR2_MICE), len(numLasers), len(numSNRs)))

    for laser in range(len(numLasers)):
        for snr in range(len(numSNRs)):
            toneChoiceThisCond = toneChoice[trialsEachCond[:, laser, snr]]
            noiseChoiceThisCond = noiseChoice[trialsEachCond[:, laser, snr]]
            psyCurves[indMouse, laser, snr] = 100.0 * np.sum(toneChoiceThisCond) / (np.sum(toneChoiceThisCond) + np.sum(noiseChoiceThisCond))

laserDiff = np.diff(psyCurves, axis=1)
laserDiffLowSNR = laserDiff[:,:,1].flatten()
laserDiffHighSNR = laserDiff[:,:,-1].flatten()
pVal = stats.wilcoxon(laserDiffLowSNR, laserDiffHighSNR)
print(f'Median low SNR change: {np.median(laserDiffLowSNR)} \nMedian high SNR change: {np.median(laserDiffHighSNR)} \npVal = {pVal[1]}')

laserDiffPercent = 1 - (psyCurves[:,1,:]/psyCurves[:,0,:])
laserDiffPercentLowSNR = 100*laserDiffPercent[:,1].flatten()
laserDiffPercentHighSNR = 100*laserDiffPercent[:,-1].flatten()
pVal = stats.wilcoxon(laserDiffPercentLowSNR, laserDiffPercentHighSNR)
print(f'Median low SNR percent change: {np.median(laserDiffPercentLowSNR)} \nMedian high SNR percent change: {np.median(laserDiffPercentHighSNR)} \npVal = {pVal[1]}')


# --- determine length of time of behavioural shaping ---
mouseDicts = [studyparams.unimplanted_PVCHR2, studyparams.unimplanted_PVARCHT, studyparams.unimplanted_SOMARCHT,
              studyparams.unimplanted_PVCRE, studyparams.unimplanted_SOMCRE]

mouseList = []
for miceThisType in mouseDicts:
    mouseList.extend(miceThisType.keys())

FIGNAME = 'figure_characterise_behaviour'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)
fileName = 'unimplanted_behaviour_v2.npz'
dataFullPath = os.path.join(dataDir, fileName)
data = np.load(dataFullPath)

accuracies = data['allPercentCorrect']

indsToIgnore = []
for indAcc in range(accuracies.shape[0]):
    if not all(accuracies[indAcc,:] > 60):
        indsToIgnore.append(indAcc)

mouseList = np.delete(mouseList, indsToIgnore)
daysToLearn = np.zeros(len(mouseList))
daysToFinalTask = np.zeros(len(mouseList))

for indMouse, mouse in enumerate(mouseList):
    mouseDir = os.path.join(settings.BEHAVIOR_PATH, mouse)
    sessionFileNames = os.listdir(mouseDir)
    sessionFileNames = sorted(sessionFileNames) # put the files in alphabetical order!!!

    # find first session where sound stops on withdrawal (learned to differentiate signal vs. no signal)
    for indSession, session in enumerate(sessionFileNames):
        behavFile = os.path.join(settings.BEHAVIOR_PATH, mouse, session)
        bdata = loadbehavior.BehaviorData(behavFile)

        soundMode = np.unique(bdata['soundMode'])
        offOnWithdrawal = bdata.labels['soundMode']['off_on_withdrawal']
        if soundMode == offOnWithdrawal:
            daysToLearn[indMouse] = indSession
            break

    # find first session where there are multiple SNRs (reached final stage of task)
    for indSession, session in enumerate(sessionFileNames):
        behavFile = os.path.join(settings.BEHAVIOR_PATH, mouse, session)
        bdata = loadbehavior.BehaviorData(behavFile)

        SNRs = np.unique(bdata['currentSNR'])
        if len(SNRs)>2:
            daysToFinalTask[indMouse] = indSession
            break
    #break

print(f'Median days to learn basic task: {np.median(daysToLearn)}\nMedian days to final task: {np.median(daysToFinalTask)}')

bins = np.arange(10, 45)
plt.hist(daysToLearn, bins)
plt.xlabel('Days to learn basic task')

bins = np.arange(30, 70)
plt.hist(daysToFinalTask, bins)
plt.xlabel('Days to reach final task')

plt.show()