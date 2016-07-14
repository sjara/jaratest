import os
import csv
from pandas.io.parsers import read_csv
import numpy as np
import itertools
import matplotlib.pyplot as plt
from sklearn.metrics import jaccard_similarity_score
from sklearn import manifold

basePath = '/home/nick/Programming/jaratoolbox/test/nick/histology/'

anat030_str = read_csv(os.path.join(basePath, 'Anat030_str_red_left.csv'), header=None)
anat030_mgn = read_csv(os.path.join(basePath, 'Anat030_mgn_red_left.csv'), header=None)
anat024_str = read_csv(os.path.join(basePath, 'Anat024_str_red_left.csv'), header=None)
anat024_mgn = read_csv(os.path.join(basePath, 'Anat024_mgn_red_left.csv'), header=None)


anat030_str = np.reshape(np.array(anat030_str), [16, 3, 3])
anat024_str = np.reshape(np.array(anat024_str), [16, 3, 3])
print "FIXME: Hardcoded array shapes"

mouse_strs = [anat030_str, anat024_str]

anat030_mgn = np.reshape(np.array(anat030_mgn), [13, 3, 3])
anat024_mgn = np.reshape(np.array(anat024_mgn), [13, 3, 3])

mouse_mgns = [anat030_mgn, anat024_mgn]


results_by_thal_vox = []
results_array = np.zeros((13, 3, 3, 16, 3, 3), dtype=bool)

ravel_array_shape = (len(anat030_mgn.ravel()), len(anat030_str.ravel()))
init_ravel_array = np.zeros(ravel_array_shape)

results_rav_array = init_ravel_array.copy()

for voxelNumber, voxelInd in enumerate(itertools.product(*map(xrange, np.shape(mouse_mgns[0])))): #Iterate through the thalamus voxels
    positives = np.zeros((16, 3, 3), dtype = bool)
    negatives = np.zeros((16, 3, 3), dtype = bool) #Init arrays to hold pos and neg. data
    for indmouse, mgn in enumerate( mouse_mgns ): #Iterate through the mgn data
        if mgn[voxelInd]>0: #Positive injection
            positives = positives + (mouse_strs[indmouse]>0) #adding boolean arrays
        elif mgn[voxelInd]==0: #Negative Injection
            negatives = negatives + (mouse_strs[indmouse]>0)

    all_mouse_results = positives * np.logical_not(negatives) #take pos. list, flip to false any that are true in the negative list

    all_mouse_ravel = all_mouse_results.ravel()

    results_rav_array[voxelNumber, :] = all_mouse_ravel
    results_by_thal_vox.append(all_mouse_results)
    results_array[voxelInd[0], voxelInd[1], voxelInd[2], :, :, :] = all_mouse_results


mgn_shape = np.shape(anat030_mgn)
mgn_rav_len = len(np.zeros(mgn_shape).ravel())
mgn_coord_array = np.reshape(np.array(range(mgn_rav_len)), mgn_shape)

#Coordinates for different 'ravelings' - to use, ravel normally (A-P) and then slice with these.
mgn_ap_ravel = mgn_coord_array.ravel()
mgn_ap_str_ap_heatmap = init_ravel_array.copy()
heatmap_by_cluster = init_ravel_array.copy()

#AP mgn, AP str Actually, P-A
for indRavelMgn in mgn_ap_ravel:
    str_this_mgn = results_by_thal_vox[indRavelMgn]
    mgn_ap_str_ap_heatmap[indRavelMgn, :] = str_this_mgn.ravel()


###Sorting the raveled results using DBSCAN
#from sklearn.metrics.pairwise import euclidean_distances
#from sklearn.cluster import DBSCAN
#
#D = euclidean_distances(results_rav_array)
#
#db = DBSCAN(metric = 'precomputed').fit(D)
#
##The cluster labels
#unique_labels = np.unique(db.labels_)
#
#sorted_rav_array = init_ravel_array.copy()
#count = 0
#for label in unique_labels:
    #indsThisLabel = np.flatnonzero(db.labels_ == label)
    #for ind in indsThisLabel:
        #striatum = results_rav_array[ind]
        #sorted_rav_array[count, :] = striatum
        #count += 1
       #
#plt.imshow(sorted_rav_array, cmap = 'Blues')
#plt.xlabel('All Possible Striatum Voxels')
#plt.ylabel('All Possible Thalamus Voxels')
#plt.show()
###

##Code to plot projections of the voxels - not working yet

#holder01 = np.zeros((13, 3, 3))
#indsThisLabel = np.flatnonzero(db.labels_ == -1)
#for ind in indsThisLabel:
    #position = np.unravel_index(ind, (13, 3, 3))
    #print position
    #holder[position] = 1
