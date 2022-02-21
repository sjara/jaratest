'''
Test function for plotting psy-curves of bili mice (speech categorization)
'''


from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint #Used to compute confidence interval for the error bars.
from jaratoolbox import settings
import sys

subject = 'bili036'
#subjects = ['bili001','bili002','bili003','bili004','bili005','bili006','bili007']

paradigm = '2afc'

plt.clf()
fontsize=12
for inds,subject in enumerate(subjects):

    bfile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
    bdata = loadbehavior.BehaviorData(bfile,readmode='full')

    targetPercentage = bdata['targetFrequency'] # I used name 'frequency' initially
    choiceRight = bdata['choice']==bdata.labels['choice']['right']
    valid=bdata['valid']& (bdata['choice']!=bdata.labels['choice']['none'])
    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
           behavioranalysis.calculate_psychometric(choiceRight,targetPercentage,valid)

    plt.subplot(4,2,inds+1)
    plt.title('{0} [{1}]'.format(subject,session))
    #behavioranalysis.plot_frequency_psycurve(behavData,fontsize=12)

    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                    ciHitsEachValue,xTickPeriod=1, xscale='linear')
    plt.xlabel('Frequency (kHz)',fontsize=fontsize)
    plt.ylabel('Rightward trials (%)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(plt.gca(),fontsize)

    plt.show()

sys.exit()
