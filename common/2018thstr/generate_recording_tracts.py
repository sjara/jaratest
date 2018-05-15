import os
import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import celldatabase
from scipy import stats
import pandas as pd
import xml.etree.ElementTree as ETree
import re
import figparams
from jaratoolbox import histologyanalysis as ha

def tract_fraction(tipCoords, brainSurfCoords, fractionFromSurface):
    refVec = [tipCoords[0]-brainSurfCoords[0], tipCoords[1]-brainSurfCoords[1]]
    vecToAdd = fractionFromSurface * np.array(refVec)
    coordsAtFraction = [brainSurfCoords[0]+vecToAdd[0], brainSurfCoords[1]+vecToAdd[1]]
    return coordsAtFraction

tractsDBPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'tracts_db.h5')
tractsDB = pd.read_hdf(tractsDBPath, key='dataframe')
# tractsDB = pd.DataFrame(allTracts)

# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
db = pd.read_hdf(dbPath, key='dataframe')

goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodLaser = goodShape.query('autoTagged==1')
goodNSpikes = goodLaser.query('nSpikes>2000')

dataframe = goodNSpikes

#The shank number for each tetrode number
shankNum = {1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4}

allFiles = []
for indRow, dbRow in dataframe.iterrows():
    # print dbRow
    info = dbRow['info']
    if isinstance(info, list):
        shankName = info[0]
    else:
        shankName = info

    brainArea = dbRow['brainArea']
    if brainArea=="rightThal":
        registrationFolder = "registrationATh"
        shanksFolder = 'recordingTractsATh'
    elif brainArea=="rightAC":
        registrationFolder = "registrationAC"
        shanksFolder = 'recordingTractsAC'

    subject = dbRow['subject']
    histFullPath = os.path.join(settings.HISTOLOGY_PATH, subject, registrationFolder)

    tetrode = int(dbRow['tetrode'])
    fullFn = os.path.join(histFullPath, "{}_shank{}.svg".format(shankName, shankNum[tetrode]))
    allFiles.append(fullFn)

    fullShankName = "{}_shank{}".format(shankName, shankNum[tetrode])
    tract = tractsDB.query("subject == @subject and recordingTract==@fullShankName")
    filenameSlice = os.path.join(settings.HISTOLOGY_PATH, subject, shanksFolder, '{}.jpg'.format(fullShankName))

    if len(tract)==0:
        # We need the atlas Z to generate the svg_pre files
        # This chunk will show each jpg and allow you to enter a z value, which gets stored in a database.
        # TODO: Figure out why the image.close() method is not working
        # if not os.path.exists(filenameSlice):
        #     print filenameSlice
        image = Image.open(filenameSlice)
        image.show()
        print fullShankName
        atlasZ = input("Enter Atlas Z: ")
        image.close()

        shankDict = {'subject':subject, 'brainArea':dbRow['brainArea'],
                     'recordingTract':fullShankName, 'atlasZ':atlasZ,
                     'maxDepth':dbRow['maxDepth']}

        print shankDict
        tractsDB = tractsDB.append(shankDict, ignore_index=True)

    else: #If we have the atlas z we can proceed with the SVG files
        filenameAtlas = '/mnt/jarahubdata/atlas/AllenCCF_25/JPEG/allenCCF_Z{}.jpg'.format(tract['atlasZ'].values[0])
        filenameSVGpre = os.path.join(settings.HISTOLOGY_PATH, tract['subject'].values[0], registrationFolder, '{}_pre.svg'.format(tract['recordingTract'].values[0]))
        filenameSVG = os.path.join(settings.HISTOLOGY_PATH, tract['subject'].values[0], registrationFolder, '{}.svg'.format(tract['recordingTract'].values[0]))

        if not os.path.exists(filenameSVGpre): # Need to make the SVG file if the pre does not exist
            print "Generating SVG file: {}".format(filenameSVGpre)

            #NOTE: Just to fix some pinp017 alignment issues
            atlasZ = input("Enter Atlas Z: ")
            filenameAtlas = '/mnt/jarahubdata/atlas/AllenCCF_25/JPEG/allenCCF_Z{}.jpg'.format(atlasZ)

            (atlasSize, sliceSize) = ha.save_svg_for_registration(filenameSVGpre, filenameAtlas, filenameSlice)

        if not os.path.exists(filenameSVG): # If we have not registered the svg file yet
            print "Please register {}".format(filenameSVGpre)
            continue

        else: #We have the registered SVG file and can compute the coords for the cell.

            tree = ETree.parse(filenameSVG)
            root=tree.getroot()
            paths = root.findall('{http://www.w3.org/2000/svg}path')
            if len(paths)!=1:
                raise ValueError('The SVG file must contain exactly 1 path')
            pathCoords = paths[0].attrib['d']

            # FIXME:This is the correct way to do it, but not working for me and I'm fed up
            reString = r'[a-zA-Z, ]*(\d+\.*\d*),(\d+\.*\d*)[a-zA-Z, ]*(\d+\.*\d*),(\d+\.*\d*)'
            coordStrings = re.findall(reString, pathCoords, flags=re.IGNORECASE)

            # stackedCoordStrings = [coords.split(',') for coords in pathCoords.split(' ')[1:]]
            # allPathStrings = pathCoords.split(' ')
            # stackedCoordStrings = [coords.split(',') for coords in allPathStrings if ',' in coords]
            # coordStrings = []
            # for coordPair in stackedCoordStrings:
            #     for coord in coordPair:
            #         coordStrings.append(coord)

            # # if len(coordStrings)==0:
            # if len(coordStrings)!=4:
            #     raise ValueError('The path does not have the correct format. You probably did not double click for this tract')
            # tractCoords = coordStrings[0]
            # tractCoords = map(float, tractCoords)
            tractCoords = map(float, coordStrings[0])
            # line = Line(tractCoords)

            tipCoords = [tractCoords[0], tractCoords[1]]
            brainSurfCoords = [tractCoords[2], tractCoords[3]]

            #Was doing this because sometimes Inkscape will use relative path coords and it will break things. 
            import ipdb
            if any(np.array(tipCoords)<1):
                ipdb.set_trace()
            if any(np.array(brainSurfCoords)<1):
                ipdb.set_trace()

            if tipCoords[1] < brainSurfCoords[1]:
                # raise ValueError('The brain surface is deeper than the tip!')
                print "Bad coords, skipping {}".format(tract)
                continue

            cellFracFromSurface = np.array(dbRow['depth'])/float(dbRow['maxDepth'])
            cellCoords = tract_fraction(tipCoords, brainSurfCoords, cellFracFromSurface)
            print "Cell Coords:"
            # print cellCoords.append(tract['atlasZ'].values[0])
            # print cellCoords
            db.loc[indRow, 'cellX'] = cellCoords[0]
            db.loc[indRow, 'cellY'] = cellCoords[1]
            db.loc[indRow, 'cellZ'] = tract['atlasZ'].values[0]

            # if dbRow['subject']=='pinp016':
            #     ipdb.set_trace()

