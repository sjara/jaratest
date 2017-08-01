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

STUDY_NAME = '2016astr'
FIGNAME = 'photostim_2afc'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1] # Which panels to plot

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_photostim_2afc_control' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,5]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1
labelPosX = [0.02, 0.54]   # Horiz position for panel labels
labelPosY = [0.95, 0.95]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 2)
gs.update(left=0.12, right=0.9, top=0.95, bottom=0.1, wspace=0.2, hspace=0.15)


# -- Panel A: L vs R hemi stim bias in d1pi and wildtype controls -- #
ax1 = plt.subplot(gs[0, 0])
plt.axis('off')
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


# -- Panel B: relationship between distance off from center and contralateral bias -- #
ax2 = plt.subplot(gs[0,1])
extraplots.boxoff(ax2)
ax2.annotate('B', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

# -- Load data about behavior bias in photostim 2afc -- #
FIGNAME_behav = 'photostim_2afc'
dataDir_behav = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME_behav)

summaryFilename_behav = 'summary_photostim_percent_contra_choice_change.npz'
summaryFullPath_behav = os.path.join(dataDir_behav,summaryFilename_behav)
summary_behav = np.load(summaryFullPath_behav)

# These numbers are percent change in contralateral choice (stim - control) for each condition:
left014 = summary_behav['d1pi014leftHemiStim']
left015 = summary_behav['d1pi015leftHemiStim']
left016 = summary_behav['d1pi016leftHemiStim']
right014 = summary_behav['d1pi014rightHemiStim']
right015 = summary_behav['d1pi015rightHemiStim']
right016 = summary_behav['d1pi016rightHemiStim']

left014sessions = summary_behav['d1pi014leftHemiStimSessions']
left015sessions = summary_behav['d1pi015leftHemiStimSessions']
left016sessions = summary_behav['d1pi016leftHemiStimSessions']
right014sessions = summary_behav['d1pi014rightHemiStimSessions']
right015sessions = summary_behav['d1pi015rightHemiStimSessions']
right016sessions = summary_behav['d1pi016rightHemiStimSessions']


locationDict = {'0': {'d1pi014':left014,
                      'd1pi016':right016,
                      'd1pi015':left015,
                      'd1pi015':right015},
                '0.4': {'d1pi014':right014,
                        'd1pi016':left016}
                }
SHAPES = {'d1pi014':'s',
          'd1pi015':'o',
          'd1pi016':'^'}

np.random.seed(7)
for key, valueDict in locationDict.items():
    for animal, value in valueDict.items():
        randOffset = 0.1*(np.random.rand(len(value))-0.5)
        ax2.plot(float(key)+randOffset, 100*value, SHAPES[animal], mec='k', mfc='None')
ax2.set_xlim([-0.2, 0.6])
ax2.set_xticks([0, 0.4])
ax2.set_xticklabels(['center', 'border'])
ax2.set_ylabel('Contra lateral bias: stim - control (%)')
#plt.show()
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

