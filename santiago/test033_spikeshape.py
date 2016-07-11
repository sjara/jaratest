'''
Estimate spike shape
'''

from pylab import *
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from scipy.interpolate import interp1d
import sys

'''
animalName = 'test055'
ephysSession = '20150228a'
tetrode = 3
cluster = 11
'''

# -- Load some spike data --
import allcells_test055 as allcells
cellID = allcells.cellDB.findcell('test055','20150228a',3,9) # 11 #6
oneCell = allcells.cellDB[cellID]

spkData = ephyscore.CellData(oneCell)
waveforms = spkData.spikes.samples
samplingRate = spkData.spikes.samplingRate

# -- Align waveforms --
waveforms = spikesorting.align_waveforms(waveforms)

# -- Get spike shape --
N_INTERP_SAMPLES = 200
avWaveforms = np.mean(waveforms,0)
avWaveforms = avWaveforms - 2**15 # FIXME: this is specific to OpenEphys
energyEachChannel = np.sum(np.abs(avWaveforms),1)
maxChannel = np.argmax(energyEachChannel)
spikeShape = avWaveforms[maxChannel,:]
sampVals = np.arange(0,len(spikeShape)/samplingRate,1/samplingRate)

interpFun = interp1d(sampVals, spikeShape, kind='cubic')
interpSampVals = np.linspace(0,sampVals[-1],N_INTERP_SAMPLES)
interpSpikeShape = interpFun(interpSampVals)

# NOTE: the peaks of the action potential are: (1) capacitive, (2) Na+, (3) K+
peakNaSample = np.argmin(interpSpikeShape)
peakNaTime = interpSampVals[peakNaSample]


'''
### Old way, uses min and max values ###
#peakCapSample = np.argmax(interpSpikeShape[:peakNaSample])
peakCapSample = np.argmin(np.diff(np.diff(interpSpikeShape[:peakNaSample])))
peakCapTime = interpSampVals[peakCapSample]
#peakKSample = np.argmax(interpSpikeShape[peakNaSample:])+peakNaSample
peakKSample = np.argmin(np.diff(np.diff(interpSpikeShape[peakNaSample:])))+peakNaSample
peakKTime = interpSampVals[peakKSample]
'''

# -- Calculate the change in sign of slope (and pad to align to original vector)
dsign = np.r_[0,np.diff(np.sign(np.diff(interpSpikeShape)))]

extremePointsPre = flatnonzero(dsign[0:peakNaSample])
peakCapSample = extremePointsPre[-1] if len(extremePointsPre) else 0
peakCapTime = interpSampVals[peakCapSample]

extremePointsPost = flatnonzero(dsign[peakNaSample+1:])
peakKSample = extremePointsPost[0]+peakNaSample+1 if len(extremePointsPost) else len(extremePointsPost)-1
peakKTime = interpSampVals[peakKSample]



clf()
hold(1)
plot(sampVals,spikeShape,'.')
plot(interpSampVals,interpSpikeShape,'g-')
axvline(peakNaTime,ls='--',color='r')
axvline(peakCapTime,ls='--',color='0.75')
axvline(peakKTime,ls='--',color='0.75')
hold(0)
show()

