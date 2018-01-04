import os
import numpy as np
from numpy import inf
from scipy import optimize
from scipy import stats
from scipy import signal
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import extraplots
from jaratoolbox import settings
import matplotlib.pyplot as plt
import figparams
import pandas as pd

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')

strCells = db.groupby('brainArea').get_group('rightAstr')

for indIter, (indRow, dbRow) in enumerate(strCells.iterrows()):
    cell = ephyscore.Cell(dbRow)
    try:
        ephysData, bdata = cell.load('am')
    except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
        failed=True
        print "No am for cell {}".format(indRow)
        continue

    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    freqEachTrial = bdata['currentFreq']
    alignmentRange = [-0.2, 0.7]
    possibleFreq = np.unique(freqEachTrial)
    freqLabels = ['{0:.1f}'.format(freq) for freq in possibleFreq]
    trialsEachCondition = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)

    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   alignmentRange)

    plt.clf()
    ax = plt.subplot(111)

    print len(spikeTimesFromEventOnset)



    pRaster, hCond, zline = extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial,
                                                   alignmentRange, trialsEachCondition,
                                                   labels=freqLabels)

    ax.set_xticks([0, 0.5])
    ax.set_xlabel('Time from sound onset (s)')
    ax.set_ylabel('AM Rate (Hz)')
    # plt.setp(pRaster, ms=2)

    figName = '{name}_{date}_{depth}um_TT{tetrode}c{cluster}.png'.format(name = cell.subject,
                                                                        date = cell.dbRow['date'],
                                                                        depth = cell.dbRow['depth'],
                                                                        tetrode = cell.tetrode,
                                                                        cluster = cell.cluster)
    savePath = os.path.join('/home/nick/data/reports/nick/20171218_striatum_am', figName)
    # plt.show()
    # plt.waitforbuttonpress()
    plt.savefig(savePath)
