import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import loadbehavior

paradigm = 'detectiontwochoice'
alternativeParadigm = 'twochoice'

def licks_per_day(subject):

    behavPath = "/Users/bethmccarry/src/behaviorData/"
    behavFolder = os.path.join(behavPath, "{}".format(subject))
    #print(behavFolder)

    sessions = []

    for dailyBehavData in os.listdir(behavFolder):
        date = dailyBehavData[-12:-3]
        sessions.append(date)

    sessions = sorted(sessions)
    #print(subject,sessions)

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

        if bdata['taskMode'][-1] == 0:
            numTrials = len(bdata['outcome'])
            licksPerDay.append(numTrials)
        else:
            #print('{} {} was not a Stage 1 training session.'.format(subject, session))
            continue

    #print(licksPerDay)
    return(licksPerDay)

chad045 = licks_per_day('chad045')
chad046 = licks_per_day('chad046')
chad047 = licks_per_day('chad047')
chad048 = licks_per_day('chad048')
chad049 = licks_per_day('chad049')
chad050 = licks_per_day('chad050')

"""
PLOTTING
"""

threshold = 200 # Licks in a single one hour session to advance on to the next training stage
plt.clf()
ax = plt.subplot2grid((2,3), (0,0)) # Subplots with 6 animals
plt.suptitle('Stage 1 Training - Change Detection Task')
#rgb(0,10,50)
ax0 = plt.subplot2grid((2,3), (0,0))
plt.bar(list(range(1, len(chad045)+1)), chad045, color=(0.00,0.04,0.20))
plt.axhline(y=threshold, color='r', linewidth=0.5)
plt.title('chad045')
plt.ylabel('Licks')
plt.xlabel('Day of training')
plt.xticks(range(1,len(chad045)+1))

#rgb(0,80,125)
ax1 = plt.subplot2grid((2,3), (0,1))
plt.bar(list(range(1, len(chad046)+1)), chad046, color=(0.00,0.31,0.49))
plt.axhline(y=threshold, color='r', linewidth=0.5)
plt.title('chad046')
plt.ylabel('Licks')
plt.xlabel('Day of training')
plt.xticks(range(1,len(chad046)+1))

#rgb(0,150,200)
ax2 = plt.subplot2grid((2,3), (0,2))
plt.bar(list(range(1, len(chad047)+1)), chad047, color=(0.00,0.59,0.78))
plt.axhline(y=threshold, color='r', linewidth=0.5)
plt.title('chad047')
plt.ylabel('Licks')
plt.xlabel('Day of training')
plt.xticks(range(1,len(chad047)+1))

#rgb(86,197,184)
ax3 = plt.subplot2grid((2,3), (1,0))
plt.bar(list(range(1, len(chad048)+1)), chad048, color=(0.34,0.77,0.72))
plt.axhline(y=threshold, color='r', linewidth=0.5)
plt.title('chad048')
plt.ylabel('Licks')
plt.xlabel('Day of training')
plt.xticks(range(1,len(chad048)+1))

#rgb(172,245,168)
ax4 = plt.subplot2grid((2,3), (1,1))
plt.bar(list(range(1, len(chad049)+1)), chad049, color=(0.67,0.96,0.66))
plt.axhline(y=threshold, color='r', linewidth=0.5)
plt.title('chad049')
plt.ylabel('Licks')
plt.xlabel('Day of training')
plt.xticks(range(1,len(chad049)+1))

#rgb(211,250,211)
ax5 = plt.subplot2grid((2,3), (1,2))
plt.bar(list(range(1, len(chad050)+1)), chad050, color=(0.83,0.98,0.83))
plt.axhline(y=threshold, color='r', linewidth=0.5)
plt.title('chad050')
plt.ylabel('Licks')
plt.xlabel('Day of training')
plt.xticks(range(1,len(chad050)+1))

plt.show()
