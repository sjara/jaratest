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

animalList = ['gosi001','gosi002','gosi003','gosi004','''gosi005''',
              'gosi006','''gosi007''','gosi008','gosi009','gosi010',
              '''gosi011''','gosi012','gosi013','gosi014','''gosi015''']

nValidAll = []
fractionValidAll = []
fractionCorrectAll = []

for inds,subject in enumerate(animalList):
    behavFile = loadbehavior.path_to_behavior_data(subject,'2afc',session)
    bdata = loadbehavior.BehaviorData(behavFile)

    delayToTargetMean = bdata['delayToTargetMean'][-1]
    delayToTargetHalfRange = bdata['delayToTargetHalfRange'][-1]
    targetDuration = bdata['targetDuration'][-1]
    delayToGoSignal = bdata['delayToGoSignal'][-1]
    antibiasMode = bdata['antibiasMode'][-1]

    targetFrequency = bdata['targetFrequency']
    choice = bdata['choice']
    valid = bdata['valid'] & (choice!=bdata.labels['choice']['none'])
    choiceRight = (choice==bdata.labels['choice']['right'])
    outcome = bdata['outcome']
    validCorrect = outcome[valid.astype(bool)]==bdata.labels['outcome']['correct']

    nValid = np.sum(valid)
    fractionValid = np.mean(valid)
    fractionCorrect = np.mean(validCorrect)
    
    print '--- {0} ---'.format(subject)
    print 'Target delay = {0}+/-{1}   Target duration = {2}   Go-delay = {3}    Antibias Mode = {4}'.format(delayToTargetMean,delayToTargetHalfRange,
                                                                                     targetDuration,delayToGoSignal,antibiasMode)
    print 'N valid trials  = {0}'.format(nValid)
    print 'Percent valid = {0:0.0%}'.format(fractionValid)
    print 'Percent correct = {0:0.0%}'.format(fractionCorrect)
    print ''

    nValidAll.append(nValid)
    fractionValidAll.append(fractionValid)
    fractionCorrectAll.append(fractionCorrect)

plt.clf()
nSubjects = len(animalList)
xvals = np.arange(1,len(animalList)+1)

plt.subplot(3,1,1)
plt.bar(xvals, nValidAll, align='center', color='0.75')
plt.ylabel('N valid')
plt.xlim([0,nSubjects+1])
plt.title('Go-signal mice - {0}'.format(session), fontweight='bold')

plt.subplot(3,1,2)
plt.bar(xvals, 100*np.array(fractionValidAll), align='center', color='g')
plt.ylabel('% valid')
plt.ylim([0,100])
plt.xlim([0,nSubjects+1])

plt.subplot(3,1,3)
plt.bar(xvals, 100*np.array(fractionCorrectAll), align='center', color='b')
plt.ylabel('% correct')
plt.ylim([0,100])
plt.xlim([0,nSubjects+1])


plt.show()
