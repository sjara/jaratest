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

PANELS = [1,1,1] # Which panels to plot

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'figure_sound_freq_selectivity' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [10,3.5]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1

timeRangeSound = [-0.2, 0.4]
msRaster = 2
smoothWinSizePsth1 = 1 #2
smoothWinSizePsth2 = 3 #2
lwPsth = 2
downsampleFactorPsth = 1

colormapTuning = matplotlib.cm.winter 

labelPosX = [0.015, 0.355, 0.68]   # Horiz position for panel labels
labelPosY = [0.92]    # Vert position for panel labels

PHOTOSTIMCOLORS = {'no_laser':'k', 'laser_left':'red', 'laser_right':'green'}
soundColor = figparams.colp['sound']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 3)
gs.update(left=0.08, right=0.98, top=0.95, bottom=0.15, wspace=0.4, hspace=0.1)

gs00 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gs[:,0], hspace=0.15)
gs01 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gs[:,1], hspace=0.15)


# -- Panel C: example of sound-evoked raster and psth from 2afc task (cell in A) -- #
ax5 = plt.subplot(gs00[0:3,:])
ax5.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[0]:
    rasterFilename = 'example_freq_tuning_2afc_raster_adap017_20160317a_T5_c3.npz' 
    rasterFullPath = os.path.join(dataDir, rasterFilename)
    rasterExample =np.load(rasterFullPath)

    possibleFreq = rasterExample['possibleFreq']
    trialsEachCond = rasterExample['trialsEachFreq']
    spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
    indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
    #timeRange = rasterExample['timeRange']
    labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]

    colorEachFreq = [colormapTuning(x) for x in np.linspace(1.0, 0.2, len(possibleFreq))] 

    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRangeSound,
                                                   trialsEachCond=trialsEachCond,
                                                   colorEachCond=colorEachFreq,
                                                   labels=labels)
    plt.setp(pRaster, ms=msRaster)
    plt.setp(hcond,zorder=3)
    #plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.gca().set_xticklabels('')
    plt.ylabel('Frequency (kHz)',fontsize=fontSizeLabels) #, labelpad=labelDis)
    plt.xlim(timeRangeSound[0],timeRangeSound[1])

    ax6 = plt.subplot(gs00[3,:])

    psthFilename = 'example_freq_tuning_2afc_psth_adap017_20160317a_T5_c3.npz' 
    psthFullPath = os.path.join(dataDir, psthFilename)
    psthExample =np.load(psthFullPath)

    trialsEachCond = psthExample['trialsEachFreq']
    spikeCountMat = psthExample['spikeCountMat']
    timeVec = psthExample['timeVec']
    binWidth = psthExample['binWidth']
    timeRange = psthExample['timeRange']
    possibleFreq = psthExample['possibleFreq']
    numFreqs = len(possibleFreq)
    labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]

    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth1,timeVec,
                                 trialsEachCond=trialsEachCond,colorEachCond=colorEachFreq,
                                 linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    for ind,line in enumerate(pPSTH):
        plt.setp(line, label=labels[ind])
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    plt.xlim(timeRangeSound)
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels) #, labelpad=labelDis
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #, labelpad=labelDis
    yLims = [0,80]
    plt.ylim(yLims)
    plt.yticks(yLims)
    soundBarHeight = 0.1*yLims[-1]
    plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    extraplots.boxoff(plt.gca())
    #plt.legend(loc='upper right', fontsize=fontSizeTicks, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)

# -- Panel D: another example of sound-evoked raster and psth from 2afc task (sound-suppressed) -- #
ax6 = plt.subplot(gs01[0:3,:])
ax6.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    rasterFilename = 'example_freq_tuning_2afc_raster_adap015_20160205a_T6_c5.npz'#adap017_20160405a_T3_c7 #test055_20150307a_T5_c3 
    rasterFullPath = os.path.join(dataDir, rasterFilename)
    rasterExample =np.load(rasterFullPath)

    possibleFreq = rasterExample['possibleFreq']
    trialsEachCond = rasterExample['trialsEachFreq']
    spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
    indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
    #timeRange = rasterExample['timeRange']
    labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]

    colorEachFreq = [colormapTuning(x) for x in np.linspace(1.0, 0.2, len(possibleFreq))] 

    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRangeSound,
                                                   trialsEachCond=trialsEachCond,
                                                   colorEachCond=colorEachFreq,
                                                   labels=labels)
    plt.setp(pRaster, ms=msRaster)
    plt.setp(hcond,zorder=3)
    #plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.gca().set_xticklabels('')
    plt.ylabel('Frequency (kHz)',fontsize=fontSizeLabels) #, labelpad=labelDis)
    plt.xlim(timeRangeSound[0],timeRangeSound[1])

    ax7 = plt.subplot(gs01[3,:])

    psthFilename = 'example_freq_tuning_2afc_psth_adap015_20160205a_T6_c5.npz' #adap017_20160405a_T3_c7
    psthFullPath = os.path.join(dataDir, psthFilename)
    psthExample =np.load(psthFullPath)

    trialsEachCond = psthExample['trialsEachFreq']
    spikeCountMat = psthExample['spikeCountMat']
    timeVec = psthExample['timeVec']
    binWidth = psthExample['binWidth']
    timeRange = psthExample['timeRange']
    possibleFreq = psthExample['possibleFreq']
    numFreqs = len(possibleFreq)
    labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]

    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth2,timeVec,
                                 trialsEachCond=trialsEachCond,colorEachCond=colorEachFreq,
                                 linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    for ind,line in enumerate(pPSTH):
        plt.setp(line, label=labels[ind])
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    plt.xlim(timeRangeSound)
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels) #, labelpad=labelDis
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #, labelpad=labelDis
    yLims = [0,10]
    soundBarHeight = 0.1*yLims[-1]
    plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    extraplots.boxoff(plt.gca())
    #plt.legend(loc='upper right', fontsize=fontSizeTicks, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)



