"""
Create a database of cells from neuropixels data.
"""

import sys
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import spikesanalysis
from jaratoolbox import settings

#from jaratoolbox import ephyscore_npix as ephyscore
#from jaratoolbox import celldatabase_npix as celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import celldatabase

import importlib
importlib.reload(celldatabase)
importlib.reload(ephyscore)

# pd.set_option("display.max_rows", None)

inforecFile = os.path.join(settings.INFOREC_PATH,'npix000_inforec.py')
celldb = celldatabase.generate_cell_database(inforecFile)

#celldatabase.save_hdf(celldb, '/tmp/testdb.h5')
#df = celldatabase.load_hdf('/tmp/testdb.h5')
'''
clustersToShow = [200] # 267 
subcelldb = celldb[celldb.cluster.isin(clustersToShow)]


plt.clf()
indplot = 1
for indRow, dbRow in subcelldb.iterrows():
    oneCell = ephyscore.Cell(dbRow)
    ephysData, bdata = oneCell.load('FT')
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.2, 0.8]
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)
#    plt.subplot(5, 2, indplot)
    plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.k', markersize=3)
    if indplot>8:
        plt.xlabel('Time (s)')
    else:
        plt.gca().set_xticklabels('')
    plt.ylabel('Trials')
    plt.xlim(timeRange)
    plt.title(oneCell)
    print(oneCell)
    plt.show()
    indplot += 1
plt.gcf().set_size_inches([8.5, 11])
plt.tight_layout()
#plt.savefig('/tmp/feat001_2021-11-09_examples.png', format='png')

sys.exit()
'''

for indRow, dbRow in celldb.iterrows():


    plt.clf()
    indplot = 1
    oneCell = ephyscore.Cell(dbRow)
    ephysData, bdata = oneCell.load('VOT')
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.2, 0.8]
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)
    plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.k', markersize=3)
    if indplot>8:
        plt.xlabel('Time (s)')
    else:
        plt.gca().set_xticklabels('')
    plt.ylabel('Trials')
    plt.xlim(timeRange)
    plt.title(oneCell)
    print(oneCell)
    plt.show()
    input("press enter for next cell")
    indplot += 1
#plt.gcf().set_size_inches([8.5, 11])
plt.tight_layout()

#plt.savefig('/tmp/feat001_2021-11-09_examples.png', format='png')

sys.exit()


'''
plt.clf()
for indRow,dbRow in celldb.iterrows():
    oneCell = ephyscore.Cell(dbRow)
    ephysData, bdata = oneCell.load('AMtest')
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.2, 0.8]
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    plt.cla()
    plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.k', markersize=3)
    plt.ylabel('Trials')
    plt.xlabel('Time (s)')
    plt.xlim(timeRange)
    plt.title(oneCell)
    print(oneCell)
    plt.show()
    plt.pause(0.5)
    #input('Press ENTER')
sys.exit()
'''

'''
cellDict = {'subject': 'feat001',
            'date': '2021-11-09',
            'pdepth': 3242,
            'egroup': 0,
            'cluster': 270}

cellInd, dbRow = celldatabase.find_cell(celldb, **cellDict)
oneCell = ephyscore.Cell(dbRow)

#bdata = oneCell.load_behavior_by_index(0)
#ephysData = oneCell.load_ephys_by_index(0)
ephysData, bdata = oneCell.load('AMtest')

spikeTimes = ephysData['spikeTimes']
eventOnsetTimes = ephysData['events']['stimOn']
timeRange = [-0.2, 0.8]

(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

plt.clf()
plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.k', markersize=3)
plt.ylabel('Trials')
plt.xlabel('Time (s)')
#plt.gcf().set_size_inches([12, 2.28])
plt.tight_layout()
plt.show()

sys.exit()
'''

