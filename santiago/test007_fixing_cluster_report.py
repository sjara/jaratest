'''
Fixing issues with the cluster report.
'''

from jaratoolbox import spikesorting
reload(spikesorting)

CASE = 1

if CASE==1:
    animalName = 'test030'
    ephysSession = '2014-06-25_18-33-30_TT6goodGND'
    tetrode = 6

oneTT = spikesorting.TetrodeToCluster(animalName,ephysSession,tetrode)

'''
oneTT.create_fet_files()
oneTT.run_clustering()
'''

'''
self.dataTT = loadopenephys.DataSpikes(self.tetrodeFile) #,readWaves=True)
self.nSpikes = self.dataTT.nRecords# FIXME: this is specific to the OpenEphys format
self.dataTT.samples = self.dataTT.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
self.dataTT.timestamps = self.dataTT.timestamps/self.dataTT.samplingRate
'''

oneTT.save_report()

'''
    if timeZero is None:
        timeZero = timeStamps[0]
'''

'''
# -- Align waveforms --
from pylab import *
oneTT.load_waveforms()
waveforms = oneTT.dataTT.samples[12:20,:,:]
subplot(2,1,1)
plot(waveforms[:,0,:].T); show()

meanWaveforms = np.mean(waveforms,axis=0)
minEachChan = meanWaveforms.min(axis=1)
minChan = argmin(minEachChan)

minSampleEachSpike = waveforms[:,minChan,:].argmin(axis=1)
print minSampleEachSpike

peakPosition = 8
wavesToShift = flatnonzero(minSampleEachSpike!=peakPosition)
for indw in wavesToShift:
    waveforms[indw,:,:] = np.roll(waveforms[indw,:,:],peakPosition-minSampleEachSpike[indw],axis=1)
subplot(2,1,2)
plot(waveforms[:,0,:].T); show()
'''

'''
#[nSpikes,nChan,nSamples]
maxEachChan = abs(waveforms).max(axis=2)
maxChan = maxEachChan.argmax(axis=1)
waveforms[:,maxChan,:]
'''
