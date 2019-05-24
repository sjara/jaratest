import os
from jaratoolbox import histologyanalysis as ha
from jaratoolbox import settings
reload(settings)
 
tracts = [
    {'subject':'band056', 'brainArea':'LeftAC',
     'recordingTract':'p2-A3-03_medialDiO_shank1', 'atlasZ':227},

    {'subject':'band056', 'brainArea':'LeftAC',
     'recordingTract':'p2-A2-03_medialDiO_shank2', 'atlasZ':225},

    {'subject':'band056', 'brainArea':'LeftAC',
     'recordingTract':'p1-C6-03_middleDiD_shank3', 'atlasZ':211},

    {'subject':'band056', 'brainArea':'LeftAC',
     'recordingTract':'p1-C4-03_middleDiD_shank4', 'atlasZ':209},

    {'subject':'band056', 'brainArea':'RightAC',
     'recordingTract':'p1-C4-02_lateralDiD_shank1', 'atlasZ':203},

    {'subject':'band056', 'brainArea':'RightAC',
     'recordingTract':'p2-B1-02_lateralDiO_shank1', 'atlasZ':232},

    {'subject':'band056', 'brainArea':'RightAC',
     'recordingTract':'p2-A1-02_lateralDiO_shank3', 'atlasZ':224},

    {'subject':'band056', 'brainArea':'RightAC',
     'recordingTract':'p1-D3-02_lateralDiO_shank4', 'atlasZ':221},

    {'subject':'band056', 'brainArea':'RightAC',
     'recordingTract':'p1-D3-02_medialDiD_shank1', 'atlasZ':221},

    {'subject':'band056', 'brainArea':'RightAC',
     'recordingTract':'p1-C5-02_medialDiD_shank2', 'atlasZ':208},

    {'subject':'band056', 'brainArea':'RightAC',
     'recordingTract':'p1-C2-02_medialDiD_shank3', 'atlasZ':200},

    {'subject':'band056', 'brainArea':'RightAC',
     'recordingTract':'p1-B4-02_medialDiD_shank4', 'atlasZ':192},

    {'subject':'band056', 'brainArea':'RightAC',
     'recordingTract':'p2-A3-02_middleDiO_shank1', 'atlasZ':227},

    {'subject':'band056', 'brainArea':'RightAC',
     'recordingTract':'p1-C4-02_middleDiD_shank1', 'atlasZ':203}
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
