import os
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
reload(settings)
from jaratoolbox import extraplots
from jaratoolbox import extrastats
import figparams
reload(figparams)



FIGNAME = 'muscimol_inactivation'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_muscimol_inactivation' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7, 5]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [-0.35]   # Horiz position for panel labels
labelPosY = [1]    # Vert position for panel labels

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

muscimolColor = figparams.colp['muscimol']

animalNumbers = {'adap021':'Mouse 1',
                 'adap023':'Mouse 2',
                 'adap028':'Mouse 3',
                 'adap029':'Mouse 4',
                 'adap035':'Mouse 5'}

animalShapes = {'adap021':'D',
                'adap028':'>',
                'adap029':'<',
                'adap023':'s',
                'adap035':'o'}

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

panelsToPlot=[0, 1]

gs = gridspec.GridSpec(2, 2)
gs.update(left=0.15, right=0.98, top=0.95, bottom=0.1, wspace=0.5, hspace=0.5)
ax0 = plt.subplot(gs[:, 0])
ax1 = plt.subplot(gs[0, 1])
ax2 = plt.subplot(gs[1, 1])

## Panel: Space for the brain slice diagram, with legend
outsideCoords = [-1,-1]
ax0.set_axis_off()

ax0.hold(True)
ax0.plot(outsideCoords, 'kD', label=animalNumbers['adap021'])
ax0.plot(outsideCoords, 'ks', label=animalNumbers['adap023'])
ax0.plot(outsideCoords, 'k>', label=animalNumbers['adap028'])
ax0.plot(outsideCoords, 'k<', label=animalNumbers['adap029'])
ax0.plot(outsideCoords, 'ko', label=animalNumbers['adap035'])

ax0.set_ylim([0, 1])
ax0.set_xlim([0, 1])

ax0.legend(bbox_to_anchor=(-0.35, 0),
           loc=3,
           numpoints=1,
           fontsize=fontSizeTicks,
           ncol=3,
           handlelength=0.05,
           columnspacing=1.5,
           frameon=False)

ax0.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='axes fraction',
                fontsize=fontSizePanel, fontweight='bold')

