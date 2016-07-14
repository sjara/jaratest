from jaratoolbox import histologyanalysis
from jaratoolbox import settings
import matplotlib.pyplot as plt
reload(histologyanalysis)
import json
import os
        
class RegisteredBrainGrid(object):

    def __init__(self, animalName):
        
        self.animalName = animalName
        self.localHistologyDir = settings.HISTOLOGY_PATH
        self.coordsFromFile = []

    def reference_grid(self, site, side, refSliceNumber):

        if site == 'injection':
            imageBaseName = '-'.join([self.animalName, 'regwhole'])
            referenceFilename, imageFolder = self.injection_image_filename('b', refSliceNumber, imageBaseName, self.localHistologyDir, self.animalName)
            self.ogrid = histologyanalysis.OverlayGrid(referenceFilename, nRows = 4, nCols = 3)
            self.ogrid.set_grid()
            self.ogridSite = site
            self.ogridSide = side
            overlayFilename, self.ogridOverlayFolder = self.injection_overlay_filename('b', refSliceNumber, imageBaseName, self.localHistologyDir, self.animalName, side)
            
            

        elif site == 'mgn':
            imageBaseName = '-'.join([self.animalName, 'regMGN'])
            referenceFilename, imageFolder = self.mgn_image_filename('b', side, refSliceNumber, imageBaseName, self.localHistologyDir, self.animalName)
            self.ogrid = histologyanalysis.OverlayGrid(referenceFilename, nRows = 4, nCols = 3)
            self.ogrid.set_grid()
            self.ogridSite = site
            self.ogridSide = side
            overlayFilename, self.ogridOverlayFolder = self.mgn_overlay_filename('b', side, refSliceNumber, imageBaseName, self.localHistologyDir, self.animalName)
            
        else:
            print "Site must be either 'injection' or 'mgn'"
            pass
            
    def save_coords(self):
        
        overlayFolder = self.ogridOverlayFolder
        side = self.ogridSide
        coordsFileName = os.path.join(overlayFolder, 'coords_{}.json'.format(side)) 
        print "Writing coords file:"
        print coordsFileName
        with open(coordsFileName, 'w') as f:
            json.dump(self.ogrid.coords, f)
            

    def load_coords(self, site, side):

        if site == 'injection':
            imageBaseName = '-'.join([self.animalName, 'regwhole'])
            overlayFilename, overlayFolder = self.injection_overlay_filename('b', 1, imageBaseName, self.localHistologyDir, self.animalName, side)
            coordsFileName = os.path.join(overlayFolder, 'coords_{}.json'.format(side)) 
            
        elif site == 'mgn':
            imageBaseName = '-'.join([self.animalName, 'regMGN'])
            overlayFilename, overlayFolder = self.mgn_overlay_filename('b', side, 1, imageBaseName, self.localHistologyDir, self.animalName)
            coordsFileName = os.path.join(overlayFolder, 'coords_{}.json'.format(side)) 

        
        coordsFileName = os.path.join(overlayFolder, 'coords_{}.json'.format(side)) 
        with open(coordsFileName, 'r') as f:
            coords = json.load(f)

        return coords

    def apply_to_slices(self, site, side, loadCoords = False, nCols = None, nRows = None):
        
        if loadCoords:
            coords = self.load_coords(site, side)
        else:
            if isinstance(self.ogrid, histologyanalysis.OverlayGrid):
                coords = self.ogrid.coords
            else:
                print "Requires an OverlayGrid object if loadCoords = False"
            
        
        if site == 'injection':
            imageBaseName = '-'.join([self.animalName, 'regwhole'])
            referenceFilename, imageFolder = self.injection_image_filename('b', 0, imageBaseName, self.localHistologyDir, self.animalName)
            num_slices = self.count_slices(imageFolder)

            for i in range(num_slices):
                for channel in ['b', 'g', 'r']:
                    sliceName = self.injection_image_filename(channel, i, imageBaseName, self.localHistologyDir, self.animalName)
                    histologyanalysis.OverlayGrid.apply_grid(sliceName, coords, nRows, nCols)
                    overlayFilename, overlayFolder = self.injection_overlay_filename(channel, i, imageBaseName, self.localHistologyDir, self.animalName, side)
                    plt.savefig(overlayFilename)

        elif site == 'mgn':
            imageBaseName = '-'.join([self.animalName, 'regMGN'])
            referenceFilename, imageFolder = self.mgn_image_filename('b', side, 0, imageBaseName, self.localHistologyDir, self.animalName)
            num_slices = self.count_slices(imageFolder)

            for i in range(num_slices):
                for channel in ['b', 'g', 'r']:
                    sliceName = self.mgn_image_filename(channel, side, i, imageBaseName, self.localHistologyDir, self.animalName)
                    histologyanalysis.OverlayGrid.apply_grid(sliceName, coords, nRows, nCols)
                    overlayFilename, overlayFolder = self.mgn_overlay_filename(channel, side, i, imageBaseName, self.localHistologyDir, self.animalName, side)
                    plt.savefig(overlayFilename)

        else:
            print "Site must be either 'injection' or 'mgn'"

    def count_slices(self, directory):
        slice_count = len([f for f in os.listdir(directory) if f.startswith(self.animalName)])
        return slice_count
        
    def injection_image_filename(self, channel, imNumber, imageBaseName, localHistologyDir, animalName):
        baseName = '-'.join([imageBaseName, channel])
        fullImageName = ''.join([baseName, '{:04d}'.format(imNumber), '.jpg'])
        imageFolder = os.path.join(localHistologyDir, animalName, '1.25', 'registered', '{}Channel'.format(channel))
        fullImagePath = os.path.join(imageFolder, fullImageName)
        return fullImagePath, imageFolder
        
    def injection_overlay_filename(self, channel, imNumber, imageBaseName, localHistologyDir, animalName, side):
        baseName = '-'.join([imageBaseName, channel])
        overlayImageName = ''.join([baseName, '{:04d}'.format(imNumber), 'gridOverlay', '.jpg'])
        overlayFolder = os.path.join(localHistologyDir, animalName, '1.25', 'registered', '{}Channel'.format(channel), 'gridOverlay', side)
        if not os.path.exists(overlayFolder):
            print "Making directory {}".format(overlayFolder)
            os.makedirs(overlayFolder)
        overlayImagePath = os.path.join(overlayFolder, overlayImageName)
        return overlayImagePath, overlayFolder

    def mgn_image_filename(self, channel, side, imNumber, imageBaseName, localHistologyDir, animalName):
        baseName = '-'.join([imageBaseName, channel])
        fullImageName = ''.join([baseName, '{:04d}'.format(imNumber), '.jpg'])
        imageFolder = os.path.join(localHistologyDir, animalName, '2.5', side, 'registered', '{}Channel'.format(channel))
        fullImagePath = os.path.join(imageFolder, fullImageName)
        return fullImagePath, imageFolder
        
    def mgn_overlay_filename(self, channel, side, imNumber, imageBaseName, localHistologyDir, animalName):
        baseName = '-'.join([imageBaseName, channel])
        overlayImageName = ''.join([baseName, '{:04d}'.format(imNumber), 'gridOverlay', '.jpg'])
        overlayFolder = os.path.join(localHistologyDir, animalName, '2.5', side, 'registered', '{}Channel'.format(channel), 'gridOverlay')
        if not os.path.exists(overlayFolder):
            print "Making directory {}".format(overlayFolder)
            os.makedirs(overlayFolder)
        overlayImagePath = os.path.join(overlayFolder, overlayImageName)
        return overlayImagePath, overlayFolder 
    
    
