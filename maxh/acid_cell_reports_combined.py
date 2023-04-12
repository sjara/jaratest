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

subject = 'inpi002'

# Set to True if want to load one cell. Defaults to loading first cell unless cellDict is complete.
oneFigure = False

# Add info for loading a specific cell.
cellDict = {'subject' : '',
            'date' : '',
            'pdepth' : 1250,
            'egroup' : 0,
            'cluster' : 4}


inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
dbPath = os.path.join(settings.DATABASE_PATH ,f'celldb_{subject}.h5')

celldb = celldatabase.generate_cell_database(inforecFile)
# Used to load specific recording session dates.
celldb = celldb.query("date == '2023-03-23'")
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
        plt.clf()

        oneCell = ephyscore.Cell(dbRow)


        gsMain = gs.GridSpec(2, 4)
        gsOne = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[0])
        gsTwo = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[1])
        gsThree = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[2])
        gsFour = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[3])
        gsFive = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[4])
        gsSix = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[5])
        gsSeven = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[6])
        gsEight = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[7])
        plt.subplots_adjust(hspace=0.10)
        gsMain.update(top=0.9, bottom=0.1, wspace=0.45, hspace=0.45) #Change spacing of things (left=0.075, right=0.98) 

        
        # Title of image
        plt.suptitle(f'{oneCell} pureTones {figureCount}/{figureTotal}', fontsize=16, fontweight='bold', y = 0.99)
        

        # Plot Waveform

        
    #     ax0 = gsMain.fig.add_subplot(111)
    #    # ax0 = plt.add_axes([0.1, 0.7, 0.8, 0.2])
    #     ax0.plot(dbRow.spikeShape, linewidth = 3)
    #     #plt.text(30, -0.1, f"bestChannel = {dbRow.bestChannel}")
    #     ax0.set_position([0.1, 0.6, 0.2, 0.2])

        # lowFreq = the low frequency is the oddball
        
        # Pre Injection
        if oneCell.get_session_inds('preLowFreq') != []: #and oneCell.get_session_inds('lowFreq') != []:
            # Load session, lock spikes to event, seperate trials into columns.
            (spikeTimesLowPre, trialIndexLowPre, indexLimitsLowPre, preLowOdd, preHighStd) = max.main_function(oneCell, 'preLowFreq', timeRange)
            (spikeTimesHighPre, trialIndexHighPre, indexLimitsHighPre, preLowStd, preHighOdd) = max.main_function(oneCell, 'preHighFreq', timeRange)

            # Get standard trials before oddball trials       
            trialsBeforeOddHighStd = max.trials_before_oddball(preLowOdd)
            trialsBeforeOddLowStd = max.trials_before_oddball(preHighOdd)

            # Combine spike times and index limits of standard and oddball trials.
            (combinedSpikeTimesHigh, combinedIndexLimitsHigh) = max.combine_index_limits(spikeTimesLowPre, spikeTimesHighPre, indexLimitsLowPre, indexLimitsHighPre)
            (combinedSpikeTimesLow, combinedIndexLimitsLow) = max.combine_index_limits(spikeTimesHighPre, spikeTimesLowPre, indexLimitsHighPre, indexLimitsLowPre)
            
            # Combine trials of high freq before oddball and high freq oddball.
            combinedTrialsHigh = max.combine_trials(trialsBeforeOddHighStd, preHighOdd)

            # Combine trials of low freq before oddball and low freq oddball.
            combinedTrialsLow = max.combine_trials(trialsBeforeOddLowStd, preLowOdd)

            # Create spikeCountMat for pre injection
            spikeCountMatPreHigh = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeVec)
            spikeCountMatPreLow = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesLow, combinedIndexLimitsLow, timeVec)


            # Raster plot of high frequency
            colorsEachCond = ['#39b5c4', '#f04158']
            highFreqLabels = ('Standard', "Oddball")
            ax1 = plt.subplot(gsOne[0])
            # plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('13kHz Tone (pre)')
            ax1.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeRange, combinedTrialsHigh, colorsEachCond, labels= highFreqLabels)

            # PSTH of highFreq trials
            ax2 = plt.subplot(gsOne[1], sharex=ax1)    
            extraplots.plot_psth(spikeCountMatPreHigh/binWidth, smoothWinSizePsth, timeVec, combinedTrialsHigh, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('13kHz (pre)')
            plt.legend(("Standard Tone", "Oddball Tone"), bbox_to_anchor=(0, -0.20), loc = 'upper left', fontsize = 8)


            # Raster plot of low frequency        
            ax3 = plt.subplot(gsTwo[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('8kHz Tone (pre)')
            ax3.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesLow, combinedIndexLimitsLow, timeRange, combinedTrialsLow, colorsEachCond, labels= highFreqLabels)

            # PSTH of lowFreq trials
            ax3 = plt.subplot(gsTwo[1], sharex=ax3)    
            extraplots.plot_psth(spikeCountMatPreLow/binWidth, smoothWinSizePsth, timeVec, combinedTrialsLow, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('8kHz (pre)')
            plt.legend(("Standard Tone", "Oddball Tone"), bbox_to_anchor=(0, -0.20), loc = 'upper left', fontsize = 8)
            #plt.legend(("Standard Tone", "Oddball Tone"))

        if oneCell.get_session_inds('preFM_Up') != []: #and oneCell.get_session_inds('lowFreq') != []:
            # Load session, lock spikes to event, seperate trials into columns.
            (spikeTimesLowPre, trialIndexLowPre, indexLimitsLowPre, preLowOdd, preHighStd) = max.main_function(oneCell, 'preFM_Up', timeRange)
            (spikeTimesHighPre, trialIndexHighPre, indexLimitsHighPre, preLowStd, preHighOdd) = max.main_function(oneCell, 'preFM_Down', timeRange)

            # Get standard trials before oddball trials       
            trialsBeforeOddHighStd = max.trials_before_oddball(preLowOdd)
            trialsBeforeOddLowStd = max.trials_before_oddball(preHighOdd)

            # Combine spike times and index limits of standard and oddball trials.
            (combinedSpikeTimesHigh, combinedIndexLimitsHigh) = max.combine_index_limits(spikeTimesLowPre, spikeTimesHighPre, indexLimitsLowPre, indexLimitsHighPre)
            (combinedSpikeTimesLow, combinedIndexLimitsLow) = max.combine_index_limits(spikeTimesHighPre, spikeTimesLowPre, indexLimitsHighPre, indexLimitsLowPre)
            
            # Combine trials of high freq before oddball and high freq oddball.
            combinedTrialsHigh = max.combine_trials(trialsBeforeOddHighStd, preHighOdd)

            # Combine trials of low freq before oddball and low freq oddball.
            combinedTrialsLow = max.combine_trials(trialsBeforeOddLowStd, preLowOdd)

            # Create spikeCountMat for pre injection
            spikeCountMatPreHigh = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeVec)
            spikeCountMatPreLow = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesLow, combinedIndexLimitsLow, timeVec)


            # Raster plot of high frequency
            colorsEachCond = ['#39b5c4', '#f04158']
            highFreqLabels = ('Standard', "Oddball")
            ax1 = plt.subplot(gsThree[0])
            # plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('FM Down Sweep(pre)')
            ax1.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeRange, combinedTrialsHigh, colorsEachCond, labels= highFreqLabels)

            # PSTH of highFreq trials
            ax2 = plt.subplot(gsThree[1], sharex=ax1)    
            extraplots.plot_psth(spikeCountMatPreHigh/binWidth, smoothWinSizePsth, timeVec, combinedTrialsHigh, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('13kHz (pre)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(0, -0.20), loc = 'upper left', fontsize = 8)


            # Raster plot of low frequency        
            ax3 = plt.subplot(gsFour[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('FM Up Sweep(pre)')
            ax3.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesLow, combinedIndexLimitsLow, timeRange, combinedTrialsLow, colorsEachCond, labels= highFreqLabels)

            # PSTH of lowFreq trials
            ax3 = plt.subplot(gsFour[1], sharex=ax3)    
            extraplots.plot_psth(spikeCountMatPreLow/binWidth, smoothWinSizePsth, timeVec, combinedTrialsLow, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('8kHz (pre)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(0, -0.20), loc = 'upper left', fontsize = 8)
            #plt.legend(("Standard Tone", "Oddball Tone"))
        
        
        # Post Injection
        if oneCell.get_session_inds('postLowFreq') != []:
            # Load session, lock spikes to event, seperate trials into columns.
            (spikeTimesHighPost, trialIndexHighPost, indexLimitsHighPost, postLowStd, postHighOdd) = max.main_function(oneCell, 'postHighFreq', timeRange)
            (spikeTimesLowPost, trialIndexLowPost, indexLimitsLowPost, postLowOdd, postHighStd) = max.main_function(oneCell, 'postLowFreq', timeRange)
            

            # Get standard trials before oddball trials
            trialsBeforeOddLowStdPost = max.trials_before_oddball(postHighOdd)       
            trialsBeforeOddHighStdPost = max.trials_before_oddball(postLowOdd)
            

            # Combine spike times and index limits of standard and oddball trials.
            (combinedSpikeTimesPostHigh, combinedIndexLimitsPostHigh) = max.combine_index_limits(spikeTimesLowPost, spikeTimesHighPost, indexLimitsLowPost, indexLimitsHighPost)
            (combinedSpikeTimesPostLow, combinedIndexLimitsPostLow) = max.combine_index_limits(spikeTimesHighPost, spikeTimesLowPost, indexLimitsHighPost, indexLimitsLowPost)
            
            
            
            # Combine trials of high freq before oddball and high freq oddball.
            combinedTrialsHighPost = max.combine_trials(trialsBeforeOddHighStdPost, postHighOdd)

            # Combine trials of low freq before oddball and low freq oddball.
            combinedTrialsLowPost = max.combine_trials(trialsBeforeOddLowStdPost, postLowOdd)

            # Create spikeCountMat for Post injection.
            spikeCountMatPostHigh = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesPostHigh, combinedIndexLimitsPostHigh, timeVec)
            spikeCountMatPostLow = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesPostLow, combinedIndexLimitsPostLow, timeVec)


            # Raster plot of high frequency
            colorsEachCond = ['#39b5c4', '#f04158']
            highFreqLabels = ('Standard', "Oddball")
            ax5 = plt.subplot(gsFive[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('13kHz Tone (post)')
            ax5.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesPostHigh, combinedIndexLimitsPostHigh, timeRange, combinedTrialsHighPost, colorsEachCond, labels= highFreqLabels)

            # PSTH of highFreq trials (may not need spikeCountMatHigh)
            ax6 = plt.subplot(gsFive[1], sharex=ax5)    
            extraplots.plot_psth(spikeCountMatPostHigh/binWidth, smoothWinSizePsth, timeVec, combinedTrialsHighPost, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('8kHz (post)')
            plt.legend(("Standard Tone", "Oddball Tone"), bbox_to_anchor=(0, -0.20), loc = 'upper left', fontsize = 8)


            # Raster plot of low frequency        
            ax7 = plt.subplot(gsSix[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('8kHz Tone (post)')
            ax7.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesPostLow, combinedIndexLimitsPostLow, timeRange, combinedTrialsLowPost, colorsEachCond, labels= highFreqLabels)

            # PSTH of lowFreq trials
            ax8 = plt.subplot(gsSix[1], sharex=ax7)    
            extraplots.plot_psth(spikeCountMatPostLow/binWidth, smoothWinSizePsth, timeVec, combinedTrialsLowPost, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('13kHz (post)')
            plt.legend(("Standard Tone", "Oddball Tone"), bbox_to_anchor=(0, -0.20), loc = 'upper left', fontsize = 8)


        if oneCell.get_session_inds('postFM_Up') != []:
            # Load session, lock spikes to event, seperate trials into columns.
            (spikeTimesLowPost, trialIndexLowPost, indexLimitsLowPost, postLowOdd, postHighStd) = max.main_function(oneCell, 'postFM_Up', timeRange)
            (spikeTimesHighPost, trialIndexHighPost, indexLimitsHighPost, postLowStd, postHighOdd) = max.main_function(oneCell, 'postFM_Down', timeRange)
            

            # Get standard trials before oddball trials
            trialsBeforeOddLowStdPost = max.trials_before_oddball(postHighOdd)       
            trialsBeforeOddHighStdPost = max.trials_before_oddball(postLowOdd)
            

            # Combine spike times and index limits of standard and oddball trials.
            (combinedSpikeTimesPostHigh, combinedIndexLimitsPostHigh) = max.combine_index_limits(spikeTimesLowPost, spikeTimesHighPost, indexLimitsLowPost, indexLimitsHighPost)
            (combinedSpikeTimesPostLow, combinedIndexLimitsPostLow) = max.combine_index_limits(spikeTimesHighPost, spikeTimesLowPost, indexLimitsHighPost, indexLimitsLowPost)
            
            
            
            # Combine trials of high freq before oddball and high freq oddball.
            combinedTrialsHighPost = max.combine_trials(trialsBeforeOddHighStdPost, postHighOdd)

            # Combine trials of low freq before oddball and low freq oddball.
            combinedTrialsLowPost = max.combine_trials(trialsBeforeOddLowStdPost, postLowOdd)

            # Create spikeCountMat for Post injection.
            spikeCountMatPostHigh = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesPostHigh, combinedIndexLimitsPostHigh, timeVec)
            spikeCountMatPostLow = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesPostLow, combinedIndexLimitsPostLow, timeVec)


            # Raster plot of high frequency
            colorsEachCond = ['#39b5c4', '#f04158']
            highFreqLabels = ('Standard', "Oddball")
            ax5 = plt.subplot(gsSeven[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('FM Down Sweep(post)')
            ax5.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesPostHigh, combinedIndexLimitsPostHigh, timeRange, combinedTrialsHighPost, colorsEachCond, labels= highFreqLabels)

            # PSTH of highFreq trials (may not need spikeCountMatHigh)
            ax6 = plt.subplot(gsSeven[1], sharex=ax5)    
            extraplots.plot_psth(spikeCountMatPostHigh/binWidth, smoothWinSizePsth, timeVec, combinedTrialsHighPost, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('8kHz (post)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(0, -0.20), loc = 'upper left', fontsize = 8)


            # Raster plot of low frequency        
            ax7 = plt.subplot(gsEight[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('FM Up Sweep(post)')
            ax7.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesPostLow, combinedIndexLimitsPostLow, timeRange, combinedTrialsLowPost, colorsEachCond, labels= highFreqLabels)

            # PSTH of lowFreq trials
            ax8 = plt.subplot(gsEight[1], sharex=ax7)    
            extraplots.plot_psth(spikeCountMatPostLow/binWidth, smoothWinSizePsth, timeVec, combinedTrialsLowPost, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('13kHz (post)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(0, -0.20), loc = 'upper left', fontsize = 8)            
            
            plt.gcf().set_size_inches([16, 9])
            #plt.gcf().set_dpi(100)

            #mng = plt.get_current_fig_manager()
            #mng.full_screen_toggle()
            plt.show()
            figDirectory = os.path.join(settings.FIGURES_DATA_PATH, f'{subject}/pureTones/' 'cell_reports')
            if not os.path.exists(figDirectory):
                os.makedirs(figDirectory)
            figName= f'{figureCount}_{subject}_{dbRow.date}_{dbRow.maxDepth}um_c{dbRow.cluster}_pureTones_report.png'
            fileName = os.path.join(figDirectory, figName)

            #plt.savefig(fileName, format='png')
            print(f'saving image {figName}')
            figureCount+=1
            
            if oneFigure == True:
                sys.exit()
            
            plt.close()
    print("done")




