import os
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
reload(settings)
from jaratoolbox import extraplots
from jaratoolbox import extrastats
import figparams
from scipy import stats
reload(figparams)


FIGNAME = 'reward_change_behavior_times'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'figure_reward_change_behavior_times' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
#figSize = [7, 5]
figSize = [10, 8]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.015, 0.5]   # Horiz position for panel labels
labelPosY = [0.95, 0.48]    # Vert position for panel labels

colorsDict = {'more_left':figparams.colp['MoreRewardL'], 
              'more_right':figparams.colp['MoreRewardR']} 


animalShapes = {'adap005': 'o',
                'adap012': 's',
                'adap013': 'p',
                'adap015': '*',
                'adap017': 'h',
                'gosi001': '+',
                'gosi004': 'x',
                'gosi008': '1',
                'gosi010': '2',
                'adap067': '3',
                'adap071': '4'}


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')


gs = gridspec.GridSpec(2, 2)
gs.update(left=0.08, right=0.98, top=0.9, bottom=0.1, wspace=0.3, hspace=0.6)
ax0 = plt.subplot(gs[0, 0])
ax1 = plt.subplot(gs[0, 1])
ax2 = plt.subplot(gs[1, 0])
ax3 = plt.subplot(gs[1, 1])

summaryFilename = 'rc_behavior_reaction_and_response_times.npz'
#'rc_rightward_choice_each_condition_by_freq_summary.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
summary = np.load(summaryFullPath)

modulationWindow = [0, 0.3]

# for animal in animalShapes.keys():
#     for times in ['reactionTime', 'responseTime']:
#         for choice in ['LeftChoice', 'RightChoice']:
#             relevantTimes = [item for item in summary.keys() if ((animal in item) and (times in item) and (choice in item))]
#             for item in relevantTimes:
#                 print('{} trial number:{}, average {}s'
#                     .format(item, len(summary[item]), np.mean(summary[item])))


ax0.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                fontsize=fontSizePanel, fontweight='bold')
allMiceMeanLeftMore = []
allMiceMeanRightMore = []
for (animal,shape) in animalShapes.items():
    reactionTimeLeftwardLeftMore = summary[animal+'_reactionTimeLeftChoiceMoreLeft']
    meanReactionTimeLeftwardLeftMore = np.mean(reactionTimeLeftwardLeftMore)
    reactionTimeLeftwardRightMore = summary[animal+'_reactionTimeLeftChoiceMoreRight']
    meanReactionTimeLeftwardRightMore = np.mean(reactionTimeLeftwardRightMore)
    print('{} mean reaction times moving leftward (ipsi, contra more reward): {}'
        .format(animal, [meanReactionTimeLeftwardLeftMore,meanReactionTimeLeftwardRightMore]))
    allMiceMeanLeftMore.append(meanReactionTimeLeftwardLeftMore)
    allMiceMeanRightMore.append(meanReactionTimeLeftwardRightMore)
    ax0.plot([1,2], [meanReactionTimeLeftwardLeftMore,meanReactionTimeLeftwardRightMore],
     marker=shape, color='k')
ax0.set_ylabel('Reaction time (s)')
ax0.set_xlim([0.5, 2.5])
extraplots.boxoff(ax0)
zScore,pVal = stats.ranksums(allMiceMeanLeftMore, allMiceMeanRightMore)
print('reaction time leftward p={}'.format(pVal))

ax1.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                 fontsize=fontSizePanel, fontweight='bold')
allMiceMeanLeftMore = []
allMiceMeanRightMore = []
for (animal,shape) in animalShapes.items():
    reactionTimeRightwardLeftMore = summary[animal+'_reactionTimeRightChoiceMoreLeft']
    meanReactionTimeRightwardLeftMore = np.mean(reactionTimeRightwardLeftMore)
    reactionTimeRightwardRightMore = summary[animal+'_reactionTimeRightChoiceMoreRight']
    meanReactionTimeRightwardRightMore = np.mean(reactionTimeRightwardRightMore)
    print('{} mean reaction times moving rightward (ipsi, contra more reward): {}'
        .format(animal, [meanReactionTimeRightwardLeftMore,meanReactionTimeRightwardRightMore]))
    allMiceMeanLeftMore.append(meanReactionTimeRightwardLeftMore)
    allMiceMeanRightMore.append(meanReactionTimeRightwardRightMore)
    ax1.plot([1,2], [meanReactionTimeRightwardRightMore,meanReactionTimeRightwardLeftMore], 
        marker=shape, color='k')
ax1.set_xlim([0.5, 2.5])
extraplots.boxoff(ax1)
zScore,pVal = stats.ranksums(allMiceMeanLeftMore, allMiceMeanRightMore)
print('reaction time rightward p={}'.format(pVal))


ax2.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
                fontsize=fontSizePanel, fontweight='bold')