db.to_hdf(dbPath, key='dataframe')


# allUniqueFiles = set(allFiles)

# doneFiles = []
# todoFiles = []
# for fullFn in allUniqueFiles:
#     if os.path.exists(fullFn):
#         doneFiles.append(fullFn)
#     else:
#         todoFiles.append(fullFn)

# for fullFn in doneFiles:
#     print "DONE: {}".format(fullFn)
# for fullFn in todoFiles:
#     print "TODO: {}".format(fullFn)


#Used to first construct the tracts database
# allTracts = [{'subject':'pinp015', 'brainArea':'AC',
#  'maxDepth':1146., 'recordingDepths':[894, 1146],
#  'atlasZ':202, 'recordingTract':'medialDiI_shank1'},

# {'subject':'pinp015', 'brainArea':'AC',
#  'maxDepth':1146., 'recordingDepths':[1146],
#  'atlasZ':205, 'recordingTract':'medialDiI_shank2'},

# {'subject':'pinp015', 'brainArea':'AC',
#  'maxDepth':1146., 'recordingDepths':[957],
#  'atlasZ':209, 'recordingTract':'medialDiI_shank4'},

# {'subject':'pinp015', 'brainArea':'AC',
#  'maxDepth':1503., 'recordingDepths':[957, 1175, 1275, 1378],
#  'atlasZ':201, 'recordingTract':'DiD_shank1'},

# {'subject':'pinp015', 'brainArea':'AC',
#  'maxDepth':1503., 'recordingDepths':[975, 1087],
#  'atlasZ':207, 'recordingTract':'DiD_shank3'},

# {'subject':'pinp015', 'brainArea':'AC',
#  'maxDepth':1503., 'recordingDepths':[975, 1087, 1175],
#  'atlasZ':210, 'recordingTract':'DiD_shank4'},

# {'subject':'pinp016', 'brainArea':'AC',
#  'maxDepth':2051., 'recordingDepths':[2051],
#  'atlasZ':214, 'recordingTract':'lateralDiI_shank1'},

# {'subject':'pinp016', 'brainArea':'AC',
#  'maxDepth':2051., 'recordingDepths':[1904],
#  'atlasZ':202, 'recordingTract':'lateralDiI_shank3'},

# {'subject':'pinp016', 'brainArea':'AC',
#  'maxDepth':2051., 'recordingDepths':[1153, 1904, 2051],
#  'atlasZ':197, 'recordingTract':'lateralDiI_shank4'},

# {'subject':'pinp016', 'brainArea':'AC',
#  'maxDepth':2091., 'recordingDepths':[1143, 1338],
#  'atlasZ':193, 'recordingTract':'extraLateralDiD_shank3'},

