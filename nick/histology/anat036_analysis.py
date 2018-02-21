import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from jaratoolbox import histologyanalysis as ha
from collections import Counter
import operator

HISTOLOGY_DIR = '/mnt/jarahubdata/jarashare/histology'
subject = 'anat036'
barColor = '0.5'

AREA='ATh'
CASE=6

if AREA=='AC':
    jpgFolder = '5xAC_JPEG'
    registrationFolder = 'registrationAC'
    slices = ['p1d5', 'p1d6', 'p2a1', 'p2a2']
    #What I used for cortex. A first pass that might have been 50um off in places
    ccfSlice = {'p1d5':205, 'p1d6':213, 'p2a1':217, 'p2a2':219}
elif AREA=="ATh":
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
                'p1c6':184, #DONE
                'p1d1':185, #DONE
                'p1d2':192, #DONE
                'p1d3':196, #DONE
                'p1d4':199, #DONE
                'p1d5':200, #DONE
                'p1d6':202, #DONE
                'p2a1':204, #DONE
                'p2a2':207, #DONE.
                'p2a3':210, #DONE.
                'p2a4':213, #DONE
                'p2a5':217, #DONE
                'p2a6':220} #DONE

def counter_values(counterList):
    '''
    Takes a list of counter objects and returns a dict with each unique key mapped to a list of the values for
    that key in each counter object. The list will contain nan if the counter object did not contain a value for that key.
    '''
    allKeys = set().union(*(d.keys() for d in counterList))
    resultDict = {key:[] for key in allKeys}
    for counter in counterList:
        for key in allKeys:
            try:
                countThisKey = counter[key]
            except KeyError:
                countThisKey = np.nan
            resultDict[key].append(countThisKey)
    return resultDict


#Save svg files for registration
if CASE==0:
    for sliceNum in slices:
        filenameAtlas = '/mnt/jarahubdata/atlas/AllenCCF_25/JPEG/allenCCF_Z{}.jpg'.format(ccfSlice[sliceNum])
        filenameSlice = os.path.join(HISTOLOGY_DIR, subject, jpgFolder, '{}tl.jpg'.format(sliceNum))
        filenameSVG = os.path.join(HISTOLOGY_DIR, subject, registrationFolder, '{}_pre.svg'.format(sliceNum))
        (atlasSize, sliceSize) = ha.save_svg_for_registration(filenameSVG, filenameAtlas, filenameSlice)

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
    for sliceNum in slices:
        plt.clf()
        filenameSVGPost = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.svg'.format(subject, registrationFolder, sliceNum)
        (scale, translate, affine) = ha.get_svg_transform(filenameSVGPost, sliceSize=[1388, 1040])
        filenameCSV = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.csv'.format(subject, registrationFolder, sliceNum)
        coords = ha.get_coords_from_fiji_csv(filenameCSV, pixelSize=4.0048)
        newCoords = ha.apply_svg_transform(scale, translate, affine, coords)
        filenameAtlas = '/mnt/jarahubdata/atlas/AllenCCF_25/JPEG/allenCCF_Z{}.jpg'.format(ccfSlice[sliceNum])
        atlasIm = mpimg.imread(filenameAtlas)
        plt.clf()
        plt.imshow(atlasIm,cmap='gray')
        plt.plot(newCoords[0,:],newCoords[1,:],'o',mec='r',mfc=[0,1,0], ms=3)
        plt.axis('image')
        plt.show()
        plt.waitforbuttonpress()

#Read coords, apply transform, output the cortical depth for each cell
elif CASE==3:

    corticalVolume = ha.AllenCorticalCoordinates()
    annotationVolume = ha.AllenAnnotation()
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

    plt.clf()
    ax = plt.subplot(111)
    ax.hist(allSliceDepths, bins=50, color=barColor)
    ax.set_xlim([0, 1])
    plt.ylabel('Number of cells')
    plt.xlabel('Normalized distance from pia')
    plt.show()


elif CASE==4:
    #Thalamus counts
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

elif CASE==5:
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

    sliceCountSum = reduce(operator.add, allSliceCounts)

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
    allCells = sum([val for key, val in sliceCountSum.iteritems()])

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

elif CASE==6:
    annotationVolume = ha.AllenAnnotation()
    allSliceCounts = []

    areasToPlot = {
        'Medial geniculate complex, dorsal part':'r',
        'Medial geniculate complex, medial part':'g',
        'Medial geniculate complex, ventral part':'b',
        'Lateral posterior nucleus of the thalamus':'m',
        'Suprageniculate nucleus':'c',
        'Posterior limiting nucleus of the thalamus': 'y'}

    for sliceNum in slices:
        filenameSVGPost = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.svg'.format(subject, registrationFolder, sliceNum)
        (scale, translate, affine) = ha.get_svg_transform(filenameSVGPost, sliceSize=[1388, 1040])
        filenameCSV = '/mnt/jarahubdata/jarashare/histology/{}/{}/{}.csv'.format(subject, registrationFolder, sliceNum)
        filenameAtlas = '/mnt/jarahubdata/atlas/AllenCCF_25/JPEG/allenCCF_Z{}.jpg'.format(ccfSlice[sliceNum])
        coords = ha.get_coords_from_fiji_csv(filenameCSV, pixelSize=4.0048)
        newCoords = ha.apply_svg_transform(scale, translate, affine, coords)
        structIDs = annotationVolume.get_structure_id_many_xy(newCoords, ccfSlice[sliceNum])
        structNames = [annotationVolume.get_structure_from_id(structID) for structID in structIDs]
        structCounts = Counter(structNames)

        atlasIm = mpimg.imread(filenameAtlas)

        plt.clf()
        plt.imshow(atlasIm,cmap='gray')
        for area, color in areasToPlot.iteritems():
            indsThisArea = np.array(structNames) == area
            coordsThisArea = newCoords[:,indsThisArea]
            plt.plot(coordsThisArea[0,:],coordsThisArea[1,:],'o',color=color, ms=3)
            plt.hold(True)
        plt.axis('image')
        plt.xlim([290, 350])
        plt.ylim([170, 120])
        plt.show()
        plt.waitforbuttonpress()
