import os
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import behaviour_analysis_funcs as funcs
import studyparams

figName = 'figure_inhibitory_inactivation'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

dbName = 'good_sessions.csv'
dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
sessionDB = pd.read_csv(dbPath)

dbName = 'good_mice.csv'
dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, dbName)
mouseDB = pd.read_csv(dbPath)

mouseRow = mouseDB.query('strain=="PVArchT"')
PV_ARCHT_MICE = mouseRow['mice'].apply(eval).iloc[-1]
mouseRow = mouseDB.query('strain=="SOMArchT"')
SOM_ARCHT_MICE = mouseRow['mice'].apply(eval).iloc[-1]
mouseType = [PV_ARCHT_MICE, SOM_ARCHT_MICE]
sessionType = ['laser', 'control']

REACTION_TIME_CUTOFF = studyparams.REACTION_TIME_CUTOFF

accuracy = []
bias = []
hits = []
FAs = []
dprime = []
pVals = []
fractionNoChoice = []

accuracyAllBand = []
biasAllBand = []
hitsAllBand = []
FAallBand = []
dprimeAllBand = []
pValsAllBand = []

dprimeEachSession = [ len(PV_ARCHT_MICE)*[[]], len(SOM_ARCHT_MICE)*[[]] ]
eachSessionLabels = [sessionType, ['none','bilateral']]  # WARNING! this is hardcoded

