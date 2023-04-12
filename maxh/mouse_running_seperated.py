import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import main_function as max
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis

import scipy.optimize
import matplotlib

subject = 'acid006'

# Set to True if want to load one cell. Defaults to loading first cell unless cellDict is complete.
oneFigure = False

# Add info for loading a specific cell.
cellDict = {'subject' : '',
            'date' : '2023-03-23',
            'pdepth' : 3000,
            'egroup' : 1,
            'cluster' : 120}


inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
dbPath = os.path.join(settings.DATABASE_PATH ,f'celldb_{subject}.h5')

celldb = celldatabase.generate_cell_database(inforecFile)
# Used to load specific recording session dates.
#celldb = celldb.query("date == '2023-03-23'")
figureCount = 1
figureTotal = 0



# PSTH params
timeRange = [-0.3, 0.45]
binWidth = 0.010
timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
smoothWinSizePsth = 2 
lwPsth = 2
downsampleFactorPsth = 1

if (oneFigure == True) and (cellDict['subject'] != '' ):
    cellInd, dbRow = celldatabase.find_cell(celldb, **cellDict)
    oneCell = ephyscore.Cell(dbRow)

else: 
    for indRow, dbRow in celldb.iterrows():
        oneCell = ephyscore.Cell(dbRow)
        if oneCell.get_session_inds('preLowFreq') != [] and oneCell.get_session_inds('preHighFreq') != []:
            figureTotal += 1

    for indRow, dbRow in celldb.iterrows():
        #plt.clf()

        oneCell = ephyscore.Cell(dbRow)


        fig = plt.figure()
        gsMain = gs.GridSpec(2, 3, figure=fig)
        gsOne = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[0])
        gsTwo = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[1])
        gsThree = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[2])
        gsFour = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[3])
        gsFive = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[4])
        gsSix = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[5])
        plt.subplots_adjust(hspace=0.10)
        gsMain.update(top=0.9, bottom=0.1, wspace=0.45, hspace=0.45) #Change spacing of things (left=0.075, right=0.98) 

        
        # Title of image
        plt.suptitle(f'{oneCell} combined {figureCount:03d}/{figureTotal:03d}', fontsize=16, fontweight='bold', y = 0.99)
        
        
        if oneCell.get_session_inds('salineLowFreq') != []:
            ephysData, bdata = oneCell.load('salineLowFreq')


            startTrialState = bdata.stateMatrix['statesNames']['startTrial']
            trialStartEvents = (bdata.events['nextState']==startTrialState)
            trialStartTime = bdata.events['eventTime'][trialStartEvents]


            spikeTimes = ephysData['spikeTimes']
            eventOnsetTimes = ephysData['events']['stimOn']


            # Timestamps of running and stopping in video
            runStart = [0, 21, 64] #- trialStartTime[0]
            runStop = [12, 38, 83 ] #- trialStartTime[0]

            selectedTrials = []

            # Creates an list of indexs of the trials where the mouse is running.
            for start, stop in zip(runStart, runStop):
                selectedTrials.extend([j for j,v in enumerate(eventOnsetTimes) if start <= v <= stop])


            frequencies_each_trial = bdata['currentStartFreq']

            if (len(frequencies_each_trial) > len(eventOnsetTimes)) or (len(frequencies_each_trial) < len(eventOnsetTimes)-1):
                print(f'Warning! BevahTrials ({len(frequencies_each_trial)}) and ' + f'EphysTrials ({len(eventOnsetTimes)})')
                sys.exit()

            if len(frequencies_each_trial) == len(eventOnsetTimes)-1:
                eventOnsetTimes = eventOnsetTimes[:len(frequencies_each_trial)]


            # Creates a boolean of all the trials where running is TRUE
            ntrials = len(eventOnsetTimes)
            runningBoolean = np.zeros(ntrials, dtype=bool)
            runningBoolean[selectedTrials] = True
                






            (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

            array_of_frequencies = np.unique(frequencies_each_trial)
            trialsEachCond = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)


            # Extract column and reshape array for raster_plot function
            trialsEachFreqColumn1 = trialsEachCond[:,0].reshape(-1,1) 
            trialsEachFreqColumn2 = trialsEachCond[:,1].reshape(-1,1)


            # Post Saline
            if oneCell.get_session_inds('salineLowFreq') != []:

                (spikeTimesHigh, trialIndexHigh, indexLimitsHigh, LowStd, HighOdd) = max.main_function(oneCell, 'salineHighFreq', timeRange)
                (spikeTimesLow, trialIndexLow, indexLimitsLow, LowOdd, HighStd) = max.main_function(oneCell, 'salineLowFreq', timeRange)

                # Get standard trials before oddball trials
                trialsBeforeOddLowStd = max.trials_before_oddball(HighOdd)       
                trialsBeforeOddHighStd = max.trials_before_oddball(LowOdd)
                

                # Combine spike times and index limits of standard and oddball trials.
                (combinedSpikeTimesHigh, combinedIndexLimitsHigh) = max.combine_index_limits(spikeTimesLow, spikeTimesHigh, indexLimitsLow, indexLimitsHigh)
                (combinedSpikeTimesLow, combinedIndexLimitsLow) = max.combine_index_limits(spikeTimesHigh, spikeTimesLow, indexLimitsHigh, indexLimitsLow)
                
                
                
                # Combine trials of high freq before oddball and high freq oddball.
                combinedTrialsHigh = max.combine_trials(trialsBeforeOddHighStd, HighOdd)

                # Combine trials of low freq before oddball and low freq oddball.
                combinedTrialsLow = max.combine_trials(trialsBeforeOddLowStd, LowOdd)


                # Creates a trialsEachCond for the running and nonrunning oddball.
                runningOddballHigh, nonRunningOddballHigh = max.seperate_running_trials(combinedTrialsHigh, runningBoolean)
                runningOddballLow, nonRunningOddballHigh = max.seperate_running_trials(combinedTrialsLow, runningBoolean)

                # Create spikeCountMat for psth
                spikeCountMatHigh = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeVec)
                spikeCountMatLow = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesLow, combinedIndexLimitsLow, timeVec)

                # Raster plot of high frequency
                colorsEachCond = ['#39b5c4', '#f04158']
                highFreqLabels = ('Standard', "Oddball")
                ax0 = plt.subplot(gsOne[0])
                #plt.xlabel('Time (s)')
                plt.ylabel('Trials')
                plt.title('13kHz Tone - Combined')
                ax0.tick_params(labelbottom=False) 
                pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeRange, combinedTrialsHigh, colorsEachCond, labels= highFreqLabels)
                for p in pRaster:
                    p.set_markersize(4)

                # PSTH of highFreq trials (may not need spikeCountMatHigh)
                ax1 = plt.subplot(gsOne[1], sharex=ax0)    
                extraplots.plot_psth(spikeCountMatHigh/binWidth, smoothWinSizePsth, timeVec, combinedTrialsHigh, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
                plt.xlabel('Time (s)')
                plt.ylabel('Firing Rate')
                #plt.title('8kHz (post)')
                plt.legend(("Standard Tone", "Oddball Tone"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)


                # Raster plot of running     
                ax2 = plt.subplot(gsTwo[0])
                #plt.xlabel('Time (s)')
                plt.ylabel('Trials')
                plt.title('13kHz Tone - Running')
                ax2.tick_params(labelbottom=False) 
                pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeRange, runningOddballHigh, colorsEachCond, labels= highFreqLabels)
                for p in pRaster:
                    p.set_markersize(4)

                # PSTH of lowFreq trials
                ax2 = plt.subplot(gsTwo[1], sharex=ax2)    
                extraplots.plot_psth(spikeCountMatHigh/binWidth, smoothWinSizePsth, timeVec, runningOddballHigh, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
                plt.xlabel('Time (s)')
                plt.ylabel('Firing Rate')
                #plt.title('13kHz (post)')
                plt.legend(("Standard Tone", "Oddball Tone"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)


                # Raster plot of nonrunning     
                ax3 = plt.subplot(gsThree[0])
                #plt.xlabel('Time (s)')
                plt.ylabel('Trials')
                plt.title('13kHz Tone - NonRunning')
                ax3.tick_params(labelbottom=False) 
                pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeRange, nonRunningOddballHigh, colorsEachCond, labels= highFreqLabels)
                for p in pRaster:
                    p.set_markersize(4)

                # PSTH of lowFreq trials
                ax4 = plt.subplot(gsThree[1], sharex=ax3)    
                extraplots.plot_psth(spikeCountMatHigh/binWidth, smoothWinSizePsth, timeVec, nonRunningOddballHigh, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
                plt.xlabel('Time (s)')
                plt.ylabel('Firing Rate')
                #plt.title('13kHz (post)')
                plt.legend(("Standard Tone", "Oddball Tone"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)

                ax5 = plt.subplot(gsFour[0])
                pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeRange, nonRunningOddballHigh, colorsEachCond, labels= highFreqLabels)
                pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeRange, runningOddballHigh, colorsEachCond, labels= highFreqLabels)
                

 
                


                num_plots = len(fig.get_axes())

                # Goes through each psth plot and calculutes the lowest and highest ylimit values.
                max_ylim = -np.inf
                min_ylim = np.inf
                for i, ax in enumerate(fig.get_axes()[1::2]):
                    ylim = ax.get_ylim()
                    if ylim[0] < min_ylim:
                        min_ylim = ylim[0]
                    if ylim[1] > max_ylim:
                        max_ylim = ylim[1]
                    
                # Iterates through each psth plot and changes the ylimits to the min and max ylimit.
                new_ylimits = [0, max_ylim]
                for i, ax in enumerate(fig.get_axes()[1::2]):
                    ax.set_ylim(new_ylimits)


                '''
                # concatenate the array with itself to create an array of size 1002
                b = np.concatenate((runningBoolean, runningBoolean))

                # add a new dimension to the array and copy the data
                runningBoolean = np.tile(b[:, np.newaxis], (1, 2))

                runningOddball = np.zeros_like(combinedTrialsHigh, dtype=bool)
                for i in range(combinedTrialsHigh.shape[0]):
                    for j in range(combinedTrialsHigh.shape[1]):
                        if combinedTrialsHigh[i,j] and runningBoolean[i,j]:
                            runningOddball[i,j] = True
                 '''


            
                # Plot Waveform
                ax0 = fig.add_axes([0.9, 0.9, 0.1, 0.1])
                ax0.plot(dbRow.spikeShape, linewidth = 3)
                #plt.text(30, -0.1, f"bestChannel = {dbRow.beate}_{dbRow.maxDepth}um_c{dbRow.cluster}_combined_report.png'
                #fileName = os.path.join(figDirectory, figName)

                plt.gcf().set_size_inches([16, 9])
                #plt.gcf().set_dpi(100)

                #mng = plt.get_current_fig_manager()
                #mng.full_screen_toggle()
                plt.show()
                #plt.savefig(fileName, format='png')
                #print(f'saving image {figName}')
                figureCount+=1
        
                if oneFigure == True:
                    sys.exit()
                
                plt.close()
        print("done")




