import os
import numpy as np
from scipy import io
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

saveDir = '/home/nick/data/1pdata/tmpData'
inputFn = 'imag003_noiseburst_skipby4_dff.npy'
# inputFn = 'imag003_noiseburst_skipby4_avg.npy'

imgArr = np.load(os.path.join(saveDir, inputFn))

imgMin = np.min(imgArr.ravel())
imgMax = np.max(imgArr.ravel())

nFrames = imgArr.shape[0]

plt.clf()
axPlot = plt.subplot(111)
plt.subplots_adjust(left=0.25, bottom=0.25)
im = axPlot.imshow(imgArr[0, :, :])
im.set_clim(imgMin, imgMax)

axSlider = plt.axes([0.25, 0.1, 0.65, 0.03])
sliderIndF = Slider(axSlider, 'Frame', 0, nFrames-1, valinit=0)

def update(val):
    indFrame = int(np.floor(sliderIndF.val))
    axPlot.cla()
    im = axPlot.imshow(imgArr[indFrame,:,:])
    im.set_clim(imgMin, imgMax)
    plt.draw()

sliderIndF.on_changed(update)
plt.show()
