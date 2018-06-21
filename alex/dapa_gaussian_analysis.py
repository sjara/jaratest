import os, sys
import argparse
import pdb
import numpy as np
from numpy import inf
from scipy import optimize
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
from jaratoolbox import celldatabase
from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import ephyscore
reload(loadopenephys)
from jaratoolbox import settings

parser = argparse.ArgumentParser(description='Generate reports for dapa mice electrophysiology')
#parser.add_argument('subject', metavar='subject', help='dapa mouse to analyze')
#parser.add_argument('--analyze_all', action='store_true', help='analyze all cells')
parser.add_argument('--cell', type = int, default=None, help='specific cell to analyze')
parser.add_argument('--gaussian', action='store_true', help='test Gaussian function')

args = parser.parse_args()

#subject = args.subject
#subject = dapa011

'''
if args.cell:
    dbRow = goodCells.loc[args.cell]
    generate_report(args.cell, dbRow)
    sys.exit()

if not args.analyze_all:
    current = os.listdir(finaldir)
    date_list = []
    for cell in current:
        date = cell.split('_')[0]
        if date not in date_list:
            date_list.append(date)
    #print(len(goodCells))
    newCells = goodCells
    for ind, cell in goodCells.iterrows():
        if cell['date'] in date_list:
            newCells = newCells.drop([ind])
    #print(len(newCells))
    goodCells = newCells
'''



dapa_list = ['dapa012', 'dapa013', 'dapa014']

cell_list = [[73,86,126,127,129,182,191],
             [157,161,223,227,436,453,454,455,456,
             457,464,490,504,620,621,626,631,633,634,
             658,674,676,677,679,693,694,695,696,708,
             728,731,742,743,744,746,774,777,800],
             [305,306,307,328,329,330,331,398,399,414,
              423,478,481,484,497,538,539,554,565,567,
              678]]

all_cell_len = [len(x) for x in cell_list]

all_amplitude = np.empty((sum(all_cell_len), 4))
all_mean = np.empty((sum(all_cell_len), 4))
all_sigma = np.empty((sum(all_cell_len), 4))
all_asymptote = np.empty((sum(all_cell_len), 4))
count = 0
for dapaInd, dapa in enumerate(dapa_list):

    dbpath = '/home/jarauser/data/databases/{}_clusterdatabase.h5'.format(dapa)
    db = pd.read_hdf(dbpath, key='database')

    finaldir = '/home/jarauser/data/reports_alex/{}/test/'.format(dapa)

    # Select the good, isolated cells from the database
    goodCells = db.query('isiViolations < 0.02')
    goodCells = goodCells.reset_index(drop=True)

    for ind, indRow in enumerate(cell_list[dapaInd]):
        print(count)
        dbRow = goodCells.loc[indRow]

        #generate_report(indRow, dbRow)
        cell = ephyscore.Cell(dbRow)

        #Find the inds for the laser tuning curve sessions
        laserTuningSessionInds = cell.get_session_inds('laserTuningCurve')

        #Go through the tuning curve sessions and plot the rasters
        if len(laserTuningSessionInds) == 0:
            continue

        all_amplitude[count,:] = (dbRow['gaussianVals'][0][0], dbRow['gaussianVals'][1][0], dbRow['gaussianVals'][2][0], dbRow['gaussianVals'][3][0])
        all_mean[count,:] = (dbRow['gaussianVals'][0][1], dbRow['gaussianVals'][1][1], dbRow['gaussianVals'][2][1], dbRow['gaussianVals'][3][1])
        all_sigma[count,:] = (dbRow['gaussianVals'][0][2], dbRow['gaussianVals'][1][2], dbRow['gaussianVals'][2][2], dbRow['gaussianVals'][3][2])
        all_asymptote[count,:] = (dbRow['gaussianVals'][0][3], dbRow['gaussianVals'][1][3], dbRow['gaussianVals'][2][3], dbRow['gaussianVals'][3][3])

        count += 1

amplitude_diffs = all_amplitude[:,3]-all_amplitude[:,1]

plt.figure()
plt.hist(amplitude_diffs, range=(-10, 10), bins=40)
#plt.hist(amplitude_diffs, range=(-50, 50), bins=40)
#plt.hist(amplitude_diffs, bins=20)
plt.show()

sys.exit()
