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

FIGNAME = 'dif_fr_sorted_sound'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
STUDY_NAME = figparams.STUDY_NAME
bestFreqOnly = True

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'figure_dif_fr_sorted_sound' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
#figSize = [7, 5]
figSize = [5, 10]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.015, 0.45]   
labelPosY = [0.9]    

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

if bestFreqOnly:
	dataFilename = 'average_spike_count_by_rc_cond_best_freq.npz'
else:
	dataFilename = 'average_spike_count_by_rc_cond_all_freqs.npz'
dataFilePath = os.path.join(dataDir, dataFilename)
data = np.load(dataFilePath)
aveSpikeCountByBlock = data['aveSpikeCountByBlock']
timeBinEdges = np.around(data['timeVec'], decimals=2)
brainAreaEachCell = data['brainAreaEachCell']
#soundRespInds = data['soundRespInds']
binWidth = data['binWidth']
timePeriodToPlot = [0, 0.1]
startInd = list(timeBinEdges).index(timePeriodToPlot[0])
endInd = list(timeBinEdges).index(timePeriodToPlot[1])
numOfBins = endInd - startInd
absSpikeDifEachCell = np.abs(aveSpikeCountByBlock[0,:,:] - aveSpikeCountByBlock[1,:,:])
absSpikeDifEachCell = absSpikeDifEachCell[startInd:endInd, :]
sortedAbsSpikeDifEachCell = np.zeros(absSpikeDifEachCell.shape)
brainAreaLabels = np.unique(brainAreaEachCell)

for indA,brainArea in enumerate(brainAreaLabels):
	cellsThisArea = brainAreaEachCell==brainArea
	absSpikeDifEachCellThisArea = absSpikeDifEachCell[:, cellsThisArea]
	maxDifBinEachCellThisArea = np.argmax(absSpikeDifEachCellThisArea, axis=0)
	cellReInd = np.argsort(maxDifBinEachCellThisArea)
	sortedAbsSpikeDifEachCellThisArea = absSpikeDifEachCellThisArea[:, cellReInd]
	sortedAbsSpikeDifEachCell[:, cellsThisArea] = sortedAbsSpikeDifEachCellThisArea

	ax = plt.subplot(1,2,indA+1)
	ax.imshow(np.transpose(sortedAbsSpikeDifEachCellThisArea), origin='lower', cmap='viridis', interpolation='nearest')
	ax.set_xticks(range(numOfBins+1)[::10])#np.arange(len(timeBinEdges))[::10])
	ax.set_xticklabels(np.arange(timePeriodToPlot[0],timePeriodToPlot[1]+0.01,binWidth*10))
	#xticklabels = ['{:.1f}'.format(x) for x in xticks]
	#ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:g}"))
	#plt.yticks([150, 50], brainAreaLabels)
	ax.set_yticks([0,50,100])
	ax.set_ylabel('{}\nCell number'.format(brainArea))
	ax.set_xlabel('Time from movement onset (sec)')

if SAVE_FIGURE:
	extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

plt.show()

