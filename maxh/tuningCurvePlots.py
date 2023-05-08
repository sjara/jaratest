import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
#sys.path.append('/Home/src/jaratest/maxh')
#sys.path.append('C:/Users/mdhor/Documents/GitHub/jaratest/maxh')
#import oddball_analysis_functions as odbl
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis

timeRangePlot = [-0.3, 0.45]
timeRangeStim = [0.015, 0.115]
timeRangeBaseline = [-0.2, 0]
baselineDuration = timeRangeBaseline[1] - timeRangeBaseline[0]
stimDuration = timeRangeStim[1] - timeRangeStim[0]


subject = 'acid006'

inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')

celldb = celldatabase.generate_cell_database(inforecFile)
dbPath = os.path.join(settings.DATABASE_PATH ,f'celldb_{subject}.h5')

# Add info for loading a specific cell.
cellDict = {'subject' : 'acid006',
            'date' : '2023-03-22',
            'pdepth' : 3000,
            'egroup' : 0,
            'cluster' : 431}

cellInd, dbRow = celldatabase.find_cell(celldb, **cellDict)
oneCell = ephyscore.Cell(dbRow)

reagents = ('saline', 'doi')
oddballSessions = ('FM_Up', 'FM_Down')

fig = plt.figure(figsize=(8,10))
gsMain = gs.GridSpec(2, 2, figure=fig)
#gsOne = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[0])
#plt.subplots_adjust(hspace=0.50)

ephysData, bdata = oneCell.load(f'salinePureTones')  
spikeTimes = ephysData['spikeTimes']
eventOnsetTimes = ephysData['events']['stimOn']


frequencies_each_trial = bdata['currentFreq']
array_of_frequencies = np.unique(bdata['currentFreq'])

# Checks to see if trial count from bdata is the same as trial count from ephys
if (len(frequencies_each_trial) > len(eventOnsetTimes)) or (len(frequencies_each_trial) < len(eventOnsetTimes)-1):
    print(f'Warning! BevahTrials ({len(frequencies_each_trial)}) and ' + f'EphysTrials ({len(eventOnsetTimes)})')
    sys.exit()

# If the ephys data is 1 more than the bdata, delete the last ephys trial.
if len(frequencies_each_trial) == len(eventOnsetTimes)-1:
    eventOnsetTimes = eventOnsetTimes[:len(frequencies_each_trial)]

(spikeTimesFromEventOnsetSaline, trialIndexForEachSpikeSaline, indexLimitsEachTrialSaline) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRangePlot)    

trialsEachCondSaline = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)

ephysData, bdata = oneCell.load(f'doiPureTones')  
spikeTimes = ephysData['spikeTimes']
eventOnsetTimes = ephysData['events']['stimOn']


frequencies_each_trial = bdata['currentFreq']
array_of_frequenciesDOI = np.unique(bdata['currentFreq'])

# Checks to see if trial count from bdata is the same as trial count from ephys
if (len(frequencies_each_trial) > len(eventOnsetTimes)) or (len(frequencies_each_trial) < len(eventOnsetTimes)-1):
    print(f'Warning! BevahTrials ({len(frequencies_each_trial)}) and ' + f'EphysTrials ({len(eventOnsetTimes)})')
    sys.exit()

# If the ephys data is 1 more than the bdata, delete the last ephys trial.
if len(frequencies_each_trial) == len(eventOnsetTimes)-1:
    eventOnsetTimes = eventOnsetTimes[:len(frequencies_each_trial)]

(spikeTimesFromEventOnsetDOI, trialIndexForEachSpikeDOI, indexLimitsEachTrialDOI) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRangePlot)    

trialsEachCondDOI = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)

spikeCountMatSaline = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetSaline, indexLimitsEachTrialSaline, timeRangeStim)
spikeCountMatDOI = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetDOI, indexLimitsEachTrialDOI, timeRangeStim)

nTrialsSaline = len(indexLimitsEachTrialSaline[0])
nTrialsDOI= len(indexLimitsEachTrialDOI[0])

#get trial index for each condition
trialsEachCondIndsSaline, nTrialsEachCondSaline, nCondSaline= extraplots.trials_each_cond_inds(trialsEachCondSaline, nTrialsSaline)
trialsEachCondIndsDOI, nTrialsEachCondDOI, nCondDOI= extraplots.trials_each_cond_inds(trialsEachCondDOI, nTrialsDOI)

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
plt.xlabel('Time (s)')
plt.ylabel('Trials')
plt.title('Saline tuningFreq Raster')
fRaster = extraplots.raster_plot(spikeTimesFromEventOnsetSaline, indexLimitsEachTrialSaline, timeRangePlot, trialsEachCondSaline, labels = array_of_frequencies)

ax1 = plt.subplot(gsMain[2], sharex = ax0)
plt.xlabel('Time (s)')
plt.ylabel('Trials')
plt.title('DOI tuningFreq Raster')
fRaster = extraplots.raster_plot(spikeTimesFromEventOnsetDOI, indexLimitsEachTrialDOI, timeRangePlot, trialsEachCondDOI, labels = array_of_frequencies)

possibleLogFreq = np.log2(array_of_frequencies)

try: 
    fitParamsSaline, RSquaredSaline = extraplots.fit_tuning_curve(possibleLogFreq, firingRatesSaline)
    fitParamsDOI, RSquaredDOI = extraplots.fit_tuning_curve(possibleLogFreq, firingRatesDOI)

    ax2 = plt.subplot(gsMain[1])
    pdots1,pfit1 = extraplots.plot_tuning_curve(array_of_frequencies, firingRatesSaline, fitParamsSaline)
    pfit1[0].set_color('blue')
    pdots1[0].set_color('blue')
    #plt.legend("Saline", "Dot")
    pdots2,pfit2 =extraplots.plot_tuning_curve(array_of_frequencies, firingRatesDOI, fitParamsDOI)
    pfit2[0].set_color('red')
    pdots2[0].set_color('red')
    #ax2.legend(['Saline', 'DOI'])
    


    figDirectory = os.path.join(settings.FIGURES_DATA_PATH, f'{subject}/tuningFreq')
    if not os.path.exists(figDirectory):
        os.makedirs(figDirectory)
    figName= f'{subject}_{dbRow.date}_{dbRow.maxDepth}um_c{dbRow.cluster}_tuningFreq.png'
    fileName = os.path.join(figDirectory, figName)

    plt.show()
    #plt.savefig(fileName, format='png')
    print(f'saving image {figName}')
    plt.close()
except:
    print('fitParams error')
    plt.close()


print("done")