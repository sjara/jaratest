import os
import numpy as np
from collections import Counter
import operator
from jaratoolbox import settings
reload(settings)
from jaratoolbox import histologyanalysis as ha
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache
reload(ha)
import figparams

FIGNAME = 'figure_anatomy'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
annotationVolume = ha.AllenAnnotation()
corticalVolume = ha.AllenCorticalCoordinates()
subject = 'anat036'

mcc = MouseConnectivityCache(resolution=25)
rsp = mcc.get_reference_space()

#This is the allen atlas rotated to coronal so that it matches what we use
rspAnnotationVolumeRotated = np.rot90(rsp.annotation, 1, axes=(2, 0))

# -- Calculate AC cell depths --

# jpgFolder = '5xAC_JPEG'
# registrationFolder = 'registrationAC'
# slices = ['p1d5', 'p1d6', 'p2a1', 'p2a2']
# #What I used for cortex. A first pass that might have been 50um off in places
# ccfSlice = {'p1d5':205, 'p1d6':213, 'p2a1':217, 'p2a2':219}

# allSliceDepths = []
# for sliceNum in slices:
#     filenameSVGPost = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.svg'.format(subject, registrationFolder, sliceNum)
#     (scale, translate, affine) = ha.get_svg_transform(filenameSVGPost, sliceSize=[1388, 1040])
#     filenameCSV = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.csv'.format(subject, registrationFolder, sliceNum)
#     coords = ha.get_coords_from_fiji_csv(filenameCSV, pixelSize=4.0048)
#     newCoords = ha.apply_svg_transform(scale, translate, affine, coords)
#     structIDs = annotationVolume.get_structure_id_many_xy(newCoords, ccfSlice[sliceNum])
#     structNames = np.array([annotationVolume.get_structure_from_id(structID) for structID in structIDs])
#     primaryBool = np.array(['Primary auditory area' in name for name in structNames], dtype=bool)
#     primaryCoords = newCoords[:,primaryBool]
#     allDepths = corticalVolume.get_cortical_depth_many_xy(primaryCoords, ccfSlice[sliceNum])
#     allSliceDepths.append(allDepths)

# allSliceDepths = np.concatenate(allSliceDepths)
# acSavePath = os.path.join(dataDir, 'cortexCellDepths.npy')
# print "Saving to: {}".format(acSavePath)
# np.save(acSavePath, allSliceDepths)

# -- Calculate thalamus area totals --

jpgFolder = '5xATh_JPEG'
registrationFolder = 'registrationATh'

# anat036slices = ['p1b6', 'p1c1', 'p1c2', 'p1c3', 'p1c4', 'p1c5', 'p1c6',
#             'p1d1', 'p1d2', 'p1d3', 'p1d4', 'p1d5', 'p1d6', 'p2a1',
#             'p2a2', 'p2a3', 'p2a4', 'p2a5', 'p2a6']

