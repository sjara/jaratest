import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors
import matplotlib.patches as patches

from scipy import ndimage
from scipy import stats

from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import extraplots

import studyparams
import figparams

FIGNAME = 'supplement_figure_histology'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'SuppFig1_histology' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [6,3] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

excColor = figparams.colp['excitatoryCell']

labelPosX = [0.01, 0.48]   # Horiz position for panel labels
labelPosY = 0.94    # Vert position for panel labels

histFileName = 'band055_outlines.jpg'
#histFileName = 'band004_p1-C5-02_tracks.jpg'

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,2, width_ratios=[1,0.9])
gs.update(top=0.95, bottom=0.21, left=0.04, right=0.95, wspace=0.3, hspace=0.2)

if PANELS[0]:
    panelLabel = 'a'
    
    histFullPath = os.path.join(dataDir, histFileName)
    histImage = ndimage.imread(histFullPath)
    
    imageBounds = [400, 800, 0, 400] #for band055
    #imageBounds = [300, 700, 988, 1388] #for band004
    
    axImage = plt.subplot(gs[0,0])
    plt.imshow(histImage[imageBounds[0]:imageBounds[1],imageBounds[2]:imageBounds[3],:])
    plt.axis('off')
    
    axImage.annotate(panelLabel, xy=(labelPosX[0],labelPosY), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
    
    axImage.annotate('AUDp', xy=(0.65,0.35), xycoords='axes fraction', fontsize=fontSizeLabels, color='w')
    axImage.annotate('AUDpo', xy=(0.7,0.75), xycoords='axes fraction', fontsize=fontSizeLabels, color='w')
    axImage.annotate('AUDv', xy=(0.5,0.05), xycoords='axes fraction', fontsize=fontSizeLabels, color='w')
    
if PANELS[1]:
    panelLabel = 'b'
    
    dbFilename = '/home/jarauser/data/database/photoidentification_cells2.h5'
    db = celldatabase.load_hdf(dbFilename)
    
    cellsWithDepths = db[db['cortexRatioDepth'].notnull()]
    EXC_CELLS = cellsWithDepths.query('(laserPVal>{} or laserUStat<0) and spikeWidth>{} and subject=={}'.format(studyparams.EXC_LASER_RESPONSE_PVAL,studyparams.EXC_SPIKE_WIDTH,studyparams.SOM_CHR2_MICE))
    
    depths = EXC_CELLS['cortexRatioDepth']
    SIs = EXC_CELLS['fitSustainedSuppressionIndexNoZeroHighAmp']
    
    slope, intercept, rVal, pVal, stdErr = stats.linregress(depths, SIs)
            
    print "SI vs cortical depth linear regression: \ncorrelation coefficient (r): {}\np Value: {}".format(rVal,pVal)
    
    axScatter = plt.subplot(gs[0,1])

    plt.hold(True)
    plt.plot(depths, SIs, 'o', color=excColor)
    xvals = np.linspace(-2,2,200)
    yvals = slope*xvals + intercept
    plt.plot(xvals, yvals, '--', color=excColor, zorder=-1)
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)
    plt.xlabel('Depth from pia \n(fraction cortical width)', fontsize = fontSizeLabels)
    plt.ylabel('Suppression Index', fontsize = fontSizeLabels)
    
    extraplots.boxoff(axScatter)
    
    axScatter.annotate(panelLabel, xy=(labelPosX[1],labelPosY), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
    
    
    