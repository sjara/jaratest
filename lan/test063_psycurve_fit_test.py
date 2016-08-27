'''
Fitting psychometric curve.
'''
import numpy as np
from jaratoolbox import extrastats
from jaratoolbox import extraplots
reload(extraplots)
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt
import pypsignifit as psi
from jaratoolbox import colorpalette

FREQCOLORS = [colorpalette.TangoPalette['Chameleon3'],
                  colorpalette.TangoPalette['ScarletRed1'],
                  colorpalette.TangoPalette['SkyBlue2'] , 'g', 'm', 'k']

animal = 'd1pi015'
sessions = ['20160804a']

#behavFile = loadbehavior.path_to_behavior_data(subject,'2afc',session)
#bdata = loadbehavior.BehaviorData(behavFile)
bdata = behavioranalysis.load_many_sessions(animal,sessions)
targetFrequency=bdata['targetFrequency']
choice=bdata['choice']
valid=bdata['valid'] & (choice!=bdata.labels['choice']['none'])
choiceRight = choice==bdata.labels['choice']['right']

trialType = bdata['trialType']
stimTypes = [bdata.labels['trialType']['no_laser'],bdata.labels['trialType']['laser_left'],bdata.labels['trialType']['laser_right']]
stimLabels = ['no_laser','laser_left','laser_right']
trialsEachType = behavioranalysis.find_trials_each_type(trialType,stimTypes)

nStimTypes = len(stimTypes)
for stimType in range(nStimTypes):
    if np.any(trialsEachType[:,stimType]):
        targetFrequencyThisBlock = targetFrequency[trialsEachType[:,stimType]]    
        validThisBlock = valid[trialsEachType[:,stimType]]
        choiceRightThisBlock = choiceRight[trialsEachType[:,stimType]]
        # -- Calculate and plot psychometric points --
        (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
    behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)

        logPossibleValues = np.log2(possibleValues)

        #plt.clf()


        #(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(possibleValues,fractionHitsEachValue,ciHitsEachValue)
        plt.plot(logPossibleValues,fractionHitsEachValue,color=FREQCOLORS[stimType])
        #plt.setp(pdots,ms=6,mec='k',mew=2,mfc='k')
        plt.xlabel('Frequency (log_Hz)')
        plt.ylabel('Rightward choice (%)')
        plt.hold(True)
        


    # -- Calculate and plot psychometric fit --
        constraints = None
        #constraints = ['flat', 'Uniform(0,0.3)' ,'Uniform(0,0.2)', 'Uniform(0,0.2)']
        #constraints = ['Uniform({},{})'.format(logPossibleValues[0],logPossibleValues[-1]), 'unconstrained' ,'Uniform(0,0.2)', 'Uniform(0,0.2)']
        #curveParams = extrastats.psychometric_fit(possibleValues,nTrialsEachValue, nHitsEachValue)
        

        # -- Fit psy curve with psi.BoostrapInference object -- #

        data = np.c_[logPossibleValues,nHitsEachValue,nTrialsEachValue]

        # linear core 'ab': (x-a)/b; logistic sigmoid: 1/(1+np.exp(-(xval-alpha)/beta))
        psyCurveInference = psi.BootstrapInference(data,sample=False, sigmoid='logistic', core='ab',priors=constraints, nafc=1)

        curveParams = psyCurveInference.estimate
        deviance = psyCurveInference.deviance
        predicted = psyCurveInference.predicted

        xValues = logPossibleValues
        xRange = xValues[-1]-xValues[1]
        fitxval = np.linspace(xValues[0]-0.1*xRange,xValues[-1]+0.1*xRange,40)
        fityval = psyCurveInference.evaluate(x=fitxval)
        #fityval = extrastats.psychfun(fitxval,*curveParams)
        hfit = plt.plot(fitxval, fityval, '-', linewidth=2, color=FREQCOLORS[stimType])
        plt.plot(logPossibleValues, predicted,'^',color=FREQCOLORS[stimType])
        plt.hold(True)
        plt.draw()
plt.show()
