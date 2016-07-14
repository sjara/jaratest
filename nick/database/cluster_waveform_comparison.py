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


c = db[8]
spikeData, eventData, behavData = loader.get_cluster_data(c, 'laserPulse')

spikeTimes = spikeData.timestamps
eventOnsetTimes = loader.get_event_onset_times(eventData)

simple_spike_selector.compare_session_spike_waveforms(spikeData.samples, spikeData.timestamps, eventOnsetTimes, [-0.5, 1], [[-0.2, 0], [0.002, 0.005]])

plt.show()