'''
Create figure about effect of unilateral photo-activation of astr neurons in the 2afc task.
'''
import os
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
import matplotlib.gridspec as gridspec
from scipy import stats
import matplotlib
import figparams

FIGNAME = 'sound_freq_selectivity'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

#dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)

PANELS = [1,1,1,1] # Which panels to plot

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plot_response_each_freq_psychometric' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [12,3.5]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1

timeRangeSound = [-0.2, 0.4]
msRaster = 2
msMvStart = 3
smoothWinSizePsth1 = 1 #2
smoothWinSizePsth2 = 3 #2
lwPsth = 2
downsampleFactorPsth = 1

colormapTuning = matplotlib.cm.winter 

labelPosX = [0.015, 0.28, 0.52, 0.76]   # Horiz position for panel labels
labelPosY = [0.95]    # Vert position for panel labels

PHOTOSTIMCOLORS = {'no_laser':'k', 'laser_left':'red', 'laser_right':'green'}
soundColor = figparams.colp['sound']

alphaLevel = 0.05
numFreqs = 6
bonferroniCorrectedAlphaLevel = alphaLevel/numFreqs

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

# -- Panel E: summary of maximal response index in 2afc task -- #

summaryFilename = 'summary_2afc_best_freq_maxZ_psychometric.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
summary = np.load(summaryFullPath)

cellSelectorBoolArray = summary['cellSelectorBoolArray']
bestFreqEachCell = summary['bestFreqEachCell'] #[cellSelectorBoolArray]
#bestFreqEachCell = bestFreqEachCell[bestFreqEachCell!=0]
maxZscoreEachCell = summary['maxZscoreEachCell'] #[cellSelectorBoolArray]
#maxZscoreEachCell = maxZscoreEachCell[maxZscoreEachCell!=0]
responseIndEachCell = summary['responseIndEachCell'] #[cellSelectorBoolArray]

nansInData = np.isnan(responseIndEachCell)
if np.any(nansInData):
    print '*** WARNING! *** I found NaN in some elements of responseIndEachCell. I will replace with zero.'
    responseIndEachCell[nansInData] = 0

###############################################################################
pValEachFreqEachCell = summary['pValEachFreqEachCell'] #[cellSelectorBoolArray]
minPValEachCell = np.amin(pValEachFreqEachCell, axis=1)
sigResp = (minPValEachCell <= bonferroniCorrectedAlphaLevel) # In the 6 ranksum tests, at least one freq past bonferroni corrected p test
###############################################################################

################################################
# -- Compare response to all freqs to all baselines -- #
responseFilename = 'response_each_freq_each_cell_psycurve_2afc.npz'
responseFullPath = os.path.join(dataDir,responseFilename)
responseEachCellEachFreq = np.load(responseFullPath)
baselineFilename = 'baseline_each_freq_each_cell_psycurve_2afc.npz'
baselineFullPath = os.path.join(dataDir,baselineFilename)
baselineEachCellEachFreq = np.load(baselineFullPath)
numCells = sum(cellSelectorBoolArray)
overallRespInds = np.array([])
pVals = np.array([])
for cellInd in range(numCells):
    fSound = responseEachCellEachFreq[cellInd,:,:].compressed()
    fBaseline = baselineEachCellEachFreq[cellInd,:,:].compressed()
    zScore,pVal = stats.ranksums(fBaseline, fSound)
    pVals = np.append(pVals,pVal)
    if np.mean(fSound)+np.mean(fBaseline)==0:
        overallRespIndexThisCell = 0
    else:
        overallRespIndexThisCell = (np.mean(fSound)-np.mean(fBaseline)) / (np.mean(fSound)+np.mean(fBaseline))
    overallRespInds = np.append(overallRespInds, overallRespIndexThisCell)
sigRespOverall = (pVals <= 0.05)
nansInData = np.isnan(overallRespInds)
if np.any(nansInData):
    print '*** WARNING! *** I found NaN in some elements of overall sound responsive index. I will replace with zero.'
    overallRespInds[nansInData] = 0
################################################
numCells = sum(cellSelectorBoolArray)
#numResponsiveCells = sum(sigResp)
numOverallRespCells = sum(sigRespOverall)
#percentResp = float(numResponsiveCells)/numCells*100
percentRespOverall = float(numOverallRespCells)/numCells*100
#print 'Using Bonferroni corrected p value, out of {} cells, {} cells showed significant change in firing rate to at least one sound stim presented. That is {}% of cells.'.format(numCells, numResponsiveCells,percentResp)
print 'Summing all the sound freqs together and comparing evoked activity to baseline, {} cells were significantly responsive. That is {}% of all cells.'.format(numOverallRespCells, percentRespOverall)

#plt.hist(bestFreqEachCell[sigRespOverall])
#plt.hist(np.log2(bestFreqEachCell[sigRespOverall]))
#plt.title('sound responsive cells best freq')

# -- Panel E: summary of sound selectivity index in 2afc task -- #
responseFilename = 'response_each_freq_each_cell_psycurve_2afc.npz'
responseFullPath = os.path.join(dataDir,responseFilename)
responseEachCellEachFreq = np.load(responseFullPath)
#baselineFilename = 'baseline_each_freq_each_cell_psycurve_2afc.npz'
#baselineFullPath = os.path.join(dataDir,summaryFilename)
#baselineEachCellEachFreq = np.load(baselineFullPath)
selectivityInds = np.array([])
pVals = np.array([])
for cellInd in range(numCells):
    fLow = responseEachCellEachFreq[cellInd,:,:3].compressed()
    fHigh = responseEachCellEachFreq[cellInd,:,3:].compressed()
    zScore,pVal = stats.ranksums(fLow, fHigh)
    pVals = np.append(pVals,pVal)
    if (np.mean(fHigh)+np.mean(fLow))==0:
        selectivityIndexThisCell = 0
    else:
        selectivityIndexThisCell = (np.mean(fHigh)-np.mean(fLow)) / (np.mean(fHigh)+np.mean(fLow))
    selectivityInds = np.append(selectivityInds, selectivityIndexThisCell)