#
#holder0 = np.zeros((13, 3, 3))
#indsThisLabel = np.flatnonzero(db.labels_ == 0)
#for ind in indsThisLabel:
    #position = np.unravel_index(ind, (13, 3, 3))
    #print position
    #holder[position] = 1
       #
#holder1 = np.zeros((13, 3, 3))
#indsThisLabel = np.flatnonzero(db.labels_ == 1)
#for ind in indsThisLabel:
    #position = np.unravel_index(ind, (13, 3, 3))
    #print position
    #holder[position] = 1
#
#holder2 = np.zeros((13, 3, 3))
#indsThisLabel = np.flatnonzero(db.labels_ == 2)
#for ind in indsThisLabel:
    #position = np.unravel_index(ind, (13, 3, 3))
    #print position
    #holder[position] = 1
   #
#
#subplot2grid(


 #Testing code, not producing very interpretable results yet.

# ravel_array_shape = (len(anat030_mgn.ravel()), len(anat030_str.ravel()))

# mgn_shape = np.shape(anat030_mgn)

# mgn_rav_len = len(np.zeros(mgn_shape).ravel())
# mgn_coord_array = np.reshape(np.array(range(mgn_rav_len)), mgn_shape)

# #Coordinates for different 'ravelings' - to use, ravel normally (A-P) and then slice with these.
# mgn_ap_ravel = mgn_coord_array.ravel()
# mgn_dv_ravel = np.swapaxes(mgn_coord_array, 0, 1).ravel()
# mgn_ml_ravel = np.swapaxes(mgn_coord_array, 0, 2).ravel()

# init_ravel_array = np.zeros(ravel_array_shape)
# #Initialize 9 arrays to hold the raveled data

# mgn_ap_str_ap_heatmap = init_ravel_array.copy()
# mgn_ap_str_dv_heatmap = init_ravel_array.copy()
# mgn_ap_str_ml_heatmap = init_ravel_array.copy()

# mgn_dv_str_ap_heatmap = init_ravel_array.copy()
# mgn_dv_str_dv_heatmap = init_ravel_array.copy()
# mgn_dv_str_ml_heatmap = init_ravel_array.copy()

# mgn_ml_str_ap_heatmap = init_ravel_array.copy()
# mgn_ml_str_dv_heatmap = init_ravel_array.copy()
# mgn_ml_str_ml_heatmap = init_ravel_array.copy()

# #AP mgn, AP str Actually, P-A
# for indEnum, indRavelMgn in enumerate(mgn_ap_ravel):
#     str_this_mgn = results_by_thal_vox[indRavelMgn]
#     mgn_ap_str_ap_heatmap[indEnum, :] = str_this_mgn.ravel()


# #AP mgn, dv str Actually, P-A
# count = 0
# for indEnum, indRavelMgn in enumerate(mgn_ap_ravel):
#     str_this_mgn = results_by_thal_vox[indRavelMgn]
#     mgn_ap_str_dv_heatmap[indEnum, :] = np.swapaxes(str_this_mgn, 0, 1).ravel()


# #AP mgn, ml str Actually, P-A
# for indEnum, indRavelMgn in enumerate(mgn_ap_ravel):
#     str_this_mgn = results_by_thal_vox[indRavelMgn]
#     mgn_ap_str_ml_heatmap[indEnum, :] = np.swapaxes(str_this_mgn, 0, 2).ravel()

# #DV MGN, PA STR
# for indEnum, indRavelMgn in enumerate(mgn_dv_ravel):
#     str_this_mgn = results_by_thal_vox[indRavelMgn]
#     mgn_dv_str_ap_heatmap[indEnum, :] = str_this_mgn.ravel()


# #DV MGN, DV Str
# for indEnum, indRavelMgn in enumerate(mgn_dv_ravel):
#     str_this_mgn = results_by_thal_vox[indRavelMgn]
#     mgn_dv_str_dv_heatmap[indEnum, :] = np.swapaxes(str_this_mgn, 0, 1).ravel()


# #DV MGN, ML Str
# for indEnum, indRavelMgn in enumerate(mgn_dv_ravel):
#     str_this_mgn = results_by_thal_vox[indRavelMgn]
#     mgn_dv_str_ml_heatmap[indEnum, :] = np.swapaxes(str_this_mgn, 0, 2).ravel()

# #ML MGN, PA STR
# for indEnum, indRavelMgn in enumerate(mgn_ml_ravel):
#     str_this_mgn = results_by_thal_vox[indRavelMgn]
#     mgn_ml_str_ap_heatmap[indEnum, :] = str_this_mgn.ravel()


