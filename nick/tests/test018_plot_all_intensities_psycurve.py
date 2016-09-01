
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
import numpy as np
from pylab import *
import matplotlib.pyplot as plt

subjects = ['hm4d003', 'hm4d004', 'hm4d005', 'hm4d006']
session = '20140820a'

for ind, subject in enumerate(subjects):
    fname=loadbehavior.path_to_behavior_data(subject,'nick','2afc',session)


    bdata=loadbehavior.BehaviorData(fname)
    from jaratoolbox import settings 

    targetFrequency=bdata['targetFrequency']
    valid=bdata['valid']
    choice=bdata['choice']
    intensities=bdata['targetIntensity']
    choiceRight = choice==bdata.labels['choice']['right']


    possibleFreq = np.unique(targetFrequency)
    nFreq = len(possibleFreq) 
    trialsEachFreq = behavioranalysis.find_trials_each_type(targetFrequency,possibleFreq)

    positions=[(0,0), (0,1), (1,0), (1,1)]
    ax1=plt.subplot2grid((2,2), positions[ind])

    for intensity in np.unique(intensities):
        nTrialsEachFreq = np.empty(nFreq)
        nRightwardEachFreq = np.empty(nFreq)
        for indf,thisFreq in enumerate(possibleFreq):
            nTrialsEachFreq[indf] = sum(valid & trialsEachFreq[:,indf] & (intensities==intensity))
            nRightwardEachFreq[indf] = sum(valid & choiceRight & trialsEachFreq[:,indf] & (intensities==intensity))

        fractionRightEachFreq = nRightwardEachFreq/nTrialsEachFreq.astype(float)

        #plot(possibleFreq,fractionRightEachFreq,'-o')
        #gca().set_xscale('log')
        ax1.plot(fractionRightEachFreq,'-o', label=intensity)
    title(subject)
    legend()
    ylim([0,1])
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
