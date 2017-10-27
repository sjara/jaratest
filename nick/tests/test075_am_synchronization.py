import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib import pyplot as plt
import scipy.signal
from jaratoolbox import spikesanalysis

def rayleigh_test(r, n):
    #r (mean vector length) comes from the vectorstrength calculation (as strength)
    #Rayleigh's R statistic = n (number of samples) * r (mean vector length)
    #The probability of R is approximated by:
    # R = n*r
    # P = exp[ sqrt( 1+4*n+4(n**2 - R**2) ) - (1+2*n) ]
    # From Biostatistical Analysis, Zar, 3rd edition eq 26.4, cites Greenwood and Durand, 1955
    R = n*r
    p = np.exp( np.sqrt( 1+4*n+4*(n**2 - R**2) ) - (1+2*n) )
    return p

plt.clf()
gs = gridspec.GridSpec(3, 3)
timeRange = [-1, 6]

# Fake data
# Freq of stimulus is 1Hz
# Clean spike data, 100% synchronized

period = 1 #1 second per cycle
freq = 1.0/period

#Number of radians in one second of the stimulus
radsPerSec=freq*2*np.pi

#Event times for plotting rasters
eventOnsetTimes = np.arange(0, 100, period*5)


### -- Clean data -- ###

cleanData = np.arange(0, 100, period)

# spikeTimestamps = cleanData
(spikeTimesFromEventOnset,
trialIndexForEachSpike,
indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(cleanData,
                                                             eventOnsetTimes,
                                                              timeRange)
#The value of each spike in radians, relative to the beginning of the cycle
#spikeTimestamps in seconds, times radsPerSec gives radians for each spike.
#Mod 2pi to make relative to beginning of envelope
spikeRads = (cleanData*radsPerSec)%(2*np.pi)
strength, phase = scipy.signal.vectorstrength(cleanData, period)

p = rayleigh_test(strength, len(cleanData))

ch1 = plt.subplot(gs[0, 0], projection='polar')
ch1.hist(spikeRads, bins=50)

r1 = plt.subplot(gs[0, 1:3])
r1.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')
plt.xlim([-1, 6])
plt.title('VS = {}, p = {}'.format(strength, p))


### -- Noisy data -- ###
jitter = np.random.randn(len(cleanData)) * (0.1 * period)
noisyData = cleanData + jitter

(spikeTimesFromEventOnset,
trialIndexForEachSpike,
indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(noisyData,
                                                             eventOnsetTimes,
                                                             timeRange)

#The value of each spike in radians, relative to the beginning of the cycle
#spikeTimestamps in seconds, times radsPerSec gives radians for each spike.
#Mod 2pi to make relative to beginning of envelope
spikeRads = (noisyData*radsPerSec)%(2*np.pi)
strength, phase = scipy.signal.vectorstrength(noisyData, period)

p = rayleigh_test(strength, len(noisyData))

ch2 = plt.subplot(gs[1, 0], projection='polar')
ch2.hist(spikeRads, bins=50)

r2 = plt.subplot(gs[1, 1:3])
r2.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')
plt.xlim([-1, 6])
plt.title('VS = {}, p = {}'.format(strength, p))

### -- REALLY noisy data -- ###
jitter = np.random.randn(len(cleanData)) * (0.5 * period)
reallyNoisyData = cleanData + jitter

(spikeTimesFromEventOnset,
trialIndexForEachSpike,
indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(reallyNoisyData,
                                                             eventOnsetTimes,
                                                             timeRange)
spikeRads = (reallyNoisyData*radsPerSec)%(2*np.pi)
strength, phase = scipy.signal.vectorstrength(reallyNoisyData, period)

p = rayleigh_test(strength, len(reallyNoisyData))

ch3 = plt.subplot(gs[2, 0], projection='polar')
ch3.hist(spikeRads, bins=50)
r3 = plt.subplot(gs[2, 1:3])
r3.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')
plt.xlim([-1, 6])
plt.title('VS = {}, p = {}'.format(strength, p))

plt.tight_layout()
plt.show()
