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
performanceArrays = dataZ['performanceArrays']


def find_change_points(stepArray):
    '''
    Find the index of the session where training steps were first acheived.

    Args:
        stepArray (arr): Array of length nSessions with the step of each session

    Returns:
        stepList (list): List of each step acheived across the training of the animal
        indList (list): List of the index in stepArray where the step was first acheived
    '''

    #Lists to hold the step that was acheived,
    #and the index of the session when it was acheived

    stepList = []
    indList = []

    for indStep, stepNum in enumerate(stepArray):
        if indStep==0:
            #Animal changed to step 0 at index 0
            stepList.append(0)
            indList.append(0)
        else:
            stepDiff = stepArray[indStep] - stepArray[indStep-1]
            if stepDiff == 0:
                #Same step as before, do nothing
                pass
            elif stepDiff >= 1:
                #These can be the change points if they are real
                #Have to check if it was a single session problem
                if stepArray[indStep] == stepArray[indStep+1]:
                    #Still the same step tomorrow, treat as a change point
                    stepList.append(stepNum)
                    indList.append(indStep)
                else:
                    #We are going to ignore this because it was likely a bad session.
                    pass
            elif stepDiff < 0:
                #We are going down in the steps, ignore it.
                pass

    return stepList, indList

def find_ready_for_experiment(stepArray, percentCorrectArray, stepList, indList,
                              thresh=0.75):
    '''
    Determine when an animal reached the final stage of being ready to start an experiment.

    Args:
        stepArray (arr): Array of length nSessions with the step of each session
        percentCorrectArray (arr): Array of length nSessions with percent correct
        stepList (list): List of each step acheived across the training of the animal
        indList (list): List of the index in stepArray where the step was first acheived

    Returns:
        stepList (list): List of steps acheived with the final step added (if acheived)
        indList (list): List of the index in stepArray where the step was acheived
    '''

    #The change point to the final step (step 8, not yet considering 'ready for experiment')
    finalStep = np.max(stepList)
    indsFinalStep = np.flatnonzero(stepArray==finalStep)

    done = False
    failed = False
    indI = 2
    while not done:
        try:
            perfThisRange = percentCorrectArray[indsFinalStep[indI]-2:indsFinalStep[indI]+1]
        except IndexError:
            #This animal was never ready to complete the experiment
            failed = True
            break
        if np.all(perfThisRange >= thresh):
            done=True
        else:
            indI+=1

    if not failed:
        indFinished = indsFinalStep[indI]
        stepList.append(9)
        indList.append(indFinished)

    return stepList, indList

def make_step_trace(stepArray, stepList, indList):
    '''
    Construct a trace to plot, showing progression through steps.

    Args:
        stepArray (arr): Array of length nSessions with the step of each session
        stepList (list): List of each step acheived across the training of the animal
        indList (list): List of the index in stepArray where the step was first acheived

    Returns:
        stepTrace (arr): Array of length nSessions with the current highest acheived step.
    '''
    stepTrace = np.empty(len(stepArray))
    for indStep, step in enumerate(stepList):
        start = indList[indStep]
        if indStep < len(stepList)-1:
            #If we aren't on the last step, we find the end point
            stop = indList[indStep+1]
            stepTrace[start:stop] = step
        else:
            #Otherwise, we just go to the end
            stepTrace[start:] = step
    return stepTrace


def get_colors(nColors):
    '''
    Returns n colors from the matplotlib rainbow colormap.
    '''
    from matplotlib.pyplot import cm
    colors = cm.rainbow(np.linspace(0, 1, nColors))
    return colors


def test_find_change_points():
    input = np.array([0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 2, 3, 3, 3])
    output = np.array([1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0])
    assert np.all(find_change_points(input) == output)

ytickLabels = ['SD AM', 'D AM', 'NC AM', 'IC AM', 'P AM', 'IC F', 'P F', 'IC M', 'P M', 'R']
ytickInds = range(len(ytickLabels))

plt.clf()

colors = get_colors(len(subjects))
maxJitter = 0.3
increment = (maxJitter*2)/len(subjects)
lineJitter = np.arange(start=-maxJitter, stop=maxJitter+increment, step=increment)
lw = 2

axSessions = plt.subplot(211)
axTrials = plt.subplot(212)


for indArray in range(len(subjects)):
    mouseColor = colors[indArray]
    stepArray = stepArrays[indArray]
    percentCorrectArray = performanceArrays[indArray]
    stepArrayNN = stepArray[stepArray>=0] #Remove -1s
    percentCorrectArrayNN = percentCorrectArray[stepArray>=0]
    trialNumArray = trialNumArrays[indArray]
    trialNumArrayNN = trialNumArray[stepArray>=0]
    assert len(stepArrayNN)==len(trialNumArrayNN)

    #The main pipeline for producing the trace to plot
    stepList, indList = find_change_points(stepArrayNN)
    stepListFinal, indListFinal = find_ready_for_experiment(stepArrayNN,
                                                            percentCorrectArrayNN,
                                                            stepList,
                                                            indList)
    traceToPlot = make_step_trace(stepArrayNN, stepListFinal, indListFinal)

    traceToPlot = traceToPlot+lineJitter[indArray]

    if max(stepListFinal)==9: #The animal actually reached the ready stage
        readyInd = indListFinal[-1]
        trialNumArrayTruncated = trialNumArrayNN[:readyInd+1]
        traceToPlotTruncated = traceToPlot[:readyInd+1]
        axTrials.plot(trialNumArrayTruncated, traceToPlotTruncated,
                      '-', color=mouseColor)
        axSessions.plot(range(len(traceToPlotTruncated)),
                              traceToPlotTruncated, '-', color=mouseColor)
        axTrials.plot(trialNumArrayTruncated[readyInd],
                      traceToPlotTruncated[readyInd],'o', color=mouseColor,
                      label=subjects[indArray])
        axSessions.plot(readyInd, traceToPlotTruncated[readyInd],
                        'o', color=mouseColor)

    else:
        axTrials.plot(trialNumArrayNN, traceToPlot,'-', color=mouseColor,
                      label=subjects[indArray])
        axSessions.plot(range(len(traceToPlot)), traceToPlot, '-', color=mouseColor)
for ax in [axSessions, axTrials]:
    ax.set_yticks(ytickInds)
    ax.set_yticklabels(ytickLabels)
    extraplots.boxoff(ax)
axTrials.set_xlabel('Number of trials')
axSessions.set_xlabel('Number of sessions')
plt.legend(ncol=2, frameon=False)
plt.show()
plt.savefig('/home/nick/data/dissertation_amod/figure_training_time.png')
