'''
Example for loading behavior data with jaratoolbox
'''

from jaratoolbox import loadbehavior
import numpy as np

subject = 'test019'
experimenter = 'santiago'
paradigm = '2afc'
sessionstr = '20141224a'

behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,
                                                      paradigm,sessionstr)
bdata = loadbehavior.BehaviorData(behaviorFilename)


correct = bdata['outcome']==bdata.labels['outcome']['correct']

incorrect = bdata['outcome']==bdata.labels['outcome']['error']

# Calculate average correct
numcorrect = sum(correct)
numincorrect = sum(incorrect)
percentcorrect = float(numcorrect)/(numcorrect+numincorrect)
print percentcorrect

# Another way (all valid except those with no choice)
invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
nochoice =  bdata['outcome']==bdata.labels['outcome']['nochoice']
numvalid = sum(~invalid)-sum(nochoice)
percentcorrect = float(numcorrect)/numvalid
print percentcorrect

# Average number of rightward trials (not including no choice) for each frequency
possibleFreq = np.unique(bdata['targetFrequency'])
totalFreq=[0]*len(possibleFreq)
rightFreq=[0]*len(possibleFreq)

for i in range(len(bdata['choice'])):
    currentFreq = bdata['targetFrequency'][i]
    freqIndex = np.where(possibleFreq==currentFreq)[0][0]
    if (correct[i] or incorrect[i]):
        totalFreq[freqIndex] += 1
        if (bdata['choice'][i]==bdata.labels['choice']['right']):
            rightFreq[freqIndex] += 1



#This gives an array with true at indices of trials that are correct and went right
correctRightward = (bdata['outcome']==bdata.labels['outcome']['correct'] and bdata['choice']==bdata.labels['choice']['right'])

#This gives an array with true at indices of trials that are correct and went left
