import os
from jaratoolbox import histologyanalysis as ha
from jaratoolbox import settings
reload(settings)
 
tracts = [
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'middleDiD_shank1', 'atlasZ':195},
          
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'middleDiD_shank2', 'atlasZ':192},
          
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'middleDiD_shank3', 'atlasZ':185},
          
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'middleDiD_shank4', 'atlasZ':180},
          
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'medialDiO_shank4', 'atlasZ':181},
          
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'medialDiO_shank3', 'atlasZ':186},
          
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'medialDiO_shank2', 'atlasZ':190},
          
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'medialDiO_shank1', 'atlasZ':196},
]

#Save svg files for registration
HISTOLOGY_PATH = settings.HISTOLOGY_PATH
for tract in tracts:
    filenameAtlas = '/home/jarauser/data/jarahubdata/atlas/AllenCCF_25/JPEG/allenCCF_Z{}.jpg'.format(tract['atlasZ'])
    shanksFolder = 'recordingTracts{}'.format(tract['brainArea'])
    registrationFolder = 'registration{}'.format(tract['brainArea'])
    filenameSlice = os.path.join(HISTOLOGY_PATH, '{}_processed'.format(tract['subject']), shanksFolder, '{}.jpg'.format(tract['recordingTract']))
    filenameSVG = os.path.join(HISTOLOGY_PATH, '{}_processed'.format(tract['subject']), registrationFolder, '{}_pre.svg'.format(tract['recordingTract']))
    (atlasSize, sliceSize) = ha.save_svg_for_registration(filenameSVG, filenameAtlas, filenameSlice)