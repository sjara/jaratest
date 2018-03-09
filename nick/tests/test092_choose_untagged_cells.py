import os
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import colorpalette
from scipy import stats
import pandas as pd
import copy
# import figparams
# reload(figparams)

STUDY_NAME = '2018thstr'

dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase.h5')
dbase = pd.read_hdf(dbPath, key='dataframe')
soundResponsive = dbase[dbase['noiseZscore']<0.05]
taggedBool = (soundResponsive['pulsePval']<0.05) & (soundResponsive['trainRatio']>0.8)
taggedCells = soundResponsive[taggedBool]

# #This is the old way of selecting untagged cells
untaggedCells = soundResponsive[~taggedBool]

# taggedSelectionAttrs = taggedCells[['subject', 'date', 'depth', 'tetrode']]

# #The untagged cells need to come from a subject, date, depth of a tagged cell. Enforcing tetrode would be easy, but I think we should enforce shank instead.
# #So if a tagged cell is on tetrode 2, an untagged cell can come from TT1 or 2 but not any others. So we need to be able to translate between tetrodes on
# #the same shank.
# #Use: sameShankAs[1] = 2
sameShankAs = {1:2, 2:1, 3:4, 4:3, 5:6, 6:5, 7:8, 8:7}

untaggedCellsSSA = copy.deepcopy(untaggedCells)
newTetrode = [sameShankAs[tt] for tt in untaggedCellsSSA['tetrode']]
untaggedCellsSSA['tetrode'] = newTetrode

for indRow, row in untaggedCells.iterrows():
    idString = "{}_{}_{}_{}".format(row['subject'], row['date'], row['depth'], row['tetrode'])
    untaggedCells.loc[indRow, 'idString'] = idString

for indRow, row in taggedCells.iterrows():
    idString = "{}_{}_{}_{}".format(row['subject'], row['date'], row['depth'], row['tetrode'])
    taggedCells.loc[indRow, 'idString'] = idString

for indRow, row in untaggedCellsSSA.iterrows():
    idString = "{}_{}_{}_{}".format(row['subject'], row['date'], row['depth'], row['tetrode'])
    untaggedCellsSSA.loc[indRow, 'idString'] = idString

untaggedBool = (untaggedCells['idString'].isin(taggedCells['idString']) | untaggedCellsSSA['idString'].isin(taggedCells['idString']))


