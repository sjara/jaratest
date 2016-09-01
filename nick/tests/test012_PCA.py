
from jaratoolbox import loadopenephys
import os
import numpy as np
from pylab import *
from matplotlib.mlab import PCA
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, MiniBatchKMeans

spike_filename = '/home/nick/data/ephys/hm4d002/cno_08-14/2014-08-14_12-45-30/Tetrode3.spikes'

spikes = loadopenephys.DataSpikes(spike_filename)

ch0 = spikes.samples[:,0]

results = PCA(ch0)

#kmeanshift=MeanShift()
X=results.Y[:,0:1]
x=results.Y[:,0]
y=results.Y[:,1]
X=zeros((len(x), 2))

mbk=MiniBatchKMeans(n_clusters=2)
fit = mbk.fit_predict(X)
cluster0=(fit==0)
cluster1=(fit==1)


# -- Plotting PC 0 and 1
ax2 = plt.subplot2grid((2,3), (0, 0), colspan=2, rowspan=2)
ax2.plot(results.Y[:,0][cluster0], results.Y[:,1][cluster0], 'b.', ms=1)
ax2.plot(results.Y[:,0][cluster1], results.Y[:,1][cluster1], 'r.', ms=1)

ax3 = plt.subplot2grid((2,3), (0,2), colspan=1, rowspan=1)
ax3.plot(results.Wt[0])

ax4 = plt.subplot2grid((2,3), (1,2), colspan=1, rowspan=1)
ax4.plot(results.Wt[1])

plt.show()


cluster0=(dbpred==-1.0)
cluster1=(dbpred==1.0)

