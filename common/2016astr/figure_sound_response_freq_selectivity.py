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
matplotlib.rcParams['svg.fonttype'] = 'none'  # To

#dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)

PANELS = [1,1,1,1] # Which panels to plot

SAVE_FIGURE = 0
outputDir = '/tmp/'
figFilename = 'figure_sound_freq_selectivity' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [10,6]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1

timeRangeSound = [-0.2, 0.4]
msRaster = 2
smoothWinSizePsth = 3
lwPsth = 2
downsampleFactorPsth = 1

colormapTuning = matplotlib.cm.winter 

labelPosX = [0.07, 0.27, 0.47, 0.67]   # Horiz position for panel labels
labelPosY = [0.9]    # Vert position for panel labels

PHOTOSTIMCOLORS = {'no_laser':'k', 'laser_left':'red', 'laser_right':'green'}

#SHAPESEACHANIMAL = ['o','s','^']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 5)
gs.update(left=0.1, right=0.9, wspace=0.35, hspace=0.2)

gs00 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[:,0], hspace=0.2)
gs01 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[:,1], hspace=0.2)
gs02 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[:,2], hspace=0.2)
gs03 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[:,3], hspace=0.2)

# -- Panel A: representative sound-evoked raster and psth from tuning task -- #
ax1 = plt.subplot(gs00[0:2,:])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[0]:
    rasterFilename = 'example_freq_tuning_raster_adap017_20160317a_T5_c3.npz' 
    rasterFullPath = os.path.join(dataDir, rasterFilename)
    rasterExample =np.load(rasterFullPath)

    possibleFreq = rasterExample['possibleFreq']
    trialsEachCond = rasterExample['trialsEachFreq']
    spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
    indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
    timeRange = timeRangeSound #rasterExample['timeRange']
    labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]
    cm_subsection = np.linspace(1.0, 0.0, len(possibleFreq))
    colorEachFreq = [colormapTuning(x) for x in cm_subsection] 

    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRange,
                                                   trialsEachCond=trialsEachCond,
                                                   colorEachCond=colorEachFreq,
                                                   labels=labels)

    plt.setp(pRaster, ms=msRaster)
    #plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.ylabel('Frequency (kHz)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.xlim(timeRangeSound[0],timeRangeSound[1])

    ax2 = plt.subplot(gs00[2,:])
    psthFilename = 'example_freq_tuning_psth_adap017_20160317a_T5_c3.npz' 
    psthFullPath = os.path.join(dataDir, psthFilename)
    psthExample = np.load(psthFullPath)

    trialsEachCond = psthExample['trialsEachFreq']
    spikeCountMat = psthExample['spikeCountMat']
    timeVec = psthExample['timeVec']
    binWidth = psthExample['binWidth']
    timeRange = psthExample['timeRange']
    possibleFreq = psthExample['possibleFreq']
    numFreqs = len(possibleFreq)

    labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]
    #cm_subsection = np.linspace(0.0, 1.0, numFreqs)
    #colorEachCond = [colormapTuning(x) for x in cm_subsection] 

    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,
                                 trialsEachCond=trialsEachCond,colorEachCond=colorEachFreq,
                                 linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    for ind,line in enumerate(pPSTH):
        plt.setp(line, label=labels[ind])
    plt.legend(loc='upper right', fontsize=fontSizeTicks, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    plt.xlim(timeRangeSound[0],timeRangeSound[1])
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels, labelpad=labelDis)

    
# -- Panel B: another example of sound-evoked raster and psth from tuning task -- #
ax3 = plt.subplot(gs01[0:2,:])
ax3.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    rasterFilename = 'example_freq_tuning_raster_test055_20150307a_T4_c3.npz' 
    rasterFullPath = os.path.join(dataDir, rasterFilename)
    rasterExample =np.load(rasterFullPath)

    possibleFreq = rasterExample['possibleFreq']
    trialsEachCond = rasterExample['trialsEachFreq']
    spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
    indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
    timeRange = rasterExample['timeRange']
    labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRange,
                                                   trialsEachCond=trialsEachCond,
                                                   labels=labels)

    plt.setp(pRaster, ms=msRaster)
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.ylabel('Frequency (kHz)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.xlim(timeRangeSound[0],timeRangeSound[1])

    ax4 = plt.subplot(gs01[2,:])

    psthFilename = 'example_freq_tuning_psth_test055_20150307a_T4_c3.npz' 
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

    cm_subsection = np.linspace(0.0, 1.0, numFreqs)
    colorEachCond = [colormapTuning(x) for x in cm_subsection] 

    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    for ind,line in enumerate(pPSTH):
        plt.setp(line, label=labels[ind])
    plt.legend(loc='upper right', fontsize=fontSizeTicks, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    plt.xlim(timeRangeSound[0],timeRangeSound[1])
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.ylabel('Firing rate (spk/sec)',fontsize=fontSizeLabels, labelpad=labelDis)


# -- Panel C: example of sound-evoked raster and psth from 2afc task (cell in A) -- #
ax5 = plt.subplot(gs02[0:2,:])
ax5.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[2]:
    rasterFilename = 'example_freq_tuning_2afc_raster_adap017_20160317a_T5_c3.npz' 
    rasterFullPath = os.path.join(dataDir, rasterFilename)
    rasterExample =np.load(rasterFullPath)

    possibleFreq = rasterExample['possibleFreq']
    trialsEachCond = rasterExample['trialsEachFreq']
    spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
    indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
    timeRange = rasterExample['timeRange']
    labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRange,
                                                   trialsEachCond=trialsEachCond,
                                                   labels=labels)

    plt.setp(pRaster, ms=msRaster)
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.ylabel('Frequency (kHz)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.xlim(timeRangeSound[0],timeRangeSound[1])

    ax6 = plt.subplot(gs02[2,:])

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

    cm_subsection = np.linspace(0.0, 1.0, numFreqs)
    colorEachCond = [colormapTuning(x) for x in cm_subsection] 

    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    for ind,line in enumerate(pPSTH):
        plt.setp(line, label=labels[ind])
    plt.legend(loc='upper right', fontsize=fontSizeTicks, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    plt.xlim(timeRangeSound[0],timeRangeSound[1])
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.ylabel('Firing rate (spk/sec)',fontsize=fontSizeLabels, labelpad=labelDis)


# -- Panel D: another example of sound-evoked raster and psth from 2afc task (cell in B) -- #
ax6 = plt.subplot(gs03[0:2,:])
ax6.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[2]:
    rasterFilename = 'example_freq_tuning_2afc_raster_test055_20150307a_T4_c3.npz' 
    rasterFullPath = os.path.join(dataDir, rasterFilename)
    rasterExample =np.load(rasterFullPath)

    possibleFreq = rasterExample['possibleFreq']
    trialsEachCond = rasterExample['trialsEachFreq']
    spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
    indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
    timeRange = rasterExample['timeRange']
    labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRange,
                                                   trialsEachCond=trialsEachCond,
                                                   labels=labels)

    plt.setp(pRaster, ms=msRaster)
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.ylabel('Frequency (kHz)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.xlim(timeRangeSound[0],timeRangeSound[1])

    ax7 = plt.subplot(gs03[2,:])

    psthFilename = 'example_freq_tuning_2afc_psth_test055_20150307a_T4_c3.npz' 
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

    cm_subsection = np.linspace(0.0, 1.0, numFreqs)
    colorEachCond = [colormapTuning(x) for x in cm_subsection] 

    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    for ind,line in enumerate(pPSTH):
        plt.setp(line, label=labels[ind])
    plt.legend(loc='upper right', fontsize=fontSizeTicks, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    plt.xlim(timeRangeSound[0],timeRangeSound[1])
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.ylabel('Firing rate (spk/sec)',fontsize=fontSizeLabels, labelpad=labelDis)


# -- Panel E: summary of freq selectivity in 2afc task -- #
ax8 = plt.subplot(gs[:, 4])
ax8.annotate('D', xy=(labelPosX[3],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[3]:
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
    ###############################################################################
    #sigSoundResponse = (summary['pValSoundResponseEachCell'][cellSelectorBoolArray] <= alphaLevel)
    #freqSelective = (summary['pValSoundResponseEachCell'][cellSelectorBoolArray] <= alphaLevel) & (summary['freqSelectivityEachCell'][cellSelectorBoolArray] <= alphaLevel)
    freqSelective = summary['freqSelectivityEachCell'][cellSelectorBoolArray] <= alphaLevel
    ###############################################################################

    plt.hist((responseIndEachCell[freqSelective],responseIndEachCell[~freqSelective]), color=['k','None'], bins=20)
    #plt.xticks([0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000], ['0', '5', '10', '15', '20', '25', '30', '35', '40'])
    plt.xlabel('Sound response index')
    plt.ylabel('Number of cells')
    #sig_patch = mpatches.Patch(color='k', label='Frequency selective')
    #nonsig_patch = mpatches.Patch(facecolor='None', edgecolor='k', label='Not frequency selective')
    #plt.legend(handles=[sig_patch,nonsig_patch], loc='upper center', fontsize=fontSizeTicks, frameon=False, labelspacing=0.1, handlelength=0.2)

     # -- Statistic test for  -- #
    numCells = sum(cellSelectorBoolArray)
    numFreqSelCells = sum(freqSelective.astype(int))
    print 100*float(numFreqSelCells)/numCells, '%', numFreqSelCells, 'out of', numCells, 'in 2afc psycurve task show frequency selectivity (one-way ANOVA)'
    print 'median response index:', np.mean(responseIndEachCell[~np.isnan(responseIndEachCell)]) #These is one nan value

    print sum((responseIndEachCell < 0).astype(int)), 'cells showed decreased activity;', sum((responseIndEachCell > 0).astype(int)), 'cells showed increased activity'

    
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)


