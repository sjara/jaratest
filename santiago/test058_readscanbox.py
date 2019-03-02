'''
Read scanbox data.
'''

from jaratoolbox import loadscanbox
reload(loadscanbox)
from matplotlib import pyplot as plt

filename = '/data/exampleNeurolabware/G6H73LTRN_001_001.sbx'

data = loadscanbox.sbxread(filename)

maxdata = data.max(axis=3)[0,:,:]
plt.imshow(maxdata)
plt.show()
