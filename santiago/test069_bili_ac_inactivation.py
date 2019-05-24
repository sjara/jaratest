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
#from scipy import stats

#subjects = ['bili001','bili002','bili003','bili004','bili005','bili006','bili007']

subjects = ['bili002']
#sessions = ['20190219a','20190220a','20190222a','20190225a','20190228a','20190302a','20190304a'] # Laser inside
#sessions = ['20190221a','20190223a','20190224a','20190301a','20190303a'] # Control (outside brain)

subjects = ['bili006']
#sessions = ['20190301a','20190303a','20190305a'] # Laser inside
sessions = ['20190302a','20190304a'] # Laser inside

paradigm = '2afc'

laserColor = [0,0.75,0]

plt.clf()
fontsize=12
for inds,subject in enumerate(subjects):
    
    #bfile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
    #bdata = loadbehavior.BehaviorData(bfile,readmode='full')

    bdata = behavioranalysis.load_many_sessions(subjects,sessions)

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
    #plt.title('{0} [{1}]'.format(subject,session))

    plt.hold(1)
    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                    ciHitsEachValue,xTickPeriod=1, xscale='linear')
    (plineL, pcapsL, pbarsL, pdotsL) = extraplots.plot_psychometric(1e-3*possibleValuesL,fractionHitsEachValueL,
                                                                    ciHitsEachValueL,xTickPeriod=1, xscale='linear')

    plt.setp([pline,plineL],lw=3)
    plt.setp([plineL,pcapsL,pbarsL,pdotsL],color=laserColor)
    plt.setp(pdotsL,mfc=laserColor)
    #plt.setp([plineL,pcapsL,pbarsL,pdotsL],visible=False)
    #plt.setp([pline,pcaps,pbars,pdots],visible=False)
    
    plt.xlabel('Stimulus',fontsize=fontsize)
    plt.ylabel('Rightward trials (%)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(plt.gca(),fontsize)

    plt.legend([pline,plineL],['Control','Laser'],loc='lower right')
    plt.title(subject)
    plt.show()

sys.exit()



'''
extraplots.save_figure('/tmp/bili002_laser','pdf',[5,5],outputDir='/tmp/')
extraplots.save_figure('/tmp/bili002_control','pdf',[5,5],outputDir='/tmp/')
'''
