"""
Calculates and plots the number of rewards/trials each day of training in Stage 1 of the change detection behavioral paradigm for any/all animals in a cohort.

This code can be run with subject names as arguments.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import loadbehavior
from jaratoolbox import settings
# Throws an error if the name of the animal(s) you want reward/trial plots for is not specified.
if len(sys.argv) < 2:
    sys.exit('You must pass at least one argument: animalName')

# When the first round of training began, there wasn't a paradigm written yet, so we defaulted to 'twochoice' which was already ready to go. Eight days into the training, the 'detectiontwochoice' paradigm was completed and we switched to that one. To analyze data, we are looking at data from two different paradigms.
paradigm = 'detectiontwochoice'
alternativeParadigm = 'twochoice'

# Creates a list of the animal(s) you want reward/trial plots for.
subjects = sys.argv[1:]

rewardsBySubject = []

# For each animal specified
for subject in subjects:
    # Specifies where the behavioral data is stored in your computer for a subject.
    behavPath = "/Users/bethmccarry/src/behaviorData/"
    behavFolder = os.path.join(behavPath, "{}".format(subject))

    sessions = []
    rewardsPerDay = []

    # Goes to the folder where the behavioral data is stored, and extracts the session name ('yyyymmdda') for each file. Then we sort these by date.
    for dailyBehavData in os.listdir(behavFolder):
        date = dailyBehavData[-12:-3]
        sessions.append(date)
    sessions = sorted(sessions)

    # For each session:
    for session in sessions:
        # Loading behavior data (bdata) for a single session. This is a work-around because we have data from two different paradigms that we're analyzing. Future cohorts will only need to load from 'behavFile', not 'behavFile' and 'alternativeBehavFile'.
        behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
        alternativeBehavFile = loadbehavior.path_to_behavior_data(subject,alternativeParadigm,session)
        if os.path.isfile(behavFile):
            bdata = loadbehavior.BehaviorData(behavFile)
        elif os.path.isfile(alternativeBehavFile):
            bdata = loadbehavior.BehaviorData(alternativeBehavFile)
        else:
            print('There is no file named {} or {}.'.format(behavFile, alternativeBehavFile))
            continue

        # Search through data where the 'taskMode' is equivalent to the Stage 1 task mode parameter. This way we know we're only extracting data from Stage 1 of training and none others. If the 'taskMode' is not equivalent to the Stage 1 task mode, move on to the next session.
        if bdata['taskMode'][-1] == bdata.labels['taskMode']['water_on_lick']:
            # Calculate the number of rewards/trials and add that number to a list. Number of rewards is same as number of trials in Stage 1.
            numRewards = len(bdata['outcome'])
            rewardsPerDay.append(numRewards)
            print('{} {} is completed.'.format(subject, session))
        else:
            continue

    # Make a list of each animal and the number of rewards they recieved during each training day.
    rewardsBySubject.append((subject, rewardsPerDay))

# Parameters for plots
threshold = 200 # Rewards to move on to next training stage

# Defines the number of rows the figure should have depending on how many animals are being trained and spacing between plots. This will need to change if a cohort has more than 6 animals.
if len(subjects) == 1:
    nRows = 1
    nCols = 1
    figsize = (6,4)
    #plt.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9) # Figure spacing
elif len(subjects) == 2:
    nRows = 1
    nCols = 2
    figsize = (12,4)
    #plt.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.3)
elif len(subjects) == 3:
    nRows = 1 # Number of rows in the plot
    nCols = 3
    figsize = (18, 4) # Size of the figure
    #plt.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.3)
else:
    nRows = 2
    nCols = 3
    figsize = (18, 8)
    #plt.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.3,hspace=0.35)

# Plotting number of rewards/trials per day for all Stage 1 training sessions.
fig = plt.figure(figsize=figsize)

# Assigns each animal with an ascending number (for ex. 'chad045, 1', 'chad046, 2') in order to iterate through each animal and pull out data for a single animal from the 'rewardsBySubject' list created earlier.
for subject, num in zip(subjects, range(1, len(subjects)+1)):

    # Defining the x and y values for the rewards per day plot.
    daysTrained = np.arange(1, len(rewardsBySubject[num-1][1])+1)
    listDaysTrained = list(daysTrained)
    rewards = rewardsBySubject[num-1][1]

    # Add a new plot for each animal
    ax = fig.add_subplot(nRows, nCols, num)
    #plt.suptitle('Training Stage 1 - Change Detection Task')

    # Creates a bar graph of the number of rewards/trials for each day trained and a horizontal line that is the threshold that an animal must meet before moving on to the next training stage.
    ax.bar(daysTrained, rewards, color=(0.00,0.59,0.78))
    plt.axhline(y=threshold, color='r', linewidth=0.5)
    plt.title(subject, fontsize=18)
    plt.ylabel('Rewards', fontsize=18)
    plt.xlabel('Day of training', fontsize=18)
    #plt.xticks(daysTrained, 2, fontsize=16)
    plt.xticks(np.arange(min(daysTrained), max(daysTrained)+1, 2), fontsize=18)
    plt.yticks(np.arange(0, max(rewards)+100, 200),fontsize=18)

# Saving the figure
figFormat = 'png'
figFilename ='all_animals_stage1.{}'.format(figFormat)
outputDir = settings.BEHAVIOR_REPORTS_PATH
figFullpath = os.path.join(outputDir,figFilename)
plt.gcf().set_size_inches([17,7.5])
plt.subplots_adjust(left=0.15,bottom=0.1,right=0.9,top=0.9,wspace=0.35,hspace=0.45) # Sets the spacing of plots.
plt.savefig(figFullpath,format=figFormat)

plt.show()
