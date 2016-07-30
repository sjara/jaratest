import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os
from jaratoolbox import loadopenephys
from jaratoolbox import settings
SAMPLING_RATE=30000.0

db = pd.io.parsers.read_csv('/home/jarauser/src/jaratest/nick/analysis/test098_celldb_analysis-copy.csv')

db = db[db['date']=='2016-07-28']

cells = db[db['isiViolation']<2.0]

sessions = np.unique(cells['timestamp'])

plt.figure()
plt.hold(1)

for indSession, session in enumerate(sessions):
    cellsThisSession = cells[cells['timestamp']==session]
    ratesThisSession = []

    #The stuff below all looks pretty boilerplate
    for indCell, cell in cellsThisSession.iterrows():
        ephysPath = os.path.join(settings.EPHYS_PATH,
                               cell['subject'],
                               '{}_{}'.format(cell['date'],cell['timestamp']))
        ephysFn = os.path.join(ephysPath,
                               'Tetrode{}.spikes'.format(int(cell['tetrode'])))
        clusterFn = os.path.join('{}_kk'.format(ephysPath),
                               'Tetrode{}.clu.1'.format(int(cell['tetrode'])))
                                   
        dataSpikes = loadopenephys.DataSpikes(ephysFn)
        dataSpikes.set_clusters(clusterFn)
        dataSpikes.timestamps = dataSpikes.timestamps[dataSpikes.clusters==int(cell['cluster'])]
        #Make timestamps in seconds
        dataSpikes.timestamps = dataSpikes.timestamps/SAMPLING_RATE
        dataSpikes.samples = dataSpikes.samples[dataSpikes.clusters==int(cell['cluster'])]

        startTime = dataSpikes.timestamps[0]
        endTime = dataSpikes.timestamps[-1]
        sessionLength = endTime - startTime
        nSpikes = len(dataSpikes.timestamps)
        spikeRate = nSpikes/np.double(sessionLength)
        
        plt.plot(indSession, spikeRate, 'k.')
        ratesThisSession.append(spikeRate)
    plt.plot(indSession, np.mean(ratesThisSession), 'ro')


plt.show()
