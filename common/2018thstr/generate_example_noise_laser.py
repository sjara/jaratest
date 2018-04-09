import os
import numpy as np
from numpy import inf
from scipy import optimize
from scipy import stats
from scipy import signal
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
import figparams
import pandas as pd
import matplotlib.pyplot as plt

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
db = pd.read_hdf(dbPath, key='dataframe')

ath = db.groupby('brainArea').get_group('rightThal')
ac = db.groupby('brainArea').get_group('rightAC')

queryString = 'noisePval<0.05 and pulsePval<0.05 and pulseZscore>0 and trainRatio>0.8'
athResponsive = ath.query(queryString)
acResponsive = ac.query(queryString)

sessionsToSave = ['noiseburst', 'laserpulse']

# for indRow, dbRow in acResponsive.iterrows():
#     plt.clf()
#     cell = ephyscore.Cell(dbRow)
#     for indSessiontype, sessiontype in enumerate(sessionsToSave):
#         try:
#             ephysData, bdata = cell.load(sessiontype)
#         except:
#             print "Cell {} has no {}".format(indRow, sessiontype)
#             continue
#         spikeTimes = ephysData['spikeTimes']
#         eventOnsetTimes = ephysData['events']['stimOn']
#         alignmentRange = [-0.5, 1]
#         (spikeTimesFromEventOnset,
#          trialIndexForEachSpike,
#          indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
#                                                                        eventOnsetTimes,
#                                                                        alignmentRange)
#         plt.subplot(2, 1, indSessiontype+1)

#         plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.')
#     plt.suptitle(indRow)
#     plt.waitforbuttonpress()

thalExampleDict = celldatabase.get_cell_info(db, 683)
acExampleDict = celldatabase.get_cell_info(db, 1140)


