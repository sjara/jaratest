import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pdb
animal = 'adap041'
#noiseburstSessType = 'noiseburst'
#tuningSessType = 'tc'
tuningIntensities = [40, 50, 60, 70]
plotAll = True

databaseFullPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(animal))
key = 'head_fixed'
qualityThreshold = 3 #2
maxZThreshold = 2
ISIcutoff = 0.02
#tuningIntensity = [60,50,40,30] #range(30,70,10)
celldb = pd.read_hdf(databaseFullPath, key=key)

goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{}'.format(ISIcutoff, qualityThreshold))

maxZscore = goodQualCells.ZscoreEachIntensity.apply(lambda x : np.max(np.abs(x)))
goodRespCells=goodQualCells[maxZscore >= maxZThreshold]


# -- Plot reports -- #
outputDir = '/home/languo/data/ephys/head_fixed_astr/{}/responsive_freqs/'.format(animal)
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
freqs = goodQualCells.tuningFreqs.iloc[0]

if plotAll:
    cellsToPlot = goodQualCells
else:
    cellsToPlot = goodRespCells

plt.figure(figsize=(20,8)) 
#gs = gridspec.GridSpec(2,len(tuningIntensities))
numCol = len(tuningIntensities)
fig, axes = plt.subplots(nrows=2, ncols=numCol, sharex=True, sharey='row')

#gs.update(left=0.05, right=0.95, wspace=0.15, hspace=0.3)
if plotAll:
    figname = 'allgoodcells_{}_Zscore{}'.format(animal,maxZThreshold)  
else:
    figname = '{}_Zscore{}'.format(animal,maxZThreshold)  

for indr, brainArea in enumerate(np.unique(cellsToPlot.brainarea)):
    thisArea = cellsToPlot.loc[cellsToPlot.brainarea==brainArea]
    for indc, intensity in enumerate(tuningIntensities):
        zScoresThisIntensity = thisArea.tuningZscoreEachIntEachFreq.apply(lambda x: x[indc]) #select just the zScores for that intensity
        responseEachFreqThisIntensity = zScoresThisIntensity.apply(lambda x: (np.abs(x)>=maxZThreshold).astype(int))
        responsiveCountsEachFreq = responseEachFreqThisIntensity.sum()
        # -- Plot one report for each brain area for each intensity -- #
        subtitle = '{}_{}dB'.format(brainArea,intensity)  
        print 'ploting {}'.format(subtitle)
        #ax = plt.subplot(2,numCol, 1+indr*numCol+indc) 
        #pdb.set_trace()
        ax = axes[indr, indc]
        #ax = plt.subplot(gs[indr, indc])
        log2Freqs = np.log2(freqs)
        ax.bar(log2Freqs,responsiveCountsEachFreq,width=0.3,align='center')       
        #plt.hist(responsiveCountsEachFreq, 16, facecolor='green', alpha=0.75)
        ax.set_ylabel('Num of responsive cells')
        ax.set_xlabel('Frequency of tones (kHz)')
        #plt.xscale('log')
        xLabels = np.around(freqs/1000, 1)
        ax.set_xticks(log2Freqs)
        ax.set_xticklabels(xLabels, fontsize=6)
        ax.set_xlim([np.log2(min(freqs))-0.1,np.log2(max(freqs))+0.1])
        ax.set_title(subtitle)
fig.set_tight_layout({'rect': [0, 0, 1, 0.95], 'w_pad': 0.3, 'h_pad': 0.3})  
plt.suptitle(figname)
#plt.grid(True)
figFullPath = os.path.join(outputDir, figname)
plt.savefig(figFullPath, format='png')
print 'Saving figure {}'.format(figname)



