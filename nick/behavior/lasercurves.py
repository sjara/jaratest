from jaratoolbox import loadbehavior
reload(loadbehavior)
import copy
from jaratest.nick.behavior import soundtypes
from jaratoolbox import behavioranalysis
from matplotlib import pyplot as plt
import numpy as np
from jaratoolbox import extraplots
fontsize = 12

subjects = ['amod012', 'amod013']
# sessions = ['20170411a']
# sessions = ['20170412a']
sessions = ['20170411a', '20170412a']

# bdataPath = loadbehavior.path_to_behavior_data(subject, '2afc', '20170411a')

plt.figure()
for indSubject, subject in enumerate(subjects):

    (dataObjs, dataSoundTypes) = soundtypes.load_behavior_sessions_sound_type(subject,sessions)

    for indData, bdata in enumerate(dataObjs):
        plt.subplot(2, 2, (2*indSubject) + indData+1)


        targetFrequency = bdata['targetFrequency']
        choice=bdata['choice']
        # valid=bdata['valid']& (choice!=bdata.labels['choice']['none'])
        laser = bdata['laserOn']==1
        noLaser = bdata['laserOn']==0

        choiceRight = choice==bdata.labels['choice']['right']
        possibleFreq = np.unique(targetFrequency)
        nFreq = len(possibleFreq) 
        trialsEachFreq = behavioranalysis.find_trials_each_type(targetFrequency,possibleFreq)


        #noLaser first
        (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
        behavioranalysis.calculate_psychometric(choiceRight,targetFrequency,noLaser)
        (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                    ciHitsEachValue,xTickPeriod=1)
        plt.xlabel('Frequency (kHz)',fontsize=fontsize)
        plt.ylabel('Rightward trials (%)',fontsize=fontsize)
        extraplots.set_ticks_fontsize(plt.gca(),fontsize)
        plt.setp(pline, color='k')
        plt.setp(pcaps, color='k')
        plt.setp(pbars, color='k')
        plt.setp(pdots, markerfacecolor='k')

        plt.hold(1)

        #laser second
        (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
        behavioranalysis.calculate_psychometric(choiceRight,targetFrequency,laser)
        (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                    ciHitsEachValue,xTickPeriod=1)
        plt.xlabel('Frequency (kHz)',fontsize=fontsize)
        plt.ylabel('Rightward trials (%)',fontsize=fontsize)
        extraplots.set_ticks_fontsize(plt.gca(),fontsize)
        plt.setp(pline, color='b')
        plt.setp(pcaps, color='b')
        plt.setp(pbars, color='b')
        plt.setp(pdots, markerfacecolor='b')

        plt.title('{} {}'.format(subject, list(dataSoundTypes)[indData]))

plt.show()
