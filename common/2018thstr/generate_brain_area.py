import os
import numpy as np
from jaratoolbox import settings
from jaratoolbox import celldatabase
from scipy import stats
import pandas as pd
import re
import figparams
from jaratoolbox import histologyanalysis as ha
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
db = pd.read_hdf(dbPath, key='dataframe')

mcc = MouseConnectivityCache(resolution=25)
rsp = mcc.get_reference_space()

#This is the allen atlas rotated to coronal so that it matches what we use
rspAnnotationVolumeRotated = np.rot90(rsp.annotation, 1, axes=(2, 0))

areas = []
for indRow, dbRow in db.iterrows():
    if not pd.isnull(dbRow['cellX']): #IF we have coords for the cell

        try:
            thisCoordID = rspAnnotationVolumeRotated[int(dbRow['cellX']), int(dbRow['cellY']), int(dbRow['cellZ'])]
        except IndexError:
            print "Error for cell {}".format(indRow)
        if thisCoordID != 0:
            structDict = rsp.structure_tree.get_structures_by_id([thisCoordID])
            structName = [d['name'] for d in structDict][0]
        else:
            structName = "Outside the brain?"

        areas.append(structName)


