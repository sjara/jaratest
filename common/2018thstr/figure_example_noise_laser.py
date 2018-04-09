import os
import numpy as np
from numpy import inf
from scipy import optimize
from scipy import stats
from scipy import signal
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
from jaratoolbox import extraplots
import figparams
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
db = pd.read_hdf(dbPath, key='dataframe')

FIGNAME = 'figure_noise_laser'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
figFilename = 'plots_noise_laser' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [6, 3] # In inches
SAVE_FIGURE=1

gs = gridspec.GridSpec(2, 3)
gs.update(hspace=0.4)

axThalCartoon = plt.subplot(gs[0,0])
axThalCartoon.axis('off')
axACCartoon = plt.subplot(gs[1,0])
axACCartoon.axis('off')

gsThalResp = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[0, 1], hspace=0.7)
gsThalNoise = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gsThalResp[0], hspace=0)
axThalNoiseRaster = plt.subplot(gsThalNoise[0])
axThalNoisePSTH = plt.subplot(gsThalNoise[1])

gsThalLaser = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gsThalResp[1], hspace=0)
axThalLaserRaster = plt.subplot(gsThalLaser[0])
axThalLaserPSTH = plt.subplot(gsThalLaser[1])

gsACResp = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[1, 1], hspace=0.5)
gsACNoise = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gsACResp[0], hspace=0)
axACNoiseRaster = plt.subplot(gsACNoise[0])
axACNoisePSTH = plt.subplot(gsACNoise[1])

gsACLaser = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gsACResp[1], hspace=0)
axACLaserRaster = plt.subplot(gsACLaser[0])
axACLaserPSTH = plt.subplot(gsACLaser[1])

axThalSites = plt.subplot(gs[0, 2])
axThalSites.axis('off')
axACSites = plt.subplot(gs[1, 2])
axACSites.axis('off')

thalExample = {'cluster': 2,
               'date': '2017-03-14',
               'depth': 3703.0,
               'subject': 'pinp016',
               'tetrode': 2}

acExample = {'cluster': 4,
             'date': '2017-03-23',
             'depth': 1604.0,
             'subject': 'pinp017',
             'tetrode': 7}

indRowThal, rowThal = celldatabase.find_cell(db, **thalExample)
indRowAC, rowAC = celldatabase.find_cell(db, **acExample)

## -- Plot colors -- ##
colorAThNoise = 'k'
colorAThLaser = 'k'
colorACNoise = 'k'
colorACLaser = 'k'
colorNoise = figparams.colp['sound']
colorLaser = figparams.colp['blueLaser']
stimLineWidth = 4
psthLineWidth = 2
rasterMS = 1

## -- Raster/PSTH parameters --##
stimLineOffsetFrac = 0.2
alignmentRange = [-0.2, 0.6]
displayRange = [-0.1, 0.5]
binsize = 10 #in milliseconds
binEdges = np.around(np.arange(alignmentRange[0]-(binsize/1000.0), alignmentRange[1]+2*(binsize/1000.0), (binsize/1000.0)), decimals=2)
smoothPSTH = True
smoothWinSize = 1
winShape = np.concatenate((np.zeros(smoothWinSize),np.ones(smoothWinSize))) # Square (causal)
winShape = winShape/np.sum(winShape)
psthTimeBase = np.linspace(alignmentRange[0], alignmentRange[1], num=len(binEdges)-1)

## -- Thalamus Noise -- ##
spikeTimesFromEventOnset = None
trialIndexForEachSpike = None
indexLimitsEachTrial = None
sessiontype = 'noiseburst'
cell = ephyscore.Cell(rowThal)
ephysData, bdata = cell.load(sessiontype)
spikeTimes = ephysData['spikeTimes']
eventOnsetTimes = ephysData['events']['stimOn']
(spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                eventOnsetTimes,
                                                                alignmentRange)
axThalNoiseRaster.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.',
                       ms=rasterMS)
axThalNoiseRaster.set_xlim(displayRange)
axThalNoiseRaster.axis('off')

thalNoiseLineY = max(trialIndexForEachSpike) + max(trialIndexForEachSpike)*stimLineOffsetFrac
axThalNoiseRaster.plot([0, 0.1], [thalNoiseLineY, thalNoiseLineY], lw=stimLineWidth, color=colorNoise,
                       clip_on=False)

spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                         indexLimitsEachTrial, binEdges)
thisPSTH = np.mean(spikeCountMat,axis=0)
if smoothPSTH:
    thisPSTH = np.convolve(thisPSTH, winShape, mode='same')
ratePSTH = thisPSTH/float(binsize/1000.0)
axThalNoisePSTH.plot(psthTimeBase, ratePSTH, '-',
                     color=colorAThNoise, lw=psthLineWidth)
axThalNoisePSTH.set_xlim(displayRange)
extraplots.boxoff(axThalNoisePSTH)
axThalNoisePSTH.set_ylim([0, max(ratePSTH)])
axThalNoisePSTH.set_yticks([0, np.floor(np.max(ratePSTH))])
axThalNoisePSTH.set_ylabel('spk/sec')

