import sys; sys.path.append('/home/nick/src')
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os
from jaratoolbox import loadopenephys
from jaratoolbox import settings
from jaratoolbox import spikesanalysis
SAMPLING_RATE=30000.0

db = pd.io.parsers.read_csv('/home/nick/src/jaratest/nick/analysis/test098_celldb_analysis-copy.csv')

db = db[db['date']=='2016-07-28']

cells = db[db['isiViolation']<2.0]

sessions = np.unique(cells['timestamp'])

plt.clf()
plt.hold(1)

tetrodes = range(1, 9)
colors = plt.cm.nipy_spectral(np.linspace(0, 1, len(tetrodes)))

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
        
        plt.plot(indSession, spikeRate, '.', color=colors[int(cell['tetrode'])])
        ratesThisSession.append(spikeRate)
    plt.plot(indSession, np.mean(ratesThisSession), 'ro')


plt.show()


session = '15-30-20'
# session = '15-05-26'
cellsThisSession = cells[cells['timestamp']==session]


plt.clf()
plt.hold(1)
tetrodeOverallData = []

# for tetrode in range(1, 9);
for tetrode in range(1, 9):
    cellsThisTetrode = cellsThisSession[cellsThisSession['tetrode'].astype(int)==tetrode]

    subplot(8, 1, tetrode)

    for indcell, cell in cellsThisTetrode.iterrows():

        #Get data filenames
        ephysPath = os.path.join(settings.EPHYS_PATH,
                                cell['subject'],
                                '{}_{}'.format(cell['date'],cell['timestamp']))
        ephysFn = os.path.join(ephysPath,
                                'Tetrode{}.spikes'.format(int(cell['tetrode'])))
        clusterFn = os.path.join('{}_kk'.format(ephysPath),
                                'Tetrode{}.clu.1'.format(int(cell['tetrode'])))
        eventFn = os.path.join(ephysPath, 'all_channels.events')

        #Load the event data
        dataEvents = loadopenephys.Events(eventFn)
        dataEvents.timestamps = dataEvents.timestamps/SAMPLING_RATE

        #Limit the events to ID 1 and Channel 0
        dataEvents.timestamps = dataEvents.timestamps[((dataEvents.eventID==1) & (dataEvents.eventChannel==0))]

        #Split the events into groups of 100 trials
        splitInds = np.arange(0, len(dataEvents.timestamps), 50)
        splitEvents = np.split(dataEvents.timestamps, splitInds)

        #Load the spike data for this cell
        dataSpikes = loadopenephys.DataSpikes(ephysFn)
        dataSpikes.set_clusters(clusterFn)
        dataSpikes.timestamps = dataSpikes.timestamps[dataSpikes.clusters==int(cell['cluster'])]

        #Make timestamps in seconds
        dataSpikes.timestamps = dataSpikes.timestamps/SAMPLING_RATE
        dataSpikes.samples = dataSpikes.samples[dataSpikes.clusters==int(cell['cluster'])]

        #For this cell, calculate the responsiveness in each period
        baseRange = [-0.050,-0.025]              # Baseline range (in seconds)
        binTime = baseRange[1]-baseRange[0]         # Time-bin size
        responseTimeRange = [-0.5,1]       #Time range to calculate z value for (should be divisible by binTime
        responseTime = responseTimeRange[1]-responseTimeRange[0]
        numBins = responseTime/binTime
        binEdges = np.arange(responseTimeRange[0], responseTimeRange[1], binTime)
        timeRange = [-0.5, 1]

        thisCellZscore = []
        for indsplit, events in enumerate(splitEvents):

            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(dataSpikes.timestamps,events,timeRange)

            [zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                baseRange,
                                                                binEdges)

            thisCellZscore.append(maxZ)

        plot(thisCellZscore, '-o', color = colors[int(cell['tetrode'])-1])

    title('TT{}'.format(tetrode))

ylabel('Max z score in range -0.5 to 1')
xlabel('trial block (50 trials)')

from matplotlib import patches
labels = ['Tetrode {}'.format(ind+1) for ind, color in enumerate(colors)]
patches = [
    patches.Patch(color=color, label=label)
    for label, color in zip(labels, colors)]
legend(patches, labels, loc='north', frameon=False)






# from jaratest.nick.database import ephysinterface
# cell1 = cells.iloc[0]
# ei = ephysinterface.EphysInterface(cell1['subject'], cell1['date'], '', defaultParadigm=cell1['paradigm'], defaultTetrodes=range(1, 9))

# ei.plot_session_raster(cell1['timestamp'], int(cell1['tetrode']), cluster=cell1['cluster'], replace=1)
# ei.plot_session_raster(cell1['timestamp'], int(cell1['tetrode']), replace=1)
ei.plot_session_raster('15-30-20', 6, replace=1)
