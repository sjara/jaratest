'''
Testing what is necessary to make pretty figures for papers.
'''


import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
#from jaratoolbox import figparams
import matplotlib.gridspec as gridspec

PRINT_FIGURE = 1
outputDir = '/tmp/'

fontSizeLabels = 10
fontSizeTicks = 10
fontSizePanel = 12

plt.clf()

gs = gridspec.GridSpec(2, 3)
gs.update(left=0.15, right=0.85, wspace=1, hspace=0.5)

ax1 = plt.subplot(gs[0, :])
plt.plot(np.random.randn(20),np.random.randn(20),'o',mfc='none')
extraplots.boxoff(plt.gca())
plt.xlabel('Time (s)', fontsize=fontSizeLabels)
plt.ylabel('Amplitude (V)', fontsize=fontSizeLabels)
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
ax.annotate('A', xytext=(0.8, 0.95), textcoords='figure fraction')
#plt.text('A',fontsize=)

ax2 = plt.subplot(gs[1,:-1])
plt.plot(np.random.randn(20),np.random.randn(20),'o',mfc='none')
plt.xlabel('Time (s)', fontsize=fontSizeLabels)
plt.ylabel('Amplitude (V)', fontsize=fontSizeLabels)

ax3 = plt.subplot(gs[1:, -1])
plt.plot(np.random.randn(20),np.random.randn(20),'o',mfc='none')
extraplots.set_ticks_fontsize(plt.gca(),fontSize)
plt.xlabel('Time (s)', fontsize=fontSizeLabels)
plt.ylabel('Amplitude (V)', fontsize=fontSizeLabels)

plt.show()

figFormat = 'pdf'
figFilename = 'testfig' # Do not include extension
if PRINT_FIGURE:
    extraplots.save_figure(figFilename, figFormat, [8,6], outputDir)

