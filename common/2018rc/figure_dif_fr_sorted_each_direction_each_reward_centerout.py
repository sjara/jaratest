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
figFilename = 'figure_dif_fr_sorted_each_dir_each_rw_centerout_{}ms_bin'.format(int(binWidth*1000)) # Do not include extension
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


dataFilename = 'average_spike_count_by_rc_cond_by_direction_{}ms_bin.npz'.format(int(binWidth*1000))
dataFilePath = os.path.join(dataDir, dataFilename)
data = np.load(dataFilePath)

timeBinEdges = np.around(data['timeVec'], decimals=2)
timePeriodToPlot = [0, 0.3]
startInd = list(timeBinEdges).index(timePeriodToPlot[0])
endInd = list(timeBinEdges).index(timePeriodToPlot[1])
numOfBins = endInd - startInd

aveFrLeftwardLeftMoreAllCells = data['aveFrLeftwardLeftMoreAllCells'][:, startInd:endInd]
aveFrLeftwardRightMoreAllCells = data['aveFrLeftwardRightMoreAllCells'][:, startInd:endInd]
aveFrRightwardLeftMoreAllCells = data['aveFrRightwardLeftMoreAllCells'][:, startInd:endInd]
aveFrRightwardRightMoreAllCells = data['aveFrRightwardRightMoreAllCells'][:, startInd:endInd]

brainAreaEachCell = data['brainAreaEachCell']
maxSpkCountAllCondsAllCells = np.max(np.concatenate((aveFrLeftwardLeftMoreAllCells,
	aveFrLeftwardRightMoreAllCells,
	aveFrRightwardLeftMoreAllCells,
	aveFrRightwardRightMoreAllCells)))  
minSpkCountAllCondsAllCells = np.min(np.concatenate((aveFrLeftwardLeftMoreAllCells,
	aveFrLeftwardRightMoreAllCells,
	aveFrRightwardLeftMoreAllCells,
	aveFrRightwardRightMoreAllCells))) 

brainAreaLabels = np.unique(brainAreaEachCell)

for indA,brainArea in enumerate(brainAreaLabels):
	cellsThisArea = brainAreaEachCell==brainArea
	aveFrLeftwardLeftMoreThisArea = aveFrLeftwardLeftMoreAllCells[cellsThisArea, :]
	aveFrLeftwardRightMoreThisArea = aveFrLeftwardRightMoreAllCells[cellsThisArea, :]
	aveFrRightwardLeftMoreThisArea = aveFrRightwardLeftMoreAllCells[cellsThisArea, :]
	aveFrRightwardRightMoreThisArea = aveFrRightwardRightMoreAllCells[cellsThisArea, :]
	
	for indC, aveSpkCountMat in enumerate([aveFrLeftwardLeftMoreThisArea,
		aveFrLeftwardRightMoreThisArea,
		aveFrRightwardLeftMoreThisArea,
		aveFrRightwardRightMoreThisArea]):
		maxBinEachCellThisArea = np.argmax(aveSpkCountMat, axis=1)
		cellReInd = np.argsort(maxBinEachCellThisArea)
		#pdb.set_trace()
		sortedSpkCountEachCellThisArea = aveSpkCountMat[cellReInd, :]
	
		ax = plt.subplot(2,4,indA*4+indC+1)
		ax.imshow(sortedSpkCountEachCellThisArea, origin='lower', cmap='viridis', 
			vmin=minSpkCountAllCondsAllCells, vmax=maxSpkCountAllCondsAllCells, interpolation='nearest')
		ax.set_xticks(range(numOfBins+1)[::10])#np.arange(len(timeBinEdges))[::10])
		ax.set_xticklabels([0. , 0.1, 0.2, 0.3])
		ax.set_yticks([0,50,100])
		ax.set_ylabel('{}\nCell number'.format(brainArea))
plt.gca().set_xlabel('Time from movement onset (sec)')

plt.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.15, wspace=0.2, hspace=0.2)

if SAVE_FIGURE:
	extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

plt.show()
