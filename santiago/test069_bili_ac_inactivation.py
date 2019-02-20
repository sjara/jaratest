'''
Performance after inactivation of AC in bili mice.
'''


from jaratoolbox import behavioranalysis
reload(behavioranalysis)
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
reload(extraplots)
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint #Used to compute confidence interval for the error bars. 
from jaratoolbox import settings 
import sys

subjects = ['bili002']
#subjects = ['bili001','bili002','bili003','bili004','bili005','bili006','bili007']
session = '20190219a'
paradigm = '2afc'

plt.clf()
fontsize=12
for inds,subject in enumerate(subjects):
    
    bfile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
    bdata = loadbehavior.BehaviorData(bfile,readmode='full')

    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    targetPercentage = bdata['targetFrequency'] # I used name 'frequency' initially
    choiceRight = bdata['choice']==bdata.labels['choice']['right']
    valid = bdata['valid'].astype(bool) & (bdata['choice']!=bdata.labels['choice']['none'])
    laserTrials = bdata['laserTrial']==bdata.labels['laserTrial']['yes']
    validLaser = valid & laserTrials
    validNoLaser = valid & ~laserTrials
    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
           behavioranalysis.calculate_psychometric(choiceRight,targetPercentage,validNoLaser)
    (possibleValuesL,fractionHitsEachValueL,ciHitsEachValueL,nTrialsEachValueL,nHitsEachValueL)=\
           behavioranalysis.calculate_psychometric(choiceRight,targetPercentage,validLaser)

    nNoLaser = np.sum(validNoLaser)
    nLaser = np.sum(validLaser)
    fractionCorrectNoLaser = np.mean(correct[validNoLaser])
    fractionCorrectLaser = np.mean(correct[validLaser])
    print('Correct: NoLaser({})={:0.1%}  Laser({})={:0.1%}'.format(nNoLaser,fractionCorrectNoLaser,
                                                                   nLaser,fractionCorrectLaser))
    
    #plt.subplot(4,2,inds+1)
    plt.title('{0} [{1}]'.format(subject,session))
    #behavioranalysis.plot_frequency_psycurve(behavData,fontsize=12)

    plt.hold(1)
    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                    ciHitsEachValue,xTickPeriod=1, xscale='linear')
    (plineL, pcapsL, pbarsL, pdotsL) = extraplots.plot_psychometric(1e-3*possibleValuesL,fractionHitsEachValueL,
                                                                    ciHitsEachValueL,xTickPeriod=1, xscale='linear')

    plt.setp([plineL,pcapsL,pbarsL,pdotsL],color='r')
    
    plt.xlabel('Frequency (kHz)',fontsize=fontsize)
    plt.ylabel('Rightward trials (%)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(plt.gca(),fontsize)

    plt.show()

sys.exit()
