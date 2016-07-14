
from jaratoolbox import spikesanalysis

#Zscore settings from billy

baseRange = [-0.050,-0.025]              # Baseline range (in seconds)
binTime = baseRange[1]-baseRange[0]         # Time-bin size
responseTimeRange = [-0.5,1]       #Time range to calculate z value for (should be divisible by binTime
responseTime = responseTimeRange[1]-responseTimeRange[0]
numBins = responseTime/binTime
binEdges = np.arange(0,numBins)*binTime  # Edges of bins to calculate response (in seconds)

binEdges = np.arange(responseTimeRange[0], responseTimeRange[1], binTime)



from jaratoolbox.test.nick.database import ephysinterface
reload(ephysinterface)

ei = ephysinterface.EphysInterface('pinp003', '2015-06-30', 'nick', 'laser_tuning_curve')


spikeTimes, eventOnsetTimes = ei.get_processed_session_data('16-56-14', 3, cluster=2)

from jaratoolbox.test.nick.database import sitefuncs
sitefuncs.calculate_isi_violations(spikeTimes) #To calculate the isi violations


timeRange = [-0.5, 1]


(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimes,eventOnsetTimes,timeRange)


[zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange,binEdges) #computes z score for each bin. zStat is array of z scores. maxZ is maximum value of z in timeRange


subplot(211)
ei.plot_session_raster('17-09-09', 3, cluster=2, replace=1)

subplot(212)
plot(zStat)


####################

#LAser pulse session
spikeTimes, eventOnsetTimes = ei.get_processed_session_data('16-48-00', 3, cluster=2)
(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimes,eventOnsetTimes,timeRange)
[zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange,binEdges) #computes z score for each bin. zStat is array of z scores. maxZ is maximum value of z in timeRange
subplot(211)
ei.plot_session_raster('16-48-00', 3, cluster=2, replace=1)
subplot(212)
plot(zStat)


############

#Laser Train session
spikeTimes, eventOnsetTimes = ei.get_processed_session_data('16-50-51', 3, cluster=2)
(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimes,eventOnsetTimes,timeRange)
[zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange,binEdges) #computes z score for each bin. zStat is array of z scores. maxZ is maximum value of z in timeRange
subplot(211)
ei.plot_session_raster('16-50-51', 3, cluster=2, replace=1)
subplot(212)
plot(zStat)
