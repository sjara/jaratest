import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pdb


animalLists = [['adap005','adap012', 'adap013', 'adap015', 'adap017'], ['gosi001','gosi004', 'gosi008','gosi010']]
animalLabels = ['astr', 'ac']

modulationWindows = ['0-0.1s_sound','0-0.1s_center-out']
freqLabels = ['Low','High']
#plotAll = True
#normalized = False
#logscaled = False

qualityThreshold = 3 
maxZThreshold = 3
ISIcutoff = 0.02
alphaLevel = 0.05

for indRegion, (label,animalList) in enumerate(zip(animalLabels, animalLists)):
    # -- Make composite celldb -- #
    allMiceDfs = []
    for animal in animalList:
        databaseFullPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(animal))
        key = 'reward_change'
        celldbThisMouse = pd.read_hdf(databaseFullPath, key=key)
        allMiceDfs.append(celldbThisMouse)
    celldb = pd.concat(allMiceDfs, ignore_index=True)
    print label, len(celldb)

    # -- Plot histogram of modulation index -- #
    goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{}'.format(ISIcutoff, qualityThreshold))

    #lowFreqResponsive = goodQualCells.behavZscore.apply(lambda x: abs(x[0]) >= maxZThreshold)
    #highFreqResponsive = goodQualCells.behavZscore.apply(lambda x: abs(x[1]) >= maxZThreshold)
    #goodLowFreqRespCells=goodQualCells[lowFreqResponsive]
    #goodHighFreqRespCells=goodQualCells[highFreqResponsive]
    
    # For each window we calculated modulation index, check all good cells and all cells that response to this frequency (for sound mod) to see which cells were modulated by reward
    outputDir = '/home/languo/data/ephys/reward_change/reports/'
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)

    for indw, modWindow in enumerate(modulationWindows):
        for indf, freq in enumerate(freqLabels):
            modIndName = 'modInd'+freq+'_'+modWindow
            modSigName = 'modSig'+freq+'_'+modWindow
            allGoodCellsModInd = goodQualCells[modIndName]
            allGoodCellsModSig = goodQualCells[modSigName]
            responsiveThisFreq = goodQualCells.behavZscore.apply(lambda x: abs(x[indf]) >= maxZThreshold)
            allGoodRespCellsThisFreq = goodQualCells[responsiveThisFreq]
            respCellsModInd = allGoodRespCellsThisFreq[modIndName]
            respCellsModSig = allGoodRespCellsThisFreq[modSigName]
            
            # -- Plot reports -- #
            

    figTitle = '{}_freq_reward_modulation'.format(freq)
    
    #if plotAll:
    cellsToPlot = goodQualCells
    #else:
    #   cellsToPlot = goodRespCells

    #plt.figure(figsize=(20,20)) 
    #gs = gridspec.GridSpec(2,len(tuningIntensities))
    numCol = len(tuningIntensities)
    fig, axes = plt.subplots(nrows=4, ncols=numCol, sharex=True, sharey='row')

    #gs.update(left=0.05, right=0.95, wspace=0.15, hspace=0.3)
    if normalized:
        figname = 'allgoodcells_Zscore{}_{}_normalized'.format(maxZThreshold,label)  
    else:
        figname = 'allgoodcells_Zscore{}_{}'.format(maxZThreshold,label)  

    for indr, region in enumerate(astrRegions):
        thisRegion = cellsToPlot.loc[cellsToPlot.astrRegion==region]
        for inda, brainArea in enumerate(np.unique(cellsToPlot.brainarea)):
            thisArea = thisRegion.loc[thisRegion.brainarea==brainArea]
            for indc, intensity in enumerate(tuningIntensities):
                zScoresThisIntensity = thisArea.tuningZscoreEachIntEachFreq.apply(lambda x: x[indc]) #select just the zScores for that intensity
                #pdb.set_trace()
                responseEachFreqThisIntensity = zScoresThisIntensity.apply(lambda x: (np.abs(x)>=maxZThreshold))
                responsiveFreqsThisIntensity = pd.Series(index=np.arange(len(celldb)),dtype=object)
                for indRow, freqsThisCell in thisArea.tuningFreqs.iteritems():
                    #pdb.set_trace()
                    #responsiveFreqs.loc[indRow, label+region+brainArea+str(intensity)] = freqsThisCell[responseEachFreqThisIntensity.loc[indRow].values]
                    responsiveFreqsThisIntensity.loc[indRow] = freqsThisCell[responseEachFreqThisIntensity.loc[indRow].values]
                responsiveFreqs[label+'_'+region+'_'+brainArea+'_'+str(intensity)] = responsiveFreqsThisIntensity
                    
                responsiveCountsEachFreq = responseEachFreqThisIntensity.apply(lambda x: x.astype(int)).sum()
                if normalized:
                    responsiveCountsEachFreq = responsiveCountsEachFreq / float(np.max(responsiveCountsEachFreq)) * 100
                
                # -- Plot one report for each brain area for each intensity -- #
                subtitle = '{}_{}_{}dB'.format(brainArea,region,intensity)  
                print 'ploting {}'.format(subtitle)
                #ax = plt.subplot(2,numCol, 1+indr*numCol+indc) 
                #pdb.set_trace()
                ax = axes[2*indr+inda, indc]
                #ax = plt.subplot(gs[indr, indc])
                log2Freqs = np.log2(freqs)
                ax.bar(log2Freqs,responsiveCountsEachFreq,width=0.3,align='center')       
                #plt.hist(responsiveCountsEachFreq, 16, facecolor='green', alpha=0.75)
                #ax.set_ylabel('Num of responsive cells', fontsize=8)
                #ax.set_xlabel('Frequency of tones (kHz)', fontsize=8)
                #plt.xscale('log')
                xLabels = np.around(freqs/1000, 1)
                ax.set_xticks(log2Freqs)
                ax.set_xticklabels(xLabels, fontsize=8, rotation=90)
                ax.set_xlim([np.log2(min(freqs))-0.1,np.log2(max(freqs))+0.1])
                ax.set_title(subtitle, fontsize=10)
        #fig.tight_layout()
        fig.text(0.5, 0.02, 'Frequency of tones (kHz)', ha='center', va='center')
        fig.text(0.02, 0.5, 'Num of responsive cells', ha='center', va='center', rotation='vertical')
        fig.set_tight_layout({'rect': [0.02, 0.02, 1, 0.95], 'w_pad': 0.06, 'h_pad': 0.05})  
        plt.suptitle(figname)
        #plt.grid(True)
        #plt.show()
        figFullPath = os.path.join(outputDir, figname)
        plt.savefig(figFullPath, format='png')
        print 'Saving figure {}'.format(figname)

