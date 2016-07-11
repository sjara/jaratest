'''
Test function for plotting psy-curves
'''


from jaratoolbox import behavioranalysis
reload(behavioranalysis)
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
reload(extraplots)
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint #Used to compute confidence interval for the error bars. 
from jaratoolbox import settings 
import sys

animalName = 'test012'
session = '20150106a'
experimenter = 'santiago'
paradigm = '2afc'

behavioranalysis.behavior_summary(animalName,session)

sys.exit()

behavFile = loadbehavior.path_to_behavior_data(animalName,experimenter,paradigm,session)
bdata = loadbehavior.FlexCategBehaviorData(behavFile)

targetFrequency = bdata['targetFrequency']
choice=bdata['choice']
valid=bdata['valid']& (choice!=bdata.labels['choice']['none'])
choiceRight = choice==bdata.labels['choice']['right']

possibleFreq = np.unique(targetFrequency)
nFreq = len(possibleFreq) 
trialsEachFreq = behavioranalysis.find_trials_each_type(targetFrequency,possibleFreq)

(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
   behavioranalysis.calculate_psychometric(choiceRight,targetFrequency,valid)

(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(possibleValues,fractionHitsEachValue,ciHitsEachValue)

'''
upperWhisker = ciHitsEachValue[1,:]-fractionHitsEachValue
lowerWhisker = fractionHitsEachValue-ciHitsEachValue[0,:]

(pline, pcaps, pbars) = errorbar(possibleValues, 100*fractionHitsEachValue, 
                                 yerr = [100*lowerWhisker, 100*upperWhisker],color='k')
plot(possibleValues, 100*fractionHitsEachValue, 'o',mec='none',mfc='k',ms=8)
setp(pline,lw=2)
axhline(y=50, color = '0.5',ls='--')
ax=gca()
ax.set_xscale('log')
#ax.set_xticks([3000,5000,7000,10000,14000,20000,40000])
ax.set_xticks([3000,7000,16000])
ax.set_xticks(np.arange(1000,40000,1000),minor=True)
from matplotlib.ticker import ScalarFormatter
for axis in [ax.xaxis, ax.yaxis]:
    axis.set_major_formatter(ScalarFormatter())

ylim([0,100])
xlim([possibleFreq[0]/1.2,possibleFreq[-1]*1.2])
xlabel('Frequency (kHz)')
ylabel('Rightward trials (%)')
title(animalName)
'''

show()
