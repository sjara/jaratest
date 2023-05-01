import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import oddball_analysis_functions as odbl
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis

import scipy.optimize
import matplotlib

subject = 'acid006'

# PSTH params
timeRange = [-0.3, 0.45]
binWidth = 0.010
timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
smoothWinSizePsth = 2 
lwPsth = 2
downsampleFactorPsth = 1

# Estimated delay in seconds between the start of ephys recording and start of video recording.
videoStartDelay = 1

# Load the videoTimes file module.
videoTimes = odbl.read_videotimes(f'./videoTimes/{subject}_videoTimes.py')


# Set to True if want to load one cell. Defaults to loading first cell unless cellDict is complete.
oneFigure = False

# Add info for loading a specific cell.
cellDict = {'subject' : '',
            'date' : '2023-03-23',
            'pdepth' : 3000,
            'egroup' : 1,
            'cluster' : 120}

# Used to load specific recording session dates.
'''
celldb = celldb.query("date == '2023-03-23'")            
'''


# Load inforec and generate cell database.
inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
dbPath = os.path.join(settings.DATABASE_PATH ,f'celldb_{subject}.h5')

celldb = celldatabase.generate_cell_database(inforecFile)

#Creates variables used for the titles of the files and figures.
figureCount = 1
figureTotal = len(celldb)


# If oneFigure is True and subject is declared, load only that specific cell.
if (oneFigure == True) and (cellDict['subject'] != '' ):
    cellInd, dbRow = celldatabase.find_cell(celldb, **cellDict)
    oneCell = ephyscore.Cell(dbRow)



