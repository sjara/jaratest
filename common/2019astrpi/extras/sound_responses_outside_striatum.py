"""Calculating ttoal number of cells that respond to sound while outside of
the striatum across all subjects histology data is known for."""
#%%
import sys
sys.path.append('..')
import pandas as pd
import numpy as np
from jaratoolbox import celldatabase
import studyparams

db = celldatabase.load_hdf('/var/tmp/figuresdata/2019astrpi/direct_and_indirect_cells_time.h5')
db = db.query(studyparams.FIRST_FLTRD_CELLS)

#%% Isolating non-empty and non-striatal clusters
foundAreasDB = db.query("recordingSiteName != ''")
inverseBrainAreaDB = foundAreasDB.query("~(recordingSiteName == 'Caudoputamen')")

#%% Finding sound responsive clusters
soundResponse = inverseBrainAreaDB.query("(noiseburst_pVal < 0.05 or tuning_pVal < 0.05 or am_response_pVal < 0.05)")
# soundResponse = inverseBrainAreaDB.query("(tuning_pVal < 0.05 or am_response_pVal < 0.05)")
# Finding how many of each brain region
regionCounts = soundResponse.recordingSiteName.value_counts()
print(regionCounts, regionCounts.sum(), sep="\n")
