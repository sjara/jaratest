''' 
Show results of the model.

Parameters taken from Li et al (2014)
https://dx.doi.org/10.1523%2FJNEUROSCI.1516-14.2014

IPSC Amplitude in Exc from PV:
0 um : 157.4 pA
80 um: 11.56 pA
100um: 0 pA
NOTE: findsigma(80,11.56,0,157.4) results in a sigma of 35.0

IPSC Amplitude in Exc from SOM:
0 um : 50.8 pA
80 um: 30.9 pA
240um: 7.62 pA
400um: 0 pA
NOTE: findsigma(80,30.9,0,50.8) results in a sigma of 80.23
      findsigma(240,7.62,0,50.8) results in a sigma of 123.21

So Amp is 3x higher for PV
and StDev is 3x higher for SOM

Total IPSC Amplitude in Exc:
Activating PV : 442 pA 
Activating SOM: 128 pA


'''
import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors
#import matplotlib.patches as patches
#from mpl_toolkits.axes_grid1.inset_locator import inset_axes
#from scipy import ndimage

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
import studyparams
import model_suppression as suppmodel
reload(suppmodel)


FIGNAME = 'figure_model'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)


SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'Fig8_model' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
#figFormat = 'svg'
#figSize = [6.6, 6] # In inches
figSize = [10,6] # In inches


fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.01, 0.3, 0.64]   # Horiz position for panel labels
labelPosY = [0.96, 0.48]    # Vert position for panel labels

ExcColor = figparams.colp['excitatoryCell']
Exclight = matplotlib.colors.colorConverter.to_rgba(ExcColor, alpha=0.5)
PVcolor = figparams.colp['PVcell']
PVlight = matplotlib.colors.colorConverter.to_rgba(PVcolor, alpha=0.5)
SOMcolor = figparams.colp['SOMcell']
SOMlight = matplotlib.colors.colorConverter.to_rgba(SOMcolor, alpha=0.5)

# -- Simulate model --
nCells = 101
wParams = {'ampPV':-20, 'stdPV':10,
           'ampSOM':-20, 'stdSOM':30,
           'ampThal':100, 'stdThal':6}
#rfWidths = {'PV':5, 'SOM':5, 'Thal':5}
rfWidths = {'PV':10, 'SOM':10, 'Thal':10}
net = suppmodel.Network(nCells, wParams, rfWidths)
centerCellOutput,  bandwidths, condLabels = net.simulate_inactivation()
maxFiringRate = np.max(centerCellOutput[0,:])
bandwidthsNormed = bandwidths/float(wParams['stdSOM'])

# -- Plot resutls --
fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 3, width_ratios=[0.8,0.8,1.1], height_ratios=[1,1])
gs.update(top=0.96, left=0.07, right=0.95, bottom=0.11, wspace=0.5, hspace=0.3)

# -- Panel Cartoon --
axCartoon = plt.subplot(gs[0, 0:2])
axCartoon.set_axis_off()
axCartoon.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                   fontsize=fontSizePanel, fontweight='bold')

# -- Panel No PV --
lineWidth = 3
#xLims = [16,100]/stdSOM
xLims = [0.6,3.4]
#rangeToPlot = [10,100]
axNoPV = plt.subplot(gs[1, 0])
axNoPV.annotate('B', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
                fontsize=fontSizePanel, fontweight='bold')
plt.plot(bandwidthsNormed, centerCellOutput[0,:]/maxFiringRate, '-', lw=lineWidth, color=ExcColor)
plt.plot(bandwidthsNormed, centerCellOutput[1,:]/maxFiringRate, '--', lw=lineWidth, color=PVcolor)
plt.xlim(xLims)
plt.ylabel('Firing rate (normalized)')
plt.xlabel('Bandwidth ($\sigma_{SOM}$)')
plt.legend(['Control','No PV'], frameon=False, fontsize=fontSizeLegend)
extraplots.boxoff(axNoPV)

# -- Panel No PV --
axNoSOM = plt.subplot(gs[1, 1])
axNoSOM.annotate('C', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
                fontsize=fontSizePanel, fontweight='bold')
plt.plot(bandwidthsNormed, centerCellOutput[0,:]/maxFiringRate, '-', lw=lineWidth, color=ExcColor)
plt.plot(bandwidthsNormed, centerCellOutput[2,:]/maxFiringRate, '--', lw=lineWidth, color=SOMcolor)
plt.xlim(xLims)
plt.ylabel('Firing rate (normalized)')
plt.xlabel('Bandwidth ($\sigma_{SOM}$)')
plt.legend(['Control','No SOM'], frameon=False, fontsize=fontSizeLegend)
extraplots.boxoff(axNoSOM)


# -- Supp index and response change summaries --
responseChangeFile = os.path.join(dataDir,'response_change_summary.npz')
responseChangeData = np.load(responseChangeFile)
suppIndexVec = responseChangeData['suppIndexVec']
changeAtPeakVec = responseChangeData['changeAtPeakVec']
changeAtWNVec = responseChangeData['changeAtWNVec']
condLabels = responseChangeData['condLabels']

markerSize = 3

# -- Plot supp index --
axSuppIndex = plt.subplot(gs[0, 2:])
axSuppIndex.annotate('D', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
                   fontsize=fontSizePanel, fontweight='bold')
plt.plot(suppIndexVec[0],suppIndexVec[1],'s', color=PVcolor, mfc='none', ms=markerSize)
plt.plot(suppIndexVec[0],suppIndexVec[2],'o', color=SOMcolor, mfc='none', ms=markerSize)
xLims = [-0.1,1.1]
plt.xlim(xLims)
plt.ylim(xLims)
plt.plot(xLims,xLims,'--',color='0.5')
plt.xlabel('Suppression Index (control)')
plt.ylabel('Suppression Index (inactivation)')
#plt.axis('equal') # For older matplotlib
plt.axis('square')
extraplots.boxoff(axSuppIndex)

# -- Plot change in response --
axChange = plt.subplot(gs[1, 2:])
axChange.annotate('E', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
                   fontsize=fontSizePanel, fontweight='bold')
plt.plot(changeAtPeakVec[0,:],changeAtWNVec[0,:],'s', color=PVcolor, mfc='none', ms=markerSize)
plt.plot(changeAtPeakVec[1,:],changeAtWNVec[1,:],'o', color=SOMcolor, mfc='none', ms=markerSize)
xLims = [-50,2200]
plt.xlim(xLims)
plt.ylim(xLims)
plt.plot(xLims,xLims,'--',color='0.5')
plt.xlabel('Change in response to preferred bandwidth')
plt.ylabel('Change in response to WN')
#plt.axis('equal') # For older matplotlib
plt.axis('square')
extraplots.boxoff(axSuppIndex)

plt.show()


if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
