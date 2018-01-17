import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import histologyanalysis as ha
import figparams
reload(figparams)

FIGNAME = 'figure_anatomy'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

subject = 'anat036'

PANELS = [1, 1, 1, 1, 1, 1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_anatomy' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,5] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

barColor = '0.5'

labelPosX = [0.05, 0.35, 0.65]   # Horiz position for panel labels
labelPosY = [0.95, 0.45]    # Vert position for panel labels

# Define colors, use figparams
laserColor = figparams.colp['blueLaser']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 3)
gs.update(left=0.15, right=0.95, top=0.90, bottom=0.1, wspace=.1, hspace=0.5)


annotationVolume = ha.AllenAnnotation()

# -- Panel: Injection method --
axP = plt.subplot(gs[0, 0])
axP.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axP.axis('off')
if PANELS[0]:
    # Plot stuff
    pass


# -- Panel: Cortex detail image--
axP = plt.subplot(gs[0, 1])
axP.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axP.axis('off')
if PANELS[1]:
    # Plot stuff
    pass


# -- Panel: Cortex cell depth histogram --
acDataPath = os.path.join(dataDir, 'cortexCellDepths.npy')
allSliceDepths = np.load(acDataPath)

axP = plt.subplot(gs[0, 2])
axP.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
# axP.set_xlabel('Cell density')
# axP.set_ylabel('Depth (um)')
if PANELS[2]:
    axP.hist(allSliceDepths+0.1, bins=25, color=barColor)
    axP.set_xlim([0, 1])
    axP.set_xticks([0, 0.5, 1])
    plt.ylabel('Number of cells')
    plt.xlabel('Normalized distance from pia')
    plt.show()
    extraplots.boxoff(axP)
    pass


# -- Panel: Overview section with detail boxes --
axP = plt.subplot(gs[1, 0])
axP.annotate('D', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axP.axis('off')
if PANELS[3]:
    # Plot stuff
    pass


# -- Panel: Thalamus detail image --
axP = plt.subplot(gs[1, 1])
axP.annotate('E', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axP.axis('off')
if PANELS[4]:
    # Plot stuff
    pass


# -- Panel: Thalamus cell location histogram --

thalDataPath = os.path.join(dataDir, 'thalamusAreaCounts.npz')
sliceCountSum = np.load(thalDataPath)['sliceCountSum'].item()
sliceTotalVoxelsSum = np.load(thalDataPath)['sliceTotalVoxelsSum'].item()

# 1/0

areasToPlot = [
    'Medial geniculate complex, dorsal part',
    'Medial geniculate complex, medial part',
    'Medial geniculate complex, ventral part',
    'Lateral posterior nucleus of the thalamus',
    'Suprageniculate nucleus',
    'Posterior limiting nucleus of the thalamus'#,
    # 'Posterior triangular thalamic nucleus',
    # 'Posterior intralaminar nucleus',
    # 'Peripeduncular nucleus'
]

plotDensity=True

abbrevs = ['MGd', 'MGm', 'MGv', 'LP', 'SG', 'Pol']
areaSums = [sliceCountSum[key] for key in areasToPlot]
areaDensity = [sliceCountSum[key]/float(sliceTotalVoxelsSum[key]) for key in areasToPlot]

axP = plt.subplot(gs[1, 2])
axP.annotate('F', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')

# axP.set_xlabel('Location')
# axP.set_ylabel('Cell density')
if PANELS[5]:
    ind = np.arange(len(areaSums))
    width = 0.5
    if plotDensity:
        axP.bar(ind, areaDensity, width, color=barColor)
        plt.ylabel('Cell density (cells/voxel)')
    else:
        axP.bar(ind, areaSums, width, color=barColor)
        plt.ylabel('Number of cells')
    axP.set_xticks(ind+width)
    axP.set_xticklabels(abbrevs, rotation=70, horizontalalignment='right')
    plt.subplots_adjust(bottom=0.2, left=0.2)
    plt.xlim([ind[0]-0.3, ind[-1]+width+0.3])
    extraplots.boxoff(axP)

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)