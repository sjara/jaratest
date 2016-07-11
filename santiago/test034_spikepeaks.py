'''
Estimate spike shape
'''

from pylab import *
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
#from scipy.interpolate import interp1d
#import sys

# -- Load some spike data --
import allcells_test055 as allcells
cellID = allcells.cellDB.findcell('test055','20150228a',3,11) # 11 #6
oneCell = allcells.cellDB[cellID]

spkData = ephyscore.CellData(oneCell)
waveforms = spkData.spikes.samples.astype(float) - 2**15 # FIXME: this is specific to OpenEphys
samplingRate = spkData.spikes.samplingRate

(peakTimes, peakAmplitudes, avWaveform) = spikesorting.estimate_spike_peaks(waveforms,samplingRate)
timeVec = np.arange(0,len(avWaveform)/samplingRate,1/samplingRate)

clf()
hold(1)
plot(timeVec,avWaveform,'.-')
#plot(interpSampVals,interpSpikeShape,'g-')
axvline(peakTimes[1],ls='--',color='r')
axvline(peakTimes[0],ls='--',color='0.75')
axvline(peakTimes[2],ls='--',color='0.75')
hold(0)
show()

