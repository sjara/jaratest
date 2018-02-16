import os
import numpy as np
from collections import Counter
import operator
from jaratoolbox import settings
from jaratoolbox import histologyanalysis as ha
reload(ha)
import figparams

FIGNAME = 'figure_anatomy'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
annotationVolume = ha.AllenAnnotation()
corticalVolume = ha.AllenCorticalCoordinates()
subject = 'anat036'

# -- Calculate AC cell depths --

jpgFolder = '5xAC_JPEG'
registrationFolder = 'registrationAC'
slices = ['p1d5', 'p1d6', 'p2a1', 'p2a2']
#What I used for cortex. A first pass that might have been 50um off in places
ccfSlice = {'p1d5':205, 'p1d6':213, 'p2a1':217, 'p2a2':219}

allSliceDepths = []
for sliceNum in slices:
    filenameSVGPost = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.svg'.format(subject, registrationFolder, sliceNum)
    (scale, translate, affine) = ha.get_svg_transform(filenameSVGPost, sliceSize=[1388, 1040])
    filenameCSV = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.csv'.format(subject, registrationFolder, sliceNum)
    coords = ha.get_coords_from_fiji_csv(filenameCSV, pixelSize=4.0048)
    newCoords = ha.apply_svg_transform(scale, translate, affine, coords)
    structIDs = annotationVolume.get_structure_id_many_xy(newCoords, ccfSlice[sliceNum])
    structNames = np.array([annotationVolume.get_structure_from_id(structID) for structID in structIDs])
    primaryBool = np.array(['Primary auditory area' in name for name in structNames], dtype=bool)
    primaryCoords = newCoords[:,primaryBool]
    allDepths = corticalVolume.get_cortical_depth_many_xy(primaryCoords, ccfSlice[sliceNum])
    allSliceDepths.append(allDepths)

allSliceDepths = np.concatenate(allSliceDepths)
acSavePath = os.path.join(dataDir, 'cortexCellDepths.npy')
print "Saving to: {}".format(acSavePath)
np.save(acSavePath, allSliceDepths)



# -- Calculate thalamus area totals --

jpgFolder = '5xATh_JPEG'
registrationFolder = 'registrationATh'
slices = ['p1b6', 'p1c1', 'p1c2', 'p1c3', 'p1c4', 'p1c5', 'p1c6',
            'p1d1', 'p1d2', 'p1d3', 'p1d4', 'p1d5', 'p1d6', 'p2a1',
            'p2a2', 'p2a3', 'p2a4', 'p2a5', 'p2a6']
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

allSliceCounts = []
allSliceTotalVoxels = []
for sliceNum in slices:
    filenameSVGPost = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.svg'.format(subject, registrationFolder, sliceNum)
    (scale, translate, affine) = ha.get_svg_transform(filenameSVGPost, sliceSize=[1388, 1040])
    filenameCSV = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.csv'.format(subject, registrationFolder, sliceNum)
    coords = ha.get_coords_from_fiji_csv(filenameCSV, pixelSize=4.0048)
    newCoords = ha.apply_svg_transform(scale, translate, affine, coords)
    structIDs = annotationVolume.get_structure_id_many_xy(newCoords, ccfSlice[sliceNum])
    structNames = [annotationVolume.get_structure_from_id(structID) for structID in structIDs]
    structCounts = Counter(structNames)
    allSliceCounts.append(structCounts)
    totalVoxels = annotationVolume.get_total_voxels_per_area(ccfSlice[sliceNum])
    totalVoxels = Counter(totalVoxels)
    allSliceTotalVoxels.append(totalVoxels)

sliceCountSum = reduce(operator.add, allSliceCounts)
sliceTotalVoxelsSum = reduce(operator.add, allSliceTotalVoxels)

thalSavePath = os.path.join(dataDir, 'thalamusAreaCounts.npz')
print "Saving to: {}".format(thalSavePath)
np.savez(thalSavePath, sliceCountSum=sliceCountSum, sliceTotalVoxelsSum=sliceTotalVoxelsSum)
