"""
Example of psychometric curve.
"""

import numpy as np
from matplotlib import pyplot as plt

dataFile = './adap013_20160331a_behavior.npz'
behaviorData = np.load(dataFile)

targetFrequency = behaviorData['targetFrequency']
validTrials = behaviorData['validTrials']
choiceRight = behaviorData['choiceRight']

possibleFreq = np.unique(targetFrequency)
nFreq = len(possibleFreq)

nTrialsEachFreq = np.empty(nFreq)
nRightEachFreq = np.empty(nFreq)

for indFreq, thisFreq in enumerate(possibleFreq):
    nTrialsEachFreq[indFreq] = np.sum((targetFrequency==thisFreq) & validTrials)
    nRightEachFreq[indFreq] = np.sum((targetFrequency==thisFreq) & choiceRight & validTrials)

fractionRightEachFreq =  nRightEachFreq/nTrialsEachFreq

plt.clf()
plt.plot(possibleFreq,fractionRightEachFreq, 'o-')
plt.ylabel('Fraction rightward trials')
plt.xlabel('Frequency (Hz)')
plt.show()