'''
inforec = celldb
experiment = inforec.experiments[0]
site = experiment.sites[0]

clusterFolder = os.path.join(settings.EPHYS_NEUROPIX_PATH,
                             inforec.subject, site.clusterFolder)
clusterGroupFile = os.path.join(clusterFolder, 'cluster_group.tsv')
clusterGroup = pd.read_csv(clusterGroupFile, sep='\t')

def loadfile(filename):
    return np.load(os.path.join(clusterFolder,filename))

#amps = loadfile('amplitudes.npy').squeeze()
spikeClusters = np.load(os.path.join(clusterFolder,'spike_clusters.npy')).squeeze()
clusterGroupFile = os.path.join(clusterFolder, 'cluster_group.tsv')
clusterGroup = pd.read_csv(clusterGroupFile, sep='\t')

celldb = clusterGroup.query("KSLabel=='good'").reset_index(drop=True)
templates = np.load(os.path.join(clusterFolder,'templates.npy'))
(nClusters, nTimePoints, nChannels) = templates.shape
spikeShapes = np.empty([nClusters, nTimePoints], dtype=templates.dtype)
nSpikes = np.empty(len(celldb), dtype=int)
for indc, clusterID in enumerate(celldb['cluster_id']):
    oneTemplate = templates[clusterID]
    indMax = np.argmax(np.abs(oneTemplate))
    (rowMax, colMax) = np.unravel_index(indMax, oneTemplate.shape)
    #clusterDict = {'spikeShape': oneTemplate[:,colMax],
    #               'nSpikes': np.sum(spikeClusters==clusterID)}
    #celldb = celldb.append(clusterDict, ignore_index=True)
    spikeShapes[indc,:] = oneTemplate[:,colMax]
    #celldb['spikeShapes'][indc] = oneTemplate[:,colMax]
    nSpikes[indc] = np.sum(spikeClusters==clusterID)
celldb['nSpikes'] = nSpikes
#celldb['spikeShapes'] = spikeShapes
'''


'''
for indTemplate, oneTemplate in enumerate(templates):
    oneTemplate = templates[indTemplate]
    indMax = np.argmax(np.abs(oneTemplate))
    (rowMax, colMax) = np.unravel_index(indMax, oneTemplate.shape)
    spikeShapes[indTemplate,:] = oneTemplate[:,colMax]
    nSpikes[indTemplate] = np.sum(spikeClusters==indTemplate)
'''
#spikeClustersFile = os.path.join(clusterFolder, 'spike_clusters.npy')
#clusters = np.load(spikeClustersFile).squeeze()

#for indTemplate, oneTemplate in enumerate(templates):
          
'''
inforecPath = inforecFile
#inforec = importlib.import_module('inforec_module', inforecPath)
spec = importlib.util.spec_from_file_location('inforec_module', inforecPath)
inforec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inforec)
'''
sys.exit()

cellDict = {'subject' : 'chad010',
            'date' : '2019-02-17',
            'depth' : 1250,
            'tetrode' : 2,
            'cluster' : 4}

cellInd, dbRow = celldatabase.find_cell(celldb, **cellDict)
oneCell = ephyscore.Cell(dbRow)
ephysData, bdata = oneCell.load('noiseburst')





rawDataDir = '/data/neuropixels/pals027/2021-11-09_14-16-37'
spikesDataDir = rawDataDir+'_processed/'

convertUnits = True
spikes = loadneuropix.Spikes(spikesDataDir, convert=convertUnits)
events = loadneuropix.Events(rawDataDir, convert=convertUnits)
eventOnsetTimes = events.get_onset_times()

timeRange = [-0.2, 0.8]
(spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikes.timestamps, eventOnsetTimes, timeRange)

plt.clf()
plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.k', markersize=1)
plt.show()


