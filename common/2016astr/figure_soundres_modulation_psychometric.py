'''
Create figure about the activity of astr neurons during sound being modulated by choice in the psychometric curve task.
'''
import os
import numpy as np
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

FIGNAME = 'soundres_modulation_psychometric'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

removedDuplicates = True

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

#dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)

colorsDict = {'colorL':figparams.colp['MidFreqL'], 
              'colorR':figparams.colp['MidFreqR']} 
soundColor = figparams.colp['sound']
timeRange = [-0.3,0.5]

# -- Select example cells here -- #
exampleModulatedSharp = '11607Hz_adap017_20160411a_T3_c10'
exampleModulatedSustained = '11990Hz_adap017_20160414a_T4_c9'
exampleNonModSharp = '9781Hz_test055_20150313a_T4_c7'
exampleNonModSustained = '12216Hz_adap017_20160317a_T5_c3'
if 1:
    exampleModulated = exampleModulatedSharp
    exampleNonMod = exampleNonModSharp
else:
    exampleModulated = exampleModulatedSustained
    exampleNonMod = exampleNonModSustained
   
    

PANELS = [1,1,1] # Which panels to plot

SAVE_FIGURE = 1
outputDir = '/tmp/'
'''
if removedDuplicates:
    figFilename = 'plots_choice_modulation_psychometric_remove_dup'
else:
    figFilename = 'plots_choice_modulation_psychometric' # Do not include extension
'''
figFilename = 'figure_soundres_modulation_psychometric'
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [10,3.5]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
#labelDis = 0.1

labelPosX = [0.015, 0.355, 0.68]   # Horiz position for panel labels
labelPosY = [0.92]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 3)
gs.update(left=0.08, right=0.98, top=0.95, bottom=0.15, wspace=0.4, hspace=0.1)

gs00 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gs[:,0], hspace=0.15)
gs01 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gs[:,1], hspace=0.15)

#timeRangeSound = [-0.2, 0.4]
msRaster = 2
msMvStart = 3
smoothWinSizePsth = 3
lwPsth = 2
downsampleFactorPsth = 1

'''
# -- Panel A: schematic of psychometric curve indicating center freq-- #
#ax1 = plt.subplot(gs[0, 0:2])
ax1 = plt.subplot(gs[0, 0])
plt.axis('off')


ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
'''

ax2 = plt.subplot(gs01[0:3, :])
ax2.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

