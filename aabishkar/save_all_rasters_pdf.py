"""
Save raster plots of neurons in response to natural sounds.
 Feat017
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from importlib import reload
reload(celldatabase)

subject = 'feat017'

inforecFile = os.path.join(settings.INFOREC_PATH,f'{subject}_inforec.py')
inforecFile = inforecFile.replace('.py','.test2.py')
celldb = celldatabase.generate_cell_database(inforecFile)

# Read the inforec file and get experiments to extract date and maxDepth into a list of tuples
experiments = celldatabase.read_inforec(inforecFile).experiments
date_maxDepth = [(experiment.date, experiment.maxDepth) for experiment in experiments]

# -- Load the data --
# Since you can only load cellEnsemble for same date and pdepth, create a celldbSubsets dict
celldbSubsets = {}
for session, depth in date_maxDepth:
    key = f"{subject}_{session}_{depth}"
    celldbSubsets[key] = celldb[(celldb.date == session) & (celldb.pdepth == depth)]

pdfFilePath = f"raster_plots_{subject}.pdf"
with PdfPages(pdfFilePath) as pdf:
    for celldb_name, celldbSubset in celldbSubsets.items():
        ensemble = ephyscore.CellEnsemble(celldbSubset)

        ephysData, bdata = ensemble.load('naturalSound')
        currentStim = bdata['soundID']
        timeRange = [-0.5, 6]  # In seconds

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

        for page in range(numPages):
            plt.clf()
            fig, axs = plt.subplots(4, 7, figsize=(20, 15))
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
            pdf.savefig(fig)
            plt.close(fig)

    print(f'Raster plots saved to {pdfFilePath}')