"""
Script for creating raster plot report of multiple cells from a recording session
"""

import os
import argparse as arp
import numpy as np
import matplotlib.pyplot as plt
import time
import re
from jaratoolbox import settings, celldatabase, loadneuropix, \
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

stim_types = {
    "AM" : "currentFreq",
    "Freq" : "currentFreq",
    "optoFreq" : "currentFreq",
    "optoAM" : "currentFreq",
    "naturalSound" : "soundID",
    "L2R3_L2R1_L1R2_L3R2" : "soundLocation"
}

ylabs = {
    "AM" : "AM rate (Hz)",
    "Freq" : "Tone Frequency (Hz)",
    "optoAM" : "AM rate (Hz)",
    "optoFreq" : "Tone Frequency (Hz)",
    "naturalSound" : "Sound ID",
    "L2R3_L2R1_L1R2_L3R2" : "Sound Location"
}

# get args
args = get_args()
subject = args.subject
studyName = args.studyName
sessionDate = args.sessionDate
probeDepth = int(args.probeDepth)
paradigms = args.tkParadigms.split(',')
cellsToPlot = args.cellsToPlot
if cellsToPlot != '':
	cellInds = [int(i) for i in args.cellsToPlot.split(',')]



### Load cell database, or create/save new database if needed
dbPath = os.path.join(settings.DATABASE_PATH, studyName, f'celldb_{subject}.h5')

if os.path.exists(dbPath): 
    celldb = celldatabase.load_hdf(dbPath)
    if not celldb['date'].isin([sessionDate]).any() :
        celldb = celldatabase.generate_cell_database(os.path.join(settings.INFOREC_PATH,
                                                              f"{subject}_inforec.py"))
        celldatabase.save_hdf(celldb, dbPath)
        
else:
    celldb = celldatabase.generate_cell_database(os.path.join(settings.INFOREC_PATH,
                                                              f"{subject}_inforec.py"))
    celldatabase.save_hdf(celldb, dbPath)


celldb = celldb.rename(columns={'info' : 'extra'})
celldb['soundLoc'] = [i[1] for i in celldb.extra]

### Subset data

celldbSubset = celldb[(celldb.date==sessionDate) \
                    & (celldb.pdepth==probeDepth) \
                        & (celldb.cluster_label=='good')]


if len(celldbSubset) == 0:
    raise Exception(f"error, no cells matching {sessionDate}, {probeDepth}um")

firstCell = celldbSubset.iloc[0].name

### for doing cellsToPlot as cluster #s instead of good cell #s ---v

# if cellsToPlot:
#     celldbSubset = celldb[(celldb.date==sessionDate) \
#                           & (celldb.pdepth==probeDepth) \
#                             & (celldb.cluster_label=='good') \
#                               & (celldb.cluster.isin(cellsToPlot))]

# cellInds = np.arange(len(celldbSubset))

### ---^

### for doing cellsToPlot as good cell #s ---v

if not cellsToPlot:
    cellInds = np.arange(len(celldbSubset))

### ---^

### load ensemble
ensemble = ephyscore.CellEnsemble(celldbSubset)

sessionTimes = {}

for ind,type in enumerate(celldbSubset.iloc[0].sessionType):
    sessionTimes[type] = celldbSubset.iloc[0].ephysTime[ind]

if not paradigms[0]:
    paradigms = [i for i in list(celldbSubset.sessionType)[0] if i != 'Spont']

stims = [stim_types[sType] for sType in paradigms]




# create folders in figures directory if not already present
studyFolder = os.path.join(settings.FIGURES_DATA_PATH,studyName)
subjectFolder = os.path.join(studyFolder,subject)
sessionFolder = os.path.join(subjectFolder,sessionDate)
siteFolder = os.path.join(sessionFolder, str(probeDepth)+'um')

if not os.path.exists(studyFolder):
    os.mkdir(studyFolder)                   # folder for this study (just the figures directory if no studyName)
if not os.path.exists(subjectFolder):
    os.mkdir(subjectFolder)                 # folder for this subject
if not os.path.exists(sessionFolder):
    os.mkdir(sessionFolder)                 # folder for this session
if not os.path.exists(siteFolder):
    os.mkdir(siteFolder)                    # folder for this site

### Determine figure/page parameters
if cellsToPlot:
    cellsPerPage = NROW*NCOL//len(paradigms)
    numcells = len(cellInds)
    numpages = int(np.ceil(numcells/cellsPerPage))
    numdigits = len(str(numpages))

