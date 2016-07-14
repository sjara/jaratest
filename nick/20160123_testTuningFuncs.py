from jaratoolbox.test.nick.database import dataloader
from jaratoolbox.test.nick.database import dataplotter
from jaratoolbox.test.nick.database import cellDB
from jaratoolbox.test.nick.database import clusterfuncs
from jaratoolbox import spikesorting
from matplotlib import pyplot as plt
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis


reload(cellDB)
reload(clusterfuncs)

figdb = cellDB.CellDB()
figdbFn = '/home/nick/data/database/pinp003_thalamus_cells.json'
figdb.load_from_json(figdbFn)

loader = dataloader.DataLoader('offline', experimenter='nick')

figdb[1].get_session_types()

clusterfuncs.plot_cluster_tuning(figdb[1], 3)

spikeData, eventData, behavData = loader.get_cluster_data(figdb[1], 3)


currentFreq = behavData['currentFreq']
possibleFreq = np.unique(currentFreq)
currentIntensity=behavData['currentIntensity']
possibleIntensity = np.unique(currentIntensity)


db40= np.flatnonzero((currentIntensity==40) & (currentFreq==2000))

freq4spikes = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, freq4trials)]
freq4inds = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, freq4trials)]




# Shows the actual number of spikes after each trial. Not sure any more if this is the way we want to go.
# I am leaning more towards a z-score approach now.


timeRange = [0, 0.1]
spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
    spikeTimestamps, eventOnsetTimes, timeRange)

numSpikesInTimeRangeEachTrial = np.squeeze(np.diff(indexLimitsEachTrial,
                                                    axis=0))

baseRange = [-0.050,-0.025]              # Baseline range (in seconds)
binTime = baseRange[1]-baseRange[0]         # Time-bin size
responseTimeRange = [0,0.1]       #Time range to calculate z value for (should be divisible by binTime
responseTime = responseTimeRange[1]-responseTimeRange[0]
numBins = responseTime/binTime
binEdges = np.arange(responseTimeRange[0], responseTimeRange[1], binTime)

for indinten, inten in enumerate( possibleIntensity ):

    freqIndexEachTrial = array([])
    numSpikesEachTrial = array([])
    meanSpikesEachTrial = array([])
    maxZeachFreq = array([])

    for indfreq, freq in enumerate( possibleFreq ):

        trialsThisCombo = np.flatnonzero((currentIntensity==inten) & (currentFreq==freq))
        spikeNumsThisCombo = numSpikesInTimeRangeEachTrial[trialsThisCombo]

        numSpikesEachTrial = np.concatenate([numSpikesEachTrial, spikeNumsThisCombo])
        freqIndexEachTrial = np.concatenate([freqIndexEachTrial, array([indfreq]).repeat(len(spikeNumsThisCombo))])
        meanSpikesEachTrial = np.concatenate([meanSpikesEachTrial, array([mean(spikeNumsThisCombo)]) ])



    subplot(len( possibleIntensity ), 1, indinten+1)
    plot(freqIndexEachTrial, numSpikesEachTrial, 'k.')

    plot(range(0, len(possibleFreq)), meanSpikesEachTrial, 'r-')






#Using Z score instead of average spikes
#TODO: Not sure if this is really working. Runs but gives strange output. 

baseRange = [-0.050,-0.025]              # Baseline range (in seconds)
binTime = baseRange[1]-baseRange[0]         # Time-bin size
responseTimeRange = [0,0.1]       #Time range to calculate z value for (should be divisible by binTime
responseTime = responseTimeRange[1]-responseTimeRange[0]
numBins = responseTime/binTime
binEdges = np.arange(responseTimeRange[0], responseTimeRange[1], binTime)


#Use a longer base timerange so that we can determine baseline firing rate
timeRange = [-0.5, 1]
spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
    spikeTimestamps, eventOnsetTimes, timeRange)


