'''
Manual image registration

The idea is to open two images in inkscape, manually register them, and extract the transformation
'''

import sys
import xml.etree.ElementTree as etree
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# --- Create an SVG file ---

SVG_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   version="1.1"
   id="svg2"
   width="{atlasWidth}"
   height="{atlasHeight}"
   viewBox="0 0 {atlasWidth} {atlasHeight}">
  <image
     xlink:href="{atlasImage}"
     y="0"
     x="0"
     id="image0"
     style="image-rendering:optimizeQuality"
     preserveAspectRatio="none"
     width="456"
     height="320" />
  <image
     xlink:href="{sliceImage}"
     width="{sliceWidth}"
     height="{sliceHeight}"
     preserveAspectRatio="none"
     style="opacity:0.5;image-rendering:optimizeQuality"
     id="image1"
     x="0"
     y="0" />
</svg>
'''

def get_svg_transform(filename, imageSize=[1388,1040]):
    '''
    Get the transform of the second image from an SVG file with two images.

    Attribute 'transform' has format 'matrix(0.9,-0.1,0.3,0.9,0,0)'
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform
    '''
    tree = etree.parse(filename)
    root=tree.getroot()
    images = root.findall('{http://www.w3.org/2000/svg}image')
    if len(images)!=2:
        raise ValueError('The SVG file must contain exactly 2 images')
    if (images[0].attrib['x']!='0') or (images[0].attrib['y']!='0'):
        raise ValueError('The first image (CCF) must be located at (0,0).')
    if images[1].attrib.has_key('transform'):
        transformString = images[1].attrib['transform']
        if transformString.startswith('matrix'):
            transformValueStrings = re.findall(r'-?\d+\.*\d*', transformString)
            transformValues = [float(x) for x in transformValueStrings]
        elif transformString.startswith('rotate'):
            transformValueString = re.findall(r'-?\d+\.*\d*', transformString)[0]
            theta = -np.pi*float(transformValueString)/180 # In radians (and negative)
            # -- Note that this is different from the SVG documentation (b & c swapped) --
            transformValues = [np.cos(theta), -np.sin(theta), np.sin(theta), np.cos(theta)]
    else:
        transformValues = [1,0,0,1,0,0]
    scaleWidth = float(images[1].attrib['width'])/float(imageSize[0])
    scaleHeight = float(images[1].attrib['height'])/float(imageSize[1])
    xPos = float(images[1].attrib['x'])
    yPos = float(images[1].attrib['y'])
    scale = np.array([[scaleWidth],[scaleHeight]])
    translate = np.array([[xPos],[yPos]])
    affine = np.reshape(transformValues[:4],(2,2), order='F')
    return (scale, translate, affine)

def apply_svg_transform(scale, translate, affine, coords):
    '''Apply transformation in the appropriate order.'''
    newCoords = scale*coords + translate
    newCoords = np.dot(affine,newCoords)
    return newCoords

def get_cells_coords(filename):
    '''
    Read the location of cells from a CSV file created with Fiji.
    Returns coordinates as float in an array of shape (2,nCells)
    Note that values are in Image coordinates (inverted Y), not Cartesian.

    First row of CSV file is " ,Area,Mean,Min,Max,X,Y"
    '''
    allData = np.loadtxt(filenameCSV,delimiter=',',skiprows=1)
    coords = allData[:,5:]
    return coords.T

def save_svg_for_registration(filenameSVG, filenameAtlas, filenameSlice, verbose=True):
    '''Save SVG for manual registration'''
    import PIL
    atlasIm = PIL.Image.open(filenameAtlas)
    (atlasWidth,atlasHeight) = atlasIm.size
    sliceIm = PIL.Image.open(filenameSlice)
    (sliceWidth,sliceHeight) = sliceIm.size
    svgString = SVG_TEMPLATE.format(atlasImage=filenameAtlas, sliceImage=filenameSlice,
                                    atlasWidth=atlasWidth, atlasHeight=atlasHeight,
                                    sliceWidth=sliceWidth, sliceHeight=sliceHeight)
    fileSVG = open(filenameSVG, 'w')
    fileSVG.write(svgString)
    fileSVG.close()
    if verbose:
        print('Saved {}'.format(filenameSVG))
    return (atlasIm.size, sliceIm.size)
    

if __name__=='__main__':
    CASE = 5

    if CASE==0:
        # --- Find transform in SVG file ---
        filenameSVG = '/var/tmp/examplesRegistration/test03.svg'
        tt = get_transform(filenameSVG)
        print tt
    elif CASE==1:
        # --- Create SVG from template ---
        pass
    elif CASE==2:
        # --- Read coords from CSV cell count file ---
        filenameCSV = '/var/tmp/examplesRegistration/sliceCoords.csv'
        coords = get_cell_coords(filenameCSV)
        print coords
    elif CASE==3:
        # -- Transform coords --
        filenameSVG = '/var/tmp/examplesRegistration/test03.svg'
        (scale, translate, affine) = get_svg_transform(filenameSVG)
        filenameCSV = '/var/tmp/examplesRegistration/sliceCoords.csv'
        coords = get_cells_coords(filenameCSV)
        newCoords = apply_svg_transform(scale, translate, affine, coords)
        print newCoords.T
        filenameAtlas = '/var/tmp/examplesRegistration/atlas.jpg'
        atlasIm = mpimg.imread(filenameAtlas)
        plt.clf()
        plt.imshow(atlasIm,cmap='gray')
        plt.plot(newCoords[0,:],newCoords[1,:],'o',mec='r',mfc='none')
        plt.axis('image')
        plt.show()
    elif CASE==4:
        # -- Create SVG file --
        atlasImage = '/var/tmp/examplesRegistration/atlas.jpg'
        sliceImage = '/var/tmp/examplesRegistration/slice.jpg'
        atlasWidth = 456
        atlasHeight = 320
        sliceWidth = 1388
        sliceHeight = 1040
        svgString = SVG_TEMPLATE.format(atlasImage=atlasImage, sliceImage=sliceImage,
                                        atlasWidth=atlasWidth, atlasHeight=atlasHeight,
                                        sliceWidth=sliceWidth, sliceHeight=sliceHeight)
        print svgString
    elif CASE==5:
        atlasImage = '/var/tmp/examplesRegistration/atlas.jpg'
        sliceImage = '/var/tmp/examplesRegistration/slice.jpg'
        filenameSVG = '/tmp/testfile.svg'
        (atlasSize, sliceSize) = save_svg_for_registration(filenameSVG, atlasImage, sliceImage)
    
        '''        
    elif CASE==99:
        # -- Transform coords --
        filenameSVG = '/var/tmp/examplesRegistration/test03.svg'
        #transform = get_transform(filenameSVG)

        filename = '/var/tmp/examplesRegistration/test03.svg'
        imageSize=[1388,1040]
        tree = etree.parse(filename)
        root=tree.getroot()
        images = root.findall('{http://www.w3.org/2000/svg}image')
        if len(images)!=2:
            raise ValueError('The SVG file must contain exactly 2 images')
        if (images[0].attrib['x']!='0') or (images[0].attrib['y']!='0'):
            raise ValueError('The first image (CCF) must be located at (0,0).')

        if images[1].attrib.has_key('transform'):
            transformString = images[1].attrib['transform']
            if transformString.startswith('matrix'):
                transformValueStrings = re.findall(r'-?\d+\.*\d*', transformString)
                transformValues = [float(x) for x in transformValueStrings]
            elif transformString.startswith('rotate'):
                transformValueString = re.findall(r'-?\d+\.*\d*', transformString)[0]
                theta = -np.pi*float(transformValueString)/180 # In radians (and negative)
                #transformValues = [np.cos(theta), np.sin(theta), -np.sin(theta), np.cos(theta)]
                transformValues = [np.cos(theta), -np.sin(theta), np.sin(theta), np.cos(theta)]
        else:
            transformValues = [1,0,0,1,0,0]
        scaleWidth = float(images[1].attrib['width'])/float(imageSize[0])
        scaleHeight = float(images[1].attrib['height'])/float(imageSize[1])
        xPos = float(images[1].attrib['x'])
        yPos = float(images[1].attrib['y'])
        #scaleMat = np.array([[scaleWidth,0],[0,scaleHeight]])
        scale = np.array([[scaleWidth],[scaleHeight]])
        #translate = np.array([[xPos],[yPos]])
        affine = np.reshape(transformValues[:4],(2,2)).T
        translate = np.dot(affine, np.array([[xPos],[yPos]]))
        #translate = np.dot(affine-affine*np.eye(2), np.array([[xPos],[yPos]]))
        #translate = np.dot(np.linalg.inv(affine), np.array([[xPos],[yPos]]))
        #transformValues[4] = float(images[1].attrib['x'])
        #transformValues[5] = float(images[1].attrib['y'])
        #transformMatrix = np.reshape(transformValues,(3,2)).T
        #transformMatrix[:2,:2] = np.dot(scaleMat,transformMatrix[:2,:2])
        #transformMatrix[:2,:2] = scaleFactors * transformMatrix[:2,:2]
        #transform = transformMatrix
        
        #transformInvY = transform.copy()
        #transformInvY[1,2] = -transformInvY[1,2]
        filenameCSV = '/var/tmp/examplesRegistration/sliceCoords.csv'
        coords = get_cells_coords(filenameCSV)
        #coordsPlus = np.vstack((coords.T, np.ones(coords.shape[0])))
        #newCoords = np.dot(transformInvY,coordsPlus)
        #newCoords = np.dot(transform,coordsPlus)

        #newCoords = scale*coords.T
        #newCoords = np.dot(affine,newCoords) + translate
        newCoords = scale*coords.T + np.array([[xPos],[yPos]])
        newCoords = np.dot(affine,newCoords)

        print newCoords.T

        filenameAtlas = '/var/tmp/examplesRegistration/atlas.jpg'
        atlasIm = mpimg.imread(filenameAtlas)
        plt.clf()
        plt.imshow(atlasIm,cmap='gray')
        plt.plot(newCoords[0,:],newCoords[1,:],'o',mec='r',mfc='none')
        plt.axis('image')
        #plt.axis((315.1639, 455.3235, 213.3130, 114.9553))
        plt.show()
'''