## -- Thalamus Laser -- ##
spikeTimesFromEventOnset = None
trialIndexForEachSpike = None
indexLimitsEachTrial = None
sessiontype = 'laserpulse'
cell = ephyscore.Cell(rowThal)
ephysData, bdata = cell.load(sessiontype)
spikeTimes = ephysData['spikeTimes']
eventOnsetTimes = ephysData['events']['stimOn']
(spikeTimesFromEventOnset,
 trialIndexForEachSpike,
 indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                               eventOnsetTimes,
                                                               alignmentRange)
axThalLaserRaster.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.', ms=rasterMS)
axThalLaserRaster.set_xlim(displayRange)
axThalLaserRaster.axis('off')

thalLaserLineY = max(trialIndexForEachSpike) + max(trialIndexForEachSpike)*stimLineOffsetFrac
axThalLaserRaster.plot([0, 0.1], [thalLaserLineY, thalLaserLineY], lw=stimLineWidth, color=colorLaser,
                       clip_on=False)

spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                         indexLimitsEachTrial, binEdges)
thisPSTH = np.mean(spikeCountMat,axis=0)
if smoothPSTH:
    thisPSTH = np.convolve(thisPSTH, winShape, mode='same')
ratePSTH = thisPSTH/float(binsize/1000.0)
axThalLaserPSTH.plot(psthTimeBase, ratePSTH, '-',
                     color=colorAThLaser, lw=psthLineWidth)
axThalLaserPSTH.set_xlim(displayRange)
extraplots.boxoff(axThalLaserPSTH)
axThalLaserPSTH.set_ylim([0, max(ratePSTH)])
axThalLaserPSTH.set_yticks([0, np.floor(np.max(ratePSTH))])
axThalLaserPSTH.set_ylabel('spk/sec')


#AC Noise
spikeTimesFromEventOnset = None
trialIndexForEachSpike = None
indexLimitsEachTrial = None
sessiontype = 'noiseburst'
cell = ephyscore.Cell(rowAC)
ephysData, bdata = cell.load(sessiontype)
spikeTimes = ephysData['spikeTimes']
eventOnsetTimes = ephysData['events']['stimOn']
(spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                eventOnsetTimes,
                                                                alignmentRange)
axACNoiseRaster.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.', ms=rasterMS)
axACNoiseRaster.set_xlim(displayRange)
axACNoiseRaster.axis('off')

acNoiseLineY = max(trialIndexForEachSpike) + max(trialIndexForEachSpike)*stimLineOffsetFrac
axACNoiseRaster.plot([0, 0.1], [acNoiseLineY, acNoiseLineY], lw=stimLineWidth, color=colorNoise,
                       clip_on=False)

spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                         indexLimitsEachTrial, binEdges)
thisPSTH = np.mean(spikeCountMat,axis=0)
if smoothPSTH:
    thisPSTH = np.convolve(thisPSTH, winShape, mode='same')
ratePSTH = thisPSTH/float(binsize/1000.0)
axACNoisePSTH.plot(psthTimeBase, ratePSTH, '-',
                     color=colorAThNoise, lw=psthLineWidth)
axACNoisePSTH.set_xlim(displayRange)
extraplots.boxoff(axACNoisePSTH)
axACNoisePSTH.set_ylim([0, max(ratePSTH)])
axACNoisePSTH.set_yticks([0, np.floor(np.max(ratePSTH))])
axACNoisePSTH.set_ylabel('spk/sec')

#AC Laser
spikeTimesFromEventOnset = None
trialIndexForEachSpike = None
indexLimitsEachTrial = None
sessiontype = 'laserpulse'
cell = ephyscore.Cell(rowAC)
ephysData, bdata = cell.load(sessiontype)
spikeTimes = ephysData['spikeTimes']
eventOnsetTimes = ephysData['events']['stimOn']
(spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                eventOnsetTimes,
                                                                alignmentRange)
axACLaserRaster.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.', ms=rasterMS)
axACLaserRaster.set_xlim(displayRange)
axACLaserRaster.axis('off')

acLaserLineY = max(trialIndexForEachSpike) + max(trialIndexForEachSpike)*stimLineOffsetFrac
axACLaserRaster.plot([0, 0.1], [acLaserLineY, acLaserLineY], lw=stimLineWidth, color=colorLaser,
                       clip_on=False)

spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                         indexLimitsEachTrial, binEdges)
thisPSTH = np.mean(spikeCountMat,axis=0)
if smoothPSTH:
    thisPSTH = np.convolve(thisPSTH, winShape, mode='same')
ratePSTH = thisPSTH/float(binsize/1000.0)
axACLaserPSTH.plot(psthTimeBase, ratePSTH, '-',
                     color=colorAThLaser, lw=psthLineWidth)
axACLaserPSTH.set_xlim(displayRange)
extraplots.boxoff(axACLaserPSTH)
axACLaserPSTH.set_ylim([0, max(ratePSTH)])
axACLaserPSTH.set_yticks([0, np.floor(np.max(ratePSTH))])
axACLaserPSTH.set_ylabel('spk/sec')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

plt.show()

