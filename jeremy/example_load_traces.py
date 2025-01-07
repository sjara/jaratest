"""
Save voltage trace for an example neuron.
"""

import os
import numpy as np
import json
from matplotlib import pyplot as plt
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import extraplots
import studyparams
import importlib

# -- Data paths --
processedDataDir = '/data/neuropixels'
rawDataDir = '/mnt/My Book/neuropixels/'

nSpikesToExtract = 30

# -- Find cells to load --
dbPath = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath, f'celldb_{studyparams.STUDY_NAME}_spikeSNR.h5')
celldb = celldatabase.load_hdf(dbFilename)

celldb = celldb[celldb.rawDataExists]

#print(celldb[celldb.meanAmplitude<60])
cellsToAnalyze = [1515]  # Low
#cellsToAnalyze = [430]  # High
cellsToAnalyze = [732]  # Mid 596,  732,  799,  837, 1072, 1175, 1225, 1319, 1341, 1377, 1399, 1403, 1489, 1564
cellsToAnalyze = [596,  430, 331, 672]
yLimEachCell = [200,  500, 150, 150]
#print(celldb[(celldb.meanAmplitude>120) & (celldb.meanAmplitude<125)])
# BEST: 430:350uV, 596:125uV, 331:50uV,  672:70uV
celldbToAnalyze = celldb.loc[cellsToAnalyze]

plt.clf()
for indIter, (indRow, dbRow) in enumerate(celldbToAnalyze.iterrows()):
    subject = dbRow['subject']
    sessionDate = dbRow['date']
    sessionTime = dbRow['ephysTime'][0]
    pdepth = dbRow['pdepth']
    session = f'{sessionDate}_{sessionTime}'
    clusterID = dbRow['cluster']
    bestChan = dbRow['bestChannel']
    print(f'[{indRow}] {subject} {session} c{clusterID} CH:{bestChan}')

    multiSessionDir = os.path.join(processedDataDir, subject, f'multisession_{sessionDate}_{pdepth}um_processed')
    singleSessionDir = os.path.join(processedDataDir, subject, f'{session}_processed_multi')
    recDataDir = os.path.join(rawDataDir, subject, session, 'Record Node 101/experiment1/recording1/')
    rawDataFile = os.path.join(recDataDir, 'continuous/Neuropix-PXI-100.0/continuous.dat')
    structFile = os.path.join(recDataDir, 'structure.oebin')

    # -- Load processed data --
    amplitudeAll = np.load(os.path.join(multiSessionDir, 'amplitudes.npy')).squeeze()
    clusters = np.load(os.path.join(singleSessionDir, 'spike_clusters.npy')).squeeze()
    spikeTimesAll = np.load(os.path.join(singleSessionDir, 'spike_times.npy')).squeeze()
    #(nOrigClusters, nTimePoints, nChannels) = templates.shape
    templatesBestChan = np.load(os.path.join(multiSessionDir, 'spike_shapes.npy'))

    templates = np.load(os.path.join(multiSessionDir, 'templates.npy'))
    oneTemplate = templates[clusterID, :, :]
    indMax = np.argmax(np.abs(oneTemplate))
    (sampleMax, chanMax) = np.unravel_index(indMax, oneTemplate.shape)
    
    spikeInds = np.flatnonzero(clusters==clusterID)
    nSpikes = len(spikeInds)
    spikeTimes = spikeTimesAll[spikeInds]
    amplitude = amplitudeAll[spikeInds]
    
    # -- Load raw data --
    with open(structFile, 'r') as file:
        stfile = json.load(file)
    nChannels = stfile['continuous'][0]['num_channels']
    sampleRate = stfile['continuous'][0]['sample_rate']
    bitVolts = stfile['continuous'][0]['channels'][0]['bit_volts']
    rawdata = np.memmap(rawDataFile, dtype='int16', mode='c')
    samplesPerChan = rawdata.shape[0]//nChannels
    rawdata = rawdata.reshape((samplesPerChan, nChannels))
    nSamplesToProcess = 4 * sampleRate  # 2 sec
    #bestChan += -0  #109 #249  # 248
    traceToProcess = rawdata[:nSamplesToProcess, bestChan] * bitVolts
    rawTraceBestChan = rawdata[:, bestChan]
    stDevTrace = np.std(traceToProcess)

    traceToPlot = traceToProcess-np.mean(traceToProcess)

    spikesTimesToPlot = spikeTimes[spikeTimes<nSamplesToProcess]
    nSpikesToPlot = len(spikesTimesToPlot)

    templateBestChan = templatesBestChan[clusterID, :]  # When loading spike_shapes
    nTimePoints = len(templateBestChan)

    # -- Extract window around spikes --
    nSpikesOffset = 20
    firstSample = -30
    lastSample = 50
    spikesTimesToExtract = spikeTimes[nSpikesOffset:nSpikesToExtract+nSpikesOffset]
    spikeTraces = np.empty((nSpikesToExtract, -firstSample+lastSample))
    for inds, spikeTime in enumerate(spikesTimesToExtract):
        #spikeTraces[inds, :] = traceToPlot[int(spikeTime-firstSample):int(spikeTime+lastSample)]
        spikeTraces[inds, :] = rawTraceBestChan[int(spikeTime+firstSample):int(spikeTime+lastSample)]
    spikeTraces *= bitVolts

    if 0:
        plt.clf()
        tvec = np.arange(nSamplesToProcess)  #/sampleRate
        spikeTvec = np.arange(nTimePoints)-nTimePoints//2
        #plt.fill_between([84600, 85600], -stDev, stDev, color='0.75', alpha=1)
        plt.plot(traceToPlot)
        yPos = np.max(traceToPlot)
        plt.plot(spikesTimesToPlot, np.tile(yPos, nSpikesToPlot), '|r')
        #for inds, spikeTime in enumerate(spikesTimesToPlot):
        #    thisAmplitude = amplitude[inds]*amplitudeFactor
        #    plt.plot(tvec[spikeTime+spikeTvec], thisAmplitude*templateNormalized, 'r')
        #plt.xlim(81800, 82100)
        #plt.xlim(84600, 85600)
        plt.show()
    else:
        plt.subplot(2, len(cellsToAnalyze)//2, indIter+1)
        plt.fill_between([0, 80], -stDevTrace, stDevTrace, color='0.75', alpha=1)
        plt.plot(spikeTraces.T, 'k', alpha=0.2, rasterized=True)
        meanSpikeTrace = np.mean(spikeTraces, axis=0)
        extremeVal = np.max(np.abs(meanSpikeTrace))
        print(f'[{indRow}] Extreme value: {extremeVal}')
        plt.plot(meanSpikeTrace, 'w')
        #plt.ylim(-2*extremeVal, 2*extremeVal)
        plt.ylim([-yLimEachCell[indIter], yLimEachCell[indIter]])
        plt.title(f'{indRow} c{clusterID} CH:{bestChan}')
        plt.show()

#extraplots.save_figure('tmp_spike_traces', 'svg', [3, 4], '/tmp/')
