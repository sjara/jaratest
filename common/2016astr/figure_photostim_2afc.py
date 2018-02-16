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
import scipy.stats as stats
import figparams
reload(figparams)

FIGNAME = 'photostim_2afc'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1,1] # Which panels to plot

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_photostim_2afc' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,5]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1
labelPosX = [0.02, 0.54]   # Horiz position for panel labels
labelPosY = [0.95, 0.48]    # Vert position for panel labels

PHOTOSTIMCOLORS = {'no_laser':'k',
                   'laser_left':figparams.colp['stimLeft'],
                   'laser_right':figparams.colp['stimRight']}

SHAPESEACHANIMAL = {'d1pi014':'o',
                    'd1pi015':'s',
                    'd1pi016':'^'}

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 4)
gs.update(left=0.12, right=0.98, top=0.95, bottom=0.1, wspace=1.8, hspace=0.15)


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
if PANELS[0]:
    leftExampleFilename = 'example_photostim_psycurve_d1pi015_20160829a.npz'
    leftExampleFullPath = os.path.join(dataDir,leftExampleFilename)
    leftExample = np.load(leftExampleFullPath)

    possibleValues = leftExample['possibleValues']
    plotHandles = []
    for stimType in ['no_laser','laser_left']:
        fractionHitsEachValue = leftExample['fractionHitsEachValue_'+stimType]
        ciHitsEachValue = leftExample['ciHitsEachValue_'+stimType]
        upperWhisker = ciHitsEachValue[1,:]-fractionHitsEachValue
        lowerWhisker = fractionHitsEachValue-ciHitsEachValue[0,:]
        fitxvals = leftExample['fitxval_'+stimType]
        fityvals = leftExample['fityval_'+stimType]
        logPossibleValues = np.log2(leftExample['possibleValues'])

        plt.hold(True)
        (pline, pcaps, pbars) = ax3.errorbar(logPossibleValues,
                                             100*fractionHitsEachValue,
                                             yerr = [100*lowerWhisker, 100*upperWhisker],
                                             ecolor=PHOTOSTIMCOLORS[stimType], fmt=None, clip_on=False)
        pdots = ax3.plot(logPossibleValues, 100*fractionHitsEachValue, 'o', ms=6, mec='None',
                         mfc=PHOTOSTIMCOLORS[stimType], clip_on=False)
        pfit, = ax3.plot(fitxvals, 100*fityvals, color=PHOTOSTIMCOLORS[stimType], lw=2, clip_on=False)
        plotHandles.append(pfit)

        '''
        (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                    ciHitsEachValue,xTickPeriod=1)
        plotHandles.append(pline)
        plt.setp((pline, pcaps, pbars), color=PHOTOSTIMCOLORS[stimType])
        plt.setp(pline, label=stimType)
        plt.setp(pline,lw=2)
        plt.setp(pdots,ms=6)
        plt.hold(True)
        plt.setp(pdots, mfc=PHOTOSTIMCOLORS[stimType], mec=PHOTOSTIMCOLORS[stimType])
        plt.hold(True)
        '''

    extraplots.boxoff(ax3)
    #labelDis = 0.1
    plt.xlim([fitxvals[0],fitxvals[-1]])
    xTicks = np.array([6,11,19])
    ax3.set_xticks(np.log2(xTicks*1000))
    freqLabels = ['{:d}'.format(x) for x in xTicks]
    ax3.set_xticklabels(freqLabels)
    ax3.set_xticklabels('')
    #plt.xlabel('Frequency (kHz)',fontsize=fontSizeLabels)  # labelpad=labelDis
   
    ax3.set_ylim([0, 100])
    ax3.set_yticks([0, 50, 100])
    plt.ylabel('Rightward trials (%)',fontsize=fontSizeLabels) # labelpad=labelDis
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)

    plt.legend(plotHandles, ['No stim','Left stim'], loc='lower right', labelspacing=0.1,
               fontsize=fontSizeTicks, handlelength=1.5, handletextpad=0.2, borderaxespad=0.0, frameon=False)

    #ax3.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
    ax3.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


