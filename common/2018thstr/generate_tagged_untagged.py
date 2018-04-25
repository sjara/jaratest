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

import fnmatch

# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
dataframe = pd.read_hdf(dbPath, key='dataframe')

# # Have to remove the cols first so that this method will work when we try to regenerate
# dataframe = dataframe.drop(['tagged', 'closeUntagged', 'farUntagged'], axis=1)

# TAGGED CONDITION: 0=tagged, 1=close untagged, 2=far untagged
taggedCond = np.full(len(dataframe), np.nan)
cellInds = np.full(len(dataframe), np.nan)

#New method - we are going to read the names of the directly tagged cells from a file.
# thalFn = 'goodThal.txt'
# acFn = 'goodAC.txt'
# thalFile = open(thalFn, 'r')
# acFile = open(acFn, 'r')
# thalTaggedCells = [cell.strip() for cell in thalFile.readlines()]
# acTaggedCells = [cell.strip() for cell in acFile.readlines()]
# allTaggedCells = thalTaggedCells + acTaggedCells

#For one tagged cells file
# taggedCellsFile = '/home/nick/Desktop/20180328_2018thstr_analysis/20180328_goodCells.txt'
# taggedFile = open(taggedCellsFile, 'r')
# allTaggedCells = [cell.strip() for cell in taggedFile.readlines()]

# taggedCellsFiles = ['/home/nick/Desktop/20180328_2018thstr_analysis/20180328_goodCells.txt',
#                     '/home/nick/Desktop/20180329_cellsToRescue.txt',
#                     '/home/nick/Desktop/20180329_needsCutting.txt']
# allTaggedCells = []
# for taggedCellsFile in taggedCellsFiles:
#     taggedFile = open(taggedCellsFile, 'r')
#     allTaggedCells.extend([cell.strip() for cell in taggedFile.readlines()])

allTaggedCells = []
for indIter, (indCell, cell) in enumerate(dataframe.iterrows()):
    subject = cell['subject']
    date = cell['date']
    depth = cell['depth']
    tetrode = cell['tetrode']
    cluster = int(cell['cluster'])
    cellName = "{}_{}_{}_TT{}c{}".format(subject, date, depth, tetrode, cluster)
    if cell['autoTagged']==1:
        taggedCond[indIter] = 0
        cellInds[indIter] = indCell
        allTaggedCells.append(cellName)
        print "Cell {} is tagged".format(indCell)

taggedBool = (taggedCond==0)
sameShankAs = {1:2, 2:1, 3:4, 4:3, 5:6, 6:5, 7:8, 8:7}

for indIter, (indCell, cell) in enumerate(dataframe.iterrows()):
    if taggedCond[indIter] != 0: #Either close or far untagged
        subject = cell['subject']
        date = cell['date']
        depth = cell['depth']
        tetrode = cell['tetrode']
        pattern = "{}_{}_{}_TT{}c*".format(subject, date, depth, tetrode)
        patternSSA = "{}_{}_{}_TT{}c*".format(subject, date, depth, sameShankAs[tetrode])

        matches = fnmatch.filter(allTaggedCells, pattern)
        matchesSSA = fnmatch.filter(allTaggedCells, patternSSA)
        if (len(matches)>0) | (len(matchesSSA)>0):
            #There was a match, this is a close untagged cell
            taggedCond[indIter] = 1
            cellInds[indIter] = indCell
        else:
            taggedCond[indIter] = 2
            cellInds[indIter] = indCell

dataframe['taggedCond'] = taggedCond

print "Saving dataframe to {}".format(dbPath)
dataframe.to_hdf(dbPath, key='dataframe')


# taggedCells = dataframe[taggedBool]
# untaggedCells = dataframe[~taggedBool]


# untaggedCellsSSA = copy.deepcopy(untaggedCells)
# newTetrode = [sameShankAs[tt] for tt in untaggedCellsSSA['tetrode']]
# untaggedCellsSSA['tetrode'] = newTetrode

# for indRow, row in untaggedCells.iterrows():
#     idString = "{}_{}_{}_{}".format(row['subject'], row['date'], row['depth'], row['tetrode'])
#     untaggedCells.loc[indRow, 'idString'] = idString

# for indRow, row in taggedCells.iterrows():
#     idString = "{}_{}_{}_{}".format(row['subject'], row['date'], row['depth'], row['tetrode'])
#     taggedCells.loc[indRow, 'idString'] = idString

# for indRow, row in untaggedCellsSSA.iterrows():
#     idString = "{}_{}_{}_{}".format(row['subject'], row['date'], row['depth'], row['tetrode'])
#     untaggedCellsSSA.loc[indRow, 'idString'] = idString

# closeUntaggedBool = (untaggedCells['idString'].isin(taggedCells['idString']) | untaggedCellsSSA['idString'].isin(taggedCells['idString']))
# closeUntagged = untaggedCells[closeUntaggedBool]
# farUntaggedBool = ~closeUntaggedBool
# farUntagged = untaggedCells[farUntaggedBool]

# for indRow, row in closeUntagged.iterrows():
#     dataframe.loc[indRow, 'closeUntagged'] = 1
# dataframe['closeUntagged'][pd.isnull(dataframe['closeUntagged'])]=0
# for indRow, row in farUntagged.iterrows():
#     dataframe.loc[indRow, 'farUntagged'] = 1
# dataframe['farUntagged'][pd.isnull(dataframe['farUntagged'])]=0
# for indRow, row in taggedCells.iterrows():
#     dataframe.loc[indRow, 'tagged'] = 1
# dataframe['tagged'][pd.isnull(dataframe['tagged'])]=0

# dataframe['closeUntagged'] = dataframe['closeUntagged'].astype(bool)
# dataframe['farUntagged'] = dataframe['farUntagged'].astype(bool)
# dataframe['tagged'] = dataframe['tagged'].astype(bool)
