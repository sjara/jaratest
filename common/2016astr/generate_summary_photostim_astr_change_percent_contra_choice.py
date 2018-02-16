'''
This is a script to generate the data for a summary plot of the photostim experiments carried out in d1pi011 in the anterior striatum (astr). Data for each session is generated individually. For each session, calculates the average percent change (photostim - control) of choice to the right side, store the results in an npz file.
Lan Guo 20180202
'''

import os
import numpy as np
import pandas as pd
from jaratoolbox import settings
from jaratoolbox import behavioranalysis
import figparams

FIGNAME = 'photostim_astr_2afc'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
scriptFullPath = os.path.realpath(__file__)

animalName = ['d1pi011']

sessionsDict = {'left_astr':['20160621','20160623'],
                'right_astr':['20160622','20160624']
}

resultsDict = {}

# -- Generate data for each mouse -- #
for mouse in animalName:
    resultsDict[mouse+'leftHemiStim']=[]
    resultsDict[mouse+'leftHemiStimSessions']=[]
    resultsDict[mouse+'rightHemiStim']=[]
    resultsDict[mouse+'rightHemiStimSessions']=[]
 
    # -- Calculate % contra choice change for each session and store data for left and right hemisphere photostim sessions separately -- #
    for hemi,sessions in sessionsDict.items():
        for session in sessions:
            session = session+'a'
            stimHemi = hemi

            bdata = behavioranalysis.load_many_sessions(mouse,[session])
            trialType = bdata['trialType']
            stimTypes = [bdata.labels['trialType']['no_laser'],bdata.labels['trialType']['laser_left'],bdata.labels['trialType']['laser_right']]
            stimLabels = ['no_laser','laser_left','laser_right']
            trialsEachType = behavioranalysis.find_trials_each_type(trialType,stimTypes)
            choice=bdata['choice']
            valid=bdata['valid'] & (choice!=bdata.labels['choice']['none'])

            if stimHemi == 'left_astr': #This is a session where the left hemisphere is stimulated
                validTrialsControl = valid[trialsEachType[:,stimLabels.index('no_laser')]]
                validTrialsStim = valid[trialsEachType[:,stimLabels.index('laser_left')]]
                choiceContra = choice==bdata.labels['choice']['right']
                choiceContraControl = choiceContra[trialsEachType[:,stimLabels.index('no_laser')]]
                choiceContraStim = choiceContra[trialsEachType[:,stimLabels.index('laser_left')]]

                percentContraChoiceControl = sum(choiceContraControl&validTrialsControl)/float(sum(validTrialsControl))
                percentContraChoiceStim = sum(choiceContraStim&validTrialsStim)/float(sum(validTrialsStim))
                percentChangeContraChoice = percentContraChoiceStim-percentContraChoiceControl
                resultsDict[mouse+'leftHemiStim'].append(percentChangeContraChoice)
                resultsDict[mouse+'leftHemiStimSessions'].append(session)

            elif stimHemi == 'right_astr': #This is a session where the right hemisphere is stimulated
                validTrialsControl = valid[trialsEachType[:,stimLabels.index('no_laser')]]
                validTrialsStim = valid[trialsEachType[:,stimLabels.index('laser_right')]]
                choiceContra = choice==bdata.labels['choice']['left']
                choiceContraControl = choiceContra[trialsEachType[:,stimLabels.index('no_laser')]]
                choiceContraStim = choiceContra[trialsEachType[:,stimLabels.index('laser_right')]]

                percentContraChoiceControl = sum(choiceContraControl&validTrialsControl)/float(sum(validTrialsControl))
                percentContraChoiceStim = sum(choiceContraStim&validTrialsStim)/float(sum(validTrialsStim))
                percentChangeContraChoice = percentContraChoiceStim-percentContraChoiceControl
                resultsDict[mouse+'rightHemiStim'].append(percentChangeContraChoice)
                resultsDict[mouse+'rightHemiStimSessions'].append(session)

#outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
outputFile = 'summary_astr_photostim_percent_contra_choice_change.npz'
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, script=scriptFullPath, **resultsDict)
