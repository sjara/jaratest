"""
Plot tuning curves before and after DOI injection.

Based on tuningCurvePlots.py by Max Horrocks.


261 (change in gain in tuning) a little better fit
264 (change in gain in tuning, higher spont)
284 (change in gain, and interesting changes in dynamics)
431 (no change in tuning or spont) best
449 (no change in tuning or spont)

135 (FM oddball up and also interesting tuning)

To check tuning that did not fit:
135
275


"""

import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import colorpalette as cp


SAVE_FIGURE = 1

timeRangePlot = [-0.25, 0.45]
timeRangeStim = [0.015, 0.115]
timeRangeBaseline = [-0.2, 0]
baselineDuration = timeRangeBaseline[1] - timeRangeBaseline[0]
stimDuration = timeRangeStim[1] - timeRangeStim[0]

colors = {'saline':cp.TangoPalette['SkyBlue2'], 'doi': cp.TangoPalette['ScarletRed1']}
colorsLight = {k: matplotlib.colors.colorConverter.to_rgba(onecol, alpha=0.5)
               for k,onecol in colors.items()}
#{'saline':colors['saline'], 'doi': cp.TangoPalette['ScarletRed1']}

rasterMarkerSize = 1  #3

subject = 'acid006'

inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')

celldb = celldatabase.generate_cell_database(inforecFile)
dbPath = os.path.join(settings.DATABASE_PATH ,f'celldb_{subject}.h5')

# Add info for loading a specific cell.
CELL_TO_PLOT = 1
if CELL_TO_PLOT == 0:
    cellDict = {'subject' : 'acid006',
                'date' : '2023-03-22',
                'pdepth' : 3000,
                'egroup' : 0,
                'cluster' : 431}
elif CELL_TO_PLOT == 1:
    cellDict = {'subject' : 'acid006',
                'date' : '2023-03-22',
                'pdepth' : 3000,
                'egroup' : 0,
                'cluster' : 261}

cellInd, dbRow = celldatabase.find_cell(celldb, **cellDict)
oneCell = ephyscore.Cell(dbRow)

reagents = ('saline', 'doi')
oddballSessions = ('FM_Up', 'FM_Down')


def plot_stim(yLims, stimDuration, stimLineWidth=6, stimColor='#edd400'):
    # -- Plot the stimulus --
    yPos = 1.0*yLims[-1] + 0.075*(yLims[-1]-yLims[0])
    pstim = plt.plot([0, stimDuration], 2*[yPos], lw=stimLineWidth, color=stimColor,
                     clip_on=False, solid_capstyle='butt')
    return pstim[0]


#fig = plt.figure(figsize=(8,10))
fig = plt.gcf()
gsMain = gs.GridSpec(2, 2, figure=fig, )
gsMain.update(top=0.95, bottom=0.2, left=0.08, right=0.99, wspace=0.3, hspace=0.075)
#gsOne = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[0])
#plt.subplots_adjust(hspace=0.50)

ephysData, bdata = oneCell.load(f'salinePureTones')  
spikeTimes = ephysData['spikeTimes']
eventOnsetTimes = ephysData['events']['stimOn']

stimDuration = bdata['stimDur'][-1]

frequencies_each_trial = bdata['currentFreq']
array_of_frequencies = np.unique(bdata['currentFreq'])
nFreq = len(array_of_frequencies)

# Checks to see if trial count from bdata is the same as trial count from ephys
if (len(frequencies_each_trial) > len(eventOnsetTimes)) or \
   (len(frequencies_each_trial) < len(eventOnsetTimes)-1):
    print(f'Warning! BevahTrials ({len(frequencies_each_trial)}) and ' +
          f'EphysTrials ({len(eventOnsetTimes)})')
    sys.exit()

# If the ephys data is 1 more than the bdata, delete the last ephys trial.
if len(frequencies_each_trial) == len(eventOnsetTimes)-1:
    eventOnsetTimes = eventOnsetTimes[:len(frequencies_each_trial)]

(spikeTimesFromEventOnsetSaline, trialIndexForEachSpikeSaline, indexLimitsEachTrialSaline) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRangePlot)    

trialsEachCondSaline = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)

ephysData, bdata = oneCell.load(f'doiPureTones')  
spikeTimes = ephysData['spikeTimes']
eventOnsetTimes = ephysData['events']['stimOn']


frequencies_each_trial = bdata['currentFreq']
array_of_frequenciesDOI = np.unique(bdata['currentFreq'])

# Checks to see if trial count from bdata is the same as trial count from ephys
if (len(frequencies_each_trial) > len(eventOnsetTimes)) or \
   (len(frequencies_each_trial) < len(eventOnsetTimes)-1):
    print(f'Warning! BevahTrials ({len(frequencies_each_trial)}) and ' +
          f'EphysTrials ({len(eventOnsetTimes)})')
    sys.exit()

# If the ephys data is 1 more than the bdata, delete the last ephys trial.
if len(frequencies_each_trial) == len(eventOnsetTimes)-1:
    eventOnsetTimes = eventOnsetTimes[:len(frequencies_each_trial)]