if __name__=='__main__':
    overlayObj = RegisteredBrainGrid('anat027')
    #overlayObj.reference_grid('injection', 'left', 33)
    overlayObj.reference_grid('mgn', 'left', 1)
#fixme: use 2.5 instead of mgn
    
        
        
        

        

'''
mouse = 'anat027'

localHistologyDir = '/mnt/jarahubdata/histology/'

imageBaseName = '-'.join([mouse, 'regwhole'])

def image_filename(channel, imNumber, imageBaseName, localHistologyDir, mouse):
    baseName = '-'.join([imageBaseName, channel])
    fullImageName = ''.join([baseName, '{:04d}'.format(imNumber), '.jpg'])
    imageFolder = os.path.join(localHistologyDir, mouse, '1.25', 'registered', '{}Channel'.format(channel))
    fullImagePath = os.path.join(imageFolder, fullImageName)
    return fullImagePath

def overlay_filename(channel, imNumber, imageBaseName, localHistologyDir, mouse, side):
    baseName = '-'.join([imageBaseName, channel])
    overlayImageName = ''.join([baseName, '{:04d}'.format(imNumber), 'gridOverlay', '.jpg'])
    overlayFolder = os.path.join(localHistologyDir, mouse, '1.25', 'registered', '{}Channel'.format(channel), 'gridOverlay', side)
    if not os.path.exists(overlayFolder):
        print "Making directory {}".format(overlayFolder)
        os.makedirs(overlayFolder)
    overlayImagePath = os.path.join(overlayFolder, overlayImageName)
    return overlayImagePath
    
#print image_filename('b', 1, imageBaseName, localHistologyDir, mouse)
#print overlay_filename('b', 1, imageBaseName, localHistologyDir, mouse, 'right')

imgFile = image_filename('b', 33, imageBaseName, localHistologyDir, mouse)

ogrid = histologyanalysis.OverlayGrid(imgFile, nRows = 4, nCols = 3)
ogrid.set_grid()
    

def apply_to_stack(first, last):
    for i in range(first, last+1):

        for channel in ['b', 'g', 'r']:
            sliceName = image_filename(channel, i, imageBaseName, localHistologyDir, mouse)
            ogrid.apply_grid(sliceName)
            overlayFilename = overlay_filename(channel, i, imageBaseName, localHistologyDir, mouse, 'left')
            plt.savefig(overlayFilename, format = 'jpg')
        
        #plt.waitforbuttonpress()
        '''