if PANELS[1]:
    rasterFilename = 'example_psycurve_soundaligned_raster_{}.npz'.format(exampleNonMod) 
    rasterFullPath = os.path.join(dataDir, rasterFilename)
    rasterExample =np.load(rasterFullPath)

    trialsEachCond = rasterExample['trialsEachCond']
    colorEachCond = rasterExample['colorEachCond']
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
    bplot = plt.boxplot(movementTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]+5], widths=[5])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')

    #plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    #ax2.axes.xaxis.set_ticklabels([])
    ax2.set_yticklabels([])
    ax2.set_xticklabels([])
    #plt.ylabel('Trials',fontsize=fontSizeLabels,labelpad=labelDis)
    plt.ylabel('Mid-freq trials\ngrouped by choice', fontsize=fontSizeLabels)
    #plt.xlim(timeRangeSound[0],timeRangeSound[1])


    # -- Panel B2: representative sound-evoked psth from psychometric task, Not modulated -- #
    ax3 = plt.subplot(gs01[3, :])
    psthFilename = 'example_psycurve_soundaligned_psth_{}.npz'.format(exampleNonMod)
    psthFullPath = os.path.join(dataDir, psthFilename)
    psthExample =np.load(psthFullPath)

    condLabels = psthExample['condLabels']
    trialsEachCond = psthExample['trialsEachCond']
    colorEachCond = psthExample['colorEachCond']
    spikeCountMat = psthExample['spikeCountMat']
    timeVec = psthExample['timeVec']
    binWidth = psthExample['binWidth']
    #timeRange = psthExample['timeRange']

    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    yLims = [0,100]
    soundBarHeight = 0.1*yLims[-1]
    plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xlim(timeRange)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #,labelpad=labelDis)
    extraplots.boxoff(plt.gca())
    
    plt.legend(['Left','Right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
           frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)


# -- Representative sound-evoked raster from psychometric task, Modulated-- #
ax4 = plt.subplot(gs00[0:3, :])
ax4.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    rasterFilename = 'example_psycurve_soundaligned_raster_{}.npz'.format(exampleModulated) 
    rasterFullPath = os.path.join(dataDir, rasterFilename)
    rasterExample =np.load(rasterFullPath)

    trialsEachCond = rasterExample['trialsEachCond']
    colorEachCond = rasterExample['colorEachCond']
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
    bplot = plt.boxplot(movementTimesFromEventOnset[trialsToUse], sym='', vert=False, positions=[yLims[-1]+5], widths=[5])
    extraplots.boxoff(plt.gca())
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.axis('off')
    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color='grey', linewidth=1)
    plt.setp(bplot['whiskers'], linestyle='-')
    plt.setp(bplot['medians'], color='orange')

    #plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels) 
    #ax4.axes.xaxis.set_ticklabels([])
    ax4.set_yticklabels([])
    ax4.set_xticklabels([])
    #plt.ylabel('Trials',fontsize=fontSizeLabels, labelpad=labelDis)
    plt.ylabel('Mid-freq trials\ngrouped by choice', fontsize=fontSizeLabels)
    #plt.xlim(timeRangeSound[0],timeRangeSound[1])



    # -- Panel C2: representative sound-evoked psth from psychometric task, Modulated -- #
    #ax5 = plt.subplot(gs[1,4:6])
    ax5 = plt.subplot(gs00[3, :])
    psthFilename = 'example_psycurve_soundaligned_psth_{}.npz'.format(exampleModulated)
    psthFullPath = os.path.join(dataDir, psthFilename)
    psthExample =np.load(psthFullPath)

    condLabels = psthExample['condLabels']
    trialsEachCond = psthExample['trialsEachCond']
    colorEachCond = psthExample['colorEachCond']
    spikeCountMat = psthExample['spikeCountMat']
    timeVec = psthExample['timeVec']
    binWidth = psthExample['binWidth']
    #timeRange = psthExample['timeRange']

    pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

    '''
    for ind,line in enumerate(pPSTH):
        plt.setp(line, label=condLabels[ind])
    plt.legend(loc='upper right', fontsize=fontSizeTicks, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)
    '''
    #plt.legend()
    plt.legend(['Left','Right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
           frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    plt.xlim(timeRange)
    yLims = [0,25]
    soundBarHeight = 0.1*yLims[-1]
    plt.fill([0,0.1,0.1,0],yLims[-1]+np.array([0,0,soundBarHeight,soundBarHeight]), ec='none', fc=soundColor, clip_on=False)
    plt.ylim(yLims)
    plt.yticks(yLims)
    plt.xticks(np.arange(-0.2,0.6,0.2))
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #, labelpad=labelDis)
    extraplots.boxoff(plt.gca())

# -- Panel D: summary distribution of psychometric modulation index -- #
ax6 = plt.subplot(gs[0,2])
ax6.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[2]:
    '''
    if removedDuplicates:
        summaryFilename = 'summary_psychometric_sound_modulation_good_cells_responsive_midfreq_remove_dup.npz'
    else:
        summaryFilename = 'summary_psychometric_sound_modulation_good_cells_responsive_midfreq.npz'
    '''
    summaryFilename = 'summary_psychometric_sound_modulation_good_cells_responsive_midfreq_remove_dup.npz'
    summaryFullPath = os.path.join(dataDir,summaryFilename)
    summary = np.load(summaryFullPath)

    sigModulated = summary['modulated']
    sigMI = summary['modulationIndex'][sigModulated]
    nonsigMI = summary['modulationIndex'][~sigModulated]
    #binsEdges = np.linspace(-1,1,30)
    binsEdges = np.linspace(-1,1,20)
    plt.hist([sigMI,nonsigMI], bins=binsEdges, edgecolor='None', color=['k','darkgrey'], stacked=True, rwidth=0.8)
    '''
    sig_patch = mpatches.Patch(color='k', label='Modulated')
    nonsig_patch = mpatches.Patch(color='darkgrey', label='Not modulated')
    plt.legend(handles=[sig_patch,nonsig_patch], loc='upper center', fontsize=fontSizeTicks, frameon=False, labelspacing=0.1, handlelength=0.2)
    '''

    yPosText = 0.95*plt.ylim()[1]
    plt.text(-0.5,yPosText,'Contra',ha='center',fontsize=fontSizeLabels)
    plt.text(0.5,yPosText,'Ipsi',ha='center',fontsize=fontSizeLabels)
    plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Modulation index', fontsize=fontSizeLabels)
    plt.ylabel('Number of cells', fontsize=fontSizeLabels)
    extraplots.boxoff(plt.gca())
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)


# -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
print 'Total number of good cells responsive to mid frequency is:', len(sigModulated), '\nNumber of cells significantly modulated is:', sum(sigModulated)
(T, pVal) = stats.wilcoxon(summary['modulationIndex'])
print 'Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of', pVal