'''
import os
import numpy as np
import pandas as pd

spikeTimesFile = os.path.join(dataDir, 'spike_times.npy')
spikeClustersFile = os.path.join(dataDir, 'spike_clusters.npy')
clusterGroupFile = os.path.join(dataDir, 'cluster_group.tsv')

timestamps = np.load(spikeTimesFile).squeeze()
clusters = np.load(spikeClustersFile).squeeze()
clusterGroup = pd.read_csv(clusterGroupFile, sep='\t')
'''

'''
            spikeShapes = np.empty([nGoodClusters, nTimePoints], dtype=templates.dtype)
            nSpikes = np.empty(nGoodClusters, dtype=int)
            bestChannel = np.empty(nGoodClusters, dtype=int)
            for indc, clusterID in enumerate(tempdb['cluster_id']):
                oneTemplate = templates[clusterID]
                indMax = np.argmax(np.abs(oneTemplate))
                (rowMax, colMax) = np.unravel_index(indMax, oneTemplate.shape)
                spikeShapes[indc,:] = oneTemplate[:,colMax]
                bestChannel[indc] = colMax
                nSpikes[indc] = np.sum(spikeClusters==clusterID)
            tempdb['nSpikes'] = nSpikes
            tempdb['bestChannel'] = bestChannel
            tempdb['maxDepth'] = maxDepthThisExp
            celldb = celldb.append(tempdb, ignore_index=True)

'''


'''
            for indc, clusterID in enumerate(tempdb['cluster_id']):
                # -- Get best channel and spikeshape --
                oneTemplate = templates[clusterID]
                indMax = np.argmax(np.abs(oneTemplate))
                (bestChannel, timePointMax) = np.unravel_index(indMax, oneTemplate.shape)
                spikeShape = oneTemplate[:, bestChannel]
                clusterDict = {'cluster': clusterID,
                               'KSLabel': tempdb['KSLabel'][indc],
                               'maxDepth': maxDepthThisExp,
                               'bestChannel': bestChannel,
                               'nSpikes': np.sum(spikeClusters==clusterID)}
                clusterDict.update(site.cluster_info())
                celldb = celldb.append(clusterDict, ignore_index=True)
'''
                
'''
            for indTemplate, oneTemplate in enumerate(templates):
                indMax = np.argmax(np.abs(oneTemplate))
                (rowMax, colMax) = np.unravel_index(indMax, oneTemplate.shape)
                spikeShapes[indTemplate,:] = oneTemplate[:,colMax]
                clusterDict = {'maxDepth': maxDepthThisExp,
                               'cluster': indTemplate,
                               'nSpikes': 0,
                               }
                celldb = celldb.append(clusterDict, ignore_index=True)
'''
'''
            for indc, cluster in enumerate(clusterStats['clusters']):
                # Calculate cluster shape quality
                clusterPeakAmps = clusterStats['clusterPeakAmplitudes'][indc]
                clusterSpikeSD = clusterStats['clusterSpikeSD'][indc]
                clusterShapeQuality = abs(clusterPeakAmps[1]/clusterSpikeSD.mean())
                clusterDict = {'maxDepth': maxDepthThisExp,
                               'tetrode': tetrode,
                               'cluster': cluster,
                               'nSpikes': clusterStats['nSpikes'][indc],
                               'isiViolations': clusterStats['isiViolations'][indc],
                               'spikeShape': clusterStats['clusterSpikeShape'][indc],
                               'spikeShapeSD': clusterSpikeSD,
                               'spikePeakAmplitudes': clusterPeakAmps,
                               'spikePeakTimes': clusterStats['clusterPeakTimes'][indc],
                               'spikeShapeQuality': clusterShapeQuality}
                clusterDict.update(site.cluster_info())
                celldb = celldb.append(clusterDict, ignore_index=True)
'''
# NOTE: This is an ugly way to force these columns to be int. Will fix in future if possible
#celldb['tetrode'] = celldb['tetrode'].astype(int)
#celldb['cluster'] = celldb['cluster'].astype(int)
#celldb['nSpikes'] = celldb['nSpikes'].astype(int)

