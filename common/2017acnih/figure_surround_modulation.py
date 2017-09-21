'''
Create figure showing frequency tuning (pure tones) and bandwidth tuning (AM band-pass noise).
'''

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


DIRNAME = 'photoidentified_cells_bandwidth_tuning'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2017acnih', DIRNAME)

PANELS_TO_PLOT = [1,0,1] # [ExperimentalRaster, ExperimentalTuning, ModelTuning]

filenameFreqTuning = 'example_frequency_tuning_band002_2016-08-12_T6_c4.npz'
filenameBandTuning = 'example_bandwidth_tuning_band002_2016-08-12_T6_c4.npz'

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'surround_modulation' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
#figSize = [4,6]
figSize = [3.5, 4.5]

fontSizeLabels = 14
fontSizeTicks = 12
fontSizePanel = 16
labelDis = 0.1
labelPosX = [0.07, 0.45]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

#laserColor = ['#4e9a06','#8ae234']
#laserColor = ['#90C000','#B0F020']
#laserColor = ['#9AB973','#AAD983']
#laserColor = ['0.5','0.75']
#noLaserColor = ['0.25', '0.75']
laserColor = [cp.TangoPalette['Butter3'],cp.TangoPalette['Butter1']]
freqTuningColor = ['0', '0.5']
bandTuningColor = [cp.TangoPalette['Plum2'],cp.TangoPalette['Plum1']]
#colors = [freqTuningColor, laserColor]

gs = gridspec.GridSpec(2,1)
#gs.update(top=0.9, left=0.1, bottom=0.15, right=0.98, wspace=0.25, hspace=0.25) # Horizontal
#gs.update(top=0.95, left=0.15, bottom=0.08, right=0.95, wspace=0.25, hspace=0.25)  # Vertical
gs.update(top=0.95, left=0.15, bottom=0.1, right=0.95, wspace=0.25, hspace=0.4)  # Vertical

dataFreq = np.load(os.path.join(dataDir,filenameFreqTuning))
dataBand = np.load(os.path.join(dataDir,filenameBandTuning))


if PANELS_TO_PLOT[0]:
    spikeArray = dataFreq['spikeArray']
    errorArray = dataFreq['errorArray']
    baselineMean = dataFreq['baselineMean']
    baselineSEM = dataFreq['baselineSEM']
    bands = dataFreq['possibleBands']
    axTuning = plt.subplot(gs[0,0])
    intensityInd = 1  # Intensities are [30,40,50,60]
    #firingRateToPlot = spikeArray[:,:].mean(1)
    firingRateToPlot = spikeArray[:,intensityInd].flatten()
    lines = []
    plt.hold(True)
    l2,=plt.plot(np.log2(bands), firingRateToPlot, '-o', clip_on=False,
                 color = freqTuningColor[0], mec=freqTuningColor[0], linewidth = 3)
    plt.fill_between(np.log2(bands), firingRateToPlot - errorArray[:,intensityInd].flatten(), 
                     firingRateToPlot + errorArray[:,intensityInd].flatten(),
                     alpha=0.2, edgecolor = freqTuningColor[1], facecolor=freqTuningColor[1])
    plt.axhline(baselineMean,color='k',ls='--',lw=2)
    #axTuning.set_xscale('log')
    xTicks = np.array([2000,4000,8000,16000,32000])
    axTuning.set_xticks(np.log2(xTicks))
    axTuning.set_xticklabels(xTicks/1000)
    axTuning.set_xlim([11-0.5, 15+0.5])
    #axTuning.set_ylim([2,7])
    plt.xlabel('Frequency (kHz)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    extraplots.boxoff(axTuning)
    #plt.legend(lines,['no laser', 'laser'], bbox_to_anchor=(0.95, 0.95), borderaxespad=0.)
    #plt.legend(lines,['No SOM', 'Control'], loc='lower center', frameon=False) #'upper left'
    #plt.title('Mouse AC',fontsize=fontSizeLabels,fontweight='bold')


'''
# --- Raster plots of sound response with and without laser ---
if PANELS_TO_PLOT[1]:
    laserTrials = data['possibleSecondSort']
    for laser in laserTrials:
        plt.subplot(gs[laser,1])
        colorEachCond = np.tile(colors[laser], len(data['possibleBands'])/2+1)
        pRaster, hcond, zline = extraplots.raster_plot(data['spikeTimesFromEventOnset'],
                                                   data['indexLimitsEachTrial'],
                                                   data['timeRange'],
                                                   trialsEachCond=data['trialsEachCond'][:,:,laser],
                                                   labels=data['firstSortLabels'])
        plt.setp(pRaster, ms=3, color=colors[laser][0])
        plt.ylabel('Bandwidth (oct)')
    plt.xlabel('Time (s)')
'''

# --- Plot of bandwidth tuning with and without laser ---
if PANELS_TO_PLOT[2]:
    spikeArray = dataBand['spikeArray']
    errorArray = dataBand['errorArray']
    bands = dataBand['possibleBands']
    axTuning = plt.subplot(gs[1,0])
    intensityInd = 0 # There are two different intensities 0=54dB RMS (34dB tone) , 1=66dB RMS (42dB tone)
    lines = []
    plt.hold(True)
    l2,=plt.plot(range(len(bands)), spikeArray[:,intensityInd].flatten(), '-o', clip_on=False,
                 color = bandTuningColor[0], mec = bandTuningColor[0], linewidth = 3)
    lines.append(l2)
    plt.fill_between(range(len(bands)), spikeArray[:,intensityInd].flatten() - errorArray[:,intensityInd].flatten(), 
                     spikeArray[:,intensityInd].flatten() + errorArray[:,intensityInd].flatten(),
                     alpha=0.2, edgecolor = bandTuningColor[1], facecolor=bandTuningColor[1])
    '''
    l1,=plt.plot(range(len(bands)), spikeArray[:,0].flatten(), '-o', clip_on=False,
                 color = bandTuningColor[0], mec = bandTuningColor[0], linewidth = 3)
    lines.append(l1)
    plt.fill_between(range(len(bands)), spikeArray[:,0].flatten() - errorArray[:,0].flatten(), 
                     spikeArray[:,0].flatten() + errorArray[:,0].flatten(),
                     alpha=0.2, edgecolor = bandTuningColor[1], facecolor=bandTuningColor[1])
    '''
    axTuning.set_xticklabels(bands)
    #axTuning.set_ylim([2,7])
    plt.xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    extraplots.boxoff(axTuning)
    #plt.legend(lines,['no laser', 'laser'], bbox_to_anchor=(0.95, 0.95), borderaxespad=0.)
    #plt.legend(lines,['No SOM', 'Control'], loc='lower center', frameon=False) #'upper left'
    #plt.title('Mouse AC',fontsize=fontSizeLabels,fontweight='bold')


    
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
