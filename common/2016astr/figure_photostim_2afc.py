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
import figparams

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To

dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'fig_photostim_2afc' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [8,6]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.07, 0.5]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

PHOTOSTIMCOLORS = {'no_laser':'k', 'laser_left':'red', 'laser_right':'green'}

SHAPESEACHANIMAL = ['o','s','^']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 4)
gs.update(left=0.15, right=0.85, wspace=1, hspace=0.5)


# -- Panel A: schematic of 2afc task -- #
ax1 = plt.subplot(gs[0, 0:2])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


# -- Panel B: representative histology/schematic about implant -- #
ax2 = plt.subplot(gs[0,2:])
ax2.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


# -- Panel C1: representative photostim psycurves -- #
ax3 = plt.subplot(gs[1,0])
leftExampleFilename = 'example_photostim_psycurve_d1pi015_20160829a.npz'
leftExampleFullPath = os.path.join(dataDir,leftExampleFilename)
leftExample = np.load(leftExampleFullPath)

possibleValues = leftExample['possibleValues']
for stimType in ['no_laser','laser_left']:
    fractionHitsEachValue = leftExample['fractionHitsEachValue_'+stimType]
    ciHitsEachValue = leftExample['ciHitsEachValue_'+stimType]

    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,ciHitsEachValue,xTickPeriod=1)
    plt.setp((pline, pcaps, pbars), color=PHOTOSTIMCOLORS[stimType])
    plt.hold(True)
    plt.setp(pdots, mfc=PHOTOSTIMCOLORS[stimType], mec=PHOTOSTIMCOLORS[stimType])
    plt.hold(True)
plt.title('Left AStr Stim',fontsize=fontSizeLabels)
plt.xlabel('Frequency (kHz)',fontsize=fontSizeLabels)
plt.ylabel('Rightward trials (%)',fontsize=fontSizeLabels)
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
ax3.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

# -- Panel C2: another representative photostim psycurves -- #

ax4 = plt.subplot(gs[1,1])
rightExampleFilename = 'example_photostim_psycurve_d1pi016_20160803a.npz'
rightExampleFullPath = os.path.join(dataDir,rightExampleFilename)
rightExample = np.load(rightExampleFullPath)

possibleValues = rightExample['possibleValues']
for stimType in ['no_laser','laser_right']:
    fractionHitsEachValue = rightExample['fractionHitsEachValue_'+stimType]
    ciHitsEachValue = rightExample['ciHitsEachValue_'+stimType]

    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,ciHitsEachValue,xTickPeriod=1)
    plt.setp((pline, pcaps, pbars), color=PHOTOSTIMCOLORS[stimType])
    plt.hold(True)
    plt.setp(pdots, mfc=PHOTOSTIMCOLORS[stimType], mec=PHOTOSTIMCOLORS[stimType])
    plt.hold(True)
plt.title('Right AStr Stim',fontsize=fontSizeLabels)
plt.xlabel('Frequency (kHz)',fontsize=fontSizeLabels)
plt.ylabel('Rightward trials (%)',fontsize=fontSizeLabels)
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)


# -- Panel D: summary for effect of photostim on performance -- #
ax5 = plt.subplot(gs[1,2:])
summaryFilename = 'summary_photostim_percent_contra_choice_change.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
summary = np.load(summaryFullPath)

left014 = summary['d1pi014leftHemiStim']
left015 = summary['d1pi015leftHemiStim']
left016 = summary['d1pi016leftHemiStim']
right014 = summary['d1pi014rightHemiStim']
right015 = summary['d1pi015rightHemiStim']
right016 = summary['d1pi016rightHemiStim']

for ind,leftData in enumerate([left014,left015,left016]):
    ax5.plot(np.repeat(1+0.2*(ind-1),len(leftData)), leftData, marker=SHAPESEACHANIMAL[ind], mfc=PHOTOSTIMCOLORS['laser_left'], ls='None')
    
for ind,rightData in enumerate([right014,right015,right016]):
    ax5.plot(np.repeat(2+0.2*(ind-1),len(rightData)), rightData, marker=SHAPESEACHANIMAL[ind], mfc=PHOTOSTIMCOLORS['laser_right'], ls='None')
xlim = [0.3,2.7]
ylim = [-0.2, 0.5]
plt.xlim(xlim)
plt.ylim(ylim)
xticks = [1,2]
xticklabels = ['left', 'right']
plt.xticks(xticks, xticklabels, fontsize=fontSizeTicks)
plt.xlabel('Photostim hemisphere', fontsize=fontSizeLabels)
plt.ylabel('Contralateral bias: stim - control (%)', fontsize=fontSizeLabels)
ax5.annotate('D', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

