import numpy as np
from jaratest.nick.twophoton import loadflycap
from jaratest.nick.twophoton import imageanalysis

dataDir = '/home/nick/data/1pdata/imag003/20181221_3freqs_4to16kHz_70dB_2sec02isi'

#Loading a stack of images saved as a folder of PGMs by FlyCap
flc = loadflycap.LoadFlyCap(dataDir, skipBy=4, binX=10, binY=10)

spca = imageanalysis.StackPCA(flc.imgArr, nComponents=None)
