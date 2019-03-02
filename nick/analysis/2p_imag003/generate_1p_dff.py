import os
import numpy as np

saveDir = '/home/nick/data/1pdata/tmpData'
inputFn = 'imag003_noiseburst_skipby4.npy'
outputFn = 'imag003_noiseburst_skipby4_dff.npy'
avgArrayFn = 'imag003_noiseburst_skipby4_avg.npy'

imgArr = np.load(os.path.join(saveDir, inputFn))

imgArr_avg = np.mean(imgArr[:10,:,:], axis=0)

# We need to repeat the average frame the same number of times as the
# number of frames in the data, so that we can subtract the average
# frame from each data frame.
imgArr_avg_repeat = np.repeat(imgArr_avg[np.newaxis,:,:], imgArr.shape[0], axis=0)
imgArr_dff = (imgArr - imgArr_avg_repeat) / imgArr_avg_repeat

np.save(os.path.join(saveDir, outputFn), imgArr_dff)
