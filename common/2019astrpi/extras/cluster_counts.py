"""
Calulcate number of clusters by D1 vs nD1, by brain region filters, by
tuning filters, etc. Needs a database that has calculations for tuningTest
paradigms stored (from extras/tuning_test_comparisons.py)
"""
import sys
sys.path.append('..')  # Added to allow import of studyparams using a relative import
import pandas as pd
import numpy as np
from jaratoolbox import celldatabase
import studyparams

db = celldatabase.load_hdf('/var/tmp/figuresdata/2019astrpi/ttDBR2.h5')
db = db.query(studyparams.FIRST_FLTRD_CELLS)

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
D1DBPure = D1DB[D1DB.rsquaredFit.notnull()]
nD1DBPure = nD1DB[nD1DB.rsquaredFit.notnull()]
D1ClustersResponsive = D1DBPure.__len__()
nD1ClustersResponsive = nD1DBPure.__len__()
print("D1 total R2 = {0}\nnD1 total R2 = {1}".format(D1ClustersResponsive, nD1ClustersResponsive))
# Now filtering to R2 > 0.03
D1DBTuned = D1DBPure.query(studyparams.TUNING_FILTER)
nD1DBTuned = nD1DBPure.query(studyparams.TUNING_FILTER)
D1ClustersTuned = D1DBTuned.__len__()
nD1ClustersTuned = nD1DBTuned.__len__()
print("D1 filtered R2 = {0}\nnD1 filtered R2 = {1}".format(D1ClustersTuned, nD1ClustersTuned))

#%% Sound responsive in any capacity
D1DBResponse = D1DB.query("(noiseburst_pVal < 0.05 or tuning_pVal < 0.05 or am_response_pVal < 0.05 or tuningTest_pVal < 0.05)")
nD1DBResponse = nD1DB.query("(noiseburst_pVal < 0.05 or tuning_pVal < 0.05 or am_response_pVal < 0.05 or tuningTest_pVal < 0.05)")  # Adding in the tuningTest gave 50 cells to D1 and 200 cells to nD1
D1ResponseClusters = D1DBResponse.__len__()
nD1ResponseClusters = nD1DBResponse.__len__()
print("D1 sound responsive clusters = {0}\nnD1 sound responsive clusters = {1}".format(D1ResponseClusters, nD1ResponseClusters))

#%% AM cells
D1AM = D1DB.query("am_response_pVal < 0.05")
nD1AM = nD1DB.query("am_response_pVal < 0.05")
D1AMCount = D1AM.__len__()
nD1AMCount = nD1AM.__len__()
print("D1 AM cell count: {0}\nnD1 AM cell count: {1}".format(D1AMCount, nD1AMCount))

D1Synced = D1DB.query("am_synchronization_pVal < 0.05")
nD1Synced = nD1DB.query("am_synchronization_pVal < 0.05")
D1SyncedCount = D1Synced.__len__()
nD1SyncedCount = nD1Synced.__len__()
print("D1 synced cell count: {0}\nnD1 synced cell count: {1}".format(D1SyncedCount, nD1SyncedCount))

#%% Tuning test counts
D1tt = D1DB.query("tuningTest_pVal < 0.05")
nD1tt = nD1DB.query("tuningTest_pVal < 0.05")
D1TTCount = D1tt.__len__()
nD1TTCount = nD1tt.__len__()
print("D1 tuning test responsive cells: {0}\nnD1 tuning test responsive cells: {1}".format(D1TTCount, nD1TTCount))

D1TTTuned = D1tt.query("ttR2Fit > 0.03")
nD1TTTuned = nD1tt.query("ttR2Fit > 0.03")
D1TTTunedCount = D1TTTuned.__len__()
nD1TTTunedCount = nD1TTTuned.__len__()
print("D1 tuned TT cells: {0}\nnD1 tuned TT cells: {1}".format(D1TTTunedCount, nD1TTTunedCount))
