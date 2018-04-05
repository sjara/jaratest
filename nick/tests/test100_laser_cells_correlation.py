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

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')

# laserCells = db.query('pulsePval < 0.05 and pulseZscore > 0 and trainRatio > 0.8')
allMaxCorrs = np.empty(len(db))

for indCellIter, (indCell, cell) in enumerate(db.iterrows()):
    try:
        subject = cell['subject']
        date = cell['date']
        depth = cell['depth']
        tetrode = cell['tetrode']
        taggedCellCluster = int(cell['cluster'])
        cellsThisTetrode = db.query("subject==@subject and date==@date and depth==@depth and tetrode==@tetrode")

        wavesThisTetrode = np.empty((len(cellsThisTetrode), 160))
        namesThisTetrode = []

        cellName = "{}_{}_{}_TT{}c{}".format(subject, date, depth, tetrode, taggedCellCluster)

        subfolder = '20180323_laserCellCorr'
        figPath = '/home/nick/data/reports/nick/{}/{}'.format(subfolder, cellName)
        if not os.path.exists(figPath):
            os.makedirs(figPath)

        for indIter, (indCTS, cellThisTetrode) in enumerate(cellsThisTetrode.iterrows()):
            timestamps, samples, recordingNumber = load_all_spikedata(cellThisTetrode)

            sampleReshape = np.reshape(samples, [len(samples), 160])
            sampleAverage = sampleReshape.mean(axis=0)
            wavesThisTetrode[indIter, :] = sampleAverage
            # plt.plot(range(len(sampleAverage)), sampleAverage)
            # plt.show()
            # plt.waitforbuttonpress()
            subject = cellThisTetrode['subject']
            date = cellThisTetrode['date']
            depth = int(cellThisTetrode['depth'])
            tetrode = int(cellThisTetrode['tetrode'])
            cluster = int(cellThisTetrode['cluster'])
            namesThisTetrode.append("c{}".format(cluster))
            cellName = "{}_{}_{}_TT{}c{}".format(subject, date, depth, tetrode, cluster)

            # plt.clf()
            # pinp_report.plot_pinp_report(cellThisTetrode )
            # figsize = (9, 11)
            # plt.gcf().set_size_inches(figsize)
            # outputDir = figPath
            # fullName = os.path.join(outputDir, cellName)
            # plt.savefig(fullName,format='png')

        indTaggedCell = namesThisTetrode.index("c{}".format(taggedCellCluster))
        ccSelf, ccAcross = clusteranalysis.spikeshape_correlation([wavesThisTetrode])
        plt.clf()
        corrArr = ccSelf[0]
        corrTaggedCell = corrArr[indTaggedCell, :]
        maxCorr = sorted(corrTaggedCell)[-2] #Have to take second to last because self-self corr is 1
        allMaxCorrs[indCellIter] = maxCorr
        print "Cell {} out of {}".format(indCellIter, len(db))
    except:
        allMaxCorrs[indCellIter] = np.nan

    ### Plotting correlation arrays
    # plt.imshow(corrArr, cmap='Reds')
    # for (ind0, ind1), pixVal in np.ndenumerate(corrArr):
    #     plt.text(ind0, ind1, np.round(pixVal, decimals=3), ha='center', va='center')
    # ax = plt.gca()
    # ax.set_xticks(range(len(wavesThisTetrode)))
    # ax.set_yticks(range(len(wavesThisTetrode)))
    # ax.set_xticklabels(namesThisTetrode)
    # ax.set_yticklabels(namesThisTetrode)
    # figsize=(4, 4)
    # plt.gcf().set_size_inches(figsize)
    # outputDir = figPath
    # fullName = os.path.join(outputDir, "corrs")
    # plt.savefig(fullName,format='png')


    # plt.clf()
    # plt.imshow(ccSelf[0])
    # plt.show()
    # plt.waitforbuttonpress()



