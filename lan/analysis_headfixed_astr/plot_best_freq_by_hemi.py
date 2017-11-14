import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

animal = 'adap046'
#noiseburstSessType = 'noiseburst'
#tuningSessType = 'tc'

databaseFullPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(animal))
key = 'head_fixed'
qualityThreshold = 3 #2
maxZThreshold = 3
ISIcutoff = 0.02
#tuningIntensity = [60,50,40,30] #range(30,70,10)
celldb = pd.read_hdf(databaseFullPath, key=key)

goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{}'.format(ISIcutoff, qualityThreshold))
#goodRespCells = goodQualCells.loc[abs(goodQualCells.tuningZscore) >= maxZThreshold]
maxZscore = goodQualCells.ZscoreEachIntensity.apply(lambda x : np.max(np.abs(x)))
goodRespCells=goodQualCells[maxZscore >= maxZThreshold]
freqs = goodRespCells.tuningFreqs.iloc[0]
tuningIntensities = [30, 40, 50, 60]
# -- Plot reports -- #
outputDir = '/home/languo/data/ephys/head_fixed_astr/{}/weighted_bf/'.format(animal)
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
# -- Plot a separate report for each date, brain area, tetrode, and depth -- #
for date in np.unique(goodRespCells.date):
    thisDate = goodRespCells.loc[(goodRespCells.date==date)]
    for brainArea in np.unique(thisDate.brainarea):
        for tetrode in range(1,9):
            thisTTthisArea = thisDate.loc[(thisDate.brainarea==brainArea) & (thisDate.tetrode == tetrode)]
            if len(thisTTthisArea) != 0:
                figname = '{}_{}_{}_T{}'.format(animal,brainArea,date,tetrode)  
                print 'ploting {}'.format(figname)
                plt.figure(figsize=(20,6))
                gs = gridspec.GridSpec(1,len(tuningIntensities))
                gs.update(left=0.05, right=0.95, wspace=0.15, hspace=0.1)
                for ind, intensity in enumerate(tuningIntensities):
                    ax = plt.subplot(gs[0, ind])
                    bestFreqs = thisTTthisArea.tuningWeightedBFEachIntensity.apply(lambda x: x[ind]).dropna()
                    log2Freqs = np.log2(bestFreqs)
                    plt.hist(log2Freqs, facecolor='green', alpha=0.75)
                    plt.ylabel('Num of sound responsive cells')
                    plt.xlabel('Weighted best frequency')
                    #plt.xscale('log')
                    xLabels = np.around(freqs/1000, 1)
                    #xTicks = np.logspace(np.log2(np.min(freqs)), np.log2(np.max(freqs)), num=16, base=2)
                    plt.xticks(np.log2(freqs), xLabels, fontsize=10)
                    #plt.xlim([1900, 42000])
                    plt.xlim([np.log2(min(freqs))-0.1,np.log2(max(freqs))+0.1])
                    plt.title('{}dB'.format(intensity))
                plt.suptitle(figname)
                #plt.grid(True)
                figFullPath = os.path.join(outputDir, figname)
                plt.savefig(figFullPath, format='png')
                print 'Saving figure {}'.format(figname)

# -- Plot one report for each brain area -- #
for brainArea in np.unique(goodRespCells.brainarea):
    thisArea = goodRespCells.loc[goodRespCells.brainarea==brainArea]
    figname = '{}_{}'.format(animal,brainArea)  
    print 'ploting {}'.format(figname)
    plt.figure(figsize=(20,6))
    gs = gridspec.GridSpec(1,len(tuningIntensities))
    gs.update(left=0.05, right=0.95, wspace=0.15, hspace=0.1)
    for ind, intensity in enumerate(tuningIntensities):
        ax = plt.subplot(gs[0, ind])
        bestFreqs = thisArea.tuningWeightedBFEachIntensity.apply(lambda x: x[ind]).dropna()
        #plt.xscale('log')
        log2Freqs = np.log2(bestFreqs)
        plt.hist(log2Freqs, 20, facecolor='green', alpha=0.75)
        plt.ylabel('Num of sound responsive cells')
        plt.xlabel('Weighted best frequency')
        #xTicks = np.logspace(np.log2(np.min(freqs)), np.log2(np.max(freqs)), num=16, base=2)
        xLabels = np.around(freqs/1000, 1)
        plt.xticks(np.log2(freqs), xLabels,fontsize=10)
        #plt.xlim([1900, 42000])
        plt.xlim([np.log2(min(freqs))-0.1,np.log2(max(freqs))+0.1])
        plt.title('{}dB'.format(intensity))
    plt.suptitle(figname)
    #plt.grid(True)
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath, format='png')
    print 'Saving figure {}'.format(figname)