allMiceMeanLeftMore = []
allMiceMeanRightMore = []
allMiceLeftMoreRemoved = []
allMiceRightMoreRemoved = []
for (animal,shape) in animalShapes.items():
    responseTimeLeftwardLeftMore = summary[animal+'_responseTimeLeftChoiceMoreLeft']
    meanResponseTimeLeftwardLeftMore = np.mean(responseTimeLeftwardLeftMore)
    responseTimeLeftwardRightMore = summary[animal+'_responseTimeLeftChoiceMoreRight']
    meanResponseTimeLeftwardRightMore = np.mean(responseTimeLeftwardRightMore)
    print('{} mean response times moving leftward (ipsi, contra more reward): {}'
        .format(animal, [meanResponseTimeLeftwardLeftMore,meanResponseTimeLeftwardRightMore]))
    allMiceMeanLeftMore.append(meanResponseTimeLeftwardLeftMore)
    allMiceMeanRightMore.append(meanResponseTimeLeftwardRightMore)
    proportionSideInBeforeModWindow = sum(responseTimeLeftwardLeftMore< modulationWindow[-1]) / float(len(responseTimeLeftwardLeftMore))
    allMiceLeftMoreRemoved.append(proportionSideInBeforeModWindow)
    proportionSideInBeforeModWindow = sum(responseTimeLeftwardRightMore< modulationWindow[-1]) / float(len(responseTimeLeftwardRightMore))
    allMiceRightMoreRemoved.append(proportionSideInBeforeModWindow)
    ax2.plot([1,2], [meanResponseTimeLeftwardLeftMore,meanResponseTimeLeftwardRightMore], 
        marker=shape, color='k')
ax2.set_ylabel('Response time (s)')
ax2.set_xticks([1,2])
ax2.set_xticklabels(['More same side', 'More contra side'], fontsize=fontSizeLabels)
ax2.set_xlabel('Leftward trials', fontsize=fontSizeLabels)
ax2.set_xlim([0.5, 2.5])
extraplots.boxoff(ax2)
zScore,pVal = stats.ranksums(allMiceMeanLeftMore, allMiceMeanRightMore)
print('response time leftward p={}'.format(pVal))
print('response time leftward left more {}%, right more {}% shorter than {}s'
    .format(np.mean(allMiceLeftMoreRemoved)*100, np.mean(allMiceRightMoreRemoved)*100, modulationWindow[-1]))


ax3.annotate('D', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
                 fontsize=fontSizePanel, fontweight='bold')
allMiceMeanLeftMore = []
allMiceMeanRightMore = []
allMiceLeftMoreRemoved = []
allMiceRightMoreRemoved = []
for (animal,shape) in animalShapes.items():
    responseTimeRightwardLeftMore = summary[animal+'_responseTimeRightChoiceMoreLeft']
    meanResponseTimeRightwardLeftMore = np.mean(responseTimeRightwardLeftMore)
    responseTimeRightwardRightMore = summary[animal+'_responseTimeRightChoiceMoreRight']
    meanResponseTimeRightwardRightMore = np.mean(responseTimeRightwardRightMore)
    print('{} mean response times moving rightward (ipsi, contra more reward): {}'
        .format(animal, [meanResponseTimeRightwardLeftMore,meanResponseTimeRightwardRightMore]))
    allMiceMeanLeftMore.append(meanResponseTimeRightwardLeftMore)
    allMiceMeanRightMore.append(meanResponseTimeRightwardRightMore)
    proportionSideInBeforeModWindow = sum(responseTimeRightwardLeftMore< modulationWindow[-1]) / float(len(responseTimeRightwardLeftMore))
    allMiceLeftMoreRemoved.append(proportionSideInBeforeModWindow)
    proportionSideInBeforeModWindow = sum(responseTimeRightwardRightMore< modulationWindow[-1]) / float(len(responseTimeRightwardRightMore))
    allMiceRightMoreRemoved.append(proportionSideInBeforeModWindow)
    ax3.plot([1,2], [meanResponseTimeRightwardRightMore,meanResponseTimeRightwardLeftMore], 
        marker=shape, color='k')
ax3.set_xticks([1,2])
ax3.set_xticklabels(['More same side', 'More contra side'], fontsize=fontSizeLabels)
ax3.set_xlabel('Rightward trials', fontsize=fontSizeLabels)
ax3.set_xlim([0.5, 2.5])
extraplots.boxoff(ax3)
zScore,pVal = stats.ranksums(allMiceMeanLeftMore, allMiceMeanRightMore)
print('response time rightward p={}'.format(pVal))
print('response time rightward left more {}%, right more {}% shorter than {}s'
    .format(np.mean(allMiceLeftMoreRemoved)*100, np.mean(allMiceRightMoreRemoved)*100, modulationWindow[-1]))


    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)


plt.show()