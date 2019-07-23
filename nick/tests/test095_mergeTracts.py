import os
import numpy as np
import nrrd
from matplotlib import pyplot as plt
from jaratoolbox import histologyanalysis as ha
from jaratoolbox import settings
from jaratoolbox import extraplots
import xml.etree.ElementTree as ETree
import re

# tracts = [
#     {'subject':'pinp015', 'brainArea':'ATh',
#      'recordingTract':'medialDiD_shank1', 'atlasZ':194}
# ]

#Thalamus, pinp015, pinp016, pinp017
tracts = [
    {'subject':'pinp015', 'brainArea':'ATh',
     'recordingTract':'medialDiD_shank1', 'atlasZ':194,
     'maxDepth':3110, 'recordingDepths':[2902]},

    {'subject':'pinp015', 'brainArea':'ATh',
     'recordingTract':'medialDiD_shank2', 'atlasZ':200,
     'maxDepth':3110, 'recordingDepths':[3009, 3110]},

    {'subject':'pinp015', 'brainArea':'ATh',
     'recordingTract':'medialDiD_shank3', 'atlasZ':205,
     'maxDepth':3110, 'recordingDepths':[2902, 3009, 3110]},

    {'subject':'pinp015', 'brainArea':'ATh',
     'recordingTract':'medialDiD_shank4', 'atlasZ':209,
     'maxDepth':3110, 'recordingDepths':[2902, 3009, 3110]},

    {'subject':'pinp016', 'brainArea':'ATh',
     'recordingTract':'medialDiI_shank1', 'atlasZ':178,
     'maxDepth':3802, 'recordingDepths':[3797]},

    {'subject':'pinp016', 'brainArea':'ATh',
     'recordingTract':'lateralDiI_shank1', 'atlasZ':181,
     'maxDepth':3797, 'recordingDepths':[3797]},

    {'subject':'pinp016', 'brainArea':'ATh',
     'recordingTract':'extraLateralDiD_shank2', 'atlasZ':184,
     'maxDepth':3800, 'recordingDepths':[3800]},

    {'subject':'pinp016', 'brainArea':'ATh',
     'recordingTract':'extraLateralDiD_shank4', 'atlasZ':189,
     'maxDepth':3800, 'recordingDepths':[3800]},

    {'subject':'pinp017', 'brainArea':'ATh',
     'recordingTract':'medialDiI_shank1', 'atlasZ':192,
     'maxDepth':3349, 'recordingDepths':[3074]},

    {'subject':'pinp017', 'brainArea':'ATh',
     'recordingTract':'medialDiI_shank2', 'atlasZ':196,
     'maxDepth':3349, 'recordingDepths':[3210]}
]

atlasPath = os.path.join(settings.ALLEN_ATLAS_DIR, 'coronal_average_template_25.nrrd')
atlasData = nrrd.read(atlasPath)
atlas = atlasData[0]

#Hardcoded stuff
atlasWidth = 456
atlasHeight = 320

# class Line(object):
#     def __init__(self, coords):
#         self.x = [coords[0], coords[2]]
#         self.y = [coords[1], coords[3]]

HISTOLOGY_PATH = settings.HISTOLOGY_PATH

#This splits the penetrations into 3 groups with similar atlas z values
zBounds = [185, 197]


def tract_fraction(tipCoords, brainSurfCoords, fractionFromSurface):
    refVec = [tipCoords[0]-brainSurfCoords[0], tipCoords[1]-brainSurfCoords[1]]
    vecToAdd = fractionFromSurface * np.array(refVec)
    coordsAtFraction = [brainSurfCoords[0]+vecToAdd[0], brainSurfCoords[1]+vecToAdd[1]]
    return coordsAtFraction

for tract in tracts:
    registrationFolder = 'registration{}'.format(tract['brainArea'])
    filenameSVG = os.path.join(HISTOLOGY_PATH, tract['subject'], registrationFolder, '{}.svg'.format(tract['recordingTract']))
    tree = ETree.parse(filenameSVG)
    root=tree.getroot()
    paths = root.findall('{http://www.w3.org/2000/svg}path')
    if len(paths)!=1:
        raise ValueError('The SVG file must contain exactly 1 path')
    pathCoords = paths[0].attrib['d']
    reString = r'M (\d+\.*\d*),(\d+\.*\d*) (\d+\.*\d*),(\d+\.*\d*)'
    coordStrings = re.findall(reString, pathCoords)
    if len(coordStrings)==0:
        raise ValueError('The path does not have the correct format. You probably did not double click for this tract')
    tractCoords = coordStrings[0]
    tractCoords = map(float, tractCoords)
    # line = Line(tractCoords)

    tipCoords = [tractCoords[0], tractCoords[1]]
    brainSurfCoords = [tractCoords[2], tractCoords[3]]

    if tipCoords[1] < brainSurfCoords[1]:
        raise ValueError('The brain surface is deeper than the tip!')

    siteFracFromSurface = np.array(tract['recordingDepths'])/float(tract['maxDepth'])
    siteCoords = [tract_fraction(tipCoords, brainSurfCoords, fracFromSurface) for fracFromSurface in siteFracFromSurface]
    tract.update({'siteCoords':siteCoords, 'tipCoords':tipCoords, 'brainSurfCoords':brainSurfCoords})

plt.close('all')

numFigs = len(zBounds)+1
figs = []
axs = []
for indFig in range(numFigs):
    fig, ax = plt.subplots()
    ax.set_xlim([0, atlasWidth])
    ax.set_ylim([0, atlasHeight])
    ax.invert_yaxis()
    figs.append(fig)
    axs.append(ax)

lineColor = 'r'
lineWidth = 1
markerColor = 'r'

for tract in tracts:

    # FIXME: This only works for 2 bounds

    if tract['atlasZ']<zBounds[0]:
        tractAx = axs[0]
        tractFig = figs[0]
        sliceNum = 181
    elif (tract['atlasZ']>zBounds[0]) & (tract['atlasZ']<zBounds[1]):
        tractAx = axs[1]
        tractFig = figs[1]
        sliceNum = 193
    elif (tract['atlasZ']>zBounds[1]):
        tractAx = axs[2]
        tractFig = figs[2]
        sliceNum = 206
    plt.sca(tractAx)
    plt.figure(tractFig.number)

    tractAx.imshow(np.rot90(atlas[:,:,sliceNum], -1), 'gray')
    plt.hold(1)
    tractAx.plot([tract['tipCoords'][0], tract['brainSurfCoords'][0]], [tract['tipCoords'][1], tract['brainSurfCoords'][1]],
                color=lineColor, linewidth=lineWidth)
    for coordPair in tract['siteCoords']:
        tractAx.plot(coordPair[0], coordPair[1], '*', mfc=markerColor, mec=markerColor)
    plt.hold(1)

for indFig, fig in enumerate(figs):
    plt.figure(fig.number)
    extraplots.save_figure('tracts{}'.format(indFig+1), 'svg', (5, 3), outputDir='/tmp')
plt.show()
