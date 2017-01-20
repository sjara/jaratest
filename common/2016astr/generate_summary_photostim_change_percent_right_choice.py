'''
This is a script to generate the data for a summary plot of the photostim experiments. Data from each mouse is generated separately, data for each session is also generated individually.

Loads all the photostim behavior sessions for each mice in the database; for each session, calculates the average percent change (photostim - control) of choice to the right side, store the results in an npz file.
Lan Guo 20170108
'''

import os
import numpy as np
import pandas as pd
from jaratoolbox import settings
from jaratoolbox import behavioranalysis
import figparams

scriptFullPath = os.path.realpath(__file__)

# -- Load the photostim experiments database -- #
tuingFilePath = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
tuningFileName = 'photostim_response_freq_summary.csv'
tuningFullPath = os.path.join(tuingFilePath,tuningFileName)
tuningDf = pd.read_csv(tuningFullPath)

resultsDict = {}

# -- Generate data for each mouse -- #
for mouse in np.unique(tuningDf.animalName):
    resultsDict[mouse+'leftHemiStim']=[]
    resultsDict[mouse+'rightHemiStim']=[]
    dfThisMouse = tuningDf.loc[tuningDf.animalName==mouse]
 
    # -- Calculate % contra choice change for each session and store data for left and right hemisphere photostim sessions separately -- #
    for ind,row in dfThisMouse.iterrows():
        session = str(row['session'])+'a'
        stimHemi = row['stim_hemi'] # 1=Left, 2=Right

        bdata = behavioranalysis.load_many_sessions(mouse,[session])
        trialType = bdata['trialType']
        stimTypes = [bdata.labels['trialType']['no_laser'],bdata.labels['trialType']['laser_left'],bdata.labels['trialType']['laser_right']]
        stimLabels = ['no_laser','laser_left','laser_right']
        trialsEachType = behavioranalysis.find_trials_each_type(trialType,stimTypes)
        choice=bdata['choice']
        valid=bdata['valid'] & (choice!=bdata.labels['choice']['none'])
        
        if stimHemi == 1: #This is a session where the left hemisphere is stimulated
            validTrialsControl = valid[trialsEachType[:,stimLabels.index('no_laser')]]
            validTrialsStim = valid[trialsEachType[:,stimLabels.index('laser_left')]]
            choiceRight = choice==bdata.labels['choice']['right']
            choiceRightControl = choiceRight[trialsEachType[:,stimLabels.index('no_laser')]]
            choiceRightStim = choiceRight[trialsEachType[:,stimLabels.index('laser_left')]]

            percentRightChoiceControl = sum(choiceRightControl&validTrialsControl)/float(sum(validTrialsControl))
            percentRightChoiceStim = sum(choiceRightStim&validTrialsStim)/float(sum(validTrialsStim))
            percentChangeRightChoice = percentRightChoiceStim-percentRightChoiceControl
            resultsDict[mouse+'leftHemiStim'].append(percentChangeRightChoice)
 
        elif stimHemi == 2: #This is a session where the right hemisphere is stimulated
            validTrialsControl = valid[trialsEachType[:,stimLabels.index('no_laser')]]
            validTrialsStim = valid[trialsEachType[:,stimLabels.index('laser_right')]]
            choiceRight = choice==bdata.labels['choice']['right']
            choiceRightControl = choiceRight[trialsEachType[:,stimLabels.index('no_laser')]]
            choiceRightStim = choiceRight[trialsEachType[:,stimLabels.index('laser_right')]]

            percentRightChoiceControl = sum(choiceRightControl&validTrialsControl)/float(sum(validTrialsControl))
            percentRightChoiceStim = sum(choiceRightStim&validTrialsStim)/float(sum(validTrialsStim))
            percentChangeRightChoice = percentRightChoiceStim-percentRightChoiceControl
            resultsDict[mouse+'rightHemiStim'].append(percentChangeRightChoice)

outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
outputFile = 'summary_photostim_percent_right_choice_change.npz'
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, script=scriptFullPath, **resultsDict)
