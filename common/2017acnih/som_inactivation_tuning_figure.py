''' Create figure showing bandwidth tuning with and without SOM inactivation'''
import os
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

FIGNAME = 'SOM_inactivation_bandwidth_tuning'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2017acnih', FIGNAME)


matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

# copied this right out of Lan's scripts

SAVE_FIGURE = 1
outputDir = '/home/jarauser/tmp/'
figFilename = 'figure_som_inactivation_bandwidth_tuning' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [8,6]

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16
labelDis = 0.1
labelPosX = [0.07, 0.45]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

laserColour = ['#4e9a06','#8ae234'] #CHANGE TO WHATEVER WEIRD COLOURS YOU WANT SANTIAGO
noLaserColour = ['0.25', '0.75']
colours = [noLaserColour, laserColour]

gs = gridspec.GridSpec(2,4)
gs.update(left=0.15, right=0.85, wspace=0.5, hspace=0.5)

filename = 'example_bandwidth_tuning_band025_2017-04-20_T6_c6.npz'
dataFullPath = os.path.join(dataDir,filename)
data = np.load(dataFullPath)

# --- raster plots of sound response with and without laser ---
laserTrials = data['possibleSecondSort']
for laser in laserTrials:
    plt.subplot(gs[laser,0:2])
    colourEachCond = np.tile(colours[laser], len(data['possibleBands'])/2+1)
    pRaster, hcond, zline = extraplots.raster_plot(data['spikeTimesFromEventOnset'],
                                               data['indexLimitsEachTrial'],
                                               data['timeRange'],
                                               trialsEachCond=data['trialsEachCond'][:,:,laser],
                                               labels=data['firstSortLabels'],
                                               colorEachCond=colourEachCond)
    plt.ylabel('bandwidth (octaves)')
plt.xlabel('Time from stimulus onset (s)')

# --- plot of bandwidth tuning with and without laser ---
spikeArray = data['spikeArray']
errorArray = data['errorArray']
bands = data['possibleBands']
plt.subplot(gs[0:,2:])
lines = []
plt.hold(True)
l1,=plt.plot(range(len(bands)), spikeArray[:,0].flatten(), '-o', color = noLaserColour[0], mec = noLaserColour[0], linewidth = 3)
lines.append(l1)
plt.fill_between(range(len(bands)), spikeArray[:,0].flatten() - errorArray[:,0].flatten(), 
                     spikeArray[:,0].flatten() + errorArray[:,0].flatten(), alpha=0.2, edgecolor = noLaserColour[1], facecolor=noLaserColour[1])
l2,=plt.plot(range(len(bands)), spikeArray[:,1].flatten(), '-o', color = laserColour[0], mec = laserColour[0], linewidth = 3)
lines.append(l2)
plt.fill_between(range(len(bands)), spikeArray[:,1].flatten() - errorArray[:,1].flatten(), 
                         spikeArray[:,1].flatten() + errorArray[:,1].flatten(), alpha=0.2, edgecolor = laserColour[1], facecolor=laserColour[1])
ax = plt.gca()
ax.set_xticklabels(bands)
plt.xlabel('bandwidth (octaves)')
plt.ylabel('Average num spikes')
plt.legend(lines,['no laser', 'laser'], bbox_to_anchor=(0.95, 0.95), borderaxespad=0.)

plt.show()