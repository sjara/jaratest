from jaratoolbox import loadbehavior
import os
from jaratoolbox import behavioranalysis
from statsmodels.stats.proportion import proportion_confint
import numpy as np
import matplotlib.pyplot as plt


# subjects = ['adap022', 'adap026', 'adap027', 'adap030']
# sessions = ['20160612a', '20160613a', '20160614a', '20160615a', '20160616a', '20160617a', '20160618a', '20160619a', '20160620a', '20160621a', '20160622a']

subjects = ['adap025']
sessions = ['20160712a','20160713a']


def light_discrim_behavior_report(subjects, sessions, outputDir=None):

#allPerf(subjects, sessions)
    allPerf = np.zeros((len(subjects), len(sessions)))
    upper = np.zeros((len(subjects), len(sessions)))
    lower = np.zeros((len(subjects), len(sessions)))

    allPerfRightSide = np.zeros((len(subjects), len(sessions)))
    allPerfLeftSide = np.zeros((len(subjects), len(sessions)))

    for indSubject, subject in enumerate(subjects):
        for indSession, session in enumerate(sessions):
            bfile = loadbehavior.path_to_behavior_data(subject, 'lightDiscrim', session)
            bdata = loadbehavior.BehaviorData(bfile)

            valid = bdata['valid']
            correct = bdata['outcome'] == bdata.labels['outcome']['correct']

            validCorrect = (valid & correct)

            numValid = sum(valid)
            numCorrect = sum(validCorrect)

            allPerf[indSubject, indSession] = numCorrect/float(numValid)

            # import ipdb; ipdb.set_trace()

            ci = proportion_confint(numCorrect, numValid)

            lower[indSubject, indSession] = ci[0]
            upper[indSubject, indSession] = ci[1]

            rightTrials = bdata['rewardSide']==bdata.labels['rewardSide']['right']
            leftTrials = bdata['rewardSide']==bdata.labels['rewardSide']['left']

            correctRight = (validCorrect & rightTrials)
            correctLeft = (validCorrect & leftTrials)

            allPerfRightSide[indSubject, indSession] = sum(correctRight)/float(sum(rightTrials))
            allPerfLeftSide[indSubject, indSession] = sum(correctLeft)/float(sum(leftTrials))



    # plt.figure()
    plt.clf()
    for indSubject, subject in enumerate(subjects):

        plt.subplot(len(subjects), 1, indSubject+1)
        thisPerf = allPerf[indSubject, :]
        plt.plot(100*thisPerf, 'b-o')
        upperWhisker = np.array(upper[indSubject, :] - thisPerf)
        lowerWhisker = np.array(thisPerf - lower[indSubject, :])
        plt.errorbar(range(len(thisPerf)), 100*thisPerf, yerr=[100*lowerWhisker, 100*upperWhisker], label='Overall')
        plt.plot(100*allPerfLeftSide[indSubject, :], 'r-o', label='Left')
        plt.plot(100*allPerfRightSide[indSubject, :], 'g-o', label='Right')
        plt.ylim([-5, 105])
        plt.xlim([-0.1, len(sessions)-0.9])
        plt.title('{}'.format(subject))
        plt.ylabel('% correct')
        plt.axhline(100, color='0.7')
        plt.axhline(50, color='0.7')
        plt.axhline(0, color='0.7')

    plt.legend(loc=8)
    plt.xlabel('session')
    plt.show()

    if outputDir:
        subjectString = '-'.join(subjects)
        dateString = '_to_'.join([sessions[0], sessions[-1]])
        figName = '{}.png'.format('_'.join([subjectString, dateString]))
        fullFigPath = os.path.join(outputDir, figName)
        plt.savefig(fullFigPath)

if __name__=='__main__':
    light_discrim_behavior_report(subjects, sessions)
