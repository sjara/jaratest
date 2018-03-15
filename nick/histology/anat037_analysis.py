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
