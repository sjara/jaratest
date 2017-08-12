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
figSize = [4,10]

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

#panelsToPlot=[0, 1]

gs = gridspec.GridSpec(3, 1)
gs.update(left=0.2, right=0.75, bottom=0.05, top=0.95,  wspace=0.2, hspace=0.4)

# -- Panel A: number of valid trials -- #
# ax1 = plt.subplot(gs[0, 0])
ax2 = plt.subplot(gs[0, 0])
# ax2 = plt.subplot(111)

numTrialsFilename = 'muscimol_num_trials_summary.npz'
numTrialsFullPath = os.path.join(dataDir,numTrialsFilename)
numTrialsFile = np.load(numTrialsFullPath)

totalMat = numTrialsFile['totalMat']
validMat = numTrialsFile['validMat']
subjects = numTrialsFile['subjects']
conditions = numTrialsFile['conditions']

#dataMat(subject, session, condition)
ind = np.arange(len(subjects))
width = 0.35

muscimolColor = figparams.colp['muscimol']
condColors = ['k', muscimolColor]

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

    rects1 = ax.bar(ind, dataMat[:, :, 0].mean(1)-0.5, width, bottom=0.5, edgecolor='k', facecolor='w', lw=2, label='Saline')
    rects2 = ax.bar(ind+width+0.015, dataMat[:, :, 1].mean(1)-0.5, width, bottom=0.5, edgecolor=muscimolColor, lw=2, facecolor='w', label='Muscimol')

    ax.set_xticks(ind + width)
    ax.set_xticklabels(np.arange(6)+1, fontsize=fontSizeLabels)
    ax.set_xlabel('Mouse', fontsize=fontSizeLabels)
    ax.axhline(y=0.5, color='0.5', linestyle='-')
    # ax.set_ylim([0.45, 1])
    ax.set_xlim([ind[0]-0.5*width, ind[-1]+2.5*width ])
    ax.set_ylabel('Number of trials', fontsize=fontSizeLabels)
    # ax.set_yticks([0.5, 1])

    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    extraplots.boxoff(ax)

    ax.legend(bbox_to_anchor=(0.95, 0.6),
            loc=3,
            numpoints=1,
            fontsize=fontSizeLabels,
            ncol=1,
            columnspacing=1.5,
            frameon=False)

    for i in [1, 3, 4]:
        extraplots.significance_stars([i+0.5*width,i+1.5*width], 1000, 50, starSize=6, gapFactor=0.4, color='0.5')

# plot_bars(ax1, totalMat, 'total')
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


# -- Panel B: reaction times -- #
ax3 = plt.subplot(gs[1, 0])
centerToSideFilename = 'muscimol_reaction_time_summary.npz'
centerToSideFullPath = os.path.join(dataDir,centerToSideFilename)
centerToSideFile = np.load(centerToSideFullPath)

subjects = centerToSideFile['subjects']
conditions = centerToSideFile['conditions']

for inds, subject in enumerate(subjects):
    centersThisSubject = inds+np.array([-0.25,0.25])
    for indc, condition in enumerate(conditions):
        thisSubjectThisCondValid = centerToSideFile['{}validmean{}'.format(subject,condition)]
        #thisSubjectThisCondAll = centerToSideFile['{}all{}']
        #randOffset = 0.3*(np.random.rand(len(thisSubjectThisCondValid))-0.5)
        plt.hold('True')
        ax3.plot(np.tile(centersThisSubject[indc], 4), 1000*thisSubjectThisCondValid, 'o', mec=condColors[indc], mfc='None')
        meanThisSubjectThisCond = np.mean(thisSubjectThisCondValid)
        ax3.plot(0.3*np.array([-1,1])+centersThisSubject[indc], 1000*np.tile(meanThisSubjectThisCond,2), lw=2.5, color=condColors[indc])

plt.ylim([250,730])
xticks = range(5)
xticklabels = range(1,6)
plt.xticks(xticks, xticklabels, fontsize=fontSizeTicks)
plt.ylabel('Time from center port to side port (ms)')
plt.xlabel('Mouse')
extraplots.boxoff(ax3)
for sigSubjectInd in [0,2,3,4]:
    extraplots.significance_stars(sigSubjectInd+np.array([-0.25,0.25]), 710, 25, starSize=6, gapFactor=0.4, color='0.5')



# -- Panel C: response times -- #
ax4 = plt.subplot(gs[2, 0])
soundToCoutFilename = 'muscimol_response_time_summary.npz'
soundToCoutFullPath = os.path.join(dataDir,soundToCoutFilename)
soundToCoutFile = np.load(soundToCoutFullPath)

subjects = soundToCoutFile['subjects']
conditions = soundToCoutFile['conditions']

for inds, subject in enumerate(subjects):
    centersThisSubject = inds+np.array([-0.25,0.25])
    for indc, condition in enumerate(conditions):
        thisSubjectThisCondValid = soundToCoutFile['{}validmean{}'.format(subject,condition)]
        #thisSubjectThisCondAll = soundToCoutFile['{}all{}']
        #randOffset = 0.3*(np.random.rand(len(thisSubjectThisCondValid))-0.5)
        plt.hold('True')
        ax4.plot(np.tile(centersThisSubject[indc], 4), 1000*thisSubjectThisCondValid, 'o', mec=condColors[indc], mfc='None')
        meanThisSubjectThisCond = np.mean(thisSubjectThisCondValid)
        ax4.plot(0.3*np.array([-1,1])+centersThisSubject[indc], 1000*np.tile(meanThisSubjectThisCond,2), lw=2.5, color=condColors[indc])

plt.ylim([100,250])
xticks = range(5)
xticklabels = range(1,6)
plt.xticks(xticks, xticklabels, fontsize=fontSizeTicks)
plt.ylabel('Time from sound to center port exit (ms)')
plt.xlabel('Mouse')
extraplots.boxoff(ax4)
for sigSubjectInd in [0,1,2,3,4]:
    extraplots.significance_stars(sigSubjectInd+np.array([-0.25,0.25]), 250, 10, starSize=6, gapFactor=0.4, color='0.5')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
