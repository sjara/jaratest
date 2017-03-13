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

labelPosX = [0.07, 0.35, 0.6]   # Horiz position for panel labels
labelPosY = [0.9]    # Vert position for panel labels

PHOTOSTIMCOLORS = {'no_laser':'k', 'laser_left':'red', 'laser_right':'green'}

#SHAPESEACHANIMAL = ['o','s','^']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 6)
gs.update(left=0.15, right=0.85, wspace=2.5, hspace=0.2)


# -- Panel A: representative sound-evoked raster from tuning task -- #
ax1 = plt.subplot(gs[0, 0:2])

rasterFilename = 'example_freq_tuning_raster_adap020_20160420a_T3_c5.npz' 
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
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


# -- Panel A2: representative sound-evoked psth from tuning task -- #
ax2 = plt.subplot(gs[1,0:2])

psthFilename = 'example_freq_tuning_psth_adap020_20160420a_T3_c5.npz' 
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


'''
# -- Panel B: summary of sound freq selectivity during psychometric curve task -- #
ax3 = plt.subplot(gs[0:,2:4])
psycurveSumFilename = 'summary_freq_selectivity_all_psycurve_mice.npz' 
psycurveSumFullPath = os.path.join(dataDir, psycurveSumFilename)
psycurveSum =np.load(psycurveSumFullPath)

psycurveMice = psycurveSum['psychometricMice']
numOfFreqs = psycurveSum['numOfFreqs']
allFreqs = range(numOfFreqs)
cellProportion = np.empty((len(psycurveMice),numOfFreqs))
for ind,mouse in enumerate(psycurveMice):
    cellProportionThisMouse = psycurveSum[mouse]/sum(psycurveSum[mouse]).astype('float')*100
    cellProportion[ind,:] = cellProportionThisMouse

for indf in allFreqs:
    x = np.repeat(indf+1,len(psycurveMice))
    y = cellProportion[:,indf]
    ax3.scatter(x,y)
'''

# -- Panel B: another example of sound-evoked raster and psth from tuning task -- #
ax3 = plt.subplot(gs[0, 2:4])

rasterFilename = 'example_freq_tuning_raster_test089_20150911a_T7_c7.npz' 
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

ax3.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


ax4 = plt.subplot(gs[1,2:4])

psthFilename = 'example_freq_tuning_psth_test089_20150911a_T7_c7.npz' 
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


# -- Panel C: summary left vs right hemi best frequency (from photostim mice) -- #
ax5 = plt.subplot(gs[0:,4:6])

summaryFilename = 'summary_bilateral_best_freq.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
summary = np.load(summaryFullPath)

left014 = summary['d1pi014_left']
left015 = summary['d1pi015_left']
left016 = summary['d1pi016_left']
right014 = summary['d1pi014_right']
right015 = summary['d1pi015_right']
right016 = summary['d1pi016_right']

#for ind,leftData in enumerate([left014,left015,left016]):
    #ax4.plot(np.repeat(1+0.2*(ind-1),len(leftData)), leftData, marker=SHAPESEACHANIMAL[ind], mfc=PHOTOSTIMCOLORS['laser_left'], ls='None')
    
#for ind,rightData in enumerate([right014,right015,right016]):
    #ax4.plot(np.repeat(2+0.2*(ind-1),len(rightData)), rightData, marker=SHAPESEACHANIMAL[ind], mfc=PHOTOSTIMCOLORS['laser_right'], ls='None')

leftData = np.r_[left014,left015,left016]
kdeLeft = stats.gaussian_kde(leftData)
densityLeft = kdeLeft(leftData)
xleft = 1 + densityLeft * (np.random.rand(*leftData.shape) - 0.5) 
#xleft = 1+0.3*(np.random.rand(*leftData.shape)-0.5)
ax5.plot(xleft, leftData, marker='o', mfc=PHOTOSTIMCOLORS['laser_left'], ls='None', alpha=0.7)

rightData = np.r_[right014,right015,right016]
kdeRight = stats.gaussian_kde(rightData)
densityRight = kdeRight(rightData)
xright = 2 + densityRight * (np.random.rand(*rightData.shape) - 0.5) 
#xright = 2+0.3*(np.random.rand(*rightData.shape)-0.5)
ax5.plot(xright, rightData, marker='o', mfc=PHOTOSTIMCOLORS['laser_right'], ls='None', alpha=0.7)

xlim = [0.3,2.7]
ylim = [-2, 2]
plt.axhline(y=0, linestyle='--',linewidth=1.5, color='k')
plt.xlim(xlim)
plt.ylim(ylim)
xticks = [1,2]
xticklabels = ['left', 'right']
plt.xticks(xticks, xticklabels, fontsize=fontSizeTicks)

labelDis = 0.1
plt.xlabel('Recording hemisphere', fontsize=fontSizeLabels, labelpad=labelDis)
plt.ylabel('Log2(most responsive frequency - psychometric boundary)', fontsize=fontSizeLabels,labelpad=labelDis)
ax5.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)


# -- Statistic test for comparing left versus right hemi tuning -- #
import scipy.stats as stats
(x,pvalue) = stats.ranksums(leftData,rightData)
print 'all three mice left vs right hemi best freq\n p value:', pvalue
