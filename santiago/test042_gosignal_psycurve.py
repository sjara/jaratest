'''
Behavior analysis for go-signal mice.
'''

import numpy as np
from jaratoolbox import extraplots
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt
import sys
import matplotlib.pyplot as plt

#subject = sys.argv[1]
session = sys.argv[1]

animalList = ['gosi006','gosi010','gosi012']
'''
animalList = ['gosi001','gosi002','gosi003','gosi004','gosi005',
              'gosi006','gosi007','gosi008','gosi009','gosi010',
              'gosi011','gosi012','gosi013','gosi014','gosi015']
'''

nValidAll = []
fractionValidAll = []
fractionCorrectAll = []

plt.clf()
nSubjects = len(animalList)

for inds,subject in enumerate(animalList):
    behavFile = loadbehavior.path_to_behavior_data(subject,'2afc',session)
    bdata = loadbehavior.BehaviorData(behavFile)

    delayToTargetMean = bdata['delayToTargetMean'][-1]
    delayToTargetHalfRange = bdata['delayToTargetHalfRange'][-1]
    targetDuration = bdata['targetDuration'][-1]
    delayToGoSignal = bdata['delayToGoSignal'][-1]
    
    targetFrequency = bdata['targetFrequency']
    choice = bdata['choice']
    valid = bdata['valid'] & (choice!=bdata.labels['choice']['none'])
    choiceRight = (choice==bdata.labels['choice']['right'])
    outcome = bdata['outcome']
    validCorrect = outcome[valid.astype(bool)]==bdata.labels['outcome']['correct']

    nValid = np.sum(valid)
    fractionValid = np.mean(valid)
    fractionCorrect = np.mean(validCorrect)

    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
                           behavioranalysis.calculate_psychometric(choiceRight,targetFrequency,valid)

    nValidAll.append(nValid)
    fractionValidAll.append(fractionValid)
    fractionCorrectAll.append(fractionCorrect)

    plt.subplot(nSubjects//2+1,2,inds+1)
    # -- plot things here --
    (plineC, pcapsC, pbarsC, pdotsC) = extraplots.plot_psychometric(possibleValues,
                                                                    fractionHitsEachValue,
                                                                    ciHitsEachValue)
    #plt.ylabel('{0}'.format(animalList[inds]))
    plt.ylabel('Trials rightward (%)')
    #plt.xlim([-0.1,0.8])
    plt.xlabel('Frequency (Hz)')

    
    #if inds==0:
    plt.title('[{0}] Delay-to-go = {1:0.2}s'.format(animalList[inds],delayToGoSignal))
    plt.draw()
    plt.show()


