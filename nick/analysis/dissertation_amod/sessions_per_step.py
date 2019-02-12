import os
import numpy as np
from jaratoolbox import settings
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
from matplotlib import pyplot as plt

'''
Behavior steps:
0: Sides direct AM
1: Direct AM
2: Next correct AM
3: If correct AM
4: AM psychometric
5: If correct Tones
6: Tones psychometric
7: If correct Mixed tones
8: Mixed tones psychometric
'''

ytickInds = range(9)
ytickLabels = ['SD AM', 'D AM', 'NC AM', 'IC AM', 'P AM', 'IC F', 'P F', 'IC M', 'P M']

#Amod animals 001 through 014
subjects = ['amod{:03d}'.format(i) for i in range(1, 15)]

def behavior_step(sessionData):
    '''
    Calculate the training step given a bdata object
    '''
    outcomeMode = sessionData.labels['outcomeMode'][sessionData['outcomeMode'][0]]
    soundTypeMode = sessionData.labels['soundTypeMode'][sessionData['soundTypeMode'][0]]
    psycurveMode = sessionData.labels['psycurveMode'][sessionData['psycurveMode'][0]]
    if outcomeMode == 'sides_direct':
        assert soundTypeMode == 'amp_mod'
        step = 0
    elif outcomeMode == 'direct':
        assert soundTypeMode == 'amp_mod'
        step = 1
    elif outcomeMode == 'on_next_correct':
        assert soundTypeMode == 'amp_mod'
        step = 2
    elif outcomeMode == 'only_if_correct':
        if soundTypeMode == 'amp_mod':
            if psycurveMode == 'off':
                step=3
            elif psycurveMode == 'uniform':
                step=4
            else:
                raise AttributeError('Psycurve mode not listed: {}'.format(psycurveMode))
        elif soundTypeMode in ['tones', 'chords']:
            if psycurveMode == 'off':
                step=5
            elif psycurveMode == 'uniform':
                step=6
            else:
                raise AttributeError('Psycurve mode not listed: {}'.format(psycurveMode))
        elif soundTypeMode in ['mixed_tones', 'mixed_chords']:
            if psycurveMode == 'off':
                step=7
            elif psycurveMode == 'uniform':
                step=8
            else:
                raise AttributeError('Psycurve mode not listed: {}'.format(psycurveMode))
        else:
            raise AttributeError('Sound mode not listed: {}'.format(soundTypeMode))
    else:
        raise AttributeError('Outcome mode not listed: {}'.format(outcomeMode))
    return step

subjects = ['amod007', 'amod008', 'amod009', 'amod010', 'amod011', 'amod012', 'amod013', 'amod014']
stepArrays = []
trialNumArrays = []
for subject in subjects:
    dataDir = os.path.join(settings.BEHAVIOR_PATH, subject)
    sessions = sorted(os.listdir(dataDir))
    trainingSteps = np.empty(len(sessions))
    trialStartEachSession = np.empty(len(sessions))
    trials = 0
    for indSession, sessionFn in enumerate(sessions):
        sessionFullPath = os.path.join(dataDir, sessionFn)
        try:
            bdata = loadbehavior.BehaviorData(sessionFullPath)
        except KeyError:
            print "Key Error with session: {}".format(sessionFullPath)
        step = behavior_step(bdata)
        trialStartEachSession[indSession] = trials
        trainingSteps[indSession] = step
        trials += len(bdata['valid']) #Using total length, not just valid trials
    stepArrays.append(trainingSteps)
    trialNumArrays.append(trialStartEachSession)

plt.clf()
for indArray, stepArray in enumerate(stepArrays):
    changePointsToShow = np.concatenate([np.array([True]), np.diff(stepArray)==1])
    plt.plot(trialNumArrays[indArray][changePointsToShow],
             stepArray[changePointsToShow], '-o')
ax = plt.gca()
ax.set_yticks(ytickInds)
ax.set_yticklabels(ytickLabels)
ax.set_xlabel('Number of trials')
plt.show()
