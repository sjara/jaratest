import numpy as np
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
9: Ready for experiment
'''

#Get the data
dataFn = '/home/nick/data/dissertation_amod/sessions_per_step.npz'
dataZ = np.load(dataFn)

subjects = dataZ['subjects']
stepArrays = dataZ['stepArrays']
trialNumArrays = dataZ['trialNumArrays']

def find_change_points(stepArray):
    '''
    Find the session where the animal was advanced to the next step.
    For advancement to the final step, consecutive days at criterion
    are required.

    Args:
        stepArray (np.array): Array of length nSessions, containing training step.
        finalStepDays (int): Number of required consecutive days at final step.
        FIXME: This only works for finalStepDays = 3 for now

    Returns:
        changePoints (np.array): Array of length nSession - True if the session
                                 was a change point, and False otherwise.
    '''

    uniqueSteps = np.unique(stepArray)
    changePointEachStep = np.empty(len(uniqueSteps))

    for indStep, thisStep in enumerate(uniqueSteps):
        if indStep != len(uniqueSteps)-1: #Not the last step
            if indStep == 0: #If first step, change needs to be 0
                changePointEachStep[indStep] = 0
            else:
                indsThisStep = np.flatnonzero(stepArray==thisStep)
                #Only show jumps of 1 - all other things must be mistake sessions
                done = False
                indI = 0
                while not done:
                    if stepArray[indsThisStep[indI]] - stepArray[indsThisStep[indI]-1] == 1:
                        done = True
                        indToUse = indsThisStep[indI]
                    else:
                        indI += 1
                changePointEachStep[indStep] = indToUse

        else:
            indsThisStep = np.flatnonzero(stepArray==thisStep)
            done = False
            indI = 0
            while not done:
                if np.all(np.diff(indsThisStep[indI:indI+3]) == np.array([1, 1])):
                    done=True
                else:
                    indI+=1

    changePointEachStep[indStep] = indsThisStep[indI]
    changePoints = np.zeros(len(stepArray))
    changePoints[changePointEachStep.astype(int)] = 1
    return changePoints.astype(bool)

def test_find_change_points():
    input = np.array([0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 2, 3, 3, 3])
    output = np.array([1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0])
    assert np.all(find_change_points(input) == output)

ytickLabels = ['SD AM', 'D AM', 'NC AM', 'IC AM', 'P AM', 'IC F', 'P F', 'IC M', 'P M', 'R']
ytickInds = range(len(ytickLabels))

plt.clf()
for indArray in range(len(subjects)):
    stepArray = stepArrays[indArray]
    stepArrayNN = stepArray[stepArray>=0] #Remove -1s
    trialNumArray = trialNumArrays[indArray]
    trialNumArrayNN = trialNumArray[stepArray>=0]
    assert len(stepArrayNN)==len(trialNumArrayNN)

    # changePointsToShow = np.concatenate([np.array([True]), np.diff(stepArray)==1])
    try:
        changePointsToShow = find_change_points(stepArrayNN)
    except IndexError: #FIXME: Some animals have messed up progressions.
        print "Failure for animal {}".format(subjects[indArray])
    plt.plot(trialNumArrayNN[changePointsToShow],
                stepArrayNN[changePointsToShow], '-o')

ax = plt.gca()
ax.set_yticks(ytickInds)
ax.set_yticklabels(ytickLabels)
ax.set_xlabel('Number of trials')
plt.show()

#FIXME: Why do some animals not get all the way to the top?
#FIXME: Why do the plots go 7 9 8 at the end? 
