import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import decomposition


allcells = pd.read_hdf('/home/languo/data/ephys/switching_summary_stats/all_cells_all_measures_extra_mod_waveform_switching.h5',key='switching')

goodcells = allcells.loc[(allcells['cellQuality'].isin([1,6]))&(allcells['ISI']<=0.02)]

Na2K = abs(goodcells['peakNaAmp'] / goodcells['peakKAmp'])      
Cap2Na = abs(goodcells['peakCapAmp'] / goodcells['peakNaAmp'])
spkWidth = (goodcells['peakKTime'] - goodcells['peakNaTime']) #unit in sec

sigModSound = np.array(((goodcells['modSig']<=0.05)&(goodcells['modDir']>=1)),dtype=bool) 
sigModCenterout = np.array(((goodcells['modSig_-0.1-0s_center-out']<=0.05)&(goodcells['modDir_-0.1-0s_center-out']>=1)),dtype=bool)
soundResponsive = np.array((abs(goodcells['maxZSoundMid'])>=3),dtype=bool) 

dataToPlot = pd.DataFrame({'Na2K':Na2K,'spkWidth':1000*spkWidth,'Cap2Na':Cap2Na,'soundResponsive':soundResponsive,'sigModSound':sigModSound,'sigModCenterout':sigModCenterout})

# -- Run K-Means clustering on (spkWidth and Cap2Na) -- # 
##From previous plots can see using spkWidth and Cap2Na gives good separation of cells
#waveformParams = np.array(zip(spkWidth,Cap2Na,Na2K))
waveformParams = np.array(zip(spkWidth,Cap2Na))

pca = decomposition.PCA(n_components=3)
pca.fit(waveformParams)
X = pca.transform(waveformParams)
##################### NOT FINISHED ############################
#plt.scatter(X[:, 0], X[:, 1], X[:, 2], c=['r','b','g'])
plt.show()
'''
#fig, ax = plt.subplots()

for i in range(nClusters):
    # select only data observations with cluster label == i
    ds = dataToPlot.iloc[np.where(labelsEachGoodCell1==i)]
    # plot the data observations
    plt.plot(ds.spkWidth,ds.Cap2Na,'o')
    # plot the centroids
    lines = plt.plot(clusterMeans1[i,0],clusterMeans1[i,1],'kx')
    # make the centroid x's bigger
    plt.setp(lines,ms=15.0)
    plt.setp(lines,mew=2.0)
plt.show()
'''


'''
g = sns.FacetGrid(dataToPlot, hue='sigModSound', hue_kws={"marker": ["^", "v"], "color":['blue','red'], "s":[20,26]})
g.map(plt.scatter, 'spkWidth', 'Cap2Na', edgecolor='white',alpha=0.7)
#g.set(xscale='log',yscale='log')
g.set_ylabels('Capacitance peak to Na peak ratio (log scale)')
g.set_xlabels('spike width (time between Na&K peaks) ms (log scale)')
g.add_legend()

ax = plt.gca()


plt.figure()
ax = plt.gca()
for i, txt in enumerate(labelsEachGoodCell1):
    ax.annotate(str(txt), (dataToPlot.spkWidth.values[i],dataToPlot.Cap2Na.values[i]), fontsize=8, color='blue')

for i in range(0,nClusters):
    x,y,z = clusterMeans1[i]
    ax.annotate('clu'+str(i+1), (x,y), fontsize=15, color='blue')

plt.title('Random init centroid 20 times')


plt.figure()
ax = plt.gca()
for i, txt in enumerate(labelsEachGoodCell2):
    ax.annotate(str(txt), (dataToPlot.spkWidth.values[i],dataToPlot.Cap2Na.values[i]), fontsize=8, color='red')

for i in range(0,nClusters):
    x,y = clusterMeans2[i]
    ax.annotate('clu'+str(i+1), (x,y), fontsize=15, color='red')

plt.title('Manually selected centroids')
plt.show()
'''
