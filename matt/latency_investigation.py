#%%
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import studyparams
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
import database_generation_funcs as funcs

#%% Loading in one cell
inforecFile = os.path.join(settings.INFOREC_PATH, 'd1pi042_inforec.py')
celldb = celldatabase.generate_cell_database(inforecFile)

cellDict = {'subject': 'd1pi042',
            'date': '2019-09-11',
            'depth': 3100.0,
            'tetrode': 4,
            'cluster': 3,
            }

cellInd, dbRow = celldatabase.find_cell(celldb, **cellDict)
oneCell = ephyscore.Cell(dbRow)
tuningEphysData, tuningBehavData = oneCell.load('tuningCurve')

#%% Calculations to test
baseRange = [-0.1, 0]

# Extracting information from ephys and behavior data to do calculations later with
currentFreq = tuningBehavData['currentFreq']
currentFreq = np.random.permutation(currentFreq)
currentIntensity = tuningBehavData['currentIntensity']
uniqFreq = np.unique(currentFreq)
uniqueIntensity = np.unique(currentIntensity)
tuningTrialsEachCond = behavioranalysis.find_trials_each_combination(currentFreq, uniqFreq, currentIntensity, uniqueIntensity)

allIntenBase = np.array([])
respSpikeMean = np.empty((len(uniqueIntensity), len(uniqFreq)))  # same as allIntenResp
allIntenRespMedian = np.empty((len(uniqueIntensity), len(uniqFreq)))
Rsquareds = []
popts = []
tuningSpikeTimes = tuningEphysData['spikeTimes']
tuningEventOnsetTimes = tuningEphysData['events']['soundDetectorOn']
tuningEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(tuningEventOnsetTimes, minEventOnsetDiff=0.2)

# Checking to see if the ephys data has one more trial than the behavior data and removing the last session if it does
if len(tuningEventOnsetTimes) == (len(currentFreq) + 1):
    tuningEventOnsetTimes = tuningEventOnsetTimes[0:-1]
    print("Correcting ephys data to be same length as behavior data")
    toCalculate = True
elif len(tuningEventOnsetTimes) == len(currentFreq):
    print("Data is already the same length")
    toCalculate = True
else:
    print("Something is wrong with the length of these data")
    toCalculate = False
    # Instead of generating an error I made it just not calculate statistics. I should possibly have it log all mice
    # and sites where it failed to calculate so someone can review later
timeRange = [-0.1, 0.3]
(tuningSpikeTimesFromEventOnset, tuningTrialIndexForEachSpike, tuningIndexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(tuningSpikeTimes, tuningEventOnsetTimes, timeRange)

trialsEachType = behavioranalysis.find_trials_each_type(currentFreq,
                                                        uniqFreq)
# -------------------- Start of calculations for the tuningCurve data -------------------------
# The latency of the cell from the onset of the stim
if toCalculate:
    tuningZStat, tuningPVal = \
        funcs.sound_response_any_stimulus(tuningEventOnsetTimes, tuningSpikeTimes, tuningTrialsEachCond[:, :, -1],
                                          timeRange=[0.0, 0.05], baseRange=baseRange)  # All trials at all frequencies at the highest intensity
    respLatency = funcs.calculate_latency(tuningEventOnsetTimes, currentFreq, uniqFreq, currentIntensity,
                                          uniqueIntensity, tuningSpikeTimes, 0)
    if tuningPVal > 0.05:
        toCalculate = False
else:
    respLatency = np.nan
    tuningPVal = np.nan
    tuningZStat = np.nan

#%% Plotting of data
b = np.array(["%.0f" % i for i in uniqFreq])  # this is unique frequencies, but rounded off
freqTicks = [str(b[i]) + " [" + str(i) + "]" for i, con in enumerate(b)]
nTrialsEachCond = [trialsEachType[:, i].sum() for i in range(trialsEachType.shape[1])]
new_tick_locations = np.cumsum(nTrialsEachCond)

fig, ax = plt.subplots(1, 1)
pTuningRaster, hTuningCond, zline = extraplots.raster_plot(tuningSpikeTimesFromEventOnset,
                                                           tuningIndexLimitsEachTrial,
                                                           timeRange,
                                                           trialsEachCond=trialsEachType)
plt.axvline(respLatency)
plt.setp(pTuningRaster, ms=3)
plt.setp(hTuningCond, zorder=3)
plt.ylabel('Trial')
ax.set_yticks(new_tick_locations)
ax.set_yticklabels(freqTicks)

ylim = ax.get_ylim()
onsetPatch = patches.Rectangle((respLatency, ylim[1] * 1.01),
                               0.05, ylim[1] * 0.02, linewidth=0.3,
                               edgecolor='green', facecolor='green', clip_on=False)
sustainedPatch = patches.Rectangle((respLatency + .05, ylim[1] * 1.01),
                                   0.05, ylim[1] * 0.02, linewidth=0.3,
                                   edgecolor='red', facecolor='red', clip_on=False)
ax.add_patch(onsetPatch)
ax.add_patch(sustainedPatch)

plt.title("latency = {0:.1f} ms".format(respLatency*1000), pad=15)
extraplots.save_figure('/home/spider/Desktop/respTest', 'png', [10, 5], facecolor='w')
plt.show()
