import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import figparams
reload(figparams)
import scipy.stats as stats

FIGNAME = 'dif_fr_sorted_center-out'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
STUDY_NAME = figparams.STUDY_NAME
binWidth = 0.01

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'figure_fr_sorted_by_reward_centerout_{}ms_bin'.format(int(binWidth*1000)) # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
#figSize = [7, 8]
figSize = [8, 10]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.015, 0.45]   
labelPosY = [0.9]    

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

#gs = gridspec.GridSpec(1, 2)
#gs.update(left=0.1, right=0.97, top=0.97, bottom=0.06, wspace=0.5, hspace=1.7)

dataFilename = 'average_spike_count_by_rc_cond_preferred_direction_{}ms_bin.npz'.format(int(binWidth*1000))
dataFilePath = os.path.join(dataDir, dataFilename)
data = np.load(dataFilePath)
aveSpikeCountByBlock = data['aveSpikeCountByBlock']
#maxEach = np.max(aveSpikeCountByBlock, axis=1)
#aveSpikeCountByBlock = aveSpikeCountByBlock/maxEach[:,np.newaxis,:]

timeBinEdges = np.around(data['timeVec'], decimals=2)
brainAreaEachCell = data['brainAreaEachCell']
#soundRespInds = data['soundRespInds']
#binWidth = np.around(data['binWidth'], decimals=2)
timePeriodToPlot = [0, 0.3]
startInd = list(timeBinEdges).index(timePeriodToPlot[0])
endInd = list(timeBinEdges).index(timePeriodToPlot[1])
numOfBins = endInd - startInd
absSpikeDifEachCell = np.abs(aveSpikeCountByBlock[0,:,:] - aveSpikeCountByBlock[1,:,:])
absSpikeDifEachCell = absSpikeDifEachCell[startInd:endInd, :]
sortedAbsSpikeDifEachCell = np.zeros(absSpikeDifEachCell.shape)
# more left - more right
spikeDifIndEachCell = (aveSpikeCountByBlock[0,:,:] - aveSpikeCountByBlock[1,:,:]) / (aveSpikeCountByBlock[0,:,:] + aveSpikeCountByBlock[1,:,:])
spikeDifIndEachCell[np.isnan(spikeDifIndEachCell)] = 0 # for those bins that does not have a spike, set index to 0
spikeDifIndEachCell = spikeDifIndEachCell[startInd:endInd, :]

