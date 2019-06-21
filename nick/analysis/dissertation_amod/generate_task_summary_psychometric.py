
import numpy as np
import os
import copy
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import extrastats
from jaratest.nick.behavior import soundtypes

# scriptFullPath = os.path.realpath(__file__)

def calculate_psychometric_and_estimate(bdata, fullDataPath):
    '''
    Calculates psychometric from bdata and estimates fit
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
             estimate=estimate)
    print 'Saved results to {}'.format(fullDataPath)

saveDir = '/home/nick/data/dissertation_amod/'

# muscimolSessions = ['20160413a', '20160415a', '20160417a', '20160419a', '20160421a']
salineSessions = ['20160412a', '20160414a', '20160416a', '20160418a', '20160420a']
animal = 'amod002'
# animal = 'amod003'

# animal = 'amod004'
# muscimolSessions = ['20160427a', '20160429a', '20160501a', '20160503a', '20160505a', '20160507a', '20160509a']
# salineSessions = ['20160426a', '20160428a', '20160430a', '20160502a', '20160504a', '20160506a', '20160508a']

# Saline Data
salDataObjs, salSoundTypes = soundtypes.load_behavior_sessions_sound_type(animal, salineSessions)
for soundType, stInd in salSoundTypes.iteritems():
    dataFn ='task_psychometric_{}_{}_saline.npz'.format(animal, soundType)
    dataPath = os.path.join(saveDir, dataFn)
    calculate_psychometric_and_estimate(salDataObjs[stInd], dataPath)

# Muscimol Data
# musDataObjs, musSoundTypes = soundtypes.load_behavior_sessions_sound_type(animal, muscimolSessions)
# for soundType, stInd in musSoundTypes.iteritems():
#     dataFn ='task_psychometric_{}_{}_muscimol.npz'.format(animal, soundType)
#     dataPath = os.path.join(saveDir, dataFn)
#     calculate_psychometric_and_estimate(musDataObjs[stInd], dataPath)

