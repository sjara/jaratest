import os
import numpy as np
import matplotlib.colors

from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import settings

#REALLY DUMB WORKAROUND FOR THE FACT THAT COLOR LISTS ONLY TAKES RGBA INPUTS
def list_colours_to_rgba(colours):
    dumbcolours = np.zeros((len(colours),4))
    for indColour, colour in enumerate(colours):
        thisColour = matplotlib.colors.colorConverter.to_rgba(colour, alpha=1)
        dumbcolours[indColour,:] = thisColour
    return dumbcolours

def bootstrap_median_CI(data, reps=1000, interval=95):
    medians = np.zeros(reps)
    for ind in range(reps):
        samples = np.random.choice(data, len(data), replace=True)
        medians[ind] = np.median(samples)
    low = np.percentile(medians,(100-interval)/2.0)
    high = np.percentile(medians,interval+(100-interval)/2.0)
    return [low, high]

# function to calculate effect size (Cohen's d)
def cohend(data1, data2, independent=True):
    n1, n2 = len(data1), len(data2)

    # use pooled std for independent samples or pre-treatment std for paired samples
    if independent:
        stdev1, stdev2 = np.var(data1, ddof=1), np.var(data2, ddof=1)
        stdev = np.sqrt(((n1-1)*stdev1 + (n2-1)*stdev2) / (n1 + n2 - 2))
    else:
        stdev = np.var(data1, ddof=1)
    return (np.mean(data1) - np.mean(data2)) / stdev

def get_reaction_times(mouse, sessions):
    behavData = behavioranalysis.load_many_sessions(mouse, sessions)
    if all(~np.isnan(behavData['timeCenterOut'])):
        reactionTimes = behavData['timeCenterOut'] - behavData['timeTarget']
        decisionTimes = behavData['timeSideIn'] - behavData['timeCenterOut']
    else:
        reactionTimes = []
        decisionTimes = []
        for session in sessions:
            thisBehavFile = os.path.join(settings.BEHAVIOR_PATH, mouse, mouse + '_2afc_' + session + '.h5')
            if os.path.exists(thisBehavFile):
                thisBehavData = loadbehavior.BehaviorData(thisBehavFile, readmode='full')
            timeSound = thisBehavData['timeTarget']
            timeCenterOut = np.zeros(len(timeSound))
            timeSideIn = thisBehavData['timeSideIn']

            eventCode = np.array(thisBehavData.events['eventCode'])
            eventTime = thisBehavData.events['eventTime']
            CoutInds = np.where(eventCode == behavData.stateMatrix['eventsNames']['Cout'])[0]

            for trial in range(len(timeSound)):
                soundEventInd = np.where(eventTime == timeSound[trial])[0][0]
                CoutInd = CoutInds[np.argmax(CoutInds > soundEventInd)]
                timeCenterOut[trial] = eventTime[CoutInd]

            thisReactionTimes = timeCenterOut - timeSound
            thisDecisionTimes = timeSideIn - timeCenterOut

            reactionTimes.extend(thisReactionTimes)
            decisionTimes.extend(thisDecisionTimes)

        reactionTimes = np.array(reactionTimes)
        decisionTimes = np.array(decisionTimes)

    return reactionTimes, decisionTimes

def get_trials(behavData):
    numLasers = np.unique(behavData['laserSide'])
    numBands = np.unique(behavData['currentBand'])
    numSNRs = np.unique(behavData['currentSNR'])

    trialsEachCond = behavioranalysis.find_trials_each_combination(behavData['laserSide'], numLasers,
                                                                   behavData['currentBand'], numBands)
    trialsEachSNR = behavioranalysis.find_trials_each_type(behavData['currentSNR'], numSNRs)

    trialsEachCond3Params = np.zeros((len(behavData['laserSide']), len(numLasers), len(numBands), len(numSNRs)), dtype=bool)
    for ind in range(len(numSNRs)):
        trialsEachCond3Params[:, :, :, ind] = trialsEachCond & trialsEachSNR[:, ind][:, np.newaxis, np.newaxis]

    incorrect = behavData['outcome'] == behavData.labels['outcome']['error']
    correct = behavData['outcome'] == behavData.labels['outcome']['correct']
    rightChoice = behavData['choice'] == behavData.labels['choice']['right']
    leftChoice = behavData['choice'] == behavData.labels['choice']['left']

    if 'toneSide' in behavData.keys():
        if behavData['toneSide'][-1] == behavData.labels['toneSide']['right']:
            toneChoice = rightChoice
            noiseChoice = leftChoice
        elif behavData['toneSide'][-1] == behavData.labels['toneSide']['left']:
            toneChoice = leftChoice
            noiseChoice = rightChoice
    else:
        # all tones meant go to right before introduction of 'toneSide' key
        toneChoice = rightChoice
        noiseChoice = leftChoice

    return correct, incorrect, toneChoice, noiseChoice, trialsEachCond3Params, [numLasers, numBands, numSNRs]

if __name__ == "__main__":
    mouse = 'band091'
    sessions = ['20200317a', '20200318a', '20200320a', '20200321a', '20200323a']

    reactionTimes, decisionTimes = get_reaction_times(mouse, sessions)
