#! /usr/bin/env python

import os
import argparse as arp
import numpy as np
import matplotlib.pyplot as plt
import time
from jaratoolbox import settings, celldatabase, \
    ephyscore, extraplots, spikesanalysis, behavioranalysis

NROW = 3
NCOL = 4


def get_args():
    '''Parses user inputs from command line'''
    
    parser = arp.ArgumentParser(description="""This script is for creating cell reports containing 
                                raster plots for multiple cellsrecorded in a single session. Plots
                                are saved to the FIGURES_DATA_PATH specificed in jaratoolbox.settings""") 
    
    parser.add_argument("-s","--subject", help='Subject name (e.g., "-s test000")',
                        required=True)
    parser.add_argument("-d","--sessionDate", help='Date of recording (e.g., \
                        "-d 2025-01-21")',
                        required=True)
    parser.add_argument("-p","--probeDepth", help="Depth of probe",
                        required=True)
    parser.add_argument("-t", "--tkParadigms", help='(Optional) tkParadigms to be summarized \
                        (e.g., "-t AM"). Should be comma separated if doing multiple \
                        (e.g, "-t AM,Freq"). Defaults to plotting all paradigms',
                        required=False, default='')
    parser.add_argument("-n","--studyName", help="(Optional) name of study",
                        required=False,default='')
    parser.add_argument("-c","--cellsToPlot", help='(Optional) list of cells to plot (e.g., \
                        "-c 12,52,19,29"). Defaults to plotting all cells',
                        required=False,default='')
    return parser.parse_args()



stim_types = {"AM":"currentFreq",
              "Freq":"currentFreq",
              "naturalSound":"soundID"}

ylabs = {"AM":"AM rate (Hz)",
         "Freq":"Tone Frequency (Hz)",
         "naturalSound":"Sound ID"}

# get args
args = get_args()
subject = args.subject
studyName = args.studyName
sessionDate = args.sessionDate
probeDepth = int(args.probeDepth)
paradigms = args.tkParadigms.split(',')
someCells = args.cellsToPlot
if someCells != '':
	someCells = [int(i) for i in args.cellsToPlot.split(',')]



# get data
dbPath = os.path.join(settings.DATABASE_PATH, studyName, f'celldb_{subject}.h5')

if os.path.exists(dbPath):
    celldb = celldatabase.load_hdf(dbPath)
else:
    celldb = celldatabase.generate_cell_database(os.path.join(settings.INFOREC_PATH,
                                                              f"{subject}_inforec.py"))


# subset data
if not someCells:
    celldbSubset = celldb[(celldb.date==sessionDate) & (celldb.pdepth==probeDepth)]
else:
    celldbSubset = celldb[(celldb.date==sessionDate) & (celldb.pdepth==probeDepth) & (celldb.cluster in someCells)]

someCells = np.arange(len(celldbSubset))
ensemble = ephyscore.CellEnsemble(celldbSubset)

if not paradigms[0]:
    paradigms = list(celldbSubset.sessionType)[0]

stims = [stim_types[sType] for sType in paradigms]

cellsPerPage = NROW*NCOL
rasterTimeRange = [-0.5, 1]  # In seconds


numcells = len(someCells)
numpages = int(np.ceil(numcells/cellsPerPage))

# create folders in figures directory if not already present

studyFolder = os.path.join(settings.FIGURES_DATA_PATH,studyName)
subjectFolder = os.path.join(studyFolder,subject)
sessionFolder = os.path.join(subjectFolder,sessionDate)

if not os.path.exists(studyFolder):
    os.mkdir(studyFolder)                   # folder for this study (just the figures directory if no studyName)
if not os.path.exists(subjectFolder):
    os.mkdir(subjectFolder)                 # folder for this subject
if not os.path.exists(sessionFolder):
    os.mkdir(sessionFolder)                 # folder for this session

for paradigm,stim in zip(paradigms,stims):
    paradigmFolder = os.path.join(sessionFolder,paradigm)
    if not os.path.exists(paradigmFolder):
        os.mkdir(paradigmFolder)                # folder for current paradigm

    ephysData,bdata = ensemble.load(paradigm)
    nTrials = len(bdata[stim])
    eventOnsetTimes = ephysData['events']['stimOn'][:nTrials] # Ignore trials not in bdata 

    spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = \
        ensemble.eventlocked_spiketimes(eventOnsetTimes, rasterTimeRange)
    

    for page in range(numpages):
        fig = plt.figure(1,figsize=(20, 12))
        filename = f"{subject}_{sessionDate}_{probeDepth}_{paradigm}_{page+1}.png"
        figname = f"{subject} {sessionDate} {probeDepth} {paradigm} {page+1}/{numpages}"
        
        # plot cells for current page
        currentStim = bdata[stim]
        possibleStim = np.unique(currentStim)
        trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStim)

        for count, indcell in enumerate(someCells[page*cellsPerPage:(page+1)*cellsPerPage]):
            plt.subplot(NROW, NCOL, count+1)
            pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnsetAll[indcell], indexLimitsEachTrialAll[indcell],
                                                    rasterTimeRange, trialsEachCond, labels=possibleStim)
            
            plt.setp(pRaster, ms=2)
            plt.xlabel('Time (s)')
            plt.ylabel(ylabs[paradigm])
            plt.title(f"Cell #{celldbSubset.iloc[indcell].cluster} (best channel: {celldbSubset.iloc[indcell].bestChannel})")
            
        plt.suptitle(figname)
        plt.tight_layout()
        plt.savefig(os.path.join(paradigmFolder,filename))
        plt.close(1)

