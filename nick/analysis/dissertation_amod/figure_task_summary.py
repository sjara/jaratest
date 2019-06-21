
import numpy as np
import pypsignifit
from jaratoolbox import extrastats
from jaratoolbox import extraplots
from matplotlib import pyplot as plt
# from jaratest.nick import behavioranalysis_vnick as behavioranalysis
from jaratest.nick.behavior import behavioranalysis_vnick as behavioranalysis

labelFontSize = 5

#############################################
# These are the days for amod002 and amod003#
# animal = 'amod003'
animal = 'amod002'

# salFilename = 'psychometric_{}_{}_saline.npz'.format(subject, stype)
dataDir = '/home/nick/data/dissertation_amod'


plt.figure()
dataToPlot = salData
curveColors = ['b', 'g']
plotHandles = []

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

soundtypes = ['chords', 'amp_mod']

# ax1 = plt.subplot(2, 2, indSt+3)
fig, axes = plt.subplots(nrows=2, ncols=2)
for ax in axes[0, :]:
    ax.axis('off')
#The axes to plot on
plotAxes = axes[1, :]

labelPosX = [0.02, 0.48]
labelPosY = [0.85, 0.47]

plt.text(x=labelPosX[0], y=labelPosY[0],
         s='A', fontsize=20, transform=fig.transFigure)

plt.text(x=labelPosX[1], y=labelPosY[0],
         s='B', fontsize=20, transform=fig.transFigure)

plt.text(x=labelPosX[2], y=labelPosY[0],
         s='C', fontsize=20, transform=fig.transFigure)

plt.text(x=labelPosX[0], y=labelPosY[1],
         s='D', fontsize=20, transform=fig.transFigure)

plt.text(x=labelPosX[2], y=labelPosY[1],
         s='E', fontsize=20, transform=fig.transFigure)


plt.subplots_adjust(hspace=0.5)

for indSt, stype in enumerate(soundtypes):

    dataFn ='task_psychometric_{}_{}_saline.npz'.format(animal, stype)
    fullPath = os.path.join(dataDir,dataFn)
    stData = np.load(fullPath)

    ax1 = plotAxes[indSt]

    color = curveColors[indSt]

    logPossibleValues = stData['logPossibleValues']
    estimate = stData['estimate']
    ciHitsEachValue = stData['ciHitsEachValue']
    fractionHitsEachValue = stData['fractionHitsEachValue']
    possibleValues = stData['possibleValues']

    xRange = logPossibleValues[-1]-logPossibleValues[1]

    fitxvals = np.linspace(logPossibleValues[0]-0.1*xRange,logPossibleValues[-1]+0.1*xRange,40)
    fityvals = extrastats.psychfun(fitxvals, *estimate)

    upperWhisker = ciHitsEachValue[1,:]-fractionHitsEachValue
    lowerWhisker = fractionHitsEachValue-ciHitsEachValue[0,:]

    # ax1.hold(True)
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

    # ax1.annotate('B', xy=(labelPosX[0],labelPosY[0]), xycoords='axes fraction',
    #                 fontsize=fontSizePanel, fontweight='bold')

    extraplots.boxoff(ax1)

    xticks = ax1.get_xticks()
    newXtickLabels = np.logspace(logPossibleValues[0], logPossibleValues[-1], 3, base=2)
    # 1/0
    ax1.set_xticks(np.log2(np.array(newXtickLabels)))
    if not stype=='amp_mod':
        ax1.set_xticklabels(['{:.3}'.format(x/1000.0) for x in newXtickLabels])
        ax1.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)
        ax1.set_title(stype.capitalize())
    else:
        ax1.set_xticklabels(['{:.3}'.format(x) for x in newXtickLabels])
        ax1.set_xlabel('AM Rate (Hz)', fontsize=fontSizeLabels)
        ax1.set_title("AM")

    # ax1.set_xlim([fitxvals[0],fitxvals[-1]])

    ax1.set_ylim([0, 100])
    ax1.set_ylabel('Rightward trials (%)', fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    ax1.set_yticks([0, 50, 100])

leg = ax1.legend([plotHandles[1],plotHandles[0]], ['Saline','Muscimol'], loc='upper left', frameon=False,
                    labelspacing=0.1, handlelength=1.5, handletextpad=0.2, borderaxespad=0.1, fontsize=12)

# plt.show()
plt.savefig('/home/nick/data/dissertation_amod/plots_task_summary.svg')
