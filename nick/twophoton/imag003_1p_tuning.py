import os
import numpy as np
from jaratest.nick.twophoton import loadflycap
from jaratest.nick.twophoton import imageanalysis
from matplotlib import pyplot as plt
from matplotlib import widgets

# dataDir = '/home/nick/data/1pdata/imag003/20181221_3freqs_4to16kHz_70dB_2sec02isi/'
dataDir = '/home/nick/data/1pdata/imag003/20181221_2freqs_8to16kHz_70dB_2sec02isi_1frameOutOf4'
flc = loadflycap.LoadFlyCap(dataDir, skipBy=1, binX=10, binY=10)

imgf0 = np.mean(flc.imgArr[:10, :, :], axis=0)
imgf0_repeat = np.repeat(imgf0[np.newaxis,:,:], flc.imgArr.shape[0], axis=0)

dff = (flc.imgArr - imgf0_repeat) / imgf0_repeat
spca = imageanalysis.StackPCA(dff, nComponents=None)
