''' 
Create figure showing various controls done to test the effect observed for SI, including:
* preferred frequency
* AM rate
* intensity tuning
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

import figparams
import studyparams

FREQFIGNAME = 'supplement_figure_gaussian_frequency_tuning_fit'
freqDataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FREQFIGNAME)

AMFIGNAME = 'supplement_figure_characterisation_of_responses_by_AM_rate'
AMDataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, AMFIGNAME)

INTFIGNAME = 'supplement_figure_intensity_tuning'
intDataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, INTFIGNAME)

PANELS = [1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'Fig4_characterisation_controls' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [6,9] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

ExColor = figparams.colp['excitatoryCell']
PVColor = figparams.colp['PVcell']
SOMColor = figparams.colp['SOMcell']

labelPosX = 0.01   # Horiz position for panel labels
labelPosY = [0.97, 0.69, 0.34]    # Vert position for panel labels

ExampleFileName = 'example_frequency_tuning_band016_2016-12-11_950um_T6_c6.npz'
freqFileName = 'all_photoidentified_cells_stats_by_best_freq.npz'
AMFileName = 'all_photoidentified_cells_stats_by_AM_rate.npz'
intFileName = 'all_cells_intensity_tuning.npz'

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(3, 1, height_ratios=[0.7,1,1])
gs.update(top=0.96, bottom=0.08, left=0.1, right=0.96, wspace=0.3, hspace=0.4)

# --- suppression indices for cells of different preferred frequencies ---
if PANELS[0]:
    dataFullPath = os.path.join(freqDataDir,freqFileName)
    data = np.load(dataFullPath)
    
    exampleDataFullPath = os.path.join(freqDataDir, ExampleFileName)
    exampleData = np.load(exampleDataFullPath)
    
    panelLabel = 'A'
    
    ExbestFreq = np.log2(data['ExbestFreq'])
    PVbestFreq = np.log2(data['PVbestFreq'])
    SOMbestFreq = np.log2(data['SOMbestFreq'])
    
    ExSI = data['fitExcSustainedSuppressionInd']
    PVSI = data['fitPVsustainedSuppressionInd']
    SOMSI = data['fitSOMsustainedSuppressionInd']
    
    possibleFreqs = exampleData['possibleFreqs']
    
    logFreqs = np.log2(possibleFreqs)
    
    cellTypeLabels = ['Exc.', r'PV$^+$', r'SOM$^+$']
    
    cellFreqs = [ExbestFreq, PVbestFreq, SOMbestFreq]
    cellSIs = [ExSI, PVSI, SOMSI]
    cellTypeColours = [ExColor, PVColor, SOMColor]
    
    axScatter = gs[0,0]
    
    inner = gridspec.GridSpecFromSubplotSpec(1, len(cellFreqs), subplot_spec=axScatter, wspace=0.1, hspace=0.3)
    
    for cellType in range(len(cellFreqs)):
        thisAx = plt.subplot(inner[cellType])
        plt.plot(cellFreqs[cellType],cellSIs[cellType], 'o', mfc=cellTypeColours[cellType], mec=cellTypeColours[cellType], ms=4, zorder=cellType)
    
        # -- compute and plot linear regression between SI and noise SI
        slope, intercept, rVal, pVal, stdErr = stats.linregress(cellFreqs[cellType], cellSIs[cellType])
        xvals = np.linspace(10,16,200)
        yvals = slope*xvals + intercept
        plt.plot(xvals, yvals, '-', color=cellTypeColours[cellType], zorder=-1)
        
        print "SI vs Pref freq"
        print "Linear regression over {0} cells: \ncorrelation coefficient (r): {1}\np Value: {2}".format(cellTypeLabels[cellType],rVal,pVal)
        
    
#         labels = ['%.1f' % f for f in possibleFreqs/1000]
#         labels[1::4] = ['']*len(labels[1::4])
#         labels[2::4] = ['']*len(labels[2::4])
#         labels[3::4] = ['']*len(labels[2::4])
#         thisAx.set_xticks(np.log2(possibleFreqs))
#         thisAx.set_xticklabels(labels)
        plt.locator_params(axis='x', nbins=6)
        labels = ['%.1f' % freq for freq in (2**plt.xticks()[0])/1000]
        thisAx.set_xticks(plt.xticks()[0])
        thisAx.set_xticklabels(labels)
        print labels
        print plt.xticks()
        
        plt.xlim(11.5,15.5)
        plt.ylim(-0.1, 1.1)
        plt.title("{} cells".format(cellTypeLabels[cellType]), color=cellTypeColours[cellType], fontsize=fontSizeLabels)
        if cellType == 0:
            plt.ylabel('Suppression Index',fontsize=fontSizeLabels)
        else:
            thisAx.set_yticklabels([''])
        if cellType == 1:
            plt.xlabel('Preferred frequency (kHz)',fontsize=fontSizeLabels)
        extraplots.boxoff(thisAx)
        
    thisAx.annotate(panelLabel, xy=(labelPosX,labelPosY[0]), xycoords='figure fraction',
                      fontsize=fontSizePanel, fontweight='bold')
    
    # --- plots of suppression index vs AM rate ---    
if PANELS[1]:
    dataFullPath = os.path.join(AMDataDir,AMFileName)
    data = np.load(dataFullPath)
    
    axScatter = plt.subplot(gs[1,0])
    
    panelLabel = 'B'

    ExAMrate = data['ExAMrate']
    PVAMrate = data['PVAMrate']
    SOMAMrate = data['SOMAMrate']
    
    ExSI = data['fitExcSustainedSuppressionInd']
    PVSI = data['fitPVsustainedSuppressionInd']
    SOMSI = data['fitSOMsustainedSuppressionInd']
    
    cellRates = [ExAMrate, PVAMrate, SOMAMrate]
    cellSIs = [ExSI, PVSI, SOMSI]
    cellTypeColours = [ExColor, PVColor, SOMColor]
    
    bar_width = 0.15
    bar_spacing = 0.13
    bar_loc = [-1,0,1]
    
    xticks = []
    xticklabels = []
    
    for cellType in range(len(cellRates)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[cellType], alpha=0.5)
        thisCellTypeSIs = cellSIs[cellType]
        thisCellTypeAMrates = cellRates[cellType]
        
        SIs16 = thisCellTypeSIs[np.where(thisCellTypeAMrates<=16)[0]]
        SIs32 = thisCellTypeSIs[np.where(thisCellTypeAMrates==32)[0]]
        SIs64 = thisCellTypeSIs[np.where(thisCellTypeAMrates==64)[0]]
        
        allSIs = []
        for indSI, SIs in enumerate([SIs16, SIs32, SIs64]):
            if len(SIs)>0:
                allSIs.append(SIs)
                if indSI==0:
                    xticklabels.append(r'$\leq$16')
                else:
                    xticklabels.append(16*(2**indSI))
                
        print "SI p-val:{}".format(stats.kruskal(*allSIs))
            
        for indSI, SIs in enumerate(allSIs):    
            xval = (cellType+1)+(bar_loc[indSI]*(bar_width+bar_spacing))
            xticks.append(xval)
            xvals = xval*np.ones(len(SIs))
              
            jitterAmt = np.random.random(len(xvals))
            xvals = xvals + (bar_width * jitterAmt) - bar_width/2
              
            plt.hold(True)
            plt.plot(xvals, SIs, 'o', mec=edgeColour, mfc='none', clip_on=False, markeredgewidth=1.3)
            median = np.median(SIs)
            plt.plot([xval-bar_width/2,xval+bar_width/2], [median,median], '-', color='k', mec=edgeColour, lw=3)
            
    ExPatch = mpatches.Patch(color=ExColor, label='Exc.')
    PVPatch = mpatches.Patch(color=PVColor, label=r'PV$^+$')
    SOMPatch = mpatches.Patch(color=SOMColor, label=r'SOM$^+$')
    plt.legend(handles=[ExPatch,PVPatch,SOMPatch],frameon=False, fontsize=fontSizeLabels, loc='best')
    
    plt.ylim(-0.1,1.1)
    plt.xlim(xticks[0]-bar_width, xticks[-1]+bar_width)
    plt.ylabel('Suppression Index')
    plt.xlabel('AM rate (Hz)')
    axScatter.set_xticks(xticks)
    axScatter.set_xticklabels(xticklabels)
    extraplots.boxoff(axScatter)
    
    axScatter.annotate(panelLabel, xy=(labelPosX,labelPosY[1]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
    
# --- SI vs diff/sum response at pure tone ---
if PANELS[2]:
    panelLabel = 'C'
    
    dataFullPath = os.path.join(intDataDir,intFileName)
    data = np.load(dataFullPath)
    
    ExcSI = data['fitExsustainedSuppressionNoZero']
    ExcDiffSumTone = np.vstack(data['ExdiffSum'])[:,0]
    ExcDiffSumNoise = np.vstack(data['ExdiffSum'])[:,-1]
    
    # some of the excitatory cells don't have data at two intensities
    notNanInds = np.where(~np.isnan(ExcDiffSumNoise))
    ExcSI = ExcSI[notNanInds]
    ExcDiffSumTone = ExcDiffSumTone[notNanInds]
    ExcDiffSumNoise = ExcDiffSumNoise[notNanInds]
    
    diffSums = [ExcDiffSumTone, ExcDiffSumNoise]
    labels = ['pure tone', 'white noise']
    
    axScatter = gs[2,0]
    inner = gridspec.GridSpecFromSubplotSpec(1, len(diffSums), subplot_spec=axScatter, wspace=0.1, hspace=0.3)
    
    # -- plot excitatory cells --
    for ind, diffsum in enumerate(diffSums):
        thisAx = plt.subplot(inner[ind])
    
        plt.plot(diffsum,ExcSI, 'o', mec=ExColor, mfc=ExColor, ms=4)
        
        # -- compute and plot linear regression between SI and noise SI
        slope, intercept, rVal, pVal, stdErr = stats.linregress(diffsum, ExcSI)
        
        xvals = np.linspace(-1,1,200)
        yvals = slope*xvals + intercept
        plt.plot(xvals, yvals, 'k--')
        
        print "SI vs {}".format(labels[ind])
        print "Linear regression over all cells: \ncorrelation coefficient (r): {0}\np Value: {1}".format(rVal,pVal)
        
        if ind == 0:
            plt.ylabel('Suppression Index',fontsize=fontSizeLabels)
        else:
            thisAx.set_yticklabels([''])
         
        plt.xlabel('Intensity index ({})'.format(labels[ind]), fontsize=fontSizeLabels)
        
        plt.xlim(-1.1,1.1)
        plt.ylim(-0.1,1.1)
    
        extraplots.boxoff(thisAx)
        
    thisAx.annotate(panelLabel, xy=(labelPosX,labelPosY[2]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)