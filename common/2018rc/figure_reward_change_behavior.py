import os
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
reload(settings)
from jaratoolbox import extraplots
from jaratoolbox import extrastats
import figparams
from scipy import stats
reload(figparams)


FIGNAME = 'reward_change_behavior'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_reward_change_behavior' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
#figSize = [7, 5]
figSize = [7, 5]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.015, 0.45]   # Horiz position for panel labels
labelPosY = [0.95, 0.5]    # Vert position for panel labels

colorsDict = {'more_left':figparams.colp['MoreRewardL'], 
              'more_right':figparams.colp['MoreRewardR'],
              'same_reward': 'gray'} 

'''
animalNumbers = {'adap021':'Mouse 1',
                 'adap023':'Mouse 2',
                 'adap028':'Mouse 3',
                 'adap029':'Mouse 4',
                 'adap035':'Mouse 5'}
'''

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

panelsToPlot=[0, 1]

gs = gridspec.GridSpec(2, 6)
gs.update(left=0.08, right=0.98, top=0.95, bottom=0.05, wspace=0.3, hspace=0.4)
ax0 = plt.subplot(gs[0, 0:3])
ax1 = plt.subplot(gs[0, 3:])
ax2 = plt.subplot(gs[1, 0:2])
ax2.hold(True)
ax3 = plt.subplot(gs[1, 2:4])
ax3.hold(True)
ax4 = plt.subplot(gs[1, 4:6])
ax4.hold(True)

# -- Panel A: task schematic -- #
ax0.set_axis_off()
ax0.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                fontsize=fontSizePanel, fontweight='bold')

