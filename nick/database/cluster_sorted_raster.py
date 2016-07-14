from jaratoolbox.test.nick.database import simple_spike_selector
reload(simple_spike_selector)

from jaratoolbox.test.nick.database import dataloader
reload(dataloader)

from jaratoolbox.test.nick.database import cellDB
reload(cellDB)

from jaratoolbox.test.nick.database import dataplotter
from jaratoolbox import spikesorting
from jaratoolbox.test.nick import clustercutting

from pylab import *


loader = dataloader.DataLoader('offline', experimenter='nick')

dbFn = '/home/nick/data/database/nick_thalamus_cells.json'
db = cellDB.CellDB()
db.load_from_json(dbFn)


c = db[0]
spikeData, eventData, behavData = loader.get_cluster_data(c, 'tc_heatmap')

spikeTimes = spikeData.timestamps
eventOnsetTimes = loader.get_event_onset_times(eventData)
currentFreq = behavData['currentFreq']
currentIntensity = behavData['currentIntensity']
trialsToPlot = currentIntensity==70
eventOnsetTimes=eventOnsetTimes[trialsToPlot]
currentFreq = currentFreq[trialsToPlot]

dataplotter.plot_raster(spikeTimes, eventOnsetTimes, sortArray=currentFreq)
plt.show()
