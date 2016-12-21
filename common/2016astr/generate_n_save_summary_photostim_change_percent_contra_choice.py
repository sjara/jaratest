'''
This is a script to generate the data for a summary plot of the photostim experiments. Data from each mouse is generated separately, data for each session is also generated individually.

Loads all the photostim behavior sessions for each mice in the database; for each session, calculates the average percent change (photostim - control) of choice to the side contralateral to stimulated hemisphere, store the results in an npz file.
Lan Guo 20161220
'''

import os
import numpy as np
import pandas as pd
from jaratoolbox import behavioranalysis

# -- Load the photostim experiments database -- #
databaseFile = '/home/languo/data/behavior_reports/photostim_response_freq_summary.csv'
tuningDf = pd.read_csv(databaseFile)

resultsDict = {}

# -- Generate data for each mouse -- #
for mouse in np.unique(tuningDf.animalName):
    resultsDict[mouse+'leftHemiStim']=[]
    resultsDict[mouse+'rightHemiStim']=[]
    dfThisMouse = tuningDf.loc[tuningDf.animalName==mouse]
 
    # -- Calculate % contra choice change for each session and store data for left and right hemisphere photostim sessions separately -- #
    for row in dfThisMouse.itertuples():
        session = row['session']+'a'
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

            percentContraChoiceControl = sum(choiceRightControl&validTrialsControl)/sum(validTrialsControl)
            percentContraChoiceStim = sum(choiceRightLeftStim&validTrialsStim)/sum(validTrialsStim)
            percentChangeContraChoice = percentContraChoiceLeftStim-percentContraChoiceControl
            resultsDict[mouse+'leftHemiStim'].append(percentChangeContraChoice)
 
       elif stimHemi == 2: #This is a session where the right hemisphere is stimulated
            validTrialsControl = valid[trialsEachType[:,stimLabels.index('no_laser')]]
            validTrialsStim = valid[trialsEachType[:,stimLabels.index('laser_right')]]
            choiceLeft = choice==bdata.labels['choice']['left']
            choiceLeftControl = choiceLeft[trialsEachType[:,stimLabels.index('no_laser')]]
            choiceLeftStim = choiceLeft[trialsEachType[:,stimLabels.index('laser_right')]]

            percentContraChoiceControl = sum(choiceLeftControl&validTrialsControl)/sum(validTrialsControl)
            percentContraChoiceStim = sum(choiceLeftStim&validTrialsStim)/sum(validTrialsStim)
            percentChangeContraChoice = percentContraChoiceStim-percentContraChoiceControl
            resultsDict[mouse+'rightHemiStim'].append(percentChangeContraChoice)

outputDir = '/home/languo/data/mnt/figures_papers'
outputFile = 'summary_photostim_percent_contra_choice_change.npz'
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, **resultsDict)
