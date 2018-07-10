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

if bestFreqOnly:
	dataFilename = 'average_spike_count_by_rc_cond_best_freq.npz'
else:
	dataFilename = 'average_spike_count_by_rc_cond_all_freqs.npz'
dataFilePath = os.path.join(dataDir, dataFilename)
data = np.load(dataFilePath)
aveSpikeCountByBlock = data['aveSpikeCountByBlock']
timeBinEdges = data['timeVec']
brainAreaEachCell = data['brainAreaEachCell']
#soundRespInds = data['soundRespInds']
binWidth = data['binWidth']

absSpikeDifEachCell = np.abs(aveSpikeCountByBlock[0,:,:] - aveSpikeCountByBlock[1,:,:])

sortedAbsSpikeDifEachCell = np.zeros(absSpikeDifEachCell.shape)
for brainArea in np.unique(brainAreaEachCell):
	cellsThisArea = brainAreaEachCell==brainArea
	absSpikeDifEachCellThisArea = absSpikeDifEachCell[:, cellsThisArea]
	maxDifBinEachCellThisArea = np.argmax(absSpikeDifEachCellThisArea, axis=0)
	cellReInd = np.argsort(maxDifBinEachCellThisArea)
	sortedAbsSpikeDifEachCellThisArea = absSpikeDifEachCellThisArea[:, cellReInd]
	sortedAbsSpikeDifEachCell[:, cellsThisArea] = sortedAbsSpikeDifEachCellThisArea

brainAreaLabels = np.unique(brainAreaEachCell)

fig, ax = plt.subplots()
ax.imshow(np.transpose(sortedAbsSpikeDifEachCell), cmap='viridis', interpolation='nearest')
ax.set_xticks(np.arange(len(timeBinEdges))[::10])
xticks = np.arange(timeBinEdges[0], timeBinEdges[-1], binWidth*10)
xticklabels = ['{:.1f}'.format(x) for x in xticks]
ax.set_xticklabels(xticklabels)

#ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:g}"))
plt.yticks([150, 50], brainAreaLabels)
plt.xlabel('Time from sound onset (sec)')
plt.show()
