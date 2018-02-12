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

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
reload(figparams)

FIGNAME = 'figure_PV_SOM_firing_rates'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'PV_SOM_firing_rates' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [12,5] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.33, 0.65]   # Horiz position for panel labels
labelPosY = [0.9]    # Vert position for panel labels

summaryFileName = 'photoidentified_cells_firing_rates.npz'


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')


gs = gridspec.GridSpec(1,3,width_ratios=[1, 1, 1])
gs.update(top=0.9, left=0.07, right=0.95, wspace=0.3, hspace=0.2)

if PANELS[0]:
    dataFullPath = os.path.join(dataDir,summaryFileName)
    data = np.load(dataFullPath)
    
    PVonsetProp = data['PVonsetProp']
    SOMonsetProp = data['SOMonsetProp']
    
    categoryLabels = ['PV', 'SOM']
    colours = [figparams.colp['PVcell'],figparams.colp['SOMcell']]
    
    axHist = plt.subplot(gs[0,0])
    plt.hold(1)
    bins = np.linspace(0, 1, 25)
    plt.hist([PVonsetProp, SOMonsetProp], bins, alpha=0.7, label=categoryLabels, color=colours, lw=3, normed=True, histtype='stepfilled',edgecolor='none')
    plt.legend(loc='best')
    plt.xlim((0,1))
    plt.xlabel('Proportion of spikes in time range 0-50ms', fontsize=fontSizeLabels)
    extraplots.boxoff(axHist)
    plt.hold(0)
    axHist.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')

if PANELS[1]:
    dataFullPath = os.path.join(dataDir,summaryFileName)
    data = np.load(dataFullPath)
    
    PVonsetMedianResponse = data['PVonsetMedianResponse']
    PVsustainedMedianResponse = data['PVsustainedMedianResponse']
    SOMonsetMedianResponse = data['SOMonsetMedianResponse']
    SOMsustainedMedianResponse = data['SOMsustainedMedianResponse']
    numBands = data['possibleBands']
    
    onsetResponses = [PVonsetMedianResponse, SOMonsetMedianResponse]
    sustainedResponses = [PVsustainedMedianResponse, SOMsustainedMedianResponse]
    
    responses = [onsetResponses, sustainedResponses]
    titles = ["Median onset response","Median sustained response"]
    
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    panelLabels = ['B', 'C']
    
    for ind, response in enumerate(responses):
        axCurve = plt.subplot(gs[0,ind+1])
        plt.hold(True)
        l1,=plt.plot(range(len(numBands)),response[0],'-', color=PVColor, lw=3)
        l2,=plt.plot(range(len(numBands)),response[1],'-', color=SOMColor, lw=3)
        plt.legend([l1,l2],['PV','SOM'], borderaxespad=0., loc='best')
        axCurve.set_xticks(range(len(numBands)))
        axCurve.set_xticklabels(numBands)
        axCurve.set_ylim(bottom=0)
        axCurve.set_xlabel('bandwidth (octaves)',fontsize=fontSizeLabels)
        axCurve.set_ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
        axCurve.set_title(titles[ind],fontsize=fontSizeLabels,fontweight='normal')
        axCurve.annotate(panelLabels[ind], xy=(labelPosX[ind+1],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
