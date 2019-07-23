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

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors

from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)

import figparams
reload(figparams)



FIGNAME = 'supplement_figure_characterisation_of_responses_raw_data'
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'figure_characterisation_of_responses_by_cell_type')
dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', 'figure_characterisation_of_responses_by_cell_type') #using data calculated for main figure

PANELS = [1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'characterisation_of_suppression_raw_data' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [5,4] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.01, 0.59]   # Horiz position for panel labels
labelPosY = [0.96]    # Vert position for panel labels


summaryFileName = 'all_photoidentified_cells_stats.npz'


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,2)
gs.update(top=0.90, bottom=0.08, left=0.12, right=0.95, wspace=0.4, hspace=0.6)

# gs0 = gridspec.GridSpec(2,3,width_ratios=[1, 1.3, 1.3])
# gs0.update(top=0.95, bottom=0.05, left=0.1, right=0.95, wspace=0.4, hspace=0.3)

# -- Summary plots comparing suppression indices of PV, SOM, and excitatory cells for sustained responses --    
if PANELS[0]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVsustainedSuppression = summaryData['rawPVsustainedSuppressionInd']
    SOMsustainedSuppression = summaryData['rawSOMsustainedSuppressionInd']
    ACsustainedSuppression = summaryData['rawExcSustainedSuppressionInd']
    
    sustainedSuppressionVals = [ACsustainedSuppression, PVsustainedSuppression, SOMsustainedSuppression]
    
    excitatoryColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [excitatoryColor, PVColor, SOMColor]
    
    categoryLabels = ['Exc.', 'PV', 'SOM']
    
    panelLabel = 'a'
    
    axScatter = plt.subplot(gs[0,0])
    plt.hold(1)
    
    for category in range(len(sustainedSuppressionVals)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
        xval = (category+1)*np.ones(len(sustainedSuppressionVals[category]))
          
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.4 * jitterAmt) - 0.2
          
        plt.hold(True)
        plt.plot(xval, sustainedSuppressionVals[category], 'o', mec=edgeColour, mfc='none', clip_on=False)
        median = np.median(sustainedSuppressionVals[category])
        #sem = stats.sem(vals[category])
        plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
    
#     bplot = plt.boxplot(sustainedSuppressionVals, widths=0.6, showfliers=False)
#     
#     for box in range(len(bplot['boxes'])):
#         plt.setp(bplot['boxes'][box], color=cellTypeColours[box])
#         plt.setp(bplot['whiskers'][2*box:2*(box+1)], linestyle='-', color=cellTypeColours[box])
#         plt.setp(bplot['caps'][2*box:2*(box+1)], color=cellTypeColours[box])
#         plt.setp(bplot['medians'][box], color='k', linewidth=2)
#         #plt.setp(bplot['fliers'][box, marker='o', color=cellTypeColours[box]])
# 
#     plt.setp(bplot['medians'], color='k')   
    
    axScatter.annotate(panelLabel, xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    plt.xlim(0,len(sustainedSuppressionVals)+1)
    plt.ylim(-0.05,1.05)
    plt.ylabel('Suppression Index',fontsize=fontSizeLabels)
    axScatter.set_xticks(range(1,len(sustainedSuppressionVals)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,3], yLims[1]*1.07, yLims[1]*0.02, gapFactor=0.25)
    extraplots.significance_stars([1,2], yLims[1]*1.03, yLims[1]*0.02, gapFactor=0.25)
    plt.hold(0)
    
# -- Summary plots comparing preferred bandwidth of PV, SOM, and excitatory cells for sustained responses --    
if PANELS[1]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVsustainedPrefBW = summaryData['rawPVsustainedPrefBW']
    PVsustainedPrefBW[np.isinf(PVsustainedPrefBW)] = 6
    SOMsustainedPrefBW = summaryData['rawSOMsustainedPrefBW']
    SOMsustainedPrefBW[np.isinf(SOMsustainedPrefBW)] = 6
    ACsustainedPrefBW = summaryData['rawExcSustainedPrefBW']
    ACsustainedPrefBW[np.isinf(ACsustainedPrefBW)] = 6
    possibleBands = summaryData['possibleBands']
    
    prefBandwidths = [ACsustainedPrefBW, PVsustainedPrefBW, SOMsustainedPrefBW]
    
    excitatoryColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [excitatoryColor, PVColor, SOMColor]
    
    categoryLabels = ['Exc.', 'PV', 'SOM']
    
    panelLabel = 'b'
    
    axScatter = plt.subplot(gs[0,1])
    plt.hold(1)
    axScatter.set_yscale('symlog', basey=2, linthreshy=0.25, linscaley=0.5)
    plt.hold(True)
    for category in range(len(prefBandwidths)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
        xval = (category+1)*np.ones(len(prefBandwidths[category]))
          
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.4 * jitterAmt) - 0.2
          
        plt.plot(xval, prefBandwidths[category], 'o', mec=edgeColour, mfc='none', clip_on=False)
        median = np.median(prefBandwidths[category])
        plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
    
#     bplot = plt.boxplot(prefBandwidths, widths=0.6, showfliers=False)
#     
#     for box in range(len(bplot['boxes'])):
#         plt.setp(bplot['boxes'][box], color=cellTypeColours[box])
#         plt.setp(bplot['whiskers'][2*box:2*(box+1)], linestyle='-', color=cellTypeColours[box])
#         plt.setp(bplot['caps'][2*box:2*(box+1)], color=cellTypeColours[box])
#         plt.setp(bplot['medians'][box], color='k', linewidth=2)
#         #plt.setp(bplot['fliers'][box, marker='o', color=cellTypeColours[box]])
# 
#     plt.setp(bplot['medians'], color='k')
    
    axScatter.annotate(panelLabel, xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    plt.xlim(0,len(prefBandwidths)+1)
    plt.ylim(-0.05,7)
    plt.ylabel('Preferred bandwidth (oct)',fontsize=fontSizeLabels)
    axScatter.set_xticks(range(1,len(prefBandwidths)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    axScatter.set_yticks(possibleBands)
    bandLabels = possibleBands.tolist()
    bandLabels[-1] = 'WN'
    axScatter.set_yticklabels(bandLabels)
    axScatter.tick_params(top=False, right=False, which='both')
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    #extraplots.significance_stars([1,3], yLims[1]*1.05, yLims[1]*0.1, gapFactor=0.25)
    plt.hold(0)
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)