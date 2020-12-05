import os
import numpy as np

from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import settings

def bootstrap_median_CI(data, reps=1000, interval=95):
    medians = np.zeros(reps)
    for ind in range(reps):
        samples = np.random.choice(data, len(data), replace=True)
        medians[ind] = np.median(samples)
    low = np.percentile(medians,(100-interval)/2.0)
    high = np.percentile(medians,interval+(100-interval)/2.0)
    return [low, high]

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

if __name__ == "__main__":
    mouse = 'band091'
    sessions = ['20200317a', '20200318a', '20200320a', '20200321a', '20200323a']

    reactionTimes, decisionTimes = get_reaction_times(mouse, sessions)