# -- Stats -- #
#responsiveFreqs is a big dataframe with each group as a column and each cell from the celldb as a row
from scipy import stats
import seaborn as sns
outputDir = '/home/languo/data/ephys/head_fixed_astr/all_mice/responsive_freqs_by_location/stats/'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

for intensity in tuningIntensities:
    # -- Compare all possible groups (combinations of training contingency, hemisphere, medial/lateral location) -- #
    freqsDictAllGroups = {}
    groupsThisIntensity = [col for col in responsiveFreqs.columns if str(intensity) in col]
    responsiveFreqsThisIntensity = responsiveFreqs[groupsThisIntensity].dropna(how='all')
    for name, values in responsiveFreqsThisIntensity.iteritems():
        freqs = []
        values.dropna().apply(lambda x: freqs.extend(x))
        if logscaled:
            freqs = np.log2(freqs)
        freqsDictAllGroups[name] = freqs

    plt.figure()
    colors = ['k','g','r','blue','yellow','grey','purple','magenta']
    for index, (key,value) in enumerate(sorted(freqsDictAllGroups.items())):
        sns.distplot(value, bins=20, label=key, color=colors[index], hist_kws={'facecolor':'None', 'lw':2, 'edgecolor':colors[index]})
    plt.legend()
    #plt.show()
    Hstat, pVal = stats.kruskal(*freqsDictAllGroups.values())
    if logscaled:
        print 'Using log-frequencies, for {}db, the Kruskal-Wallis H-statistic for all groups is {}, p value is {}. \n'.format(intensity, Hstat, pVal) 
        figname = '{}dB all groups responsive log-freqs'.format(intensity)
    else:
        print 'For {}db, the Kruskal-Wallis H-statistic for all groups is {}, p value is {}. \n'.format(intensity, Hstat, pVal) 
        figname = '{}dB all groups responsive freqs'.format(intensity)
    plt.title(figname)
    #pbd.set_trace()
    xExtends = plt.gca().get_xlim()
    yExtends = plt.gca().get_ylim()
    plt.text(0.5*sum(xExtends), 0.5*sum(yExtends), 'p value: {}'.format(pVal))
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath, format='png')

    # -- Compare medial vs lateral for each intensity -- #
    freqsMedial = []
    freqsLateral = []
    for name, values in responsiveFreqsThisIntensity.iteritems():
        if 'medial' in name:
            values.dropna().apply(lambda x: freqsMedial.extend(x))
        elif 'lateral' in name:
            values.dropna().apply(lambda x: freqsLateral.extend(x))
    plt.figure()
    if logscaled:
        freqsMedial = np.log2(freqsMedial)
        freqsLateral = np.log2(freqsLateral)
    sns.distplot(freqsMedial, label='medial')
    sns.distplot(freqsLateral, label='lateral')
    plt.legend()
    #plt.show()
    zStats, pVal = stats.ranksums(freqsMedial, freqsLateral)
    if logscaled:
        print 'For {}db, the Wilcoxon rank-sum Z-statistic for logscaled responsive frequencies found in medial astr vs lateral astr is {}, p value is {}.\n'.format(intensity, zStats, pVal)
        figname = '{}dB medial vs lateral astr responsive log-freqs \n'.format(intensity)
    else:
        print 'For {}db, the Wilcoxon rank-sum Z-statistic for responsive frequencies found in medial astr vs lateral astr is {}, p value is {}.\n'.format(intensity, zStats, pVal)
        figname = '{}dB medial vs lateral astr responsive freqs \n'.format(intensity)
    
    plt.title(figname)
    xExtends = plt.gca().get_xlim()
    yExtends = plt.gca().get_ylim()
    plt.text(0.5*sum(xExtends), 0.5*sum(yExtends), 'p value: {}'.format(pVal))
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath, format='png')

    # -- Compare left vs right hemi for each intensity -- #
    freqsLeft = []
    freqsRight = []
    for name, values in responsiveFreqsThisIntensity.iteritems():
        if 'leftAStr' in name:
            values.dropna().apply(lambda x: freqsLeft.extend(x))
        elif 'rightAStr' in name:
            values.dropna().apply(lambda x: freqsRight.extend(x))
    if logscaled:
        freqsLeft = np.log2(freqsLeft)
        freqsRight = np.log2(freqsRight)
    plt.figure()
    sns.distplot(freqsLeft, label='left')
    sns.distplot(freqsRight, label='right')
    plt.legend()
    #plt.show()
    zStats, pVal = stats.ranksums(freqsLeft, freqsRight)
    if logscaled:
        print 'For {}db, the Wilcoxon rank-sum Z-statistic for responsive log-frequencies found in left astr vs right astr is {}, p value is {}. \n'.format(intensity, zStats, pVal)
        figname = '{}dB left vs right hemisphere responsive log-freqs'.format(intensity)
    else:
        print 'For {}db, the Wilcoxon rank-sum Z-statistic for responsive frequencies found in left astr vs right astr is {}, p value is {}. \n'.format(intensity, zStats, pVal)
        figname = '{}dB left vs right hemisphere responsive freqs'.format(intensity)
    plt.title(figname)
    xExtends = plt.gca().get_xlim()
    yExtends = plt.gca().get_ylim()
    plt.text(0.5*sum(xExtends), 0.5*sum(yExtends), 'p value: {}'.format(pVal))
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath, format='png')

    # -- Compare left vs right hemi in each training contingency for each intensity -- #
    freqsLeftLowGoLeft = []
    freqsLeftLowGoRight = []
    freqsRightLowGoLeft = []
    freqsRightLowGoRight = []
    for name, values in responsiveFreqsThisIntensity.iteritems():
        if 'leftAStr' in name:
            if 'low_freq_go_left' in name:
                values.dropna().apply(lambda x: freqsLeftLowGoLeft.extend(x))
            elif 'low_freq_go_right' in name:
                values.dropna().apply(lambda x: freqsLeftLowGoRight.extend(x))
        elif 'rightAStr' in name:
            if 'low_freq_go_left' in name:
                values.dropna().apply(lambda x: freqsRightLowGoLeft.extend(x))
            elif 'low_freq_go_right' in name:
                values.dropna().apply(lambda x: freqsRightLowGoRight.extend(x))

    if logscaled:
        freqsLeftLowGoLeft = np.log2(freqsLeftLowGoLeft)
        freqsRightLowGoLeft = np.log2(freqsRightLowGoLeft)
        freqsLeftLowGoRight = np.log2(freqsLeftLowGoRight)
        freqsRightLowGoRight = np.log2(freqsRightLowGoRight)

    plt.figure()
    sns.distplot(freqsLeftLowGoLeft, label='leftAStr_low_go_left', color='g')
    sns.distplot(freqsRightLowGoLeft, label='rightAStr_low_go_left', color='r')
    sns.distplot(freqsLeftLowGoRight, label='leftAStr_low_go_right', color='yellow')
    sns.distplot(freqsRightLowGoRight, label='rightAStr_low_go_right', color='blue')

    
    plt.legend()
    #plt.show()
    zStats1, pVal1 = stats.ranksums(freqsLeftLowGoLeft, freqsRightLowGoLeft)
    zStats2, pVal2 = stats.ranksums(freqsLeftLowGoRight, freqsRightLowGoRight)
    if logscaled:
        print 'For {}db in the low-freq-go-left contingency, the Wilcoxon rank-sum Z-statistic for log responsive frequencies found in left astr vs right astr is {}, p value is {}. \n'.format(intensity, zStats, pVal)    
        print 'For {}db in the low-freq-go-right contingency, the Wilcoxon rank-sum Z-statistic for log responsive frequencies found in left astr vs right astr is {}, p value is {}. \n'.format(intensity, zStats, pVal)
        figname = '{}dB by diff contingency left vs right hemisphere log responsive freqs'.format(intensity)

    else:
        print 'For {}db in the low-freq-go-left contingency, the Wilcoxon rank-sum Z-statistic for responsive frequencies found in left astr vs right astr is {}, p value is {}. \n'.format(intensity, zStats, pVal)    
        print 'For {}db in the low-freq-go-right contingency, the Wilcoxon rank-sum Z-statistic for responsive frequencies found in left astr vs right astr is {}, p value is {}. \n'.format(intensity, zStats, pVal)
        figname = '{}dB by diff contingency left vs right hemisphere responsive freqs'.format(intensity)

    plt.title(figname)
    xExtends = plt.gca().get_xlim()
    yExtends = plt.gca().get_ylim()
    plt.text(0.5*sum(xExtends), 0.5*sum(yExtends), 'p value for low-go-left: {}'.format(pVal1))
    plt.text(0.5*sum(xExtends), 0.7*sum(yExtends), 'p value for low-go-right: {}'.format(pVal2))
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath, format='png')
    
    # -- Comparison between 'low-freq encoding' vs 'high-freq encoding' hemis (hypothesized based on training contigency) -- #
    lowFreqEncodingThisIntensity = [col for col in groupsThisIntensity if ((('low_freq_go_left' in col) & ('rightAStr' in col)) | (('low_freq_go_right' in col) & ('leftAStr' in col)))]
    highFreqEncodingThisIntensity = [col for col in groupsThisIntensity if ((('low_freq_go_left' in col) & ('leftAStr' in col)) | (('low_freq_go_right' in col) & ('rightAStr' in col)))]
    
    lowFreqColsThisIntensity = responsiveFreqs[lowFreqEncodingThisIntensity].dropna(how='all')
    lowFreqs = []
    for name, values in lowFreqColsThisIntensity.iteritems():
        values.dropna().apply(lambda x: lowFreqs.extend(x))
  
    highFreqColsThisIntensity = responsiveFreqs[highFreqEncodingThisIntensity].dropna(how='all')
    highFreqs = []
    for name, values in highFreqColsThisIntensity.iteritems():
        values.dropna().apply(lambda x: highFreqs.extend(x))
    
    if logscaled:
        lowFreqs = np.log2(lowFreqs)
        highFreqs = np.log2(highFreqs)
    
    plt.figure()
    sns.distplot(lowFreqs, label='low_freq_encoding_areas', color='g')
    sns.distplot(highFreqs, label='high_freq_encoding_areas', color='r')
    plt.legend()
    #plt.show()
    zStats, pVal = stats.ranksums(lowFreqs, highFreqs)

    if logscaled:
        print 'For {}db, the Wilcoxon rank-sum Z-statistic for log responsive frequencies found in low vs high frequency-encoding area is {}, p value is {}. \n'.format(intensity, zStats, pVal)
        figname = '{}dB low vs high freq encoding areas_logscaled'.format(intensity)
    else:
        print 'For {}db, the Wilcoxon rank-sum Z-statistic for responsive frequencies found in low vs high frequency-encoding area is {}, p value is {}. \n'.format(intensity, zStats, pVal)
        figname = '{}dB low vs high freq encoding areas'.format(intensity)
    plt.title(figname)
    xExtends = plt.gca().get_xlim()
    yExtends = plt.gca().get_ylim()
    plt.text(0.5*sum(xExtends), 0.5*sum(yExtends), 'p value: {}'.format(pVal))
    figFullPath = os.path.join(outputDir, figname)
    plt.savefig(figFullPath, format='png')
