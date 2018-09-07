import numpy as np
import Image
import os
from jaratoolbox import settings
from jaratoolbox import histologyanalysis as ha
import nrrd
import matplotlib.pyplot as plt

sliceNum = 207
# atlasPath = os.path.join(settings.ALLEN_ATLAS_DIR, 'coronal_average_template_25.nrrd')
'''
atlasPath = os.path.join(settings.ALLEN_ATLAS_DIR, 'coronal_laplacian_25.nrrd')
atlasData = nrrd.read(atlasPath)
atlas = atlasData[0]

# ax = plt.subplot(111)

sliceData = np.rot90(atlas[:,:,sliceNum], -1)
h, binEdges = np.histogram(sliceData, bins=10)
binEdgesCorrected = np.r_[0, 0.00001, binEdges[1:]] #So that low vals don't fall into the 0 bin like background
quantized = np.digitize(sliceData, binEdgesCorrected)
ax.imshow(quantized, 'gray')
'''

#Load the equivalent cells CSV file and transform

# subject = 'anat036'
# registrationFolder = 'registrationAC'
# sliceName = 'p1d5'

# ccfZ = sliceNum
# filenameSVGPost = os.path.join(settings.HISTOLOGY_PATH, subject, registrationFolder, '{}.svg'.format(sliceName))
# (scale, translate, affine) = ha.get_svg_transform(filenameSVGPost, sliceSize=[1388, 1040])
# filenameCSV = os.path.join(settings.HISTOLOGY_PATH, subject, registrationFolder, '{}.csv'.format(sliceName))
# coords = ha.get_coords_from_fiji_csv(filenameCSV, pixelSize=4.0048)
# newCoords = ha.apply_svg_transform(scale, translate, affine, coords)

# ax.hold(1)
# ax.plot(newCoords[0], newCoords[1], 'r.', ms=1)

plt.clf()




# #Need to save out to a jpg

# #Rescale to 0-255 and convert to uint8
# rescaled = (255.0 / quantized.max() * (quantized - quantized.min())).astype(np.uint8)
# im = Image.fromarray(rescaled)
# imFn = '/tmp/allen{}_laplacian.png'.format(sliceNum)
# im.save(imFn)
# print "Saved image to: {}".format(imFn)


# plt.show()
# ax = plt.subplot(111)
# ax.imshow(sliceData>0.95, 'gray')
# ax.imshow((sliceData<0.03) & (sliceData>0), 'gray')

# plt.show()


# Select neurons from primary
subject = 'anat036'
registrationFolder = 'registrationAC'
sliceName = 'p1d5'


ccfZ = sliceNum

atlasPath = os.path.join(settings.ALLEN_ATLAS_DIR, 'coronal_average_template_25.nrrd')
atlasData = nrrd.read(atlasPath)
atlas = atlasData[0]

sliceData = np.rot90(atlas[:,:,sliceNum], -1)

annotationVolume = ha.AllenAnnotation()

filenameSVGPost = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.svg'.format(subject, registrationFolder, sliceName)
(scale, translate, affine) = ha.get_svg_transform(filenameSVGPost, sliceSize=[1388, 1040])
filenameCSV = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.csv'.format(subject, registrationFolder, sliceName)
coords = ha.get_coords_from_fiji_csv(filenameCSV, pixelSize=4.0048)
newCoords = ha.apply_svg_transform(scale, translate, affine, coords)
structIDs = annotationVolume.get_structure_id_many_xy(newCoords, sliceNum)
structNames = np.array([annotationVolume.get_structure_from_id(structID) for structID in structIDs])
primaryBool = np.array(['Primary auditory area' in name for name in structNames], dtype=bool)
primaryCoords = newCoords[:,primaryBool]

plt.imshow(sliceData, 'gray')
plt.plot(primaryCoords[0], primaryCoords[1], 'r.')
plt.hold(1)

# Get the top and bottom of cortex
lapPath = os.path.join(settings.ALLEN_ATLAS_DIR, 'coronal_laplacian_25.nrrd')
lapData = nrrd.read(lapPath)
lap = lapData[0]

# ax = plt.subplot(111)
cortexDepthData = np.rot90(lap[:,:,sliceNum], -1)

# ax.imshow(cortexDepthData>0.95, 'gray')
# ax.imshow((cortexDepthData<0.03) & (cortexDepthData>0), 'gray')

bottomData = np.where(cortexDepthData>0.95)
plt.plot(bottomData[1], bottomData[0], 'y.')
# topData = np.where((cortexDepthData<0.03) & (cortexDepthData>0))
topData = np.where((cortexDepthData<0.02) & (cortexDepthData>0))
# plt.show()
plt.plot(topData[1], topData[0], 'g.')
plt.show()

# for indCell in range(shape(primaryCoords)[1]):
numCells = np.shape(primaryCoords)[1]
cellDepths = np.empty(numCells)
for indCell in range(numCells):
    print "Cell {}".format(indCell)
    cellX = primaryCoords[0, indCell]
    cellY = primaryCoords[1, indCell]

    dXTop = topData[1] - cellX
    dYTop = topData[0] - cellY
    distanceTop = np.sqrt(dXTop**2 + dYTop**2)
    indMinTop = np.argmin(distanceTop)
    minDistanceTop = distanceTop.min()

    dXBottom = bottomData[1] - cellX
    dYBottom = bottomData[0] - cellY
    distanceBottom = np.sqrt(dXBottom**2 + dYBottom**2)
    minDistanceBottom = distanceBottom.min()

    cellRatio = minDistanceTop / (minDistanceBottom + minDistanceTop)
    cellDepths[indCell] = cellRatio


# Plot cells to verify
# plt.plot(cellX, cellY, 'bo')
# plt.plot(topData[1][indMinTop], topData[0][indMinTop], 'bo')
# plt.show()

plt.clf()
plt.hist(cellDepths, bins=30, histtype='step')
plt.xlim([0, 1])


# plt.figure()
# plt.hist(cellDepths, bins=16, histtype='step')
# plt.xlim([0, 1])

plt.show()
