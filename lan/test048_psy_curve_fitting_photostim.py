'''
Script to fit psychometric curves to data generated during photostim_freq_discri paradigm.
Lan Guo 20160720
'''

from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import colorpalette
from jaratoolbox import extraplots
#from jaratoolbox import extrastats
import numpy as np
import pypsignifit as psi
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

subjects = ['d1pi011']
if len(sys.argv)>1:
    sessions = sys.argv[1:]
FREQCOLORS = [colorpalette.TangoPalette['Chameleon3'],
              colorpalette.TangoPalette['ScarletRed1'],
              colorpalette.TangoPalette['SkyBlue2'] , 'g', 'm', 'k']    
nSessions = len(sessions)
nAnimals = len(subjects)
gs = gridspec.GridSpec(2*nAnimals,1)

for inda, thisAnimal in enumerate(subjects):
    allBehavDataThisAnimal = behavioranalysis.load_many_sessions(thisAnimal,sessions)
    targetFrequency = allBehavDataThisAnimal['targetFrequency']
    choice=allBehavDataThisAnimal['choice']
    valid=allBehavDataThisAnimal['valid']& (choice!=allBehavDataThisAnimal.labels['choice']['none'])
    choiceRight = choice==allBehavDataThisAnimal.labels['choice']['right']
    trialType = allBehavDataThisAnimal['trialType']
    stimTypes = [allBehavDataThisAnimal.labels['trialType']['no_laser'],allBehavDataThisAnimal.labels['trialType']['laser_left'],allBehavDataThisAnimal.labels['trialType']['laser_right']]
    
    stimLabels = ['no_laser','laser_left','laser_right']
    
    trialsEachType = behavioranalysis.find_trials_each_type(trialType,stimTypes)

    nConditions = len(stimTypes)
    fittedSessions=[]
    allPline = []
    curveLegends = []
    thisAnimalPos = inda
    ax1=plt.subplot(gs[thisAnimalPos,0])

    for stimType in range(nConditions):
        if np.any(trialsEachType[:,stimType]):
            targetFrequencyThisBlock = targetFrequency[trialsEachType[:,stimType]]    
            validThisBlock = valid[trialsEachType[:,stimType]]
            choiceRightThisBlock = choiceRight[trialsEachType[:,stimType]]
            
            (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
                                                                                                    behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)
            
            #plot psychometric curve
            (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                ciHitsEachValue,xTickPeriod=1)

            plt.setp((pline, pcaps, pbars), color=FREQCOLORS[stimType])
            plt.setp(pdots, mfc=FREQCOLORS[stimType], mec=FREQCOLORS[stimType])
            allPline.append(pline)
            curveLegends.append(stimLabels[stimType])

            ####fitting psychometric curve using BootstrapInference
            data = zip(possibleValues,nHitsEachValue,nTrialsEachValue)
            constraints=('flat','Uniform(0,0.3)' ,'Uniform(0,0.2)', 'Uniform(0,0.2)')
            ###parameters that may need to be optimized: priors,sigmoid and core functions
            session = psi.BootstrapInference(data,sample=True, priors=constraints, nafc=1, sigmoid='logistic', core='ab')
            fittedSessions.append(session)
    plt.hold(1)
    psi.psigniplot.plotMultiplePMFs(*fittedSessions)
    ax2=plt.subplot(gs[thisAnimalPos+1,0])
    for session in fittedSessions:
        #session.sample()
        psi.psigniplot.ParameterPlot(session)
        plt.hold(1)
    plt.show()
