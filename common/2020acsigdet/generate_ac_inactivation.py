import os
import numpy as np
import pandas as pd
from scipy import stats

from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import behaviour_analysis_funcs as funcs
import studyparams

figName = 'figure_ac_inactivation'
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

dbName = 'good_sessions.csv'
# dataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
dbPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
sessionDB = pd.read_csv(dbPath)

dbName = 'good_mice.csv'
# dataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
dataPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
mouseDB = pd.read_csv(dataPath)

mouseRow = mouseDB.query('strain=="PVChR2"')
PV_CHR2_MICE = mouseRow['mice'].apply(eval).iloc[-1]

BANDS_TO_USE = [0,-1] #ignore intermetiate bandwidth for the mice it was done for
arrayDims = (2, len(PV_CHR2_MICE), len(BANDS_TO_USE), 2) # sort by: laser in/out, mouse, bandwidth, laser off/on
arayDimsAllBands = (2, len(PV_CHR2_MICE), 2)

sessionType = ['laser', 'control']

accuracy = np.zeros(arrayDims)
bias = np.zeros(arrayDims)
hits = np.zeros(arrayDims)
FAs = np.zeros(arrayDims)
dprime = np.zeros(arrayDims)

accuracyAllBand = np.zeros(arayDimsAllBands)
biasAllBand = np.zeros(arayDimsAllBands)
hitsAllBand = np.zeros(arayDimsAllBands)
FAallBand = np.zeros(arayDimsAllBands)
dprimeAllBand = np.zeros(arayDimsAllBands)

for indMouse, mouse in enumerate(PV_CHR2_MICE):
    for indSesType, sesType in enumerate(sessionType):
        sessionTypeName = f'3mW {sesType}'
        print(mouse, sessionTypeName)

        dbRow = sessionDB.query('mouse==@mouse and sessionType==@sessionTypeName')
        laserSessions = dbRow['goodSessions'].apply(eval).iloc[-1]
        print(laserSessions)

        laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

        correct, incorrect, toneChoice, noiseChoice, trialsEachCond3Params, labels = funcs.get_trials(laserBehavData)

        numLasers = np.unique(laserBehavData['laserSide'])
        numBands = np.unique(laserBehavData['currentBand'])

        trialsEachLaser = behavioranalysis.find_trials_each_type(laserBehavData['laserSide'], numLasers)
        trialsEachCond = behavioranalysis.find_trials_each_combination(laserBehavData['laserSide'], numLasers,
                                                                       laserBehavData['currentBand'], numBands)

        # -- compute accuracies and bias for each bandwidth --
        for indBand in BANDS_TO_USE:
            for indLaser in range(len(numLasers)):
                trialsThisCond = trialsEachCond[:, indLaser, indBand]

                # -- compute accuracy as percent correct trials out of all valid trials --
                thisIncorrect = incorrect[trialsThisCond]
                thisCorrect = correct[trialsThisCond]

                accuracy[indSesType, indMouse, indBand, indLaser] = 100.0 * np.sum(thisCorrect) / (np.sum(thisCorrect) + np.sum(thisIncorrect))

                # -- compute bias to a side as difference/sum --
                thisToneChoice = toneChoice[trialsThisCond]
                thisNoiseChoice = noiseChoice[trialsThisCond]

                bias[indSesType, indMouse, indBand, indLaser] = 1.0 * (np.sum(thisToneChoice) - np.sum(thisNoiseChoice)) / (np.sum(thisToneChoice) + np.sum(thisNoiseChoice))

                # -- compute hits, FAs, and d prime --
                toneTrials = np.sum(thisCorrect & thisToneChoice) + np.sum(thisIncorrect & thisNoiseChoice)
                noiseTrials = np.sum(thisCorrect & thisNoiseChoice) + np.sum(thisIncorrect & thisToneChoice)

                thisHitRate = np.sum(thisCorrect & thisToneChoice) / toneTrials
                thisFARate = np.sum(thisIncorrect & thisToneChoice) / noiseTrials

                hits[indSesType, indMouse, indBand, indLaser] = 100.0 * thisHitRate
                FAs[indSesType, indMouse, indBand, indLaser] = 100.0 * thisFARate
                dprime[indSesType, indMouse, indBand, indLaser] = (stats.norm.ppf(thisHitRate) - stats.norm.ppf(thisFARate))

        # -- also compute this stuff without splitting by band --
        for indLaser in range(len(numLasers)):
            trialsThisCond = trialsEachLaser[:, indLaser]

            # -- compute accuracy as percent correct trials out of all valid trials --
            thisIncorrect = incorrect[trialsThisCond]
            thisCorrect = correct[trialsThisCond]

            accuracyAllBand[indSesType, indMouse, indLaser] = 100.0 * np.sum(thisCorrect) / (np.sum(thisCorrect) + np.sum(thisIncorrect))

            # -- compute bias to a side as difference/sum --
            thisToneChoice = toneChoice[trialsThisCond]
            thisNoiseChoice = noiseChoice[trialsThisCond]

            biasAllBand[indSesType, indMouse, indLaser] = 1.0 * (np.sum(thisToneChoice) - np.sum(thisNoiseChoice)) / (
                        np.sum(thisToneChoice) + np.sum(thisNoiseChoice))

            # -- compute hits, FAs, and d prime --
            toneTrials = np.sum(thisCorrect & thisToneChoice) + np.sum(thisIncorrect & thisNoiseChoice)
            noiseTrials = np.sum(thisCorrect & thisNoiseChoice) + np.sum(thisIncorrect & thisToneChoice)

            thisHitRate = np.sum(thisCorrect & thisToneChoice) / toneTrials
            thisFARate = np.sum(thisIncorrect & thisToneChoice) / noiseTrials

            hitsAllBand[indSesType, indMouse, indLaser] = 100.0 * thisHitRate
            FAallBand[indSesType, indMouse, indLaser] = 100.0 * thisFARate
            dprimeAllBand[indSesType, indMouse, indLaser] = (stats.norm.ppf(thisHitRate) - stats.norm.ppf(thisFARate))

