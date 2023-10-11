"""
Generate FM sounds for Evan Vickers and Chris Fiels.

For the oddball session with FM sounds:
- Frequency sweep: 8 kHz to 13 kHz for up-sweep stim (and the opposite for down-sweep)
- Duration: 100 ms
- Intensity: 70 db-SPL
- Interstimulus interval: 0.1 seconds
- Oddball period: every 10+/-1 stim
- Number of trials: 500 total (about 50 oddballs)

"""

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt


#sampFreq = 44100
sampFreq = 200000
duration = 0.1

amplitude = 0.1

soundFreqsList = [ [8000,13000], [13000,8000] ]
soundNames = ['FMup','FMdown']

def fmwave(f0, f1, duration, amplitude, sampFreq):
    '''
    Inspired by tftb.generators.fmlin()
    https://github.com/scikit-signal/pytftb
    '''
    timeVec = np.arange(0,duration,1/float(sampFreq))
    fInstant = f0*timeVec +  ((f1-f0) / (2.0*duration)) * timeVec**2
    waveform = amplitude*np.sin(2.0 * np.pi * fInstant)
    return waveform, timeVec, fInstant

def waveform_to_ints(waveform, nbits=16):
    intType = 'int'+str(nbits) # Usually 'int16'
    waveInt = ((2**nbits)*waveform).astype(intType)
    return waveInt
    

for inds,soundName in enumerate(soundNames):
    f0 = soundFreqsList[inds][0]
    f1 = soundFreqsList[inds][1]
    waveformFM, timeVec, fi = fmwave(f0, f1, duration, amplitude, sampFreq)

    #filename = '/tmp/fmsound.wav'
    filename = f'/tmp/{soundName}_{f0}Hzto{f1}Hz_at{sampFreq/1000:0.0f}kHz.wav'
    waveInt = waveform_to_ints(waveformFM)
    wavfile.write(filename, sampFreq, waveInt)
    print(f'Saved {filename}')

plt.clf()
plt.subplot(2,1,1)
plt.specgram(waveformFM, NFFT=512, Fs=sampFreq)
plt.ylim(0,20000)
plt.subplot(2,1,2)
plt.plot(timeVec,waveformFM,'.-')
plt.xlim(-0.001,0.1)
plt.show()