# -- Panel C: another representative photostim psycurves -- #
ax4 = plt.subplot(gs[1,2:])
ax4.annotate('C', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    rightExampleFilename = 'example_photostim_psycurve_d1pi015_20160901a.npz'
    rightExampleFullPath = os.path.join(dataDir,rightExampleFilename)
    rightExample = np.load(rightExampleFullPath)

    possibleValues = rightExample['possibleValues']
    plotHandles = []
    for stimType in ['no_laser','laser_right']:
        fractionHitsEachValue = rightExample['fractionHitsEachValue_'+stimType]
        ciHitsEachValue = rightExample['ciHitsEachValue_'+stimType]
        upperWhisker = ciHitsEachValue[1,:]-fractionHitsEachValue
        lowerWhisker = fractionHitsEachValue-ciHitsEachValue[0,:]
        fitxvals = rightExample['fitxval_'+stimType]
        fityvals = rightExample['fityval_'+stimType]
        logPossibleValues = np.log2(rightExample['possibleValues'])

        plt.hold(True)
        (pline, pcaps, pbars) = ax4.errorbar(logPossibleValues,
                                             100*fractionHitsEachValue,
                                             yerr = [100*lowerWhisker, 100*upperWhisker],
                                             ecolor=PHOTOSTIMCOLORS[stimType], fmt=None, clip_on=False)
        pdots = ax4.plot(logPossibleValues, 100*fractionHitsEachValue, 'o', ms=6, mec='None',
                         mfc=PHOTOSTIMCOLORS[stimType], clip_on=False)
        pfit, = ax4.plot(fitxvals, 100*fityvals, color=PHOTOSTIMCOLORS[stimType], lw=2, clip_on=False)
        plotHandles.append(pfit)
        
        '''
        (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                    ciHitsEachValue,xTickPeriod=1)
        plotHandles.append(pline)
        plt.setp((pline, pcaps, pbars), color=PHOTOSTIMCOLORS[stimType])
        plt.setp(pline, label=stimType)
        plt.setp(pline,lw=2)
        plt.setp(pdots,ms=6)
        plt.hold(True)
        plt.setp(pdots, mfc=PHOTOSTIMCOLORS[stimType], mec=PHOTOSTIMCOLORS[stimType])
        plt.hold(True)
        '''

    extraplots.boxoff(ax4)
    #labelDis = 0.1
    plt.xlim([fitxvals[0],fitxvals[-1]])
    xTicks = np.array([6,11,19])
    ax4.set_xticks(np.log2(xTicks*1000))
    freqLabels = ['{:d}'.format(x) for x in xTicks]
    ax4.set_xticklabels(freqLabels)
    plt.xlabel('Frequency (kHz)',fontsize=fontSizeLabels)  # labelpad=labelDis
   
    ax4.set_ylim([0, 100])
    ax4.set_yticks([0, 50, 100])
    plt.ylabel('Rightward trials (%)',fontsize=fontSizeLabels) # labelpad=labelDis
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)

    plt.legend(plotHandles, ['No stim','Right stim'], loc='upper left', labelspacing=0.1,
               fontsize=fontSizeTicks, handlelength=1.5, handletextpad=0.2, borderaxespad=0.0, frameon=False)

    #ax4.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


