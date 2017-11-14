'''
This will generate a database with the overall muscimol and saline psychometric curves for

WIP: I still need to figure out how to structure the data arrays

'''

import os
import figparams
import copy
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
import figparams
import numpy as np
from muscimol_sessions import animals
from jaratoolbox import extrastats

animalName = 'adap029'

FIGNAME = 'muscimol_inactivation'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
scriptFullPath = os.path.realpath(__file__)

def calculate_psychometric_and_estimate(bdata, fullDataPath):
    '''
    This wraps behavioranalysis.calculate_psychometric so that I can just give it the bdata
    Also calculates the psycurve estimate and saves the data at the end
    '''
    targetFrequency = bdata['targetFrequency']
    choice=bdata['choice']
    valid=bdata['valid'] & (choice!=bdata.labels['choice']['none'])
    choiceRight = choice==bdata.labels['choice']['right']
    possibleFreq = np.unique(targetFrequency)
    nFreq = len(possibleFreq)

    (possibleValues,
     fractionHitsEachValue,
     ciHitsEachValue,
     nTrialsEachValue,
     nHitsEachValue) = behavioranalysis.calculate_psychometric(choiceRight,
                                                               targetFrequency,
                                                               valid)

    #Calculate the estimate for the psychometric function
    logPossibleValues = np.log2(possibleValues)
    lowerFreqConstraint = logPossibleValues[1]
    upperFreqConstraint = logPossibleValues[-2]
    maxFreq = max(logPossibleValues)
    minFreq = min(logPossibleValues)

    constraints = ( 'Uniform({}, {})'.format(lowerFreqConstraint, upperFreqConstraint),
                    'Uniform(0,5)' ,
                    'Uniform(0,1)',
                    'Uniform(0,1)')
    estimate = extrastats.psychometric_fit(logPossibleValues,
                                           nTrialsEachValue,
                                           nHitsEachValue,
                                           constraints)

    np.savez(fullDataPath,
             possibleValues=possibleValues,
             fractionHitsEachValue=fractionHitsEachValue,
             ciHitsEachValue=ciHitsEachValue,
             nTrialsEachValue=nTrialsEachValue,
             nHitsEachValue=nHitsEachValue,
             logPossibleValues=logPossibleValues,
             estimate=estimate,
             script=scriptFullPath)
    print 'Saved results to {}'.format(fullDataPath)

animalSessionDict = animals[animalName]
for muscimolConc in ['muscimol00625', 'muscimol0125', 'muscimol0250']:
    musSessions = animalSessionDict[muscimolConc]
    musBdata = behavioranalysis.load_many_sessions([animalName], musSessions)
    musFilename = '{}_{}_psychometric.npz'.format(animalName, muscimolConc)
    musFullPath = os.path.join(outputDir,musFilename)
    calculate_psychometric_and_estimate(musBdata, musFullPath)

# salBdata = behavioranalysis.load_many_sessions([animalName], salSessions)
# salSessions = animalSessionDict['saline']
# salFilename = '{}_saline_psychometric.npz'.format(animalName)
# salFullPath = os.path.join(outputDir,salFilename)
# calculate_psychometric_and_estimate(salBdata, salFullPath)
