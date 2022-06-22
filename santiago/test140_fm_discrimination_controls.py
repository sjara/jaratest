"""
Test performance of pamo mice under the control FM stimuli.
Based on 2022apas/generate_fm_controls.py 
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots
from jaratoolbox import extrastats
from importlib import reload

paradigm = '2afc'

subjects = ['pamo010', 'pamo014', 'pamo015', 'pamo017', 'pamo018',
            'pamo021', 'pamo023', 'pamo025', 'pamo024']

sessions = ['20220406a']


plt.clf()
for indsub, subject in enumerate(subjects):
    print(f'{indsub}  {subject}')

    nSessions = len(sessions)
    correctEachSession = np.empty(nSessions)
    validEachSession = np.empty(nSessions)
    for indsession, session in enumerate(sessions):
        behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
        bdata = loadbehavior.BehaviorData(behavFile)

        correct = bdata['outcome']==bdata.labels['outcome']['correct']
        valid = bdata['valid'].astype(bool)
        rightwardChoice = bdata['choice']==bdata.labels['choice']['right']

        correctEachSession[indsession] = np.sum(correct)
        validEachSession[indsession] = np.sum(valid)
        
        targetParamValue = bdata['targetFMslope']
        possibleParamValue = np.unique(targetParamValue)
        nParamValues = len(possibleParamValue)
        startFreq = bdata['startFreq']
        possibleStartFreq = np.unique(startFreq)
        endFreq = bdata['endFreq']
        possibleEndFreq = np.unique(endFreq)

        extSubset = (startFreq==possibleStartFreq[0]) | (startFreq==possibleStartFreq[2])
        #extSubset = (endFreq==possibleEndFreq[1])
        midSubset = (startFreq==possibleStartFreq[1])
        
        (possibleValues1, fractionHitsEachValue1, ciHitsEachValue1, nTrialsEachValue1, nHitsEachValue1)=\
            behavioranalysis.calculate_psychometric(rightwardChoice, targetParamValue, valid & extSubset)
        (possibleValues2, fractionHitsEachValue2, ciHitsEachValue2, nTrialsEachValue2, nHitsEachValue2)=\
            behavioranalysis.calculate_psychometric(rightwardChoice, targetParamValue, valid & midSubset)
        
        if 1:
            plt.cla()
            xTicks = np.arange(-1, 1.5, 0.5)
            fontSizeLabels = 12
            (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(possibleValues1,
                                                                        fractionHitsEachValue1,
                                                                        ciHitsEachValue1, xTicks=None,
                                                                        xscale='linear')
            (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(possibleValues2,
                                                                        fractionHitsEachValue2,
                                                                        ciHitsEachValue2, xTicks=None,
                                                                        xscale='linear')
            plt.xlim([-1.2, 1.2])
            plt.ylabel('Rightward choice (%)', fontsize=fontSizeLabels)
            plt.xlabel('FM slope (A.U.)', fontsize=fontSizeLabels)
            titleStr = f'{subject}: {session}'
            plt.title(titleStr, fontsize=fontSizeLabels, fontweight='bold')
            plt.grid(True, axis='y', color='0.9')
            plt.show()
            plt.pause(0.01)
            plt.waitforbuttonpress()

