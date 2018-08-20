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


FIGNAME = 'movement_selectivity'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'figure_movement_sel_control' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
#figSize = [7, 5]
figSize = [10, 8]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.015, 0.5]   # Horiz position for panel labels
labelPosY = [0.95]    # Vert position for panel labels

colorsDict = {'more_left':figparams.colp['MoreRewardL'], 
              'more_right':figparams.colp['MoreRewardR']} 


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')


gs = gridspec.GridSpec(1, 2)
gs.update(left=0.08, right=0.98, top=0.9, bottom=0.1, wspace=0.3, hspace=0.6)
ax0 = plt.subplot(gs[0, 0])
ax0.hold(True)
ax1 = plt.subplot(gs[0, 1])
ax1.hold(True)

summaryFilename = 'summary_movement_sel_cells_control_sound_resp.npz'
#'rc_rightward_choice_each_condition_by_freq_summary.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
summary = np.load(summaryFullPath)

movementSelWindow = [0, 0.3]

brainAreaEachCell = summary['brainAreaEachCell']
difCountHighSoundLvR = summary['difCountHighSoundLvR']
difCountLowSoundLvR = summary['difCountLowSoundLvR']
difCountLowvHighLeft = summary['difCountLowvHighLeft']
difCountLowvHighRight = summary['difCountLowvHighRight']
aveDifSameSoundLvR = np.mean(np.c_[difCountHighSoundLvR, difCountLowSoundLvR], axis=1)
aveDifLowvHighSameMovement = np.mean(np.c_[difCountLowvHighLeft, difCountLowvHighRight], axis=1)

ax0.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                fontsize=fontSizePanel, fontweight='bold')

cellsAC = (brainAreaEachCell == 'rightAC')

for indC in range(sum(cellsAC)):
    ax0.plot([1,2], [aveDifSameSoundLvR[cellsAC][indC], aveDifLowvHighSameMovement[cellsAC][indC]],
     marker='o', color='k')
ax0.set_ylabel('Mean difference in spike count')
ax0.set_xlim([0.5, 2.5])
ax0.set_xticks([1,2])
ax0.set_xticklabels(['same sound\ndifferent movement', 'same movement\ndifferent sound'], fontsize=fontSizeLabels)
ax0.set_title('AC')
extraplots.boxoff(ax0)
zScore,pVal = stats.wilcoxon(aveDifSameSoundLvR[cellsAC], aveDifLowvHighSameMovement[cellsAC])
print('AC p={}'.format(pVal))
careAboutMv = aveDifSameSoundLvR[cellsAC] >= aveDifLowvHighSameMovement[cellsAC]
careAboutSound = aveDifSameSoundLvR[cellsAC] < aveDifLowvHighSameMovement[cellsAC]
percentMvRelated = sum(careAboutMv) / float(len(careAboutMv)) * 100
percentSoundRelated = sum(careAboutSound) / float(len(careAboutSound)) * 100
print('AC {:.2f}% cells showed larger or equal difference between different movement directions,\n{:.2f}% show larger difference between different sounds'
    .format(percentMvRelated, percentSoundRelated))


ax1.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                 fontsize=fontSizePanel, fontweight='bold')
cellsAStr = (brainAreaEachCell == 'rightAStr')

for indC in range(sum(cellsAStr)):
    ax1.plot([1,2], [aveDifSameSoundLvR[cellsAStr][indC], aveDifLowvHighSameMovement[cellsAStr][indC]],
     marker='o', color='k')
ax1.set_ylabel('Mean difference in spike count')
ax1.set_xlim([0.5, 2.5])
ax1.set_xticks([1,2])
ax1.set_xticklabels(['same sound\ndifferent movement', 'same movement\ndifferent sound'], fontsize=fontSizeLabels)
ax1.set_title('AStr')
extraplots.boxoff(ax1)
zScore,pVal = stats.wilcoxon(aveDifSameSoundLvR[cellsAStr], aveDifLowvHighSameMovement[cellsAStr])
print('AStr p={}'.format(pVal))
careAboutMv = aveDifSameSoundLvR[cellsAStr] >= aveDifLowvHighSameMovement[cellsAStr]
careAboutSound = aveDifSameSoundLvR[cellsAStr] < aveDifLowvHighSameMovement[cellsAStr]
percentMvRelated = sum(careAboutMv) / float(len(careAboutMv)) * 100
percentSoundRelated = sum(careAboutSound) / float(len(careAboutSound)) * 100
print('AStr {:.2f}% cells showed larger or equal difference between different movement directions,\n{:.2f}% show larger difference between different sounds'
    .format(percentMvRelated, percentSoundRelated))

    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)


plt.show()