# -- save data --
outputFile = 'all_behaviour_ac_inactivation_v2.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         expLaserAccuracy=accuracy[0,:,:,1], expNoLaserAccuracy=accuracy[0,:,:,0],
         controlLaserAccuracy=accuracy[1,:,:,1], controlNoLaserAccuracy=accuracy[1,:,:,0],
         expLaserBias=bias[0,:,:,1], expNoLaserBias=bias[0,:,:,0],
         controlLaserBias=bias[1,:,:,1], controlNoLaserBias=bias[1,:,:,0],

         expLaserHits=hits[0,:,:,1], expNoLaserHits=hits[0,:,:,0],
         controlLaserHits=hits[1,:,:,1], controlNoLaserHits=hits[1,:,:,0],
         expLaserFA=FAs[0,:,:,1], expNoLaserFA=FAs[0,:,:,0],
         controlLaserFA=FAs[1,:,:,1], controlNoLaserFA=FAs[1,:,:,0],
         expLaserdprime=dprime[0,:,:,1], expNoLaserdprime=dprime[0,:,:,0],
         controlLaserdprime=dprime[1,:,:,1], controlNoLaserdprime=dprime[1,:,:,0],

         expLaserAccuracyAllBands=accuracyAllBand[0, :, 1], expNoLaserAccuracyAllBands=accuracyAllBand[0, :, 0],
         controlLaserAccuracyAllBands=accuracyAllBand[1, :, 1], controlNoLaserAccuracyAllBands=accuracyAllBand[1, :, 0],
         expLaserBiasAllBands=biasAllBand[0, :, 1], expNoLaserBiasAllBands=biasAllBand[0, :, 0],
         controlLaserBiasAllBands=biasAllBand[1, :, 1], controlNoLaserBiasAllBands=biasAllBand[1, :, 0],

         expLaserHitsAllBands=hitsAllBand[0, :, 1], expNoLaserHitsAllBands=hitsAllBand[0, :, 0],
         controlLaserHitsAllBands=hitsAllBand[1, :, 1], controlNoLaserHitsAllBands=hitsAllBand[1, :, 0],
         expLaserFAallBands=FAallBand[0, :, 1], expNoLaserFAallBands=FAallBand[0, :, 0],
         controlLaserFAallBands=FAallBand[1, :, 1], controlNoLaserFAallBands=FAallBand[1, :, 0],
         expLaserdprimeAllBands=dprimeAllBand[0, :, 1], expNoLaserdprimeAllBandsAllBand=dprimeAllBand[0, :, 0],
         controlLaserdprimeAllBands=dprimeAllBand[1, :, 1], controlNoLaserdprimeAllBands=dprimeAllBand[1, :, 0],
         possibleBands=numBands[BANDS_TO_USE])
print(outputFile + " saved")