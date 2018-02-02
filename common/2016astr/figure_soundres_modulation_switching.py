'''
Create figure about the activity of astr neurons during sound being modulated by contingency in the switching task.
'''
import os
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import scipy.stats as stats
import figparams
reload(figparams)

FIGNAME = 'soundres_modulation_switching'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

#removedDuplicates = True

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To

colorLeft = figparams.colp['MidFreqL']
colorRight = figparams.colp['MidFreqR']

soundColor = figparams.colp['sound']
timeRange = [-0.3,0.5]

#dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)

PANELS = [1,1,1] # Which panels to plot

SAVE_FIGURE = 1
outputDir = '/tmp/'
'''
if removedDuplicates:
    figFilename = 'plots_modulation_switching_remove_dup' # Do not include extension
else:
    figFilename = 'plots_modulation_switching'
'''
figFilename = 'plots_soundres_modulation_switching'
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,7]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1

labelPosX = [0.02, 0.54]   # Horiz position for panel labels
labelPosY = [0.95, 0.67, 0.48, 0.35]    # Vert position for panel labels

#COLORMAP = {'leftTrials':'red', 'rightTrials':'green'}

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(6, 2)
gs.update(left=0.14, right=0.98, top=0.95, bottom=0.1, wspace=0.5, hspace=1.5)
#gs00 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[0,0], hspace=0.15)
gs01 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[0:3,1], hspace=0.15)
gs02 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[3:,1], hspace=0.15)

#timeRangeSound = [-0.2, 0.4]
msRaster = 2
msMvStart = 3
smoothWinSizePsth = 2#3
lwPsth = 2
downsampleFactorPsth = 1

# -- Panel A: schematic of switching task -- #
#ax1 = plt.subplot(gs[0:2, 0:2])
ax1 = plt.subplot(gs[0:2, 0])
plt.axis('off')
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

