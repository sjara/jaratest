import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from collections import Counter
from scipy import stats
import pandas as pd
import figparams
reload(figparams)

FIGNAME = 'figure_am'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')

db = pd.read_hdf(dbPath, key='dataframe')
goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
cellsToUse = goodShape.query('autoTagged==1')
goodNSpikes = goodLaser.query('nSpikes>2000')

cellsToUse = goodNSpikes.query('taggedCond==0 or taggedCond==1')

ac = cellsToUse.groupby('brainArea').get_group('rightAC')
thal = cellsToUse.groupby('brainArea').get_group('rightThal')


