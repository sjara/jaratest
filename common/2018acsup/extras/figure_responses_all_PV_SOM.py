''' 
Create figure showing comparisons between excitatory and inhibitory onsetivity and high bandwidth responses not shown in figure 1.
'''
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from jaratoolbox import extraplots
from jaratoolbox import colorpalette as cp



# FIGNAME = 'figure_characterisation_of_responses_by_cell_type'
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'all_PV_SOM_high_band_responses' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [6,10] # In inches

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16
fontSizeTitles = 12
fontSizeLegend = 10

labelPosX = [0.01, 0.36, 0.69]   # Horiz position for panel labels
labelPosY = [0.94]    # Vert position for panel labels

summaryFileName = '/home/jarauser/data/figuresdata/2018acsup/all_photoidentified_cells_untuned_stats.npz'

PVColor = cp.TangoPalette['SkyBlue2']
SOMColor = cp.TangoPalette['ScarletRed1']
ExcColor = 'k'

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(3,1)
gs.update(top=0.98, bottom=0.05, left=0.16, right=0.97, wspace=0.45, hspace=0.3)

# Summary plots showing firing rates of PV, SOM during sound presentation
if PANELS[0]:
    #summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryFileName)
    
    PVtunedAveragePSTH = summaryData['PVtunedAveragePSTH']
    SOMtunedAveragePSTH = summaryData['SOMtunedAveragePSTH']
    ExcTunedAveragePSTH = summaryData['ExcTunedAveragePSTH']
    
    PVtunedOffCentreAveragePSTH = summaryData['PVtunedOffCentreAveragePSTH']
    SOMtunedOffCentreAveragePSTH = summaryData['SOMtunedOffCentreAveragePSTH']
    ExcTunedOffCentreAveragePSTH = summaryData['ExcTunedOffCentreAveragePSTH']
    
    PVuntunedAveragePSTH = summaryData['PVuntunedAveragePSTH']
    SOMuntunedAveragePSTH = summaryData['SOMuntunedAveragePSTH']
    ExcUntunedAveragePSTH = summaryData['ExcUntunedAveragePSTH']
    
    binStartTimes = summaryData['PSTHbinStartTimes']
    
    categoryLabels = [r'PV$^+$', r'SOM$^+$', 'Exc.']

    panelLabel = 'A'
    
    axPSTH = plt.subplot(gs[0,0])
    plt.hold(1)
    
    l4, = plt.plot(binStartTimes[1:-1],PVuntunedAveragePSTH[1:-1],color=PVColor, lw=2, linestyle='--')
    l5, = plt.plot(binStartTimes[1:-1],SOMuntunedAveragePSTH[1:-1],color=SOMColor, lw=2, linestyle='--')
    l6, = plt.plot(binStartTimes[1:-1],ExcUntunedAveragePSTH[1:-1],color=ExcColor, lw=2, linestyle='--')
    
    l7, = plt.plot(binStartTimes[1:-1],PVtunedOffCentreAveragePSTH[1:-1],color=cp.TangoPalette['SkyBlue1'], lw=2)
    l8, = plt.plot(binStartTimes[1:-1],SOMtunedOffCentreAveragePSTH[1:-1],color=cp.TangoPalette['ScarletRed3'], lw=2)
    l9, = plt.plot(binStartTimes[1:-1],ExcTunedOffCentreAveragePSTH[1:-1],color='0.5', lw=2)
    
    l1, = plt.plot(binStartTimes[1:-1],PVtunedAveragePSTH[1:-1],color=PVColor, lw=2)
    l2, = plt.plot(binStartTimes[1:-1],SOMtunedAveragePSTH[1:-1],color=SOMColor, lw=2)
    l3, = plt.plot(binStartTimes[1:-1],ExcTunedAveragePSTH[1:-1],color=ExcColor, lw=2)
    
    plt.legend([l1,l2,l3],categoryLabels, loc='best', frameon=False, fontsize=fontSizeLabels)
    zline = plt.axvline(0,color='0.75',zorder=-10)
    plt.ylim(-0.1,1.1)
    plt.xlabel('Time from sound onset (s)', fontsize=fontSizeLabels)
    plt.ylabel('Normalized firing rate', fontsize=fontSizeLabels)
