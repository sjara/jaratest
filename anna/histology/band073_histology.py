import os
from jaratoolbox import histologyanalysis as ha
from jaratoolbox import settings
reload(settings)
 
tracts = [
    {'subject':'band073', 'brainArea':'LeftAC',
     'recordingTract':'p1-C5-03_midlateralDiO_shank1', 'atlasZ':180},

    {'subject':'band073', 'brainArea':'LeftAC',
     'recordingTract':'p1_D1-03_medialDiD_shank1', 'atlasZ':185},

    {'subject':'band073', 'brainArea':'LeftAC',
     'recordingTract':'p1_D5-03_medialDiD_shank2', 'atlasZ':193},

    {'subject':'band073', 'brainArea':'LeftAC',
     'recordingTract':'p1-D2-03_midlateralDiO_shank2', 'atlasZ':188},

    {'subject':'band073', 'brainArea':'LeftAC',
     'recordingTract':'p2_A1-03_medialDiD_shank3', 'atlasZ':200},

    {'subject':'band073', 'brainArea':'LeftAC',
     'recordingTract':'p2_A5-03_medialDiD_shank4', 'atlasZ':208},

    {'subject':'band073', 'brainArea':'RightAC',
     'recordingTract':'p2-A2-02_middleDiO_shank4', 'atlasZ':201},

    {'subject':'band073', 'brainArea':'RightAC',
     'recordingTract':'p2-A5-02_middleDiO_shank3', 'atlasZ':206},

    {'subject':'band073', 'brainArea':'RightAC',
     'recordingTract':'p2-B3-02_middleDiO_shank2', 'atlasZ':212},

    {'subject':'band073', 'brainArea':'RightAC',
     'recordingTract':'p2-B5-02_medialDiD_shank1', 'atlasZ':219},

    {'subject':'band073', 'brainArea':'RightAC',
     'recordingTract':'p2-C2-02_middleDiO_shank1', 'atlasZ':225},
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