elif "optoFreq" in paradigms or "optoAM" in paradigms:
    cellsPerPage = NROW*NCOL
    numcells = len(cellInds)
    numpages = int(np.ceil(numcells/cellsPerPage))
    numdigits = len(str(numpages))

else:
    cellsPerPage = NROW*NCOL
    numcells = len(cellInds)
    numpages = int(np.ceil(numcells/cellsPerPage))
    numdigits = len(str(numpages))
    

### Allocate data dicts
spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = {},{},{}
possibleStim,trialsEachCond,possibleLaser,trialsEachComb,rasterTimeRange,stimDur = {},{},{},{},{},{}
possibleYticks = {}

### Extract data
for paradigm,stim in zip(paradigms,stims):
    # load in the data
    ephysData,bdata = ensemble.load(paradigm)

    XML_PATH = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject,
                            f"{sessionDate}_{sessionTimes[paradigm]}_processed_multi",
                            "info", "settings.xml")

    pmap = loadneuropix.ProbeMap(XML_PATH)
    nTrials = len(bdata[stim])
    eventOnsetTimes = ephysData['events']['stimOn'][:nTrials] # Ignore trials not in bdata 

    stimDur[paradigm] = ephysData['events']['stimOff'][0] - ephysData['events']['stimOn'][0]

    rasterTimeRange[paradigm] = (min(-0.2,-0.5*stimDur[paradigm]),
                    max(0.6,1.5*stimDur[paradigm]))  # In seconds
    
    spikeTimesFromEventOnsetAll[paradigm], trialIndexForEachSpikeAll[paradigm], indexLimitsEachTrialAll[paradigm] = \
        ensemble.eventlocked_spiketimes(eventOnsetTimes, rasterTimeRange[paradigm])
    
    currentStim = bdata[stim]
    currentLaser = bdata['laserTrial']
        
    possibleStim[paradigm] = np.unique(currentStim)
    possibleLaser = np.unique(currentLaser)

    trialsEachCond[paradigm] = \
        behavioranalysis.find_trials_each_type(currentStim, possibleStim[paradigm])
    
    trialsEachComb[paradigm] = \
        behavioranalysis.find_trials_each_combination(currentStim,possibleStim[paradigm],
                                                      currentLaser,possibleLaser)
    

    if 'Freq' in paradigm:
        possibleYticks[paradigm] = np.round(possibleStim[paradigm]/1000,1)
        ylabs[paradigm] = ylabs[paradigm].replace('Hz','kHz')

    else:
        possibleYticks[paradigm] = possibleStim[paradigm]

    if 'opto' in paradigm:
        possibleYticks[paradigm] = list(possibleStim[paradigm])+list(possibleStim[paradigm])
    

