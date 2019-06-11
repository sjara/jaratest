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
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
#dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', FIGNAME)

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'SuppFig8_inactivation_control' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [10,3] # In inches

PANELS = [1,1]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.01, 0.31, 0.67]   # Horiz position for panel labels
labelPosY = [0.94]    # Vert position for panel labels

dataFileName = 'control_inactivated_cells_stats.npz'

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,3, width_ratios=[1,1.3,1.3])
gs.update(top=0.94, bottom=0.15, left=0.08, right=0.98, wspace=0.45, hspace=0.2)

dataFullPath = os.path.join(dataDir,dataFileName)
data = np.load(dataFullPath)

PVNoLaser = data['PVNoLaser']
PVLaser = data['PVLaser']
noPVChange = 100.0*(PVLaser-PVNoLaser)/PVNoLaser

# normalisation fails in some cases due to control firing rate being 0
notNanInds = np.where(np.isfinite(noPVChange))
noPVChange = noPVChange[notNanInds]

controlPVNoLaser = data['PVControlNoLaser']
controlPVLaser = data['PVControlLaser']
controlPVChange = 100.0*(controlPVLaser-controlPVNoLaser)/controlPVNoLaser

SOMNoLaser = data['SOMNoLaser']
SOMLaser = data['SOMLaser']
noSOMChange = 100.0*(SOMLaser-SOMNoLaser)/SOMNoLaser

# normalisation fails in some cases due to control firing rate being 0
notNanInds = np.where(np.isfinite(noSOMChange))
noSOMChange = noSOMChange[notNanInds]

controlSOMNoLaser = data['SOMControlNoLaser']
controlSOMLaser = data['SOMControlLaser']
controlSOMChange = 100.0*(controlSOMLaser-controlSOMNoLaser)/controlSOMNoLaser

excColor = figparams.colp['excitatoryCell']
PVcolour = figparams.colp['PVcell']
SOMcolour = figparams.colp['SOMcell']

