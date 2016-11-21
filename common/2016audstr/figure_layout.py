'''
Template for making figures.

First, make the followin change to ~/.config/matplotlib/matplotlibrc
font.sans-serif     : Helvetica, Bitstream Vera Sans, Arial, sans-serif
'''

import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
#from jaratoolbox import figparams
import matplotlib.gridspec as gridspec

import matplotlib
matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To


PRINT_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'testfig' # Do not include extension
figFormat = 'svg' #'pdf'
figSize = [8,6]

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

labelPosX = [0.07, 0.65]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

amplitudeColor = cp.TangoPalette['ScarletRed1']
distanceColor = cp.TangoPalette['SkyBlue2']
velocityColor = cp.TangoPalette['Chameleon3']
markerSize = 8

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 3)
gs.update(left=0.15, right=0.85, wspace=1, hspace=0.5)

ax1 = plt.subplot(gs[0, :])
plt.plot(np.random.randn(20),np.random.randn(20),'o-',ms=markerSize, color='0.75',mfc=amplitudeColor,mec='w')
extraplots.boxoff(plt.gca())
plt.xlabel('Time (s)', fontsize=fontSizeLabels)
plt.ylabel('Amplitude (V)', fontsize=fontSizeLabels)
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')

ax2 = plt.subplot(gs[1,:-1])
plt.plot(np.random.randn(20),np.random.randn(20),'o-',ms=markerSize,color='0.75',mfc=distanceColor,mec='w')
extraplots.boxoff(plt.gca())
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.xlabel('Time (s)', fontsize=fontSizeLabels)
plt.ylabel('Distance (m)', fontsize=fontSizeLabels)
ax2.annotate('B', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

ax3 = plt.subplot(gs[1:, -1])
plt.plot(np.random.randn(20),np.random.randn(20),'o-',ms=markerSize,color='0.75',mfc=velocityColor,mec='w')
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.xlabel('Time (s)', fontsize=fontSizeLabels)
plt.ylabel('Velocity (m/s)', fontsize=fontSizeLabels)
xLims = [-2,2]
ax3.set_xlim(xLims)
ax3.set_xticks(np.arange(xLims[0],xLims[1]+1))
ax3.annotate('C', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()

if PRINT_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

