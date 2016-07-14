from jaratoolbox.test.nick.database import dataloader
reload(dataloader)

from jaratoolbox.test.nick.database import cellDB
reload(cellDB)

from jaratoolbox.test.nick.database import dataplotter
reload(dataplotter)
from jaratoolbox import spikesorting
from jaratoolbox.test.nick import clustercutting
reload(clustercutting)

from pylab import *


loader = dataloader.DataLoader('offline', experimenter='nick')

dbFn = '/home/nick/data/database/nick_thalamus_cells.json'
db = cellDB.CellDB()
db.load_from_json(dbFn)


c = db[0]
spikeData, eventData, behavData = loader.get_cluster_data(c, 'tc_heatmap')

spikeTimes = spikeData.timestamps
eventOnsetTimes = loader.get_event_onset_times(eventData)

figure()
dataplotter.two_axis_heatmap(spikeTimes, eventOnsetTimes, behavData['currentIntensity'], behavData['currentFreq'])
title('All Spikes')
show()

# figure()
# spikesorting.plot_waveforms(spikeData.samples)
# title('all spikes')

# figure()
# dataplotter.plot_raster(spikeTimes, eventOnsetTimes)
# show()

fet = spikesorting.calculate_features(spikeData.samples, ['peak', 'valley', 'energy'])
# fet = spikesorting.calculate_features(spikeData.samples, ['peak'])

cw = clustercutting.AdvancedClusterCutter(spikeData.samples)

cont = raw_input("Press enter to continue")
while cont != '':
    cont = raw_input("Press enter to continue")

    
figure()
dataplotter.two_axis_heatmap(spikeTimes[cw.inCluster], eventOnsetTimes, behavData['currentIntensity'], behavData['currentFreq'])
title('Selected Spikes')
show()

    
