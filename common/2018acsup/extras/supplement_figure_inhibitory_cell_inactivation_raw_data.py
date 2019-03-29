import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors
import matplotlib.patches as patches

from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)

import figparams
reload(figparams)


FIGNAME = 'figure_inhibitory_cell_inactivation'
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'figure_inhibitory_cell_inactivation')
dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', 'figure_inhibitory_cell_inactivation') #using data generated for main figure

PANELS = [1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'effect_of_inhibitory_inactivation_on_suppression_raw_data' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [8,4] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.5]   # Horiz position for panel labels
labelPosY = [0.96]    # Vert position for panel labels


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,2)
gs.update(top=0.95, bottom=0.18, left=0.1, right=0.95, wspace=0.5, hspace=0.2)

summaryFileName = 'all_inactivated_cells_stats.npz'

if PANELS[0]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVsustainedSuppressionNoLaser = summaryData['rawPVsustainedSuppressionNoLaser']
    PVsustainedSuppressionLaser = summaryData['rawPVsustainedSuppressionLaser']
    
    SOMsustainedSuppressionNoLaser = summaryData['rawSOMsustainedSuppressionNoLaser']
    SOMsustainedSuppressionLaser = summaryData['rawSOMsustainedSuppressionLaser']

    PVsupNoLaser = summaryData['rawMeanPVsupNoLaser']
    PVsupLaser = summaryData['rawMeanPVsupLaser']
    
    semPVsupNoLaser = summaryData['rawSemPVsupNoLaser']
    semPVsupLaser = summaryData['rawSemPVsupLaser']
    
    SOMsupNoLaser = summaryData['rawMeanSOMsupNoLaser']
    SOMsupLaser = summaryData['rawMeanSOMsupLaser']
    
    semSOMsupNoLaser = summaryData['rawSemSOMsupNoLaser']
    semSOMsupLaser = summaryData['rawSemSOMsupLaser']
    
    panelLabel = 'a'
    
    cellLabels = ['no PV', 'no SOM']
    
    PVcolour = figparams.colp['PVcell']
    SOMcolour = figparams.colp['SOMcell']
    cellTypeColours = [PVcolour, SOMcolour]
    
    axScatter = plt.subplot(gs[0,0])
    
    plt.hold(True)
    plt.plot([-2,2],[-2,2], 'k--')
    l2, = plt.plot(SOMsustainedSuppressionNoLaser,SOMsustainedSuppressionLaser, 'o', color=SOMcolour, mec='none', ms=4)
    plt.errorbar(SOMsupNoLaser, SOMsupLaser, xerr = [[semSOMsupNoLaser, semSOMsupNoLaser]], yerr = [[semSOMsupLaser, semSOMsupLaser]], fmt='none', ecolor=SOMcolour, capsize=0, lw=2)
    l1, = plt.plot(PVsustainedSuppressionNoLaser,PVsustainedSuppressionLaser, 'o', color=PVcolour, mec='none', ms=4)
    plt.errorbar(PVsupNoLaser, PVsupLaser, xerr = [[semPVsupNoLaser, semPVsupNoLaser]], yerr = [[semPVsupLaser, semPVsupLaser]], fmt='none', ecolor=PVcolour, capsize=0, lw=2)
    plt.ylabel('Suppression Index (laser)',fontsize=fontSizeLabels)
    plt.xlabel('Suppression Index (control)',fontsize=fontSizeLabels)
    plt.xlim(-0.1,1.1)
    plt.ylim(-0.1,1.1)

    plt.legend([l1,l2], ['No PV', 'No SOM'], loc='best', fontsize=fontSizeLabels, numpoints=1, handlelength=0.3)

    extraplots.boxoff(axScatter)

    plt.ylabel('Change in suppression index',fontsize=fontSizeLabels)
    axScatter.annotate(panelLabel, xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    
if PANELS[1]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVpeakChangeFR = summaryData['rawPVpeakChangeFR']
    PVWNChangeFR = summaryData['rawPVWNChangeFR']
    
    SOMpeakChangeFR = summaryData['rawSOMpeakChangeFR']
    SOMWNChangeFR = summaryData['rawSOMWNChangeFR']
    
    PVpeakChange = summaryData['rawMeanPVpeakChange']
    PVWNChange = summaryData['rawMeanPVWNChange']
    
    semPVpeakChange = summaryData['rawSemPVpeakChange']
    semPVWNChange = summaryData['rawSemPVWNChange']
    
    SOMpeakChange = summaryData['rawMeanSOMpeakChange']
    SOMWNChange = summaryData['rawMeanSOMWNChange']
    
    semSOMpeakChange = summaryData['rawSemSOMpeakChange']
    semSOMWNChange = summaryData['rawSemSOMWNChange']
    
    panelLabel = 'b'
    
    PVcolour = figparams.colp['PVcell']
    SOMcolour = figparams.colp['SOMcell']
    cellTypeColours = [PVcolour, SOMcolour]
    
    axScatter = plt.subplot(gs[0,1])
    
    plt.hold(True)
    plt.plot([-20,30],[-20,30], 'k--')
    l2, = plt.plot(SOMpeakChangeFR,SOMWNChangeFR, 'o', color=SOMcolour, mec='none', ms=4)
    plt.errorbar(SOMpeakChange, SOMWNChange, xerr = [[semSOMpeakChange, semSOMpeakChange]], yerr = [[semSOMWNChange, semSOMWNChange]], fmt='none', ecolor=SOMcolour, capsize=0, lw=2, zorder=9)
    l1, = plt.plot(PVpeakChangeFR,PVWNChangeFR, 'o', color=PVcolour, mec='none', ms=4)
    plt.errorbar(PVpeakChange, PVWNChange, xerr = [[semPVpeakChange, semPVpeakChange]], yerr = [[semPVWNChange, semPVWNChange]], fmt='none', ecolor=PVcolour, capsize=0, lw=2, zorder=10)    
    plt.ylabel('Change in response to WN (spk/s)',fontsize=fontSizeLabels)
    plt.xlabel('Change in response to \n preferred bandwidth (spk/s)',fontsize=fontSizeLabels)
    plt.xlim(-5,10)
    plt.ylim(-5,10)
#     plt.xlim(-10,22)
#     plt.ylim(-10,22)
    plt.legend([l1,l2], ['No PV', 'No SOM'], loc='best', fontsize=fontSizeLabels, numpoints=1, handlelength=0.3)
    axScatter.annotate(panelLabel, xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    extraplots.boxoff(axScatter)
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)