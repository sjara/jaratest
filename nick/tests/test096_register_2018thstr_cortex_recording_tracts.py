import os
from jaratoolbox import histologyanalysis as ha
from jaratoolbox import settings

tracts = [
{'subject':'pinp015', 'brainArea':'AC',
 'maxDepth':1146., 'recordingDepths':[894, 1146],
 'atlasZ':202, 'recordingTract':'medialDiI_shank1'},

{'subject':'pinp015', 'brainArea':'AC',
 'maxDepth':1146., 'recordingDepths':[1146],
 'atlasZ':205, 'recordingTract':'medialDiI_shank2'},

{'subject':'pinp015', 'brainArea':'AC',
 'maxDepth':1146., 'recordingDepths':[957],
 'atlasZ':209, 'recordingTract':'medialDiI_shank4'},

{'subject':'pinp015', 'brainArea':'AC',
 'maxDepth':1503., 'recordingDepths':[957, 1175, 1275, 1378],
 'atlasZ':201, 'recordingTract':'DiD_shank1'},

{'subject':'pinp015', 'brainArea':'AC',
 'maxDepth':1503., 'recordingDepths':[975],
 'atlasZ':204, 'recordingTract':'DiD_shank2'},

{'subject':'pinp015', 'brainArea':'AC',
 'maxDepth':1503., 'recordingDepths':[975, 1087],
 'atlasZ':207, 'recordingTract':'DiD_shank3'},

{'subject':'pinp015', 'brainArea':'AC',
 'maxDepth':1503., 'recordingDepths':[975, 1087, 1175],
 'atlasZ':210, 'recordingTract':'DiD_shank4'},

{'subject':'pinp016', 'brainArea':'AC',
 'maxDepth':2051., 'recordingDepths':[2051],
 'atlasZ':214, 'recordingTract':'lateralDiI_shank1'},

{'subject':'pinp016', 'brainArea':'AC',
 'maxDepth':2051., 'recordingDepths':[1904],
 'atlasZ':202, 'recordingTract':'lateralDiI_shank3'},

{'subject':'pinp016', 'brainArea':'AC',
 'maxDepth':2051., 'recordingDepths':[1153, 1904, 2051],
 'atlasZ':197, 'recordingTract':'lateralDiI_shank4'},

{'subject':'pinp016', 'brainArea':'AC',
 'maxDepth':2091., 'recordingDepths':[1143, 1338],
 'atlasZ':193, 'recordingTract':'extraLateralDiD_shank3'},

{'subject':'pinp017', 'brainArea':'AC',
 'maxDepth':1338., 'recordingDepths':[1143],
 'atlasZ':200, 'recordingTract':'medialDiI_shank1'},

{'subject':'pinp017', 'brainArea':'AC',
 'maxDepth':1338., 'recordingDepths':[1143, 1338],
 'atlasZ':210, 'recordingTract':'medialDiI_shank2'},

{'subject':'pinp017', 'brainArea':'AC',
 'maxDepth':1338., 'recordingDepths':[1338],
 'atlasZ':217, 'recordingTract':'medialDiI_shank3'},

{'subject':'pinp017', 'brainArea':'AC',
 'maxDepth':1338., 'recordingDepths':[1143, 1247, 1338],
 'atlasZ':228, 'recordingTract':'medialDiI_shank4'},

{'subject':'pinp017', 'brainArea':'AC',
 'maxDepth':1604., 'recordingDepths':[1281, 1604],
 'atlasZ':198, 'recordingTract':'medialDiD_shank1'},

{'subject':'pinp017', 'brainArea':'AC',
 'maxDepth':1604., 'recordingDepths':[1281, 1518],
 'atlasZ':205, 'recordingTract':'medialDiD_shank2'},

{'subject':'pinp017', 'brainArea':'AC',
 'maxDepth':1604., 'recordingDepths':[1414, 1518],
 'atlasZ':211,'recordingTract':'medialDiD_shank3'},

{'subject':'pinp017', 'brainArea':'AC',
 'maxDepth':1604., 'recordingDepths':[1281, 1518, 1604],
 'atlasZ':218,'recordingTract':'medialDiD_shank4'},

{'subject':'pinp017', 'brainArea':'AC',
 'maxDepth':1525., 'recordingDepths':[1401],
 'atlasZ':213,'recordingTract':'lateralDiI_shank1'},

{'subject':'pinp017', 'brainArea':'AC',
 'maxDepth':1525., 'recordingDepths':[1401, 1525],
 'atlasZ':215,'recordingTract':'lateralDiI_shank3'},

{'subject':'pinp017', 'brainArea':'AC',
 'maxDepth':1525., 'recordingDepths':[1401],
 'atlasZ':220,'recordingTract':'lateralDiI_shank4'},

{'subject':'pinp018', 'brainArea':'AC',
 'maxDepth':1136., 'recordingDepths':[1016],
 'atlasZ':200,'recordingTract':'DiD_shank2'},

{'subject':'pinp018', 'brainArea':'AC',
 'maxDepth':1136., 'recordingDepths':[966],
 'atlasZ':201,'recordingTract':'DiD_shank4'}
    ]

HISTOLOGY_PATH = settings.HISTOLOGY_PATH
for tract in tracts:
    filenameAtlas = '/mnt/jarahubdata/atlas/AllenCCF_25/JPEG/allenCCF_Z{}.jpg'.format(tract['atlasZ'])
    shanksFolder = 'recordingTracts{}'.format(tract['brainArea'])
    registrationFolder = 'registration{}'.format(tract['brainArea'])
    filenameSlice = os.path.join(HISTOLOGY_PATH, tract['subject'], shanksFolder, '{}.jpg'.format(tract['recordingTract']))
    filenameSVG = os.path.join(HISTOLOGY_PATH, tract['subject'], registrationFolder, '{}_pre.svg'.format(tract['recordingTract']))
    (atlasSize, sliceSize) = ha.save_svg_for_registration(filenameSVG, filenameAtlas, filenameSlice)
