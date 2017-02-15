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

FIGNAME = 'muscimol_inactivation'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_{}'.format(FIGNAME) # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [8, 6]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [-0.35]   # Horiz position for panel labels
labelPosY = [1]    # Vert position for panel labels

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

animalNumbers = {'adap021':'Mouse 1',
                 'adap023':'Mouse 2',
                 'adap028':'Mouse 3',
                 'adap029':'Mouse 4',
                 'adap035':'Mouse 5'}

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

panelsToPlot=[0, 1]

gs = gridspec.GridSpec(2, 1)
gs.update(left=0.15, right=0.95, bottom=0.15, wspace=0.5, hspace=0.5)
ax1 = plt.subplot(gs[0, 0])
ax2 = plt.subplot(gs[1, 0])

summaryFilename = 'muscimol_num_trials_summary.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
fcFile = np.load(summaryFullPath)

totalMat = fcFile['totalMat']
validMat = fcFile['validMat']
subjects = fcFile['subjects']
conditions = fcFile['conditions']

#dataMat(subject, session, condition)
ind = np.arange(len(subjects))
width = 0.35
condColors = ['k', 'r']

shiftAmt = width*0.05
# shiftAmt = 0
fontSizeLabels = 12
fontSizeTicks = 10

#FIXME: Hardcoded number of points per animal here
pointShift = np.array([-shiftAmt, shiftAmt, -shiftAmt, shiftAmt])


def plot_bars(ax, dataMat, label):
    for indSubject, subject in enumerate(subjects):
        for indCond, condition in enumerate(conditions):
            sessionsThisCondThisSubject = dataMat[indSubject, :, indCond]
            ax.plot(np.zeros(len(sessionsThisCondThisSubject)) + (indSubject + 0.5*width + indCond*width) + pointShift,
                    sessionsThisCondThisSubject, marker='o', linestyle='none', mec=condColors[indCond], mfc='none')
            ax.hold(1)

    rects1 = ax.bar(ind, dataMat[:, :, 0].mean(1)-0.5, width, bottom=0.5, edgecolor='k', facecolor='w')
    rects2 = ax.bar(ind+width+0.015, dataMat[:, :, 1].mean(1)-0.5, width, bottom=0.5, edgecolor='r', facecolor='w')

    ax.set_xticks(ind + width)
    ax.set_xticklabels(np.arange(6)+1, fontsize=fontSizeLabels)
    ax.set_xlabel('Mouse', fontsize=fontSizeLabels)
    ax.axhline(y=0.5, color='0.5', linestyle='-')
    # ax.set_ylim([0.45, 1])
    ax.set_xlim([ind[0]-0.5*width, ind[-1]+2.5*width ])
    ax.set_ylabel('Number of {} trials'.format(label), fontsize=fontSizeLabels)
    # ax.set_yticks([0.5, 1])

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    extraplots.boxoff(ax)

plot_bars(ax1, totalMat, 'total')
plot_bars(ax2, validMat, 'valid')

# ax2.annotate('C', xy=(labelPosX[0],labelPosY[0]), xycoords='axes fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()

print "Total trials"
dataMat = totalMat
for indSubject in range(5):
    subDataSal = dataMat[indSubject, :, 0]
    subDataMus = dataMat[indSubject, :, 1]

    print indSubject
    print stats.ranksums(subDataSal, subDataMus)

print "Valid trials"
dataMat = validMat
for indSubject in range(5):
    subDataSal = dataMat[indSubject, :, 0]
    subDataMus = dataMat[indSubject, :, 1]

    print indSubject
    print stats.ranksums(subDataSal, subDataMus)
