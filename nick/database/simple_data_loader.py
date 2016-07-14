'''
2015-07-31 Nick Ponvert

This file shows how to load a database file, query the database to find certain clusters,
extract the session filenames from the cluster, and use the **DataLoading** object to load the
data.
'''
from jaratoolbox.test.nick.database import dataloader
from jaratoolbox.test.nick.database import cellDB
from jaratoolbox import spikesanalysis
from matplotlib import pyplot as plt
reload(cellDB)
reload(dataloader)

# ----------------------
##Load the database and find a cluster
# ----------------------

dbfile = '/tmp/allcells.json'
db = cellDB.CellDB()
db.load_from_json(dbfile)

cell1 = db.find_cell_from_site('pinp003', '2015-06-24',  3543, 6, 5)

# -----------------------
##Getting the data from a cluster to make a plot
# -----------------------

#Sessions with no behav data return just the ephys
cell1NoisePhys = cell1.get_data_filenames('noiseBurst')

#Sessions with behav data return the tuple (ephysFilename, behavFilename)
cell1TuningPhys, cell1TuningBehavior = cell1.get_data_filenames('tcHeatmap')

# -----------------------
##Initialize an offline data loader
# -----------------------

#For now we still need to specify the experimenter for offline data analysis
#since the behavior data is broken up by experimenter
loader = dataloader.DataLoader('offline', experimenter = 'nick')

# -----------------------
##Get ephys and behavior data by passing the filenames from the cluster
# -----------------------

cell1NoiseSpikesTT6 = loader.get_session_spikes(cell1NoisePhys, 6, cluster=cell1.cluster)
cell1NoiseEvents = loader.get_session_events(cell1NoisePhys)
cell1TuningBdata = loader.get_session_behavior(cell1TuningBehavior)
eventOnsetTimes = loader.get_event_onset_times(cell1NoiseEvents)
spikeTimes = cell1NoiseSpikesTT6.timestamps

# -----------------------
##Make a raster plot
# -----------------------

timeRange = [-0.5, 1]
spikeTimesFromEventOnset, trialIndexEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

# plt.figure()
# plt.plot(spikeTimesFromEventOnset, trialIndexEachSpike, 'k.', ms=2)
# plt.show()

# -----------------------
##The loader still has an online mode for use during ephys experiments
# -----------------------

#Get data online using -1, -2, etc. or by supplying the timestamp
onlineLoader = dataloader.DataLoader('online', 'pinp003', '2015-06-24', 'nick', 'laser_tuning_curve')
onlineSpikes = onlineLoader.get_session_spikes('15-22-29', 6)
onlineEvents = onlineLoader.get_session_events('15-22-29')
onlineBehavior = onlineLoader.get_session_behavior('a')

