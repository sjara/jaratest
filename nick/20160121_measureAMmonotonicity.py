from jaratoolbox.test.nick.database import cellDB
from jaratoolbox.test.nick.database import dataloader
from jaratoolbox.test.nick.database import dataplotter
from jaratoolbox import behavioranalysis



dbFn ='/home/nick/data/database/amdatabase.json'

db = cellDB.CellDB()

db.load_from_json(dbFn)


loader = dataloader.DataLoader('offline', experimenter='nick')


spikeData, eventData, behavData = loader.get_cluster_data(db[0], sessionType='AM')


spikeTimestamps = spikeData.timestamps
eventOnsetTimes = loader.get_event_onset_times(eventData)
currentFreq = behavData['currentFreq']

plt.clf()
dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray = currentFreq)
plt.show()



trialsEachCond = behavioranalysis.find_trials_each_type(currentFreq, np.unique(currentFreq))

timeRange=[0, 0.5]
spikeArray = dataplotter.avg_spikes_in_event_locked_timerange_each_cond(spikeTimestamps, trialsEachCond, eventOnsetTimes, timeRange)

#The firing rate over the length of the stimulus is non-monotonic
plot(spikeArray)

plot(log(unique(currentFreq)), spikeArray)