maxZarray = np.zeros([len(possibleIntensity), len(possibleFreq)])
for indInt, intensity in enumerate(possibleIntensity):
    for indFreq, freq in enumerate(possibleFreq):
        trialsThisCombo = np.flatnonzero((currentIntensity==inten) & (currentFreq==freq))
        indexLimitsThisCombo = indexLimitsEachTrial[:, trialsThisCombo]
        spikeTimesThisCombo= spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, trialsThisCombo)]

        [zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesThisCombo,indexLimitsThisCombo,baseRange,binEdges) #computes z score for each bin. zStat is array of z scores. maxZ is maximum value of z in timeRange

        maxZarray[indInt, indFreq] = maxZ




#Testing the above method
testfreq = possibleFreq[6]
testinten = 60

trialsThisCombo = np.flatnonzero((currentFreq==testfreq)&(currentIntensity==testinten))

timeRange = [-0.5, 1]
spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
    spikeTimestamps, eventOnsetTimes, timeRange)

testspikes = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, trialsThisCombo)]
freq4inds = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, trialsThisCombo)]










#A potentially flawed idea that I might come back to. It is not as helpful with this idea as I thought it would be
#Copies of two functions from dataplotter that should help with the analysis of TCs

trialsEachCond = behavioranalysis.find_trials_each_combination(currentIntensity, possibleIntensity, currentFreq, possibleFreq)
conditionMatShape = np.shape(trialsEachCond)



timeRange = [0, 0.1]
spikeTimestamps = spikeData.timestamps
eventOnsetTimes = loader.get_event_onset_times(eventData)

if len(eventOnsetTimes) != np.shape(trialsEachCond)[0]:
    eventOnsetTimes = eventOnsetTimes[:-1]

spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
    spikeTimestamps, eventOnsetTimes, timeRange)

numSpikesInTimeRangeEachTrial = np.squeeze(np.diff(indexLimitsEachTrial,
                                                    axis=0))

trialsEachCond = behavioranalysis.find_trials_each_combination(currentIntensity, possibleIntensity, currentFreq, possibleFreq)

conditionMatShape = np.shape(trialsEachCond)

numRepeats = np.product(conditionMatShape[1:])


nSpikesMat = np.reshape(numSpikesInTimeRangeEachTrial.repeat(numRepeats),
                        conditionMatShape)


spikesFilteredByTrialType = nSpikesMat * trialsEachCond

avgSpikesArray = np.sum(spikesFilteredByTrialType,
                        0) / np.sum(trialsEachCond, 0).astype('float')

#The problem with this approach is that it does not allow us to distinguish between trials where the cell
#actually had a zero firing rate and trials 


def avg_spikes_in_event_locked_timerange_each_cond(spikeTimestamps,
                                                   trialsEachCond,
                                                   eventOnsetTimes, timeRange):

    '''
    Aligns the spikes to the ephys events and then passes them to the next fxn
    '''
    if len(eventOnsetTimes) != np.shape(trialsEachCond)[0]:
        eventOnsetTimes = eventOnsetTimes[:-1]
        print "FIXME: Using bad hack to make event onset times equal number of trials"


    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeTimestamps, eventOnsetTimes, timeRange)

    spikeArray = avg_locked_spikes_per_condition(indexLimitsEachTrial,
                                                 trialsEachCond)

    return spikeArray

def avg_locked_spikes_per_condition(indexLimitsEachTrial, trialsEachCond):

    numSpikesInTimeRangeEachTrial = np.squeeze(np.diff(indexLimitsEachTrial,
                                                       axis=0))
    conditionMatShape = np.shape(trialsEachCond)
    numRepeats = np.product(conditionMatShape[1:])
    nSpikesMat = np.reshape(numSpikesInTimeRangeEachTrial.repeat(numRepeats),
                            conditionMatShape)
    spikesFilteredByTrialType = nSpikesMat * trialsEachCond
    avgSpikesArray = np.sum(spikesFilteredByTrialType,
                            0) / np.sum(trialsEachCond, 0).astype('float')
    return avgSpikesArray