else:
    
    # Loops through each cell to count the figures. Depricated. consider deleting.
    '''
    for indRow, dbRow in celldb.iterrows():
        oneCell = ephyscore.Cell(dbRow)
        if oneCell.get_session_inds('preLowFreq') != [] and oneCell.get_session_inds('preHighFreq') != []:
            figureTotal += 1
    '''
    for indRow, dbRow in celldb.iterrows():
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
        plt.suptitle(f'{oneCell} running vs. nonrunning {figureCount:03d}/{figureTotal:03d}', fontsize=16, fontweight='bold', y = 0.99)



        # Converts the video timestamps into seconds.
        # Adds the value of videoStartDelay to each timestamp.
        runStartHigh, runStopHigh = odbl.convert_videotimes(videoTimes, "salineHighFreq")
        runStartHigh, runStopHigh = [[x + videoStartDelay for x in times] for times in (runStartHigh, runStopHigh)]

        runStartLow, runStopLow = odbl.convert_videotimes(videoTimes, "salineLowFreq")
        runStartLow, runStopLow = [[x + videoStartDelay for x in times] for times in (runStartLow, runStopLow)]


        '''
        runStartDown, runStopDown = odbl.convert_videotimes(videoTimes, "salineFMDown")
        runStartDown, runStopDown = [[x + videoStartDelay for x in times] for times in (runStartDown, runStopDown)]

        runStartUp, runStopUp = odbl.convert_videotimes(videoTimes, "salineFMUp")
        runStartUp, runStopUp = [[x + videoStartDelay for x in times] for times in (runStartUp, runStopUp)]
        '''
        '''
        # Timestamps of running and stopping in video
        runStartHigh = list(np.asarray([133, 298]) + videoStartDelay)
        runStopHigh = list(np.asarray([145, 300]) + videoStartDelay)

        # Timestamps of running and stopping in video
        runStartLow = list(np.asarray([0, 21, 64]) + videoStartDelay)
        runStopLow = list(np.asarray([12, 38, 83 ]) + videoStartDelay)
        '''

        runningBooleanHigh = odbl.create_running_boolean(runStartHigh, runStopHigh, oneCell, 'salineHighFreq')
        runningBooleanLow = odbl.create_running_boolean(runStartLow, runStopLow, oneCell, 'salineLowFreq')

        '''
        runningBooleanDown = odbl.create_running_boolean(runStartDown, runStopDown, oneCell, 'salineFMDown')
        runningBooleanUp = odbl.create_running_boolean(runStartUp, runStopUp, oneCell, 'salineFMUp')
        '''

        '''
        startTrialState = bdata.stateMatrix['statesNames']['startTrial']
        trialStartEvents = (bdata.events['nextState']==startTrialState)
        trialStartTime = bdata.events['eventTime'][trialStartEvents]
        '''

        # Post Saline
        if oneCell.get_session_inds('salineLowFreq') != []:

            (spikeTimesHigh, trialIndexHigh, indexLimitsHigh, LowStd, HighOdd) = odbl.main_function(oneCell, 'salineHighFreq', timeRange)
            (spikeTimesLow, trialIndexLow, indexLimitsLow, LowOdd, HighStd) = odbl.main_function(oneCell, 'salineLowFreq', timeRange)

            # Get standard trials before oddball trials
            trialsBeforeOddLowStd = odbl.trials_before_oddball(HighOdd)       
            trialsBeforeOddHighStd = odbl.trials_before_oddball(LowOdd)
            

            # Combine spike times and index limits of standard and oddball trials.
            (combinedSpikeTimesHigh, combinedIndexLimitsHigh) = odbl.combine_index_limits(spikeTimesLow, spikeTimesHigh, indexLimitsLow, indexLimitsHigh)
            (combinedSpikeTimesLow, combinedIndexLimitsLow) = odbl.combine_index_limits(spikeTimesHigh, spikeTimesLow, indexLimitsHigh, indexLimitsLow)
            
            
            
            # Combine trials of high freq standard before oddball and high freq oddball.
            combinedTrialsHigh = odbl.combine_trials(trialsBeforeOddHighStd, HighOdd)

            # Combine trials of low freq standard before oddball and low freq oddball.
            combinedTrialsLow = odbl.combine_trials(trialsBeforeOddLowStd, LowOdd)

            runningBooleanLow = runningBooleanLow.reshape(-1,1).astype(bool)
            runningBooleanHigh = runningBooleanHigh.reshape(-1,1).astype(bool)
            combinedRunningHigh = odbl.combine_trials(runningBooleanLow, runningBooleanHigh)
            combinedRunningLow = odbl.combine_trials(runningBooleanHigh, runningBooleanLow)

            # Creates a trialsEachCond for the running and nonrunning oddball.
            runningOddballHigh, nonRunningOddballHigh = odbl.seperate_running_trials(combinedTrialsHigh, combinedRunningHigh)
            runningOddballLow, nonRunningOddballLow = odbl.seperate_running_trials(combinedTrialsLow, combinedRunningLow)
    

            # Create spikeCountMat for psth
            spikeCountMatHigh = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeVec)
            spikeCountMatLow = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesLow, combinedIndexLimitsLow, timeVec)



            # Create highFrequencyLabels
            highFreqLabels = odbl.create_labels(combinedTrialsHigh)
            highFreqLabelsRun = odbl.create_labels(runningOddballHigh)
            highFreqLabelsNon = odbl.create_labels(nonRunningOddballHigh)

            # Create lowFrequencyLabels
            lowFreqLabels = odbl.create_labels(combinedTrialsLow)
            lowFreqLabelsRun = odbl.create_labels(runningOddballLow)
            lowFreqLabelsNon = odbl.create_labels(nonRunningOddballLow)


            # Raster plot of high frequency
            colorsEachCond = ['#39b5c4', '#f04158']
            ax0 = plt.subplot(gsOne[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('13kHz Chord - Combined')
            #plt.text(1.05,1.05, f'n {stdTrialLenHigh}')
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
            plt.title('13kHz Chord - Running')
            ax2.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeRange, runningOddballHigh, colorsEachCond, labels= highFreqLabelsRun)
            for p in pRaster:
                p.set_markersize(4)

           
            # PSTH of running trials
            ax3 = plt.subplot(gsTwo[1], sharex=ax2)    
            extraplots.plot_psth(spikeCountMatHigh/binWidth, smoothWinSizePsth, timeVec, runningOddballHigh, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('13kHz (post)')
            plt.legend(("Standard Tone", "Oddball Tone"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)
            

            # Raster plot of nonrunning     
            ax4 = plt.subplot(gsThree[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('13kHz Chord - NonRunning')
            ax4.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeRange, nonRunningOddballHigh, colorsEachCond, labels= highFreqLabelsNon)
            for p in pRaster:
                p.set_markersize(4)

            # PSTH of nonrunning trials
            ax5 = plt.subplot(gsThree[1], sharex=ax4)    
            extraplots.plot_psth(spikeCountMatHigh/binWidth, smoothWinSizePsth, timeVec, nonRunningOddballHigh, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('13kHz (post)')
            plt.legend(("Standard Tone", "Oddball Tone"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)


            # Low Freqency Trials ----------------------------------
            # Raster plot of Low frequency
            colorsEachCond = ['#39b5c4', '#f04158']
            highFreqLabels = ('Standard', "Oddball")
            ax6 = plt.subplot(gsFour[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('8kHz Chord - Combined')
            ax6.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesLow, combinedIndexLimitsLow, timeRange, combinedTrialsLow, colorsEachCond, labels= lowFreqLabels)
            for p in pRaster:
                p.set_markersize(4)

            # PSTH of lowFreq trials
            ax7 = plt.subplot(gsFour[1], sharex=ax6)
            extraplots.plot_psth(spikeCountMatLow/binWidth, smoothWinSizePsth, timeVec, combinedTrialsLow, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('8kHz (post)')
            plt.legend(("Standard Tone", "Oddball Tone"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)


            # Raster plot of running     
            ax8 = plt.subplot(gsFive[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('8kHz Chord - Running')
            ax8.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesLow, combinedIndexLimitsLow, timeRange, runningOddballLow, colorsEachCond, labels= lowFreqLabelsRun)
            for p in pRaster:
                p.set_markersize(4)

           
            # PSTH of running trials
            ax9 = plt.subplot(gsFive[1], sharex=ax8)    
            extraplots.plot_psth(spikeCountMatLow/binWidth, smoothWinSizePsth, timeVec, runningOddballLow, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('13kHz (post)')
            plt.legend(("Standard Tone", "Oddball Tone"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)
            

            # Raster plot of nonrunning     
            ax10 = plt.subplot(gsSix[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('8kHz Chord - NonRunning')
            ax10.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesLow, combinedIndexLimitsLow, timeRange, nonRunningOddballLow, colorsEachCond, labels= lowFreqLabelsNon)
            for p in pRaster:
                p.set_markersize(4)

            # PSTH of nonrunning trials
            ax11 = plt.subplot(gsSix[1], sharex=ax10)    
            extraplots.plot_psth(spikeCountMatLow/binWidth, smoothWinSizePsth, timeVec, nonRunningOddballLow, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('13kHz (post)')
            plt.legend(("Standard Tone", "Oddball Tone"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)








            '''
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

            # Plot Waveform
            ax12 = fig.add_axes([0.9, 0.9, 0.1, 0.1])
            ax12.plot(dbRow.spikeShape, linewidth = 3)
            ax12.axis('off')
            #plt.text(30, -0.1, f"bestChannel = {dbRow.beate}_{dbRow.maxDepth}um_c{dbRow.cluster}_combined_report.png'
            #fileName = os.path.join(figDirectory, figName)

            plt.gcf().set_size_inches([16, 9])
            #plt.gcf().set_dpi(100)

            #mng = plt.get_current_fig_manager()
            #mng.full_screen_toggle()
            #plt.show()
            figDirectory = os.path.join(settings.FIGURES_DATA_PATH, f'{subject}/FM_running_compare/saline')
            if not os.path.exists(figDirectory):
                os.makedirs(figDirectory)
            figName= f'{figureCount:03d}_{subject}_{dbRow.date}_{dbRow.maxDepth}um_c{dbRow.cluster}_running_report.png'
            fileName = os.path.join(figDirectory, figName)


            plt.savefig(fileName, format='png')
            print(f'saving image {figName}')
            figureCount+=1
    
            if oneFigure == True:
                sys.exit()
            
            plt.close()
    print("done")




