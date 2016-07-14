# We are having a problem where even gigantic beautiful spikes have a high ISI percentage
# The perfect data illustrating the problem: 2016-05-27_site4_TT2_Cluster8
# The corresponding continuous channel is Ch23 (channel 1 (i.e. the second one) of TT2)

#To convert spikes to mV, you have to divide by the gain, 


from jaratoolbox import loadopenephys
from jaratoolbox import spikesorting
import os

#Data filenames
ephysPath = '/home/nick/data/ephys/pinp013/'
ephysFn='2016-05-27_14-08-54'
contFn = os.path.join(ephysPath, ephysFn, '109_CH23.continuous')
spikesFn = os.path.join(ephysPath, ephysFn, 'Tetrode2.spikes')

#Load data
dataCont = loadopenephys.DataCont(contFn)
dataSpikes = loadopenephys.DataSpikes(spikesFn)

#Convert to microvolts
GAIN = 5000.0
SAMPLING_RATE=30000.0
timebase = np.arange(len(dataCont.samples))/SAMPLING_RATE
dataCont.samples = (dataCont.samples / GAIN) * 1000
dataSpikes.samples = ((dataSpikes.samples - 32768.0) / GAIN) * 1000.0



#Set clusters
clustersFile = os.path.join(ephysPath, '{}_kk'.format(ephysFn), 'Tetrode2.clu.1')
dataSpikes.set_clusters(clustersFile)

#Line the spiketimes up with the cont data timebase and select cluster 8
zeroedSpikeTimes = (dataSpikes.timestamps - dataCont.timestamps[0]) / SAMPLING_RATE
zeroedCluster8 = zeroedSpikeTimes[dataSpikes.clusters==8]


figure()
plot(timebase, dataCont.samples, '0.3')
plot(zeroedSpikeTimes, ones(len(zeroedSpikeTimes)), 'go', ms=10)



c8ISI = diff(zeroedCluster8)
violations = c8ISI < 0.002

spikeDots = zeros(len(zeroedCluster8))

# Plot the ISI violation waveforms
figure()
plot(timebase, dataCont.samples, '0.3')
hold(1)
plot(zeroedCluster8, spikeDots, 'go', ms=10)
plot(zeroedCluster8[violations], spikeDots[violations], 'ro', ms=10)

figure()
plot(timebase, dataCont.samples, '0.3')
hold(1)
plot(zeroedCluster8, spikeDots, 'go', ms=10)
plot(zeroedCluster8[violations], spikeDots[violations], 'ro', ms=10)

## Plot the violation and non-violation waveforms
## This really means that for each violation, we need to plot spike n and spike n+1

violationInds = np.flatnonzero(violations)

cluster8Samples = dataSpikes.samples[dataSpikes.clusters==8]

figure()

#PLot violation and next waves individually
for violation in violationInds:
    clf()
    # subplot(2, 1, 1)

    vWave = ravel(squeeze(cluster8Samples[violation, :, :]))
    nextWave = ravel(squeeze(cluster8Samples[violation+1, :, :]))
    axvline(x=40, color='k', lw=3)
    axvline(x=80, color='k', lw=3)
    axvline(x=120, color='k', lw=3)

    # vWave = ravel(squeeze(cluster8Samples[violation, 1, :]))
    # nextWave = ravel(squeeze(cluster8Samples[violation+1, 1, :]))

    plot(vWave, 'g')
    hold(1)
    plot(nextWave, 'r')

    # subplot(2, 1, 2)
    # waveCorr = np.correlate(vWave, nextWave, 'full')
    # plot(waveCorr)

    waitforbuttonpress()


#Plot violation waves and next waves all at once
vWaves = cluster8Samples[violationInds, :, :]
vWaves = spikesorting.align_waveforms(vWaves)


vnWaves = cluster8Samples[violationInds+1, :, :]
vnWaves = spikesorting.align_waveforms(vnWaves)

figure()
subplot(2, 1, 1)
for wave in vWaves:
    plot(ravel(squeeze(wave)), 'r')
ylabel('microvolts')
subplot(2, 1, 2)
for wave in vnWaves:
    plot(ravel(squeeze(wave)), 'g')
xlabel('Samples (over 4 channels, 40 samples each)')
ylabel('microvolts')
savefig('/tmp/violationWaves.png')







#Need a null distribution of correlations to compare to
#This actually may not be the right approach to take. How to tell if spikes are from the same cell? Have to compare voltages on diff channels I think

nullCorr = zeros(5000)

for i in range(5000):
    waveA = random.randint(len(dataSpikes.samples))
    waveB = random.randint(len(dataSpikes.samples))

    sampleA = ravel(squeeze(dataSpikes.samples[waveA, 1, :]))
    sampleB = ravel(squeeze(dataSpikes.samples[waveB, 1, :]))

    maxCorr = max(np.correlate(sampleA, sampleB, 'full'))

    nullCorr[i] = maxCorr


# maxVolt = zeros((len(dataSpikes.samples), 4))
maxVolt = dataSpikes.samples.max(2)
clf()
plot(maxVolt[:,1], maxVolt[:,2], 'k.', ms=2)



for sample in dataSpikes.samples:






#Plot the average spike waveform for each cluster
# #Spikes.samples (nSpikes, chan, samples)
clusters = [2, 3, 4, 5, 6, 7, 8, 9, 10]

from jaratoolbox.colorpalette import TangoPalette as tango

clusterColors = {6: tango['ScarletRed1'],
                 8: tango['Chameleon1'],
                 5: tango['SkyBlue1'],
                 3: tango['Plum1'],
                 2: tango['Butter1'],
                 4: 'k',
                 9: 'k',
                 7: 'k',
                 10: 'k'}

figure()
for cluster in clusters:
    clusterInds = np.flatnonzero(dataSpikes.clusters==cluster)

    #select just this cluster on second channel and squeeze to (nSpikes, samples)
    clusterWaves =  np.squeeze(dataSpikes.samples[clusterInds, 1, :])

    meanWave = mean(clusterWaves, axis=0)

    plot(meanWave-meanWave[0], label='cluster{}'.format(cluster), color=clusterColors[cluster], lw = 2)
legend()

#PLot the cont data with spiketimes from each spike

#Recording timebase
SAMPLING_RATE=30000.0
timebase = np.arange(len(dataCont.samples))/SAMPLING_RATE

#Plot the cont data
figure()
plot(timebase, dataCont.samples, color='0.3')
hold(1)

for cluster in clusters:
    zeroedClusterTimes = zeroedSpikeTimes[dataSpikes.clusters==cluster]
    plot(zeroedClusterTimes, ones(len(zeroedClusterTimes)), marker='o', color=clusterColors[cluster], ms=10, linestyle='None')







#BANDPASS FILTERING

from scipy import signal

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y


filteredSignal = butter_bandpass_filter(dataCont.samples, 300, 6000, SAMPLING_RATE)

thresholdLevel = -110

plot(timebase, filteredSignal, '0.4')
axhline(thresholdLevel, color='r')
plot(zeroedSpikeTimes, ones(len(zeroedSpikeTimes))*thresholdLevel, 'o', color='r')



