"""
Test creating a celldb v4.0 for the older data (d1pi)
"""

import os
import sys
from matplotlib import pyplot as plt
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis

from importlib import reload
reload(celldatabase)
reload(ephyscore)


inforecFile = os.path.join(settings.INFOREC_PATH,'d1pi000_inforec.py')
celldb = celldatabase.generate_cell_database(inforecFile)

#d = np.load('/data/ephys/d1pi047/multisession_2020-02-24_2900um/Tetrode2_stats.npz')

cellDict = {'subject': 'd1pi047',
            'date': '2020-02-26',
            'pdepth': 3500,
            'egroup': 4,
            'cluster': 3}

# d1pi047 2020-02-25 (3500um) g2c2
# d1pi047 2020-02-26 (3500um) g4c3

#dbRow = celldb.iloc[0]
cellInd, dbRow = celldatabase.find_cell(celldb, **cellDict)

plt.clf()
#for indRow, dbRow in celldb.iterrows():
if 1:
    oneCell = ephyscore.Cell(dbRow)

    ephysData, bdata = oneCell.load('am')

    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.2, 0.8]

    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    plt.cla()
    plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.k', markersize=3)
    plt.ylabel('Trials')
    plt.xlabel('Time (s)')
    plt.title(oneCell)
    plt.tight_layout()
    plt.show()
    #input(f'{oneCell}  Press ENTER')
