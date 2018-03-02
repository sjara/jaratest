import pandas as pd
from scipy import signal
import numpy as np
from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import loadopenephys
from jaratoolbox import extraplots
from jaratoolbox import settings
from jaratoolbox import ephyscore
import figparams
from matplotlib import pyplot as plt
import os

STUDY_NAME = '2018thstr'

dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase.h5')
db = pd.read_hdf(dbPath, key='dataframe')

goodLaser = db.query('isiViolations<0.02 and spikeShapeQuality>2 and pulsePval<0.05 and trainRatio>0.8')

goodLaserAM = goodLaser.query('highestSync>0')

goodLaserTuned = goodLaser[pd.notnull(goodLaser['BW10'])].query('rsquaredFit > 0.1')

goodLaserAMTuned = goodLaserAM[pd.notnull(goodLaserAM['BW10'])].query('rsquaredFit > 0.1')


