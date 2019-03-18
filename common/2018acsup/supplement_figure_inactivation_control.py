''' 
Create figure showing effect laser has on firing rate during regular and control trials (when tether not attached to probe).
'''
import os
import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import matplotlib.colors

from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)

import figparams
reload(figparams)



FIGNAME = 'supplement_figure_inhibitory_cell_inactivation_control'
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', FIGNAME)

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'inactivation_control' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [9,4] # In inches

PANELS = [1,1]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.33, 0.67]   # Horiz position for panel labels
labelPosY = [0.94]    # Vert position for panel labels

dataFileName = 'control_inactivated_cells_stats.npz'

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,3, width_ratios=[1,1.2,1.2])
gs.update(top=0.95, bottom=0.12, left=0.08, right=0.98, wspace=0.35, hspace=0.2)

dataFullPath = os.path.join(dataDir,dataFileName)
data = np.load(dataFullPath)

PVNoLaser = data['PVNoLaser']
PVLaser = data['PVLaser']
noPVChange = PVLaser - PVNoLaser

controlPVNoLaser = data['PVControlNoLaser']
controlPVLaser = data['PVControlLaser']
controlPVChange = controlPVLaser - controlPVNoLaser

SOMNoLaser = data['SOMNoLaser']
SOMLaser = data['SOMLaser']
noSOMChange = SOMLaser - SOMNoLaser

controlSOMNoLaser = data['SOMControlNoLaser']
controlSOMLaser = data['SOMControlLaser']
controlSOMChange = controlSOMLaser - controlSOMNoLaser

cellLabels = ['no PV', 'no SOM']

excColor = figparams.colp['excitatoryCell']
PVcolour = figparams.colp['PVcell']
SOMcolour = figparams.colp['SOMcell']

if PANELS[0]:
    panelLabel = 'a'
    
    axBar = plt.subplot(gs[0,0])

    controlData = [controlPVChange, controlSOMChange]
    laserData = [noPVChange, noSOMChange]
    
    plt.hold(True)
    ind = np.arange(2)
    width = 0.35
    controlMeans = [np.mean(controlData[0]), np.mean(controlData[1])]
    controlSEMs = [stats.sem(controlData[0]), stats.sem(controlData[1])]
    controlPlot = axBar.bar(ind, controlMeans, width, color='0.2', edgecolor='0.2')
    plt.errorbar(ind+width/2, controlMeans, yerr = [controlSEMs, controlSEMs], 
                     fmt='none', ecolor=excColor, lw=1.5, capsize=5)

    laserMeans = [np.mean(laserData[0]), np.mean(laserData[1])]
    laserSEMs = [stats.sem(laserData[0]), stats.sem(laserData[1])]
    laserPlot = axBar.bar(ind+width, laserMeans, width, edgecolor=[PVcolour,SOMcolour], color='none', linewidth=3)
    plt.errorbar(ind+3*width/2, laserMeans, yerr = [laserSEMs, laserSEMs], 
                     fmt='none', ecolor=PVcolour, lw=1.5, capsize=5)

    axBar.set_xticks(ind + width)
    axBar.set_xticklabels(cellLabels)

    extraplots.boxoff(axBar)
    
    axBar.legend((controlPlot, laserPlot), ('control', 'laser'),frameon=False, fontsize=fontSizeLabels) 
    plt.ylabel('Change in spontaneous firing rate')
    plt.xlim(-0.2,2)
    
    pNoPV = stats.ranksums(controlPVChange, noPVChange)[1]
    pNoSOM = stats.ranksums(controlSOMChange, noSOMChange)[1]
    
    print "Change in FR (control vs laser) p values:\nno PV: {0}\nno SOM: {1}".format(pNoPV,pNoSOM)
    
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([ind[0]+width/2,ind[0]+3*width/2], yLims[1]*0.93, yLims[1]*0.02, gapFactor=0.25)
    extraplots.significance_stars([ind[1]+width/2,ind[1]+3*width/2], yLims[1]*0.93, yLims[1]*0.02, gapFactor=0.25)
    
    axBar.annotate(panelLabel, xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
    
if PANELS[1]:
    panelLabels = ['b', 'c']
    cellTypeData = [[PVNoLaser, PVLaser], [SOMNoLaser, SOMLaser]]
    controlCellTypeData = [[controlPVNoLaser, controlPVLaser], [controlSOMNoLaser, controlSOMLaser]]
    cellTypeColours = [PVcolour, SOMcolour]
    
    for indType in range(2):
        axScatter = plt.subplot(gs[0,indType+1])
        
        laserData = cellTypeData[indType]
        controlData = controlCellTypeData[indType]
        
        plt.hold(True)
        l2, = plt.plot(laserData[0],laserData[1], 'o', color=cellTypeColours[indType], mec='none', ms=3)
        #plt.errorbar(SOMpeakChange, SOMWNChange, xerr = [[semSOMpeakChange, semSOMpeakChange]], yerr = [[semSOMWNChange, semSOMWNChange]], fmt='none', ecolor=SOMcolour, capsize=0, lw=2, zorder=9)
        l1, = plt.plot(controlData[0],controlData[1], 'o', color=excColor, mec='none', ms=3)
        #plt.errorbar(PVpeakChange, PVWNChange, xerr = [[semPVpeakChange, semPVpeakChange]], yerr = [[semPVWNChange, semPVWNChange]], fmt='none', ecolor=PVcolour, capsize=0, lw=2, zorder=10)    
        plt.xlabel('Spontaneous firing rate (spk/s)',fontsize=fontSizeLabels)
        plt.ylabel('Laser spontaneous firing rate (spk/s)',fontsize=fontSizeLabels)
    
        plt.legend([l1,l2], ['control', cellLabels[indType]], loc='upper left', fontsize=fontSizeLabels, numpoints=1, handlelength=0.3)
        plt.plot([-20,100],[-20,100], 'k--')
        plt.xlim(-2,45)
        plt.ylim(-2,55)
     
        extraplots.boxoff(axScatter)
        
        axScatter.annotate(panelLabels[indType], xy=(labelPosX[indType+1],labelPosY[0]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)