# # Panel: Example saline and muscimol psychometric 
if 0 in panelsToPlot:
    # ax1 = plt.subplot(111)

    musFilename = 'adap029_muscimol_psychometric.npz'
    musFullPath = os.path.join(dataDir,musFilename)
    musData = np.load(musFullPath)

    salFilename = 'adap029_saline_psychometric.npz'
    salFullPath = os.path.join(dataDir,salFilename)
    salData = np.load(salFullPath)

    dataToPlot = [musData, salData]
    curveColors = [muscimolColor, 'k']
    plotHandles = []
    
    for indCond, condData in enumerate(dataToPlot):

        color = curveColors[indCond]

        logPossibleValues = condData['logPossibleValues']
        estimate = condData['estimate']
        ciHitsEachValue = condData['ciHitsEachValue']
        fractionHitsEachValue = condData['fractionHitsEachValue']
        possibleValues = condData['possibleValues']

        xRange = logPossibleValues[-1]-logPossibleValues[1]

        fitxvals = np.linspace(logPossibleValues[0]-0.1*xRange,logPossibleValues[-1]+0.1*xRange,40)
        fityvals = extrastats.psychfun(fitxvals, *estimate)

        upperWhisker = ciHitsEachValue[1,:]-fractionHitsEachValue
        lowerWhisker = fractionHitsEachValue-ciHitsEachValue[0,:]

        ax1.hold(True)
        (pline, pcaps, pbars) = ax1.errorbar(logPossibleValues,
                                             100*fractionHitsEachValue,
                                             yerr = [100*lowerWhisker, 100*upperWhisker],
                                             ecolor=color, fmt=None, clip_on=False)

        pdots = ax1.plot(logPossibleValues, 100*fractionHitsEachValue, 'o', ms=6, mec='None', mfc=color,
                         clip_on=False)

        #ax1.set_xticks(logPossibleValues)
        #freqLabels = ['{:.03}'.format(x) for x in possibleValues/1000.0]
        #ax1.set_xticklabels(freqLabels)
        #ax1.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)

        pfit, = ax1.plot(fitxvals, 100*fityvals, color=color, lw=2, clip_on=False)
        plotHandles.append(pfit)

    ax1.annotate('B', xy=(labelPosX[0],labelPosY[0]), xycoords='axes fraction',
                 fontsize=fontSizePanel, fontweight='bold')

    extraplots.boxoff(ax1)

    #xticks = ax1.get_xticks()
    #newXtickLabels = np.logspace(xticks[0], xticks[-1], 3, base=2)
    #ax1.set_xticks(np.log2(np.array(newXtickLabels)))
    #ax1.set_xticklabels(['{:.3}'.format(x/1000.0) for x in newXtickLabels])

    xTicks = np.array([6,11,19])
    ax1.set_xticks(np.log2(xTicks*1000))
    freqLabels = ['{:d}'.format(x) for x in xTicks]
    ax1.set_xticklabels(freqLabels)
    ax1.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)
    ax1.set_xlim([fitxvals[0],fitxvals[-1]])
    
    ax1.set_ylim([0, 100])
    ax1.set_ylabel('Rightward trials (%)', fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    ax1.set_yticks([0, 50, 100])

    leg = ax1.legend([plotHandles[1],plotHandles[0]], ['Saline','Muscimol'], loc='upper left', frameon=False,
                     labelspacing=0.1, handlelength=1.5, handletextpad=0.2, borderaxespad=0.1, fontsize=12)
    

# #Panel: Summary bar plots for each animal
if 1 in panelsToPlot:
    # ax2 = plt.subplot(111)

    summaryFilename = 'muscimol_frac_correct_summary.npz'
    summaryFullPath = os.path.join(dataDir,summaryFilename)
    fcFile = np.load(summaryFullPath)

    dataMat = fcFile['data']
    subjects = fcFile['subjects']
    conditions = fcFile['conditions']

    #dataMat(subject, session, condition)
    ind = np.arange(len(subjects))
    width = 0.35
    condColors = ['k', muscimolColor]

    #shiftAmt = width*0.05
    shiftAmt = 0

    #FIXME: Hardcoded number of points per animal here
    pointShift = np.array([-shiftAmt, shiftAmt, -shiftAmt, shiftAmt])

    for indSubject, subject in enumerate(subjects):
        for indCond, condition in enumerate(conditions):
            sessionsThisCondThisSubject = dataMat[indSubject, :, indCond]
            ax2.plot(np.zeros(len(sessionsThisCondThisSubject)) + (indSubject + 0.5*width + indCond*width) + pointShift,
                     100*sessionsThisCondThisSubject, marker='o', linestyle='none', mec=condColors[indCond], mfc='none',
                     clip_on=False)
            ax2.hold(1)

    rects1 = ax2.bar(ind, 100*(dataMat[:, :, 0].mean(1)-0.5), width, bottom=50, edgecolor='k', facecolor='w', lw=2)
    rects2 = ax2.bar(ind+width, 100*(dataMat[:, :, 1].mean(1)-0.5), width, bottom=50, edgecolor=muscimolColor, facecolor='w', lw=2)
    for i in ind:
        extraplots.significance_stars([i+0.5*width,i+1.5*width], 95, 1, starSize=6, gapFactor=0.4, color='0.5')
    
    ax2.set_xticks(ind + width)
    ax2.set_xticklabels(np.arange(6)+1, fontsize=fontSizeLabels)
    ax2.set_xlabel('Mouse', fontsize=fontSizeLabels)
    ax2.axhline(y=50, color='k', linestyle='-')
    ax2.set_ylim([48, 100])
    ax2.set_xlim([ind[0]-0.75*width, ind[-1]+2.5*width ])
    ax2.set_ylabel('Correct trials (%)', fontsize=fontSizeLabels)
    ax2.set_yticks([50, 75, 100])

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    extraplots.boxoff(ax2)
    ax2.annotate('C', xy=(labelPosX[0],labelPosY[0]), xycoords='axes fraction', fontsize=fontSizePanel, fontweight='bold')

    #ax2.axes.get_xaxis().set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    [t.set_visible(False) for t in ax2.get_xticklines()]

    
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

import numpy as np
from scipy import stats

##SATS
dataFn = os.path.join(dataDir, 'muscimol_frac_correct_summary.npz')

dataObj = np.load(dataFn)

data = dataObj['data']
subjects = dataObj['subjects']
conditions = dataObj['conditions']

#data(subject, session, condition)

print "\n\nWilcoxon rank-sum test of fraction correct for 4 saline sessions versus 4 muscimol sessions, each mouse."

for indSubject in range(5):
    subDataSal = data[indSubject, :, 0]
    subDataMus = data[indSubject, :, 1]

    print '\nMouse {}'.format(indSubject)
    print 'Saline frac correct: {}'.format(subDataSal)
    print 'Muscimol frac correct: {}'.format(subDataMus)
    print stats.ranksums(subDataSal, subDataMus)