anat036ccfSlice = {'p1b6':163,
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


anat037ccfSlice = {'p1c6':176,
            'p1d1':184,
            'p1d2':186,
            'p1d3':189,
            'p1d4':193,
            'p1d5':196,
            'p1d6':198,
            'p2a1':200,
            'p2a2':204,
            'p2a3':205,
            'p2a4':206,
            'p2a5':208,
            'p2a6':210,
            'p2b1':213,
            'p2b2':219,
            'p2b3':225,
            'p2b4':230,
            'p2b6':233,
            'p2c1':237,
            'p2c2':241,
            'p2c3':242}

# nSliceGroups=3
# sliceGroups = []
# for sgInd in range(nSliceGroups):
#     sliceGroups.append(slices[sgInd::nSliceGroups])

# for slices in sliceGroups:

def calculate_area_totals(subject, registrationFolder, ccfSlice, nSliceGroups=1):

    slices = sorted(ccfSlice.keys())
    sliceGroups = []
    for sgInd in range(nSliceGroups):
        sliceGroups.append(slices[sgInd::nSliceGroups])

    groupSliceCount = []

    for sgInd, slices in enumerate(sliceGroups):
        allAreaNames = []
        allSliceCounts = []
        allSliceTotalVoxels = []
        for sliceName in slices:
            ccfZ = ccfSlice[sliceName]
            filenameSVGPost = os.path.join(settings.HISTOLOGY_PATH, subject, registrationFolder, '{}.svg'.format(sliceName))
            (scale, translate, affine) = ha.get_svg_transform(filenameSVGPost, sliceSize=[1388, 1040])
            filenameCSV = os.path.join(settings.HISTOLOGY_PATH, subject, registrationFolder, '{}.csv'.format(sliceName))
            coords = ha.get_coords_from_fiji_csv(filenameCSV, pixelSize=4.0048)
            newCoords = ha.apply_svg_transform(scale, translate, affine, coords)

            structIDs = []
            for indCoords in range(np.shape(newCoords)[1]):
                x = newCoords[0,indCoords]
                y = newCoords[1,indCoords]
                thisCoordID = rspAnnotationVolumeRotated[int(x), int(y), ccfZ]
                structIDs.append(thisCoordID)

            # structIDs = annotationVolume.get_structure_id_many_xy(newCoords, ccfSlice[sliceNum])
            # structNames = [annotationVolume.get_structure_from_id(structID) for structID in structIDs]

            structDicts = rsp.structure_tree.get_structures_by_id(structIDs)
            structNames = [d['name'] for d in structDicts]

            structCounts = Counter(structNames)
            allSliceCounts.append(structCounts)
            totalVoxels = annotationVolume.get_total_voxels_per_area(ccfZ)
            totalVoxels = Counter(totalVoxels)
            allSliceTotalVoxels.append(totalVoxels)

        sliceCountSum = reduce(operator.add, allSliceCounts)
        sliceTotalVoxelsSum = reduce(operator.add, allSliceTotalVoxels)
        groupSliceCount.append(sliceCountSum)
        allAreaNames.extend(sliceCountSum.keys())
    #Compress into one dict with lists for each key
    uniqueAreaNames = set(allAreaNames)
    allAreasResults = {}
    for areaName in uniqueAreaNames:
        areaCounts = []
        for sliceCountSum in groupSliceCount:
            areaCounts.append(sliceCountSum.get(areaName, 0))
        allAreasResults.update({areaName:areaCounts})
    return allAreasResults

nSliceGroups = 3
anat036sliceCountSum = calculate_area_totals('anat036', registrationFolder, anat036ccfSlice, nSliceGroups=nSliceGroups)
anat037sliceCountSum = calculate_area_totals('anat037', registrationFolder, anat037ccfSlice, nSliceGroups=nSliceGroups)

nonLemNuclei = ['Suprageniculate nucleus', 'Medial geniculate complex, dorsal part', 'Medial geniculate complex, medial part']

anat036NonLem = np.array([anat036sliceCountSum.get(area, np.zeros(nSliceGroups)) for area in nonLemNuclei])
anat037NonLem = np.array([anat037sliceCountSum.get(area, np.zeros(nSliceGroups)) for area in nonLemNuclei])

anat036ventral = np.array(anat036sliceCountSum.get('Medial geniculate complex, ventral part', np.zeros(nSliceGroups)))
anat037ventral = np.array(anat037sliceCountSum.get('Medial geniculate complex, ventral part', np.zeros(nSliceGroups)))

savePath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
np.save(os.path.join(savePath, 'anat036NonLem.npy'), anat036NonLem)
np.save(os.path.join(savePath, 'anat036ventral.npy'), anat036ventral)
np.save(os.path.join(savePath, 'anat037NonLem.npy'), anat037NonLem)
np.save(os.path.join(savePath, 'anat037ventral.npy'), anat037ventral)


# thalSavePath = os.path.join(dataDir, 'thalamusAreaCounts.npz')
# print "Saving to: {}".format(thalSavePath)
# np.savez(thalSavePath, sliceCountSum=sliceCountSum, sliceTotalVoxelsSum=sliceTotalVoxelsSum)
