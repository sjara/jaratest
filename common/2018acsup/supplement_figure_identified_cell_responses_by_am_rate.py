''' 
Create figure showing bandwidth tuning of an example Excitatory, PV and SOM cell as well as a summary of suppression indices,
comparing SOM to PV to excitatory.

Bandwidth tuning: 30 trials each bandwidth, sound 1 sec long, average iti 1.5 seconds
Center frequency determined with shortened tuning curve (16 freq, best frequency as estimated by gaussian fit)
AM rate selected as one eliciting highest sustained spike

Using difference of gaussians fit to determine suppression indices and preferred bandwidth.
'''
import os
import numpy as np

from scipy import stats

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.colors

from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)

import figparams
reload(figparams)



FIGNAME = 'supplement_figure_characterisation_of_responses_by_AM_rate'
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', FIGNAME)

PANELS = [1,1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'characterisation_of_suppression_by_AM_rate' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [8,8] # In inches

dataFileName = 'all_photoidentified_cells_stats_by_AM_rate.npz'

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.01, 0.21]   # Horiz position for panel labels
labelPosY = [0.96, 0.65]    # Vert position for panel labels

ExColor = figparams.colp['excitatoryCell']
PVColor = figparams.colp['PVcell']
SOMColor = figparams.colp['SOMcell']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2,2,width_ratios=[1,1])
gs.update(top=0.95, bottom=0.08, left=0.08, right=0.95, wspace=0.3, hspace=0.4)

# --- Histogram of distribution of AM rates used ---
if PANELS[0]:
    dataFullPath = os.path.join(dataDir,dataFileName)
    data = np.load(dataFullPath)
    
    axBar = plt.subplot(gs[0,0])

    ExAMrate = data['ExAMrate']
    PVAMrate = data['PVAMrate']
    SOMAMrate = data['SOMAMrate']
    
    rates = np.unique(ExAMrate).astype(int)
    
    ExCounts = np.bincount(ExAMrate.astype(int))[rates]
    PVCounts = np.bincount(PVAMrate.astype(int))[rates]
    SOMCounts = np.bincount(SOMAMrate.astype(int))[rates]

    ExPercents = 100.0*ExCounts/np.sum(ExCounts)
    PVPercents = 100.0*PVCounts/np.sum(PVCounts)
    SOMPercents = 100.0*SOMCounts/np.sum(SOMCounts)
    
    plt.hold(True)
    #axBar.set_xscale('log', basex=2)
    xvals = np.arange(len(rates))
    bar_width = 0.25
    bar_spacing = 0.03
     
    ExBars = plt.bar(xvals - 1.5*bar_width - bar_spacing, ExPercents, bar_width,
                     color=ExColor,
                     edgecolor=ExColor,
                     label='Exc.')
    PVBars = plt.bar(xvals - 0.5*bar_width, PVPercents, bar_width,
                     color=PVColor,
                     edgecolor=PVColor,
                     label='PV')
    SOMBars = plt.bar(xvals + 0.5*bar_width + bar_spacing, SOMPercents, bar_width,
                     color=SOMColor,
                     edgecolor=SOMColor,
                     label='SOM')
     
    plt.legend(frameon=False, fontsize=fontSizeLabels, loc='best')
    plt.ylim(0,100)
    plt.ylabel('Percentage of cells')
    plt.xlabel('AM rate (Hz)')
    axBar.set_xticks(xvals)
    axBar.set_xticklabels(rates)
    extraplots.boxoff(axBar)