# {'subject':'pinp017', 'brainArea':'AC',
#  'maxDepth':1338., 'recordingDepths':[1143],
#  'atlasZ':200, 'recordingTract':'medialDiI_shank1'},

# {'subject':'pinp017', 'brainArea':'AC',
#  'maxDepth':1338., 'recordingDepths':[1143, 1338],
#  'atlasZ':210, 'recordingTract':'medialDiI_shank2'},

# {'subject':'pinp017', 'brainArea':'AC',
#  'maxDepth':1338., 'recordingDepths':[1338],
#  'atlasZ':217, 'recordingTract':'medialDiI_shank3'},

# {'subject':'pinp017', 'brainArea':'AC',
#  'maxDepth':1338., 'recordingDepths':[1143, 1247, 1338],
#  'atlasZ':228, 'recordingTract':'medialDiI_shank4'},

# {'subject':'pinp017', 'brainArea':'AC',
#  'maxDepth':1604., 'recordingDepths':[1281, 1604],
#  'atlasZ':198, 'recordingTract':'medialDiD_shank1'},

# {'subject':'pinp017', 'brainArea':'AC',
#  'maxDepth':1604., 'recordingDepths':[1281, 1518],
#  'atlasZ':205, 'recordingTract':'medialDiD_shank2'},

# {'subject':'pinp017', 'brainArea':'AC',
#  'maxDepth':1604., 'recordingDepths':[1414, 1518],
#  'atlasZ':211,'recordingTract':'medialDiD_shank3'},

# {'subject':'pinp017', 'brainArea':'AC',
#  'maxDepth':1604., 'recordingDepths':[1281, 1518, 1604],
#  'atlasZ':218,'recordingTract':'medialDiD_shank4'},

# {'subject':'pinp017', 'brainArea':'AC',
#  'maxDepth':1525., 'recordingDepths':[1401],
#  'atlasZ':213,'recordingTract':'lateralDiI_shank1'},

# {'subject':'pinp017', 'brainArea':'AC',
#  'maxDepth':1525., 'recordingDepths':[1401, 1525],
#  'atlasZ':215,'recordingTract':'lateralDiI_shank3'},

# {'subject':'pinp017', 'brainArea':'AC',
#  'maxDepth':1525., 'recordingDepths':[1401],
#  'atlasZ':220,'recordingTract':'lateralDiI_shank4'},

# {'subject':'pinp018', 'brainArea':'AC',
#  'maxDepth':1136., 'recordingDepths':[1016],
#  'atlasZ':200,'recordingTract':'DiD_shank2'},

# {'subject':'pinp018', 'brainArea':'AC',
#  'maxDepth':1136., 'recordingDepths':[966],
#  'atlasZ':201,'recordingTract':'DiD_shank4'},

# {'subject':'pinp015', 'brainArea':'ATh',
#     'recordingTract':'medialDiD_shank1', 'atlasZ':194,
#     'maxDepth':3110, 'recordingDepths':[2902]},

# {'subject':'pinp015', 'brainArea':'ATh',
#     'recordingTract':'medialDiD_shank2', 'atlasZ':200,
#     'maxDepth':3110, 'recordingDepths':[3009, 3110]},

# {'subject':'pinp015', 'brainArea':'ATh',
#     'recordingTract':'medialDiD_shank3', 'atlasZ':205,
#     'maxDepth':3110, 'recordingDepths':[2902, 3009, 3110]},

# {'subject':'pinp015', 'brainArea':'ATh',
#     'recordingTract':'medialDiD_shank4', 'atlasZ':209,
#     'maxDepth':3110, 'recordingDepths':[2902, 3009, 3110]},

# {'subject':'pinp016', 'brainArea':'ATh',
#     'recordingTract':'medialDiI_shank1', 'atlasZ':178,
#     'maxDepth':3802, 'recordingDepths':[3797]},

# {'subject':'pinp016', 'brainArea':'ATh',
#     'recordingTract':'lateralDiI_shank1', 'atlasZ':181,
#     'maxDepth':3797, 'recordingDepths':[3797]},

# {'subject':'pinp016', 'brainArea':'ATh',
#     'recordingTract':'extralateralDiD_shank2', 'atlasZ':184,
#     'maxDepth':3800, 'recordingDepths':[3800]},

# {'subject':'pinp016', 'brainArea':'ATh',
#     'recordingTract':'extralateralDiD_shank4', 'atlasZ':189,
#     'maxDepth':3800, 'recordingDepths':[3800]},

# {'subject':'pinp017', 'brainArea':'ATh',
#     'recordingTract':'medialDiI_shank1', 'atlasZ':192,
#     'maxDepth':3349, 'recordingDepths':[3074]},

# {'subject':'pinp017', 'brainArea':'ATh',
#     'recordingTract':'medialDiI_shank2', 'atlasZ':196,
#     'maxDepth':3349, 'recordingDepths':[3210]}
# ]
