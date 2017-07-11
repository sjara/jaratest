import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pdb

animalLists = [['adap042', 'adap043'], ['adap044', 'adap046']]
labels = ['low_freq_go_left', 'low_freq_go_right']
tuningIntensities = [40, 50, 60, 70]
plotAll = True

qualityThreshold = 3 #2
maxZThreshold = 2
ISIcutoff = 0.02

for label,animalList in zip(labels, animalLists):
    # -- Make composite celldb -- #
    allMiceDfs = []
    for animal in animalList:
        databaseFullPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(animal))
        key = 'head_fixed'
        celldbThisMouse = pd.read_hdf(databaseFullPath, key=key)
        allMiceDfs.append(celldbThisMouse)
    celldb = pd.concat(allMiceDfs, ignore_index=True)


    # -- Plot histogram of responsive freqs by hemi (!only for those TTs that are in striatum!) -- #  
    goodQualCells = celldb.query("isiViolations<{} and shapeQuality>{} and astrRegion!='undetermined'".format(ISIcutoff, qualityThreshold))

    maxZscore = goodQualCells.ZscoreEachIntensity.apply(lambda x : np.max(np.abs(x)))
    goodRespCells=goodQualCells[maxZscore >= maxZThreshold]


    # -- Plot reports -- #
    outputDir = '/home/languo/data/ephys/head_fixed_astr/all_mice/responsive_freqs_by_hemi/'
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    freqs = goodQualCells.tuningFreqs.iloc[0]

    if plotAll:
        cellsToPlot = goodQualCells
    else:
        cellsToPlot = goodRespCells

    plt.figure(figsize=(30,8)) 
    #gs = gridspec.GridSpec(2,len(tuningIntensities))
    numCol = len(tuningIntensities)
    fig, axes = plt.subplots(nrows=2, ncols=numCol, sharex=True, sharey='row')

    #gs.update(left=0.05, right=0.95, wspace=0.15, hspace=0.3)
    if plotAll:
        figname = 'allgoodcells_Zscore{}_{}'.format(maxZThreshold,label)  
    else:
        figname = 'soundrescells_Zscore{}_{}'.format(maxZThreshold,label)  

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
            #ax.set_ylabel('Num of responsive cells')
            #ax.set_xlabel('Frequency of tones (kHz)')
            #plt.xscale('log')
            xLabels = np.around(freqs/1000, 1)
            ax.set_xticks(log2Freqs)
            ax.set_xticklabels(xLabels, fontsize=8, rotation=90)
            ax.set_xlim([np.log2(min(freqs))-0.1,np.log2(max(freqs))+0.1])
            ax.set_title(subtitle, fontsize=10)
    
    fig.text(0.5, 0.02, 'Frequency of tones (kHz)', ha='center', va='center')
    fig.text(0.02, 0.5, 'Num of responsive cells', ha='center', va='center', rotation='vertical')
    fig.set_tight_layout({'rect': [0.02, 0.02, 1, 0.95], 'w_pad': 0.06, 'h_pad': 0.06})  
    plt.suptitle(figname)
    #plt.grid(True)
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath, format='png')
    print 'Saving figure {}'.format(figname)



