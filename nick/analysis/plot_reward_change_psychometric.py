import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots
from jaratoolbox import extrastats
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import colorpalette


def plot_ave_psycurve_reward_change(animal, sessions):
    FREQCOLORS =  ['0.3',
                   colorpalette.TangoPalette['Orange2'],
                   colorpalette.TangoPalette['SkyBlue2']]

    allBehavDataThisAnimal = behavioranalysis.load_many_sessions(animal,sessions)
    targetFrequency = allBehavDataThisAnimal['targetFrequency']
    choice=allBehavDataThisAnimal['choice']
    valid=allBehavDataThisAnimal['valid']& (choice!=allBehavDataThisAnimal.labels['choice']['none'])
    choiceRight = choice==allBehavDataThisAnimal.labels['choice']['right']
    currentBlock = allBehavDataThisAnimal['currentBlock']
    blockTypes = [allBehavDataThisAnimal.labels['currentBlock']['same_reward'],allBehavDataThisAnimal.labels['currentBlock']['more_left'],allBehavDataThisAnimal.labels['currentBlock']['more_right']]
    #blockTypes = [allBehavDataThisAnimal.labels['currentBlock']['more_left'],allBehavDataThisAnimal.labels['currentBlock']['more_right']]
    blockLabels = ['same_reward','more_left','more_right']
    #blockLabels = ['more_left','more_right']
    trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)

    nFreqs = len(np.unique(targetFrequency))
    #print trialsEachType
    nBlocks = len(blockTypes)
    #thisAnimalPos = inda
    #ax1=plt.subplot(gs[thisAnimalPos])
    #plt.clf()
    fontsize = 12
    allPline = []
    blockLegends = []
    fractionHitsEachValueAllBlocks = np.empty((nBlocks,nFreqs))

    for blockType in range(nBlocks):
        if np.any(trialsEachType[:,blockType]):
            targetFrequencyThisBlock = targetFrequency[trialsEachType[:,blockType]]
            validThisBlock = valid[trialsEachType[:,blockType]]
            choiceRightThisBlock = choiceRight[trialsEachType[:,blockType]]
            #currentBlockValue = currentBlock[trialsEachBlock[0,block]]
            (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
            behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)


            logPossibleValues = np.log2(possibleValues)
            lowerFreqConstraint = logPossibleValues[1]
            upperFreqConstraint = logPossibleValues[-2]
            maxFreq = max(logPossibleValues)
            minFreq = min(logPossibleValues)

            constraints = ( 'Uniform({}, {})'.format(lowerFreqConstraint, upperFreqConstraint),
                            'Uniform(0,5)' ,
                            'Uniform(0,1)',
                            'Uniform(0,1)')
            estimate = extrastats.psychometric_fit(logPossibleValues,
                                                nTrialsEachValue,
                                                nHitsEachValue,
                                                constraints)


            fractionHitsEachValueAllBlocks[blockType,:] = fractionHitsEachValue

            upperWhisker = ciHitsEachValue[1,:]-fractionHitsEachValue
            lowerWhisker = fractionHitsEachValue-ciHitsEachValue[0,:]

            xRange = logPossibleValues[-1]-logPossibleValues[1]
            fitxvals = np.linspace(logPossibleValues[0]-0.1*xRange,logPossibleValues[-1]+0.1*xRange,40)
            fityvals = extrastats.psychfun(fitxvals, *estimate)


	    # (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,  ciHitsEachValue,xTickPeriod=1)


            ax = plt.gca()
            ax.hold(True)
            (pline, pcaps, pbars) = ax.errorbar(logPossibleValues,
                                                100*fractionHitsEachValue,
                                                yerr = [100*lowerWhisker, 100*upperWhisker],
                                                ecolor=FREQCOLORS[blockType], fmt=None, clip_on=False)

            pdots = ax.plot(logPossibleValues, 100*fractionHitsEachValue, 'o', ms=6, mec='None', mfc=FREQCOLORS[blockType],
                            clip_on=False)
            if blockType == 0:
                pfit = ax.plot(fitxvals, 100*fityvals, color=FREQCOLORS[blockType], lw=2, clip_on=False, linestyle='--')
            else:
                pfit = ax.plot(fitxvals, 100*fityvals, color=FREQCOLORS[blockType], lw=2, clip_on=False)

            # plt.setp((pline, pcaps, pbars), color=FREQCOLORS[blockType])
            # plt.setp((pline, pbars), color=FREQCOLORS[blockType])
            # plt.setp(pdots, mfc=FREQCOLORS[blockType], mec=FREQCOLORS[blockType])
            allPline.append(pline)
            blockLegends.append(blockLabels[blockType])

            if blockType == nBlocks-1:
                plt.xlabel('Frequency (kHz)',fontsize=fontsize)
                plt.ylabel('Rightward trials (%)',fontsize=fontsize)
                extraplots.set_ticks_fontsize(plt.gca(),fontsize)
                ax.set_xticks(logPossibleValues)
                tickLabels = ['']* len(possibleValues)
                tickLabels[0] = 6.2
                tickLabels[-1] = 19.2
                ax.set_xticklabels(tickLabels)
                ax.axhline(y=50, linestyle='-', color='0.7')
                extraplots.boxoff(ax)
                # legend = plt.legend(allPline,blockLegends,loc=2) #Add the legend manually to the current Axes.
                # ax = plt.gca().add_artist(legend)
                #plt.hold(True)
        #plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
        #plt.show()
    # plt.title('%s %s-%s'%(animal,sessions[0],sessions[-1]))
    return fractionHitsEachValueAllBlocks

# animal = 'gosi004'
# sessions = [
#     '20170127a',
#     '20170128a',
#     '20170129a',
#     '20170130a',
#     '20170131a',
#     '20170201a'
#     ]

animal = 'gosi008'
sessions = [
    # '20170817a',
    '20170210a',
    #  '20170211a',
    '20170212a',
    '20170213a',
    '20170214a',
    '20170215a'
    ]

plt.clf()
figName = "{}_{}-{}.svg".format(animal, sessions[0], sessions[-1])
plot_ave_psycurve_reward_change(animal, sessions)
plt.savefig('/mnt/jarahubdata/reports/nick/figsForPoster/{}.svg'.format(figName))
plt.show()
