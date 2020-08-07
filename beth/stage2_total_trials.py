import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import loadbehavior

paradigm = 'detectiontwochoice'
#alternativeParadigm = 'twochoice'

subject = 'chad045'

def trials_per_day(subject):

    behavPath = "/Users/bethmccarry/src/behaviorData/"
    behavFolder = os.path.join(behavPath, "{}".format(subject))
    #print(behavFolder)

    sessions = []

    for dailyBehavData in os.listdir(behavFolder):
        date = dailyBehavData[-12:-3]
        sessions.append(date)

    sessions = sorted(sessions)
    #print(subject,sessions)

    numTrials = []
    hitsL = []
    hitsR = []
    missesL = []
    missesR = []

    numSessions = 0
    for session in sessions:

        behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
        #alternativeBehavFile = loadbehavior.path_to_behavior_data(subject,alternativeParadigm,session)
        if os.path.isfile(behavFile):
            bdata = loadbehavior.BehaviorData(behavFile)
        else:
            #print("This was the alternative paradigm we ran before we got the new paradigm written. It is only relevant for Stage 1 of training.")
            continue


        if bdata['taskMode'][-1] == 1:
            numSessions += 1
            numTrialsDay = len(bdata['taskMode'])
            numTrials.append(numTrialsDay)

            numHitsL = bdata['nHitsLeft'][-1]
            normalizedHitsL = numHitsL / numTrialsDay * 100
            hitsL.append(normalizedHitsL)

            numHitsR = bdata['nHitsRight'][-1]
            normalizedHitsR = numHitsR / numTrialsDay * 100
            hitsR.append(normalizedHitsR)

            numMissesL = bdata['nMissesLeft'][-1]
            normalizedMissesL = numMissesL / numTrialsDay * 100
            missesL.append(normalizedMissesL)

            numMissesR = bdata['nMissesRight'][-1]
            normalizedMissesR = numMissesR / numTrialsDay * 100
            missesR.append(normalizedMissesR)
        else:
            #print('{} {} was not a Stage 1 training session.'.format(subject, session))
            continue

    #print(numTrials, hitsL, hitsR, missesL, missesR)

    return(numTrials, hitsL, hitsR, missesL, missesR)

chad045trials, chad045hitsL, chad045hitsR, chad045missesL, chad045missesR = trials_per_day('chad045')
chad046trials, chad046hitsL, chad046hitsR, chad046missesL, chad046missesR = trials_per_day('chad046')
chad047trials, chad047hitsL, chad047hitsR, chad047missesL, chad047missesR = trials_per_day('chad047')
chad048trials, chad048hitsL, chad048hitsR, chad048missesL, chad048missesR = trials_per_day('chad048')
chad049trials, chad049hitsL, chad049hitsR, chad049missesL, chad049missesR = trials_per_day('chad049')
chad050trials, chad050hitsL, chad050hitsR, chad050missesL, chad050missesR = trials_per_day('chad050')


"""
Plotting
"""

def plots(subject, trials, hitsL, hitsR, missesL, missesR):
    plt.figure()
    ax = plt.subplot2grid((1,2), (0,0))
    plt.suptitle('{} - Stage 2 Training - Change Detection Task'.format(subject))

    # Parameters
    barWidth = 0.15
    x = np.arange(len(trials)) + 1
    x1 = [day + barWidth for day in x] # These are a necessity for grouped bar graphs.
    x2 = [day + barWidth for day in x1]
    x3 = [day + barWidth for day in x2]

    ax0 = plt.subplot2grid((1,2), (0,0))
    plt.bar(x, trials, width=barWidth*2, color=(0.00,0.04,0.20))
    plt.ylabel('Number of Trials')
    plt.xlabel('Day of Training')
    plt.xticks(range(1,len(trials)+1))

    ax1 = plt.subplot2grid((1,2), (0,1))
    plt.bar(x, hitsR, width=barWidth, color=(0.00,0.31,0.49), align='center', label='hitsR')
    plt.bar(x1, hitsL, width=barWidth, color=(0.00,0.59,0.78), align='center', label='hitsL')
    plt.bar(x2, missesR, width=barWidth, color=(0.34,0.77,0.72), align='center', label='missesR')
    plt.bar(x3, missesL, width=barWidth, color=(0.67,0.96,0.66), align='center', label='missesL')
    plt.legend()
    plt.ylabel('Percent of Total Trials')
    plt.xlabel('Day of Training')
    plt.xticks(range(1,len(trials)+1))
    plt.show()

plots('chad045', chad045trials, chad045hitsL, chad045hitsR, chad045missesL, chad045missesR)
plots('chad046', chad046trials, chad046hitsL, chad046hitsR, chad046missesL, chad046missesR)
plots('chad047', chad047trials, chad047hitsL, chad047hitsR, chad047missesL, chad047missesR)
plots('chad048', chad048trials, chad048hitsL, chad048hitsR, chad048missesL, chad048missesR)
plots('chad049', chad049trials, chad049hitsL, chad049hitsR, chad049missesL, chad049missesR)
plots('chad050', chad050trials, chad050hitsL, chad050hitsR, chad050missesL, chad050missesR)
