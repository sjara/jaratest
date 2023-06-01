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

subject = 'acid007'

# Set to True if want to load one cell. Defaults to loading first cell unless cellDict is complete.
oneFigure = False

# Add info for loading a specific cell.
cellDict = {'subject' : '',
            'date' : '2023-03-19',
            'pdepth' : 3000,
            'egroup' : 1,
            'cluster' : 120}


inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
dbPath = os.path.join(settings.DATABASE_PATH ,f'celldb_{subject}.h5')

celldb = celldatabase.generate_cell_database(inforecFile)
# Used to load specific recording session dates.
celldb = celldb.query("date == '2023-05-17'")
figureCount = 1
figureTotal = 0

timeRange = [-0.3, 0.45]


for indRow, dbRow in celldb.iterrows():
    oneCell = ephyscore.Cell(dbRow)
    if oneCell.get_session_inds('preLowFreq') != [] and oneCell.get_session_inds('preHighFreq') != []:
            figureTotal += 1

for indRow, dbRow in celldb.iterrows():
    #plt.clf()

    oneCell = ephyscore.Cell(dbRow)

    gsMain = gs.GridSpec(1,3)
    plt.subplots_adjust(hspace=0.10)
    gsMain.update(top=0.9, bottom=0.1, wspace=0.45, hspace=0.45) #Change spacing of things (left=0.075, right=0.98) 
    # Title of image
    plt.suptitle(f'{oneCell} frequency tuning {figureCount}/{figureTotal}', fontsize=16, fontweight='bold', y = 0.99)


    if oneCell.get_session_inds('prePureTones') != []:

        ephysData, bdata = oneCell.load('prePureTones')  
        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['stimOn']
        #eventOnsetTimes = eventOnsetTimes[:-1]

        frequencies_each_trial = bdata['currentFreq']

        if (len(frequencies_each_trial) > len(eventOnsetTimes)) or (len(frequencies_each_trial) < len(eventOnsetTimes)-1):
            print(f'Warning! BevahTrials ({len(frequencies_each_trial)}) and ' + f'EphysTrials ({len(eventOnsetTimes)})')
            sys.exit()

        if len(frequencies_each_trial) == len(eventOnsetTimes)-1:
            eventOnsetTimes = eventOnsetTimes[:len(frequencies_each_trial)]

        (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

        array_of_frequencies = np.unique(frequencies_each_trial)
        trialsEachCond = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)



        PTlabels = list(np.rint(array_of_frequencies))

        # Raster plot of high frequency
        ax1 = plt.subplot(gsMain[0])
        plt.xlabel('Time (s)')
        #plt.ylabel('Trials')
        plt.title('Pre Injection')
        ax1.tick_params(labelbottom=False)

        '''
        # Generate an array of 16 equally spaced numbers between 0 and 1
        numbers = np.linspace(0, 1, 16)

        # Generate a colormap that maps the numbers to colors
        cmap = plt.get_cmap('tab20')

        # Use the colormap to map the numbers to colors
        colors = [cmap(x) for x in numbers]
        '''


        pRaster = extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange, trialsEachCond, labels = PTlabels)

    if oneCell.get_session_inds('salinePureTones') != []:

        ephysData, bdata = oneCell.load('salinePureTones')  
        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['stimOn']
        #eventOnsetTimes = eventOnsetTimes[:-1]

        frequencies_each_trial = bdata['currentFreq']

        if (len(frequencies_each_trial) > len(eventOnsetTimes)) or (len(frequencies_each_trial) < len(eventOnsetTimes)-1):
            print(f'Warning! BevahTrials ({len(frequencies_each_trial)}) and ' + f'EphysTrials ({len(eventOnsetTimes)})')
            sys.exit()

        if len(frequencies_each_trial) == len(eventOnsetTimes)-1:
            eventOnsetTimes = eventOnsetTimes[:len(frequencies_each_trial)]

        (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

        array_of_frequencies = np.unique(frequencies_each_trial)
        trialsEachCond = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)


        PTlabels = list(np.rint(array_of_frequencies))

        # Raster plot of high frequency
        ax2 = plt.subplot(gsMain[1])
        # plt.xlabel('Time (s)')
        #plt.ylabel('Trials')
        plt.title('Saline Injection')
        ax1.tick_params(labelbottom=False)

        # Generate an array of 16 equally spaced numbers between 0 and 1
        numbers = np.linspace(0, 1, 16)

        # Generate a colormap that maps the numbers to colors
        cmap = plt.get_cmap('tab20')

        # Use the colormap to map the numbers to colors
        colors = [cmap(x) for x in numbers]



        pRaster = extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange, trialsEachCond, labels = PTlabels)


    if oneCell.get_session_inds('doiPureTones') != []:

        ephysData, bdata = oneCell.load('doiPureTones')  
        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['stimOn']
        #eventOnsetTimes = eventOnsetTimes[:-1]

        frequencies_each_trial = bdata['currentFreq']

        if (len(frequencies_each_trial) > len(eventOnsetTimes)) or (len(frequencies_each_trial) < len(eventOnsetTimes)-1):
            print(f'Warning! BevahTrials ({len(frequencies_each_trial)}) and ' + f'EphysTrials ({len(eventOnsetTimes)})')
            sys.exit()

        if len(frequencies_each_trial) == len(eventOnsetTimes)-1:
            eventOnsetTimes = eventOnsetTimes[:len(frequencies_each_trial)]

        (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

        array_of_frequencies = np.unique(frequencies_each_trial)
        trialsEachCond = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)


        PTlabels = list(np.rint(array_of_frequencies))

        # Raster plot of high frequency
        ax3 = plt.subplot(gsMain[2])
        # plt.xlabel('Time (s)')
        #plt.ylabel('Trials')
        plt.title('DOI Injection')
        ax1.tick_params(labelbottom=False)

        # Generate an array of 16 equally spaced numbers between 0 and 1
        numbers = np.linspace(0, 1, 16)

        # Generate a colormap that maps the numbers to colors
        cmap = plt.get_cmap('tab20')

        # Use the colormap to map the numbers to colors
        colors = [cmap(x) for x in numbers]



        pRaster = extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange, trialsEachCond, labels = PTlabels)

        plt.gcf().set_size_inches([16, 9])
        #plt.gcf().set_dpi(100)

        #mng = plt.get_current_fig_manager()
        #mng.full_screen_toggle()
        #plt.show()
        figDirectory = os.path.join(settings.FIGURES_DATA_PATH, f'{subject}/{dbRow.date}/combined/' 'freq_tuning')
        if not os.path.exists(figDirectory):
            os.makedirs(figDirectory)
        figName= f'{figureCount}_{subject}_{dbRow.date}_{dbRow.maxDepth}um_c{dbRow.cluster}_combined_freqTuning.png'
        fileName = os.path.join(figDirectory, figName)

        plt.savefig(fileName, format='png')
        print(f'saving image {figName}')
        figureCount+=1
    
        if oneFigure == True:
            sys.exit()
        
        plt.close()
print("done")



    
