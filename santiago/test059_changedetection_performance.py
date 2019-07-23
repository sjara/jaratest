'''
Load behavior from change detection task and calculate performance.
'''

from __future__ import division
import numpy as np
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt
import sys

subjects = ['chad002','chad003','chad004']
sessions = ['20180426a','20180427a','20180428a','20180429a','20180430a','20180501a']
paradigm = 'gonogo'

for subject in subjects:
    print('\n----- {} -----'.format(subject))
    for session in sessions:
        behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
        bdata = loadbehavior.BehaviorData(behavFile)

        nTrials = len(bdata['nValid'])
        nValid = bdata['nValid'][-1]
        nRewarded = bdata['nRewarded'][-1]
        nEarly = nTrials-nValid
        nMiss = nValid-nRewarded

        fractionValid = float(nValid)/nTrials
        fractionRewarded = float(nRewarded)/nTrials
        fractionEarly = float(nEarly)/nTrials
        fractionMiss = float(nMiss)/nTrials

        print('\n-- {} --'.format(session))
        print('Hit: {} ({:.1%})'.format(nRewarded, fractionRewarded))
        print('FA: {} ({:.1%})'.format(nEarly, fractionEarly))
        print('Miss: {} ({:.1%})'.format(nMiss, fractionMiss))
