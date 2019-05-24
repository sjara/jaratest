#Need to show what effect muscimol has on discriminations of one sound type at a time, to address whether the switching component of the task adds an additional layer of cortical dependence.
import numpy as np
import os
import copy
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import extrastats
from jaratest.nick.behavior import soundtypes

scriptFullPath = os.path.realpath(__file__)

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
             estimate=estimate,
             script=scriptFullPath)
    print 'Saved results to {}'.format(fullDataPath)

saveDir = '/home/nick/data/dissertation_amod/'


# AM only

sessions = {'amod001':['20160316a', '20160317a', '20160318a', '20160319a',
                       '20160320a', '20160321a', '20160322a', '20160323a'],
            'amod005':['20160316a', '20160317a', '20160318a', '20160319a',
                       '20160320a', '20160321a', '20160322a', '20160323a']}
muscimol = {'amod001':[0, 1, 0, 1, 0, 1, 0, 1],
            'amod005':[0, 1, 0, 1, 0, 1, 0, 1]}

salineSessions = {animal: [session for session, mus in zip(sessions[animal], muscimol[animal]) if mus==0] for animal in sessions.keys()}
muscimolSessions = {animal: [session for session, mus in zip(sessions[animal], muscimol[animal]) if mus==1] for animal in sessions.keys()}

for subject in ['amod001', 'amod005']:
    salineThisSubject = salineSessions[subject]
    muscimolThisSubject = muscimolSessions[subject]

    bdata = behavioranalysis.load_many_sessions(subject, salineThisSubject)
    dataFn ='am_psychometric_{}_saline.npz'.format(subject)
    print 'Saving: {}'.format(dataFn)
    dataPath = os.path.join(saveDir, dataFn)
    calculate_psychometric_and_estimate(bdata, dataPath)

    # Muscimol Data
    bdata = behavioranalysis.load_many_sessions(subject, muscimolThisSubject)
    dataFn ='am_psychometric_{}_muscimol.npz'.format(subject)
    print 'Saving: {}'.format(dataFn)
    dataPath = os.path.join(saveDir, dataFn)
    calculate_psychometric_and_estimate(bdata, dataPath)
