import os
import numpy as np
from jaratoolbox import settings
from jaratoolbox import celldatabase
from scipy import stats
import pandas as pd
import re
import ipdb
import figparams
from jaratoolbox import histologyanalysis as ha
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache

# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_calculated_columns.h5')
db = celldatabase.load_hdf(dbPath)

# db = pd.read_hdf(dbPath, key='dataframe')

mcc = MouseConnectivityCache(resolution=25)
rsp = mcc.get_reference_space()

#This is the allen atlas rotated to coronal so that it matches what we use
rspAnnotationVolumeRotated = np.rot90(rsp.annotation, 1, axes=(2, 0))

areas = []

goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodLaser = goodShape.query("autoTagged==1 and subject not in ['pinp018', 'pinp021']")
# goodNSpikes = goodLaser.query('nSpikes>2000')

goodPulseLatency = goodLaser.query('summaryPulseLatency<0.01')
goodNSpikes = goodPulseLatency.query('nSpikes>2000')

goodSoundResponsiveBool = (~pd.isnull(goodNSpikes['BW10'])) | (~pd.isnull(goodNSpikes['highestSyncCorrected'])) | (goodNSpikes['noiseZscore']<0.05)
# goodSoundResponsiveBool = (~pd.isnull(goodNSpikes['BW10'])) | (~pd.isnull(goodNSpikes['highestSyncCorrected']))
goodSoundResponsive = goodNSpikes[goodSoundResponsiveBool]

ac = goodSoundResponsive.groupby('brainArea').get_group('rightAC')
thal = goodSoundResponsive.groupby('brainArea').get_group('rightThal')

dataframe = ac
for indRow, dbRow in dataframe.iterrows():
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
    else:
        # ipdb.set_trace()
        structName = 'No Coords!'

    areas.append(structName)

from collections import Counter





