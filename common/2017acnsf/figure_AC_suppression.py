# Figure showing example of surround suppression in AC
#
# CURRENTLY, IT DEPENDS ON:
# jaratest.nick.database import dataloader_v2 as dataloader
# jaratest.anna import bandwidths_analysis
# jaratest/anna/analysis/band002_celldb.csv
# and of course, the ephys data.

import numpy as np
import pandas as pd
from jaratest.nick.database import dataloader_v2 as dataloader
#from jaratest.anna import bandwidths_analysis
#reload(bandwidths_analysis)
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
#from jaratoolbox import figparams
import matplotlib.gridspec as gridspec
import matplotlib
import string
import pdb
#from jaratest.nick.database import dataplotter
#reload(dataplotter)

SAMPLING_RATE=30000.0
#band002, 2016-08-12, 1380um, T6c4
CELL_NUM = 161

db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/band002_celldb.csv')
cell = db.loc[CELL_NUM]
ephysDirs = [word.strip(string.punctuation) for word in cell['ephys'].split()]
behavDirs = [word.strip(string.punctuation) for word in cell['behavior'].split()]
sessType = [word.strip(string.punctuation) for word in cell['sessiontype'].split()]
bandIndex = sessType.index('bandwidth')

def bandwidth_raster_inputs(eventOnsetTimes, spikeTimestamps, bandEachTrial, ampEachTrial, timeRange = [-0.2, 1.5]):          
    from jaratoolbox import behavioranalysis
    from jaratoolbox import spikesanalysis
    numBands = np.unique(bandEachTrial)
    numAmps = np.unique(ampEachTrial)
            
    firstSortLabels = ['{}'.format(band) for band in numBands]
            
    trialsEachCond = behavioranalysis.find_trials_each_combination(bandEachTrial, 
                                                                           numBands, 
                                                                           ampEachTrial, 
                                                                           numAmps)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimestamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        timeRange) 

    return spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachCond, firstSortLabels

def band_select(spikeTimeStamps, eventOnsetTimes, amplitudes, bandwidths, timeRange, fullRange = [0.0, 2.0]):
    from jaratoolbox import behavioranalysis
    from jaratoolbox import spikesanalysis
    from scipy import stats
    numBands = np.unique(bandwidths)
    numAmps = np.unique(amplitudes)
    spikeArray = np.zeros((len(numBands), len(numAmps)))
    errorArray = np.zeros_like(spikeArray)
    trialsEachCond = behavioranalysis.find_trials_each_combination(bandwidths, 
                                                                   numBands, 
                                                                   amplitudes, 
                                                                   numAmps)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimeStamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        fullRange)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    baseTimeRange = [timeRange[1]+0.5, fullRange[1]]
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseTimeRange)
    baselineSpikeRate = np.mean(baseSpikeCountMat)/(baseTimeRange[1]-baseTimeRange[0])
    plt.hold(True)
    for amp in range(len(numAmps)):
        trialsThisAmp = trialsEachCond[:,:,amp]
        for band in range(len(numBands)):
            trialsThisBand = trialsThisAmp[:,band]
            if spikeCountMat.shape[0] != len(trialsThisBand):
                spikeCountMat = spikeCountMat[:-1,:]
                print "FIXME: Using bad hack to make event onset times equal number of trials"
            thisBandCounts = spikeCountMat[trialsThisBand].flatten()
            spikeArray[band, amp] = np.mean(thisBandCounts)
            errorArray[band,amp] = stats.sem(thisBandCounts)
    return spikeArray, errorArray, baselineSpikeRate