# -- Panel E: summary of freq selectivity in 2afc task -- #
ax8 = plt.subplot(gs[:, 2])
ax8.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[2]:
    alphaLevel = 0.05
    numFreqs = 16
    bonferroniCorrectedAlphaLevel = alphaLevel/numFreqs

    summaryFilename = 'summary_2afc_best_freq_maxZ_psychometric.npz'
    summaryFullPath = os.path.join(dataDir,summaryFilename)
    summary = np.load(summaryFullPath)

    cellSelectorBoolArray = summary['cellSelectorBoolArray']
    bestFreqEachCell = summary['bestFreqEachCell'][cellSelectorBoolArray]
    #bestFreqEachCell = bestFreqEachCell[bestFreqEachCell!=0]
    maxZscoreEachCell = summary['maxZscoreEachCell'][cellSelectorBoolArray]
    #maxZscoreEachCell = maxZscoreEachCell[maxZscoreEachCell!=0]
    responseIndEachCell = summary['responseIndEachCell'][cellSelectorBoolArray]

    nansInData = np.isnan(responseIndEachCell)
    if np.any(nansInData):
        print '*** WARNING! *** I found NaN in some elements of responseIndEachCell. I will replace with zero.'
        responseIndEachCell[nansInData] = 0
    
    ###############################################################################
    #sigSoundResponse = (summary['pValSoundResponseEachCell'][cellSelectorBoolArray] <= alphaLevel)
    #freqSelective = (summary['pValSoundResponseEachCell'][cellSelectorBoolArray] <= alphaLevel) & (summary['freqSelectivityEachCell'][cellSelectorBoolArray] <= alphaLevel)
    freqSelective = summary['freqSelectivityEachCell'][cellSelectorBoolArray] <= alphaLevel
    ###############################################################################
    
    '''
    plt.hist((responseIndEachCell[freqSelective],responseIndEachCell[~freqSelective]), color=['k','None'], bins=20)
    #plt.xticks([0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000], ['0', '5', '10', '15', '20', '25', '30', '35', '40'])
    plt.xlabel('Sound response index')
    plt.ylabel('Number of cells')
    #sig_patch = mpatches.Patch(color='k', label='Frequency selective')
    #nonsig_patch = mpatches.Patch(facecolor='None', edgecolor='k', label='Not frequency selective')
    #plt.legend(handles=[sig_patch,nonsig_patch], loc='upper center', fontsize=fontSizeTicks, frameon=False, labelspacing=0.1, handlelength=0.2)
    '''
    plt.hold(True)
    binsEdges = np.linspace(-1,1,20)
    #plt.hist(responseIndEachCell, bins=binsEdges, color='0.75')
    #plt.hist(responseIndEachCell[freqSelective], bins=binsEdges, color='k')
    plt.hist([responseIndEachCell[freqSelective],responseIndEachCell[~freqSelective]], bins=binsEdges, color=['k','darkgrey'],
             edgecolor='None',stacked=True)

    nCellsString = '{} cells'.format(sum(cellSelectorBoolArray))
    nMiceString = '{} mice'.format(5)
    plt.text(0.4, 65, nCellsString, ha='left',fontsize=fontSizeLabels)
    plt.text(0.4, 60, nMiceString, ha='left',fontsize=fontSizeLabels)
    plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
    plt.xlabel('Sound response index',fontsize=fontSizeLabels)
    plt.ylabel('Number of cells',fontsize=fontSizeLabels)
    
    plt.xlim([-1.01,1.01])
    extraplots.boxoff(ax8)
    
     # -- Statistic test for  -- #
    numCells = sum(cellSelectorBoolArray)
    numFreqSelCells = sum(freqSelective.astype(int))
    print 100*float(numFreqSelCells)/numCells, '%', numFreqSelCells, 'out of', numCells, 'in 2afc psycurve task show frequency selectivity (one-way ANOVA)'
    print 'median response index:', np.mean(responseIndEachCell[~np.isnan(responseIndEachCell)]) #These is one nan value

    print sum((responseIndEachCell < 0).astype(int)), 'cells showed decreased activity;', sum((responseIndEachCell > 0).astype(int)), 'cells showed increased activity;', sum((responseIndEachCell == 0).astype(int)), 'cells had unchanged activity during sound'

    
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)


