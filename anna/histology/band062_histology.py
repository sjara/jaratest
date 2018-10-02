import os
from jaratoolbox import histologyanalysis as ha
from jaratoolbox import settings
reload(settings)
 
tracts = [
    {'subject':'band062', 'brainArea':'LeftAC',
     'recordingTract':'p1-D4-03_medialDiD_shank4', 'atlasZ':198},

    {'subject':'band062', 'brainArea':'LeftAC',
     'recordingTract':'p2-A2-03_lateralDiD_shank4', 'atlasZ':219},
    
    {'subject':'band062', 'brainArea':'LeftAC',
     'recordingTract':'p2-A2-03_lateralDiO_shank4', 'atlasZ':219},

    {'subject':'band062', 'brainArea':'LeftAC',
     'recordingTract':'p2-A5-03_lateralDiD_shank3', 'atlasZ':222},

    {'subject':'band062', 'brainArea':'LeftAC',
     'recordingTract':'p2-B1-03_medialDiD_shank2', 'atlasZ':224},

    {'subject':'band062', 'brainArea':'LeftAC',
     'recordingTract':'p2-B2-03_lateralDiD_shank2', 'atlasZ':226},

    {'subject':'band062', 'brainArea':'LeftAC',
     'recordingTract':'p2-B2-03_lateralDiO_shank2', 'atlasZ':226},

    {'subject':'band062', 'brainArea':'LeftAC',
     'recordingTract':'p2-B5-03_lateralDiD_shank1', 'atlasZ':228},

    {'subject':'band062', 'brainArea':'RightAC',
     'recordingTract':'p1-D3-02_medialDiD_shank4', 'atlasZ':200},

    {'subject':'band062', 'brainArea':'RightAC',
     'recordingTract':'p1-D4-02_lateralDiO_shank4', 'atlasZ':206},

    {'subject':'band062', 'brainArea':'RightAC',
     'recordingTract':'p1-D4-02_middleDiO_shank4', 'atlasZ':206},

    {'subject':'band062', 'brainArea':'RightAC',
     'recordingTract':'p2-A1-02_medialDiD_shank3', 'atlasZ':209},

    {'subject':'band062', 'brainArea':'RightAC',
     'recordingTract':'p2-A2-02_lateralDiD_shank3', 'atlasZ':220},

    {'subject':'band062', 'brainArea':'RightAC',
     'recordingTract':'p2-A2-02_lateralDiO_shank3', 'atlasZ':220},

    {'subject':'band062', 'brainArea':'RightAC',
     'recordingTract':'p2-A5-02_lateralDiD_shank2', 'atlasZ':222},

    {'subject':'band062', 'brainArea':'RightAC',
     'recordingTract':'p2-A5-02_lateralDiO_shank2', 'atlasZ':222},

    {'subject':'band062', 'brainArea':'RightAC',
     'recordingTract':'p2-A5-02_medialDiD_shank2', 'atlasZ':222},

    {'subject':'band062', 'brainArea':'RightAC',
     'recordingTract':'p2-A5-02_middleDiO_shank2', 'atlasZ':222},

    {'subject':'band062', 'brainArea':'RightAC',
     'recordingTract':'p2-B2-02_lateralDiO_shank1', 'atlasZ':230},

    {'subject':'band062', 'brainArea':'RightAC',
     'recordingTract':'p2-B3-02_middleDiO_shank1', 'atlasZ':232},

    {'subject':'band062', 'brainArea':'RightAC',
     'recordingTract':'p2-B4-02_medialDiD_shank1', 'atlasZ':234},
    ]

#Save svg files for registration
import pdb
HISTOLOGY_PATH = settings.HISTOLOGY_PATH
ATLAS_PATH = settings.ATLAS_PATH
for tract in tracts:
    filenameAtlas = os.path.join(ATLAS_PATH,'allenCCF_Z{}.jpg'.format(tract['atlasZ']))
    #pdb.set_trace()    
    shanksFolder = 'recordingTracts{}'.format(tract['brainArea'])
    registrationFolder = 'registration{}'.format(tract['brainArea'])
    filenameSlice = os.path.join(HISTOLOGY_PATH, '{}_processed'.format(tract['subject']), shanksFolder, '{}.jpg'.format(tract['recordingTract']))
    filenameSVG = os.path.join(HISTOLOGY_PATH, '{}_processed'.format(tract['subject']), registrationFolder, '{}_pre.svg'.format(tract['recordingTract']))
    (atlasSize, sliceSize) = ha.save_svg_for_registration(filenameSVG, filenameAtlas, filenameSlice)
