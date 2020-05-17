'''
Show spectrograms of speech.
'''

import scipy.io.wavfile
import scipy.signal
from matplotlib import pyplot as plt
import numpy as np
from jaratoolbox import extraplots


#filenames = ['/home/sjara/src/jarasounds/bada_1x_000.wav',
#             '/home/sjara/src/jarasounds/bada_1x_100.wav',
#             '/home/sjara/src/jarasounds/bapa_1x_000.wav']
filenames = ['/var/tmp/speechsounds/bada_1x_000.wav',
             '/var/tmp/speechsounds/bada_1x_100.wav',
             '/var/tmp/speechsounds/bapa_1x_050.wav']

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'Fig_spectrograms_speech' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [2.5,4] # In inches

plt.clf()
for indf,filename in enumerate(filenames):
    
    fs, mywave = scipy.io.wavfile.read(filename)

    WINDOW = ('tukey', 0.25)
    WINDOW = 'hanning'
    NFFT = 2048
    [fvec,tvec,sgram] = scipy.signal.spectrogram(mywave, fs=fs, window=WINDOW, mode='complex',
                                                 nperseg=NFFT, noverlap=int(0.8*NFFT),)

    imgExtent = [tvec[0], tvec[-1], fvec[0], fvec[-1]]
    #, extent=imgExtent

    INTERP = 'nearest'
    #INTERP = 'bilinear'
    INTERP = 'hanning'

    sgramVals = np.log10(np.abs(sgram)**2)
    #sgramVals = sgram
    #VMAX = sgramVals.max()/20; VMIN=None
    VMAX = 5.2; # None
    VMIN = -2 #sgramVals.min()

    plt.subplot(3,1,indf+1)
    plt.gca().set_axis_bgcolor('k')
    plt.imshow(sgramVals, cmap='viridis', aspect='auto', interpolation=INTERP, vmin=VMIN, vmax=VMAX, resample=True)
    #plt.imshow(sgramVals, cmap='viridis', aspect='auto', interpolation=INTERP)

    plt.ylim([70,0])
    plt.xlim([7,50])

    plt.gca().invert_yaxis()
    plt.colorbar()

    

#CMAPS:    'magma', 'viridis', 'inferno', 'plasma' 'CMRmap'
# hist(sgramVals.flatten(),100)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
   
plt.show()
