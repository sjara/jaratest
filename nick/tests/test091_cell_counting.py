import os
import numpy as np
import mahotas as mh
from matplotlib import pyplot as plt

regDir = '/home/nick/data/jarahubdata/jarashare/histology/anat037/registrationAC'
testFn = 'p1d5r.jpg'

im = mh.imread(os.path.join(regDir, testFn))

# thresh = mh.thresholding.otsu(im) #not strong enough
# thresh = mh.thresholding.rc(im) #even worse
# thresh = mh.thresholding.soft_threshold(im, 1) #Not sure how to make this one work
thresh = mh.thresholding.bernsen(im, radius=10, contrast_threshold=0)


plt.clf()
plt.imshow(im>thresh, cmap='bone')
plt.show()



