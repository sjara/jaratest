'''
Testing Inkscape-assisted manual image registration.

Steps:
1. Create an SVG file using code below.
2. Open the SVG file in Inkscape and manually register the images.
3. 

'''

import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from jaratoolbox import histologyanalysis as ha
reload(ha)

CREATE_SVG = 0

# -- Create SVG file with images --
if CREATE_SVG:
    filenameAtlas = '/var/tmp/examplesRegistration/atlas.jpg'
    filenameSlice = '/var/tmp/examplesRegistration/slice.jpg'
    filenameSVG = '/tmp/testfile.svg'
    (atlasSize, sliceSize) = ha.save_svg_for_registration(filenameSVG, filenameAtlas, filenameSlice)
    sys.exit()
        
# -- Transform coords --
filenameSVG = '/var/tmp/examplesRegistration/test03.svg'
(scale, translate, affine) = ha.get_svg_transform(filenameSVG)

filenameCSV = '/var/tmp/examplesRegistration/sliceCoords.csv'
coords = ha.get_coords_from_fiji_csv(filenameCSV)

newCoords = ha.apply_svg_transform(scale, translate, affine, coords)
print newCoords.T

filenameAtlas = '/var/tmp/examplesRegistration/atlas.jpg'
atlasIm = mpimg.imread(filenameAtlas)

plt.clf()
plt.imshow(atlasIm,cmap='gray')
plt.plot(newCoords[0,:],newCoords[1,:],'o',mec='r',mfc='none')
plt.axis('image')
plt.show()
