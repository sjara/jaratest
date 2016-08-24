'''
Testing what is necessary to make pretty figures for papers.

Changes to ~/.config/matplotlib/matplotlibrc
font.sans-serif     : Helvetica, Bitstream Vera Sans, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif

Do the SVG font thing.
rc(font=''font.sans-serif' = 'Helvetica'
#rcParams['font.family']='monospace'

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

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

labelPosX = [0.07, 0.65]  # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

plt.clf()

gs = gridspec.GridSpec(2, 3)
gs.update(left=0.15, right=0.85, wspace=1, hspace=0.5)

ax1 = plt.subplot(gs[0, :])
plt.plot(np.random.randn(20),np.random.randn(20),'o',mfc='none')
extraplots.boxoff(plt.gca())
plt.xlabel('Time (s)', fontsize=fontSizeLabels)
plt.ylabel('Amplitude (V)', fontsize=fontSizeLabels)
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')

ax2 = plt.subplot(gs[1,:-1])
plt.plot(np.random.randn(20),np.random.randn(20),'o',mfc='none')
extraplots.boxoff(plt.gca())
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.xlabel('Time (s)', fontsize=fontSizeLabels)
plt.ylabel('Amplitude (V)', fontsize=fontSizeLabels)
ax2.annotate('B', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

ax3 = plt.subplot(gs[1:, -1])
plt.plot(np.random.randn(20),np.random.randn(20),'o',mfc='none')
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.xlabel('Time (s)', fontsize=fontSizeLabels)
plt.ylabel('Amplitude (V)', fontsize=fontSizeLabels)
ax2.annotate('C', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()

figFormat = 'pdf' #'svg' 
figFilename = 'testfig' # Do not include extension
if PRINT_FIGURE:
    extraplots.save_figure(figFilename, figFormat, [8,6], outputDir)

