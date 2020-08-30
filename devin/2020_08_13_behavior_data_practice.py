"""
Loads a behavior file and plots a curve of preformance. 
Devin Henderling - 2020-08-07
"""
from jaratoolbox import loadbehavior
import numpy as np
from matplotlib import pyplot as plt

subject = 'adap021'
session = '20160524a'
#subject = 'adap013'
#session = '20160331a'
paradigm = '2afc'
behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
bdata = loadbehavior.BehaviorData(behavFile)

# Total number of trials
numTrials = len(bdata['choice'])

# Frequencies presented 
freqsPresented = np.unique(bdata['targetFrequency'])

# Number of trials for each frequency
numPerFreq = np.empty(len(freqsPresented))
for indFreq, freq in enumerate(freqsPresented):
    numPerFreq[indFreq] = np.count_nonzero((bdata['targetFrequency'] == freq) & bdata['valid']) 

# Percentage of rightward trials 
rightFreq = np.empty(len(freqsPresented))
for indFreq, freq in enumerate(freqsPresented):
    rightFreq[indFreq] = np.sum((bdata['targetFrequency'] == freq) & \
                                (bdata['choice'] == bdata.labels['choice']['right']) & \
                                 bdata['valid'])
percentageRight = ((rightFreq / numPerFreq) * 100)
        
# Line plot of preformance 
plt.plot(freqsPresented, percentageRight, c="black")
plt.title("Preformance Pyschometric Curve")
plt.xlabel("Frequency")
plt.ylabel("Rightward Trials (%)")
ax = plt.subplot()
#ax.set_xscale('log')
ax.set_xticks(freqsPresented)
ax.set(xlim=(freqsPresented[0] - 1000, freqsPresented[-1] + 1000), ylim=(0, 100))
