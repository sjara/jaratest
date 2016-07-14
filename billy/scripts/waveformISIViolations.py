from jaratoolbox import settings
from jaratoolbox import loadopenephys
import numpy as np
import os
from pylab import *
from jaratoolbox import spikesorting
reload(spikesorting)
from jaratoolbox import loadbehavior
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
import matplotlib.pyplot as plt
import sys
import importlib
import re


mouseName   = 'test089'
behavSession = '20150803a'
#ephysSession = '2015-07-31_14-40-40'
tetrode = 2
cluster = 11

channel_to_plot = 0 #which channel on tetrode to plot waveforms

allcellsFileName = 'allcells_'+mouseName
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)


ISIcutoff = 0.002

SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
ephysRootDir = settings.EPHYS_PATH



def waveformPlot(waveform1,waveform2):
    plt.subplot(211)
    plt.plot(waveform1)
    plt.subplot(212)
    plt.plot(waveform2)
    plt.show()


cellID = allcells.cellDB.findcell(mouseName,behavSession,tetrode,cluster)
oneCell = allcells.cellDB[cellID]
'''
ephysDir = os.path.join(ephysRoot, ephysSession)
eventFilename=os.path.join(ephysDir, 'all_channels.events')
events = loadopenephys.Events(eventFilename) # Load events data
eventTimes=np.array(events.timestamps)/SAMPLING_RATE 

soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)

eventOnsetTimes = eventTimes[soundOnsetEvents]
'''


spkData = ephyscore.CellData(oneCell)
spkTimeStamps = spkData.spikes.timestamps

ISI = np.diff(spkTimeStamps)

if np.any(ISI<0):
    raise 'Times of events are not ordered (or there is at least one repeated).'
if len(ISI)==0:  # Hack in case there is only one spike
    ISI = np.array(10)

ISIVioBool = ISI<ISIcutoff

fractionViolation = np.mean(ISIVioBool) # Assumes ISI in usec

print 'ISI Violation less than ',ISIcutoff,' is ',fractionViolation

ISIVioBoolFirst = np.append(ISIVioBool,False)
ISIVioBoolSecond = np.append(False,ISIVioBool)

dataDir = os.path.join(settings.EPHYS_PATH,mouseName,oneCell.ephysSession)
tetrodeFile = os.path.join(dataDir,'Tetrode{0}.spikes'.format(tetrode))
clustersDir = os.path.join(settings.EPHYS_PATH,mouseName,oneCell.ephysSession+'_kk')

dataTT = loadopenephys.DataSpikes(tetrodeFile) #,readWaves=True)
dataTT.samples = dataTT.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
# FIXME: This assumes the gain is the same for all channels and records
dataTT.samples = (1000.0/dataTT.gain[0,0]) * dataTT.samples
dataTT.timestamps = dataTT.timestamps/dataTT.samplingRate
clustersFile = os.path.join(clustersDir,'Tetrode%d.clu.1'%tetrode)
if os.path.isfile(clustersFile):
    dataTT.set_clusters(clustersFile)
else:
    print('Clusters file does not exist for this tetrode: {0}'.format(tetrode))

fetFilename = os.path.join(clustersDir,'Tetrode%d.fet.1'%tetrode)
fetFile = open(fetFilename, 'r')

numFetclusters = fetFile.readline()
fetList = fetFile.read().split('\n')

for indF,fet in enumerate(fetList):
    fetList[indF] = fet.split()

fetList = np.asarray(fetList[:-1])

waveFet = fetList[dataTT.clusters == cluster]



waveforms = dataTT.samples[dataTT.clusters == cluster]

waveforms_first = waveforms[ISIVioBoolFirst]
waveforms_second = waveforms[ISIVioBoolSecond]

#ax4 = plt.subplot2grid((1,2), (0,0), colspan = (numCols/2), rowspan = sizeRasters)
#raster_sound_block_switching()
#ax5 = plt.subplot2grid((numRows,numCols), (sizeRasters,0), colspan = (numCols/2), rowspan = sizeHists)
#hist_sound_block_switching()


nISIVio = len(waveforms_first)
allWaves  = []
for indISI in range(nISIVio):
    allWaves.append((waveforms_first[indISI][channel_to_plot],waveforms_second[indISI][channel_to_plot]))
#alldata.append((spikeTimesFromEventOnset, sortedIndexForEachSpike,meanSpikesEachFrequency,possibleFreq,responseRange,tetrodeID))
flipPlots = extraplots.FlipThrough(waveformPlot,allWaves)