# --- plots of suppression index vs AM rate ---    
if PANELS[1]:
    dataFullPath = os.path.join(dataDir,dataFileName)
    data = np.load(dataFullPath)
    
    axScatter = plt.subplot(gs[0,1])

    ExAMrate = data['ExAMrate']
    PVAMrate = data['PVAMrate']
    SOMAMrate = data['SOMAMrate']
    
    ExSI = data['fitExcSustainedSuppressionInd']
    PVSI = data['fitPVsustainedSuppressionInd']
    SOMSI = data['fitSOMsustainedSuppressionInd']
    
    cellRates = [ExAMrate, PVAMrate]
    cellSIs = [ExSI, PVSI]
    cellTypeColours = [ExColor, PVColor, SOMColor]
    
    bar_width = 0.2
    bar_spacing = 0.1
    bar_loc = [-1,0,1]
    
    allxvals = []
    
    for cellType in range(len(cellRates)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[cellType], alpha=0.6)
        thisCellTypeSIs = cellSIs[cellType]
        thisCellTypeAMrates = cellRates[cellType]
        
        SIs16 = thisCellTypeSIs[np.where(thisCellTypeAMrates==16)[0]]
        SIs32 = thisCellTypeSIs[np.where(thisCellTypeAMrates==32)[0]]
        SIs64 = thisCellTypeSIs[np.where(thisCellTypeAMrates==64)[0]]
        
        print "SI p-vals"
        print "16 vs 32Hz: {}".format(stats.ranksums(SIs16, SIs32)[1])
        print "32 vs 64Hz: {}".format(stats.ranksums(SIs32, SIs64)[1])
        print "16 vs 64Hz: {}".format(stats.ranksums(SIs16, SIs64)[1])
        
        for indSI, SIs in enumerate([SIs16, SIs32, SIs64]):
            xval = (cellType+1)+(bar_loc[indSI]*(bar_width+bar_spacing))
            allxvals.append(xval)
            xvals = xval*np.ones(len(SIs))
              
            jitterAmt = np.random.random(len(xvals))
            xvals = xvals + (bar_width * jitterAmt) - bar_width/2
              
            plt.hold(True)
            plt.plot(xvals, SIs, 'o', mec=edgeColour, mfc='none', clip_on=False)
            median = np.median(SIs)
            plt.plot([xval-bar_width/2,xval+bar_width/2], [median,median], '-', color='k', mec=edgeColour, lw=3)
            
    ExPatch = mpatches.Patch(color=ExColor, label='Exc.')
    PVPatch = mpatches.Patch(color=PVColor, label='PV')
    plt.legend(handles=[ExPatch,PVPatch],frameon=False, fontsize=fontSizeLabels, loc='best')
    
    plt.ylim(-0.1,1.1)
    plt.ylabel('Suppression Index')
    plt.xlabel('AM rate (Hz)')
    axScatter.set_xticks(allxvals)
    axScatter.set_xticklabels(np.tile([16,32,64],len(cellRates)))
    extraplots.boxoff(axScatter)
    
# --- plots of preferred bandwidth ---
if PANELS[2]:
    dataFullPath = os.path.join(dataDir,dataFileName)
    data = np.load(dataFullPath)
    
    axScatter = plt.subplot(gs[1,0])

    ExAMrate = data['ExAMrate']
    PVAMrate = data['PVAMrate']
    SOMAMrate = data['SOMAMrate']
    
    ExPrefBW = data['fitExcSustainedPrefBW']
    PVPrefBW = data['fitPVsustainedPrefBW']
    SOMPrefBW = data['fitSOMsustainedPrefBW']
    
    cellRates = [ExAMrate, PVAMrate]
    cellBWs = [ExPrefBW, PVPrefBW]
    cellTypeColours = [ExColor, PVColor, SOMColor]
    
    bar_width = 0.2
    bar_spacing = 0.1
    bar_loc = [-1,0,1]
    
    allxvals = []
    
    axScatter.set_yscale('symlog', basey=2, linthreshy=0.25, linscaley=0.5)
    for cellType in range(len(cellRates)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[cellType], alpha=0.6)
        thisCellTypeBWs = cellBWs[cellType]
        thisCellTypeAMrates = cellRates[cellType]
        
        BWs16 = thisCellTypeBWs[np.where(thisCellTypeAMrates==16)[0]]
        BWs32 = thisCellTypeBWs[np.where(thisCellTypeAMrates==32)[0]]
        BWs64 = thisCellTypeBWs[np.where(thisCellTypeAMrates==64)[0]]
        
        print "Pref BW p-vals"
        print "16 vs 32Hz: {}".format(stats.ranksums(BWs16, BWs32)[1])
        print "32 vs 64Hz: {}".format(stats.ranksums(BWs32, BWs64)[1])
        print "16 vs 64Hz: {}".format(stats.ranksums(BWs16, BWs64)[1])
        
        for indBW, BWs in enumerate([BWs16, BWs32, BWs64]):
            xval = (cellType+1)+(bar_loc[indBW]*(bar_width+bar_spacing))
            allxvals.append(xval)
            xvals = xval*np.ones(len(BWs))
              
            jitterAmt = np.random.random(len(xvals))
            xvals = xvals + (bar_width * jitterAmt) - bar_width/2
              
            plt.hold(True)
            plt.plot(xvals, BWs, 'o', mec=edgeColour, mfc='none', clip_on=False)
            median = np.median(BWs)
            plt.plot([xval-bar_width/2,xval+bar_width/2], [median,median], '-', color='k', mec=edgeColour, lw=3)
            
    ExPatch = mpatches.Patch(color=ExColor, label='Exc.')
    PVPatch = mpatches.Patch(color=PVColor, label='PV')
    plt.legend(handles=[ExPatch,PVPatch],frameon=False, fontsize=fontSizeLabels, loc='best')
    
    plt.ylim(-0.1,7)
    plt.ylabel('Preferred Bandwidth (octaves)')
    plt.xlabel('AM rate (Hz)')
    axScatter.set_xticks(allxvals)
    axScatter.set_xticklabels(np.tile([16,32,64],len(cellRates)))
    extraplots.boxoff(axScatter)
    
