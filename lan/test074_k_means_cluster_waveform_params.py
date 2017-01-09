import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


allcells = pd.read_hdf('/home/languo/data/ephys/switching_summary_stats/all_cells_all_measures_extra_mod_waveform_switching.h5',key='switching')

goodcells = allcells.loc[(allcells['cellQuality'].isin([1,6]))&(allcells['ISI']<=0.02)]

Na2K = abs(goodcells['peakNaAmp'] / goodcells['peakKAmp'])      
Cap2Na = np.array(abs(goodcells['peakCapAmp'] / goodcells['peakNaAmp']),dtype=float)
Cap2Na = np.log10(Cap2Na)
spkWidth = np.array(1000*(goodcells['peakKTime'] - goodcells['peakNaTime']),dtype=float) #unit in sec
spkWidth = np.log10(spkWidth)

sigModSound = np.array(((goodcells['modSig']<=0.05)&(goodcells['modDir']>=1)),dtype=bool) 
sigModCenterout = np.array(((goodcells['modSig_-0.1-0s_center-out']<=0.05)&(goodcells['modDir_-0.1-0s_center-out']>=1)),dtype=bool)
soundResponsive = np.array((abs(goodcells['maxZSoundMid'])>=3),dtype=bool) 

dataToPlot = pd.DataFrame({'Na2K':Na2K,'spkWidth':spkWidth,'Cap2Na':Cap2Na,'soundResponsive':soundResponsive,'sigModSound':sigModSound,'sigModCenterout':sigModCenterout})

# -- Run K-Means clustering on (spkWidth and Cap2Na) -- # 
##From previous plots can see using spkWidth and Cap2Na gives good separation of cells
#waveformParams = np.array(zip(spkWidth,Cap2Na,Na2K))
waveformParamsPre = np.array(zip(spkWidth,Cap2Na)) #Tried using original and log 10 scaled data

waveformParams = (waveformParamsPre-np.mean(waveformParamsPre,axis=0))/np.std(waveformParamsPre,axis=0) 
#waveformParams = waveformParams*np.array([1,2])

nClusters = 2
kmeans1 = KMeans(n_clusters=nClusters,n_init=20).fit(waveformParams) #kmeans using randomly initiated centroids, run 20 random selections

#centroids = np.array([[0.14,0.25],[0.85,1.12],[0.53,0.02]], np.float64)
#kmeans2 = KMeans(n_clusters=nClusters, init=centroids, n_init=1).fit(waveformParams)

labelsEachCell = np.chararray(waveformParams.shape[0], itemsize=7)
labels = kmeans1.labels_  #Each cell gets a label saying which cluster it belongs to
#labelsEachGoodCell2 = kmeans2.labels_

clusterMeans = kmeans1.cluster_centers_
#clusterMeanSortedCap2Na = list(clusterMeans).sort(key=lambda mean: mean[1])
clusterMeansCap2Na = clusterMeans[:,1]

order = np.argsort(clusterMeansCap2Na)
# Manually generate labels for cells that are interpretable, right now this is hard coded!!
labelsEachCell[labels==order[0]]='sCap2Na'
labelsEachCell[labels==order[1]]='mCap2Na'
#labelsEachCell[labels==order[2]]='lCap2Na'
#labelsEachCell[labels==order[3]]='another'
#clusterMeans2 = kmeans2.cluster_centers_
clusterMeanSortedCap2Na = clusterMeans[order]

# Store clustering results in df
goodcells['labels'] = labelsEachCell
goodcells.to_hdf('/home/languo/data/ephys/switching_summary_stats/good_cells_all_measures_extra_mod_waveform_switching.h5',key='switching')

#fig, ax = plt.subplots()

plt.clf()
#for ind,i in enumerate(['sCap2Na','mCap2Na','lCap2Na','another']):
for ind,i in enumerate(['sCap2Na','mCap2Na']):
    # select only data observations with cluster label == i
    ds = dataToPlot.iloc[np.where(labelsEachCell==i)]
    # plot the data observations
    #plt.plot(ds.spkWidth,ds.Cap2Na,'o')
    plt.plot(waveformParams[:,0][labels==ind],waveformParams[:,1][labels==ind],'o')
    
    # plot the centroids
    lines = plt.plot(clusterMeanSortedCap2Na[ind,0],clusterMeanSortedCap2Na[ind,1],'kx')
    plt.annotate(i, (clusterMeanSortedCap2Na[ind,0],clusterMeanSortedCap2Na[ind,1]), color='m', fontsize=20)
    # make the centroid x's bigger
    plt.setp(lines,ms=15.0)
    plt.setp(lines,mew=2.0)

    #plt.gca.set_yscale('log')
    #plt.gca.set_xscale('log')
#plt.axis('equal')
plt.show()



'''
g = sns.FacetGrid(dataToPlot, hue='sigModSound', hue_kws={"marker": ["^", "v"], "color":['blue','red'], "s":[20,26]})
g.map(plt.scatter, 'spkWidth', 'Cap2Na', edgecolor='white',alpha=0.7)
#g.set(xscale='log',yscale='log')
g.set_ylabels('Capacitance peak to Na peak ratio (log scale)')
g.set_xlabels('spike width (time between Na&K peaks) ms (log scale)')
g.add_legend()
plt.show()
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

numCellsC1 = len(goodcells[(goodcells.labels=='sCap2Na')])
soundResC1 = len(goodcells[(goodcells.labels=='sCap2Na')&(abs(goodcells.maxZSoundMid)>3)])
percentSoundResC1 = float(soundResC1)/numCellsC1
numModC1 = len(goodcells[(goodcells.labels=='sCap2Na')&(goodcells.modSig<=0.05)&(goodcells.modDir>=1)&(abs(goodcells.maxZSoundMid)>3)])
percentModC1 = float(numModC1)/soundResC1

numCellsC2 = len(goodcells[(goodcells.labels=='mCap2Na')])
soundResC2 = len(goodcells[(goodcells.labels=='mCap2Na')&(abs(goodcells.maxZSoundMid)>3)])
percentSoundResC2 = float(soundResC2)/numCellsC2
numModC2 = len(goodcells[(goodcells.labels=='mCap2Na')&(goodcells.modSig<=0.05)&(goodcells.modDir>=1)&(abs(goodcells.maxZSoundMid)>3)])
percentModC2 = float(numModC2)/soundResC2

print 'Sound resp: {0:.1%}, {1:.1%}'.format(percentSoundResC1, percentSoundResC2)
print 'Sound resp (Mod): {0:.1%}, {1:.1%}'.format(percentModC1, percentModC2) 
