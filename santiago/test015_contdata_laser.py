'''
Plot continuous data during laser stimulation

http://wiki.scipy.org/Cookbook/ButterworthBandpass
'''

from jaratoolbox import settings
import numpy as np
from pylab import *
import os
from jaratoolbox import loadopenephys
from scipy.signal import butter, lfilter


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


subject = 'pinp001'
#ephysSession = '2015-03-22_17-13-54' # tuning
ephysSession = '2015-03-22_17-27-28' # laser

ephysRoot = os.path.join(settings.EPHYS_PATH, subject)

filename = os.path.join(ephysRoot,ephysSession,'109_CH11.continuous')

dc=loadopenephys.DataCont(filename)

fc = butter_bandpass_filter(dc.samples,300,6000,30000)

x=140000; 
plot(fc[x:x+200000])

show()
