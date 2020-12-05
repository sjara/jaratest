import sys
sys.path.append('..')
import os
import numpy as np
from statsmodels.stats.proportion import proportion_confint

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches

from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import extraplots

import studyparams

SOM_ARCHT_MICE = studyparams.SOM_ARCHT_MICE
PV_ARCHT_MICE = studyparams.PV_ARCHT_MICE
PV_CHR2_MICE = studyparams.PV_CHR2_MICE
mouseType = [PV_ARCHT_MICE, SOM_ARCHT_MICE, PV_CHR2_MICE]
mouseLabel = ['PV-ArchT', 'SOM-ArchT', 'PV-ChR2']
legendLabel = ['no PV', 'no SOM', 'PV activated']
colour = ['b', 'r', 'b']
faceColour = ['white', 'white', 'b']

# 'control' or 'laser'
sessionType = 'control'
#sessionType = 'laser'

for indType, mice in enumerate(mouseType):
    for mouse in mice:
        fig = plt.gcf()
        fig.clf()
        fig.set_facecolor('w')

        gs = gridspec.GridSpec(1, 4, width_ratios=[1.4, 1, 1.4, 1])
        gs.update(top=0.90, bottom=0.15, left=0.07, right=0.98, wspace=0.5, hspace=0.3)

        if indType == 2:
            laserSessions = studyparams.miceDict[mouse][f'3mW {sessionType}']
        else:
            laserSessions = studyparams.miceDict[mouse][f'10mW {sessionType}']
        laserBehavData = behavioranalysis.load_many_sessions(mouse, laserSessions)

        numLasers = np.unique(laserBehavData['laserSide'])
        numBands = np.unique(laserBehavData['currentBand'])
        numSNRs = np.unique(laserBehavData['currentSNR'])

        trialsEachCond = behavioranalysis.find_trials_each_combination(laserBehavData['laserSide'], numLasers,
                                                                       laserBehavData['currentBand'], numBands)

        valid = laserBehavData['valid'].astype(bool)
        correct = laserBehavData['outcome'] == laserBehavData.labels['outcome']['correct']
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
            decisionTimes = laserBehavData['timeSideIn'] - laserBehavData['timeCenterOut']
        else:
            reactionTimes = []
            decisionTimes = []
            for session in laserSessions:
                thisBehavFile = os.path.join(settings.BEHAVIOR_PATH, mouse,
                                             mouse + '_2afc_' + session + '.h5')
                if os.path.exists(thisBehavFile):
                    thisBehavData = loadbehavior.BehaviorData(thisBehavFile, readmode='full')
                timeSound = thisBehavData['timeTarget']
                timeCenterOut = np.zeros(len(timeSound))
                timeSideIn = thisBehavData['timeSideIn']

                eventCode = np.array(thisBehavData.events['eventCode'])
                eventTime = thisBehavData.events['eventTime']
                CoutInds = np.where(eventCode == laserBehavData.stateMatrix['eventsNames']['Cout'])[0]

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

        trialsEachLaser = trialsEachCond[:, :, 0]

        controlReactionTimes = reactionTimes[trialsEachLaser[:, 0]]
        controlReactionTimes = controlReactionTimes[np.isfinite(controlReactionTimes)]
        laserReactionTimes = reactionTimes[trialsEachLaser[:, 1]]
        laserReactionTimes = laserReactionTimes[np.isfinite(laserReactionTimes)]

        controlDecisionTimes = decisionTimes[trialsEachLaser[:, 0]]
        controlDecisionTimes = controlDecisionTimes[np.isfinite(controlDecisionTimes)]
        laserDecisionTimes = decisionTimes[trialsEachLaser[:, 1]]
        laserDecisionTimes = laserDecisionTimes[np.isfinite(laserDecisionTimes)]

        # -- plot reaction times for 0.25 octaves and laser presentation --
        axHist = plt.subplot(gs[0, 0])

        bins = np.linspace(0, 0.5, 12)
        n, bins, patches = plt.hist([controlReactionTimes, laserReactionTimes], bins=bins, color=['k', faceColour[indType]],
                 density=True)
        plt.setp(patches[0], edgecolor='k')
        plt.setp(patches[1], edgecolor=colour[indType], lw=1.5)

        axHist.set_xlabel('Sampling time (s)')

        extraplots.boxoff(axHist)

        # -- plot change in reaction time for each bandwidth and laser presentation --
        axScatter = plt.subplot(gs[0, 1])

        barLoc = np.array([-0.24, 0.24])
        xLocs = np.arange(len(numBands))
        xTickLabels = numBands

        for indBand in range(len(numBands)):
            trialsEachLaser = trialsEachCond[:, :, indBand]

            laserReactionTimes = reactionTimes[trialsEachLaser[:, 1]]
            laserReactionTimes = laserReactionTimes[np.isfinite(laserReactionTimes)]
            thisLaserReaction = np.mean(laserReactionTimes)

            controlReactionTimes = reactionTimes[trialsEachLaser[:, 0]]
            controlReactionTimes = controlReactionTimes[np.isfinite(controlReactionTimes)]
            thisControlReaction = np.mean(controlReactionTimes)

            thisxLocs = barLoc + xLocs[indBand]

            plt.plot(thisxLocs, [thisControlReaction, thisLaserReaction], '-',
                         color='k')

            l1, = plt.plot(thisxLocs[1], thisLaserReaction, 'o', mec=colour[indType], mfc=faceColour[indType])
            l2, = plt.plot(thisxLocs[0], thisControlReaction, 'o', mec='k', mfc='k')

            # median = np.median(accuracyData, axis=0)
            # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
        axScatter.legend([l2, l1], ['control', legendLabel[indType]], loc='best')

        axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(np.tile(xTickLabels, len(xLocs)))
        axScatter.set_xlabel('Masker bandwidth (oct)')

        axScatter.set_ylim(0.05,0.2)
        axScatter.set_ylabel('Sampling time (s)')

        extraplots.boxoff(axScatter)

        # -- plot histogram of decision times for 0.25 octaves and each laser presentation --
        axHist = plt.subplot(gs[0, 2])

        bins = np.linspace(0.1, 0.8, 12)
        n, bins, patches = plt.hist([controlDecisionTimes, laserDecisionTimes], bins=bins, color=['k', faceColour[indType]],
                                    density=True)
        plt.setp(patches[0], edgecolor='k')
        plt.setp(patches[1], edgecolor=colour[indType], lw=1.5)

        axHist.set_xlabel('Time to decision (s)')

        extraplots.boxoff(axHist)

        # -- plot change in decision time for each bandwidth and laser presentation --
        axScatter = plt.subplot(gs[0, 3])

        barLoc = np.array([-0.24, 0.24])
        xLocs = np.arange(len(numBands))
        xTickLabels = numBands

        for indBand in range(len(numBands)):
            trialsEachLaser = trialsEachCond[:, :, indBand]

            laserDecisionTimes = decisionTimes[trialsEachLaser[:, 1]]
            laserDecisionTimes = laserDecisionTimes[np.isfinite(laserDecisionTimes)]
            thisLaserDecision = np.mean(laserDecisionTimes)

            controlDecisionTimes = decisionTimes[trialsEachLaser[:, 0]]
            controlDecisionTimes = controlDecisionTimes[np.isfinite(controlDecisionTimes)]
            thisControlDecision = np.mean(controlDecisionTimes)

            thisxLocs = barLoc + xLocs[indBand]

            plt.plot(thisxLocs, [thisControlDecision, thisLaserDecision], '-',
                     color='k')

            l1, = plt.plot(thisxLocs[1], thisLaserDecision, 'o', mec=colour[indType], mfc=faceColour[indType])
            l2, = plt.plot(thisxLocs[0], thisControlDecision, 'o', mec='k', mfc='k')

        axScatter.legend([l2, l1], ['control', legendLabel[indType]], loc='best')

        axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(np.tile(xTickLabels, len(xLocs)))
        axScatter.set_xlabel('Masker bandwidth (oct)')

        axScatter.set_ylim(0.2, 0.5)
        axScatter.set_ylabel('Decision time (s)')

        extraplots.boxoff(axScatter)

        # -- save fig --
        plt.suptitle(mouse + ' ({})'.format(mouseLabel[indType]))

        figFilename = f'{mouse}_behav_report_{sessionType}'
        extraplots.save_figure(figFilename, 'png', [12, 4], '/tmp/')
