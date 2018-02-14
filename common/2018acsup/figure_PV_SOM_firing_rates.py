''' 
Create figure showing median firing rates for identified PV and SOM cells during onset and sustained responses.

Bandwidth tuning: 30 trials each bandwidth, sound 1 sec long, average iti 1.5 seconds
Center frequency determined with shortened tuning curve (16 freq, best frequency as estimated by gaussian fit)
AM rate selected as one eliciting highest sustained spike
'''
import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
reload(figparams)
reload(extraplots)

FIGNAME = 'figure_PV_SOM_firing_rates'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'PV_SOM_firing_rates' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [9,9] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.48]   # Horiz position for panel labels
labelPosY = [0.93, 0.47]    # Vert position for panel labels

summaryFileName = 'photoidentified_cells_firing_rates.npz'


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')


gs = gridspec.GridSpec(2,2)
gs.update(top=0.9, left=0.07, right=0.95, wspace=0.3, hspace=0.3)

if PANELS[0]:
    dataFullPath = os.path.join(dataDir,summaryFileName)
    data = np.load(dataFullPath)
    
    PVaveragePSTH = data['PVaveragePSTH']
    SOMaveragePSTH = data['SOMaveragePSTH']
    binStartTimes = data['PSTHbinStartTimes']
    PVMAD = data['PVPSTHMAD']
    SOMMAD = data['SOMPSTHMAD']
    
    categoryLabels = ['PV', 'SOM']
    PVcolor = figparams.colp['PVcell']
    SOMcolor = figparams.colp['SOMcell']
    
    axPSTH = plt.subplot(gs[0,0])
    plt.hold(1)
    plt.plot(binStartTimes[1:-1],PVaveragePSTH[1:-1],color=PVcolor, lw=2)
    plt.plot(binStartTimes[1:-1],SOMaveragePSTH[1:-1],color=SOMcolor, lw=2)
#     plt.fill_between(binStartTimes[1:-1], PVaveragePSTH[1:-1] - PVMAD[:-2], 
#                              PVaveragePSTH[1:-1] + PVMAD[:-2], alpha=0.2, color=PVcolor, edgecolor='none')
#     plt.fill_between(binStartTimes[1:-1], SOMaveragePSTH[1:-1] - SOMMAD[:-2], 
#                              SOMaveragePSTH[1:-1] + SOMMAD[:-2], alpha=0.2, color=SOMcolor, edgecolor='none')
    zline = plt.axvline(0,color='0.75',zorder=-10)
    plt.ylim(0,1.1)
    plt.xlabel('Time from sound onset (s)', fontsize=fontSizeLabels)
    plt.ylabel('Normalized firing rate', fontsize=fontSizeLabels)
    axPSTH.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    extraplots.boxoff(axPSTH)

if PANELS[1]:
    dataFullPath = os.path.join(dataDir,summaryFileName)
    data = np.load(dataFullPath)
    
    PVonsetProp = data['PVonsetProp']
    SOMonsetProp = data['SOMonsetProp']
    cellTypes = [PVonsetProp, SOMonsetProp]
    
    categoryLabels = ['PV', 'SOM']
    colours = [figparams.colp['PVcell'],figparams.colp['SOMcell']]
    
    axScatter = plt.subplot(gs[0,1])
    plt.hold(1)
    for category in range(len(cellTypes)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(colours[category], alpha=0.5)
        xval = (category+1)*np.ones(len(cellTypes[category]))
        
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.4 * jitterAmt) - 0.2
        
        plt.plot(xval, cellTypes[category]*100.0, 'o', mec=edgeColour, mfc='none', ms=8, mew = 2, clip_on=False)
        median = np.median(cellTypes[category])
        #sem = stats.sem(vals[category])
        plt.plot([category+0.7,category+1.3], [median*100.0,median*100.0], '-', color='k', mec=colours[category], lw=3)
    plt.xlim(0,len(cellTypes)+1)
    plt.ylim(0,60)
    axScatter.set_xticks(range(1,len(cellTypes)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    plt.ylabel('Percentage of spikes in first 50 ms', fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.new_significance_stars([1,2], yLims[1]*1.05, yLims[1]*0.04, starMarker='p = 0.007', gapFactor=0.4)
    plt.hold(0)
    axScatter.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')

if PANELS[2]:
    dataFullPath = os.path.join(dataDir,summaryFileName)
    data = np.load(dataFullPath)
    
    PVonsetResponses = data['PVonsetResponses']
    PVsustainedResponses = data['PVsustainedResponses']
    SOMonsetResponses = data['SOMonsetResponses']
    SOMsustainedResponses = data['SOMsustainedResponses']
    numBands = data['possibleBands']
    
    onsetResponses = [PVonsetResponses, SOMonsetResponses]
    sustainedResponses = [PVsustainedResponses, SOMsustainedResponses]
    
    responses = [onsetResponses, sustainedResponses]
    ylabels = ["Onset firing rate (spk/s)","Sustained firing rate (spk/s)"]
    
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    panelLabels = ['C', 'D']
    sigLabels = [['ns','ns','ns','ns','ns','ns','ns'],
                 ['ns','ns','*','*','*','*','ns']]
    
    for ind, response in enumerate(responses):
        axCurve = plt.subplot(gs[1,ind])
        plt.hold(True)
        bpPV = plt.boxplot(response[0].tolist(), positions=np.array(xrange(len(response[0])))*2.0-0.4, sym='', widths=0.6)
        bpSOM = plt.boxplot(response[1].tolist(), positions=np.array(xrange(len(response[1])))*2.0+0.4, sym='', widths=0.6)

        plt.setp(bpPV['boxes'], color=PVColor)
        plt.setp(bpPV['whiskers'], color=PVColor)
        plt.setp(bpPV['caps'], color=PVColor)
        plt.setp(bpPV['medians'], color='k')
        
        plt.setp(bpSOM['boxes'], color=SOMColor)
        plt.setp(bpSOM['whiskers'], color=SOMColor)
        plt.setp(bpSOM['caps'], color=SOMColor)
        plt.setp(bpSOM['medians'], color='k')
        
        plt.xticks(xrange(0, len(numBands) * 2, 2), numBands)
        plt.xlim(-2, len(numBands)*2)
        
        yLims = np.array(plt.ylim())
        for ind2, label in enumerate(sigLabels[ind]):
            fontsize = 10
            color = '0.5'
            if label=='*':
                fontsize = 16
                color='k'
            #axCurve.text(ind2, max(response[0][ind2],response[1][ind2])+yLims[1]*0.06, label, color=color, fontsize=fontsize, va='center', ha='center', clip_on=False)
        #plt.legend([l1,l2],['PV','SOM'], borderaxespad=0., loc='best')
        #axCurve.set_xlim(left=-0.5)
        #axCurve.set_xticks(range(len(numBands)))
        axCurve.set_xticklabels(numBands)
        #axCurve.set_ylim(bottom=0)
        axCurve.set_xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        axCurve.set_ylabel(ylabels[ind],fontsize=fontSizeLabels)
        axCurve.annotate(panelLabels[ind], xy=(labelPosX[ind],labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
        extraplots.boxoff(axCurve)
    

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
