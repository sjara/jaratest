
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from jaratoolbox import histologyanalysis
reload(histologyanalysis)

imagesToAnalyze = ['/data/brainmix_data/test043_TL/p1-D1-01b.jpg',
                   '/data/brainmix_data/test043_TL/p1-D2-01b.jpg',
                   '/data/brainmix_data/test043_TL/p1-D3-01b.jpg']

nRows,nCols = (3,2)
ogrid = histologyanalysis.OverlayGrid(nRows=nRows, nCols=nCols)
ogrid.set_grid([(1080,106),(1340,450)])
#ogrid.set_grid([(500,400),(800,1000)])

#ogrid.enter_grid(imagesToAnalyze[0])
#ogrid.apply_grid(imagesToAnalyze[1])

plt.clf()
#ogrid.apply_grid(imagesToAnalyze[1])
if 0:
    image = mpimg.imread(imagesToAnalyze[1])[:,:,0]
    measured = ogrid.quantify(image)
    print measured
else:
    print 'Loading ...'
    stack = ogrid.load_stack(imagesToAnalyze)
    print 'Quantifying ...'
    measuredStack = ogrid.quantify_stack(stack)
    print measuredStack

ogrid.apply_to_stack(imagesToAnalyze)
plt.show()

'''
xvals,yvals = ogrid.coords
imShape = ogrid.image.shape[0:2]
maskList = []
for indr in range(nRows):
    rowCoords = yvals[indr:indr+2].astype(int)
    print rowCoords
    for indc in range(nCols):
        colCoords = xvals[indc:indc+2].astype(int)
        print colCoords
        mask = np.zeros(imShape,dtype=bool)
        mask[rowCoords[0]:rowCoords[1], colCoords[0]:colCoords[1]] = True
        maskList.append(mask)

#plt.title('{0},{1}'.format(indr,indc))

for indmask,mask in enumerate(maskList):
    newImage = ogrid.image.copy()
    newImage[~mask] = 0
    plt.imshow(newImage)
    plt.title(indmask)
    plt.waitforbuttonpress()


image = mpimg.imread(imagesToAnalyze[1])[:,:,0]
#measured = np.empty((nRows,nCols))
meanIntensity = []
for indmask,mask in enumerate(maskList):
    oneMeanIntensity = np.mean(image[mask])
    meanIntensity.append(oneMeanIntensity)
measured = np.reshape(meanIntensity,(nRows,nCols))

'''

'''
[[ 188.93562753  173.84048583]
 [ 152.5651505   175.47270903]
 [  80.32280936  157.35779264]]
'''
