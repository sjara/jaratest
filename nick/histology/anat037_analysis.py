import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from jaratoolbox import histologyanalysis as ha
from collections import Counter
import operator

HISTOLOGY_DIR = '/mnt/jarahubdata/jarashare/histology'
subject = 'anat037'
barColor = '0.5'

AREA='ATh'

jpgFolder = '5xATh_JPEG'
registrationFolder = 'registrationATh'
# ccfSlice = {'p1c3':165,
#             'p1c4':168,


slices = ['p1c6', 'p1d1', 'p1d2', 'p1d3', 'p1d4', 'p1d5', 'p1d6', 'p2a1', 'p2a2', 'p2a3', 'p2a4',
          'p2a5', 'p2a6', 'p2b1', 'p2b2', 'p2b3', 'p2b4', 'p2b6', 'p2c1', 'p2c2', 'p2c3']

ccfSlice = {'p1c6':176,
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

# for sliceName, ccfZ in ccfSlice.iteritems():
#     filenameAtlas = '/mnt/jarahubdata/atlas/AllenCCF_25/JPEG/allenCCF_Z{}.jpg'.format(ccfZ)
#     filenameSlice = os.path.join(HISTOLOGY_DIR, subject, jpgFolder, '{}tl.jpg'.format(sliceName))
#     filenameSVG = os.path.join(HISTOLOGY_DIR, subject, registrationFolder, '{}_pre.svg'.format(sliceName))
#     (atlasSize, sliceSize) = ha.save_svg_for_registration(filenameSVG, filenameAtlas, filenameSlice)

CASE=2

if CASE==0:
    annotationVolume = ha.AllenAnnotation()
    allSliceCounts = []
    for sliceName, ccfZ in ccfSlice.iteritems():
        filenameSVGPost = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.svg'.format(subject, registrationFolder, sliceName)
        (scale, translate, affine) = ha.get_svg_transform(filenameSVGPost, sliceSize=[1388, 1040])
        filenameCSV = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.csv'.format(subject, registrationFolder, sliceName)
        coords = ha.get_coords_from_fiji_csv(filenameCSV, pixelSize=4.0048)
        newCoords = ha.apply_svg_transform(scale, translate, affine, coords)

        structIDs = annotationVolume.get_structure_id_many_xy(newCoords, ccfZ)
        structNames = [annotationVolume.get_structure_from_id(structID) for structID in structIDs]
        structCounts = Counter(structNames)
        allSliceCounts.append(structCounts)

    sliceCountSum = reduce(operator.add, allSliceCounts)
    allCells = sum([val for key, val in sliceCountSum.iteritems()])

    areasToPlot = [
        'Medial geniculate complex, dorsal part',
        'Medial geniculate complex, medial part',
        'Medial geniculate complex, ventral part',
        'Lateral posterior nucleus of the thalamus',
        'Suprageniculate nucleus',
        'Posterior limiting nucleus of the thalamus'
    ]

    abbrevs = ['MGd', 'MGm', 'MGv', 'LP', 'SG', 'Pol']

    areaSums = [sliceCountSum[key] for key in areasToPlot]

    ind = np.arange(len(areaSums))
    width = 0.35
    plt.clf()
    ax = plt.subplot(111)
    ax.bar(ind, areaSums, width, color=barColor)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(abbrevs, rotation=70, horizontalalignment='right')
    plt.subplots_adjust(bottom=0.2, left=0.2)
    plt.ylabel('Number of cells')
    plt.show()

#Read coords, apply transform, output counts per area
elif CASE==1:
    annotationVolume = ha.AllenAnnotation()
    allSliceCounts = []
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

    resultCounts = counter_values(allSliceCounts)
    resultMean = {key:np.nanmean(val) for key, val in resultCounts.iteritems()}
    resultStd = {key:np.nanstd(val) for key, val in resultCounts.iteritems()}

    # areasToPlot = [
    #     'Primary auditory area, layer 2/3',
    #     'Primary auditory area, layer 4',
    #     'Primary auditory area, layer 5',
    #     'Primary auditory area, layer 6a',
    #     'Primary auditory area, layer 6b',
    #     'Dorsal auditory area, layer 2/3',
    #     'Dorsal auditory area, layer 4',
    #     'Dorsal auditory area, layer 5',
    #     'Dorsal auditory area, layer 6a',
    #     'Dorsal auditory area, layer 6b',
    #     'Ventral auditory area, layer 2/3',
    #     'Ventral auditory area, layer 4',
    #     'Ventral auditory area, layer 5',
    #     'Ventral auditory area, layer 6a',
    #     'Ventral auditory area, layer 6b'
    # ]
    # areasToPlot = [
    #     'Primary auditory area, layer 2/3',
    #     'Primary auditory area, layer 4',
    #     'Primary auditory area, layer 5',
    #     'Primary auditory area, layer 6a',
    #     'Primary auditory area, layer 6b'
    # ]

    means = [resultMean[key] for key in areasToPlot]
    stds = [resultStd[key] for key in areasToPlot]

    ind = np.arange(len(means))
    width = 0.35
    plt.clf()
    ax = plt.subplot(111)
    ax.bar(ind, means, width, color=barColor, yerr=stds)
    ax.set_xticks(ind+width+0.1)
    ax.set_xticklabels(areasToPlot, rotation=70, horizontalalignment='right')
    plt.subplots_adjust(bottom=0.4, left=0.15)
    plt.ylabel('Average number of cells per slice')
    plt.show()

#Plot some points to verify alignment
elif CASE==2:
    for sliceNum in slices[:1]:
        plt.clf()
        filenameSVGPost = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.svg'.format(subject, registrationFolder, sliceNum)
        (scale, translate, affine) = ha.get_svg_transform(filenameSVGPost, sliceSize=[1388, 1040])
        filenameCSV = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.csv'.format(subject, registrationFolder, sliceNum)
        coords = ha.get_coords_from_fiji_csv(filenameCSV, pixelSize=4.0048)
        # newCoords = scale*coords + translate
        # newCoords = coords
        newCoords = ha.apply_svg_transform(scale, translate, affine, coords)
        filenameAtlas = '/mnt/jarahubdata/atlas/AllenCCF_25/JPEG/allenCCF_Z{}.jpg'.format(ccfSlice[sliceNum])
        atlasIm = mpimg.imread(filenameAtlas)
        plt.clf()
        plt.imshow(atlasIm,cmap='gray')
        plt.plot(newCoords[0,:],newCoords[1,:],'o',mec='r',mfc=[0,1,0], ms=3)
        plt.axis('image')
        plt.show()
        # plt.waitforbuttonpress()
