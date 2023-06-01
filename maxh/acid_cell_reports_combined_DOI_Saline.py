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
celldb = celldb.query("date == '2023-05-30'")
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
        gsMain = gs.GridSpec(3, 4, figure=fig)
        gsOne = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[0])
        gsTwo = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[1])
        gsThree = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[2])
        gsFour = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[3])
        gsFive = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[4])
        gsSix = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[5])
        gsSeven = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[6])
        gsEight = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[7])
        gsNine = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[8])
        gsTen = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[9])
        gsEleven = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[10])
        gsTwelve = gs.GridSpecFromSubplotSpec(2, 1, subplot_spec = gsMain[11])
        plt.subplots_adjust(hspace=0.10)
        gsMain.update(top=0.9, bottom=0.1, wspace=0.45, hspace=0.45) #Change spacing of things (left=0.075, right=0.98) 

        
        # Title of image
        plt.suptitle(f'{oneCell} combined {figureCount:03d}/{figureTotal:03d}', fontsize=16, fontweight='bold', y = 0.99)
        



        # lowFreq = the low frequency is the oddball
        
        # Pre Injection

        

        if oneCell.get_session_inds('preHighFreq') != []:
            (combinedSpikeTimesHighPre, combinedSpikeTimesLowPre, combinedIndexLimitsHighPre, combinedIndexLimitsLowPre, combinedTrialsHighPre, combinedTrialsLowPre, spikeCountMatHighPre, spikeCountMatLowPre ) = max.prepare_plots(oneCell, timeRange, 'preHighFreq', 'preLowFreq', timeVec)
            
            # Raster plot of high frequency
            colorsEachCond = ['#39b5c4', '#f04158']
            highFreqLabels = ('Standard', "Oddball")
            ax1 = plt.subplot(gsOne[0])
            # plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('13kHz Chord (pre)')
            ax1.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesHighPre, combinedIndexLimitsHighPre, timeRange, combinedTrialsHighPre, colorsEachCond, labels= highFreqLabels)
            for p in pRaster:
                p.set_markersize(4)

            # PSTH of highFreq trials
            ax2 = plt.subplot(gsOne[1], sharex=ax1)    
            extraplots.plot_psth(spikeCountMatHighPre/binWidth, smoothWinSizePsth, timeVec, combinedTrialsHighPre, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('13kHz (pre)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)


            # Raster plot of low frequency        
            ax3 = plt.subplot(gsTwo[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('8kHz Chord (pre)')
            ax3.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesLowPre, combinedIndexLimitsLowPre, timeRange, combinedTrialsLowPre, colorsEachCond, labels= highFreqLabels)
            for p in pRaster:
                p.set_markersize(4)

            # PSTH of lowFreq trials
            ax4 = plt.subplot(gsTwo[1], sharex=ax3)    
            extraplots.plot_psth(spikeCountMatLowPre/binWidth, smoothWinSizePsth, timeVec, combinedTrialsLowPre, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('8kHz (pre)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)
                #plt.legend(("Standard Tone", "Oddball Tone"))

        if oneCell.get_session_inds('preFM_Up') != []: #and oneCell.get_session_inds('lowFreq') != []:

            (combinedSpikeTimesDownPre, combinedSpikeTimesUpPre, combinedIndexLimitsDownPre, combinedIndexLimitsUpPre, combinedTrialsDownPre, combinedTrialsUpPre, spikeCountMatDownPre, spikeCountMatUpPre ) = max.prepare_plots(oneCell, timeRange, 'preFM_Down', 'preFM_Up', timeVec)


            # Raster plot of Down Sweep
            colorsEachCond = ['#39b5c4', '#f04158']
            highFreqLabels = ('Standard', "Oddball")
            ax5 = plt.subplot(gsThree[0])
            # plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('FM Down Sweep(pre)')
            ax5.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesDownPre, combinedIndexLimitsDownPre, timeRange, combinedTrialsDownPre, colorsEachCond, labels= highFreqLabels)
            for p in pRaster:
                p.set_markersize(4)

            # PSTH of Down Sweep trials
            ax6 = plt.subplot(gsThree[1], sharex=ax5)    
            extraplots.plot_psth(spikeCountMatDownPre/binWidth, smoothWinSizePsth, timeVec, combinedTrialsDownPre, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('13kHz (pre)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)


            # Raster plot of Up Sweep        
            ax7 = plt.subplot(gsFour[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('FM Up Sweep(pre)')
            ax7.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesUpPre, combinedIndexLimitsUpPre, timeRange, combinedTrialsUpPre, colorsEachCond, labels= highFreqLabels)
            for p in pRaster:
                p.set_markersize(4)

            # PSTH of lowFreq trials
            ax8 = plt.subplot(gsFour[1], sharex=ax7)    
            extraplots.plot_psth(spikeCountMatUpPre/binWidth, smoothWinSizePsth, timeVec, combinedTrialsUpPre, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('8kHz (pre)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)
            #plt.legend(("Standard Tone", "Oddball Tone"))
        
        
        # Post Saline
        if oneCell.get_session_inds('salineLowFreq') != []:
            (combinedSpikeTimesHighSaline, combinedSpikeTimesLowSaline, combinedIndexLimitsHighSaline, combinedIndexLimitsLowSaline, combinedTrialsHighSaline, combinedTrialsLowSaline, spikeCountMatHighSaline, spikeCountMatLowSaline ) = max.prepare_plots(oneCell, timeRange, 'salineHighFreq', 'salineLowFreq', timeVec)

            # Raster plot of high frequency
            colorsEachCond = ['#39b5c4', '#f04158']
            highFreqLabels = ('Standard', "Oddball")
            ax9 = plt.subplot(gsFive[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('13kHz Chord(saline)')
            ax9.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesHighSaline, combinedIndexLimitsHighSaline, timeRange, combinedTrialsHighSaline, colorsEachCond, labels= highFreqLabels)
            for p in pRaster:
                p.set_markersize(4)

            # PSTH of highFreq trials (may not need spikeCountMatHigh)
            ax10 = plt.subplot(gsFive[1], sharex=ax9)    
            extraplots.plot_psth(spikeCountMatHighSaline/binWidth, smoothWinSizePsth, timeVec, combinedTrialsHighSaline, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('8kHz (post)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)


            # Raster plot of low frequency        
            ax11 = plt.subplot(gsSix[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('8kHz Chord (saline)')
            ax11.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesLowSaline, combinedIndexLimitsLowSaline, timeRange, combinedTrialsLowSaline, colorsEachCond, labels= highFreqLabels)
            for p in pRaster:
                p.set_markersize(4)

            # PSTH of lowFreq trials
            ax12 = plt.subplot(gsSix[1], sharex=ax11)    
            extraplots.plot_psth(spikeCountMatLowSaline/binWidth, smoothWinSizePsth, timeVec, combinedTrialsLowSaline, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('13kHz (post)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)


        if oneCell.get_session_inds('salineFM_Up') != []:
            (combinedSpikeTimesDownSaline, combinedSpikeTimesUpSaline, combinedIndexLimitsDownSaline, combinedIndexLimitsUpSaline, combinedTrialsDownSaline, combinedTrialsUpSaline, spikeCountMatDownSaline, spikeCountMatUpSaline ) = max.prepare_plots(oneCell, timeRange, 'salineFM_Down', 'salineFM_Up', timeVec)

            # Raster plot of Down Sweep
            colorsEachCond = ['#39b5c4', '#f04158']
            highFreqLabels = ('Standard', "Oddball")
            ax13 = plt.subplot(gsSeven[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('FM Down Sweep(saline)')
            ax13.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesDownSaline, combinedIndexLimitsDownSaline, timeRange, combinedTrialsDownSaline, colorsEachCond, labels= highFreqLabels)
            for p in pRaster:
                p.set_markersize(4)

            # PSTH of Down Sweep trials
            ax14 = plt.subplot(gsSeven[1], sharex=ax13)    
            extraplots.plot_psth(spikeCountMatDownSaline/binWidth, smoothWinSizePsth, timeVec, combinedTrialsDownSaline, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('8kHz (post)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)


            # Raster plot of Up Sweep        
            ax15 = plt.subplot(gsEight[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('FM Up Sweep(saline)')
            ax15.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesUpSaline, combinedIndexLimitsUpSaline, timeRange, combinedTrialsUpSaline, colorsEachCond, labels= highFreqLabels)
            for p in pRaster:
                p.set_markersize(4)

            # PSTH of Up Sweep trials
            ax16 = plt.subplot(gsEight[1], sharex=ax15)    
            extraplots.plot_psth(spikeCountMatUpSaline/binWidth, smoothWinSizePsth, timeVec, combinedTrialsUpSaline, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('13kHz (post)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)            
            

        # Post DOI
        if oneCell.get_session_inds('doiLowFreq') != []:
            (combinedSpikeTimesHighDoi, combinedSpikeTimesLowDoi, combinedIndexLimitsHighDoi, combinedIndexLimitsLowDoi, combinedTrialsHighDoi, combinedTrialsLowDoi, spikeCountMatHighDoi, spikeCountMatLowDoi ) = max.prepare_plots(oneCell, timeRange, 'doiHighFreq', 'doiLowFreq', timeVec)

            # Raster plot of high frequency
            colorsEachCond = ['#39b5c4', '#f04158']
            highFreqLabels = ('Standard', "Oddball")
            ax17 = plt.subplot(gsNine[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('13kHz Chord (DOI)')
            ax17.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesHighDoi, combinedIndexLimitsHighDoi, timeRange, combinedTrialsHighDoi, colorsEachCond, labels= highFreqLabels)
            for p in pRaster:
                p.set_markersize(4)

            # PSTH of highFreq trials (may not need spikeCountMatHigh)
            ax18 = plt.subplot(gsNine[1], sharex=ax17)    
            extraplots.plot_psth(spikeCountMatHighDoi/binWidth, smoothWinSizePsth, timeVec, combinedTrialsHighDoi, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('8kHz (post)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)


            # Raster plot of low frequency        
            ax19 = plt.subplot(gsTen[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('8kHz Chord (DOI)')
            ax19.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesLowDoi, combinedIndexLimitsLowDoi, timeRange, combinedTrialsLowDoi, colorsEachCond, labels= highFreqLabels)
            for p in pRaster:
                p.set_markersize(4)
                
            # PSTH of lowFreq trials
            ax20 = plt.subplot(gsTen[1], sharex=ax19)    
            extraplots.plot_psth(spikeCountMatLowDoi/binWidth, smoothWinSizePsth, timeVec, combinedTrialsLowDoi, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('13kHz (post)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)


        if oneCell.get_session_inds('doiFM_Up') != []:
            (combinedSpikeTimesDownDoi, combinedSpikeTimesUpDoi, combinedIndexLimitsDownDoi, combinedIndexLimitsUpDoi, combinedTrialsDownDoi, combinedTrialsUpDoi, spikeCountMatDownDoi, spikeCountMatUpDoi ) = max.prepare_plots(oneCell, timeRange, 'doiFM_Down', 'doiFM_Up', timeVec)

            # Raster plot of Down Sweep
            colorsEachCond = ['#39b5c4', '#f04158']
            highFreqLabels = ('Standard', "Oddball")
            ax21 = plt.subplot(gsEleven[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('FM Down Sweep(DOI)')
            ax21.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesDownDoi, combinedIndexLimitsDownDoi, timeRange, combinedTrialsDownDoi, colorsEachCond, labels= highFreqLabels)
            for p in pRaster:
                p.set_markersize(4)

            # PSTH of Down Sweep trials 
            ax22 = plt.subplot(gsEleven[1], sharex=ax21)    
            extraplots.plot_psth(spikeCountMatDownDoi/binWidth, smoothWinSizePsth, timeVec, combinedTrialsDownDoi, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('8kHz (post)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)


            # Raster plot of Up Sweep        
            ax23 = plt.subplot(gsTwelve[0])
            #plt.xlabel('Time (s)')
            plt.ylabel('Trials')
            plt.title('FM Up Sweep(DOI)')
            ax23.tick_params(labelbottom=False) 
            pRaster, hcond, zline = extraplots.raster_plot(combinedSpikeTimesUpDoi, combinedIndexLimitsUpDoi, timeRange, combinedTrialsUpDoi, colorsEachCond, labels= highFreqLabels)
            for p in pRaster:
                p.set_markersize(4)

            # PSTH of Up Sweep trials
            ax24 = plt.subplot(gsTwelve[1], sharex=ax23)    
            extraplots.plot_psth(spikeCountMatUpDoi/binWidth, smoothWinSizePsth, timeVec, combinedTrialsUpDoi, colorsEachCond, linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
            plt.xlabel('Time (s)')
            plt.ylabel('Firing Rate')
            #plt.title('13kHz (post)')
            plt.legend(("Standard", "Oddball"), bbox_to_anchor=(-0.20, -0.20), loc = 'upper left', fontsize = 8)


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


            
            # Plot Waveform
            ax0 = fig.add_axes([0.9, 0.9, 0.1, 0.1])
            ax0.plot(dbRow.spikeShape, linewidth = 3)
            #plt.text(30, -0.1, f"bestChannel = {dbRow.bestChannel}")
            ax0.axis('off')
   

            plt.gcf().set_size_inches([16, 9])
            #plt.gcf().set_dpi(100)

            #mng = plt.get_current_fig_manager()
            #mng.full_screen_toggle()
            #plt.show()
            figDirectory = os.path.join(settings.FIGURES_DATA_PATH, f'{subject}/{dbRow.date}/combined/' 'cell_reports')
            if not os.path.exists(figDirectory):
                os.makedirs(figDirectory)
            figName= f'{figureCount:03d}_{subject}_{dbRow.date}_{dbRow.maxDepth}um_c{dbRow.cluster}_combined_report.png'
            fileName = os.path.join(figDirectory, figName)

            plt.savefig(fileName, format='png')
            print(f'saving image {figName}')
            figureCount+=1
       
            if oneFigure == True:
                sys.exit()
            
            plt.close()
    print("done")