(spikeTimesFromEventOnsetDOI, trialIndexForEachSpikeDOI, indexLimitsEachTrialDOI) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRangePlot)    

trialsEachCondDOI = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)

spikeCountMatSaline = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetSaline,
                                                               indexLimitsEachTrialSaline, timeRangeStim)
spikeCountMatDOI = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetDOI,
                                                            indexLimitsEachTrialDOI, timeRangeStim)

nTrialsSaline = len(indexLimitsEachTrialSaline[0])
nTrialsDOI= len(indexLimitsEachTrialDOI[0])

#get trial index for each condition
trialsEachCondIndsSaline, nTrialsEachCondSaline, nCondSaline = \
    extraplots.trials_each_cond_inds(trialsEachCondSaline, nTrialsSaline)
trialsEachCondIndsDOI, nTrialsEachCondDOI, nCondDOI = \
    extraplots.trials_each_cond_inds(trialsEachCondDOI, nTrialsDOI)

firingRatesSaline = np.empty(nCondSaline)
for cond in range(nCondSaline):
    nSpikesEachTrial = spikeCountMatSaline[trialsEachCondSaline[:,cond]]
    avgSpikes = np.mean(nSpikesEachTrial)
    spikesFiringRate = (avgSpikes / stimDuration)
    firingRatesSaline[cond] = spikesFiringRate


firingRatesDOI = np.empty(nCondDOI)
for cond in range(nCondDOI):
    nSpikesEachTrial = spikeCountMatDOI[trialsEachCondDOI[:,cond]]
    avgSpikes = np.mean(nSpikesEachTrial)
    spikesFiringRate = (avgSpikes / stimDuration)
    firingRatesDOI[cond] = spikesFiringRate


ax0 = plt.subplot(gsMain[0])
colorEachCond = [colors['saline'], colorsLight['saline']]*(nFreq//2+1)
(pRasterS,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnsetSaline,
                                                indexLimitsEachTrialSaline, timeRangePlot,
                                                trialsEachCondSaline, labels=array_of_frequencies,
                                                colorEachCond=colorEachCond)
#plt.setp(pRasterS, color=colors['saline'])
plt.setp(pRasterS, ms=rasterMarkerSize)
#plt.xlabel('Time (s)')
plt.ylabel('Freq (kHz)')
ax0.set_yticklabels(['2']+['']*(nFreq-2)+['40'])
#plt.title('Saline tuningFreq Raster')
ax0.set_xticklabels([])
plot_stim(plt.ylim(), stimDuration)

#ax1 = plt.subplot(gsMain[2], sharex = ax0)
ax1 = plt.subplot(gsMain[2])
colorEachCond = [colors['doi'], colorsLight['doi']]*(nFreq//2+1)
(pRasterD,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnsetDOI,
                                                indexLimitsEachTrialDOI, timeRangePlot,
                                                trialsEachCondDOI, labels=array_of_frequencies,
                                                colorEachCond=colorEachCond)
#plt.setp(pRasterD, color=colors['doi'])
plt.setp(pRasterD, ms=rasterMarkerSize)
plt.xlabel('Time (s)')
plt.ylabel('Freq (kHz)')
ax1.set_yticklabels(['2']+['']*(nFreq-2)+['40'])


possibleLogFreq = np.log2(array_of_frequencies)

#try: 
fitParamsSaline, RSquaredSaline = extraplots.fit_tuning_curve(possibleLogFreq, firingRatesSaline)
fitParamsDOI, RSquaredDOI = extraplots.fit_tuning_curve(possibleLogFreq, firingRatesDOI)

ax2 = plt.subplot(gsMain[:, 1])
pdots1,pfit1 = extraplots.plot_tuning_curve(array_of_frequencies, firingRatesSaline, fitParamsSaline)
pfit1[0].set_color(colors['saline'])
pdots1[0].set_color(colors['saline'])
#plt.legend("Saline", "Dot")
pdots2,pfit2 =extraplots.plot_tuning_curve(array_of_frequencies, firingRatesDOI, fitParamsDOI)
pfit2[0].set_color(colors['doi'])
pdots2[0].set_color(colors['doi'])
extraplots.boxoff(ax2)
xTicks = np.array([2000, 4000, 8000,16000, 32000])
ax2.set_xticks(np.log2(xTicks))
ax2.set_xticklabels((xTicks/1000).astype(int))

ax2.legend([pfit1[0], pfit2[0]], ['Saline', 'DOI'], loc='upper left', handlelength=1.5)


figDirectory = os.path.join(settings.FIGURES_DATA_PATH, f'{subject}/tuningFreq')
if not os.path.exists(figDirectory):
    os.makedirs(figDirectory)
figName= f'{subject}_{dbRow.date}_{dbRow.maxDepth}um_c{dbRow.cluster}_tuningFreq'
fileName = os.path.join(figDirectory, figName)

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figName, 'png', [6, 2.5], outputDir='/tmp/', facecolor='w')

