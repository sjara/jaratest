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



FIGNAME = 'supplement_figure_excitatory_high_band_responses'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'figure_characterisation_of_responses_by_cell_type') #using data from figure 1

PANELS = [1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'SuppFig6_excitatory_high_band_responses' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [8,3] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.01, 0.33, 0.64]   # Horiz position for panel labels
labelPosY = [0.94]    # Vert position for panel labels

summaryFileName = 'all_photoidentified_cells_stats.npz' #using same data file as fig 1


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,3)
gs.update(top=0.95, bottom=0.15, left=0.08, right=0.95, wspace=0.5, hspace=0.6)

# Summary plots showing firing rates of PV, SOM during sound presentation
if PANELS[0]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    ExcAveragePSTH = summaryData['ExcAveragePSTH']
    PVaveragePSTH = summaryData['PVaveragePSTH']
    SOMaveragePSTH = summaryData['SOMaveragePSTH']
    
    binStartTimes = summaryData['PSTHbinStartTimes']
    
    categoryLabels = ['Exc.', 'PV', 'SOM']
    ExcColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    panelLabel = 'a'
    
    axPSTH = plt.subplot(gs[0,0])
    plt.hold(1)
    l1, = plt.plot(binStartTimes[1:-1],ExcAveragePSTH[1:-1],color=ExcColor, lw=2, zorder=10)
    l2, = plt.plot(binStartTimes[1:-1],PVaveragePSTH[1:-1],color=PVColor, lw=2)
    l3, = plt.plot(binStartTimes[1:-1],SOMaveragePSTH[1:-1],color=SOMColor, lw=2)
    plt.legend([l1,l2,l3],categoryLabels, loc='best', frameon=False, fontsize=fontSizeLabels)
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
    
    ExcOnsetProp = summaryData['ExcOnsetProp']*100.0
    PVonsetProp = summaryData['PVonsetProp']*100.0
    SOMonsetProp = summaryData['SOMonsetProp']*100.0
    
    onsetProps = [ExcOnsetProp, PVonsetProp, SOMonsetProp]
    
    categoryLabels = ['Exc.', 'PV', 'SOM']
    ExcColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [ExcColor, PVColor, SOMColor]
    
    panelLabel = 'b'
    
    axScatter = plt.subplot(gs[0,1])
    plt.hold(1)
    
#     for category in range(len(onsetProps)):
#         edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
#         xval = (category+1)*np.ones(len(onsetProps[category]))
#           
#         jitterAmt = np.random.random(len(xval))
#         xval = xval + (0.4 * jitterAmt) - 0.2
#           
#         plt.plot(xval, onsetProps[category], 'o', mec=edgeColour, mfc='none', ms=8, mew = 2, clip_on=False)
#         median = np.median(onsetProps[category])
#         #sem = stats.sem(vals[category])
#         plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
          
    bplot = plt.boxplot(onsetProps, widths=0.6, showfliers=False)
    
    for box in range(len(bplot['boxes'])):
        plt.setp(bplot['boxes'][box], color=cellTypeColours[box])
        plt.setp(bplot['whiskers'][2*box:2*(box+1)], linestyle='-', color=cellTypeColours[box])
        plt.setp(bplot['caps'][2*box:2*(box+1)], color=cellTypeColours[box])
        plt.setp(bplot['medians'][box], color='k', linewidth=2)
        #plt.setp(bplot['fliers'][box, marker='o', color=cellTypeColours[box]])

    plt.setp(bplot['medians'], color='k')
    
    plt.xlim(0,len(onsetProps)+1)
    #plt.ylim(0,32)
    axScatter.set_xticks(range(1,len(onsetProps)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    plt.ylabel('Spikes in first 50 ms (%)', fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,3], yLims[1]*0.98, yLims[1]*0.04, gapFactor=0.25)
    plt.hold(0)
    axScatter.annotate(panelLabel, xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    
    PVSOM = stats.ranksums(PVonsetProp, SOMonsetProp)[1]
    print "Difference in PV-SOM onsetivity p val: {}".format(PVSOM)
    
    ExcPV = stats.ranksums(ExcOnsetProp, PVonsetProp)[1]
    print "Difference in Exc-PV onsetivity p val: {}".format(ExcPV)
    
    ExcSOM = stats.ranksums(ExcOnsetProp, SOMonsetProp)[1]
    print "Difference in Exc-SOM onsetivity p val: {}".format(ExcSOM)


# Summary plot showing difference in Exc., PV, and SOM sustained sound response at high bandwidths
if PANELS[2]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    ExcHighBandRate = summaryData['ExcSustainedResponses']-summaryData['ExcBaselines']
    PVhighBandRate = summaryData['PVsustainedResponses']-summaryData['PVbaselines']
    SOMhighBandRate = summaryData['SOMsustainedResponses']-summaryData['SOMbaselines']
    
    responseRates = [ExcHighBandRate, PVhighBandRate, SOMhighBandRate]
    
    categoryLabels = ['Exc.', 'PV', 'SOM']
    ExcColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [ExcColor, PVColor, SOMColor]
    
    panelLabel = 'c'
    
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
        plt.setp(bplot['boxes'][box], color=cellTypeColours[box])
        plt.setp(bplot['whiskers'][2*box:2*(box+1)], linestyle='-', color=cellTypeColours[box])
        plt.setp(bplot['caps'][2*box:2*(box+1)], color=cellTypeColours[box])
        plt.setp(bplot['medians'][box], color='k', linewidth=2)

    plt.setp(bplot['medians'], color='k')
    
    plt.xlim(0,len(responseRates)+1)
    plt.ylim(top=17)
    axScatter.set_xticks(range(1,len(responseRates)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    plt.ylabel('High bandwidth response (spk/s)', fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,2], yLims[1]*0.85, yLims[1]*0.04, gapFactor=0.25)
    extraplots.significance_stars([1,3], yLims[1]*0.95, yLims[1]*0.04, gapFactor=0.25)
    plt.hold(0)
    axScatter.annotate(panelLabel, xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    
    PVSOM = stats.ranksums(PVhighBandRate, SOMhighBandRate)[1]
    print "Difference in PV-SOM high bandwidth sound response p val: {}".format(PVSOM)
    
    ExcPV = stats.ranksums(ExcHighBandRate, PVhighBandRate)[1]
    print "Difference in Exc-PV high bandwidth sound response p val: {}".format(ExcPV)
    
    ExcSOM = stats.ranksums(ExcHighBandRate, SOMhighBandRate)[1]
    print "Difference in Exc-SOM high bandwidth sound response p val: {}".format(ExcSOM)
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)