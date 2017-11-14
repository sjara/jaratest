import pandas
import sys
from jaratest.nick.stats import eventresponse
from jaratest.nick.utils import progressbar
from jaratest.nick.database import dataloader_v2 as dataloader
import numpy as np

# dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb_q10.pickle'
dbfn = '/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb_q10.pickle'
database = pandas.read_pickle(dbfn)

nCells = len(database)

noiseburstZ = []
noiseburstP = []
for index, cell in database.iterrows():
    zStat, pVal = eventresponse.event_response_score(cell, 'NoiseBurst',
                                              responseRange = [0, 0.1],
                                              baseRange = [-0.1, 0])
    noiseburstZ.append(zStat)
    noiseburstP.append(pVal)

    message = 'Calculating Noise Burst Response'
    progressbar.progress_bar(index, nCells, message)

laserpulseZ = []
laserpulseP = []
for index, cell in database.iterrows():
    zStat, pVal = eventresponse.event_response_score(cell, 'LaserPulse',
                                              responseRange = [0, 0.1],
                                              baseRange = [-0.1, 0])
    laserpulseZ.append(zStat)
    laserpulseP.append(pVal)

    message = 'Calculating Laser Pulse Response'
    progressbar.progress_bar(index, nCells, message)

lasertrainZ = []
lasertrainP = []
for index, cell in database.iterrows():
    zStat, pVal = eventresponse.event_response_score(cell, 'LaserTrain', skip=5,
                                              responseRange = [0, 0.02],
                                              baseRange = [-0.02, 0])
    lasertrainZ.append(zStat)
    lasertrainP.append(pVal)

    message = 'Calculating Laser Train Response (last pulse)'
    progressbar.progress_bar(index, nCells, message)

noiseburstZ = np.array(noiseburstZ)
laserpulseZ = np.array(laserpulseZ)
lasertrainZ = np.array(lasertrainZ)

noiseburstP = np.array(noiseburstP)
laserpulseP = np.array(laserpulseP)
lasertrainP = np.array(lasertrainP)

database['noiseburstZ'] = noiseburstZ
database['laserpulseZ'] = laserpulseZ
database['lasertrainZ'] = lasertrainZ

database['noiseburstP'] = noiseburstP
database['laserpulseP'] = laserpulseP
database['lasertrainP'] = lasertrainP

database.to_pickle(dbfn)
