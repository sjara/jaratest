import os
from jaratoolbox import histologyanalysis as ha
from jaratoolbox import settings
reload(settings)
 
tracts = [
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'p1-D6-03_middleDiD_shank1', 'atlasZ':196},
          
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'p1-D3-03_middleDiD_shank2', 'atlasZ':190},
          
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'p1-C6-03_middleDiD_shank3', 'atlasZ':182},
          
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'p1-C2-03_middleDiD_shank4', 'atlasZ':176},
          
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'p1-C6-03_medialDiO_shank3', 'atlasZ':182},
          
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'p1-D2-03_medialDiO_shank2', 'atlasZ':188},
          
    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'p1-D5-03_medialDiO_shank1', 'atlasZ':194},

    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'p1-D6-03_lateralDiO_shank1', 'atlasZ':196},

    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'p1-D3-03_lateralDiO_shank2', 'atlasZ':190},

    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'p1-C6-03_lateralDiO_shank3', 'atlasZ':182},	

    {'subject':'band055', 'brainArea':'LeftAC',
     'recordingTract':'p1-C2-03_lateralDiO_shank4', 'atlasZ':176},

    {'subject':'band055', 'brainArea':'RightAC',
     'recordingTract':'p2-A4-02_lateralDiI_shank1', 'atlasZ':207},

    {'subject':'band055', 'brainArea':'RightAC',
     'recordingTract':'p1-D4-02_lateralDiI_shank3', 'atlasZ':191},

    {'subject':'band055', 'brainArea':'RightAC',
     'recordingTract':'p1-D2-02_lateralDiI_shank4', 'atlasZ':188},

    {'subject':'band055', 'brainArea':'RightAC',
     'recordingTract':'p2-A6-02_medialDiI_shank1', 'atlasZ':210},

    {'subject':'band055', 'brainArea':'RightAC',
     'recordingTract':'p2-A4-02_medialDiI_shank2', 'atlasZ':207},

    {'subject':'band055', 'brainArea':'RightAC',
     'recordingTract':'p1-D6-02_medialDiI_shank4', 'atlasZ':197},

    {'subject':'band055', 'brainArea':'RightAC',
     'recordingTract':'p2-A4-02_middleDiD_shank1', 'atlasZ':207},

    {'subject':'band055', 'brainArea':'RightAC',
     'recordingTract':'p2-A2-02_middleDiD_shank2', 'atlasZ':203},

    {'subject':'band055', 'brainArea':'RightAC',
     'recordingTract':'p1-D6-02_middleDiD_shank3', 'atlasZ':197},

    {'subject':'band055', 'brainArea':'RightAC',
     'recordingTract':'p1-D5-02_middleDiD_shank4', 'atlasZ':193}, 
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
