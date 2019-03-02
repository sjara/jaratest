import os
from jaratoolbox import histologyanalysis as ha
from jaratoolbox import settings
reload(settings)
 
tracts = [
    {'subject':'band054', 'brainArea':'LeftAC',
     'recordingTract':'p1-B2-03_lateralDiI_shank4', 'atlasZ':200},

    {'subject':'band054', 'brainArea':'LeftAC',
     'recordingTract':'p1-B5-03_lateralDiI_shank3', 'atlasZ':208},

    {'subject':'band054', 'brainArea':'LeftAC',
     'recordingTract':'p1-C2-03_lateralDiI_shank2', 'atlasZ':210},

    {'subject':'band054', 'brainArea':'LeftAC',
     'recordingTract':'p1-C5-03_lateralDiI_shank1', 'atlasZ':217},

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
