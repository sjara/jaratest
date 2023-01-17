import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
import scipy.optimize
import matplotlib

subject = 'acid001'

inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
dbPath = os.path.join(settings.DATABASE_PATH ,f'celldb_{subject}.h5')

celldb = celldatabase.generate_cell_database(inforecFile)

for indRow, dbRow in celldb.iterrows():
    plt.clf()

    oneCell = ephyscore.Cell(dbRow)
    gsMain = gs.GridSpec(1, 3)
    gsMain.update(left=0.075, right=0.98, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4) #Change spacing of things
    plt.suptitle(oneCell, fontsize=16, fontweight='bold', y = 0.99)

    # Plot Waveform
    ax0 = plt.subplot(gsMain[0, 0])
    plt.plot(dbRow.spikeShape, linewidth = 3)
    plt.text(30, -0.1, f"bestChannel = {dbRow.bestChannel}")

    # lowFreq = lowfrequency is the oddball
    # Lock to event
    if oneCell.get_session_inds('lowFreq') != []: #and oneCell.get_session_inds('lowFreq') != []:
        ephysData, bdata = oneCell.load('lowFreq')
        spikeTimesLow = ephysData['spikeTimes']
        eventOnsetTimesLow = ephysData['events']['stimOn']
        eventOnsetTimesLow = eventOnsetTimesLow[:-1]
        timeRange = [-0.3, 0.45]  # In seconds

        (spikeTimesFromEventOnsetLow, trialIndexForEachSpikeLow, indexLimitsEachTrialLow) = spikesanalysis.eventlocked_spiketimes(spikeTimesLow, eventOnsetTimesLow, timeRange)


        # raster Plot
        frequencies_each_trial = bdata['currentStartFreq']

        oddballIndex = []
        for i in range(0, len(frequencies_each_trial)): 
            if frequencies_each_trial[i] == 8000 : 
                oddballIndex.append(i)

        array_of_frequencies = np.unique(frequencies_each_trial)
        trialsEachCond = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)

        #sorted, sortedtrialsindex = spikesanalysis.sort_by_trial_type(trialIndexForEachSpikeLow, trialsEachCond)


        #trialsEachHighFreq = trialsEachCond[:,1]

       
        fRaster = extraplots.raster_plot(spikeTimesFromEventOnsetLow, indexLimitsEachTrialLow, timeRange)


        ax1 = plt.subplot(gsMain[0, 1])
        #lowRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnsetLow, indexLimitsEachTrialLow,timeRange)
        #plt.setp(fRaster, ms=2)
        plt.xlabel('Time (s)')
        plt.ylabel('Trials')
        plt.title('13kHz (lowFreq)')
        plt.show()



        # binWidth = 0.010
        # timeRange = [-0.3, 0.45]
        # timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
        # smoothWinSizePsth = 2 
        # lwPsth = 2
        # downsampleFactorPsth = 1
        # ax2 = plt.subplot(gsMain[0,2 ])    
        # spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetLow, indexLimitsEachTrialLow, timeVec)
        # frequenciesEachTrialStd = bdata['highFreq']
        # numberOfTrialsStd = len(frequenciesEachTrialStd)
        # arrayOfFrequenciesStd = np.unique(bdata['currentStartFreq'])

        # trialsEachCondStd = behavioranalysis.find_trials_each_type(frequenciesEachTrialStd,
        # arrayOfFrequenciesStd)

        # HighFreqStdInStdPara = indexLimitsEachTrialLow[:,trialsEachCondStd[:,1]]
        # spikeCountMatHighFreqStdInStdPara = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetLow,
        #         HighFreqStdInStdPara,timeVec)


        # #labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesStd]


        # highPSTH = extraplots.plot_psth(spikeCountMatHighFreqStdInStdPara/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)

        plt.show()