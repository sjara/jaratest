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
import matplotlib
import matplotlib.lines as mlines
import figparams
import scipy.stats as stats


FIGNAME = 'photostim_2afc'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_photostim_2afc' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [7,5]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1
labelPosX = [0.07, 0.45]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

PHOTOSTIMCOLORS = {'no_laser':'k', 'laser_left':'red', 'laser_right':'green'}

SHAPESEACHANIMAL = {'d1pi014':'o',
                    'd1pi015':'s',
                    'd1pi016':'^'}

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 4)
gs.update(left=0.15, right=0.85, wspace=1.5, hspace=0.7)


# -- Panel A: schematic of 2afc task -- #
ax1 = plt.subplot(gs[0, 0:2])
plt.axis('off')
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

'''
# -- Panel B: representative histology/schematic about implant -- #
ax2 = plt.subplot(gs[0,2:])
plt.axis('off')
ax2.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
'''

# -- Panel B: representative photostim psycurves -- #
#ax3 = plt.subplot(gs[1,0])
ax3 = plt.subplot(gs[0,2:])
leftExampleFilename = 'example_photostim_psycurve_d1pi015_20160829a.npz'
leftExampleFullPath = os.path.join(dataDir,leftExampleFilename)
leftExample = np.load(leftExampleFullPath)

possibleValues = leftExample['possibleValues']
for stimType in ['no_laser','laser_left']:
    fractionHitsEachValue = leftExample['fractionHitsEachValue_'+stimType]
    ciHitsEachValue = leftExample['ciHitsEachValue_'+stimType]

    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,ciHitsEachValue,xTickPeriod=1)
    plt.setp((pline, pcaps, pbars), color=PHOTOSTIMCOLORS[stimType])
    plt.setp(pline, label=stimType)
    plt.hold(True)
    plt.setp(pdots, mfc=PHOTOSTIMCOLORS[stimType], mec=PHOTOSTIMCOLORS[stimType])
    plt.hold(True)
#plt.title('Left AStr Stim',fontsize=fontSizeLabels)
plt.legend(scatterpoints=1, loc='lower right', labelspacing=0.1, fontsize=fontSizeTicks, frameon=False)

plt.xlabel('Frequency (kHz)',fontsize=fontSizeLabels, labelpad=labelDis)
plt.ylabel('Rightward trials (%)',fontsize=fontSizeLabels, labelpad=labelDis)
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
#ax3.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
ax3.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

# -- Panel C: another representative photostim psycurves -- #
ax4 = plt.subplot(gs[1,:2])
rightExampleFilename = 'example_photostim_psycurve_d1pi015_20160817a.npz'
rightExampleFullPath = os.path.join(dataDir,rightExampleFilename)
rightExample = np.load(rightExampleFullPath)

possibleValues = rightExample['possibleValues']
for stimType in ['no_laser','laser_right']:
    fractionHitsEachValue = rightExample['fractionHitsEachValue_'+stimType]
    ciHitsEachValue = rightExample['ciHitsEachValue_'+stimType]

    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,ciHitsEachValue,xTickPeriod=1)
    plt.setp((pline, pcaps, pbars), color=PHOTOSTIMCOLORS[stimType])
    plt.setp(pline, label=stimType)
    plt.hold(True)
    plt.setp(pdots, mfc=PHOTOSTIMCOLORS[stimType], mec=PHOTOSTIMCOLORS[stimType])
    plt.hold(True)

#plt.title('Right AStr Stim',fontsize=fontSizeLabels)
plt.legend(scatterpoints=1, loc='upper left', labelspacing=0.1, fontsize=fontSizeTicks, frameon=False)
labelDis = 0.1
plt.xlabel('Frequency (kHz)',fontsize=fontSizeLabels, labelpad=labelDis)
plt.ylabel('Rightward trials (%)',fontsize=fontSizeLabels, labelpad=labelDis)
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)

ax4.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

# -- Panel D: summary for effect of photostim on performance -- #
ax5 = plt.subplot(gs[1,2:])
#summaryFilename = 'summary_photostim_percent_contra_choice_change.npz'
summaryFilename = 'summary_photostim_percent_right_choice_change.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
summary = np.load(summaryFullPath)

left014 = summary['d1pi014leftHemiStim']
left015 = summary['d1pi015leftHemiStim']
left016 = summary['d1pi016leftHemiStim']
right014 = summary['d1pi014rightHemiStim']
right015 = summary['d1pi015rightHemiStim']
right016 = summary['d1pi016rightHemiStim']