for indCell, mice in enumerate(mouseType):

    thisAccuracy = None
    thisBias = None
    thisHits = None
    thisFAs = None
    thisdprime = None
    thispVals = None
    thisFractionNoChoice = None

    thisAccuracyAllBand = None
    thisBiasAllBand = None
    thisHitsAllBand = None
    thisFAsAllBand = None
    thisdprimeAllBand = None
    thispValsAllBand = None

    for indMouse, mouse in enumerate(mice):
        dprimeEachSession[indCell][indMouse] = len(sessionType)*[[]] # List of session types

        # contingency tables used for comparing laser in to laser out sessions
        conTableAllBands = np.zeros((2, 2, 2))  # laser off/on, tone/noise choice, exp/control session
        conTable = None  # laser off/on, tone/noise choice, exp/control session

        for indType, sesType in enumerate(sessionType):
            sessionTypeName = f'10mW {sesType}'
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

            reactionTimes, decisionTimes = funcs.get_reaction_times(mouse, laserSessions)
            trialsToUse = reactionTimes>=REACTION_TIME_CUTOFF

            if thisAccuracy is None:
                arrayDims = (2, len(mice), len(numBands), 2)  # sort by: laser in/out, mouse, bandwidth, laser off/on
                arrayDimsAllBands = (2, len(mice), 2)

                thisAccuracy = np.zeros(arrayDims)
                thisBias = np.zeros(arrayDims)
                thisHits = np.zeros(arrayDims)
                thisFAs = np.zeros(arrayDims)
                thisdprime = np.zeros(arrayDims)
                thispVals = np.zeros((len(mice), len(numBands), 3)) # by mouse, bandwidth, (in/out, in, out)
                thisFractionNoChoice = np.zeros((2, len(mice), 2)) # sort by: laser in/out, mouse, laser off/on

                thisAccuracyAllBand = np.zeros(arrayDimsAllBands)
                thisBiasAllBand = np.zeros(arrayDimsAllBands)
                thisHitsAllBand = np.zeros(arrayDimsAllBands)
                thisFAsAllBand = np.zeros(arrayDimsAllBands)
                thisdprimeAllBand = np.zeros(arrayDimsAllBands)
                thispValsAllBand = np.zeros((len(mice), 3))

            if conTable is None:
                conTable = np.zeros((2, 2, 2, len(numBands)))

            # -- compute accuracies,bias,hits,FA,d prime for each bandwidth --
            for indBand in range(len(numBands)):
                for indLaser in range(len(numLasers)):
                    trialsThisCond = trialsEachCond[:, indLaser, indBand]

                    # -- compute accuracy as percent correct trials out of all valid trials --
                    thisCorrect = correct[trialsThisCond & trialsToUse]
                    thisIncorrect = incorrect[trialsThisCond & trialsToUse]

                    thisAccuracy[indType, indMouse, indBand, indLaser] = 100.0 * np.sum(thisCorrect) / (np.sum(thisCorrect) + np.sum(thisIncorrect))

                    # -- compute bias to a side as difference/sum --
                    thisToneChoice = toneChoice[trialsThisCond & trialsToUse]
                    thisNoiseChoice = noiseChoice[trialsThisCond & trialsToUse]
                    thisBias[indType, indMouse, indBand, indLaser] = 1.0 * (np.sum(thisToneChoice) - np.sum(thisNoiseChoice)) / \
                                                       (np.sum(thisToneChoice) + np.sum(thisNoiseChoice))

                    # -- compute hit rate, FA rate, and d prime --
                    toneTrials = np.sum(thisCorrect & thisToneChoice) + np.sum(thisIncorrect & thisNoiseChoice)
                    noiseTrials = np.sum(thisCorrect & thisNoiseChoice) + np.sum(thisIncorrect & thisToneChoice)

                    thisHitRate = np.sum(thisCorrect & thisToneChoice) / toneTrials
                    thisFARate = np.sum(thisIncorrect & thisToneChoice) / noiseTrials

                    thisHits[indType, indMouse, indBand, indLaser] = 100.0 * thisHitRate
                    thisFAs[indType, indMouse, indBand, indLaser] = 100.0 * thisFARate
                    thisdprime[indType, indMouse, indBand, indLaser] = stats.norm.ppf(thisHitRate) - stats.norm.ppf(thisFARate)

                    # -- compute laser effect pVals for each mouse and also contringency table for later --
                    conTable[indLaser, 0, indType, indBand] = np.sum(thisToneChoice)
                    conTable[indLaser, 1, indType, indBand] = np.sum(thisNoiseChoice)

                thispVals[indMouse, indBand, indType] = stats.fisher_exact(conTable[:,:,indType,indBand])[1]

            # -- also do this computations without splitting by band --
            for indLaser in range(len(numLasers)):
                trialsThisCond = trialsEachLaser[:, indLaser]

                # -- compute accuracy as percent correct trials out of all valid trials --
                thisCorrect = correct[trialsThisCond & trialsToUse]
                thisIncorrect = incorrect[trialsThisCond & trialsToUse]

                thisAccuracyAllBand[indType, indMouse, indLaser] = 100.0 * np.sum(thisCorrect) / (np.sum(thisCorrect) + np.sum(thisIncorrect))

                # -- compute bias to a side as difference/sum --
                thisToneChoice = toneChoice[trialsThisCond & trialsToUse]
                thisNoiseChoice = noiseChoice[trialsThisCond & trialsToUse]
                thisBiasAllBand[indType, indMouse, indLaser] = 1.0 * (np.sum(thisToneChoice) - np.sum(thisNoiseChoice)) / \
                                                                 (np.sum(thisToneChoice) + np.sum(thisNoiseChoice))

                # -- compute hit rate, FA rate, and d prime --
                toneTrials = np.sum(thisCorrect & thisToneChoice) + np.sum(thisIncorrect & thisNoiseChoice)
                noiseTrials = np.sum(thisCorrect & thisNoiseChoice) + np.sum(thisIncorrect & thisToneChoice)

                thisHitRate = np.sum(thisCorrect & thisToneChoice) / toneTrials
                thisFARate = np.sum(thisIncorrect & thisToneChoice) / noiseTrials

                thisHitsAllBand[indType, indMouse, indLaser] = 100.0 * thisHitRate
                thisFAsAllBand[indType, indMouse, indLaser] = 100.0 * thisFARate
                thisdprimeAllBand[indType, indMouse, indLaser] = stats.norm.ppf(thisHitRate) - stats.norm.ppf(thisFARate)

                # -- compute laser effect pVals for each mouse and also contringency table for later --
                conTableAllBands[indLaser, 0, indType] = np.sum(thisToneChoice)
                conTableAllBands[indLaser, 1, indType] = np.sum(thisNoiseChoice)

                # Calculate fraction of no-choise trials
                valid = laserBehavData['outcome']!=laserBehavData.labels['outcome']['invalid']
                nochoice = laserBehavData['outcome']==laserBehavData.labels['outcome']['nochoice']
                for indLaser in range(len(numLasers)):
                    thisFractionNoChoice[indType, indMouse, indLaser] = (nochoice[trialsEachLaser[:,indLaser]].sum() /
                                                                         valid[trialsEachLaser[:,indLaser]].sum())
        
            thispValsAllBand[indMouse, indType] = stats.fisher_exact(conTableAllBands[:,:,indType])[1]


            # -- Calculate performance by session --
            uniqueSessions = np.unique(laserBehavData['sessionID'])
            dprimeEachSession[indCell][indMouse][indType] = np.zeros((len(uniqueSessions),len(numLasers)))
            for indsession, sessionID in enumerate(uniqueSessions):
                for indLaser in range(len(numLasers)):
                    trialsThisCondS = trialsEachLaser[:, indLaser] & (laserBehavData['sessionID']==sessionID)
                    thisIncorrectS = incorrect[trialsThisCondS]
                    thisCorrectS = correct[trialsThisCondS]
                    thisNoiseChoiceS = noiseChoice[trialsThisCondS]
                    thisToneChoiceS = toneChoice[trialsThisCondS]
                    toneTrialsS = np.sum(thisCorrectS & thisToneChoiceS) + np.sum(thisIncorrectS & thisNoiseChoiceS)
                    noiseTrialsS = np.sum(thisCorrectS & thisNoiseChoiceS) + np.sum(thisIncorrectS & thisToneChoiceS)
                    thisHitRateS = np.sum(thisCorrectS & thisToneChoiceS) / toneTrialsS
                    thisFARateS = np.sum(thisIncorrectS & thisToneChoiceS) / noiseTrialsS
                    dprimeEachSession[indCell][indMouse][indType][indsession,indLaser] = (stats.norm.ppf(thisHitRateS) - \
                                                                                          stats.norm.ppf(thisFARateS))
                    #print((stats.norm.ppf(thisHitRateS) - stats.norm.ppf(thisFARateS)))

            
        conTableAnalysisAllBands = sm.stats.StratifiedTable(conTableAllBands)
        thispValsAllBand[indMouse, -1] = conTableAnalysisAllBands.test_null_odds(correction=True).pvalue

        for indBand in range(len(numBands)):
            conTableAnalysis = sm.stats.StratifiedTable(conTable[:,:,:,indBand])
            thispVals[indMouse, indBand, -1] = conTableAnalysis.test_null_odds(correction=True).pvalue

    accuracy.append(thisAccuracy)
    bias.append(thisBias)
    hits.append(thisHits)
    FAs.append(thisFAs)
    dprime.append(thisdprime)
    pVals.append(thispVals)
    fractionNoChoice.append(thisFractionNoChoice)

    accuracyAllBand.append(thisAccuracyAllBand)
    biasAllBand.append(thisBiasAllBand)
    hitsAllBand.append(thisHitsAllBand)
    FAallBand.append(thisFAsAllBand)
    dprimeAllBand.append(thisdprimeAllBand)
    pValsAllBand.append(thispValsAllBand)


