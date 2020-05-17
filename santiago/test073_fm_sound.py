'''
Generate FM sound
'''

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

sampFreq = 44100.0
duration = 0.5

amplitude = 0.1

f0 = 500
f1 = 4000


def fmwave(f0,f1,duration,amplitude,sampFreq):
    '''
    Inspired by tftb.generators.fmlin()
    https://github.com/scikit-signal/pytftb
    '''
    timeVec = np.arange(0,duration,1/float(sampFreq))
    fInstant = f0*timeVec +  ((f1-f0) / (2.0*duration)) * timeVec**2
    waveform = amplitude*np.sin(2.0 * np.pi * fInstant)
    return waveform, timeVec, fInstant

def STEPSfmwave(f0,f1,duration,amplitude,sampFreq):
    timeVec = np.arange(0,duration,1/float(sampFreq))
    nSamples = len(timeVec)
    fnormi = f0/float(sampFreq)
    fnormf = f1/float(sampFreq)

    t0 = round(nSamples / 2.0)
    y = np.arange(nSamples)
    #y = fnormi*y + ((fnormf - fnormi) / (2.0 * (nSamples - 1))) * \
    #    (y**2 - (t0 - 1) ** 2)
    #y = fnormi*y + ((fnormf - fnormi) / (2.0 * (nSamples - 1))) * y**2
    #y = f0*timeVec +  ((fnormf - fnormi) / (2.0 * (nSamples))) * y**2
    #y = f0*timeVec +  ((f1-f0) / (2.0*sampFreq*nSamples)) * y**2
    y = f0*timeVec +  ((f1-f0) / (2.0*duration)) * timeVec**2
    #y = np.exp(1j * 2.0 * np.pi * y)
    y = np.sin(2.0 * np.pi * y)
    y = y / y[int(t0) - 1]
    #iflaw = np.linspace(fnormi, fnormf, nSamples)

    waveform = amplitude*y
    #return np.real(waveform), timeVec
    return waveform, timeVec

def ORIGfmwave(f0,f1,duration,amplitude,sampFreq):
    timeVec = np.arange(0,duration,1/float(sampFreq))
    nSamples = len(timeVec)
    fnormi = f0/float(sampFreq)
    fnormf = f1/float(sampFreq)

    t0 = round(nSamples / 2.0)
    y = np.arange(1, nSamples + 1)
    y = fnormi * (y - t0) + ((fnormf - fnormi) / (2.0 * (nSamples - 1))) * \
        ((y - 1) ** 2 - (t0 - 1) ** 2)
    y = np.exp(1j * 2.0 * np.pi * y)
    y = y / y[int(t0) - 1]
    #iflaw = np.linspace(fnormi, fnormf, nSamples)

    waveform = amplitude*y
    return np.real(waveform), timeVec

def OLDfmwave(f0,f1,duration,amplitude,sampFreq):
    timeVec = np.arange(0,duration,1/float(sampFreq))
    nSamples = len(timeVec)
    #freqVec = np.logspace(np.log10(f0),np.log10(f1),nSamples)
    freqVec = np.linspace(f0,f1,nSamples) #  linear
    return waveform, timeVec


def waveform_to_ints(waveform, nbits=16):
    intType = 'int'+str(nbits) # Usually 'int16'
    waveInt = ((2**nbits)*waveform).astype(intType)
    return waveInt
    
#waveformFM, timeVec = fmwave(f0,f1,duration,amplitude,sampFreq)
waveformFM, timeVec,fi = fmwave(f1,f0,duration,amplitude,sampFreq)

plt.clf()
plt.subplot(2,1,1)
plt.specgram(waveformFM, NFFT=512, Fs=sampFreq)
plt.ylim(0,5000)
plt.subplot(2,1,2)
plt.plot(timeVec,waveformFM,'.-')
plt.xlim(-0.001,0.01)
plt.show()


filename = '/tmp/fmsound.wav'
waveInt = waveform_to_ints(waveformFM)
wavfile.write(filename, sampFreq, waveInt)



'''
CASE = 1
if CASE==0:
    #fvec = np.linspace(f0,f1,nSamples) #  Up (linear)
    fvec = np.logspace(log10(f0),log10(f1),nSamples) # Up (log)
elif CASE==1:
    #fvec = np.linspace(f1,f0,nSamples)  # Down (linear)
    fvec = np.logspace(log10(f1),log10(f0),nSamples) # Down (log)
elif CASE==2:
    fvec = np.concatenate((np.logspace(log10(fMid),log10(f1),nSamples/2),
                           np.logspace(log10(f0),log10(fMid),nSamples/2)))  # Up
elif CASE==3:
    fvec = np.concatenate((np.logspace(log10(fMid),log10(f0),nSamples/2),
                           np.logspace(log10(f1),log10(fMid),nSamples/2)))  # Down

'''

import sys
sys.exit()

# From https://github.com/scikit-signal/pytftb/blob/master/tftb/generators/frequency_modulated.py
### fmlin(n_points, fnormi=0.0, fnormf=0.5, t0=None):

'''
t0 = round(n_points / 2.0)
y = np.arange(1, n_points + 1)
y = fnormi * (y - t0) + ((fnormf - fnormi) / (2.0 * (n_points - 1))) *  ((y - 1) ** 2 - (t0 - 1) ** 2)
y = np.exp(1j * 2.0 * np.pi * y)
y = y / y[int(t0) - 1]
iflaw = np.linspace(fnormi, fnormf, n_points)
return y, iflaw

nPoints = len(timeVec)
y = f0 * (timeVec - nPoints//2) + \
    ((f1 - f0) / (2.0 * (n_points - 1))) * (timeVec - 1)**2 - \
    (t0 - 1) ** 2)
y = 
'''
