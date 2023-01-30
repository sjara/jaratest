import os
import sys
import numpy as np
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt

inforecFile = os.path.join(settings.INFOREC_PATH,'febe008_inforec.py')
celldb = celldatabase.generate_cell_database(inforecFile)

#Find a specific cell with a cellDict

# cellDict = {'subject' : 'febe008',
#             'date' : '2022-07-22',
#             'pdepth' : 2961,
#             'cluster' : 127,
#             'egroup' : 0
#             }
#cellInd = 0
#dbRow = celldb.iloc[cellInd]

#cellInd, dbRow = celldatabase.find_cell(celldb, **cellDict)
#oneCell = ephyscore.Cell(dbRow)

for indRow, dbRow in celldb.iterrows():
    oneCell = ephyscore.Cell(dbRow)
    plt.clf()

    ephysData, bdata = oneCell.load('pureTones')


    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.5, 1]  # In seconds

    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    # Raster Plot
    # timeRange = [-0.3,0.5]
    # pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange)


    #Differentiating cells by frequency.
    timeRange = [-0.3,0.5]


    frequencies_each_trial = bdata['currentFreq']
    array_of_frequencies = np.unique(bdata['currentFreq'])
    trialsEachCond = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)
    fRaster = extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange, trialsEachCond)

    plt.title(f'Cluster = {dbRow.cluster}, Depth = {dbRow.pdepth}, Date = {dbRow.date}')
    plt.imshow(trialsEachCond,aspect='auto')
    plt.show()
    input("press enter for next cell")

sys.exit()