brainAreaLabels = np.unique(brainAreaEachCell)
maxDifBinEachCellBothAreas = []
for indA,brainArea in enumerate(brainAreaLabels):
	cellsThisArea = brainAreaEachCell==brainArea
	
	aveSpikeCountThisArea = aveSpikeCountByBlock[:, :, cellsThisArea]
	spikeDifIndEachCellThisArea = spikeDifIndEachCell[:, cellsThisArea]
	maxDifBinEachCellThisArea = np.argmax(np.abs(spikeDifIndEachCellThisArea), axis=0)
	maxDifBinEachCellBothAreas.append(maxDifBinEachCellThisArea)
	meanPeakBinNum = np.mean(maxDifBinEachCellThisArea)
	medianPeakBinNum = np.median(maxDifBinEachCellThisArea)
	print('For {}, mean peak bin number is {}, median peak bin number is {}'.format(brainArea, meanPeakBinNum, medianPeakBinNum))
	maxDifEachCellThisArea = spikeDifIndEachCellThisArea[maxDifBinEachCellThisArea, range(len(maxDifBinEachCellThisArea))]
	negPeakDifCells = maxDifEachCellThisArea < 0
	posPeakDifCells = maxDifEachCellThisArea > 0
	cellReIndNeg = np.argsort(maxDifBinEachCellThisArea[negPeakDifCells])
	cellReIndPos = np.argsort(maxDifBinEachCellThisArea[posPeakDifCells])
	#pdb.set_trace()
	sortedSpikeDifIndEachNegPeakCell = spikeDifIndEachCellThisArea[:, negPeakDifCells][:, cellReIndNeg]
	sortedSpikeDifIndEachPosPeakCell = spikeDifIndEachCellThisArea[:, posPeakDifCells][:, cellReIndPos]
	sortedSpikeDifIndEachCellThisArea = np.hstack((sortedSpikeDifIndEachPosPeakCell, sortedSpikeDifIndEachNegPeakCell))
	
	sortedAveSpikeEachNegPeakCellLeftMoreReward = aveSpikeCountThisArea[0, startInd:endInd, negPeakDifCells][cellReIndNeg, :]
	sortedAveSpikeEachPosPeakCellLeftMoreReward = aveSpikeCountThisArea[0, startInd:endInd, posPeakDifCells][cellReIndPos, :]
	sortedAveSpikeEachCellLeftMoreReward = np.vstack((sortedAveSpikeEachPosPeakCellLeftMoreReward, sortedAveSpikeEachNegPeakCellLeftMoreReward)) 
	maxEach = np.max(sortedAveSpikeEachCellLeftMoreReward, axis=1)
	sortedAveSpikeEachCellLeftMoreReward = sortedAveSpikeEachCellLeftMoreReward/maxEach[:,np.newaxis]

	sortedAveSpikeEachNegPeakCellRightMoreReward = aveSpikeCountThisArea[1, startInd:endInd, negPeakDifCells][cellReIndNeg, :]
	sortedAveSpikeEachPosPeakCellRightMoreReward = aveSpikeCountThisArea[1, startInd:endInd, posPeakDifCells][cellReIndPos, :]
	sortedAveSpikeEachCellRightMoreReward = np.vstack((sortedAveSpikeEachPosPeakCellRightMoreReward, sortedAveSpikeEachNegPeakCellRightMoreReward)) 
	maxEach = np.max(sortedAveSpikeEachCellRightMoreReward, axis=1)
	sortedAveSpikeEachCellRightMoreReward = sortedAveSpikeEachCellRightMoreReward/maxEach[:,np.newaxis]
	
	ax1 = plt.subplot(2,3,indA*3+1)
	#ax1 = plt.subplot(gs[0,0])
	#ax.imshow(np.transpose(sortedAbsSpikeDifEachCellThisArea), origin='lower', cmap='viridis', interpolation='nearest')
	ax1.imshow(np.transpose(sortedSpikeDifIndEachCellThisArea), origin='lower', cmap='coolwarm', vmin=-1, vmax=1, interpolation='nearest')
	ax1.set_xticks(range(numOfBins+1)[::10])#np.arange(len(timeBinEdges))[::10])
	ax1.set_xticklabels([0. , 0.1, 0.2, 0.3])
	#xticklabels = ['{:.1f}'.format(x) for x in xticks]
	#ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:g}"))
	#plt.yticks([150, 50], brainAreaLabels)
	ax1.set_yticks([0,50,100])
	ax1.set_ylabel('{}\nCell number'.format(brainArea))
	ax1.set_xlabel('Time from movement onset (sec)')
	ax1.set_title('(left_more - right_more)/\n(left_more + right_more)')

	ax2 = plt.subplot(2,3,indA*3+2)
	ax2.imshow(sortedAveSpikeEachCellLeftMoreReward, origin='lower', cmap='viridis', interpolation='nearest')
	ax2.set_xticks(range(numOfBins+1)[::10])#np.arange(len(timeBinEdges))[::10])
	ax2.set_xticklabels([0. , 0.1, 0.2, 0.3])
	ax2.set_yticks([0,50,100])
	ax2.set_ylabel('{}\nCell number'.format(brainArea))
	ax2.set_xlabel('Time from movement onset (sec)')
	ax2.set_title('left_more')

	ax3 = plt.subplot(2,3,indA*3+3)
	ax3.imshow(sortedAveSpikeEachCellRightMoreReward, origin='lower', cmap='viridis', interpolation='nearest')
	ax3.set_xticks(range(numOfBins+1)[::10])#np.arange(len(timeBinEdges))[::10])
	ax3.set_xticklabels([0. , 0.1, 0.2, 0.3])
	ax3.set_yticks([0,50,100])
	ax3.set_ylabel('{}\nCell number'.format(brainArea))
	ax3.set_xlabel('Time from movement onset (sec)')
	ax3.set_title('right_more')




plt.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.15, wspace=0.2, hspace=0.2)

# Stats #
zScore, pVal = stats.ranksums(*maxDifBinEachCellBothAreas)
print('Using bin width of {}s, compare time bin number for peak difference between the two brain areas yielded p value of {:.3f} using Wilcoxon rank sums test.'.format(binWidth, pVal))

#plt.tight_layout()
if SAVE_FIGURE:
	extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

plt.show()
