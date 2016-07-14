from jaratoolbox import histologyanalysis
from jaratoolbox import settings
import matplotlib.pyplot as plt
reload(histologyanalysis)
import json
import os


animalName = 'anat027'
localHistologyDir = settings.HISTOLOGY_PATH
coordsFromFile = []

def reference_grid(site, side, refSliceNumber):

    if site == 'injection':
        imageBaseName = '-'.join([animalName, 'regwhole'])
        referenceFilename, imageFolder = injection_image_filename('b', refSliceNumber, imageBaseName, localHistologyDir, animalName)
        ogrid = histologyanalysis.OverlayGrid(referenceFilename, nRows = 4, nCols = 3)
        ogrid.set_grid()
        # ogridSite = site
        # ogridSide = side
        # overlayFilename, ogridOverlayFolder = injection_overlay_filename('b', refSliceNumber, imageBaseName, localHistologyDir, animalName, side)


    elif site == 'mgn':
        imageBaseName = '-'.join([animalName, 'regMGN'])
        referenceFilename, imageFolder = mgn_image_filename('b', side, refSliceNumber, imageBaseName, localHistologyDir, animalName)
        ogrid = histologyanalysis.OverlayGrid(referenceFilename, nRows = 4, nCols = 3)
        ogrid.set_grid()
        # ogridSite = site
        # ogridSide = side
        # overlayFilename, ogridOverlayFolder = mgn_overlay_filename('b', side, refSliceNumber, imageBaseName, localHistologyDir, animalName)

    else:
        print "Site must be either 'injection' or 'mgn'"
        pass

def save_coords():

    overlayFolder = ogridOverlayFolder
    side = ogridSide
    coordsFileName = os.path.join(overlayFolder, 'coords_{}.json'.format(side)) 
    print "Writing coords file:"
    print coordsFileName
    with open(coordsFileName, 'w') as f:
        json.dump(ogrid.coords, f)


def load_coords(site, side):

    if site == 'injection':
        imageBaseName = '-'.join([animalName, 'regwhole'])
        overlayFilename, overlayFolder = injection_overlay_filename('b', 1, imageBaseName, localHistologyDir, animalName, side)
        coordsFileName = os.path.join(overlayFolder, 'coords_{}.json'.format(side)) 

    elif site == 'mgn':
        imageBaseName = '-'.join([animalName, 'regMGN'])
        overlayFilename, overlayFolder = mgn_overlay_filename('b', side, 1, imageBaseName, localHistologyDir, animalName)
        coordsFileName = os.path.join(overlayFolder, 'coords_{}.json'.format(side)) 


    coordsFileName = os.path.join(overlayFolder, 'coords_{}.json'.format(side)) 
    with open(coordsFileName, 'r') as f:
        coords = json.load(f)

    return coords

def apply_to_slices(site, side, loadCoords = False, nCols = None, nRows = None):

    if loadCoords:
        coords = load_coords(site, side)
    else:
        if isinstance(ogrid, histologyanalysis.OverlayGrid):
            coords = ogrid.coords
        else:
            print "Requires an OverlayGrid object if loadCoords = False"


    if site == 'injection':
        imageBaseName = '-'.join([animalName, 'regwhole'])
        referenceFilename, imageFolder = injection_image_filename('b', 0, imageBaseName, localHistologyDir, animalName)
        num_slices = count_slices(imageFoler)

        for i in range(num_slices):
            for channel in ['b', 'g', 'r']:
                sliceName = injection_image_filename(channel, i, imageBaseName, localHistologyDir, animalName)
                histologyanalysis.OverlayGrid.apply_grid(sliceName, coords, nRows, nCols)
                overlayFilename, overlayFolder = injection_overlay_filename(channel, i, imageBaseName, localHistologyDir, animalName, side)
                plt.savefig(overlayFilename)

    elif site == 'mgn':
        imageBaseName = '-'.join([animalName, 'regMGN'])
        referenceFilename, imageFolder = mgn_image_filename('b', side, 0, imageBaseName, localHistologyDir, animalName)
        num_slices = count_slices(imageFolder)

        for i in range(num_slices):
            for channel in ['b', 'g', 'r']:
                sliceName = mgn_image_filename(channel, side, i, imageBaseName, localHistologyDir, animalName)
                histologyanalysis.OverlayGrid.apply_grid(sliceName, coords, nRows, nCols)
                overlayFilename, overlayFolder = mgn_overlay_filename(channel, side, i, imageBaseName, localHistologyDir, animalName, side)
                plt.savefig(overlayFilename)

    else:
        print "Site must be either 'injection' or 'mgn'"

def count_slices(directory):
    slice_count = len([f for f in os.listdir(directory) if f.startswith(animalName)])
    return slice_count

def injection_image_filename(channel, imNumber, imageBaseName, localHistologyDir, animalName):
    baseName = '-'.join([imageBaseName, channel])
    fullImageName = ''.join([baseName, '{:04d}'.format(imNumber), '.jpg'])
    imageFolder = os.path.join(localHistologyDir, animalName, '1.25', 'registered', '{}Channel'.format(channel))
    fullImagePath = os.path.join(imageFolder, fullImageName)
    return fullImagePath, imageFolder

def injection_overlay_filename(channel, imNumber, imageBaseName, localHistologyDir, animalName, side):
    baseName = '-'.join([imageBaseName, channel])
    overlayImageName = ''.join([baseName, '{:04d}'.format(imNumber), 'gridOverlay', '.jpg'])
    overlayFolder = os.path.join(localHistologyDir, animalName, '1.25', 'registered', '{}Channel'.format(channel), 'gridOverlay', side)
    if not os.path.exists(overlayFolder):
        print "Making directory {}".format(overlayFolder)
        os.makedirs(overlayFolder)
    overlayImagePath = os.path.join(overlayFolder, overlayImageName)
    return overlayImagePath, overlayFolder

def mgn_image_filename(channel, side, imNumber, imageBaseName, localHistologyDir, animalName):
    baseName = '-'.join([imageBaseName, channel])
    fullImageName = ''.join([baseName, '{:04d}'.format(imNumber), '.jpg'])
    imageFolder = os.path.join(localHistologyDir, animalName, '2.5', side, 'registered', '{}Channel'.format(channel))
    fullImagePath = os.path.join(imageFolder, fullImageName)
    return fullImagePath, imageFolder

def mgn_overlay_filename(channel, side, imNumber, imageBaseName, localHistologyDir, animalName):
    baseName = '-'.join([imageBaseName, channel])
    overlayImageName = ''.join([baseName, '{:04d}'.format(imNumber), 'gridOverlay', '.jpg'])
    overlayFolder = os.path.join(localHistologyDir, animalName, '2.5', side, 'registered', '{}Channel'.format(channel), 'gridOverlay')
    if not os.path.exists(overlayFolder):
        print "Making directory {}".format(overlayFolder)
        os.makedirs(overlayFolder)
    overlayImagePath = os.path.join(overlayFolder, overlayImageName)
    return overlayImagePath, overlayFolder 

    


reference_grid('mgn', 'left', 1)
