import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
import matplotlib.gridspec as gridspec
import matplotlib
import figparams
reload(figparams)
import matplotlib.patches as mpatches
import scipy.stats as stats

FIGNAME = 'reward_modulation_sound_extra'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
STUDY_NAME = figparams.STUDY_NAME

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

SAVE_FIGURE = 1
outputDir = '/tmp/'

figFilename = 'figure_reward_modulation_sound_extra'
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [10,5]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
#labelDis = 0.1

labelPosX = [0.015, 0.55]   # Horiz position for panel labels
labelPosY = [0.97, 0.58, 0.2]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 4)
gs.update(left=0.15, right=0.96, top=0.85, bottom=0.1, wspace=0.55, hspace=1)

brainAreas = ['rightAC','rightAStr']
cellTypes = ['responsive', 'nonresponsive']
modWindows = ['0-0.1s', '-0.1-0s']

for indA, brainArea in enumerate(brainAreas):
	for indT, cellType in enumerate(cellTypes):
		for indW, modWindow in enumerate(modWindows):

			ax = plt.subplot(gs[indA, indW+indT*2])
			#ax.annotate('E', xy=(labelPosX[0],labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

			summaryFilename = 'summary_reward_modulation_sound_{}_{}_{}_cells.npz'.format(modWindow, brainArea, cellType)
			summaryFullPath = os.path.join(dataDir, summaryFilename)
			summary = np.load(summaryFullPath)
			soundResp = summary['soundResponsive']
			sigModI = summary['sigModI']
			nonsigModI = summary['nonsigModI']
			allModI = summary['allModI']

			binsEdges = np.linspace(-1,1,20)
			plt.hist([sigModI,nonsigModI], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True)
			yPosText = 1.1*plt.ylim()[1]
			#plt.text(-0.5,yPosText,'Contra',ha='center',fontsize=fontSizeLabels)
			#plt.text(0.5,yPosText,'Ipsi',ha='center',fontsize=fontSizeLabels)
			plt.text(-0.2,yPosText, '{}\n{} window\n{}'.format(brainArea,modWindow,cellType), 
				ha='center',fontsize=fontSizeLabels)
			plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
			extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
			#plt.xlabel('Reward modulation index\n(sound period)', fontsize=fontSizeLabels)
			plt.ylabel('Number of cells', fontsize=fontSizeLabels)
			extraplots.boxoff(plt.gca())

			# -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
			print('#############################################')
			print('{} has {} sound responsive good cells and {} non-responsive cells'
				.format(brainArea, sum(soundResp), sum(~soundResp)))
			print('Among {} cells, in {} window, {} cells were significantly modulated'
				.format(cellType, modWindow, len(sigModI)))
			(Z, pVal) = stats.wilcoxon(allModI)
			print('Mean mod index is {:.3f}.\nUsing the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of {:.3f}'
				.format(np.mean(allModI), pVal))
			#(Z, pVal) = stats.wilcoxon(sigModI)
			#print('For significantly modulated {} cells in {}: Mean mod index is {:.3f}. Using the Wilcoxon signed-rank test, comparing the modulation index distribution to zero yielded a p value of {:.3f}'
			#	.format(cellType, brainArea, np.mean(sigModI), pVal))

if SAVE_FIGURE:
	extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

plt.show()
