"""
Plot psychmetric curve for an animal trained with the am_discrimination paradigm.
"""

import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots

subject = 'amod017'
paradigm = '2afc'
session = '20211212a'

behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
bdata = loadbehavior.BehaviorData(behavFile)

'''
# -- If you want to plot data pooled from many sessions use code below --
sessions = ['20211012a','20211013a','20211014a','20211015a',
            '20211016a','20211017a','20211018a','20211019a']
bdata = behavioranalysis.load_many_sessions(subject, paradigm=paradigm, sessions=sessions)
nSessions = bdata['sessionID'][-1]
'''

validTrials = bdata['valid'].astype(bool)
rightwardChoice = bdata['choice']==bdata.labels['choice']['right']

targetParamValue = bdata['targetFrequency']
possibleParamValue = np.unique(targetParamValue)
nParamValues = len(possibleParamValue)

xTicks = [8, 16, 32] #None
(possibleValues, fractionHitsEachValue, ciHitsEachValue, nTrialsEachValue, nHitsEachValue)=\
    behavioranalysis.calculate_psychometric(rightwardChoice, targetParamValue, validTrials)

plt.clf()
fontSizeLabels = 12
(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(possibleValues,fractionHitsEachValue,
                                                            ciHitsEachValue, xTicks=xTicks,
                                                            xscale='log')
plt.ylim([-5,105])
plt.ylabel('Rightward choice (%)', fontsize=fontSizeLabels)
plt.xlabel('AM rate (Hz)', fontsize=fontSizeLabels)
titleStr = f'{subject}: {session}'
#titleStr = f'{subject}: {sessions[0]} - {sessions[-1]}'  # For multisession
plt.title(titleStr, fontsize=fontSizeLabels, fontweight='bold')

plt.show()
