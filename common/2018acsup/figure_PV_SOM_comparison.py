''' 
Create figure showing comparisons between excitatory and inhibitory onsetivity and high bandwidth responses not shown in figure 1.
'''
import os
import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
reload(figparams)



FIGNAME = 'figure_characterisation_of_responses_by_cell_type'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'Fig5_PV_SOM_high_band_responses' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [10,3] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.01, 0.36, 0.69]   # Horiz position for panel labels
labelPosY = [0.94]    # Vert position for panel labels

summaryFileName = 'all_photoidentified_cells_stats.npz' #using same data file as fig 1

PVColor = figparams.colp['PVcell']
SOMColor = figparams.colp['SOMcell']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,3, width_ratios=[1.2,0.9,0.9])
gs.update(top=0.95, bottom=0.15, left=0.06, right=0.98, wspace=0.45, hspace=0.6)

# Summary plots showing firing rates of PV, SOM during sound presentation
if PANELS[0]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVaveragePSTH = summaryData['PVaveragePSTH']
    SOMaveragePSTH = summaryData['SOMaveragePSTH']
    
    binStartTimes = summaryData['PSTHbinStartTimes']
    
    categoryLabels = [r'PV$^+$', r'SOM$^+$']

    panelLabel = 'A'
    
    axPSTH = plt.subplot(gs[0,0])
    plt.hold(1)
    l1, = plt.plot(binStartTimes[1:-1],PVaveragePSTH[1:-1],color=PVColor, lw=2)
    l2, = plt.plot(binStartTimes[1:-1],SOMaveragePSTH[1:-1],color=SOMColor, lw=2)
    plt.legend([l1,l2],categoryLabels, loc='best', frameon=False, fontsize=fontSizeLabels)
    zline = plt.axvline(0,color='0.75',zorder=-10)
    plt.ylim(-0.1,1.1)
    plt.xlabel('Time from sound onset (s)', fontsize=fontSizeLabels)
    plt.ylabel('Normalized firing rate', fontsize=fontSizeLabels)
    axPSTH.annotate(panelLabel, xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    extraplots.boxoff(axPSTH)
    
    
# Summary plot showing "onsetivity" of Exc., PV, and SOM cells
if PANELS[1]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVhighBandRate = summaryData['PVonsetResponses']-summaryData['PVbaselines']
    SOMhighBandRate = summaryData['SOMonsetResponses']-summaryData['SOMbaselines']
    
    responseRates = [PVhighBandRate, SOMhighBandRate]
    
    categoryLabels = [r'PV$^+$', r'SOM$^+$']
    
    cellTypeColours = [PVColor, SOMColor]
    
    panelLabel = 'B'
    
    axScatter = plt.subplot(gs[0,1])
    plt.hold(1)
    
#     for category in range(len(responseRates)):
#         edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
#         xval = (category+1)*np.ones(len(responseRates[category]))
#          
#         jitterAmt = np.random.random(len(xval))
#         xval = xval + (0.4 * jitterAmt) - 0.2
#          
#         plt.plot(xval, responseRates[category], 'o', mec=edgeColour, mfc='none', ms=8, mew = 2, clip_on=False)
#         median = np.median(responseRates[category])
#         #sem = stats.sem(vals[category])
#         plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
        
    bplot = plt.boxplot(responseRates, widths=0.6, showfliers=False)
    
    for box in range(len(bplot['boxes'])):
        plt.setp(bplot['boxes'][box], color=cellTypeColours[box], linewidth=2)
        plt.setp(bplot['whiskers'][2*box:2*(box+1)], linestyle='-', color=cellTypeColours[box])
        plt.setp(bplot['caps'][2*box:2*(box+1)], color=cellTypeColours[box])
        plt.setp(bplot['medians'][box], color='k', linewidth=3)

    plt.setp(bplot['medians'], color='k')
    
    plt.xlim(0,len(responseRates)+1)
    plt.ylim(top=50)
    axScatter.set_xticks(range(1,len(responseRates)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    plt.ylabel('High bandwidth \n' r'onset response ($\Delta$spk/s)', fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,2], yLims[1]*0.98, yLims[1]*0.04, gapFactor=0.25)
    #extraplots.significance_stars([2,3], yLims[1]*0.98, yLims[1]*0.04, gapFactor=0.25)
    plt.hold(0)
    axScatter.annotate(panelLabel, xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    
    PVSOM = stats.ranksums(PVhighBandRate, SOMhighBandRate)[1]
    print "Difference in PV-SOM high bandwidth onset sound response p val: {}".format(PVSOM)


# Summary plot showing difference in Exc., PV, and SOM sustained sound response at high bandwidths
if PANELS[2]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVhighBandRate = summaryData['PVsustainedResponses']-summaryData['PVbaselines']
    SOMhighBandRate = summaryData['SOMsustainedResponses']-summaryData['SOMbaselines']
    
    responseRates = [PVhighBandRate, SOMhighBandRate]
    
    categoryLabels = [r'PV$^+$', r'SOM$^+$']
    
    cellTypeColours = [PVColor, SOMColor]
    
    panelLabel = 'C'
    
    axScatter = plt.subplot(gs[0,2])
    plt.hold(1)
    
#     for category in range(len(responseRates)):
#         edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
#         xval = (category+1)*np.ones(len(responseRates[category]))
#          
#         jitterAmt = np.random.random(len(xval))
#         xval = xval + (0.4 * jitterAmt) - 0.2
#          
#         plt.plot(xval, responseRates[category], 'o', mec=edgeColour, mfc='none', ms=8, mew = 2, clip_on=False)
#         median = np.median(responseRates[category])
#         #sem = stats.sem(vals[category])
#         plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
        
    bplot = plt.boxplot(responseRates, widths=0.6, showfliers=False)
    
    for box in range(len(bplot['boxes'])):
        plt.setp(bplot['boxes'][box], color=cellTypeColours[box], linewidth=2)
        plt.setp(bplot['whiskers'][2*box:2*(box+1)], linestyle='-', color=cellTypeColours[box])
        plt.setp(bplot['caps'][2*box:2*(box+1)], color=cellTypeColours[box])
        plt.setp(bplot['medians'][box], color='k', linewidth=3)

    plt.setp(bplot['medians'], color='k')
    
    plt.xlim(0,len(responseRates)+1)
    plt.ylim(top=17)
    axScatter.set_xticks(range(1,len(responseRates)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    plt.ylabel('High bandwidth \n' r'sustained response ($\Delta$spk/s)', fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,2], yLims[1]*0.95, yLims[1]*0.04, gapFactor=0.25)
    plt.hold(0)
    axScatter.annotate(panelLabel, xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    
    PVSOM = stats.ranksums(PVhighBandRate, SOMhighBandRate)[1]
    print "Difference in PV-SOM high bandwidth sustained sound response p val: {}".format(PVSOM)

    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)