# for plotting a subset of cells
if cellsToPlot: 
    outFolder = os.path.join(siteFolder,"cellSubsets") 
    if not os.path.exists(outFolder):
        os.mkdir(outFolder)                # output folder

    # draw raster plots
    for page in range(numpages):
        fig = plt.figure(1,figsize=(6*NCOL, 6*NROW))
        pageCells = cellsToPlot.split(',')[page*cellsPerPage:(page+1)*cellsPerPage]
        cellString = pageCells[0]
        for cell in pageCells[1:]:
            cellString += '-'+cell
        filename = f"{subject}_{sessionDate}_{probeDepth}_cells_{cellString}.png"
        
        if numpages > 1:
            figname = f"{subject} {sessionDate} {probeDepth} {page+1}/{numpages}"
        else:
            figname = f"{subject} {sessionDate} {probeDepth}"

        # plot cells for current page

        for count, indcell in enumerate(cellInds[page*cellsPerPage:(page+1)*cellsPerPage]):
            if len(paradigms) ==2:
                for row,paradigm in enumerate(paradigms):
                    nTrials = trialsEachCond[paradigm].shape[0]
                    plt.subplot(NROW, NCOL, count*2+row+1)
                    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnsetAll[paradigm][indcell], 
                                                                   indexLimitsEachTrialAll[paradigm][indcell],
                                                                   rasterTimeRange[paradigm], trialsEachComb[paradigm], 
                                                                   labels=possibleYticks[paradigm])
                    plt.setp(pRaster, ms=2)
                    plt.axvline(stimDur[paradigm], color='0.75', zorder=-10)
                    plt.xlabel('Time (s)')
                    plt.ylabel(ylabs[paradigm])
                    if 'opto' in paradigm:
                        midline = sum(1-np.nonzero(trialsEachComb[paradigm])[2])
                        plt.axhline(midline, color='r', zorder=-10)
                        plt.yticks([0.5*midline,1.5*midline],['laser OFF', 'laser ON'],minor=True)
                        ax = plt.gca()
                        ax.tick_params(axis='y',which='minor',left=False, right=True, labelleft=False, labelright=True)
                    curr_loc = celldbSubset.iloc[indcell]
                    curr_shank = pmap.channelShank[curr_loc.bestChannel]+1
                    curr_depth = curr_loc.maxDepth - pmap.ypos[curr_loc.bestChannel]
                    plt.title(f"Good Cell #{curr_loc.name - firstCell} {paradigm} \n (KS Unit #{curr_loc.cluster}, best channel: {curr_loc.bestChannel} (Shank #{curr_shank}, {curr_depth} {r'$\mu$'}m))")

            elif len(paradigms)==3:
                for row,paradigm in enumerate(paradigms):

                    plt.subplot(NROW, NCOL, count+row*4+1)
                    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnsetAll[paradigm][indcell], indexLimitsEachTrialAll[paradigm][indcell],
                                                            rasterTimeRange[paradigm], trialsEachCond[paradigm], labels=possibleYticks[paradigm])
                    plt.setp(pRaster, ms=2)
                    plt.axvline(stimDur[paradigm], color='0.75', zorder=-10)
                    plt.xlabel('Time (s)')
                    plt.ylabel(ylabs[paradigm])
                    if 'opto' in paradigm:
                        midline = sum(1-np.nonzero(trialsEachComb[paradigm])[2])
                        plt.axhline(midline, color='r', zorder=-10)
                        plt.yticks([0.5*midline,1.5*midline],['laser OFF', 'laser ON'],minor=True)
                        ax = plt.gca()
                        ax.tick_params(axis='y',which='minor',left=False, right=True, labelleft=False, labelright=True)
                    curr_loc = celldbSubset.iloc[indcell]
                    curr_shank = pmap.channelShank[curr_loc.bestChannel]+1
                    curr_depth = curr_loc.maxDepth - pmap.ypos[curr_loc.bestChannel]
                    if row==0:
                        plt.title(f"Good Cell #{curr_loc.name - firstCell}\n (KS Unit #{curr_loc.cluster}, best channel: {curr_loc.bestChannel} (Shank #{curr_shank}, {curr_depth} {r'$\mu$'}m))")

            elif len(paradigms)==1:
                for row,paradigm in enumerate(paradigms):
                    plt.subplot(NROW, NCOL, count+row+1)
                    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnsetAll[paradigm][indcell], indexLimitsEachTrialAll[paradigm][indcell],
                                                            rasterTimeRange[paradigm], trialsEachCond[paradigm], labels=possibleYticks[paradigm])
                    plt.setp(pRaster, ms=2)
                    plt.axvline(stimDur[paradigm], color='0.75', zorder=-10)
                    plt.xlabel('Time (s)')
                    plt.ylabel(ylabs[paradigm])
                    if 'opto' in paradigm:
                        midline = sum(1-np.nonzero(trialsEachComb[paradigm])[2])
                        plt.axhline(midline, color='r', zorder=-10)
                        plt.yticks([0.5*midline,1.5*midline],['laser OFF', 'laser ON'],minor=True)
                        ax = plt.gca()
                        ax.tick_params(axis='y',which='minor',left=False, right=True, labelleft=False, labelright=True)
                    curr_loc = celldbSubset.iloc[indcell]
                    curr_shank = pmap.channelShank[curr_loc.bestChannel]+1
                    curr_depth = curr_loc.maxDepth - pmap.ypos[curr_loc.bestChannel]
                    if row==0:
                        plt.title(f"Good Cell #{curr_loc.name - firstCell}\n (KS Unit #{curr_loc.cluster}, best channel: {curr_loc.bestChannel} (Shank #{curr_shank}, {curr_depth} {r'$\mu$'}m))")
        
        plt.suptitle(figname)
        plt.tight_layout()

        # save and close current page/fig
        plt.savefig(os.path.join(outFolder,filename))
        plt.close(1)

