import os
import sys
import numpy as np
import pandas as pd
from jaratoolbox import settings
from jaratoolbox import celldatabase
import figparams
reload(figparams)

STUDY_NAME = figparams.STUDY_NAME

####################################################################################
scriptFullPath = os.path.realpath(__file__)
alphaLevel = 0.05
numFreqs = 2
movementWindow = [0.0, 0.3]
###################################################################################
#dbKey = 'reward_change'
dbFolder = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
celldbPath = os.path.join(dbFolder, 'rc_database.h5')
celldb = celldatabase.load_hdf(celldbPath)

gosi010MaxDepth = 1660
gosi010PortionOfTrackInsideAC = 1 - float(1/2.5) # Between 1/3 and 1/2 of the track from the deepest point is outside AC

gosi004MaxDepth = 1700
gosi004PortionOfTrackOutsideAC = float(1/3) # 1/3 of the track from the surface of the brain is not in AC

goodQualACCells = celldb.query("keepAfterDupTest==1 and brainArea=='rightAC'")

gosi010Cells = goodQualACCells.query("subject=='gosi010'")
actualDepthEachCellGosi010 = gosi010Cells['depth_this_cell']
gosi010cellsOutsideAC = gosi010Cells[actualDepthEachCellGosi010 > gosi010MaxDepth * gosi010PortionOfTrackInsideAC]

gosi004Cells = goodQualACCells.query("subject=='gosi004'")
actualDepthEachCellGosi004 = gosi004Cells['depth_this_cell']
gosi004cellsOutsideAC = gosi004Cells[actualDepthEachCellGosi004 < gosi004MaxDepth * gosi004PortionOfTrackOutsideAC]

print('gosi010 has {} cells outside AC included in all good cells'.format(len(gosi010cellsOutsideAC)))
print('gosi004 has {} cells outside AC included in all good cells'.format(len(gosi004cellsOutsideAC)))

if len(gosi010cellsOutsideAC):
	movementModI = gosi010cellsOutsideAC['movementModI_{}_removedsidein'.format(movementWindow)]
	movementModS = gosi010cellsOutsideAC['movementModS_{}_removedsidein'.format(movementWindow)]
	encodeMv = (gosi010cellsOutsideAC['movementSelective_moredif_Mv'] + gosi010cellsOutsideAC['movementSelective_samedif_MvSd']).astype(bool)

	sigMovSel = (movementModS < alphaLevel) #& encodeMv

	soundResp = gosi010cellsOutsideAC.behavPval.apply(lambda x: np.min(x[~np.isnan(x)]) < alphaLevel / numFreqs) 

	print('gosi010 has {} sound responsive cells and {} choice selective cells outside AC'
		.format(sum(sigMovSel), sum(soundResp)))