# --- plots of proportion of spikes at onset ---
if PANELS[3]:
    dataFullPath = os.path.join(dataDir,dataFileName)
    data = np.load(dataFullPath)
    
    axScatter = plt.subplot(gs[1,1])

    ExAMrate = data['ExAMrate']
    PVAMrate = data['PVAMrate']
    SOMAMrate = data['SOMAMrate']
    
    ExOnsetProp = data['ExcOnsetProp']
    PVonsetProp = data['PVonsetProp']
    SOMonsetProp = data['SOMonsetProp']
    
    cellRates = [ExAMrate, PVAMrate]
    cellOnsetProps = [ExOnsetProp, PVonsetProp]
    cellTypeColours = [ExColor, PVColor, SOMColor]
    
    bar_width = 0.2
    bar_spacing = 0.1
    bar_loc = [-1,0,1]
    
    allxvals = []
    
    for cellType in range(len(cellRates)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[cellType], alpha=0.6)
        thisCellTypeOnsetProps = cellOnsetProps[cellType]
        thisCellTypeAMrates = cellRates[cellType]
        
        onsetProps16 = thisCellTypeOnsetProps[np.where(thisCellTypeAMrates==16)[0]]
        onsetProps32 = thisCellTypeOnsetProps[np.where(thisCellTypeAMrates==32)[0]]
        onsetProps64 = thisCellTypeOnsetProps[np.where(thisCellTypeAMrates==64)[0]]
        
        for indOnsetProps, onsetProps in enumerate([onsetProps16, onsetProps32, onsetProps64]):
            xval = (cellType+1)+(bar_loc[indOnsetProps]*(bar_width+bar_spacing))
            allxvals.append(xval)
            xvals = xval*np.ones(len(onsetProps))
              
            jitterAmt = np.random.random(len(xvals))
            xvals = xvals + (bar_width * jitterAmt) - bar_width/2
              
            plt.hold(True)
            plt.plot(xvals, onsetProps, 'o', mec=edgeColour, mfc='none', clip_on=False)
            median = np.median(onsetProps)
            plt.plot([xval-bar_width/2,xval+bar_width/2], [median,median], '-', color='k', mec=edgeColour, lw=3)
            
    ExPatch = mpatches.Patch(color=ExColor, label='Exc.')
    PVPatch = mpatches.Patch(color=PVColor, label='PV')
    plt.legend(handles=[ExPatch,PVPatch],frameon=False, fontsize=fontSizeLabels, loc='best')
    
    plt.ylim(-0.1,1.1)
    plt.ylabel('Proportion of spikes in first 50 ms')
    plt.xlabel('AM rate (Hz)')
    axScatter.set_xticks(allxvals)
    axScatter.set_xticklabels(np.tile([16,32,64],len(cellRates)))
    extraplots.boxoff(axScatter)
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)