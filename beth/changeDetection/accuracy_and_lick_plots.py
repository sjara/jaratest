"""
Calculates and plots the number of trials, number of hits/misses, percentage of licks that happen in the period during and after the RAP, and total number of licks per session for an animal in Stage 2, 3, or 4.

This code is run with a subject name and stage as arguments.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import loadbehavior
from jaratoolbox import settings

# Throws an error if the name of the animal and its training stage are not specified.
if len(sys.argv) < 3:
    sys.exit("You must pass two arguments: 'animalName trainingStage'")

# Parameters
paradigm = 'detectiontwochoice'
stage2Param = 1.5 # Length of RAP in Stage 2
stage3Param = 0.5 # Length of RAP in Stage 3
stage4Param = 1.0 # Length of post duration in Stage 4
stage5Param = 0.2 # Length of post duration in Stage 5

# Creates a list of the animal and stage you want plots for.
subject = sys.argv[1]
stage = sys.argv[-1]

allSessions = []

# Specifies where the behavioral data is stored in your computer for a subject.
behavPath = "/Users/bethmccarry/src/behaviorData/"
behavFolder = os.path.join(behavPath, "{}".format(subject))

# Goes to the folder where the behavioral data is stored, extracts the session name ('yyyymmdda') for each file, and sorts by date.
for dailyBehavData in os.listdir(behavFolder):
    date = dailyBehavData[-12:-3]
    allSessions.append(date)
allSessions = sorted(allSessions)
#allSessions.remove('20200818a')
#allSessions.remove('20200819a')

# Creates empty lists to fill with the sessions that happened in each training stage.
trainingStageOneSessions = []
trainingStageTwoSessions = []
trainingStageThreeSessions = []
trainingStageFourSessions = []
trainingStageFiveSessions = []

# For each session, sort the sessions according to which training stage happened on that day:
for session in allSessions:
    # This will skip over behavior files that had the paradigm 'twochoice' that was used before the 'detectiontwochoice' paradigm was written. Skipping over these is fine because all of those sessions were in Stage 1.
    behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
    if os.path.isfile(behavFile):
        bdata = loadbehavior.BehaviorData(behavFile)

        if bdata['taskMode'][-1] == bdata.labels['taskMode']['water_on_lick']:
            trainingStageOneSessions.append(session)
        elif bdata['taskMode'][-1] == bdata.labels['taskMode']['lick_after_change']:
            if bdata['rewardAvailability'][-1] == stage2Param:
                trainingStageTwoSessions.append(session)
            elif bdata['rewardAvailability'][-1] == stage3Param:
                trainingStageThreeSessions.append(session)
        elif bdata['taskMode'][-1] == bdata.labels['taskMode']['discriminate_change']:
            if bdata['preDuration'][-1] == stage4Param:
                trainingStageFourSessions.append(session)
            elif bdata['preDuration'][-1] == stage5Param:
                trainingStageFiveSessions.append(session)
    else:
        #print('There is no file named {} in {}.'.format(behavFile, behavFolder))
        continue

# Creates empty lists so we can add lick data later.
numTrials = []
hitsL = []
hitsR = []
missesL = []
missesR = []
licksL = []
licksR = []
invalidLicksL = []
invalidLicksR = []
licksInRAPL = []
licksInRAPR = []

if stage == '2':
    sessions = trainingStageTwoSessions
elif stage == '3':
    sessions = trainingStageThreeSessions
elif stage == '4':
    sessions = trainingStageFourSessions
elif stage == '5':
    sessions = trainingStageFiveSessions

if sessions == []:
    sys.exit('This animal has not started training at stage {}.'.format(stage))

for session in sessions:

    behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
    if os.path.isfile(behavFile):
        bdata = loadbehavior.BehaviorData(behavFile)

    # Calculate the number of trials, hits, and misses for the left and right ports and add them to their respective list.
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

    # Extract lick data if that data exists.
    # NOTE: This is an if statement because these four columns of data were added in midway through training. Future cohorts won't need this if statement.
    if 'nLicksLeft' in bdata.keys():

        numLicksL = bdata['nLicksLeft'][-1]
        licksL.append(numLicksL)

        numLicksR = bdata['nLicksRight'][-1]
        licksR.append(numLicksR)

        numInvalidLicksL = bdata['nLicksLeftInvalid'][-1]
        invalidLicksL.append(numInvalidLicksL)

        numInvalidLicksR = bdata['nLicksRightInvalid'][-1]
        invalidLicksR.append(numInvalidLicksR)

        # If the animal licks after the reward, but before the trial ends, they are not counted as invalid. This decision was made because animals generally lick multiple times after the reward.
        normalizedRAPLicksL = (numLicksL - numInvalidLicksL) / numLicksL * 100
        licksInRAPL.append(normalizedRAPLicksL)

        normalizedRAPLicksR = (numLicksR - numInvalidLicksR) / numLicksR * 100
        licksInRAPR.append(normalizedRAPLicksR)
    #else:
        #print('There is no lick data for Stage {} session {}.'.format(stage, session))


# Initializes the subplot environment.
#plt.figure()
ax = plt.subplot2grid((1,5), (0,0))
plt.suptitle('{} - Training Stage {} - Change Detection Task'.format(subject, stage))

# Parameters for the number of trials per day plot.
barWidth = 0.15
x = np.arange(len(numTrials)) + 1

# Creates a bar graph of the number of trials per day for each day trained in the specified stage.
ax0 = plt.subplot2grid((1,5), (0,0))
plt.bar(x, numTrials, width=barWidth*2, color=(0.00,0.04,0.20))
plt.ylabel('Number of trials', fontsize=18)
plt.xlabel('Day of training', fontsize=18)
plt.xticks(range(1, len(numTrials)+1,4), fontsize=18)
plt.yticks(fontsize=18)

# Parameters for hits/misses per day plot.
barWidth = 0.2
x = np.arange(len(numTrials)) + 1
x1 = [day + barWidth for day in x] # These are a necessity for grouped bar graphs.
x2 = [day + barWidth for day in x1]
x3 = [day + barWidth for day in x2]

# Creates a grouped bar graph of the number of hits and misses for the left and right ports for each day trained in the specified stage.
ax1 = plt.subplot2grid((1,5), (0,1), colspan = 2)
plt.bar(x, hitsR, width=barWidth, color=(0.00,0.31,0.49), align='center', label='hitsR ')
plt.bar(x1, hitsL, width=barWidth, color=(0.00,0.59,0.78), align='center', label='hitsL')
plt.bar(x2, missesR, width=barWidth, color=(0.34,0.77,0.72), align='center', label='missesR')
plt.bar(x3, missesL, width=barWidth, color=(0.67,0.96,0.66), align='center', label='missesL')
plt.legend(fontsize=18)
plt.ylabel('% of total trials', fontsize=18)
plt.xlabel('Day of training', fontsize=18)
plt.xticks(np.arange(min(x), max(x)+1), fontsize=18)
plt.yticks(fontsize=18)

# If there is lick data, use that data to plot the normalized licks per day. Otherwise, plot an empty box.
if licksL != []:
    # Parameters for normalized licks per day plot.
    # 'trainingDay' is added here because code about licking wasn't added to the paradigm until day 'trainingDay' of the training schedule. Depending on which training stage an animal was in, this day might be different for each animal. These if statements specify what the stage and training day was when lick data became readily available. Future cohorts will not need this section.
    if stage == '2':
        if subject == 'chad047' or subject == 'chad050':
            trainingDay = 11
        else:
            trainingDay = 0
    elif stage == '3':
        if subject == 'chad048':
            trainingDay = 3
        elif subject == 'chad046':
            trainingDay = 4
        else:
            trainingDay = 0
    else:
        trainingDay = 1

    # Parameters for lick plots
    barWidth = 0.3
    xx = np.arange(len(licksL)) + trainingDay
    xx1 = [day + barWidth for day in xx]
    threshold = 50 # Percent

    # Creates a grouped bar graph of the percentage of total licks per side during and after the RAP for the left and right ports as well as a horizontal line that signifies the threshold an animal must meet to move on to the next training stage.
    ax2 = plt.subplot2grid((1,5), (0,3))
    plt.bar(xx, licksInRAPL, width=barWidth, color=(0.34,0.77,0.72), align='center', label='Left')
    plt.bar(xx1, licksInRAPR, width=barWidth, color=(0.67,0.96,0.66), align='center', label='Right')
    #plt.axhline(y=threshold, color='r', linewidth=0.5)
    plt.legend(fontsize=18)
    plt.ylabel('% of licks in & after RAP', fontsize=18)
    plt.xlabel('Day of training', fontsize=18)
    #plt.xticks(range(trainingDay+1, trainingDay+len(licksL)+1))
    plt.xticks(np.arange(min(xx), max(xx)+1,2), fontsize=18)
    plt.yticks(fontsize=18)

    # Creates a grouped bar graph of the number of licks per side for each training session.
    ax3 = plt.subplot2grid((1,5), (0,4))
    licksL = np.divide(licksL, 1000)
    licksR = np.divide(licksR, 1000)
    plt.bar(xx, licksL, width=barWidth, color=(0.34,0.77,0.72), align='center', label='Left')
    plt.bar(xx1, licksR, width=barWidth, color=(0.67,0.96,0.66), align='center', label='Right')
    plt.legend(fontsize=18)
    plt.ylabel('Total licks (thousands)', fontsize=18)
    plt.xlabel('Day of training', fontsize=18)
    #plt.xticks(range(trainingDay, trainingDay+len(licksL)+1))
    plt.xticks(np.arange(min(xx), max(xx)+1,2), fontsize=18)
    plt.yticks(fontsize=18)

else:
    ax2 = plt.subplot2grid((1,5), (0,3))
    plt.ylabel('% of licks in & after RAP', fontsize=18)
    plt.xlabel('Day of Training', fontsize=18)

    ax3 = plt.subplot2grid((1,5), (0,4))
    plt.ylabel('Total licks', fontsize=18)
    plt.xlabel('Day of training', fontsize=18)

# Saving the figure
figFormat = 'png'
figFilename ='{}_stage{}.{}'.format(subject, stage, figFormat)
outputDir = settings.BEHAVIOR_REPORTS_PATH
figFullpath = os.path.join(outputDir,figFilename)
plt.gcf().set_size_inches([20,7.5])
plt.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.45) # Sets the spacing of plots.
plt.savefig(figFullpath,format=figFormat)

#plt.show()
