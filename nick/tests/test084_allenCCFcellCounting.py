'''Transform coordinates from CSV cell count file to Allen CCF.'''
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from jaratoolbox import histologyanalysis as ha

filenameSVG = '/mnt/jarahubdata/jarashare/histology/anat038/registrationAC/p1d1.svg'
(scale, translate, affine) = ha.get_svg_transform(filenameSVG, sliceSize=[1388, 1040])

filenameCSV = '/mnt/jarahubdata/jarashare/histology/anat038/registrationAC/p1d1.csv'
coords = ha.get_coords_from_fiji_csv(filenameCSV, pixelSize=4.0048)

newCoords = ha.apply_svg_transform(scale, translate, affine, coords)
print newCoords.T

filenameAtlas = '/mnt/jarahubdata/atlas/AllenCCF_25/JPEG/allenCCF_Z193.jpg'
atlasIm = mpimg.imread(filenameAtlas)

annotationVolume = ha.AllenAnnotation()
structIDs = annotationVolume.get_structure_id_many_xy(newCoords, 193)
names = [annotationVolume.get_structure_from_id(thisID) for thisID in structIDs]

areaColors = {'Primary auditory area, layer 1':'r', 'Primary auditory area, layer 2/3':'g' , 'Primary auditory area, layer 4':'b', 'Primary auditory area, layer 5':'m', 'Primary aud itory area, layer 6a':'c', 'Primary auditory area, layer 6b':'y'}

plt.clf()
plt.imshow(atlasIm, cmap='gray')
plt.hold(True)
for area, color in areaColors.iteritems():
    areaInds = [ind for ind, name in enumerate(names) if name==area]
    pointsThisArea = newCoords[:,areaInds]
    plt.plot(pointsThisArea[0,:], pointsThisArea[1,:], 'o', color=color)
plt.show()
