
"""
Plot psychmetric curve for an animal trained with the fm_discrimination paradigm.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots

subject = 'pamo026'
paradigm = '2afc'
'''
session = '20211012a'

behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
bdata = loadbehavior.BehaviorData(behavFile)

'''
# -- If you want to plot data pooled from many sessions use code below --
#sessions = ['20220304a']            
sessions = ['20220328a','20220327a','20220326a','20220325a',
            '20220324a','20220323a','20220322a','20220321a',
            '20220320a','20220319a','20220318a','20220317a',
            '20220316a','20220315a','20220314a','20220313a',
            '20220312a','20220311a','20220310a','20220309a',
            '20220308a','20220307a','20220306a','20220305a'
            '20220304a','20220303a','20220302a','20220301a']            
bdata = behavioranalysis.load_many_sessions(subject, paradigm=paradigm, sessions=sessions)
nSessions = bdata['sessionID'][-1]

validTrials = bdata['valid'].astype(bool)
rightwardChoice = bdata['choice']==bdata.labels['choice']['right']

'''
This part is edited in orignal code
'''

df_trial_information = pd.DataFrame({'sessionID': nSessions,
                                          'valid': validTrials,
                                          'r_choice': rightwardChoice
                                          })

'''
*************************
'''
print (df_trial_information)

targetParamValue = bdata['targetFMslope']
possibleParamValue = np.unique(targetParamValue)
nParamValues = len(possibleParamValue)

xTicks = np.arange(-1, 1.5, 0.5)
(possibleValues, fractionHitsEachValue, ciHitsEachValue, nTrialsEachValue, nHitsEachValue)=\
    behavioranalysis.calculate_psychometric(rightwardChoice, targetParamValue, validTrials)
print(type(possibleValues))
plt.clf()
fontSizeLabels = 12
(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(possibleValues,fractionHitsEachValue,
                                                            ciHitsEachValue, xTicks=xTicks,
                                                            xscale='linear')
plt.ylim([-5,105])
plt.ylabel('Rightward choice (%)', fontsize=fontSizeLabels)
plt.xlabel('FM slope (A.U.)', fontsize=fontSizeLabels)
#titleStr = f'{subject}: {session}'
titleStr = f'{subject}: {sessions[0]} - {sessions[-1]}'  # For multisession
plt.title(titleStr, fontsize=fontSizeLabels, fontweight='bold')
#slope = (y2-y1)/(x2-x1)
#b = y1 - slope * x1
# pamo009 first day(20220228a)
#slope = -14.325
#b=11.025
#pamo007 first day (20221119a)
#slope = -5.099
#b=35.540
#plt.plot(possibleValues, slope*possibleValues + b, 'r--')
plt.show()