# -- save responses of all sound responsive cells to 0.25 bandwidth sounds --
#outputFile = 'all_behaviour_inhib_inactivation_v2.npz'
outputFile = 'all_behaviour_inhib_inactivation_by_session.npz'
outputFullPath = os.path.join(dataDir, outputFile)
np.savez(outputFullPath,
         PVexpLaserAccuracy=accuracy[0][0, :, :, 1], PVexpNoLaserAccuracy=accuracy[0][0, :, :, 0],
         PVcontrolLaserAccuracy=accuracy[0][1, :, :, 1], PVcontrolNoLaserAccuracy=accuracy[0][1, :, :, 0],
         PVexpLaserBias=bias[0][0, :, :, 1], PVexpNoLaserBias=bias[0][0, :, :, 0],
         PVcontrolLaserBias=bias[0][1, :, :, 1], PVcontrolNoLaserBias=bias[0][1, :, :, 0],

         SOMexpLaserAccuracy=accuracy[1][0, :, :, 1], SOMexpNoLaserAccuracy=accuracy[1][0, :, :, 0],
         SOMcontrolLaserAccuracy=accuracy[1][1, :, :, 1], SOMcontrolNoLaserAccuracy=accuracy[1][1, :, :, 0],
         SOMexpLaserBias=bias[1][0, :, :, 1], SOMexpNoLaserBias=bias[1][0, :, :, 0],
         SOMcontrolLaserBias=bias[1][1, :, :, 1], SOMcontrolNoLaserBias=bias[1][1, :, :, 0],

         PVexpLaserHits=hits[0][0, :, :, 1], PVexpNoLaserHits=hits[0][0, :, :, 0],
         PVcontrolLaserHits=hits[0][1, :, :, 1], PVcontrolNoLaserHits=hits[0][1, :, :, 0],
         PVexpLaserFA=FAs[0][0, :, :, 1], PVexpNoLaserFA=FAs[0][0, :, :, 0],
         PVcontrolLaserFA=FAs[0][1, :, :, 1], PVcontrolNoLaserFA=FAs[0][1, :, :, 0],
         PVexpLaserdprime=dprime[0][0, :, :, 1], PVexpNoLaserdprime=dprime[0][0, :, :, 0],
         PVcontrolLaserdprime=dprime[0][1, :, :, 1], PVcontrolNoLaserdprime=dprime[0][1, :, :, 0],
         PVcontrolvsexppVal=pVals[0][:,:,-1], PVcontrolpVal=pVals[0][:,:,1], PVexppVal=pVals[0][:,:,0],

         SOMexpLaserHits=hits[1][0, :, :, 1], SOMexpNoLaserHits=hits[1][0, :, :, 0],
         SOMcontrolLaserHits=hits[1][1, :, :, 1], SOMcontrolNoLaserHits=hits[1][1, :, :, 0],
         SOMexpLaserFA=FAs[1][0, :, :, 1], SOMexpNoLaserFA=FAs[1][0, :, :, 0],
         SOMcontrolLaserFA=FAs[1][1, :, :, 1], SOMcontrolNoLaserFA=FAs[1][1, :, :, 0],
         SOMexpLaserdprime=dprime[1][0, :, :, 1], SOMexpNoLaserdprime=dprime[1][0, :, :, 0],
         SOMcontrolLaserdprime=dprime[1][1, :, :, 1], SOMcontrolNoLaserdprime=dprime[1][1, :, :, 0],
         SOMcontrolvsexppVal=pVals[1][:,:,-1], SOMcontrolpVal=pVals[1][:,:,1], SOMexppVal=pVals[1][:,:,0],

         PVexpLaserAccuracyAllBands=accuracyAllBand[0][0, :, 1], PVexpNoLaserAccuracyAllBands=accuracyAllBand[0][0, :, 0],
         PVcontrolLaserAccuracyAllBands=accuracyAllBand[0][1, :, 1], PVcontrolNoLaserAccuracyAllBands=accuracyAllBand[0][1, :, 0],
         PVexpLaserBiasAllBands=biasAllBand[0][0, :, 1], PVexpNoLaserBiasAllBands=biasAllBand[0][0, :, 0],
         PVcontrolLaserBiasAllBands=biasAllBand[0][1, :, 1], PVcontrolNoLaserBiasAllBands=biasAllBand[0][1, :, 0],

         SOMexpLaserAccuracyAllBands=accuracyAllBand[1][0, :, 1], SOMexpNoLaserAccuracyAllBands=accuracyAllBand[1][0, :, 0],
         SOMcontrolLaserAccuracyAllBands=accuracyAllBand[1][1, :, 1], SOMcontrolNoLaserAccuracyAllBands=accuracyAllBand[1][1, :, 0],
         SOMexpLaserBiasAllBands=biasAllBand[1][0, :, 1], SOMexpNoLaserBiasAllBands=biasAllBand[1][0, :, 0],
         SOMcontrolLaserBiasAllBands=biasAllBand[1][1, :, 1], SOMcontrolNoLaserBiasAllBands=biasAllBand[1][1, :, 0],

         PVexpLaserHitsAllBands=hitsAllBand[0][0, :, 1], PVexpNoLaserHitsAllBands=hitsAllBand[0][0, :, 0],
         PVcontrolLaserHitsAllBands=hitsAllBand[0][1, :, 1], PVcontrolNoLaserHitsAllBands=hitsAllBand[0][1, :, 0],
         PVexpLaserFAallBands=FAallBand[0][0, :, 1], PVexpNoLaserFAallBands=FAallBand[0][0, :, 0],
         PVcontrolLaserFAallBands=FAallBand[0][1, :, 1], PVcontrolNoLaserFAallBands=FAallBand[0][1, :, 0],
         PVexpLaserdprimeAllBands=dprimeAllBand[0][0, :, 1], PVexpNoLaserdprimeAllBands=dprimeAllBand[0][0, :, 0],
         PVcontrolLaserdprimeAllBands=dprimeAllBand[0][1, :, 1], PVcontrolNoLaserdprimeAllBands=dprimeAllBand[0][1, :, 0],
         PVcontrolvsexppValAllBands=pValsAllBand[0][:,-1], PVcontrolpValAllBand=pValsAllBand[0][:,1], PVexppValAllBand=pValsAllBand[0][:,0],

         SOMexpLaserHitsAllBands=hitsAllBand[1][0, :, 1], SOMexpNoLaserHitsAllBands=hitsAllBand[1][0, :, 0],
         SOMcontrolLaserHitsAllBands=hitsAllBand[1][1, :, 1], SOMcontrolNoLaserHitsAllBands=hitsAllBand[1][1, :, 0],
         SOMexpLaserFAallBands=FAallBand[1][0, :, 1], SOMexpNoLaserFAallBands=FAallBand[1][0, :, 0],
         SOMcontrolLaserFAallBands=FAallBand[1][1, :, 1], SOMcontrolNoLaserFAallBands=FAallBand[1][1, :, 0],
         SOMexpLaserdprimeAllBands=dprimeAllBand[1][0, :, 1], SOMexpNoLaserdprimeAllBands=dprimeAllBand[1][0, :, 0],
         SOMcontrolLaserdprimeAllBands=dprimeAllBand[1][1, :, 1], SOMcontrolNoLaserdprimeAllBands=dprimeAllBand[1][1, :, 0],
         SOMcontrolvsexppValAllBands=pValsAllBand[1][:,-1], SOMcontrolpValAllBand=pValsAllBand[1][:,1], SOMexppValAllBand=pValsAllBand[1][:,0],

         PVexpLaserFractionNoChoice=fractionNoChoice[0][0,:,1], PVexpNoLaserFractionNoChoice=fractionNoChoice[0][0,:,0],
         PVcontrolLaserFractionNoChoice=fractionNoChoice[0][1,:,1], PVcontrolNoLaserFractionNoChoice=fractionNoChoice[0][1,:,0],

         SOMexpLaserFractionNoChoice=fractionNoChoice[1][0,:,1], SOMexpNoLaserFractionNoChoice=fractionNoChoice[1][0,:,0],
         SOMcontrolLaserFractionNoChoice=fractionNoChoice[1][1,:,1], SOMcontrolNoLaserFractionNoChoice=fractionNoChoice[1][1,:,0],

         possibleBands=numBands,

         PVdprimeEachSession=dprimeEachSession[0],
         SOMdprimeEachSession=dprimeEachSession[1],
         eachSessionLabels=eachSessionLabels, 
)
print(outputFile + " saved")
