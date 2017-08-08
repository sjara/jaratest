'''
This is a script to generate the data for a summary plot of the photostim experiments for control mice. Data from each mouse is generated separately, data for each session is also generated individually.

Loads all the photostim behavior sessions for each mice in the database; for each session, calculates the average percent change (photostim - control) of choice to the right side, store the results in an npz file.
Lan Guo 20170802
'''

import os
import numpy as np
import pandas as pd
from jaratoolbox import settings
from jaratoolbox import behavioranalysis
import figparams
import pdb
FIGNAME = 'photostim_2afc'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
scriptFullPath = os.path.realpath(__file__)

sessionsDict = {'adap048': {'leftHemiStim': ['20170717a',
                                            '20170719a',
                                            '20170721a',
                                            '20170724a',
                                            '20170726a',
                                            '20170728a',
                                            '20170801a',
                                            '20170803a',
                                            '20170807a'
                                            ],
                            'rightHemiStim': ['20170718a',
                                            '20170720a',
                                            '20170722a',
                                            '20170725a',
                                            '20170727a',
                                            '20170731a',
                                            '20170802a',
                                            '20170804a',
                                            ]
                            },
                'adap056': {'leftHemiStim': ['20170717a',
                                            '20170719a',
                                            '20170721a',
                                            '20170724a',
                                            '20170726a',
                                            '20170728a',
                                            '20170801a',
                                            '20170803a',
                                            '20170807a'
                                            ],
                            'rightHemiStim': ['20170718a',
                                            '20170720a',
                                            '20170722a',
                                            '20170725a',
                                            '20170727a',
                                            '20170731a',
                                            '20170802a',
                                            '20170804a',
                                            ]
                            }

}
resultsDict = {}

# -- Generate data for each mouse -- #
for mouse,sessionsEachMouse in sessionsDict.items():
    for stimHemi,sessions in sessionsEachMouse.items():
        resultsDict[mouse+stimHemi+'Sessions'] = sessions
        resultsDict[mouse+stimHemi]=[]

        for session in sessions:
            bdata = behavioranalysis.load_many_sessions(mouse,[session])
            trialType = bdata['trialType']
            stimTypes = [bdata.labels['trialType']['no_laser'],bdata.labels['trialType']['laser_left'],bdata.labels['trialType']['laser_right']]
            stimLabels = ['no_laser','laser_left','laser_right']
            trialsEachType = behavioranalysis.find_trials_each_type(trialType,stimTypes)
            choice=bdata['choice']
            valid=bdata['valid'] & (choice!=bdata.labels['choice']['none'])
            if stimHemi == 'leftHemiStim':
                validTrialsControl = valid[trialsEachType[:,stimLabels.index('no_laser')]]
                validTrialsStim = valid[trialsEachType[:,stimLabels.index('laser_left')]]
                choiceRight = choice==bdata.labels['choice']['right']
                choiceRightControl = choiceRight[trialsEachType[:,stimLabels.index('no_laser')]]
                choiceRightControl = choiceRightControl&validTrialsControl
                choiceRightStim = choiceRight[trialsEachType[:,stimLabels.index('laser_left')]]
                choiceRightStim = choiceRightStim&validTrialsStim
                #pdb.set_trace()
                percentRightChoiceControl = sum(choiceRightControl)/float(sum(validTrialsControl))
                percentRightChoiceStim = sum(choiceRightStim)/float(sum(validTrialsStim))
                percentChangeRightChoice = percentRightChoiceStim-percentRightChoiceControl
                                
            elif stimHemi == 'rightHemiStim': 
                validTrialsControl = valid[trialsEachType[:,stimLabels.index('no_laser')]]
                validTrialsStim = valid[trialsEachType[:,stimLabels.index('laser_right')]]
                choiceRight = choice==bdata.labels['choice']['right']
                choiceRightControl = choiceRight[trialsEachType[:,stimLabels.index('no_laser')]]
                choiceRightControl = choiceRightControl&validTrialsControl
                choiceRightStim = choiceRight[trialsEachType[:,stimLabels.index('laser_right')]]
                choiceRightStim = choiceRightStim&validTrialsStim
                #pdb.set_trace()
                percentRightChoiceControl = sum(choiceRightControl)/float(sum(validTrialsControl))
                percentRightChoiceStim = sum(choiceRightStim)/float(sum(validTrialsStim))
                percentChangeRightChoice = percentRightChoiceStim-percentRightChoiceControl
            resultsDict[mouse+stimHemi].append(percentChangeRightChoice)
                

#outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
outputFile = 'summary_photostim_control_percent_right_choice_change.npz'
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, script=scriptFullPath, **resultsDict)
