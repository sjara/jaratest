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

FIGNAME = 'dif_fr_by_reward_sorted_center-out'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
STUDY_NAME = figparams.STUDY_NAME
binWidth = 0.01
removeSideInTrials = True
movementSelWin = [0.0,0.3]

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'figure_dif_fr_by_reward_sorted_centerout_{}ms_bin'.format(int(binWidth*1000)) # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
#figSize = [7, 5]
figSize = [8, 10]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.015, 0.45]   
labelPosY = [0.9]    

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')


if removeSideInTrials:
	dataFilename = 'average_spike_count_by_rc_cond_preferred_direction_{}ms_bin_{}_win_removed_sidein_trials.npz'.format(int(binWidth*1000), movementSelWin)
else:
	dataFilename = 'average_spike_count_by_rc_cond_preferred_direction_{}ms_bin_{}_win.npz'.format(int(binWidth*1000), movementSelWin)

dataFilePath = os.path.join(dataDir, dataFilename)
data = np.load(dataFilePath)
aveSpikeCountByBlock = data['aveSpikeCountByBlock']
timeBinEdges = np.around(data['timeVec'], decimals=2)
brainAreaEachCell = data['brainAreaEachCell']
#soundRespInds = data['soundRespInds']
#binWidth = np.around(data['binWidth'], decimals=2)
timePeriodToPlot = [0.0, 0.3]
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
	#absSpikeDifEachCellThisArea = absSpikeDifEachCell[:, cellsThisArea]
	#maxDifBinEachCellThisArea = np.argmax(absSpikeDifEachCellThisArea, axis=0)
	#cellReInd = np.argsort(maxDifBinEachCellThisArea)
	#sortedAbsSpikeDifEachCellThisArea = absSpikeDifEachCellThisArea[:, cellReInd]
	#sortedAbsSpikeDifEachCell[:, cellsThisArea] = sortedAbsSpikeDifEachCellThisArea

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
	
	ax = plt.subplot(1,2,indA+1)
	#ax.imshow(np.transpose(sortedAbsSpikeDifEachCellThisArea), origin='lower', cmap='viridis', interpolation='nearest')
	ax.imshow(np.transpose(sortedSpikeDifIndEachCellThisArea), origin='lower', cmap='coolwarm', 
		vmin=-1, vmax=1, interpolation='nearest', aspect='auto')
	ax.set_xticks([0,numOfBins])#np.arange(len(timeBinEdges))[::10])
	ax.set_xticklabels(timePeriodToPlot)
	#ax.set_xticklabels([0, 0.1, 0.2])
	#xticklabels = ['{:.1f}'.format(x) for x in xticks]
	#ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:g}"))
	#plt.yticks([150, 50], brainAreaLabels)
	ax.set_yticks([0,50,100])
	ax.set_ylabel('{}\nCell number'.format(brainArea))
	ax.set_xlabel('Time from movement onset (sec)')

plt.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.15, wspace=0.4, hspace=0.5)

# Stats #
zScore, pVal = stats.ranksums(*maxDifBinEachCellBothAreas)
print('Using bin width of {}s in time period {}, compare time bin number for peak difference between the two brain areas yielded p value of {:.3f} using Wilcoxon rank sums test.'
	.format(binWidth, timePeriodToPlot, pVal))

#plt.tight_layout()
if SAVE_FIGURE:
	extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

plt.show()
