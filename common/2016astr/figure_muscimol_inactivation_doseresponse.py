import os
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
reload(settings)
from jaratoolbox import extraplots
from jaratoolbox import extrastats
from jaratoolbox import colorpalette
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

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

panelsToPlot=[0, 1]

gs = gridspec.GridSpec(1, 1)
gs.update(left=0.15, right=0.98, top=0.95, bottom=0.1, wspace=0.5, hspace=0.5)
ax0 = plt.subplot(gs[0, 0])

# # Panel: Example saline and muscimol psychometric
if 0 in panelsToPlot:

    lowMusFn = 'adap029_muscimol00625_psychometric.npz'
    midMusFn = 'adap029_muscimol0125_psychometric.npz'
    regMusFn = 'adap029_muscimol0250_psychometric.npz'

    lowMusFullPath = os.path.join(dataDir,lowMusFn)
    midMusFullPath = os.path.join(dataDir,midMusFn)
    regMusFullPath = os.path.join(dataDir,regMusFn)
    lowMusData = np.load(lowMusFullPath)
    midMusData = np.load(midMusFullPath)
    regMusData = np.load(regMusFullPath)

    salFilename = 'adap034_saline_psychometric.npz'
    salFullPath = os.path.join(dataDir,salFilename)
    salData = np.load(salFullPath)

    dataToPlot = [lowMusData, midMusData, regMusData, salData]
    #FIXME: I am here
    curveColors = [colorpalette.TangoPalette['Butter2'],
                   colorpalette.TangoPalette['Orange2'],
                   colorpalette.TangoPalette['ScarletRed1'], 'k']
    plotHandles = []

    for indCond, condData in enumerate(dataToPlot):

        plt.hold(1)
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

        (pline, pcaps, pbars) = ax0.errorbar(logPossibleValues,
                                             100*fractionHitsEachValue,
                                             yerr = [100*lowerWhisker, 100*upperWhisker],
                                             ecolor=color, fmt=None, clip_on=False)

        pdots = ax0.plot(logPossibleValues, 100*fractionHitsEachValue, 'o', ms=6, mec='None', mfc=color,
                         clip_on=False)

        #ax0.set_xticks(logPossibleValues)
        #freqLabels = ['{:.03}'.format(x) for x in possibleValues/1000.0]
        #ax0.set_xticklabels(freqLabels)
        #ax0.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)

        pfit, = ax0.plot(fitxvals, 100*fityvals, color=color, lw=2, clip_on=False)
        plotHandles.append(pfit)

    ax0.annotate('B', xy=(labelPosX[0],labelPosY[0]), xycoords='axes fraction',
                 fontsize=fontSizePanel, fontweight='bold')

    extraplots.boxoff(ax0)

    #xticks = ax0.get_xticks()
    #newXtickLabels = np.logspace(xticks[0], xticks[-1], 3, base=2)
    #ax0.set_xticks(np.log2(np.array(newXtickLabels)))
    #ax0.set_xticklabels(['{:.3}'.format(x/1000.0) for x in newXtickLabels])

    xTicks = np.array([6,11,19])
    ax0.set_xticks(np.log2(xTicks*1000))
    freqLabels = ['{:d}'.format(x) for x in xTicks]
    ax0.set_xticklabels(freqLabels)
    ax0.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)
    ax0.set_xlim([fitxvals[0],fitxvals[-1]])

    ax0.set_ylim([0, 100])
    ax0.set_ylabel('Rightward trials (%)', fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    ax0.set_yticks([0, 50, 100])

    leg = ax0.legend(plotHandles,
                     ['Muscimol, 0.0625 mg/ml', 'Muscimol, 0.125 mg/ml', 'Muscimol, 0.25 mg/ml', 'Saline'],
                     loc='upper left', frameon=False,
                     labelspacing=0.1, handlelength=1.5,
                     handletextpad=0.2, borderaxespad=0.1, fontsize=12)

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
