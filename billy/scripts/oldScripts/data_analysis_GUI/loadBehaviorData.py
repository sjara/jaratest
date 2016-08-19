'''
Example for loading behavior data with jaratoolbox
author: Billy Walker
'''

from jaratoolbox import loadbehavior
import numpy as np

correct = np.array
def loadBehavior(subject, sessionstr):
    ############################################################################################################################
    #PARAMETERS
    ############################################################################################################################
    experimenter = 'santiago'
    paradigm = '2afc'
    ############################################################################################################################

    behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,
                                                          paradigm,sessionstr)
    bdata = loadbehavior.BehaviorData(behaviorFilename)

    numberOfTrials = len(bdata['choice'])
    targetFrequencies = bdata['targetFrequency']

    #This gives an array of all frequencies presented
    possibleFreq = np.unique(bdata['targetFrequency'])

    #This gives an array with true and indices where the mouse made a correct decision
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    #This gives an array with true and indices where the mouse made a incorrect decision
    incorrect = bdata['outcome']==bdata.labels['outcome']['error']

    #This gives an array with true at indices of trials that are correct and went right
    rightward = bdata['choice']==bdata.labels['choice']['right']
    correctRightward = correct*rightward

    #This gives an array with true at indices of trials that are correct and went left
    leftward = bdata['choice']==bdata.labels['choice']['left']
    correctLeftward = correct*leftward

    #This gives an array with true at indices of trials that are incorrect and went right
    incorrectRightward = incorrect*rightward

    #This gives an array with true at indices of trials that are incorrect and went left
    incorrectLeftward = incorrect*leftward

    #This gives an array with true at indices of correct and incorrect (valid trials where a choice was made) trials only
    #trialsWithChoices = correct or incorrect
    
    return;


