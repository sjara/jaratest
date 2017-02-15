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

fontSizeLabels = 12
fontSizeTicks = 10

panelsToPlot=[0, 1]

gs = gridspec.GridSpec(5, 1)
# gs.update(left=0.15, right=0.95, bottom=0.15, wspace=0.5, hspace=0.5)

summaryFilename = 'muscimol_reaction_time_summary.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
fcFile = np.load(summaryFullPath)

subjects = fcFile['subjects']
conditions = fcFile['conditions']

for indsubject, subject in enumerate(subjects):

    ax = plt.subplot(gs[indsubject, 0])

    ax.hist(fcFile['{}allsaline'.format(subject)], bins=100, histtype='step', color='k')
    ax.hist(fcFile['{}allmuscimol'.format(subject)], bins=100, histtype='step', color='r')
    ax.set_xlim([0, 0.5])
    extraplots.boxoff(ax)

plt.show()
