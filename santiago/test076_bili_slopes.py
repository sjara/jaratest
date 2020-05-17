'''
Calculate slopes of bili mice across learning.
'''


import sys, os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
from jaratoolbox import extrastats
from jaratoolbox import settings 

paradigm = '2afc'

cohort1 = range(0,9)   # bili016-024

for inds,CASE in enumerate(cohort1):
    
    if CASE==0:
        subject = 'bili019'
        sessions = ['20190426a','20190427a','20190428a','20190429a','20190430a','20190501a','20190502a','20190503a','20190504a','20190505a','20190506a','20190507a','20190508a','20190509a','20190510a','20190511a','20190512a','20190513a','20190514a','20190515a','20190516a','20190517a','20190518a','20190519a','20190520a','20190521a','20190522a','20190523a','20190524a','20190525a','20190526a','20190527a','20190528a','20190529a','20190530a','20190531a','20190601a','20190602a','20190603a','20190604a','20190605a','20190606a','20190607a','20190608a','20190609a']
    elif CASE==1:
        subject = 'bili016'
        sessions = ['20190427a','20190428a','20190429a','20190430a','20190501a','20190502a','20190503a','20190504a','20190505a','20190506a','20190507a','20190508a','20190509a','20190510a','20190511a','20190512a','20190513a','20190514a','20190515a','20190516a','20190517a','20190518a','20190519a','20190520a','20190521a','20190522a','20190523a','20190524a','20190525a','20190526a','20190527a','20190528a','20190529a','20190530a','20190531a','20190601a','20190602a','20190603a','20190604a','20190605a','20190606a','20190607a','20190608a','20190609a']
    elif CASE==2:
        subject = 'bili017'
        sessions = ['20190428a','20190429a','20190430a','20190501a',   '20190503a','20190504a','20190505a','20190506a','20190507a','20190508a','20190509a','20190510a','20190511a','20190512a','20190513a','20190514a','20190515a','20190516a','20190517a','20190518a','20190519a','20190520a','20190521a','20190522a','20190523a','20190524a','20190525a','20190526a','20190527a','20190528a','20190529a','20190530a','20190531a','20190601a','20190602a','20190603a','20190604a','20190605a','20190606a','20190607a','20190608a','20190609a']
    elif CASE==3:
        subject = 'bili023'
        sessions = ['20190430a','20190501a','20190502a','20190503a','20190504a','20190505a','20190506a','20190507a','20190508a','20190509a','20190510a','20190511a','20190512a','20190513a','20190514a','20190515a','20190516a','20190517a','20190518a','20190519a','20190520a','20190521a','20190522a','20190523a','20190524a','20190525a','20190526a','20190527a','20190528a','20190530a','20190531a','20190601a','20190602a','20190603a','20190604a','20190605a','20190606a','20190607a','20190608a','20190609a']
        # Corrupted: '20190529a'
    elif CASE==4:
        subject = 'bili022'
        sessions = ['20190501a','20190502a','20190503a','20190504a','20190505a','20190506a','20190507a','20190508a','20190509a','20190510a','20190511a','20190512a','20190513a','20190514a','20190515a','20190516a','20190517a','20190518a','20190519a','20190520a','20190521a','20190522a','20190523a','20190524a','20190525a','20190526a','20190527a','20190528a','20190529a','20190530a','20190531a','20190601a','20190602a','20190603a','20190604a','20190605a','20190606a','20190607a','20190608a','20190609a']
    elif CASE==5:
        subject = 'bili018'
        sessions = ['20190503a','20190504a','20190505a','20190506a','20190507a','20190508a','20190509a','20190510a','20190511a','20190512a','20190513a','20190514a','20190515a','20190516a','20190517a','20190518a','20190519a','20190520a','20190521a','20190522a','20190523a','20190524a','20190525a','20190526a','20190527a','20190528a','20190529a','20190530a','20190531a','20190601a','20190602a','20190603a','20190604a','20190605a','20190606a','20190607a','20190608a','20190609a']
    elif CASE==6:
        subject = 'bili021'
        sessions = ['20190507a','20190508a','20190509a','20190510a','20190511a','20190512a','20190513a','20190514a','20190515a','20190516a','20190517a','20190518a','20190519a','20190520a','20190521a','20190522a','20190523a','20190524a','20190525a','20190526a','20190527a','20190528a','20190529a','20190530a','20190531a','20190601a','20190602a','20190603a','20190604a','20190605a','20190606a','20190607a','20190608a','20190609a']
    elif CASE==7:
        subject = 'bili024'
        sessions = ['20190513a','20190514a','20190515a','20190516a','20190517a','20190518a','20190519a','20190520a','20190521a','20190522a','20190523a','20190524a','20190525a','20190526a','20190527a','20190528a','20190529a','20190530a','20190531a','20190601a','20190602a','20190603a','20190604a','20190605a','20190606a','20190607a','20190608a','20190609a']
    elif CASE==8:
        subject = 'bili020'
        sessions = ['20190517a','20190518a','20190519a','20190520a','20190521a','20190522a','20190523a','20190524a','20190525a','20190526a','20190527a','20190528a','20190529a','20190530a','20190531a','20190601a','20190602a','20190603a','20190604a','20190605a','20190606a','20190607a','20190608a','20190609a']

        
    nSessions = len(sessions)
    curveParamsEachSession = np.empty((4,nSessions))

    for inds,session in enumerate(sessions):

        behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
        bdata = loadbehavior.BehaviorData(behavFile)

        targetPercentage = bdata['targetPercentage']
        choice = bdata['choice']
        valid = bdata['valid'] & (bdata['choice']!=bdata.labels['choice']['none'])
        choiceRight = choice==bdata.labels['choice']['right']

        possibleStimValues = np.unique(targetPercentage)

        # -- Calculate and plot psychometric fit --
        (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
            behavioranalysis.calculate_psychometric(choiceRight,targetPercentage,valid)

        constraints = ['flat','Uniform(6,100)','flat','flat']
        #constraints = ['flat','flat','flat','flat']
        curveParams = extrastats.psychometric_fit(possibleValues, nTrialsEachValue,
                                                  nHitsEachValue, constraints)

        curveParamsEachSession[:,inds] = curveParams
        
        slope = 1/curveParams[1]
        print('{}  Slope: {}'.format(session,slope))

        if 1:#slope>0.2:
            plt.clf()
            xValues = possibleValues
            yValues = nHitsEachValue.astype(float)/nTrialsEachValue
            yOffsetFactor = 0.1
            xRange = xValues[-1]-xValues[1]
            fitxval = np.linspace(xValues[0]-yOffsetFactor*xRange,xValues[-1]+yOffsetFactor*xRange,40)
            fityval = extrastats.psychfun(fitxval,*curveParams)
            hfit = plt.plot(fitxval,100*fityval,'-',linewidth=2,color='k')
            hdots = plt.plot(xValues,100*yValues,'o',mew=1,markersize=6,mfc='none',mec='k')
            plt.xlim([-10,110])
            plt.ylim([-10,110])
            plt.xlabel('Stim percentage')
            plt.ylabel('Rightward choices (%)')
            plt.title('{} - {}'.format(subject,session))
            plt.show()
            #plt.waitforbuttonpress()
            plt.pause(0.1)

    outputFilename = os.path.join('/tmp/','psycurve_{}.npz'.format(subject))
    print('Saving to {}'.format(outputFilename))
    np.savez(outputFilename,curveParamsEachSession=curveParamsEachSession,script=__file__)
    
# bili017       
#20190514a  0.340479420449
#20190528a  1.12538731075

# plot(1/curveParamsEachSession[1,:],'o-')
# sp = 1/curveParamsEachSession[1,:]; plot(sp[sp>0.02],'o-')

