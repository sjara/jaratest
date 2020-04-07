"""
Calulcate number of clusters by D1 vs nD1, by brain region filters, by tuning filters, etc
"""
import pandas as pd
import numpy as np
from jaratoolbox import celldatabase
import studyparams

db = celldatabase.load_hdf("/var/tmp/figuresdata/2019astrpi/ttDBR2.h5")

#%% Calculations of how many clusters there are just sorting by brain region and z-coordinate
brainAreaDB = db.query("recordingSiteName == 'Caudoputamen'")
brainAreaDB = brainAreaDB.query("z_coord <= 301")
nullDB = db.query("recordingSiteName == ''")
brainAreaDB = pd.concat([brainAreaDB, nullDB], axis=0, ignore_index=True, sort=False)

print("Number of clusters that are in striatum or were not able to be located is {}".format(brainAreaDB.__len__()))

#%% Separating into D1 and nD1
nD1DB = brainAreaDB.query(studyparams.nD1_CELLS)
D1DB = brainAreaDB.query(studyparams.D1_CELLS)

# Assuming that all infinities that come up are from miscalculations, so changing them to NaNs so they can be excluded later
D1DB.rsquaredFit.replace([np.inf, -np.inf], np.nan, inplace=True)
nD1DB.rsquaredFit.replace([np.inf, -np.inf], np.nan, inplace=True)
D1Clusters = D1DB.__len__()
nD1Clusters = nD1DB.__len__()
print("D1 clusters = {0}\nnD1 clusters = {1}".format(D1Clusters, nD1Clusters))

#%% Tuning seperation
# Removing the NaNs
D1DBTuned = D1DB[D1DB.rsquaredFit.notnull()]
nD1DBTuned = nD1DB[nD1DB.rsquaredFit.notnull()]
D1ClustersTuned = D1DBTuned.__len__()
nD1ClustersTuned = nD1DBTuned.__len__()
print("D1 total R2 = {0}\nnD1 total R2 = {1}".format(D1ClustersTuned, nD1ClustersTuned))
# Now filtering to R2 > 0.03
D1DBTuned = D1DBTuned.query(studyparams.TUNING_FILTER)
nD1DBTuned = nD1DBTuned.query(studyparams.TUNING_FILTER)
D1ClustersTuned = D1DBTuned.__len__()
nD1ClustersTuned = nD1DBTuned.__len__()
print("D1 filtered R2 = {0}\nnD1 filtered R2 = {1}".format(D1ClustersTuned, nD1ClustersTuned))

#%% Sound responsive in any capacity
D1DBResponse = D1DB.query("(noiseburst_pVal < 0.05 or tuning_pVal < 0.05 or am_response_pVal < 0.05 or tuningTest_pVal < 0.05)")
nD1DBResponse = nD1DB.query("(noiseburst_pVal < 0.05 or tuning_pVal < 0.05 or am_response_pVal < 0.05 or tuningTest_pVal < 0.05)")  # Adding in the tuningTest gave 50 cells to D1 and 200 cells to nD1
D1ResponseClusters = D1DBResponse.__len__()
nD1ResponseClusters = nD1DBResponse.__len__()
print("D1 sound responsive clusters = {0}\nnD1 sound responsive clusters = {1}".format(D1ResponseClusters, nD1ResponseClusters))

# TODO Change to using the DB with tuningTest data and then also add that in as a possible pass for sound repsonse
