#!/usr/bin/env python

'''
Show performance for one session of one animal.

Santiago Jaramillo - 2016-04-15
'''

from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt

EXPERIMENTER = settings.DEFAULT_EXPERIMENTER
paradigm = '2afc'

subject = 'adap021'
session = '20160310a' # This is the date formatted as YYYYMMDD and one more character (usually 'a')

# -- Find the data filename and load the data into a data object (similar to a Python dict) --
behavFile = loadbehavior.path_to_behavior_data(subject,EXPERIMENTER,paradigm,session)
behavData = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')

# -- Calculate average performance --
nValidTrials = behavData['nValid'][-1]
nRewardedTrials = behavData['nRewarded'][-1]
print 'Average performance: {:0.1%}'.format(float(nRewardedTrials)/nValidTrials)

# -- Plot psychometric curve --
plt.clf()
(pline, pcaps, pbars, pdots) = behavioranalysis.plot_frequency_psycurve(behavData,fontsize=14)
plt.show()

'''
plt.clf()
freqsToUse = [behavData['lowFreq'][-1],behavData['highFreq'][-1]]
behavioranalysis.plot_summary(behavData,fontsize=14,soundfreq=freqsToUse)
plt.show()

plt.clf()
freqsToUse = [behavData['lowFreq'][-1],behavData['highFreq'][-1]]
behavioranalysis.plot_dynamics(behavData,winsize=40,fontsize=14,soundfreq=freqsToUse)
plt.show()
'''
