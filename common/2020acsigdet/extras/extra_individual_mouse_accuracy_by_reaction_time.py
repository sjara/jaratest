import sys
sys.path.append('..')
import os
import numpy as np
from statsmodels.stats.proportion import proportion_confint

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import extraplots

import studyparams

SOM_ARCHT_MICE = studyparams.SOM_ARCHT_MICE
PV_ARCHT_MICE = studyparams.PV_ARCHT_MICE
PV_CHR2_MICE = studyparams.PV_CHR2_MICE
mouseType = [PV_ARCHT_MICE, SOM_ARCHT_MICE, PV_CHR2_MICE]

for indType, mice in enumerate(mouseType):
    for mouse in mice:
        fig = plt.gcf()
        fig.clf()
        fig.set_facecolor('w')

        gs = gridspec.GridSpec(1, 2)
        gs.update(top=0.90, bottom=0.15, left=0.07, right=0.98, wspace=0.5, hspace=0.3)

        if indType == 2:
            laserSessions = studyparams.miceDict[mouse]['3mW laser']
        else:
            laserSessions = studyparams.miceDict[mouse]['10mW laser']
        laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

        numLasers = np.unique(laserBehavData['laserSide'])
        numBands = np.unique(laserBehavData['currentBand'])
        numSNRs = np.unique(laserBehavData['currentSNR'])

        correct = laserBehavData['outcome'] == laserBehavData.labels['outcome']['correct']
        incorrect = laserBehavData['outcome'] == laserBehavData.labels['outcome']['error']
        rightChoice = laserBehavData['choice'] == laserBehavData.labels['choice']['right']
        leftChoice = laserBehavData['choice'] == laserBehavData.labels['choice']['left']

        if 'toneSide' in laserBehavData.keys():
            if laserBehavData['toneSide'][-1] == laserBehavData.labels['toneSide']['right']:
                toneChoice = rightChoice
                noiseChoice = leftChoice
            elif laserBehavData['toneSide'][-1] == laserBehavData.labels['toneSide']['left']:
                toneChoice = leftChoice
                noiseChoice = rightChoice
        else:
            # all tones meant go to right before introduction of 'toneSide' key
            toneChoice = rightChoice
            noiseChoice = leftChoice

        if all(~np.isnan(laserBehavData['timeCenterOut'])):
            reactionTimes = laserBehavData['timeCenterOut'] - laserBehavData['timeTarget']
        else:
            reactionTimes = []
            for session in laserSessions:
                thisBehavFile = os.path.join(settings.BEHAVIOR_PATH, mouse,
                                             mouse + '_2afc_' + session + '.h5')
                if os.path.exists(thisBehavFile):
                    thisBehavData = loadbehavior.BehaviorData(thisBehavFile, readmode='full')
                timeSound = thisBehavData['timeTarget']
                timeCenterOut = np.zeros(len(timeSound))

                eventCode = np.array(thisBehavData.events['eventCode'])
                eventTime = thisBehavData.events['eventTime']
                CoutInds = np.where(eventCode == laserBehavData.stateMatrix['eventsNames']['Cout'])[0]

                for trial in range(len(timeSound)):
                    soundEventInd = np.where(eventTime == timeSound[trial])[0][0]
                    CoutInd = CoutInds[np.argmax(CoutInds > soundEventInd)]
                    timeCenterOut[trial] = eventTime[CoutInd]

                thisReactionTimes = timeCenterOut - timeSound

                reactionTimes.extend(thisReactionTimes)

            reactionTimes = np.array(reactionTimes)

        trialsEachLaser = behavioranalysis.find_trials_each_type(laserBehavData['laserSide'], numLasers)

        controlCorrect = correct & trialsEachLaser[:,0]
        controlIncorrect = incorrect & trialsEachLaser[:,0]

        correctReactionTimes = reactionTimes[controlCorrect]
        correctReactionTimes = correctReactionTimes[np.isfinite(correctReactionTimes)]
        incorrectReactionTimes = reactionTimes[controlIncorrect]
        incorrectReactionTimes = incorrectReactionTimes[np.isfinite(incorrectReactionTimes)]

        # -- plot reaction times for correct and incorrect trials with no laser --
        axHist = plt.subplot(gs[0, 0])

        # nBins = 10
        # bins1 = np.linspace(0, 0.2, nBins+1)

        binslow = np.linspace(0, 0.06, 7)
        binshigh = np.linspace(0.08, 0.2, 7)
        bins = np.concatenate((binslow, binshigh))
        nBins = len(bins)-1

        binCounts, bins, patches = plt.hist([correctReactionTimes, incorrectReactionTimes], bins=bins, color=['g', 'r'])

        axHist.legend(patches, ['correct', 'incorrect'], loc='best')

        axHist.set_xlabel('Sampling time (s)')

        extraplots.boxoff(axHist)

        # -- plot average accuracy for each reaction time --
        axAcc = plt.subplot(gs[0, 1])

        accuracies = np.zeros(nBins)
        upperErrorBar = np.zeros_like(accuracies)
        lowerErrorBar = np.zeros_like(upperErrorBar)
        for bin in range(nBins):
            accuracies[bin] = 100.0 * binCounts[0][bin]/(binCounts[0][bin]+binCounts[1][bin])
            CIthisBin = np.array(proportion_confint(binCounts[0][bin], (binCounts[0][bin]+binCounts[1][bin]), method='wilson'))
            upperErrorBar[bin] = 100.0 * CIthisBin[1] - accuracies[bin]
            lowerErrorBar[bin] = accuracies[bin] - 100.0 * CIthisBin[0]

        plt.plot(bins[:-1], accuracies, 'o-', color='k', ms=5)
        plt.errorbar(bins[:-1], accuracies, yerr=[lowerErrorBar, upperErrorBar], fmt='none',
                     color='k', lw=2, capsize=5, capthick=1, zorder=-10)

        axAcc.set_xlabel('Sampling time (s)')
        axAcc.set_ylabel('Accuracy (%)')

        extraplots.boxoff(axAcc)

        cutOff = 0.02
        percentBelow = 100.0 * np.sum(reactionTimes<cutOff)/len(reactionTimes)
        print(f'{mouse} percent reaction times below {cutOff}s: {percentBelow}%')

        # -- save fig --
        plt.suptitle(mouse)

        figFilename = f'{mouse}_correct_by_reaction'
        extraplots.save_figure(figFilename, 'png', [8, 4], '/tmp/', facecolor='w')

