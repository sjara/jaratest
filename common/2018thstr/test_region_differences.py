import os
from jaratoolbox import settings
import pandas as pd
import numpy as np
import figparams
from jaratoolbox import histologyanalysis as ha)
rsp = mcc.get_reference_space()
rspAnnotationVolumeRotated = np.rot90(rsp.annotation, 1, axes=(2, 0))


dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
db = pd.read_hdf(dbPath, key='dataframe')
db['location'] = ''

#First have to get the brain area for each cell
for indRow, dbRow in db.iterrows():
    try:
        thisCoordID = rspAnnotationVolumeRotated[int(dbRow['cellX']), int(dbRow['cellY']), int(dbRow['cellZ'])]
    except ValueError:
        db.at[indRow, 'location'] = 'NaN'
    else:
        structDict = rsp.structure_tree.get_structures_by_id([thisCoordID])[0]
        db.at[indRow, 'location'] = structDict['name']

tagged = db.query('isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==1')
untagged = db.query('isiViolations<0.02 and spikeShapeQuality>2 and autoTagged==0')

# plt.clf()
columns = ['BW10', 'latency', 'threshold', 'highestSyncCorrected', 'mutualInfoBCBits']
for col in columns:
    untagged.boxplot(by='location', column=col, rot=-90, layout=(5, 1))
plt.show()