# #ML mgn, DV Str
# for indEnum, indRavelMgn in enumerate(mgn_ml_ravel):
#     str_this_mgn = results_by_thal_vox[indRavelMgn]
#     mgn_ml_str_dv_heatmap[indEnum, :] = np.swapaxes(str_this_mgn, 0, 1).ravel()


# #ML MGN, Ml STR
# for indEnum, indRavelMgn in enumerate(mgn_ml_ravel):
#     str_this_mgn = results_by_thal_vox[indRavelMgn]
#     mgn_ml_str_ml_heatmap[indEnum, :] = np.swapaxes(str_this_mgn, 0, 2).ravel()




# plt.subplot(3, 3, 1)
# plt.imshow(mgn_ap_str_ap_heatmap, cmap = "Blues")
# plt.ylabel("Thalamus, AP")
# plt.xlabel("Striatum, AP")

# plt.subplot(3, 3, 2)
# plt.imshow(mgn_ap_str_dv_heatmap, cmap = "Blues")
# plt.ylabel("Thalamus, AP")
# plt.xlabel("Striatum, DV")

# plt.subplot(3, 3, 3)
# plt.imshow(mgn_ap_str_ml_heatmap, cmap = "Blues")
# plt.ylabel("Thalamus, AP")
# plt.xlabel("Striatum, ML")



# plt.subplot(3, 3, 4)
# plt.imshow(mgn_dv_str_ap_heatmap, cmap = "Blues")
# plt.ylabel("Thalamus, DV")
# plt.xlabel("Striatum, AP")

# plt.subplot(3, 3, 5)
# plt.imshow(mgn_dv_str_dv_heatmap, cmap = "Blues")
# plt.ylabel("Thalamus, DV")
# plt.xlabel("Striatum, DV")

# plt.subplot(3, 3, 6)
# plt.imshow(mgn_dv_str_ml_heatmap, cmap = "Blues")
# plt.ylabel("Thalamus, DV")
# plt.xlabel("Striatum, ML")



# plt.subplot(3, 3, 7)
# plt.imshow(mgn_ml_str_ap_heatmap, cmap = "Blues")
# plt.ylabel("Thalamus, ML")
# plt.xlabel("Striatum, AP")

# plt.subplot(3, 3, 8)
# plt.imshow(mgn_ml_str_dv_heatmap, cmap = "Blues")
# plt.ylabel("Thalamus, ML")
# plt.xlabel("Striatum, DV")

# plt.subplot(3, 3, 9)
# plt.imshow(mgn_ml_str_ml_heatmap, cmap = "Blues")
# plt.ylabel("Thalamus, ML")
# plt.xlabel("Striatum, ML")

# plt.show()

###Manifold stuff
#import sklearn
#from sklearn import neighbors

#dice_sim = neighbors.DistanceMetric.get_metric('dice')
#
#similarities = dice_sim.pairwise(str_ap_heatmap)

#similarities = sklearn.metrics.pairwise.euclidean_distances(str_ap_heatmap)
#similarities = sklearn.metrics.pairwise.pairwise_distances(str_ap_heatmap, metric='cosine')
#
#seed = np.random.RandomState(seed=3)
#mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                   #dissimilarity="precomputed", n_jobs=1)
#
#pos = mds.fit(similarities).embedding_



##Testing
test_shape = (5, 4, 3)          # 5 slices, 4 D-V boxes, 3 M-L boxes


rav_len = len(np.zeros(test_shape).ravel())

test_array = np.reshape(np.array(range(rav_len)), test_shape)

ap_ravel = test_array.ravel()

dv_ravel = np.swapaxes(test_array, 0, 1).ravel()

ml_ravel = np.swapaxes(test_array, 0, 2).ravel()





###If we make an array from reshape(range())..., then we can swapaxes it and ravel it
#and we will have the indices to re-create that transform with (by raveling the data
#and slicing by the raveled indices.


#thal_test_coords = [[2, 1, 1]]
##anat030 is positive at this location, anat024 is negative
#
#pos_array = np.ones((16, 3,3))
#neg_array = np.ones((16, 3,3))*-1
#
#anat030_filter = anat030_str>0
#anat024_filter = anat024_str>0
##pos_times_injection_anat030 = pos_array*anat030_filter
##neg_times_injection_anat024 = neg_array*anat024_filter
##pos_but_not_neg = pos_times_injection_anat030+neg_times_injection_anat024
##pos_but_not_neg = np.ones((16, 3, 3))import os