# -- Stats for individual animals -- #
# Comparing bias resulting from stimulating each hemisphere to zero (paired since one session has both stim trials and control trials)
(T, leftpVal014) = stats.wilcoxon(left014)
(T, leftpVal015) = stats.wilcoxon(left015)
(T, leftpVal016) = stats.wilcoxon(left016)
(T, rightpVal014) = stats.wilcoxon(right014)
(T, rightpVal015) = stats.wilcoxon(right015)
(T, rightpVal016) = stats.wilcoxon(right016)
print 'd1pi014 left hemi stim ({} sessions), p value for rightward bias in stim trials vs control trials is: {}'.format(len(left014),leftpVal014)
print 'd1pi015 left hemi stim ({} sessions), p value for rightward bias in stim trials vs control trials is: {}'.format(len(left015),leftpVal015)
print'd1pi016 left hemi stim ({} sessions), p value for rightward bias in stim trials vs control trials is: {}'.format(len(left016),leftpVal016)
print 'd1pi014 right hemi stim ({} sessions), p value for rightward bias in stim trials vs control trials is: {}'.format(len(right014),rightpVal014)
print 'd1pi015 right hemi stim ({} sessions), p value for rightward bias in stim trials vs control trials is: {}'.format(len(right015),rightpVal015)
print'd1pi016 right hemi stim ({} sessions), p value for rightward bias in stim trials vs control trials is: {}'.format(len(right016),rightpVal016)

# Comparing bias resulting from stimulation of left vs right hemi in one mouse, using all sessions so left and right may have different number of sessions for each mouse
(Z, lvrpVal014) = stats.ranksums(left014, right014)
(Z, lvrpVal015) = stats.ranksums(left015, right015)
(Z, lvrpVal016) = stats.ranksums(left016, right016)
print 'd1pi014 p value for bias resulting from left vs right hemi stim is: {}'.format(lvrpVal014)
print 'd1pi015 p value for bias resulting from left vs right hemi stim is: {}'.format(lvrpVal015)
print 'd1pi016 p value for bias resulting from left vs right hemi stim is: {}'.format(lvrpVal016)

# -- Select the first 10 sessions from each hemi each mouse so that they have equal number of sessions -- #
left014 = left014[:11]
left015 = left015[:11]
left016 = left016[:11]
right014 = right014[:11]
right015 = right015[:11]
right016 = right016[:11]

for animal,leftData in zip(['d1pi014','d1pi015','d1pi016'],[left014,left015,left016]):
    #ax5.scatter(np.repeat(1+0.2*(ind-1),len(leftData)), 100*leftData, marker=SHAPESEACHANIMAL[animal], color=PHOTOSTIMCOLORS['laser_left'], edgecolors="black")
    ax5.scatter(1+0.5*np.random.rand(len(leftData)), 100*leftData, color=PHOTOSTIMCOLORS['laser_left'], edgecolors="black")
    
for animal,rightData in zip(['d1pi014','d1pi015','d1pi016'],[right014,right015,right016]):
    #ax5.scatter(np.repeat(2+0.2*(ind-1),len(rightData)), 100*rightData, marker=SHAPESEACHANIMAL[animal], color=PHOTOSTIMCOLORS['laser_right'], edgecolors="black")
    ax5.scatter(2+0.5*np.random.rand(len(rightData)), 100*rightData, color=PHOTOSTIMCOLORS['laser_right'], edgecolors="black")
'''
# -- Add shapes as legend -- #
lines=[]
for ind,shape in enumerate(SHAPESEACHANIMAL):
    line = mlines.Line2D([], [], color='white', marker=shape, markerfacecolor='white', markeredgecolor='black')
    lines.append(line)
plt.legend(lines, ('Mouse1','Mouse2','Mouse3'), numpoints=1, markerscale=0.7, loc='upper right', labelspacing=0.1, fontsize=fontSizeTicks, frameon=False)
'''

xlim = [0.8,2.7]
ylim = [-50, 50]
plt.xlim(xlim)
plt.ylim(ylim)
xticks = [1.25,2.25]
xticklabels = ['left', 'right']
plt.xticks(xticks, xticklabels, fontsize=fontSizeTicks)
labelDis = 0.1
plt.xlabel('Photostim hemisphere', fontsize=fontSizeLabels, labelpad=labelDis)
plt.ylabel('Rightward bias: stim - control (%)', fontsize=fontSizeLabels, labelpad=labelDis)
ax5.annotate('D', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# -- Stats for summary panel in figure grouping all animals together -- #
leftStimChange = np.concatenate((left014,left015,left016))
rightStimChange = np.concatenate((right014,right015,right016))

#(T, leftpVal) = stats.wilcoxon(leftStimChange)
#(T, rightpVal) = stats.wilcoxon(rightStimChange)
#print 'p value for change in percent rightward in left hemi photostim is: ', leftpVal,  '\np value for change in percent rightward in left hemi photostim is: ', rightpVal

# -- Grouped left and right hemi data separately for all three mice, compare bias resulting from left vs right hemi stim -- #
(Z, pVal) = stats.ranksums(leftStimChange, rightStimChange)
print 'Using 10 sessions for each animal in each hemi, the overall p value for the difference of the changes of percent rightward choice from left vs. right hemi photostim is: ', pVal, ' (ranksums test)'