# -- Panel B: example dynamics plot -- #
ax2 = plt.subplot(gs[2:4, 0])
ax1.annotate('B', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

animal = 'test089'
paradigm = '2afc'
session = '20160113a'
winsize = 40
behavFileName = loadbehavior.path_to_behavior_data(animal,paradigm,session)
behavData = loadbehavior.FlexCategBehaviorData(behavFileName)
hPlots = behavioranalysis.plot_dynamics(behavData, winsize=winsize, fontsize=fontSizeLabels, soundfreq=None)
extraplots.boxoff(plt.gca())
plt.setp(hPlots[1], color=colorLeft) #Block1, midFreq
plt.setp(hPlots[2], color='grey') #Block1, highFreq
plt.setp(hPlots[3], color='grey') #Block2, lowFreq
plt.setp(hPlots[4], color=colorRight) #Block2, midFreq
plt.setp(hPlots[8], color='grey') #Block3, highFreq
plt.setp(hPlots[7], color=colorLeft) #Block3, midFreq
plt.setp(hPlots[9], color='grey') #Block4, lowFreq
plt.setp(hPlots[10], color=colorRight) #Block4, midFreq
plt.xlim([0,740])
plt.xticks([0,200,400,600])
plt.yticks([0,50,100])
plt.ylabel('Rightward\ntrials (%)', labelpad=0.5, fontsize=fontSizeLabels)
plt.xlabel('Trial', fontsize=fontSizeLabels)
#plt.fill([80,160,160,80],[110,110,113,113], ec='none', fc=colorLeft, clip_on=False)
#plt.fill([450,530,530,450],[110,110,113,113], ec='none', fc=colorRight, clip_on=False)
plt.text(30, 38, '11', fontsize=fontSizeLabels)
plt.text(165, 38, 'L', fontsize=fontSizeLabels)
plt.text(255, 38, '11', fontsize=fontSizeLabels)
plt.text(390, 38, 'R', fontsize=fontSizeLabels)
# -- Panel C: representative sound-evoked raster from switching task, Not modulated-- #
ax3 = plt.subplot(gs02[0:2, :])
ax3.annotate('E', xy=(labelPosX[1],labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

if PANELS[0]:
    rasterFilename = 'example_switching_midfreq_soundaligned_raster_adap020_20160526a_T2_c9.npz'  # H-L-H blocks
    rasterFullPath = os.path.join(dataDir, rasterFilename)
    rasterExample = np.load(rasterFullPath)

    trialsEachCond = rasterExample['trialsEachCond']
    colorEachCond = [colorLeft, colorRight, colorLeft, colorRight] #rasterExample['colorEachCond']
    spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
    indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
    #timeRange = rasterExample['timeRange']

    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRange=timeRange,
                                                   trialsEachCond=trialsEachCond,
                                                   colorEachCond=colorEachCond)

    plt.setp(pRaster, ms=msRaster)

    movementTimesFromEventOnset = rasterExample['movementTimesFromEventOnset']
    trialsToUse = np.sum(trialsEachCond, axis=1).astype('bool')
    yLims = plt.gca().get_ylim()
    plt.hold('on')
    bplot = plt.boxplot(movementTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]+10], widths=[15])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')
    
    ax3.set_yticklabels([])
    ax3.set_xticklabels([])
    #plt.ylabel('Trials',fontsize=fontSizeLabels) #, labelpad=labelDis)
    #plt.ylabel('Mid-freq trials\ngrouped by choice', fontsize=fontSizeLabels)
    plt.ylabel('Mid-freq correct\ntrials each block', fontsize=fontSizeLabels)
    #plt.xlim(timeRangeSound[0],timeRangeSound[1])
    
    # -- Panel B2: representative sound-evoked psth from switching task, Not modulated -- #
    ax3 = plt.subplot(gs02[2, :])
    psthFilename = 'example_switching_midfreq_soundaligned_psth_adap020_20160526a_T2_c9.npz' 
    psthFullPath = os.path.join(dataDir, psthFilename)
    psthExample =np.load(psthFullPath)

    trialsEachCond = psthExample['trialsEachCond']
    spikeCountMat = psthExample['spikeCountMat']
    timeVec = psthExample['timeVec']
    binWidth = psthExample['binWidth']
    #timeRange = psthExample['timeRange']
    #colorEachCond = [colorLeft, colorRight, colorLeft, colorRight]

    extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    #left_line = mlines.Line2D([], [], color=colorsDict['colorL'], label='left choice')
    #right_line = mlines.Line2D([], [], color=colorsDict['colorR'], label='right choice')
    #plt.legend(handles=[left_line, right_line], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)
    plt.legend(['11 kHz = left','11 kHz = right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
               frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)
    
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    plt.xlim(timeRange)
    yLims = [0,50]
    soundBarHeight = 0.1*yLims[-1]
    plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels, labelpad=labelDis)
    extraplots.boxoff(plt.gca())