def band_select_plot(spikeArray, errorArray, baselineSpikeRate, bands, legend = False, labels = ['50 dB SPL', '70 dB SPL'], timeRange = [0,1], title=None):
    import matplotlib.patches as mpatches
    xrange = range(len(bands))
    plt.plot(xrange, baselineSpikeRate*(timeRange[1]-timeRange[0])*np.ones(len(bands)), color = '0.75', linewidth = 2)
    plt.plot(xrange, spikeArray[:,0].flatten(), '-o', color = '#4e9a06', linewidth = 3)
    plt.fill_between(xrange, spikeArray[:,0].flatten() - errorArray[:,0].flatten(), 
                     spikeArray[:,0].flatten() + errorArray[:,0].flatten(), alpha=0.2, edgecolor = '#8ae234', facecolor='#8ae234')
    plt.plot(range(len(bands)), spikeArray[:,1].flatten(), '-o', color = '#5c3566', linewidth = 3)
    plt.fill_between(xrange, spikeArray[:,1].flatten() - errorArray[:,1].flatten(), 
                     spikeArray[:,1].flatten() + errorArray[:,1].flatten(), alpha=0.2, edgecolor = '#ad7fa8', facecolor='#ad7fa8')
    ax = plt.gca()
    ax.set_xticklabels(bands)
    plt.xlabel('bandwidth (octaves)')
    plt.ylabel('Average num spikes')
    if legend: 
        patch1 = mpatches.Patch(color='#5c3566', label=labels[1])
        patch2 = mpatches.Patch(color='#4e9a06', label=labels[0])
        plt.legend(handles=[patch1, patch2], bbox_to_anchor=(0.95, 0.95), borderaxespad=0.)
    if title:
        plt.title(title)

loader = dataloader.DataLoader(cell['subject'])

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

PRINT_FIGURE = 0
outputDir = '/tmp/'

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

labelPosX = [0.07, 0.47]  # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

plt.clf()

gs = gridspec.GridSpec(2, 4)
gs.update(left=0.15, right=0.85, wspace=1, hspace=0.5)

eventData = loader.get_session_events(ephysDirs[bandIndex])
spikeData = loader.get_session_spikes(ephysDirs[bandIndex], int(cell['tetrode']), cluster=int(cell['cluster']))
eventOnsetTimes = loader.get_event_onset_times(eventData)
spikeTimestamps = spikeData.timestamps
bdata = loader.get_session_behavior(behavDirs[bandIndex])
bandEachTrial = bdata['currentBand']
ampEachTrial = bdata['currentAmp']
spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachCond, firstSortLabels = bandwidth_raster_inputs(eventOnsetTimes, spikeTimestamps, bandEachTrial, ampEachTrial)


ax1 = plt.subplot(gs[0, :-2])
trialsThisSecondVal = trialsEachCond[:, :, 0]
pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                indexLimitsEachTrial,
                                                timeRange = [-0.2, 1.5],
                                                trialsEachCond=trialsThisSecondVal,
                                                labels=firstSortLabels,
                                                colorEachCond=np.tile(['#4e9a06','#8ae234'],len(bandEachTrial)/2+1))
plt.setp(pRaster, ms=4)
extraplots.boxoff(plt.gca())
plt.xlabel('Time from stimulus onset (s)', fontsize=fontSizeLabels)
plt.ylabel('Bandwidth (octaves)', fontsize=fontSizeLabels)
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')

ax2 = plt.subplot(gs[1,:-2])
trialsThisSecondVal = trialsEachCond[:, :, 1]
pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                indexLimitsEachTrial,
                                                timeRange = [-0.2, 1.5],
                                                trialsEachCond=trialsThisSecondVal,
                                                labels=firstSortLabels,
                                                colorEachCond=np.tile(['#5c3566','#ad7fa8'],len(bandEachTrial)/2+1))
plt.setp(pRaster, ms=4)
extraplots.boxoff(plt.gca())
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.xlabel('Time from stimulus onset (s)', fontsize=fontSizeLabels)
plt.ylabel('Bandwidth (octaves)', fontsize=fontSizeLabels)
ax2.annotate('B', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


ax3 = plt.subplot(gs[0:, -2:])
spikeArray, errorArray, baseSpikeRate = band_select(spikeTimestamps, eventOnsetTimes, ampEachTrial, bandEachTrial, timeRange = [0,1])
band_select_plot(spikeArray, errorArray, baseSpikeRate, np.unique(bandEachTrial), legend = True, labels = ['54 dB', '66 dB'])
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.xlabel('Bandwidth (octaves)', fontsize=fontSizeLabels)
plt.ylabel('Average number of spikes during stimulus', fontsize=fontSizeLabels)
ax3.annotate('C', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()

figFormat = 'pdf' #'svg' 
figFilename = 'testfig' # Do not include extension
if PRINT_FIGURE:
    extraplots.save_figure(figFilename, figFormat, [8,6], outputDir)
    