# -- Panel B: Example rc psychometric -- # 
if 0 in panelsToPlot:
    ax1.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                 fontsize=fontSizePanel, fontweight='bold')

    exampleFilename = 'example_rc_ave_pycurve_gosi008.npz' #'example_rc_ave_pycurve_adap012.npz' #'example_rc_ave_pycurve_adap071.npz'
    exampleFullPath = os.path.join(dataDir,exampleFilename)
    exampleData = np.load(exampleFullPath)

    possibleValues = exampleData['possibleFreqs']
    plotHandles = []
    blockTypes = exampleData['blockLabels']
    for indB,blockType in enumerate(blockTypes):
        color = colorsDict[blockType]
        fractionHitsEachValue = exampleData['fractionHitsEachBlockEachFreq'][indB,:]
        ciHitsEachValue = exampleData['ciHitsEachBlockEachFreq'][indB,:,:]
        upperWhisker = ciHitsEachValue[1,:]-fractionHitsEachValue
        lowerWhisker = fractionHitsEachValue-ciHitsEachValue[0,:]
        fitxvals = exampleData['fitxval'][indB,:]
        fityvals = exampleData['fityval'][indB,:]
        logPossibleValues = exampleData['logPossibleFreqs']

        ax1.hold(True)
        (pline, pcaps, pbars) = ax1.errorbar(logPossibleValues,
                                             100*fractionHitsEachValue,
                                             yerr = [100*lowerWhisker, 100*upperWhisker],
                                             ecolor=color, fmt=None, clip_on=False)

        pdots = ax1.plot(logPossibleValues, 100*fractionHitsEachValue, 'o', ms=6, mec='None', mfc=color,
                         clip_on=False)

        pfit, = ax1.plot(fitxvals, 100*fityvals, color=color, lw=2, clip_on=False)
        plotHandles.append(pfit)
    
    extraplots.boxoff(ax1)

    xTicks = np.array([6,11,19])
    ax1.set_xticks(np.log2(xTicks*1000))
    freqLabels = ['{:d}'.format(x) for x in xTicks]
    ax1.set_xticklabels(freqLabels)
    ax1.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)
    ax1.set_xlim([fitxvals[0],fitxvals[-1]])
    
    ax1.set_ylim([0, 100])
    ax1.set_ylabel('Rightward trials (%)', fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(ax1,fontSizeTicks)
    ax1.set_yticks([0, 50, 100])

    leg = ax1.legend(plotHandles, ['Same reward','Left more','Right more'], loc='upper left', frameon=False,
                     labelspacing=0.1, handlelength=1.5, handletextpad=0.2, borderaxespad=0.1, fontsize=12)
    

# #Panel: Summary bar plots for each animal
if 1 in panelsToPlot:
    '''
    summaryFilename = 'rc_rightward_choice_each_condition_summary.npz'
    summaryFullPath = os.path.join(dataDir,summaryFilename)
    summaryFile = np.load(summaryFullPath)

    dataMat = summaryFile['resultAllAnimals']
    subjects = summaryFile['animalsUsed']
    conditions = summaryFile['blockLabels']

    ind = np.arange(len(subjects))
    width = 0.3
    condColors = [colorsDict['more_left'], colorsDict['more_right']]

    #shiftAmt = width*0.05
    shiftAmt = 0

    #FIXME: Hardcoded number of points per animal here
    #pointShift = np.array([-shiftAmt, shiftAmt, -shiftAmt, shiftAmt])

    for indSubject, subject in enumerate(subjects):
        for indCond, condition in enumerate(conditions):
            sessionsThisCondThisSubject = dataMat[indCond, :, indSubject]
            ax2.plot(np.zeros(len(sessionsThisCondThisSubject)) + (indSubject + 0.5*width + indCond*width),
                     sessionsThisCondThisSubject, marker='o', linestyle='none', mec=condColors[indCond], mfc='none',
                     clip_on=False)
            ax2.hold(1)

    rects1 = ax2.bar(ind, dataMat[0, :, :].mean(axis=0), width, edgecolor=colorsDict['more_left'], facecolor='w', lw=1.5)
    rects2 = ax2.bar(ind+width, dataMat[1, :, :].mean(axis=0), width, edgecolor=colorsDict['more_right'], facecolor='w', lw=1.5)
    for i in [0,2,5,7,8,9]: #these mice were significant
        extraplots.significance_stars([i+0.5*width,i+1.5*width], 75, 1, starSize=6, gapFactor=0.4, color='0.5')
    
    ax2.set_xticks(ind + width)
    ax2.set_xticklabels(ind+1, fontsize=fontSizeLabels)
    ax2.set_xlabel('Mouse', fontsize=fontSizeLabels)
    #ax2.axhline(y=50, color='grey', linestyle='--')
    ax2.set_ylim([0, 80])
    ax2.set_xlim([ind[0]-0.75*width, ind[-1]+2.5*width ])
    ax2.set_ylabel('Rightward trials (%)', fontsize=fontSizeLabels)
    ax2.set_yticks([25, 50, 75])

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    extraplots.boxoff(ax2)
    
    #ax2.axes.get_xaxis().set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    [t.set_visible(False) for t in ax2.get_xticklines()]
    '''
    summaryFilename = 'rc_fitted_rightward_choice_each_condition_by_freq_summary.npz'
    #'rc_rightward_choice_each_condition_by_freq_summary.npz'
    summaryFullPath = os.path.join(dataDir,summaryFilename)
    summaryFile = np.load(summaryFullPath)

    dataMat = summaryFile['resultAllAnimals']
    subjects = summaryFile['animalsUsed']
    conditions = summaryFile['blockLabels']
    firstCondToPlot = 1
    numFreqs = dataMat.shape[1]

    freqToPlot = 0 #lowest freq
    rChoiceEachConcThisFreqEachAnimal = dataMat[firstCondToPlot:, freqToPlot, :]
    for animalInd in range(len(subjects)):
        ax2.plot(rChoiceEachConcThisFreqEachAnimal[:, animalInd], marker='o', color='k')
    ax2.set_xticks([0,1])
    ax2.set_xticklabels([])
    ax2.set_ylabel('Rightward trials (%)', fontsize=fontSizeLabels)
    ax2.set_yticks([0, 25]) 
    ax2.set_xlim([-0.5, 1.5])
    ax2.set_xticklabels(['Left more', 'Right more'], fontsize=fontSizeLabels) #conditions[firstCondToPlot:]
    ax2.set_ylim([-5, 30])
    #ax2.text(0, 30,'Lowest frequency')
    ax2.set_title('Lowest frequency', fontsize=fontSizeLabels)
    plt.sca(ax2)
    extraplots.significance_stars([0,1], 26, 2, starSize=8, gapFactor=0.4, color='0.5')
    extraplots.set_ticks_fontsize(ax2,fontSizeTicks)
    extraplots.boxoff(ax2) 

    freqToPlot = numFreqs / 2 # middle freq
    rChoiceEachConcThisFreqEachAnimal = dataMat[firstCondToPlot:, freqToPlot, :]
    for animalInd in range(len(subjects)):
        ax3.plot(rChoiceEachConcThisFreqEachAnimal[:, animalInd], marker='o', color='k')
    ax3.set_xticks([0,1])
    ax3.set_xticklabels(['Left more', 'Right more'], fontsize=fontSizeLabels)
    #ax3.set_ylabel('Rightward trials (%)', fontsize=fontSizeLabels)
    ax3.set_yticks([25, 50, 75, 100])
    ax3.set_ylim([0, 118]) 
    ax3.set_xlim([-0.5, 1.5])
    #ax3.text(0.1, 118, 'Middle frequency')
    ax3.set_title('Middle frequency', fontsize=fontSizeLabels)
    plt.sca(ax3)
    extraplots.significance_stars([0,1], 108, 5, starSize=8, gapFactor=0.4, color='0.5')
    extraplots.set_ticks_fontsize(ax3,fontSizeTicks)
    extraplots.boxoff(ax3) 

    freqToPlot = -1 # highest freq
    rChoiceEachConcThisFreqEachAnimal = dataMat[firstCondToPlot:, freqToPlot, :]
    for animalInd in range(len(subjects)):
        ax4.plot(rChoiceEachConcThisFreqEachAnimal[:, animalInd], marker='o', color='k')
    ax4.set_xticks([0,1])
    ax4.set_xticklabels(['Left more', 'Right more'], fontsize=fontSizeLabels)
    #ax4.set_ylabel('Rightward trials (%)', fontsize=fontSizeLabels)
    ax4.set_yticks([75, 100])
    ax4.set_ylim([70, 106]) 
    ax4.set_xlim([-0.5, 1.5])
    #ax4.text(0.1, 106, 'Highest frequency')
    ax4.set_title('Highest frequency', fontsize=fontSizeLabels)
    plt.sca(ax4)
    extraplots.significance_stars([0,1], 103, 2, starSize=8, gapFactor=0.4, color='0.5')
    extraplots.set_ticks_fontsize(ax4,fontSizeTicks)
    extraplots.boxoff(ax4) 

ax2.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)