if PANELS[0]:
    panelLabel = 'a'
    
    cellLabels = ['PV-ArchT', 'SOM-ArchT']
    
    axBar = plt.subplot(gs[0,0])

    controlData = [controlPVChange, controlSOMChange]
    laserData = [noPVChange, noSOMChange]
    
    plt.hold(True)
    ind = np.arange(2)
    width = 0.35
    controlMeans = [np.mean(controlData[0]), np.mean(controlData[1])]
    controlSEMs = [stats.sem(controlData[0]), stats.sem(controlData[1])]
    axBar.bar(ind, controlMeans, width, color='none', edgecolor=excColor,linewidth=3)
    plt.errorbar(ind+width/2, controlMeans, yerr = [controlSEMs, controlSEMs], 
                     fmt='none', ecolor=excColor, lw=1.5, capsize=5)

    laserMeans = [np.mean(laserData[0]), np.mean(laserData[1])]
    laserSEMs = [stats.sem(laserData[0]), stats.sem(laserData[1])]
    axBar.bar(ind+width, laserMeans, width, edgecolor=[PVcolour,SOMcolour], color='none', linewidth=3)
    plt.errorbar(ind[0]+3*width/2, laserMeans[0], yerr = [laserSEMs[0]], 
                     fmt='none', ecolor=PVcolour, lw=1.5, capsize=5)
    plt.errorbar(ind[1]+3*width/2, laserMeans[1], yerr = [laserSEMs[1]], 
                     fmt='none', ecolor=SOMcolour, lw=1.5, capsize=5)

    axBar.set_xticks(ind + width)
    axBar.set_xticklabels(cellLabels)#, rotation=-45)

    extraplots.boxoff(axBar)
    
    # manually make the legend!
    legendXY = [0.9, 170]
    
    #box = patches.Rectangle((legendXY[0], legendXY[1]), 1.2, 25, fill=False, clip_on=False)
    ExcPatch = patches.Rectangle((legendXY[0]+0.1, legendXY[1]+18), 0.33, 8, facecolor='none', edgecolor=excColor, linewidth=3)
    PVpatch = patches.Rectangle((legendXY[0]+0.1, legendXY[1]), 0.15, 8, facecolor='none', edgecolor=PVcolour, linewidth=3)
    SOMpatch = patches.Rectangle((legendXY[0]+0.29, legendXY[1]), 0.15, 8, facecolor='none', edgecolor=SOMcolour, linewidth=3)
    #axBar.add_patch(box)
    axBar.add_patch(ExcPatch)
    axBar.add_patch(PVpatch)
    axBar.add_patch(SOMpatch)
    axBar.annotate('control', (legendXY[0]+0.6, legendXY[1]+18), fontsize=fontSizeLabels)
    axBar.annotate('laser', (legendXY[0]+0.6, legendXY[1]), fontsize=fontSizeLabels)
    
    plt.plot([-5,5],[0,0], 'k-', zorder=-10)
    plt.ylabel('Percentage change in \nspontaneous firing rate')
    plt.ylim(-20,210)
    plt.xlim(-0.1,1.8)
    
    pNoPV = stats.ranksums(controlPVChange, noPVChange)[1]
    pNoSOM = stats.ranksums(controlSOMChange, noSOMChange)[1]
    
    print "Change in FR (control vs laser) p values:\nno PV: {0}\nno SOM: {1}".format(pNoPV,pNoSOM)
    
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([ind[0]+width/2,ind[0]+3*width/2], yLims[1]*0.94, yLims[1]*0.02, gapFactor=0.25)
    extraplots.significance_stars([ind[1]+width/2,ind[1]+3*width/2], yLims[1]*0.55, yLims[1]*0.02, gapFactor=0.25)
    
    axBar.annotate(panelLabel, xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
    
if PANELS[1]:
    panelLabels = ['b', 'c']
    cellLabels = ['no PV+', 'no SOM+']
    
    cellTypeData = [[PVNoLaser, PVLaser], [SOMNoLaser, SOMLaser]]
    controlCellTypeData = [[controlPVNoLaser, controlPVLaser], [controlSOMNoLaser, controlSOMLaser]]
    cellTypeColours = [PVcolour, SOMcolour]
    
    for indType in range(2):
        axScatter = plt.subplot(gs[0,indType+1])
        
        laserData = cellTypeData[indType]
        controlData = controlCellTypeData[indType]
        
        plt.hold(True)
        plt.scatter(laserData[0],laserData[1], edgecolors=cellTypeColours[indType], facecolors='none', s=15, label=cellLabels[indType])
        plt.scatter(controlData[0],controlData[1], edgecolors=excColor, facecolors=excColor, s=15, label='control')
        
        #l2, = plt.plot(laserData[0],laserData[1], 'o', color=cellTypeColours[indType], mec='none', ms=3)
        #plt.errorbar(SOMpeakChange, SOMWNChange, xerr = [[semSOMpeakChange, semSOMpeakChange]], yerr = [[semSOMWNChange, semSOMWNChange]], fmt='none', ecolor=SOMcolour, capsize=0, lw=2, zorder=9)
        #l1, = plt.plot(controlData[0],controlData[1], 'o', color=excColor, mec='none', ms=3)
        #plt.errorbar(PVpeakChange, PVWNChange, xerr = [[semPVpeakChange, semPVpeakChange]], yerr = [[semPVWNChange, semPVWNChange]], fmt='none', ecolor=PVcolour, capsize=0, lw=2, zorder=10)    
        plt.xlabel('Spontaneous firing rate (spk/s)',fontsize=fontSizeLabels)
        plt.ylabel('Laser-evoked firing rate (spk/s)',fontsize=fontSizeLabels)
    
        plt.legend(scatterpoints=1, loc='upper left', fontsize=fontSizeLegend, numpoints=1, handlelength=0.3, markerscale=1.5)
#         plt.plot([-20,100],[-20,100], 'k--')
#         plt.xlim(-2,45)
#         plt.ylim(-2,55)

        axScatter.set_xscale('log', basex=10)
        axScatter.set_yscale('log', basex=10)
        
        plt.plot([-5,100], [-5,100], 'k--')
        plt.xlim(0.05,100)
        plt.ylim(0.05,100)
        axScatter.tick_params(top=False, right=False, which='both')
        
        ticks=[0.1,1,10,100]
        
        axScatter.set_xticks(ticks)
        axScatter.set_xticklabels(ticks)
        axScatter.set_yticks(ticks)
        axScatter.set_yticklabels(ticks)
     
        extraplots.boxoff(axScatter)
        axScatter.set(adjustable='box-forced', aspect='equal')
        
        axScatter.annotate(panelLabels[indType], xy=(labelPosX[indType+1],labelPosY[0]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
        
        pControl = stats.wilcoxon(controlData[0],controlData[1])[1]
        pLaser = stats.wilcoxon(laserData[0],laserData[1])[1]
    
        print "Change in FR for {0} p values:\ncontrol: {1}\nlaser: {2}".format(cellLabels[indType],pControl,pLaser)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)