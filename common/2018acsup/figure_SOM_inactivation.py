import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors

from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)

import figparams
reload(figparams)


FIGNAME = 'figure_SOM_inactivation'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'SOM_inactivation' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [12,5] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.32, 0.65]   # Horiz position for panel labels
labelPosY = [0.95]    # Vert position for panel labels

exampleFileName = 'example_SOM_inactivation_band025_2017-04-20_1400um_T6_c6.npz'


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2,3,width_ratios=[1,1.3, 1.3])
gs.update(top=0.95, left=0.1, right=0.95, wspace=0.3, hspace=0.1)

# --- Raster plots of sound response with and without laser ---
if PANELS[0]:
    exampleDataFullPath = os.path.join(dataDir,exampleFileName)
    exampleData = np.load(exampleDataFullPath)
    colours = [['k','0.5'], [figparams.colp['laser'],figparams.colp['laserError']]]
    possibleBands = exampleData['possibleBands']
    bandLabels = ['{}'.format(band) for band in np.unique(possibleBands)]
    
    laserTrials = exampleData['possibleLasers']
    for laser in laserTrials:
        axRaster = plt.subplot(gs[laser,0])
        colorEachCond = np.tile(colours[laser], len(possibleBands)/2+1)
        pRaster, hcond, zline = extraplots.raster_plot(exampleData['spikeTimesFromEventOnset'],
                                                   exampleData['indexLimitsEachTrial'],
                                                   exampleData['timeRange'],
                                                   trialsEachCond=exampleData['trialsEachCond'][:,:,laser],
                                                   labels=bandLabels,
                                                   colorEachCond=colorEachCond)
        plt.setp(pRaster, ms=3)
        plt.ylabel('Bandwidth (oct)')
        if not laser:
            axRaster.set_xticklabels('')
    plt.xlabel('Time from sound onset (s)')
    axRaster.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')


# --- Plot of bandwidth tuning with and without laser ---
if PANELS[1]:
    exampleDataFullPath = os.path.join(dataDir,exampleFileName)
    exampleData = np.load(exampleDataFullPath)
    
    onsetResponseArray = exampleData['onsetResponseArray']
    onsetSTD = exampleData['onsetSTD']
    sustainedResponseArray = exampleData['sustainedResponseArray']
    sustainedSTD = exampleData['sustainedSTD']
    baseline = exampleData['baselineMean']

    bands = exampleData['possibleBands']
    laserTrials = exampleData['possibleLasers']
    bandLabels = ['{}'.format(band) for band in np.unique(possibleBands)]
    
    colours = [['k','0.5'], [figparams.colp['laser'],figparams.colp['laserError']]]
    
    responses = [onsetResponseArray, sustainedResponseArray]
    STDs = [onsetSTD, sustainedSTD]
    
    panelLabels = ['B', 'C']
    sigLabels = [['ns','ns','ns','ns','ns','ns','ns'],
                 ['ns','ns','ns','ns','*','**','***']]
    
    for ind, responseType in enumerate(responses):
        lines = []
        axCurve = plt.subplot(gs[:,ind+1])
        plt.hold(1)
        for laser in laserTrials:
            thisResponse = responseType[:,laser].flatten()
            thisSTD = STDs[ind][:,laser].flatten()
            line,=plt.plot(range(len(bands)), thisResponse, '-o', ms=7, lw=3,
                     color=colours[laser][0], mec=colours[laser][0], clip_on=False)
            lines.append(line)
            plt.fill_between(range(len(bands)), thisResponse - thisSTD, 
                             thisResponse + thisSTD, alpha=0.2, color=colours[laser][1], edgecolor='none')
        plt.plot(range(len(bands)), np.tile(baseline, len(bands)), '--', color='0.4', lw=2)
        axCurve.annotate(panelLabels[ind], xy=(labelPosX[ind+1],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
        axCurve.set_ylim(bottom=0)
        axCurve.set_xlim(left=-0.3)
        yLims = np.array(plt.ylim())
        plt.legend(lines,['Control', 'No SOM'], loc='best', frameon=False)
        extraplots.boxoff(axCurve)
        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        axCurve.set_xticks(range(len(bands)))
        axCurve.set_xticklabels(bands)
        plt.xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
        if not ind:
            plt.title('Onset responses',fontsize=fontSizeLabels)
        else:
            plt.title('Sustained responses',fontsize=fontSizeLabels)
        for ind2, label in enumerate(sigLabels[ind]):
            fontsize = 10
            color = '0.5'
            if not label=='ns':
                fontsize = 16
                color='k'
            axCurve.text(ind2, max(responseType[ind2,0],responseType[ind2,1])+yLims[1]*0.06, label, color=color, fontsize=fontsize, va='center', ha='center', clip_on=False)


    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)