##STATS
for freqToPlot in [0, numFreqs / 2, -1]:
    rChoiceEachConcThisFreqEachAnimal = dataMat[firstCondToPlot:, freqToPlot, :]
    zScore, pVal = stats.ranksums(rChoiceEachConcThisFreqEachAnimal[0,:], rChoiceEachConcThisFreqEachAnimal[1,:])
    print('Using Wilcoxon ranksum test on percent right choice for more_left vs. more_right\n For freq {} the p value is {}'
        .format(freqToPlot, pVal))
rChoiceSameRwExtremeFreqEachAnimal = np.concatenate((100-dataMat[0,0,:],dataMat[0,-1,:]))
rChoiceSameRwExtremeFreqEachAnimal = rChoiceSameRwExtremeFreqEachAnimal[~np.isnan(rChoiceSameRwExtremeFreqEachAnimal)]
print('The accuracy of discrimination at the two extreme frequencies is {} +/- {}%'
    .format(np.mean(rChoiceSameRwExtremeFreqEachAnimal), np.std(rChoiceSameRwExtremeFreqEachAnimal)))

plt.show()
'''
for indSubject in range(len(subjects)):
    subDataMoreLeft = dataMat[0, :, indSubject]
    subDataMoreRight = dataMat[1, :, indSubject]

    print '\nMouse {}'.format(indSubject)
    print 'More_left reward cond frac rightward: {}'.format(np.mean(subDataMoreLeft))
    print 'More_right reward cond frac rightward: {}'.format(np.mean(subDataMoreRight))
    Z, pVal = stats.ranksums(subDataMoreLeft, subDataMoreRight)

    print "\n\nWilcoxon rank-sum test of fraction right choice for mouse {}, p={:.3f}".format(indSubject, pVal)
'''