elif "optoFreq" in paradigms or "optoAM" in paradigms:
    for paradigm in paradigms:
        outFolder = os.path.join(siteFolder,paradigm)
        if not os.path.exists(outFolder):
            os.mkdir(outFolder)                # output folder

        midline = sum(1-np.nonzero(trialsEachComb[paradigm])[2])

        # draw raster plots
        for page in range(numpages):
            fig = plt.figure(1,figsize=(6*NCOL, 6*NROW))
            filename = f"{subject}_{sessionDate}_{probeDepth}_{paradigm}_{(page+1):02d}.png"
            
            if numpages > 1:
                figname = f"{subject} {sessionDate} {probeDepth} {paradigm} {page+1}/{numpages}"
            else:
                figname = f"{subject} {sessionDate} {probeDepth} {paradigm}"

            # plot cells for current page
            for count, indcell in enumerate(cellInds[page*cellsPerPage:(page+1)*cellsPerPage]):
                plt.subplot(NROW, NCOL, count+1)
                pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnsetAll[paradigm][indcell], indexLimitsEachTrialAll[paradigm][indcell],
                                                            rasterTimeRange[paradigm], trialsEachComb[paradigm],labels=possibleYticks[paradigm])
                plt.setp(pRaster, ms=2)
                plt.axvline(stimDur[paradigm], color='0.75', zorder=-10)
                plt.axhline(midline, color='r', zorder=-10)
                plt.xlabel('Time (s)')
                plt.ylabel(ylabs[paradigm])
                plt.axhline(midline, color='r', zorder=-10)
                plt.yticks([0.5*midline,1.5*midline],['laser OFF', 'laser ON'],minor=True)
                ax = plt.gca()
                ax.tick_params(axis='y',which='minor',left=False, right=True, labelleft=False, labelright=True)
                curr_loc = celldbSubset.iloc[indcell]
                curr_shank = pmap.channelShank[curr_loc.bestChannel]+1
                curr_depth = curr_loc.maxDepth - pmap.ypos[curr_loc.bestChannel]
                plt.title(f"Good Cell #{curr_loc.name - firstCell}\n (KS Unit #{curr_loc.cluster}, best channel: {curr_loc.bestChannel} (Shank #{curr_shank}, {curr_depth} {r'$\mu$'}m))")

                
            plt.suptitle(figname)
            plt.tight_layout()

            # save and close current page/fig
            plt.savefig(os.path.join(outFolder,filename))
            plt.close(1)

# for plotting all cells
else:
    for paradigm in paradigms:
        outFolder = os.path.join(siteFolder,paradigm)
        if not os.path.exists(outFolder):
            os.mkdir(outFolder)                # output folder

        # draw raster plots
        for page in range(numpages):
            fig = plt.figure(1,figsize=(6*NCOL, 4*NROW))
            filename = f"{subject}_{sessionDate}_{probeDepth}_{paradigm}_{(page+1):02d}.png"
            
            if numpages > 1:
                figname = f"{subject} {sessionDate} {probeDepth} {paradigm} {page+1}/{numpages}"
            else:
                figname = f"{subject} {sessionDate} {probeDepth} {paradigm}"

            # plot cells for current page
            for count, indcell in enumerate(cellInds[page*cellsPerPage:(page+1)*cellsPerPage]):
                plt.subplot(NROW, NCOL, count+1)
                pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnsetAll[paradigm][indcell], indexLimitsEachTrialAll[paradigm][indcell],
                                                            rasterTimeRange[paradigm], trialsEachCond[paradigm], labels=possibleYticks[paradigm])
                plt.setp(pRaster, ms=2)
                plt.axvline(stimDur[paradigm], color='0.75', zorder=-10)
                plt.xlabel('Time (s)')
                plt.ylabel(ylabs[paradigm])
                curr_loc = celldbSubset.iloc[indcell]
                curr_shank = pmap.channelShank[curr_loc.bestChannel]+1
                curr_depth = curr_loc.maxDepth - pmap.ypos[curr_loc.bestChannel]
                plt.title(f"Good Cell #{curr_loc.name - firstCell}\n (KS Unit #{curr_loc.cluster}, best channel: {curr_loc.bestChannel} (Shank #{curr_shank}, {curr_depth} {r'$\mu$'}m))")

                
            plt.suptitle(figname)
            plt.tight_layout()

            # save and close current page/fig
            plt.savefig(os.path.join(outFolder,filename))
            plt.close(1)

