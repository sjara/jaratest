import matplotlib.pyplot as plt
from scipy import ndimage



histImagePV = ndimage.imread('/home/jarauser/data/figuresdata/2018acsup/appeal_figures/PV_expression.png')
histImageSOM = ndimage.imread('/home/jarauser/data/figuresdata/2018acsup/appeal_figures/SOM_expression.png')

imageBounds = [400, 900, 0, 500] #for band055
imageBounds2 = [430, 930, 0, 500] #for band004

plt.subplot(1,2,1)
plt.imshow(histImagePV[imageBounds[0]:imageBounds[1],imageBounds[2]:imageBounds[3],:])
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(histImageSOM[imageBounds2[0]:imageBounds2[1],imageBounds2[2]:imageBounds2[3],:])
plt.axis('off')

plt.show()