nansInData = np.isnan(selectivityInds)
if np.any(nansInData):
    print '*** WARNING! *** I found NaN in some elements of selectivity index. I will replace with zero.'
    selectivityInds[nansInData] = 0

freqSelective = (pVals <= 0.05)

# -- Statistic test for frequency selectivity (ANOVA) -- #
numFreqSelCells = sum(freqSelective.astype(int))
print 100*float(numFreqSelCells)/numCells, '%', numFreqSelCells, 'out of', numCells, ' cells in 2afc psycurve task show different response to high and low frequencies.'

hlFreqSelSoundResp = freqSelective & sigRespOverall

#plt.figure()
#plt.hist(np.log2(bestFreqEachCell[hlFreqSelSoundResp]))
#plt.title('sound responsive cells selective to h v l')

hlFreqNonSelSoundResp = ~freqSelective & sigRespOverall
numHLFreqSelSoundRespCells = sum(hlFreqSelSoundResp)
print 100*float(numHLFreqSelSoundRespCells)/numOverallRespCells, '%, ', numHLFreqSelSoundRespCells, 'out of', numOverallRespCells, ' sound responsive cells in 2afc psycurve task show different response to high and low frequencies.'

ANOVAfreqSelective = summary['freqSelectivityEachCell'] <= alphaLevel
numOverallFreqSelCells = sum(ANOVAfreqSelective)
numOverallFreqSelSoundRespCells = sum(ANOVAfreqSelective & sigRespOverall)
print 100*float(numOverallFreqSelSoundRespCells)/numOverallRespCells, '%, ', numOverallFreqSelSoundRespCells, 'out of', numOverallRespCells, ' sound responsive cells in 2afc psycurve task show different response to all frequencies (one-way ANOVA).'
print 100*float(numOverallFreqSelCells)/numCells, '%, ', numOverallFreqSelCells, 'out of', numCells, ' total cells in 2afc psycurve task show different response to all frequencies (one-way ANOVA).'

# -- Statistic test for frequency selectivity (Kruskal-Wallis H-test) -- #
allKruskalPVals = np.ones(numCells)
for cellInd in range(numCells):
    Fstat, pVal = stats.kruskal(*np.hsplit(responseEachCellEachFreq[cellInd], numFreqs))
    allKruskalPVals[cellInd] = pVal
KruskalfreqSelective = allKruskalPVals <= alphaLevel
numOverallFreqSelCellsKruskal = sum(KruskalfreqSelective)
numOverallFreqSelSoundRespCellsKruskal = sum(KruskalfreqSelective & sigRespOverall)
print 100*float(numOverallFreqSelCellsKruskal)/numCells, '%, ', numOverallFreqSelCellsKruskal, 'out of', numCells, ' total cells in 2afc psycurve task show different response to all frequencies (Kruskal-Wallis H-test).'
print 100*float(numOverallFreqSelSoundRespCellsKruskal)/numOverallRespCells, '%, ', numOverallFreqSelSoundRespCellsKruskal, 'out of', numOverallRespCells, ' sound responsive cells in 2afc psycurve task show different response to all frequencies (Kruskal-Wallis H-test).'

respEachCellEachFreqSelective = responseEachCellEachFreq[hlFreqSelSoundResp, :, :]
respEachCellEachFreqNonSelective = responseEachCellEachFreq[hlFreqNonSelSoundResp, :, :]

#plt.figure()

rowNum = 10
colNum = 10
numOfPlots = rowNum * colNum
for cellInd in range(respEachCellEachFreqSelective.shape[0]):
    if (cellInd % numOfPlots == 0) | ((cellInd % numOfPlots == 0) & (cellInd >= numOfPlots)):
        plt.figure()
    plt.subplot(rowNum,colNum,cellInd%numOfPlots+1) 
    plt.bar(range(6), respEachCellEachFreqSelective[cellInd].mean(axis=0), width=0.3, yerr=(np.zeros(6), respEachCellEachFreqSelective[cellInd].std(axis=0)), alpha=0.5, color='grey')
    plt.xticks(range(6), [])
    plt.xlim([-1,6])
    plt.yticks([],[])
    plt.title(cellInd)
    plt.suptitle('h/l selective cells')
    plt.tight_layout()
    
#plt.xlabel('Frequencies')
#plt.ylabel('Average response')

for cellInd in range(respEachCellEachFreqNonSelective.shape[0]):
    if (cellInd % numOfPlots == 0) | ((cellInd % numOfPlots == 0) & (cellInd >= numOfPlots)):
        plt.figure()
    plt.subplot(rowNum,colNum,cellInd%numOfPlots+1) 
    plt.bar(range(6), respEachCellEachFreqNonSelective[cellInd].mean(axis=0), width=0.3, yerr=(np.zeros(6), respEachCellEachFreqNonSelective[cellInd].std(axis=0)), alpha=0.5, color='grey')
    plt.xticks(range(6), [])
    plt.xlim([-1,6])
    plt.yticks([],[])
    plt.title(cellInd)
    plt.suptitle('h/l non-selective cells')
    plt.tight_layout()
#plt.xlabel('Frequencies')
#plt.ylabel('Average response')

plt.show()