#     axPSTH.annotate(panelLabel, xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
#                      fontsize=fontSizePanel, fontweight='bold')
    extraplots.boxoff(axPSTH)
    
    
# Summary plot showing "onsetivity" of Exc., PV, and SOM cells
if PANELS[1]:
#summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryFileName)
    
    PVtunedHighBandRate = summaryData['PVTunedOnsetResponses']-summaryData['PVtunedBaselines']
    PVtunedOffCentreHighBandRate = summaryData['PVTunedOffCentreOnsetResponses']-summaryData['PVtunedOffCentreBaselines']
    PVuntunedHighBandRate = summaryData['PVUntunedOnsetResponses']-summaryData['PVuntunedBaselines']
    
    SOMtunedHighBandRate = summaryData['SOMTunedOnsetResponses']-summaryData['SOMtunedBaselines']
    SOMtunedOffCentreHighBandRate = summaryData['SOMTunedOffCentreOnsetResponses']-summaryData['SOMtunedOffCentreBaselines']
    SOMuntunedHighBandRate = summaryData['SOMUntunedOnsetResponses']-summaryData['SOMuntunedBaselines']
    
    ExcTunedHighBandRate = summaryData['ExcTunedOnsetResponses']-summaryData['ExcTunedBaselines']
    ExcTunedOffCentreHighBandRate = summaryData['ExcTunedOffCentreOnsetResponses']-summaryData['ExcTunedOffCentreBaselines']
    ExcUntunedHighBandRate = summaryData['ExcUntunedOnsetResponses']-summaryData['ExcUntunedBaselines']
    
    PVresponseRates = [PVtunedHighBandRate, PVtunedOffCentreHighBandRate, PVuntunedHighBandRate]
    SOMresponseRates = [SOMtunedHighBandRate, SOMtunedOffCentreHighBandRate, SOMuntunedHighBandRate]
    ExcResponseRates = [ExcTunedHighBandRate, ExcTunedOffCentreHighBandRate, ExcUntunedHighBandRate]
    
    responseRates = [ExcResponseRates, PVresponseRates, SOMresponseRates]
    
    categoryLabels = ['tuned', 'tuned, off-centre', 'untuned']
    cellLabels = [r'PV$^+$', r'SOM$^+$', 'Exc.']
    
    cellTypeColours = [ExcColor, PVColor, SOMColor]
    
    panelLabel = 'C'
    
    axScatter = plt.subplot(gs[1,0])
    plt.hold(1)
    
    for ind, response in enumerate(responseRates):
        bplot = plt.boxplot(response, positions=np.array(xrange(len(response)))*4.0+ind, sym='', widths=0.6)
        
        #bplot = plt.boxplot(responseRates, widths=0.6, showfliers=False)
        
        for box in range(len(bplot['boxes'])):
            plt.setp(bplot['boxes'][box], color=cellTypeColours[ind], linewidth=2)
            plt.setp(bplot['whiskers'][2*box:2*(box+1)], linestyle='-', color=cellTypeColours[ind])
            plt.setp(bplot['caps'][2*box:2*(box+1)], color=cellTypeColours[ind])
            plt.setp(bplot['medians'][box], color='k', linewidth=3)
    
    plt.plot([-10,50], [0,0], 'k--')
    
    plt.xlim(-1,len(responseRates)*4-1)
    plt.ylim(-12,60)
    axScatter.set_xticks(range(1,len(responseRates)*4+1,4))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    plt.ylabel('High bandwidth \n' r'onset response ($\Delta$spk/s)', fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
#     yLims = np.array(plt.ylim())
#     extraplots.significance_stars([1,2], yLims[1]*0.95, yLims[1]*0.04, gapFactor=0.25)
    plt.hold(0)
#     axScatter.annotate(panelLabel, xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
#                      fontsize=fontSizePanel, fontweight='bold')
    
#     PVSOM = stats.ranksums(PVhighBandRate, SOMhighBandRate)[1]
#     print "Difference in PV-SOM high bandwidth sustained sound response p val: {}".format(PVSOM)


# Summary plot showing difference in Exc., PV, and SOM sustained sound response at high bandwidths
if PANELS[2]:
    #summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryFileName)
    
    PVtunedHighBandRate = summaryData['PVTunedSustainedResponses']-summaryData['PVtunedBaselines']
    PVtunedOffCentreHighBandRate = summaryData['PVTunedOffCentreSustainedResponses']-summaryData['PVtunedOffCentreBaselines']
    PVuntunedHighBandRate = summaryData['PVUntunedSustainedResponses']-summaryData['PVuntunedBaselines']
    
    SOMtunedHighBandRate = summaryData['SOMTunedSustainedResponses']-summaryData['SOMtunedBaselines']
    SOMtunedOffCentreHighBandRate = summaryData['SOMTunedOffCentreSustainedResponses']-summaryData['SOMtunedOffCentreBaselines']
    SOMuntunedHighBandRate = summaryData['SOMUntunedSustainedResponses']-summaryData['SOMuntunedBaselines']
    
    ExcTunedHighBandRate = summaryData['ExcTunedSustainedResponses']-summaryData['ExcTunedBaselines']
    ExcTunedOffCentreHighBandRate = summaryData['ExcTunedOffCentreSustainedResponses']-summaryData['ExcTunedOffCentreBaselines']
    ExcUntunedHighBandRate = summaryData['ExcUntunedSustainedResponses']-summaryData['ExcUntunedBaselines']
    
    PVresponseRates = [PVtunedHighBandRate, PVtunedOffCentreHighBandRate, PVuntunedHighBandRate]
    SOMresponseRates = [SOMtunedHighBandRate, SOMtunedOffCentreHighBandRate, SOMuntunedHighBandRate]
    ExcResponseRates = [ExcTunedHighBandRate, ExcTunedOffCentreHighBandRate, ExcUntunedHighBandRate]
    
    responseRates = [ExcResponseRates, PVresponseRates, SOMresponseRates]
    
    categoryLabels = ['tuned', 'tuned, off-centre', 'untuned']
    cellLabels = [r'PV$^+$', r'SOM$^+$', 'Exc.']
    
    cellTypeColours = [ExcColor, PVColor, SOMColor]
    
    panelLabel = 'C'
    
    axScatter = plt.subplot(gs[2,0])
    plt.hold(1)
    
    for ind, response in enumerate(responseRates):
        bplot = plt.boxplot(response, positions=np.array(xrange(len(response)))*4.0+ind, sym='', widths=0.6)
        
        #bplot = plt.boxplot(responseRates, widths=0.6, showfliers=False)
        
        for box in range(len(bplot['boxes'])):
            plt.setp(bplot['boxes'][box], color=cellTypeColours[ind], linewidth=2)
            plt.setp(bplot['whiskers'][2*box:2*(box+1)], linestyle='-', color=cellTypeColours[ind])
            plt.setp(bplot['caps'][2*box:2*(box+1)], color=cellTypeColours[ind])
            plt.setp(bplot['medians'][box], color='k', linewidth=3)
    
    plt.plot([-10,50], [0,0], 'k--')
    
    plt.xlim(-1,len(responseRates)*4-1)
    plt.ylim(-12,20)
    axScatter.set_xticks(range(1,len(responseRates)*4+1,4))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    plt.ylabel('High bandwidth \n' r'sustained response ($\Delta$spk/s)', fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
#     yLims = np.array(plt.ylim())
#     extraplots.significance_stars([1,2], yLims[1]*0.95, yLims[1]*0.04, gapFactor=0.25)
    plt.hold(0)
#     axScatter.annotate(panelLabel, xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
#                      fontsize=fontSizePanel, fontweight='bold')
    
#     PVSOM = stats.ranksums(PVhighBandRate, SOMhighBandRate)[1]
#     print "Difference in PV-SOM high bandwidth sustained sound response p val: {}".format(PVSOM)

    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)