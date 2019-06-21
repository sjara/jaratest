import numpy as np
from jaratest.nick.twophoton import loadflycap
from jaratest.nick.twophoton import imageanalysis
import matplotlib.gridspec as gridspec
from matplotlib import pyplot as plt
from matplotlib import patches

dataDir = '/home/nick/data/1pdata/imag003/20181221_3freqs_4to16kHz_70dB_2sec02isi'

#Loading a stack of images saved as a folder of PGMs by FlyCap
flc = loadflycap.LoadFlyCap(dataDir, skipBy=4, binX=10, binY=10)


imgf0 = np.mean(flc.imgArr[:10, :, :], axis=0)
imgf0_repeat = np.repeat(imgf0[np.newaxis,:,:], flc.imgArr.shape[0], axis=0)

dff = (flc.imgArr - imgf0_repeat) / imgf0_repeat

spca = imageanalysis.StackPCA(dff, nComponents=None)

# These values tweaked to make ranges line up with PCA trace peaks
startCenter = 32
windowSize = 10 #Total window size. Will be 1/2 before and 1/2 after center
spacing = 25

# centers = np.arange(startCenter, len(dff), spacing)
centers = np.array([25, 55, 83, 115, 138, 164, 205, 224, 248, 278, 300, 326, 353, 382, 408, 439, 465, 488, 515, 544, 570, 596, 623, 644, 677, 700, 726, ])

### Plot the ranges on the PCA traces to see how they line up with the peaks
plt.clf()
spca.plot_traces()
stimColors = ['b', 'g', 'r']
for indStim in range(3):
    #Take every 3rd stimulus in 3 diff groups
    stimCenters = centers[indStim::3]
    for center in stimCenters:
        rect = patches.Rectangle(xy=(center-np.floor(windowSize/2.), -300), width=windowSize, height=800, color=stimColors[indStim], alpha=0.25)
        plt.gca().add_patch(rect)

### Calculate average image for each group of windows
# volToUse = dff
volToUse = flc.imgArr
# Now extract frames in these ranges from the chosen volume
averageEachStim = np.empty((3, np.shape(volToUse)[1], np.shape(volToUse)[2]))
for indStim in range(3):
    #Take every 3rd stimulus in 3 diff groups
    stimCenters = centers[indStim::3]
    print stimCenters
    for indCenter, center in enumerate(stimCenters):
        windowStart = int(center-np.floor(windowSize/2.))
        windowStop = int(windowStart + windowSize)
        framesThisRange = volToUse[windowStart:windowStop:,:]
        if indCenter==0:
            allFramesThisStim = framesThisRange
        else:
            allFramesThisStim = np.concatenate([allFramesThisStim, framesThisRange])
    print np.shape(allFramesThisStim)
    averageEachStim[indStim,:,:] = np.mean(allFramesThisStim, axis=0)

# For plotting individual frames, etc.

maxVal = np.max(averageEachStim.ravel())
minVal = np.min(averageEachStim.ravel())

indFrame=0
plt.clf()
ax = plt.gca()
cax = plt.imshow(averageEachStim[indFrame, :,:], cmap='viridis')
cax.set_clim(minVal, maxVal)
cbar = plt.colorbar(cax, ax=ax)
ax.axis('off')
ax.set_title('Stim {}'.format(indFrame))
plt.savefig('/home/nick/data/1pdata/tmpData/windows_average_image_stim{}.png'.format(indFrame))

# diffImage = averageEachStim[0,:,:] - averageEachStim[2,:,:]
# plt.imshow(averageEachStim[indFrame,:,:] - np.mean(averageEachStim, axis=0))

#Want to find the frame where each pixel is at its max, but I think I need to subtract the mean image first.
# NOTE: This doesn't seem to do much
# plt.clf()
# averageEachMeanSubtracted = averageEachStim - np.mean(averageEachStim, axis=0)
# plt.imshow(np.argmax(averageEachMeanSubtracted, axis=0))

### Plot differences between the 3 average images
# plt.clf()
# fig = plt.gcf()
# gs = gridspec.GridSpec(3, 3)
# gs.update(wspace=0.1, hspace=0.1)
# for indFirst in range(3):
#     for indSecond in range(3):

#         specDiff = gs[indFirst, indSecond]
#         axDiff = plt.Subplot(fig, specDiff)
#         fig.add_subplot(axDiff)
#         diffImage = averageEachStim[indFirst,:,:] - averageEachStim[indSecond,:,:]
#         axDiff.imshow(diffImage)
#         axDiff.set_title('{} - {}'.format(indFirst, indSecond))
#         axDiff.axis('off')
# plt.show()

