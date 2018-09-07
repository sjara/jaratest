import numpy as np
import Image
import os
from jaratoolbox import settings
from jaratoolbox import histologyanalysis as ha
reload(ha)
import nrrd
import matplotlib.pyplot as plt

subject = 'anat036'
registrationFolder = 'registrationAC'
sliceName = 'p1d2'
sliceNum = 195

'''Create an SVG file for manual registration.'''
from jaratoolbox import histologyanalysis as ha
filenameAtlas = '/mnt/jarahubdata/atlas/AllenCCF_25/JPEG/allenCCF_Z{}.jpg'.format(sliceNum)
filenameSlice = '/mnt/jarahubdata/jarashare/histology/{}/5xAC_JPEG/{}tl.jpg'.format(subject, sliceName)

## -- For saving the pre svg -- ##
# filenameSVG = '/mnt/jarahubdata/jarashare/histology/{}/registrationAC/{}_pre.svg'.format(subject, sliceName)
# (atlasSize, sliceSize) = ha.save_svg_for_registration(filenameSVG, filenameAtlas, filenameSlice)

filenameSVG = '/mnt/jarahubdata/jarashare/histology/{}/registrationAC/{}.svg'.format(subject, sliceName)
(scale, translate, affine) = ha.get_svg_transform(filenameSVG, sliceSize=[1388, 1040])
filenameCSV = '/mnt/jarahubdata/jarashare/histology/{}/registrationAC/{}.csv'.format(subject, sliceName)
coords = ha.get_coords_from_fiji_csv(filenameCSV, pixelSize=4.0048)

newCoords = ha.apply_svg_transform(scale, translate, affine, coords)

annotationVolume = ha.AllenAnnotation()
structIDs = annotationVolume.get_structure_id_many_xy(newCoords, sliceNum)
structNames = np.array([annotationVolume.get_structure_from_id(structID) for structID in structIDs])
primaryBool = np.array(['Primary auditory area' in name for name in structNames], dtype=bool)
primaryCoords = newCoords[:,primaryBool]


ccfZ = sliceNum

atlasPath = os.path.join(settings.ALLEN_ATLAS_DIR, 'coronal_average_template_25.nrrd')
atlasData = nrrd.read(atlasPath)
atlas = atlasData[0]

sliceData = np.rot90(atlas[:,:,sliceNum], -1)

plt.clf()
ax = plt.subplot(111)
ax.imshow(sliceData, 'gray')
# plt.plot(primaryCoords[0], primaryCoords[1], 'r.')
ax.plot(newCoords[0], newCoords[1], 'r.')
ax.hold(1)

lapPath = os.path.join(settings.ALLEN_ATLAS_DIR, 'coronal_laplacian_25.nrrd')
lapData = nrrd.read(lapPath)
lap = lapData[0]

cortexDepthData = np.rot90(lap[:,:,sliceNum], -1)

bottomData = np.where(cortexDepthData>0.95)
plt.plot(bottomData[1], bottomData[0], 'y.')
topData = np.where((cortexDepthData<0.02) & (cortexDepthData>0))
plt.plot(topData[1], topData[0], 'g.')
plt.show()

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

figName = 'figure_anatomy'
dataFn = os.path.join(settings.FIGURES_DATA_PATH, '2018thstr', figName, 'anat036_p1d2_cellDepths.npy')
np.save(dataFn, cellDepths)

plt.figure()
plt.hist(cellDepths, bins=30, histtype='step')
plt.xlim([0, 1])
plt.show()
