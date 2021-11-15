"""
Quantify fraction of no-choice trials across animals and conditions.

Uses data saved by generate_ac_inactivation_by_session.py 
"""

import sys
sys.path.append('..')

import os
import numpy as np
import pandas as pd
from scipy import stats

from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import studyparams


figName = 'figure_ac_inactivation'
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)

summaryFileName = 'all_behaviour_ac_inactivation_by_session.npz'

summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
summaryData = np.load(summaryDataFullPath)

expLaserFractionNoChoice = summaryData['expLaserFractionNoChoice']
expNoLaserFractionNoChoice = summaryData['expNoLaserFractionNoChoice']
controlLaserFractionNoChoice = summaryData['controlLaserFractionNoChoice']
controlNoLaserFractionNoChoice = summaryData['controlNoLaserFractionNoChoice']

'''
print(expLaserFractionNoChoice)
print(expNoLaserFractionNoChoice)
print(controlLaserFractionNoChoice)
print(controlNoLaserFractionNoChoice)
'''

noChoice = pd.DataFrame({'expLaser':expLaserFractionNoChoice,
                         'expNoLaser':expNoLaserFractionNoChoice,
                         'controlLaser':controlLaserFractionNoChoice,
                         'controlNoLaser':controlNoLaserFractionNoChoice})

expLaserMedian = np.median(expLaserFractionNoChoice)
expLaserMax = np.max(expLaserFractionNoChoice)
expNoLaserMedian = np.median(expNoLaserFractionNoChoice)
expNoLaserMax = np.max(expNoLaserFractionNoChoice)

print('--- PV-ChR2 ---')
print('Percentage of no-choice trials during experimental sessions:')
print(f'Median: {expLaserMedian:0.2%} (laser)  {expNoLaserMedian:0.2%} (No laser)')
print(f'Max: {expLaserMax:0.2%} (laser)  {expNoLaserMax:0.2%} (No laser)')
print('')


# -----------------------------------------------------------------------------------

figName = 'figure_inhibitory_inactivation'
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)

summaryFileName = 'all_behaviour_inhib_inactivation_by_session.npz'

summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
summaryDataInhib = np.load(summaryDataFullPath)

PVexpLaserFractionNoChoice = summaryDataInhib['PVexpLaserFractionNoChoice']
PVexpNoLaserFractionNoChoice = summaryDataInhib['PVexpNoLaserFractionNoChoice']
PVcontrolLaserFractionNoChoice = summaryDataInhib['PVcontrolLaserFractionNoChoice']
PVcontrolNoLaserFractionNoChoice = summaryDataInhib['PVcontrolNoLaserFractionNoChoice']

SOMexpLaserFractionNoChoice = summaryDataInhib['SOMexpLaserFractionNoChoice']
SOMexpNoLaserFractionNoChoice = summaryDataInhib['SOMexpNoLaserFractionNoChoice']
SOMcontrolLaserFractionNoChoice = summaryDataInhib['SOMcontrolLaserFractionNoChoice']
SOMcontrolNoLaserFractionNoChoice = summaryDataInhib['SOMcontrolNoLaserFractionNoChoice']

'''
noChoiceInhib = pd.DataFrame({'expLaser':expLaserFractionNoChoice,
                              'expNoLaser':expNoLaserFractionNoChoice,
                              'controlLaser':controlLaserFractionNoChoice,
                              'controlNoLaser':controlNoLaserFractionNoChoice})
'''

PVexpLaserMedian = np.median(PVexpLaserFractionNoChoice)
PVexpLaserMax = np.max(PVexpLaserFractionNoChoice)
PVexpNoLaserMedian = np.median(PVexpNoLaserFractionNoChoice)
PVexpNoLaserMax = np.max(PVexpNoLaserFractionNoChoice)

SOMexpLaserMedian = np.median(SOMexpLaserFractionNoChoice)
SOMexpLaserMax = np.max(SOMexpLaserFractionNoChoice)
SOMexpNoLaserMedian = np.median(SOMexpNoLaserFractionNoChoice)
SOMexpNoLaserMax = np.max(SOMexpNoLaserFractionNoChoice)

print('--- PV-ArchT ---')
print('Percentage of no-choice trials during experimental sessions:')
print(f'Median: {PVexpLaserMedian:0.2%} (laser)  {PVexpNoLaserMedian:0.2%} (No laser)')
print(f'Max: {PVexpLaserMax:0.2%} (laser)  {PVexpNoLaserMax:0.2%} (No laser)')
print('')

print('--- SOM-ArchT-ChR2 ---')
print('Percentage of no-choice trials during experimental sessions:')
print(f'Median: {SOMexpLaserMedian:0.2%} (laser)  {SOMexpNoLaserMedian:0.2%} (No laser)')
print(f'Max: {SOMexpLaserMax:0.2%} (laser)  {SOMexpNoLaserMax:0.2%} (No laser)')
print('')

