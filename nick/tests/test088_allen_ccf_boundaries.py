import os
import matplotlib.image as mpimg
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import histologyanalysis as ha
reload(ha)

an = ha.AllenAnnotation()

imageDir5xMerge = '/home/nick/Desktop/mergedImages_anat036_5x_thal'

subject = 'anat036'
slices = ['p1d1', 'p1d2', 'p1d3']
ccfSlice = {'p1b6':163,
            'p1c1':167,
            'p1c2':171,
            'p1c3':175,
            'p1c4':179,
            'p1c5':183,
            'p1c6':187,
            'p1d1':191,
            'p1d2':195,
            'p1d3':199,
            'p1d4':203,
            'p1d5':207,
            'p1d6':211,
            'p2a1':215,
            'p2a2':219,
            'p2a3':223,
            'p2a4':226,
            'p2a5':229,
            'p2a6':230}
sliceName = 'p1c6'

filenameAtlas = '/mnt/jarahubdata/atlas/AllenCCF_25/JPEG/allenCCF_Z{}.jpg'.format(ccfSlice[sliceName])
atlasIm = mpimg.imread(filenameAtlas)

areasToPlot = {
    'Medial geniculate complex, dorsal part':'g',
    'Medial geniculate complex, medial part':'w',
    'Medial geniculate complex, ventral part':'b',
    'Lateral posterior nucleus of the thalamus':'m',
    'Suprageniculate nucleus':'y',
    'Posterior limiting nucleus of the thalamus':'c'
}

def get_boundary_coords(areaName):
    areaID = int(an.structureDF.query('name==@areaName')['id'])
    structureIm = an.annotationVol[:,:,ccfSlice[sliceName]]==areaID
    # structureMask = np.ma.array(structureIm, mask=structureIm==0)
    structureGrad = np.gradient(structureIm)[1]
    structureGradCoords = np.where(structureGrad>0)
    return structureGradCoords

filenameSVG = '/mnt/jarahubdata/jarashare/histology/{}/registrationATh/{}.svg'.format(subject, sliceName)
(scale, translate, affine) = ha.get_svg_transform(filenameSVG, sliceSize=[1388, 1040])

# filenameMerge = os.path.join(imageDir5xMerge, '{}.jpg'.format(sliceName))
filenameMerge = '/home/nick/data/jarahubdata/jarashare/histology/anat036/5_thal/jpg/Composite_5xThal_z007_c001.jpg'
mergeIm = mpimg.imread(filenameMerge)


plt.clf()
plt.imshow(mergeIm)
plt.hold(True)
for areaName, color in areasToPlot.iteritems():
    structureGradCoords = get_boundary_coords(areaName)
    newStructCoords = ha.apply_svg_inverse_transform(scale, translate, affine, structureGradCoords)
    plt.plot(newStructCoords[0], newStructCoords[1], 'o', color=color)
    plt.hold(True)
# plt.imshow(np.rot90(structureMask, -1), interpolation='none')
plt.show()
