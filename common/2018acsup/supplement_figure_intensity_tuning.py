''' 
Create figure showing intensity tuning at different bandwidths
'''
import os
import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)

import figparams
reload(figparams)



FIGNAME = 'supplement_figure_intensity_tuning'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'SuppFig4_intensity_tuning' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [6,3] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

PVcolour = figparams.colp['PVcell']
SOMcolour = figparams.colp['SOMcell']
ExcColour = figparams.colp['excitatoryCell']

labelPosX = [0.01, 0.49]   # Horiz position for panel labels
labelPosY = [0.94]    # Vert position for panel labels

dataFileName = 'all_cells_intensity_tuning.npz'

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,2)
gs.update(top=0.92, bottom=0.17, left=0.1, right=0.98, wspace=0.3, hspace=0.3)

plt.hold(True)

# --- SI vs diff/sum response at pure tone ---
if PANELS[0]:
    panelLabel = 'a'
    
    dataFullPath = os.path.join(dataDir,dataFileName)
    data = np.load(dataFullPath)
    
    ExcSI = data['fitExsustainedSuppressionNoZero']
    ExcDiffSum = np.vstack(data['ExdiffSum'])[:,0]
    
    # some of the excitatory cells don't have data at two intensities
    notNanInds = np.where(~np.isnan(ExcDiffSum))
    ExcSI = ExcSI[notNanInds]
    ExcDiffSum = ExcDiffSum[notNanInds]
    
    
    ALPHA_VAL = 0.05
    
    # -- plot excitatory cells --
    axScatter = plt.subplot(gs[0,0])

    plt.plot(ExcDiffSum,ExcSI, 'o', mec=ExcColour, mfc=ExcColour, ms=4)
    
    # -- compute and plot linear regression between SI and noise SI
    slope, intercept, rVal, pVal, stdErr = stats.linregress(ExcDiffSum, ExcSI)
    
    xvals = np.linspace(-1,1,200)
    yvals = slope*xvals + intercept
    plt.plot(xvals, yvals, 'k--')
    
    print "SI vs Pure Tone"
    print "Linear regression over all cells: \ncorrelation coefficient (r): {0}\np Value: {1}".format(rVal,pVal)
        
    plt.xlabel('Intensity index (pure tone)')
    plt.ylabel('SI')
    
    plt.xlim(-1.1,1.1)
    plt.ylim(-0.1,1.1)

    axScatter.annotate(panelLabel, xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    extraplots.boxoff(axScatter)
    
    
# --- SI vs intensity tuning for all cells ---
if PANELS[1]:
    panelLabel = 'b'
    
    dataFullPath = os.path.join(dataDir,dataFileName)
    data = np.load(dataFullPath)
    
    ExcSI = data['fitExsustainedSuppressionNoZero']
    ExcDiffSum = np.vstack(data['ExdiffSum'])[:,-1]
    
    # some of the excitatory cells don't have data at two intensities
    notNanInds = np.where(~np.isnan(ExcDiffSum))
    ExcSI = ExcSI[notNanInds]
    ExcDiffSum = ExcDiffSum[notNanInds]
    
    
    ALPHA_VAL = 0.05
    
    # -- plot excitatory cells --
    
    axScatter = plt.subplot(gs[0,1])

    plt.plot(ExcDiffSum, ExcSI, 'o', mec=ExcColour, mfc=ExcColour, ms=4)
    
    # -- compute and plot linear regression between SI and noise SI
    slope, intercept, rVal, pVal, stdErr = stats.linregress(ExcDiffSum, ExcSI)
    
    xvals = np.linspace(-1,1,200)
    yvals = slope*xvals + intercept
    plt.plot(xvals, yvals, 'k--')
    
    print "SI vs White Noise"
    print "Linear regression over all cells: \ncorrelation coefficient (r): {0}\np Value: {1}".format(rVal,pVal)
        
    plt.xlabel('Intensity index (white noise)')
    plt.ylabel('SI')
    
    plt.xlim(-1.1,1.1)
    plt.ylim(-0.1,1.1)
        
    axScatter.annotate(panelLabel, xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    extraplots.boxoff(axScatter)
    
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
        
    