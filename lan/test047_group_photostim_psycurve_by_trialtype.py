'''
Script to load many behavior sessions and generate summary(average) psychometric curve for photostim_freq_discri paradigm by trialType.
Lan Guo 20160608
'''
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#from jaratest.lan import behavioranalysis_vlan as behavioranalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import colorpalette



def plot_ave_photostim_psycurve_by_trialtype(animal,sessions,trialLimit=None):
    '''
    Arguments:
    animal is a string of the animal name you want to plot.
    sessions is a list of strings of the behavior session names you want to plot.
    trialLimit is an optional parameter, should be a list of integers giving the beginning and end of trials numbers you want to plot.
    '''

    FREQCOLORS = [colorpalette.TangoPalette['Chameleon3'],
                  colorpalette.TangoPalette['ScarletRed1'],
                  colorpalette.TangoPalette['SkyBlue2'] , 'g', 'm', 'k']

    allBehavDataThisAnimal = behavioranalysis.load_many_sessions(animal,sessions)
    targetFrequency = allBehavDataThisAnimal['targetFrequency']
    choice=allBehavDataThisAnimal['choice']
    valid=allBehavDataThisAnimal['valid']& (choice!=allBehavDataThisAnimal.labels['choice']['none'])
    if trialLimit:
        trialSelector = np.zeros(len(valid),dtype=bool)
        trialSelector[trialLimit[0]:trialLimit[1]] = True
    else:
        trialSelector = np.ones(len(valid),dtype=bool)
    valid = (valid & trialSelector)
    #print sum(trialSelector), sum(valid)
    
    choiceRight = choice==allBehavDataThisAnimal.labels['choice']['right']
    trialType = allBehavDataThisAnimal['trialType']
    stimTypes = [allBehavDataThisAnimal.labels['trialType']['no_laser'],allBehavDataThisAnimal.labels['trialType']['laser_left'],allBehavDataThisAnimal.labels['trialType']['laser_right']]
    
    stimLabels = ['no_laser','laser_left','laser_right']
    
    trialsEachType = behavioranalysis.find_trials_each_type(trialType,stimTypes)
    #trialsEachType=np.vstack(( ( (trialType==0) | (trialType==2) ),trialType==1, np.zeros(len(trialType),dtype=bool) )).T  ###This is a hack when percentLaserTrials were sum of both sides and just did one side stim
    #print trialsEachType
    
    nBlocks = len(stimTypes)
    #thisAnimalPos = inda
    #ax1=plt.subplot(gs[thisAnimalPos,0])
    #ax1=plt.subplot(gs[thisAnimalPos])
    
    #plt.figure()
    fontsize = 8
    allPline = []
    curveLegends = []
    for stimType in range(nBlocks):
        if np.any(trialsEachType[:,stimType]):
            targetFrequencyThisBlock = targetFrequency[trialsEachType[:,stimType]]    
            validThisBlock = valid[trialsEachType[:,stimType]]
            #print len(validThisBlock), sum(validThisBlock)
            choiceRightThisBlock = choiceRight[trialsEachType[:,stimType]]
            numValidTrialThisBlock = sum(validThisBlock)
            (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
                                                                                                    behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)
            (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                ciHitsEachValue,xTickPeriod=1)

            plt.setp((pline, pcaps, pbars), color=FREQCOLORS[stimType])
            plt.hold(True)
            plt.setp(pdots, mfc=FREQCOLORS[stimType], mec=FREQCOLORS[stimType])
            plt.hold(True)
            plt.annotate('%s: %s trials'%(stimLabels[stimType],numValidTrialThisBlock), xy=(0.2, 0.35+stimType/10.0), fontsize=fontsize, xycoords='axes fraction')
            allPline.append(pline)
            curveLegends.append(stimLabels[stimType])
            #plt.hold(True)
    plt.xlabel('Frequency (kHz)',fontsize=fontsize)
    plt.ylabel('Rightward trials (%)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(plt.gca(),fontsize)
    legend = plt.legend(allPline,curveLegends,loc='best',labelspacing=0.2,prop={'size':4})
    # Add the legend manually to the current Axes.
    #ax = plt.gca().add_artist(legend)
    plt.gca().add_artist(legend)
    
    #plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
    #plt.show()
    if len(sessions)==1:
        plt.title('%s_%s' %(animal,sessions[0]),fontsize=fontsize)
    else:
        plt.title('%s_%sto%s'%(animal,sessions[0],sessions[-1]),fontsize=fontsize)   
    plt.show()
    '''
    #######Plot dynamics and laser trials##############
    ax2=plt.subplot(gs[thisAnimalPos,1:])
    lineWidth = 2
    #freqsToUse=np.unique(targetFrequency)[2:4] ##HARD-CODED:take the middle freqs out of the 6 freqs used 
    behavioranalysis.plot_dynamics(allBehavDataThisAnimal,winsize=10,soundfreq=None)
    for stimType in range(1,nBlocks):
        if np.any(trialsEachType[:,stimType]):
            validTrialIndex=np.nonzero(valid)[0]
            stimTrialIndex=np.nonzero((valid&trialsEachType[:,stimType]))[0]
            stimTrials=np.in1d(validTrialIndex, stimTrialIndex)
            stimTrials=np.nonzero(stimTrials)[0]
            
            ax2.vlines(stimTrials,0,100,alpha=0.2,linestyles='solid')
    '''  
def save_figure(animal,sessions,figformat='png'):
    outputDir='/home/languo/data/behavior_reports' 
    animalStr = animal
    sessionStr = '-'.join(sessions)
    #plt.gcf().set_size_inches((8.5,11))
    #figformat = 'png' 
    filename = 'behavior_summary_%s_%s.%s'%(animalStr,sessionStr,figformat)
    fullFileName = os.path.join(outputDir,filename)
    print 'saving figure to %s'%fullFileName
    plt.gcf().savefig(fullFileName,format=figformat)


def psychometric_fit(xValues, nTrials, nHits, constraints=None, alpha=0.05):
    '''
    Function moved from jaratoolbox/extrastats.py
    Given performance for each value of parameter, estimate the curve.
    This function uses psignifit (BootstrapInference)
    
    xValues: 1-D array of size M #Numbers of frequencies
    nHits:   1-D array of size M #Nnumber of hits each frequency
    nTrials: 1-D array of size M #Nnumber of trials each frequency
    
    Returns 4 values:
    '''
    import pypsignifit as psi

    if constraints is None:
        constraints = ( 'flat', 'Uniform(0,0.3)' ,'Uniform(0,0.2)', 'Uniform(0,0.2)')
    data = np.c_[xValues,nHits,nTrials]
    session = psi.BootstrapInference(data,sample=False, priors=constraints, nafc=1)
    # session = psi.BayesInference(data,sample=False,priors=constraints,nafc=1)
    # (pHit,confIntervals) = binofit(nHits,nTrials,alpha)
    # return (session.estimate,pHit,confIntervals)
    return session.estimate


def psychfun(xval,alpha,beta,lamb,gamma):
    '''Psychometric function that allowing arbitrary asymptotes.
    alpha: bias
    beta : related to slope
    lamb : lapse term (up)
    gamma: lapse term (down)
    '''
    #return gamma + (1-gamma-lamb)*weibull(xval,alpha,beta)
    #return gamma + (1-gamma-lamb)*gaussianCDF(xval,alpha,beta)
    return gamma + (1-gamma-lamb)*logistic(xval,alpha,beta)


if __name__ == '__main__':
    animals = ['adap048','adap056']

    if len(sys.argv)>1:
        sessions = sys.argv[1:]

    #nSessions = len(sessions)
    #nAnimals = len(subjects)
    #gs = gridspec.GridSpec(nAnimals, 3)
    #gs = gridspec.GridSpec(nAnimals,1)
    #gs.update(hspace=0.5,wspace=0.4)

    for inda, thisAnimal in enumerate(animals):
        plt.figure()
        plot_ave_photostim_psycurve_by_trialtype(thisAnimal,sessions)
        save_figure(thisAnimal,sessions)
