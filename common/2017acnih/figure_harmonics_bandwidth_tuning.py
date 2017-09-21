''' Create figure showing bandwidth tuning with noise and harmonically organised tones'''
import os
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'


FIGNAME = 'harmonics_bandwidth_tuning'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2017acnih', FIGNAME)

PANELS_TO_PLOT = [1,1] # [ExperimentalTuning, ModelTuning]

filenameTuning = 'example_bandwidth_tuning_band033_2017-08-02_T8_c5.npz'

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'harmonics_bandwidth_tuning' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [6,4]

fontSizeLabels = 14
fontSizeTicks = 12
fontSizePanel = 16
labelDis = 0.1
labelPosX = [0.07, 0.45]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

harmoColor = [cp.TangoPalette['Orange2'],cp.TangoPalette['Orange1']]
noiseColor = ['0.25', '0.75']
allColors = [noiseColor, harmoColor]

gs = gridspec.GridSpec(2,2)
gs.update(top=0.9, left=0.1, bottom=0.15, right=0.98, wspace=0.25, hspace=0.25)

dataFullPath = os.path.join(dataDir,filenameTuning)
data = np.load(dataFullPath)

# --- Raster plots of sound response with and without laser ---
if 0:
    harmoTrials = data['possibleSecondSort']
    trialsEachCond = data['trialsEachCond']
    for harmo in harmoTrials:
        plt.subplot(gs[1-harmo,0])
        colorEachCond = np.tile(allColors[harmo], len(data['possibleBands'])/2+1)
        trialsThisSecondVal = trialsEachCond[:, :, harmo]
        
        # a dumb workaround that dulpicates the tone trials to put in both rasters
        for ind2, band in enumerate(data['possibleBands']):
            if not any(trialsThisSecondVal[:,ind2]):
                trialsThisSecondVal[:,ind2]=trialsEachCond[:,ind2,harmo+1]
        
        pRaster, hcond, zline = extraplots.raster_plot(data['spikeTimesFromEventOnset'],
                                                   data['indexLimitsEachTrial'],
                                                   data['timeRange'],
                                                   trialsEachCond=trialsEachCond[:,:,harmo],
                                                   labels=data['firstSortLabels'])
        plt.setp(pRaster, ms=3, color=allColors[harmo][0])
        plt.ylabel('Bandwidth (oct)')
    plt.subplot(gs[1,0])
    plt.xlabel('Time (s)')

# --- Plot of bandwidth tuning with and without laser ---
if PANELS_TO_PLOT[0]:
    axTuning = plt.subplot(gs[0:,0])
    spikeArray = data['spikeArray']
    errorArray = data['errorArray']
    
    #duplicate tone data for both curves
    spikeArray[0,0]=spikeArray[0,1]
    errorArray[0,0]=errorArray[0,1]
    
    bands = data['possibleBands']
    lines = []
    plt.hold(True)
    l2,=plt.plot(range(len(bands)), spikeArray[:,1].flatten(), '-o', clip_on=False,
                 color = harmoColor[0], mec = harmoColor[0], lw=3, ms=7)
    lines.append(l2)
    plt.fill_between(range(len(bands)), spikeArray[:,1].flatten() - errorArray[:,1].flatten(), 
                     spikeArray[:,1].flatten() + errorArray[:,1].flatten(),
                     alpha=0.2, edgecolor = harmoColor[1], facecolor=harmoColor[1])
    l1,=plt.plot(range(len(bands)), spikeArray[:,0].flatten(), '-o', clip_on=False,
                 color = noiseColor[0], mec = noiseColor[0], lw=3, ms=7)
    lines.append(l1)
    plt.fill_between(range(len(bands)), spikeArray[:,0].flatten() - errorArray[:,0].flatten(), 
                     spikeArray[:,0].flatten() + errorArray[:,0].flatten(),
                     alpha=0.2, edgecolor = noiseColor[1], facecolor=noiseColor[1])
    axTuning.set_xticks(range(len(bands)))
    axTuning.set_xticklabels([str(int(val)) for val in bands])
    plt.xlim([-0.25,len(bands)-0.75])
    plt.ylim([0,6])
    plt.xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    extraplots.boxoff(axTuning)
    plt.legend(lines,['Harmonics', 'Noise'], loc='upper left', numpoints=1, markerscale=1, handlelength=1, frameon=False)
    plt.title('Mouse AC',fontsize=fontSizeLabels,fontweight='bold')

if PANELS_TO_PLOT[1]:
    axModel = plt.subplot(gs[0:,1])
    modelDataDir = './modeldata'
    import pandas as pd
    modelDataFile = 'SSNbandwidthTuning_HarmonicComplex_noRFwidth_regime1.csv'
    modelData = pd.read_csv(os.path.join(modelDataDir,modelDataFile))
    modelBW = modelData['BW(oct)']
    modelRates = [modelData['y_E_harmonics'], modelData['y_E_noise']]
    colorEachCond = [harmoColor[0], noiseColor[0]]
    for indc,rates in enumerate(modelRates):
        plt.plot(range(len(modelBW)), rates, '-o', lw=3, ms=7, color=colorEachCond[indc], mec=colorEachCond[indc], clip_on=True)
        plt.xlim([0,len(modelBW)])
        xTicks = range(len(modelBW))
        axModel.set_xticks(xTicks)
        newTickLabels = [str(val) for val in modelBW]
        axModel.set_xticklabels(newTickLabels)

        #axModel.set_ylim([0,3])
        plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        axModel.set_xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        extraplots.boxoff(axModel)
    plt.xlim([-0.25,len(modelBW)-0.75])
    plt.ylim([0,7])
    plt.legend(lines,['Harmonics', 'Noise'], loc='upper left', numpoints=1, markerscale=1, handlelength=1, frameon=False)
    plt.title('Model',fontsize=fontSizeLabels,fontweight='bold')



    
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
