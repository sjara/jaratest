import os
import numpy as np
import pandas as pd
from jaratoolbox import ephyscore
from jaratoolbox import clusteranalysis
from jaratoolbox import extraplots
from matplotlib import pyplot as plt
from jaratest.nick.reports import pinp_report
reload(pinp_report)

def load_all_spikedata(dbRow):
    '''
    Load the spike data for all recorded sessions into a set of arrays.
    Args:
        dbRow (pandas.Series): One row from a pandas cell database created using generate_cell_database or by
                              manually constructing a pandas.Series object that contains the required fields.
    Returns:
        timestamps (np.array): The timestamps for all spikes across all sessions
        samples (np.array): The samples for all spikes across all sessions
        recordingNumber (np.array): The index of the session where the spike was recorded
    '''
    samples=np.array([])
    timestamps=np.array([])
    recordingNumber=np.array([])
    cell = ephyscore.Cell(dbRow)
    for ind, sessionType in enumerate(cell.dbRow['sessionType']):
        ephysData, bdata = cell.load(sessionType)
        numSpikes = len(ephysData['spikeTimes'])
        sessionVector = np.zeros(numSpikes)+ind
        if len(samples)==0:
            samples = ephysData['samples']
            timestamps = ephysData['spikeTimes']
            recordingNumber = sessionVector
        else:
            samples = np.concatenate([samples, ephysData['samples']])
            # Check to see if next session ts[0] is lower than self.timestamps[-1]
            # If so, add self.timestamps[-1] to all new timestamps before concat
            if not len(ephysData['spikeTimes'])==0:
                if ephysData['spikeTimes'][0]<timestamps[-1]:
                    ephysData['spikeTimes'] = ephysData['spikeTimes'] + timestamps[-1]
                timestamps = np.concatenate([timestamps, ephysData['spikeTimes']])
                recordingNumber = np.concatenate([recordingNumber, sessionVector])
    return timestamps, samples, recordingNumber

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/BAD_celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')

for indCellIter, (indCell, cell) in enumerate(db.iterrows()):
    subject = cell['subject']
    date = cell['date']
    depth = cell['depth']
    tetrode = cell['tetrode']
    taggedCellCluster = int(cell['cluster'])
    cellsThisTetrode = db.query("subject==@subject and date==@date and depth==@depth and tetrode==@tetrode")

    wavesThisTetrode = np.empty((len(cellsThisTetrode), 160))
    namesThisTetrode = []

    cellName = "{}_{}_{}_TT{}c{}".format(subject, date, depth, tetrode, taggedCellCluster)

    subfolder = '20180328_BAD_2018thstr_cell_reports'
    outputDir = '/home/nick/Desktop/{}'.format(subfolder)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    fullName = os.path.join(outputDir, "{}.png".format(cellName))
    print fullName
    # NOTE: For only plotting things if they aren't already plotted
    # if os.path.exists(fullName):
    #     print "Cell {} already plotted".format(cellName)
    # else:
    try:
        plt.clf()
        pinp_report.plot_pinp_report(cell)
        figsize = (9, 11)
        plt.gcf().set_size_inches(figsize)
        fullName = os.path.join(outputDir, cellName)
        plt.savefig(fullName,format='png')
    except ValueError:
        print 'Cell {} cannot plot'.format(cellName)
