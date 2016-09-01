from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
import numpy as np
from pylab import *
import matplotlib.pyplot as plt

#subject = 'hm4d003'
#session = '20140820a'

'''
subject = 'test053'
session = '20140907a'
experimenter = 'santiago'
'''

subject = 'test000'
session = '20141110a'
experimenter = 'santiago'

minIntensityToPlot = 30

fname=loadbehavior.path_to_behavior_data(subject,experimenter,'2afc',session)


bdata=loadbehavior.BehaviorData(fname)
from jaratoolbox import settings 

targetFrequency=bdata['targetFrequency']
valid=bdata['valid']
choice=bdata['choice']
intensity=bdata['targetIntensity']
choiceRight = choice==bdata.labels['choice']['right']


possibleFreq = np.unique(targetFrequency)
nFreq = len(possibleFreq) 
trialsEachFreq = behavioranalysis.find_trials_each_type(targetFrequency,possibleFreq)

nTrialsEachFreq = np.empty(nFreq)
nRightwardEachFreq = np.empty(nFreq)
for indf,thisFreq in enumerate(possibleFreq):
    nTrialsEachFreq[indf] = sum(valid & trialsEachFreq[:,indf] & (intensity>=minIntensityToPlot))
    nRightwardEachFreq[indf] = sum(valid & choiceRight & trialsEachFreq[:,indf] & (intensity>=minIntensityToPlot))

fractionRightEachFreq = nRightwardEachFreq/nTrialsEachFreq.astype(float)

#plot(possibleFreq,fractionRightEachFreq,'-o')
#gca().set_xscale('log')

plot(np.log2(possibleFreq),fractionRightEachFreq,'-o')

#plot(fractionRightEachFreq,'-o')
title(subject)
ylim([0,1])
ylabel('Fraction correct')
xlabel('Frequency [log2(Hz)]')
show()


'''
    fractionRightEachFreq = nRightwardEachFreq/nTrialsEachFreq.astype(float)

    #plot(possibleFreq,fractionRightEachFreq,'-o')
    #gca().set_xscale('log')
    positions=[(0,0), (0,1), (1,0), (1,1)]
    ax1=plt.subplot2grid((2,2), positions[ind])
    ax1.plot(fractionRightEachFreq,'-o')
    title(subject)
    ylim([0,1])
show()
'''