# -- Panel B: representative sound-evoked raster from switching task, modulated -- #
#ax4 = plt.subplot(gs[2, 0:2])
ax4 = plt.subplot(gs01[0:2, :])
ax4.annotate('D', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

if PANELS[1]:
    rasterFilename = 'example_switching_midfreq_soundaligned_raster_test089_20160124a_T4_c6.npz'   # H-L-H blocks
    rasterFullPath = os.path.join(dataDir, rasterFilename)
    rasterExample =np.load(rasterFullPath)

    trialsEachCond = rasterExample['trialsEachCond']
    colorEachCond = [colorLeft, colorRight, colorLeft, colorRight] #rasterExample['colorEachCond']
    spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
    indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
    #timeRange = rasterExample['timeRange']

    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRange=timeRange,
                                                   trialsEachCond=trialsEachCond,
                                                   colorEachCond=colorEachCond,
                                                   fillWidth=None,labels=None)

    plt.setp(pRaster, ms=msRaster)

    movementTimesFromEventOnset = rasterExample['movementTimesFromEventOnset']
    trialsToUse = np.sum(trialsEachCond, axis=1).astype('bool')
    yLims = plt.gca().get_ylim()
    plt.hold('on')
    bplot = plt.boxplot(movementTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]+10], widths=[15])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')

    ax4.set_yticklabels([])
    ax4.set_xticklabels([])
    #plt.ylabel('Trials',fontsize=fontSizeLabels, labelpad=labelDis)
    #plt.ylabel('Mid-freq trials\ngrouped by choice', fontsize=fontSizeLabels)
    plt.ylabel('Mid-freq correct\ntrials each block', fontsize=fontSizeLabels)
    #plt.xlim(timeRangeSound[0],timeRangeSound[1])
    
    

    # -- Panel C2: representative sound-evoked psth from switching task, modulated -- #
    ax5 = plt.subplot(gs01[2, :])
    psthFilename = 'example_switching_midfreq_soundaligned_psth_test089_20160124a_T4_c6.npz' 
    psthFullPath = os.path.join(dataDir, psthFilename)
    psthExample =np.load(psthFullPath)

    trialsEachCond = psthExample['trialsEachCond']
    spikeCountMat = psthExample['spikeCountMat']
    timeVec = psthExample['timeVec']
    binWidth = psthExample['binWidth']
    #timeRange = psthExample['timeRange']
    #colorEachCond = [colorLeft, colorRight, colorLeft, colorRight]

    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    # -- Place line for second block of trials at the top --
    plt.setp(pPSTH[1],zorder=3)
             
    plt.legend(['11 kHz = left','11 kHz = right'], loc='upper right', bbox_to_anchor=(1, 1.1),
               fontsize=fontSizeTicks, handlelength=0.2,
               frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,25]
    soundBarHeight = 0.1*yLims[-1]
    plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.xlim(timeRange)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels, labelpad=labelDis)
    extraplots.boxoff(plt.gca())

# -- Panel D: summary distribution of switching modulation index, total cells is good cells in striatum (nonduplicate) that are responsive to mid freq -- #
#ax6 = plt.subplot(gs[2:,2:4])
ax6 = plt.subplot(gs[4:,0])
ax6.annotate('C', xy=(labelPosX[0],labelPosY[3]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[2]:
    colorMod = 'black'
    colorNotMod = 'darkgrey'
    '''
    if removedDuplicates:
        summaryFilename = 'summary_switching_sound_modulation_good_cells_responsive_midfreq_remove_dup.npz'
    else:
        summaryFilename = 'summary_switching_sound_modulation_good_cells_responsive_midfreq.npz'
    '''
    summaryFilename = 'summary_switching_sound_modulation_good_cells_responsive_midfreq_remove_dup.npz'
    summaryFullPath = os.path.join(dataDir,summaryFilename)
    summary = np.load(summaryFullPath)

    sigModulated = summary['modulated']
    sigMI = summary['modulationIndex'][sigModulated]
    nonsigMI = summary['modulationIndex'][~sigModulated]
    binsEdges = np.linspace(-1,1,20)
    plt.hist([sigMI,nonsigMI], bins=binsEdges, color=[colorMod,colorNotMod], edgecolor='None', stacked=True)
    '''
    sig_patch = mpatches.Patch(color=colorMod, label='Modulated')
    nonsig_patch = mpatches.Patch(color=colorNotMod, label='Not modulated')
    plt.legend(handles=[sig_patch,nonsig_patch], fontsize=fontSizeTicks, frameon=False, labelspacing=0.1, handlelength=0.2)
    '''
    yPosText = 0.95*plt.ylim()[1]
    plt.text(-0.5,yPosText,'Contra',ha='center',fontsize=fontSizeLabels)
    plt.text(0.5,yPosText,'Ipsi',ha='center',fontsize=fontSizeLabels)
    plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Modulation index', fontsize=fontSizeLabels)
    plt.ylabel('Number of cells', fontsize=fontSizeLabels) #, labelpad=labelDis)
    extraplots.boxoff(plt.gca())

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
print 'Total number of good cells responsive to mid frequency is:', len(sigModulated), '\nNumber of cells significantly modulated is:', sum(sigModulated)
(T, pVal) = stats.wilcoxon(summary['modulationIndex'])
print 'Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of {:.3f}'.format(pVal)
