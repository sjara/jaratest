import os, sys
import pdb
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import celldatabase
from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import ephyscore
reload(loadopenephys)
from jaratoolbox import settings



subject = 'dapa008'
dbpath = '/home/jarauser/data/databases/{}_clusterdatabase.h5'.format(subject)
db = pd.read_hdf(dbpath, key='database')

# Select the good, isolated cells from the database
goodCells = db.query('isiViolations < 0.02')
#print(goodCells.loc[223])

cellInd = 223

dbRow = db.loc[cellInd]

#Create a cell object using the database row
cell = ephyscore.Cell(dbRow)
print(cell['IndExperiment'])

sys.exit()

def plot_report(): 
    plt.figure()

    gs = gridspec.GridSpec(2, 2)

    #Plot noiseburst raster
    plt.subplot(gs[0, 0])

    ephysData, bdata = cell.load('noisebursts')    

    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimeStamps = ephysData['spikeTimes']
    timeRange = [-0.1, 1.0]

    trialsEachCond = []

    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
            spikeTimeStamps, eventOnsetTimes, timeRange)

    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                                   trialsEachCond=trialsEachCond)

    xlabel = 'time (s)'
    ylabel = 'Trial'

    plt.title('Noise')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    #Plot tuning curve raster
    plt.subplot(gs[0, 1])

    ephysData, bdata = cell.load('tuningCurve')    

    freqEachTrial = bdata['currentFreq']

    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimeStamps = ephysData['spikeTimes']
    timeRange = [-0.1, 1.0]

    possiblefreqs = np.unique(freqEachTrial)
    freqLabels = [round(x/1000, 1) for x in possiblefreqs]

    trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, possiblefreqs)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
            spikeTimeStamps, eventOnsetTimes, timeRange)

    #print len(freqEachTrial), len(eventOnsetTimes)



    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                                   trialsEachCond=trialsEachCond, labels=freqLabels)


    xlabel = 'time (s)'
    ylabel = 'Trial'

    plt.title('Tuning Curve')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    #show cluster analysis
    #tsThisCluster, wavesThisCluster = load_cluster_waveforms(cellInfo)
    idString = 'exp{}site{}'.format(dbRow['experimentInd'],cellInfo['siteInd'])
    oneTT = cms2.MultipleSessionsToCluster(cellInfo['subject'], cellInfo['ephysDirs'], cellInfo['tetrode'], idString)
    oneTT.load_all_waveforms()
    clusterFile = os.path.join(oneTT.clustersDir,'Tetrode%d.clu.1'%oneTT.tetrode)
    oneTT.set_clusters_from_file()
    tsThisCluster = oneTT.timestamps[oneTT.clusters==cellInfo['cluster']]
    wavesThisCluster = oneTT.samples[oneTT.clusters==cellInfo['cluster']]
    return tsThisCluster, wavesThisCluster

    # -- Plot ISI histogram --
    plt.subplot(gs[1, 0])
    spikesorting.plot_isi_loghist(tsThisCluster)
    plt.ylabel('c%d'%cellInfo['cluster'],rotation=0,va='center',ha='center')
    plt.xlabel('')

    # -- Plot waveforms --
    plt.subplot(gs[0, 1])
    spikesorting.plot_waveforms(wavesThisCluster)

    #plt.setp(pRaster, ms=ms)
    print("Saving Cell " + str(cellInd))
    #figname = '/home/jarauser/data/reports_alex/dapa008/test/{}_{}_depth{}_T{}_C{}.png'.format(dbRow['date'], dbRow['ephysTime'][sessionInd], int(dbRow['depth']), dbRow['tetrode'], dbRow['cluster'])
    figname = '/home/jarauser/data/reports_alex/dapa008/test/test.png'
    plt.savefig(figname)

    plt.clf()
    #plt.show()

### PUT THIS INTO CODE
def load_cluster_waveforms(cellInfo):
    idString = 'exp{}site{}'.format(cellInfo['experimentInd'],cellInfo['siteInd'])
    oneTT = cms2.MultipleSessionsToCluster(cellInfo['subject'], cellInfo['ephysDirs'], cellInfo['tetrode'], idString)
    oneTT.load_all_waveforms()
    clusterFile = os.path.join(oneTT.clustersDir,'Tetrode%d.clu.1'%oneTT.tetrode)
    oneTT.set_clusters_from_file()
    tsThisCluster = oneTT.timestamps[oneTT.clusters==cellInfo['cluster']]
    wavesThisCluster = oneTT.samples[oneTT.clusters==cellInfo['cluster']]
    return tsThisCluster, wavesThisCluster

sys.exit()
#######################################################
for ind in db.index:
    if ind != 339:
        continue
    #Regular tuning curves are good cells 78
    #laser trials are good cells x133, x154, 155(not just artifacts), x161
    thisCell = db.loc[ind]
    tetrode = int(thisCell['tetrode'])
    cluster = int(thisCell['cluster'])
    depth = int(thisCell['depth'])
    if len(thisCell['behavior'])<2:
      continue
    behavFileName = thisCell['behavior'][1]
    session = thisCell['ephys'][1]

    ###############CURRENT POSITION - NEED CELL TO ANALYZE#################

    #Load ephys data
    ephysBaseDir = os.path.join(settings.EPHYS_PATH, subject)
    eventFilename=os.path.join(ephysBaseDir,
                               session,
                               'all_channels.events')
    spikesFilename=os.path.join(ephysBaseDir,
                                session,
                                'Tetrode{}.spikes'.format(tetrode))
    eventData=loadopenephys.Events(eventFilename)
    spikeData = loadopenephys.DataSpikes(spikesFilename)
    clustersDir = os.path.join(ephysBaseDir, '{}_kk'.format(session))
    clustersFile = os.path.join(clustersDir,'Tetrode{}.clu.1'.format(tetrode))
    spikeData.set_clusters(clustersFile)
    if cluster is not None:
        spikeData.samples=spikeData.samples[spikeData.clusters==cluster]
        spikeData.timestamps=spikeData.timestamps[spikeData.clusters==cluster]

    # convert to seconds and millivolts
    spikeData.samples = spikeData.samples.astype(float)-2**15
    spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
    spikeData.timestamps = spikeData.timestamps/spikeData.samplingRate
    eventData.timestamps = eventData.timestamps/eventData.samplingRate


    behavFile = os.path.join(settings.BEHAVIOR_PATH,subject,behavFileName)
    bdata = loadbehavior.BehaviorData(behavFile,readmode='full')


    # LOAD YOUR SHIT
    #eventData, spikeData = load_ephys_data(subject, session, tetrode, cluster)
    eventOnsetTimes = eventData.get_event_onset_times()
    spikeTimeStamps = spikeData.timestamps
    tuningBData = bdata   

    #laser = tuningBData['laserOn']
    freqEachTrial = tuningBData['currentFreq']


    timeRange = [-0.1, 1.0]

    possiblefreqs = np.unique(freqEachTrial)

    trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, possiblefreqs)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeTimeStamps, eventOnsetTimes, timeRange)

    #print len(freqEachTrial), len(eventOnsetTimes)



    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                                   trialsEachCond=trialsEachCond, labels=possiblefreqs)


    xlabel = 'time (s)'
    ylabel = 'Trial'

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    #plt.setp(pRaster, ms=ms)
    print("Saving Cell " + str(ind))
    figname = '/home/jarauser/data/reports_alex/dapa007/' + str(session) + '_depth' + str(depth) + '_T' + str(tetrode) + '_C' + str(cluster) +'.png'
    plt.savefig(figname)
    
    plt.clf()
    #plt.show()