# -- Panel D: summary for effect of photostim on performance -- #
ax5 = plt.subplot(gs[1,:2])
ax5.annotate('D', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
if PANELS[2]:
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
    maxSessionNum = 10
    left014 = left014[:maxSessionNum]
    left015 = left015[:maxSessionNum]
    left016 = left016[:maxSessionNum]
    right014 = right014[:maxSessionNum]
    right015 = right015[:maxSessionNum]
    right016 = right016[:maxSessionNum]
    print 'Only plotting the first {} sessions in the summary panel.'.format(maxSessionNum) 
    ax5.axhline(y=0, color='k', linestyle='-')
    np.random.seed(7) #2
    for inda, (animal,leftData) in enumerate(zip(['d1pi014','d1pi015','d1pi016'],[left014,left015,left016])):
        #ax5.scatter(np.repeat(1+0.2*(ind-1),len(leftData)), 100*leftData, marker=SHAPESEACHANIMAL[animal], color=PHOTOSTIMCOLORS['laser_left'], edgecolors="black")
        #randOffset = 0.3*(np.random.rand(len(leftData))-0.5)
        #ax5.plot(1+randOffset, 100*leftData, 'o', mec=PHOTOSTIMCOLORS['laser_left'], mfc='None')
        # -- plot sessions segregated by animal -- #
        offset = np.repeat(inda*0.1, len(leftData))
        ax5.plot(0.9+offset, 100*leftData, 'o', mec=PHOTOSTIMCOLORS['laser_left'], mfc='None')
        # -- plot mean of each animal each hemi -- #
        ax5.plot(0.9+inda*0.1, np.mean(100*leftData), 'o', mfc=PHOTOSTIMCOLORS['laser_left'], mec='None')

    for inda, (animal,rightData) in enumerate(zip(['d1pi014','d1pi015','d1pi016'],[right014,right015,right016])):
        #ax5.scatter(np.repeat(2+0.2*(ind-1),len(rightData)), 100*rightData, marker=SHAPESEACHANIMAL[animal], color=PHOTOSTIMCOLORS['laser_right'], edgecolors="black")
        #randOffset = 0.3*(np.random.rand(len(leftData))-0.5)
        #ax5.plot(2+randOffset, 100*rightData, 'o', mec=PHOTOSTIMCOLORS['laser_right'], mfc='None')
        # -- plot sessions segregated by animal -- #
        offset = np.repeat(inda*0.1, len(leftData))
        ax5.plot(1.9+offset, 100*rightData, 'o', mec=PHOTOSTIMCOLORS['laser_right'], mfc='None')
        # -- plot mean of each animal each hemi -- #
        ax5.plot(1.9+inda*0.1, np.mean(100*rightData), 'o', mfc=PHOTOSTIMCOLORS['laser_right'], mec='None')

    # -- Stats for summary panel in figure grouping all animals together -- #
    leftStimChange = np.concatenate((left014,left015,left016))
    rightStimChange = np.concatenate((right014,right015,right016))
    meanLeftStim = np.mean(leftStimChange)
    meanRightStim = np.mean(rightStimChange)
    ax5.plot(0.25*np.array([-1,1])+1, 100*np.tile(meanLeftStim,2), lw=3, color=PHOTOSTIMCOLORS['laser_left'])
    ax5.plot(0.25*np.array([-1,1])+2, 100*np.tile(meanRightStim,2), lw=3, color=PHOTOSTIMCOLORS['laser_right'])

    '''
    # -- Add shapes as legend -- #
    lines=[]
    for ind,shape in enumerate(SHAPESEACHANIMAL):
        line = mlines.Line2D([], [], color='white', marker=shape, markerfacecolor='white', markeredgecolor='black')
        lines.append(line)
    plt.legend(lines, ('Mouse1','Mouse2','Mouse3'), numpoints=1, markerscale=0.7, loc='upper right', labelspacing=0.1, fontsize=fontSizeTicks, frameon=False)
    '''

    xlim = [0.5, 2.5]
    ylim = [-50, 50]
    plt.xlim(xlim)
    plt.ylim(ylim)
    xticks = [1,2]
    xticklabels = ['Left\nstim', 'Right\nstim']
    plt.xticks(xticks, xticklabels, fontsize=fontSizeTicks)
    labelDis = 0.1
    #plt.xlabel('Photostimulation', fontsize=fontSizeLabels) # labelpad=labelDis
    plt.ylabel('Rightward bias (%)\n stim - control', fontsize=fontSizeLabels) # labelpad=labelDis
    
    extraplots.boxoff(ax5)
    ax5.spines['bottom'].set_visible(False)
    [t.set_visible(False) for t in ax5.get_xticklines()]

    extraplots.significance_stars([1,2], 52, 3, starSize=10, gapFactor=0.12, color='0.5')
    
    #(T, leftpVal) = stats.wilcoxon(leftStimChange)
    #(T, rightpVal) = stats.wilcoxon(rightStimChange)
    #print 'p value for change in percent rightward in left hemi photostim is: ', leftpVal,  '\np value for change in percent rightward in left hemi photostim is: ', rightpVal

    # -- Grouped left and right hemi data separately for all three mice, compare bias resulting from left vs right hemi stim -- #
    (Z, pVal) = stats.ranksums(leftStimChange, rightStimChange)
    print 'Using 10 sessions for each animal in each hemi, the overall p value for the difference of the changes of percent rightward choice from left vs. right hemi photostim is: ', pVal, ' (ranksums test)'

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

