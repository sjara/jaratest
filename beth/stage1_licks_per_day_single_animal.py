import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import behavioranalysis

subject = 'chad049'
paradigm = 'detectiontwochoice'
alternativeParadigm = 'twochoice'
sessions = ['20200710a', '20200711a', '20200712a', '20200713a', '20200714a', '20200715a', '20200716a', '20200717a', '20200718a', '20200720a', '20200721a', '20200722a']

licksPerDay = []

for session in sessions:

    behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
    alternativeBehavFile = loadbehavior.path_to_behavior_data(subject,alternativeParadigm,session)
    if os.path.isfile(behavFile):
        bdata = loadbehavior.BehaviorData(behavFile)
    elif os.path.isfile(alternativeBehavFile):
        bdata = loadbehavior.BehaviorData(alternativeBehavFile)
    else:
        print('There is no file named {} or {}.'.format(behavFile, alternativeBehavFile))
        continue

    numTrials = len(bdata['outcome'])
    licksPerDay.append(numTrials)
    #print('{} {} {} {}'.format(subject, paradigm, session, numTrials))

plt.clf()
day = list(range(1, len(sessions)+1)) # Day 8 is when we switched from twochoice to detectiontwochoice
plt.bar(day, licksPerDay)
plt.xlabel('Day')
plt.ylabel('Number of Licks')
plt.title(subject)
plt.show()
