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
figureCount = 1
figureTotal = 0

for indRow, dbRow in celldb.iterrows():
    oneCell = ephyscore.Cell(dbRow)
    if oneCell.get_session_inds('preLowFreq') != [] and oneCell.get_session_inds('highFreq') != []:
        figureTotal += 1

for indRow, dbRow in celldb.iterrows():
    plt.clf()

    oneCell = ephyscore.Cell(dbRow)
    gsMain = gs.GridSpec(4, 3)
    gsMain.update(left=0.075, right=0.98, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4) #Change spacing of things
    

    # Plot Waveform
    ax0 = plt.subplot(gsMain[0])
    plt.plot(dbRow.spikeShape, linewidth = 3)
    plt.text(30, -0.1, f"bestChannel = {dbRow.bestChannel}")

    # lowFreq = the low frequency is the oddball
    # Lock spikes during prelowFreq paradigm to events.
    if oneCell.get_session_inds('preLowFreq') != []: #and oneCell.get_session_inds('lowFreq') != []:
        ephysData, bdataLow = oneCell.load('preLowFreq')
        spikeTimesLow = ephysData['spikeTimes']
        eventOnsetTimesLow = ephysData['events']['stimOn']
        eventOnsetTimesLow = eventOnsetTimesLow[:-1]
        timeRange = [-0.3, 0.45]  # In seconds
        (spikeTimesFromEventOnsetLowPre, trialIndexForEachSpikeLowPre, indexLimitsEachTrialLowPre) = spikesanalysis.eventlocked_spiketimes(spikeTimesLow, eventOnsetTimesLow, timeRange)

        # Lock spikes during prehighFreq paradigm to events.
        ephysData, bdataHigh = oneCell.load('preHighFreq')
        spikeTimesHigh = ephysData['spikeTimes']
        eventOnsetTimesHigh = ephysData['events']['stimOn']
        eventOnsetTimesHigh= eventOnsetTimesHigh[:-1]
        timeRange = [-0.3, 0.45]  # In seconds
        (spikeTimesFromEventOnsetHighPre, trialIndexForEachSpikeHighPre, indexLimitsEachTrialHighPre) = spikesanalysis.eventlocked_spiketimes(spikeTimesHigh, eventOnsetTimesHigh, timeRange)

        # Sort by frequencies for LowFreqOddball
        frequencies_each_trial_low = bdataLow['currentStartFreq']
        array_of_frequencies_low = np.unique(frequencies_each_trial_low)
        trialsEachCondLowPre = behavioranalysis.find_trials_each_type(frequencies_each_trial_low, array_of_frequencies_low)

        #Sort by frequencies for HighFreqOddball
        frequencies_each_trial_high= bdataHigh['currentStartFreq']
        array_of_frequencies_high = np.unique(frequencies_each_trial_high)
        trialsEachCondHighPre = behavioranalysis.find_trials_each_type(frequencies_each_trial_high, array_of_frequencies_high)


        # Extract only high freqency column and reshape array for raster_plot function
        trialsEachHighFreqLowPre = trialsEachCondLowPre[:,1].reshape(-1,1)
        trialsEachHighFreqHighPre = trialsEachCondHighPre[:,1].reshape(-1,1)

        # Extract only low freqency column and reshape array for raster_plot function
        trialsEachLowFreqLowPre = trialsEachCondLowPre[:,0].reshape(-1,1) # when low is the oddball, get the low freqs
        trialsEachLowFreqHighPre = trialsEachCondHighPre[:,0].reshape(-1,1)

        # Get the index of trials before oddball for LowFreqOddball
        trialIndexBeforeOddball = np.array(np.flatnonzero(trialsEachLowFreqLowPre[:,0])) -1
        nTrials = len(frequencies_each_trial_low)
        trialBeforeOddballPreLow = np.zeros(nTrials, dtype=bool)
        trialBeforeOddballPreLow[trialIndexBeforeOddball]=True
        trialBeforeOddballPreLow = trialBeforeOddballPreLow.reshape(-1,1) 
        
        # Get the index of trials before oddball for HighFreqOddball
        trialIndexBeforeOddball = np.array(np.flatnonzero(trialsEachHighFreqHighPre[:,0])) -1
        nTrials = len(frequencies_each_trial_high)
        trialBeforeOddballPreHigh = np.zeros(nTrials, dtype=bool)
        trialBeforeOddballPreHigh[trialIndexBeforeOddball]=True
        trialBeforeOddballPreHigh = trialBeforeOddballPreHigh.reshape(-1,1) 


        # Raster Plot of high frequency when it is standard
        # ax1 = plt.subplot(gsMain[1])
        # fRaster = extraplots.raster_plot(spikeTimesFromEventOnsetLowPre, indexLimitsEachTrialLowPre, timeRange, trialsEachHighFreqLowPre)
        # plt.xlabel('Time (s)')
        # plt.ylabel('Trials')
        # plt.title('13kHz (preLowFreq)')

        # Raster Plot of high frequency when it is oddball
        # ax3 = plt.subplot(gsMain[2])
        # fRaster = extraplots.raster_plot(spikeTimesFromEventOnsetHighPre, indexLimitsEachTrialHighPre, timeRange, trialsEachHighFreqHighPre)
        # plt.xlabel('Time (s)')
        # plt.ylabel('Trials')
        # plt.title('13kHz (preHighFreq)')

        # New Raster Plot
        colorsEachCond = ['#39b5c4', '#f04158']

        stfeo = np.concatenate((spikeTimesFromEventOnsetHighPre, spikeTimesFromEventOnsetLowPre))
        ilet = np.hstack((indexLimitsEachTrialHighPre, indexLimitsEachTrialLowPre +len(spikeTimesFromEventOnsetHighPre)))

        tec1 = np.vstack((trialBeforeOddballPreHigh, np.zeros(trialsEachHighFreqHighPre.shape)))
        tec2 = np.vstack((np.zeros(trialBeforeOddballPreHigh.shape), trialsEachHighFreqHighPre))
        tec = np.hstack((tec1, tec2))

        highFreqLabels = ('Standard', "Oddball")
        ax1 = plt.subplot(gsMain[1])
        plt.xlabel('Time (s)')
        plt.ylabel('Firing Rate')
        plt.title('13kHz Tone (pre')
        pRaster, hcond, zline = extraplots.raster_plot(stfeo, ilet, timeRange, tec, colorsEachCond, labels= highFreqLabels)
        

        
        # PSTH of high frequency 
        binWidth = 0.010
        timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
        smoothWinSizePsth = 2 
        lwPsth = 2
        downsampleFactorPsth = 1

        ax2 = plt.subplot(gsMain[4])    
        spikeCountMatLow = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetLowPre, indexLimitsEachTrialLowPre, timeVec)
        spikeCountMatHigh = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetHighPre, indexLimitsEachTrialHighPre, timeVec)

        colorsEachCond = ['#39b5c4', '#f04158'] #add to PSTH when multiple conditions present.
        colorsEachCond2 = ['#f04158'] #add to PSTH when multiple conditions present.

        extraplots.plot_psth(spikeCountMatLow/binWidth, smoothWinSizePsth, timeVec, trialBeforeOddballPreHigh, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        extraplots.plot_psth(spikeCountMatHigh/binWidth, smoothWinSizePsth, timeVec, trialsEachHighFreqHighPre, colorsEachCond2, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time (s)')
        plt.ylabel('Firing Rate')
        plt.title('13kHz (lowFreq)')
        plt.legend(("Standard Tone", "Oddball Tone"), loc='below')

        # Title of image
        plt.suptitle(f'{oneCell} {figureCount}/{figureTotal}', fontsize=16, fontweight='bold', y = 0.99)
        figureCount+=1

       
        # Change shape of entire figure
        plt.gcf().set_size_inches([12.8, 9.6])
        plt.show()

        

        # Save Figure
        # figPath = os.path.join(settings.FIGURES_DATA_PATH, 'cell_reports', f'{subject}_{dbRow.date}_{dbRow.maxDepth}um_c{dbRow.cluster}_report.png')
        # plt.savefig(figPath, format='png')



        plt.close()
