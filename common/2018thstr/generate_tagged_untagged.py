import os
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import colorpalette
from scipy import stats
import copy
import pandas as pd
import figparams
reload(figparams)

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
dataframe = pd.read_hdf(dbPath, key='dataframe')

taggedBool = (dataframe['pulsePval']<0.05) & (dataframe['trainRatio']>0.8)
taggedCells = dataframe[taggedBool]
untaggedCells = dataframe[~taggedBool]

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

closeUntaggedBool = (untaggedCells['idString'].isin(taggedCells['idString']) | untaggedCellsSSA['idString'].isin(taggedCells['idString']))
closeUntagged = untaggedCells[closeUntaggedBool]
farUntaggedBool = ~closeUntaggedBool
farUntagged = untaggedCells[farUntaggedBool]

for indRow, row in closeUntagged.iterrows():
    dataframe.loc[indRow, 'closeUntagged'] = 1
dataframe['closeUntagged'][pd.isnull(dataframe['closeUntagged'])]=0
for indRow, row in farUntagged.iterrows():
    dataframe.loc[indRow, 'farUntagged'] = 1
dataframe['farUntagged'][pd.isnull(dataframe['farUntagged'])]=0
for indRow, row in taggedCells.iterrows():
    dataframe.loc[indRow, 'tagged'] = 1
dataframe['tagged'][pd.isnull(dataframe['tagged'])]=0

dataframe['closeUntagged'] = dataframe['closeUntagged'].astype(bool)
dataframe['farUntagged'] = dataframe['farUntagged'].astype(bool)
dataframe['tagged'] = dataframe['tagged'].astype(bool)

print "Saving dataframe to {}".format(dbPath)
dataframe.to_hdf(dbPath, key='dataframe')

