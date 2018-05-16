import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from scipy import stats
import figparams
reload(figparams)

np.random.seed(54)

FIGNAME = 'figure_anatomy'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

anat036nonLem = np.load(os.path.join(dataDir, 'anat036NonLem.npy'))
anat036ventral = np.load(os.path.join(dataDir, 'anat036ventral.npy'))
anat037nonLem = np.load(os.path.join(dataDir, 'anat037NonLem.npy'))
anat037ventral = np.load(os.path.join(dataDir, 'anat037ventral.npy'))

cortexCellDepths = np.load(os.path.join(dataDir, 'anat036_p1d2_cellDepths.npy'))

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    plt.plot([start, end], [yval, yval], color=color, lw=linewidth)

PANELS = [1, 1, 1, 1, 1, 1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
# outputDir = '/tmp/'
# outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'plots_anatomy' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
# figSize = [3.25, 5.5] # In inches
figSize = [6.5, 11] # In inches
# outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
# outputDir = figparams.FIGURE_OUTPUT_DIR
outputDir = '/tmp'

# fontSizeLabels = figparams.fontSizeLabels *3
fontSizeLabels = 18
fontSizeTicks = figparams.fontSizeTicks *3
fontSizePanel = figparams.fontSizePanel *2
dataMS = 8

barColor = '0.5'
anat036NonLemColor = 'k'
anat037NonLemColor = 'k'
anat036VentralColor = 'k'
anat037VentralColor = 'k'

labelPosX = [0.03, 0.53]   # Horiz position for panel labels
labelPosY = [0.97, 0.62, 0.32]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(3, 3)
gs.update(left=0.15, right=0.92, top=0.90, bottom=0.08, wspace=.1, hspace=0.5)

# annotationVolume = ha.AllenAnnotation()

# -- Panel: Injection method --
axInjectionCartoon = plt.subplot(gs[0, :])
axInjectionCartoon.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axInjectionCartoon.axis('off')

# -- Panel: Thalamus detail image --
axThal = plt.subplot(gs[1, 0:2])
axThal.annotate('B', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axThal.axis('off')

# -- Panel: Thalamus histogram --
axThalHist = plt.subplot(gs[1, 2])
axThalHist.annotate('C', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
extraplots.boxoff(axThalHist)

anat036NonLemTotals = np.sum(anat036nonLem, axis=0)/(np.sum(anat036nonLem, axis=0) + anat036ventral).astype(float)
anat037NonLemTotals = np.sum(anat037nonLem, axis=0)/(np.sum(anat037nonLem, axis=0) + anat037ventral).astype(float)

anat036VentralTotals = anat036ventral/(np.sum(anat036nonLem, axis=0) + anat036ventral).astype(float)
anat037VentralTotals = anat037ventral/(np.sum(anat037nonLem, axis=0) + anat037ventral).astype(float)

animalSplit = 0.2
jitterFrac = 0.08
axThalHist.plot(jitter(np.zeros(len(anat036NonLemTotals))-animalSplit, jitterFrac), anat036NonLemTotals, 'o', mec=anat036NonLemColor, mfc='None', ms=dataMS)
axThalHist.plot(jitter(np.zeros(len(anat037NonLemTotals))+animalSplit, jitterFrac), anat037NonLemTotals, 'o', mec=anat037NonLemColor, mfc='None', ms=dataMS)

axThalHist.plot(jitter(np.ones(len(anat036VentralTotals))-animalSplit, jitterFrac), anat036VentralTotals, 'o', mec=anat036VentralColor, mfc='None', ms=dataMS)
axThalHist.plot(jitter(np.ones(len(anat037VentralTotals))+animalSplit, jitterFrac), anat037VentralTotals, 'o', mec=anat037VentralColor, mfc='None', ms=dataMS)

allNonLemTotals = np.concatenate([anat036NonLemTotals, anat037NonLemTotals])
allVentralTotals = np.concatenate([anat036VentralTotals, anat037VentralTotals])
nonLemMean = np.mean([np.mean(anat036NonLemTotals), np.mean(anat037NonLemTotals)])
ventralMean = np.mean([np.mean(anat036VentralTotals), np.mean(anat037VentralTotals)])

statistic, pVal = stats.ranksums(allNonLemTotals, allVentralTotals)
print("Ranksums test, NonLem vs Ventral totals, p={}".format(pVal))

medline(nonLemMean, 0, 0.5, color='k')
medline(ventralMean, 1, 0.5, color='k')

axThalHist.set_xlim([-0.5, 1.5])
axThalHist.set_yticks([0, 1])
axThalHist.set_ylabel('ATh labeled neurons (%)', fontsize=fontSizeLabels)
axThalHist.set_xticks([0, 1])
axThalHist.set_yticklabels(['0', '100'], rotation=90, va='center')
extraplots.set_ticks_fontsize(axThalHist, fontSizeTicks)

axThalHist.set_xticklabels(['Non\nlem.', 'MGv'], fontsize=fontSizeLabels)


# -- Panel: Cortex detail image--
axCortex = plt.subplot(gs[2, 0:2])
axCortex.annotate('D', xy=(labelPosX[0],labelPosY[2]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axCortex.axis('off')

# -- Panel: Cortex layers --
axCortexLayers = plt.subplot(gs[2, 2])
axCortexLayers.annotate('E', xy=(labelPosX[1],labelPosY[2]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
axCortexLayers.axis('off')


# thalDataPath = os.path.join(dataDir, 'thalamusAreaCounts.npz')
# sliceCountSum = np.load(thalDataPath)['sliceCountSum'].item()
# sliceTotalVoxelsSum = np.load(thalDataPath)['sliceTotalVoxelsSum'].item()

# areasToPlot = [
#     'Medial geniculate complex, dorsal part',
#     'Medial geniculate complex, medial part',
#     'Medial geniculate complex, ventral part',
#     'Lateral posterior nucleus of the thalamus',
#     'Suprageniculate nucleus',
#     'Posterior limiting nucleus of the thalamus'#,
#     # 'Posterior triangular thalamic nucleus',
#     # 'Posterior intralaminar nucleus',
#     # 'Peripeduncular nucleus'
# ]

# # abbrevs = ['MGd', 'MGm', 'MGv', 'SG']
# abbrevs = ['MGd', 'MGm', 'MGv', 'LP', 'SG', 'Pol']
# areaSums = [sliceCountSum[key] for key in areasToPlot]

# ##### NOTE: TotalCells used to be the sum of the cells in the areas we wanted to plot. Now
# #####       it is the sum of ALL the cells we counted, regardless of the area
# # totalCells = sum(areaSums)
# totalCells = sum([val for key, val in sliceCountSum.iteritems()])
# #####

# areaPercent = [(val/float(totalCells))*100 for val in areaSums]
# # areaDensity = [sliceCountSum[key]/float(sliceTotalVoxelsSum[key]) for key in areasToPlot]

# axP = plt.subplot(gs[2, 1])
# axP.annotate('F', xy=(labelPosX[1],labelPosY[2]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')

# # axP.set_xlabel('Location')
# # axP.set_ylabel('Cell density')
# if PANELS[5]:
#     ind = np.arange(len(areaSums))
#     width = 0.5
#     #NOTE: Plotting fraction of labeled cells here
#     axP.bar(ind, areaPercent, width, color=barColor)
#     plt.ylabel('% labeled neurons')
#     axP.set_xticks(ind+width)
#     axP.set_xticklabels(abbrevs, rotation=70, horizontalalignment='right')
#     plt.subplots_adjust(bottom=0.2, left=0.2)
#     plt.xlim([ind[0]-0.3, ind[-1]+width+0.3])
#     extraplots.boxoff(axP)


# -- Panel: Cortex cell depth histogram --
# acDataPath = os.path.join(dataDir, 'cortexCellDepths.npy')
# allSliceDepths = np.load(acDataPath)

spec = gs[2, 2]
axP = plt.subplot(gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=spec)[2])
# axP.annotate('D', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
# axP.set_xlabel('Cell density')
# axP.set_ylabel('Depth (um)')

n, bins, patches = axP.hist(cortexCellDepths, bins=20, histtype='step', orientation='horizontal', color='k', lw=2,
                            weights=np.ones_like(cortexCellDepths)/float(len(cortexCellDepths)))
axP.invert_yaxis()
axP.set_ylim([1, 0])

plt.show()
# extraplots.boxoff(axP)
axP.spines['right'].set_visible(False)
axP.spines['top'].set_visible(False)


axP.set_yticks([])
# extraplots.boxoff(axP, keep='none')

#Probably can't get rid of the x-axis
# axP.spines['bottom'].set_visible(False)
axP.set_xticks([0.16])
axP.set_xticklabels(['16'])

extraplots.set_ticks_fontsize(axP, 10)

axP.annotate('E', xy=(labelPosX[1],labelPosY[2]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')

axP.set_xlabel('AC labeled\nneurons (%)', fontsize=fontSizeLabels)

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

    #Plot histogram of cell depths. The weights argument allows the heights of the bars to add to 1.
    # h, bin_edges = np.histogram(allSliceDepths, bins=50, weights=np.ones_like(allSliceDepths)/float(len(allSliceDepths)))
    #Set custom formatter to get output in percent instead of fraction
    # formatter = mticker.FuncFormatter(lambda v, pos: str(v * 100))
    # formatter = mticker.FuncFormatter(lambda v, pos: '{0:g}'.format(v * 100))
    # axP.yaxis.set_major_formatter(formatter)
    # axP.plot(h[::-1], range(len(h)), '-', color='k')
    # axP.set_xlim([0, 1])
    # axP.set_xticks([0, 0.5, 1])
    # plt.ylabel('% labeled neurons')
    # plt.xlabel('Normalized distance from pia')
