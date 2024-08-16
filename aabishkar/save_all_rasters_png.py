"""
Save raster plots of neurons in response to natural sounds.
"""
import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from importlib import reload
reload(celldatabase)

scriptName = os.path.basename(__file__)

if len(sys.argv) < 2:
    print('This command requires a subject as argument.\n' +
          f'Example: {scriptName} test000')
    sys.exit()

if 2 < len(sys.argv) < 4:
    print('This command requires a subject, date, and probe depth as arguments.\n' +
          f'Example: {scriptName} test000 2024-01-01 3000')
    sys.exit()

start_time = time.time()

subject = sys.argv[1]
date_pdepth = [(sys.argv[2], int(sys.argv[3]))] if len(sys.argv) > 3 else []

inforecFile = os.path.join(settings.INFOREC_PATH,f'{subject}_inforec.py')

# remove this line once error-handled celldatabase file is used
inforecFile = inforecFile.replace('.py','.test2.py')

celldb = celldatabase.generate_cell_database(inforecFile)

# file path to save PNGs. Please change this before running the script
filePath = f'/Users/aabishkar/Documents/Lab/rasters/{subject}'

# Extract date and pdepth as list of tuples if user didn't specify the site.
if len(date_pdepth) == 0:
    date_grouped = celldb.groupby('date')['pdepth'].unique()
    for date, pdepth_values in date_grouped.items():
        date_pdepth.extend([(date, pdepth) for pdepth in pdepth_values])

# -- Load the data --
# Since you can only load cellEnsemble for same date and pdepth, create a celldbSubsets dict
celldbSubsets = {}
for date, pdepth in date_pdepth:
    key = f"{subject}_{date}_{pdepth}"
    celldbSubsets[key] = celldb[(celldb.date == date) & (celldb.pdepth == pdepth)]

for celldb_name, celldbSubset in celldbSubsets.items():
    ensemble = ephyscore.CellEnsemble(celldbSubset)

    ephysData, bdata = ensemble.load('naturalSound')
    currentStim = bdata['soundID']
    timeRange = [-2, 6]  # In seconds

    nTrials = len(currentStim)
    eventOnsetTimes = ephysData['events']['stimOn'][:nTrials] # Ignore trials not in bdata

    spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = \
        ensemble.eventlocked_spiketimes(eventOnsetTimes, timeRange)

    possibleStim = np.unique(currentStim)

    trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStim)
    nTrialsEachCond = trialsEachCond.sum(axis=0)  # Not used, but in case you need it

    condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)
    sortingInds = np.argsort(sortedTrials)  # This will be used to sort trialIndexForEachSpike

    # -- Plot rasters and save to PDF --
    totalNeurons = celldbSubset.shape[0]
    neuronsPerPage = 28
    numPages = (totalNeurons + neuronsPerPage - 1) // neuronsPerPage  # Calculate the number of pages needed
    images = []
    for page in range(numPages):
        plt.clf()
        fig, axs = plt.subplots(4, 7, figsize=(24, 15))
        axs = axs.flatten()
        fig.suptitle(f'{celldb_name} - Page {page + 1}', fontsize=16)
        for count, indcell in enumerate(range(page * neuronsPerPage, min((page + 1) * neuronsPerPage, totalNeurons))):
            if indcell >= totalNeurons:
                break
            sortedIndexForEachSpike = sortingInds[trialIndexForEachSpikeAll[indcell]]
            axs[count].plot(spikeTimesFromEventOnsetAll[indcell], sortedIndexForEachSpike, '.k', ms=1)
            axs[count].set_xlabel('Time (s)')
            axs[count].set_ylabel(f'[{indcell}] Sorted trials')

        # Remove any unused subplots
        for ax in axs[count + 1:]:
            fig.delaxes(ax)

        plt.tight_layout()
        os.makedirs(f'{filePath}/{celldb_name}', exist_ok=True)
        png_filename = f'{filePath}/{celldb_name}/{celldb_name}_{(page + 1):03d}.png'
        plt.savefig(png_filename, format='png', dpi=100, pad_inches=0.3)
        plt.close(fig)

    print(f'Finished saving PNGs for {celldb_name}')

end_time = time.time()
print(f"Total time taken by the script: {end_time - start_time:.2f} seconds")