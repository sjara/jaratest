import os
from jaratoolbox import histologyanalysis as ha
from jaratoolbox import settings

# pinp015, ATh, medialDiD (max depth 3110) ('pinp015', '2017-02-15')
## shank 1: 194
## shank 2: 200
## shank 3: 205
## shank 4: 209

#pinp016, ATh, medialDiI (maxDepth 3802) ('pinp016', '2017-03-14')
## shank 1: 178

#pinp016, ATh, lateralDiI (maxDepth 3797) ('pinp016', '2017-03-15')
## shank 1: 181

#pinp016, ATh, extraLateralDiD (maxDepth 3800) ('pinp016', '2017-03-16')
## shank 2, 184

# subject = 'pinp015'
# brainArea = 'ATh'
# recordingTract = 'medialDiD_shank1'
# atlasZ = 184

# tracts = [
#     {'subject':'pinp015', 'brainArea':'ATh',
#      'recordingTract':'medialDiD_shank1', 'atlasZ':194},
#     {'subject':'pinp015', 'brainArea':'ATh',
#      'recordingTract':'medialDiD_shank2', 'atlasZ':200},
#     {'subject':'pinp015', 'brainArea':'ATh',
#      'recordingTract':'medialDiD_shank3', 'atlasZ':205},
#     {'subject':'pinp015', 'brainArea':'ATh',
#      'recordingTract':'medialDiD_shank4', 'atlasZ':209},
# ]

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



#Save svg files for registration
HISTOLOGY_PATH = settings.HISTOLOGY_PATH
for tract in tracts:
    filenameAtlas = '/mnt/jarahubdata/atlas/AllenCCF_25/JPEG/allenCCF_Z{}.jpg'.format(tract['atlasZ'])
    shanksFolder = 'recordingTracts{}'.format(tract['brainArea'])
    registrationFolder = 'registration{}'.format(tract['brainArea'])
    filenameSlice = os.path.join(HISTOLOGY_PATH, tract['subject'], shanksFolder, '{}.jpg'.format(tract['recordingTract']))
    filenameSVG = os.path.join(HISTOLOGY_PATH, tract['subject'], registrationFolder, '{}_pre.svg'.format(tract['recordingTract']))
    (atlasSize, sliceSize) = ha.save_svg_for_registration(filenameSVG, filenameAtlas, filenameSlice)

