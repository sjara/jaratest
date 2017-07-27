import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pdb


animalLists = ['adap041','adap042', 'adap043','adap044', 'adap046','adap047']

#plotAll = True
#normalized = False
logscaled = True

tuningIntensities = [40, 50, 60, 70]
astrRegions = ['medial','lateral']
qualityThreshold = 3 
maxZThreshold = 2
ISIcutoff = 0.02

responsiveFreqs = {}

# -- Make composite celldb -- #
allMiceDfs = []
for animal in animalLists:
    databaseFullPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(animal))
    key = 'head_fixed'
    celldbThisMouse = pd.read_hdf(databaseFullPath, key=key)
    allMiceDfs.append(celldbThisMouse)
    
celldb = pd.concat(allMiceDfs, ignore_index=True)

# -- Plot histogram of responsive freqs by medial-lateral location -- #
goodQualCells = celldb.query("isiViolations<{} and shapeQuality>{} and astrRegion!='undefined'".format(ISIcutoff, qualityThreshold))

maxZscore = goodQualCells.ZscoreEachIntensity.apply(lambda x : np.max(np.abs(x)))
goodRespCells=goodQualCells[maxZscore >= maxZThreshold]


outputDir = '/home/languo/data/ephys/head_fixed_astr/all_mice/responsive_freqs_by_location/'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
freqs = goodQualCells.tuningFreqs.iloc[0]

#if plotAll:
cellsToPlot = goodQualCells
#else:
#   cellsToPlot = goodRespCells

#plt.figure(figsize=(20,20)) 
#gs = gridspec.GridSpec(2,len(tuningIntensities))
numCol = len(tuningIntensities)
fig, axes = plt.subplots(nrows=1, ncols=numCol, sharex=True, sharey='row')

#gs.update(left=0.05, right=0.95, wspace=0.15, hspace=0.3)
figname = 'allgoodcells_Zscore{}_medial_vs_lateral'.format(maxZThreshold)  
# Dataframe to store results:


for indi, intensity in enumerate(tuningIntensities):
    for indr, region in enumerate(astrRegions):
        thisRegion = cellsToPlot.loc[cellsToPlot.astrRegion==region]
        zScoresThisIntensity = thisRegion.tuningZscoreEachIntEachFreq.apply(lambda x: x[indi]) #select just the zScores for that intensity
        #pdb.set_trace()
        responseEachFreqThisIntensity = zScoresThisIntensity.apply(lambda x: (np.abs(x)>=maxZThreshold))
        tuningFreqsThisIntensity = thisRegion.tuningFreqs.to_frame()
        responsiveFreqsThisRegionThisIntensity = []
        for indRow, freqsThisCell in thisRegion.tuningFreqs.iteritems():
            responsiveFreqsThisRegionThisIntensity.extend(freqsThisCell[responseEachFreqThisIntensity.loc[indRow].values])
        if logscaled:
            responsiveFreqsThisRegionThisIntensity = np.log2(responsiveFreqsThisRegionThisIntensity)
        responsiveFreqs[region+'_'+str(intensity)] = responsiveFreqsThisRegionThisIntensity
        ax = axes[indi]
        ax.hist(responsiveFreqsThisRegionThisIntensity, alpha=0.75, label=region)
        #plt.hold(True)
        ax.set_title('{} db'.format(intensity))
        #pdb.set_trace()
plt.legend()
fig.set_tight_layout({'rect': [0.02, 0.02, 1, 0.95], 'w_pad': 0.06, 'h_pad': 0.05})  
fig.text(0.5, 0.02, 'Tone frequency (logscaled)', ha='center', va='center')
fig.text(0.02, 0.5, 'Number of responsive cells', ha='center', va='center', rotation='vertical')
plt.show()


# -- Stats -- #
#responsiveFreqs is a big dictionary with each group as a column and each cell from the celldb as a row
from scipy import stats
import seaborn as sns
outputDir = '/home/languo/data/ephys/head_fixed_astr/all_mice/responsive_freqs_by_location/stats/'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

for intensity in tuningIntensities:
    responsiveFreqsThisIntensity = {k: v for k, v in responsiveFreqs.items() if str(intensity) in k} 
    # -- Compare medial vs lateral for each intensity -- #
    freqsMedial = responsiveFreqsThisIntensity['medial_'+str(intensity)] 
    freqsLateral = responsiveFreqsThisIntensity['lateral_'+str(intensity)]
    #[v for k, v in responsiveFreqsThisIntensity.items() if 'lateral' in k]
    
    zStats, pVal = stats.ranksums(freqsMedial, freqsLateral)
    if logscaled:
        print 'For {}db, the Wilcoxon rank-sum Z-statistic for logscaled responsive frequencies found in medial astr vs lateral astr is {}, p value is {}.\n'.format(intensity, zStats, pVal)
        figname = '{}dB medial vs lateral astr responsive log-freqs \n'.format(intensity)
    else:
        print 'For {}db, the Wilcoxon rank-sum Z-statistic for responsive frequencies found in medial astr vs lateral astr is {}, p value is {}.\n'.format(intensity, zStats, pVal)
        figname = '{}dB medial vs lateral astr responsive freqs \n'.format(intensity)
    
    #plt.figure()
    
    #sns.distplot(freqsMedial, label='medial')
    #sns.distplot(freqsLateral, label='lateral')
    #plt.legend()
    #plt.show()
    #plt.title(figname)
    #xExtends = plt.gca().get_xlim()
    #yExtends = plt.gca().get_ylim()
    #plt.text(0.5*sum(xExtends), 0.5*sum(yExtends), 'p value: {}'.format(pVal))
    #figFullPath = os.path.join(outputDir, figname)
    #plt.savefig(figFullPath, format='png')

    
