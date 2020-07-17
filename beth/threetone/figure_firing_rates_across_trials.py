import os
import sys
import importlib
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
import studyparams

importlib.reload(studyparams)

#dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
dbPath = settings.FIGURES_DATA_PATH

# -- Database file name --
dbFilename = os.path.join(dbPath,'newresponsivedb_{}_A.h5'.format(studyparams.STUDY_NAME))
#dbFilename = os.path.join(dbPath,'newresponsivedb_{}_D.h5'.format(studyparams.STUDY_NAME))

# -- Load the database of cells --
responsivedb = celldatabase.load_hdf(dbFilename)

# -- Variables --
timeRange = [-0.05, 0.2]  # In seconds
binWidth = 0.010
timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
smoothWinSizePsth = 2
lwPsth = 2
downsampleFactorPsth = 1

def sequential_firing_rates_after_oddballs(celldb):
    #for indRow,dbRow in celldb.iterrows():
    for indRow,dbRow in celldb[124:125].iterrows():

        plt.clf()
        ax = plt.subplot2grid((1,10), (0,0)) # Subplots
        plt.box(False)

        oneCell = ephyscore.Cell(dbRow)
        ephysData, bdata = oneCell.load('ascending')
        #if oneCell.get_session_inds('ascending') != []:
              #try:
                  #ephysDataA, bdataA = oneCell.load('ascending')
              #except ValueError as verror:
                  #print(verror)
                  #continue
        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['stimOn']
        if len(eventOnsetTimes)==len(bdata['currentFreq'])+1:
            eventOnsetTimes = eventOnsetTimes[:-1]
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

        stimCondition = bdata['stimCondition']
        #if stimCondition[-1] == 1:
        #    print('Removing last trial from ascending behavioral data. Paradigm ended in the middle of an oddball sequence.')
        #    stimCondition = stimCondition[:-1]
        stimCondition = stimCondition[:-10]

        oddballs = np.flatnonzero(stimCondition)

        firstOddball = np.array(oddballs[0::2])
        trials = []
        for firstOdd in firstOddball:
            trials.extend((firstOdd+1, firstOdd+2, firstOdd+3, firstOdd+4, firstOdd+5, firstOdd+6, firstOdd+7, firstOdd+8, firstOdd+9))

        afterOddTrials = sorted(np.append(firstOddball, trials))

        firstTrial = afterOddTrials[0::10] # first oddball
        firstIndexLimits = indexLimitsEachTrial[:,firstTrial]
        spikeCountFirstTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, firstIndexLimits, timeVec)

        secondTrial = afterOddTrials[1::10] # second oddball
        secondIndexLimits = indexLimitsEachTrial[:,secondTrial]
        spikeCountSecondTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, secondIndexLimits, timeVec)

        thirdTrial = afterOddTrials[2::10] # third oddball
        thirdIndexLimits = indexLimitsEachTrial[:,thirdTrial]
        spikeCountThirdTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, thirdIndexLimits, timeVec)

        fourthTrial = afterOddTrials[3::10] # first after oddball
        fourthIndexLimits = indexLimitsEachTrial[:,fourthTrial]
        spikeCountFourthTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, fourthIndexLimits, timeVec)

        fifthTrial = afterOddTrials[4::10] # second after oddball
        fifthIndexLimits = indexLimitsEachTrial[:,fifthTrial]
        spikeCountFifthTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, fifthIndexLimits, timeVec)

        sixthTrial = afterOddTrials[5::10] # third after oddball
        sixthIndexLimits = indexLimitsEachTrial[:,sixthTrial]
        spikeCountSixthTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, sixthIndexLimits, timeVec)

        seventhTrial = afterOddTrials[6::10] # fourth after oddball
        seventhIndexLimits = indexLimitsEachTrial[:,seventhTrial]
        spikeCountSeventhTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, seventhIndexLimits, timeVec)

        eighthTrial = afterOddTrials[7::10] # fifth after oddball
        eighthIndexLimits = indexLimitsEachTrial[:,eighthTrial]
        spikeCountEighthTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, eighthIndexLimits, timeVec)

        ninthTrial = afterOddTrials[8::10] # sixth after oddball
        ninthIndexLimits = indexLimitsEachTrial[:,ninthTrial]
        spikeCountNinthTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, ninthIndexLimits, timeVec)

        tenthTrial = afterOddTrials[9::10] # seventh after oddball
        tenthIndexLimits = indexLimitsEachTrial[:,tenthTrial]
        spikeCountTenthTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, tenthIndexLimits, timeVec)


        ax0 = plt.subplot2grid((1,10), (0,0), frameon=False)
        extraplots.plot_psth(spikeCountFirstTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.27, 0.01, 0.33)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.27, 0.01, 0.33))
        ax0.xaxis.set_visible(False)
        ax0.tick_params(axis='y', which='both', right=False, left=False, labelleft=True) #vertical shading
        plt.ylabel('Firing Rate [Hz]', fontsize=10)
        plt.title('First Odd', fontsize=10, y=-0.05)

        ax1 = plt.subplot2grid((1,10), (0,1), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSecondTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.28, 0.16, 0.47)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.28, 0.16, 0.47))
        ax1.yaxis.set_visible(False)
        ax1.xaxis.set_visible(False)
        plt.title('Second Odd', fontsize=10, y=-0.05)

        ax2 = plt.subplot2grid((1,10), (0,2), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountThirdTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.24, 0.29, 0.54)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.24, 0.29, 0.54))
        ax2.yaxis.set_visible(False)
        ax2.xaxis.set_visible(False)
        plt.title('Third Odd', fontsize=10, y=-0.05)

        ax3 = plt.subplot2grid((1,10), (0,3), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountFourthTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.19, 0.41, 0.56)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.19, 0.41, 0.56))
        ax3.yaxis.set_visible(False)
        ax3.xaxis.set_visible(False)

        ax4 = plt.subplot2grid((1,10), (0,4), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountFifthTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.15, 0.51, 0.56)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.15, 0.51, 0.56))
        plt.xlabel('Time from event onset [s]', fontsize=9)
        ax4.yaxis.set_visible(False)
        ax4.xaxis.set_visible(False)

        ax5 = plt.subplot2grid((1,10), (0,5), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSixthTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.12, 0.62, 0.54)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.12, 0.62, 0.54))
        ax5.yaxis.set_visible(False)
        ax5.xaxis.set_visible(False)

        ax6 = plt.subplot2grid((1,10), (0,6), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSeventhTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.21, 0.72, 0.47)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.21, 0.72, 0.47))
        ax6.yaxis.set_visible(False)
        ax6.xaxis.set_visible(False)

        ax7 = plt.subplot2grid((1,10), (0,7), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountEighthTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.43, 0.80, 0.35)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.43, 0.80, 0.35))
        ax7.yaxis.set_visible(False)
        ax7.xaxis.set_visible(False)

        ax8 = plt.subplot2grid((1,10), (0,8), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountNinthTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.71, 0.87, 0.17)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.71, 0.87, 0.17))
        ax8.yaxis.set_visible(False)
        ax8.xaxis.set_visible(False)

        ax9 = plt.subplot2grid((1,10), (0,9), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountTenthTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.99, 0.91, 0.15)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.99, 0.91, 0.15))
        ax9.yaxis.set_visible(False)
        ax9.xaxis.set_visible(False)

        """
        Saving the figure --------------------------------------------------------------
        """
        figFormat = 'png'
        figFilename ='{}_sequential_firing_rates_after_oddballs_{}_{}_{}um_T{}_c{}.{}'.format(indRow,dbRow['subject'],dbRow['date'],dbRow['depth'], dbRow['tetrode'],dbRow['cluster'],figFormat)
        outputDir = os.path.join(settings.REPORTS_PATH, 'ascending')
        figFullpath = os.path.join(outputDir,figFilename)
        plt.savefig(figFullpath,format=figFormat)

        plt.gcf().set_size_inches([12,4])
        print('Finished {}/{}'.format(indRow, len(celldb)-1))
        plt.show()

def sequential_firing_rates_before_oddballs(celldb):
    for indRow,dbRow in celldb.iterrows():
        plt.clf()
        ax = plt.subplot2grid((1,10), (0,0)) # Subplots
        plt.box(False)

        oneCell = ephyscore.Cell(dbRow)
        ephysData, bdata = oneCell.load('ascending')
        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['stimOn']
        if len(eventOnsetTimes)==len(bdata['currentFreq'])+1:
            eventOnsetTimes = eventOnsetTimes[:-1]
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

        stimCondition = bdata['stimCondition']
        #if stimCondition[-1] == 1:
        #    print('Removing last trial from ascending behavioral data. Paradigm ended in the middle of an oddball sequence.')
        #    stimCondition = stimCondition[:-1]
        stimCondition = stimCondition[:-10]

        oddballs = np.flatnonzero(stimCondition)

        firstOddball = np.array(oddballs[0::2])
        trials = []
        for firstOdd in firstOddball:
            trials.extend((firstOdd+1, firstOdd+2, firstOdd-1, firstOdd-2, firstOdd-3, firstOdd-4, firstOdd-5, firstOdd-6, firstOdd-7, firstOdd-8, firstOdd-9))

        beforeOddTrials = sorted(np.append(firstOddball, trials))

        firstTrial = beforeOddTrials[0::12] # first standard 3
        firstIndexLimits = indexLimitsEachTrial[:,firstTrial]
        spikeCountFirstTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, firstIndexLimits, timeVec)

        secondTrial = beforeOddTrials[1::12] # second standard 3
        secondIndexLimits = indexLimitsEachTrial[:,secondTrial]
        spikeCountSecondTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, secondIndexLimits, timeVec)

        thirdTrial = beforeOddTrials[2::12] # third standard 3
        thirdIndexLimits = indexLimitsEachTrial[:,thirdTrial]
        spikeCountThirdTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, thirdIndexLimits, timeVec)

        fourthTrial = beforeOddTrials[3::12] # first standard 2
        fourthIndexLimits = indexLimitsEachTrial[:,fourthTrial]
        spikeCountFourthTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, fourthIndexLimits, timeVec)

        fifthTrial = beforeOddTrials[4::12] # second standard 2
        fifthIndexLimits = indexLimitsEachTrial[:,fifthTrial]
        spikeCountFifthTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, fifthIndexLimits, timeVec)

        sixthTrial = beforeOddTrials[5::12] # third standard 2
        sixthIndexLimits = indexLimitsEachTrial[:,sixthTrial]
        spikeCountSixthTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, sixthIndexLimits, timeVec)

        seventhTrial = beforeOddTrials[6::12] # first standard
        seventhIndexLimits = indexLimitsEachTrial[:,seventhTrial]
        spikeCountSeventhTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, seventhIndexLimits, timeVec)

        eighthTrial = beforeOddTrials[7::12] # second standard
        eighthIndexLimits = indexLimitsEachTrial[:,eighthTrial]
        spikeCountEighthTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, eighthIndexLimits, timeVec)

        ninthTrial = beforeOddTrials[8::12] # third standard
        ninthIndexLimits = indexLimitsEachTrial[:,ninthTrial]
        spikeCountNinthTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, ninthIndexLimits, timeVec)

        tenthTrial = beforeOddTrials[9::12] # first oddball
        tenthIndexLimits = indexLimitsEachTrial[:,tenthTrial]
        spikeCountTenthTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, tenthIndexLimits, timeVec)

        eleventhTrial = beforeOddTrials[10::12] # second oddball
        eleventhIndexLimits = indexLimitsEachTrial[:,eleventhTrial]
        spikeCountEleventhTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, eleventhIndexLimits, timeVec)

        twelfthTrial = beforeOddTrials[11::12] # third oddball
        twelfthIndexLimits = indexLimitsEachTrial[:,twelfthTrial]
        spikeCountTwelfthTrial = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, twelfthIndexLimits, timeVec)

        ax0 = plt.subplot2grid((1,12), (0,0), frameon=False)
        extraplots.plot_psth(spikeCountFirstTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.27, 0.01, 0.33)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.27, 0.01, 0.33))
        ax0.xaxis.set_visible(False)
        ax0.tick_params(axis='y', which='both', right=False, left=False, labelleft=True) #vertical shading
        plt.ylabel('Firing Rate [Hz]', fontsize=10)

        ax1 = plt.subplot2grid((1,12), (0,1), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSecondTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.28, 0.16, 0.47)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.28, 0.16, 0.47))
        ax1.yaxis.set_visible(False)
        ax1.xaxis.set_visible(False)

        ax2 = plt.subplot2grid((1,12), (0,2), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountThirdTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.24, 0.29, 0.54)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.24, 0.29, 0.54))
        ax2.yaxis.set_visible(False)
        ax2.xaxis.set_visible(False)

        ax3 = plt.subplot2grid((1,12), (0,3), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountFourthTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.19, 0.41, 0.56)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.19, 0.41, 0.56))
        ax3.yaxis.set_visible(False)
        ax3.xaxis.set_visible(False)

        ax4 = plt.subplot2grid((1,12), (0,4), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountFifthTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.15, 0.51, 0.56)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.15, 0.51, 0.56))
        plt.xlabel('Time from event onset [s]', fontsize=9)
        ax4.yaxis.set_visible(False)
        ax4.xaxis.set_visible(False)

        ax5 = plt.subplot2grid((1,12), (0,5), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSixthTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.12, 0.62, 0.54)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.12, 0.62, 0.54))
        ax5.yaxis.set_visible(False)
        ax5.xaxis.set_visible(False)

        ax6 = plt.subplot2grid((1,12), (0,6), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSeventhTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.21, 0.72, 0.47)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.21, 0.72, 0.47))
        ax6.yaxis.set_visible(False)
        ax6.xaxis.set_visible(False)

        ax7 = plt.subplot2grid((1,12), (0,7), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountEighthTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.43, 0.80, 0.35)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.43, 0.80, 0.35))
        ax7.yaxis.set_visible(False)
        ax7.xaxis.set_visible(False)

        ax8 = plt.subplot2grid((1,12), (0,8), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountNinthTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.71, 0.87, 0.17)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.71, 0.87, 0.17))
        ax8.yaxis.set_visible(False)
        ax8.xaxis.set_visible(False)

        ax9 = plt.subplot2grid((1,12), (0,9), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountTenthTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.99, 0.91, 0.15)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.99, 0.91, 0.15))
        ax9.yaxis.set_visible(False)
        ax9.xaxis.set_visible(False)
        plt.title('First Odd', fontsize=10, y=-0.1)

        ax10 = plt.subplot2grid((1,12), (0,10), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountEleventhTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.99, 0.91, 0.15)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.99, 0.91, 0.15))
        ax10.yaxis.set_visible(False)
        ax10.xaxis.set_visible(False)
        plt.title('Second Odd', fontsize=10, y=-0.1)

        ax11 = plt.subplot2grid((1,12), (0,11), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountTwelfthTrial/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.99, 0.91, 0.15)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.99, 0.91, 0.15))
        ax11.yaxis.set_visible(False)
        ax11.xaxis.set_visible(False)
        plt.title('Third Odd', fontsize=10, y=-0.1)

        """
        Saving the figure --------------------------------------------------------------
        """
        figFormat = 'png'
        figFilename ='{}_sequential_firing_rates_before_oddballs_{}_{}_{}um_T{}_c{}.{}'.format(indRow,dbRow['subject'],dbRow['date'],dbRow['depth'], dbRow['tetrode'],dbRow['cluster'],figFormat)
        outputDir = os.path.join(settings.REPORTS_PATH, 'ascending')
        figFullpath = os.path.join(outputDir,figFilename)
        plt.savefig(figFullpath,format=figFormat)

        plt.gcf().set_size_inches([13,4])
        print('Finished {}/{}'.format(indRow, len(celldb)-1))
        plt.show()

def sequential_firing_rates_by_freq(celldb):
    for indRow,dbRow in celldb.iterrows():
        plt.clf()
        ax = plt.subplot2grid((1,10), (0,0)) # Subplots
        plt.box(False)

        oneCell = ephyscore.Cell(dbRow)
        ephysData, bdata = oneCell.load('ascending')
        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['stimOn']
        if len(eventOnsetTimes)==len(bdata['currentFreq'])+1:
            eventOnsetTimes = eventOnsetTimes[:-1]
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

        stimCondition = bdata['stimCondition']
        #if stimCondition[-1] == 1:
        #    print('Removing last trial from ascending behavioral data. Paradigm ended in the middle of an oddball sequence.')
        #    stimCondition = stimCondition[:-1]
        stimCondition = stimCondition[:-10]

        oddballs = np.flatnonzero(stimCondition)

        firstOddball = np.array(oddballs[0::2])
        trials = []
        for firstOdd in firstOddball:
            trials.extend((firstOdd+1, firstOdd+2, firstOdd-1, firstOdd-2, firstOdd-3, firstOdd-4, firstOdd-5, firstOdd-6, firstOdd-7, firstOdd-8, firstOdd-9, firstOdd-10, firstOdd-11, firstOdd-12, firstOdd-13, firstOdd-14, firstOdd-15, firstOdd-16, firstOdd-17, firstOdd-18, firstOdd-19, firstOdd-20, firstOdd-21))

        beforeOddTrials = sorted(np.append(firstOddball, trials))

        """
        HIGH FREQUENCY
        """

        firstHigh = beforeOddTrials[2::24]
        firstIndexLimits = indexLimitsEachTrial[:,firstHigh]
        spikeCountFirstHigh = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, firstIndexLimits, timeVec)

        secondHigh = beforeOddTrials[5::24]
        secondIndexLimits = indexLimitsEachTrial[:,secondHigh]
        spikeCountSecondHigh = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, secondIndexLimits, timeVec)

        thirdHigh = beforeOddTrials[8::24]
        thirdIndexLimits = indexLimitsEachTrial[:,thirdHigh]
        spikeCountThirdHigh = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, thirdIndexLimits, timeVec)

        fourthHigh = beforeOddTrials[11::24]
        fourthIndexLimits = indexLimitsEachTrial[:,fourthHigh]
        spikeCountFourthHigh = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, fourthIndexLimits, timeVec)

        fifthHigh = beforeOddTrials[14::24]
        fifthIndexLimits = indexLimitsEachTrial[:,fifthHigh]
        spikeCountFifthHigh = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, fifthIndexLimits, timeVec)

        sixthHigh = beforeOddTrials[17::24]
        sixthIndexLimits = indexLimitsEachTrial[:,sixthHigh]
        spikeCountSixthHigh = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, sixthIndexLimits, timeVec)

        seventhHigh = beforeOddTrials[20::24]
        seventhIndexLimits = indexLimitsEachTrial[:,seventhHigh]
        spikeCountSeventhHigh = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, seventhIndexLimits, timeVec)

        eighthHigh = beforeOddTrials[23::24]
        eighthIndexLimits = indexLimitsEachTrial[:,eighthHigh]
        spikeCountEighthHigh = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, eighthIndexLimits, timeVec)

        ax0 = plt.subplot2grid((3,8), (0,0), frameon=False)
        extraplots.plot_psth(spikeCountFirstHigh/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.47, 0.16, 0.12)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.47, 0.16, 0.12))
        ax0.xaxis.set_visible(False)
        ax0.tick_params(axis='y', which='both', right=False, left=False, labelleft=True) #vertical shading
        plt.ylabel('Firing Rate [Hz]', fontsize=10)

        ax1 = plt.subplot2grid((3,8), (0,1), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSecondHigh/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.58, 0.19, 0.14)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.58, 0.19, 0.14))
        ax1.yaxis.set_visible(False)
        ax1.xaxis.set_visible(False)

        ax2 = plt.subplot2grid((3,8), (0,2), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountThirdHigh/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.69, 0.23, 0.18)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.69, 0.23, 0.18))
        ax2.yaxis.set_visible(False)
        ax2.xaxis.set_visible(False)

        ax3 = plt.subplot2grid((3,8), (0,3), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountFourthHigh/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.80, 0.26, 0.21)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.80, 0.26, 0.21))
        ax3.yaxis.set_visible(False)
        ax3.xaxis.set_visible(False)

        ax4 = plt.subplot2grid((3,8), (0,4), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountFifthHigh/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.91, 0.30, 0.24)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.91, 0.30, 0.24))
        plt.xlabel('Time from event onset [s]', fontsize=9)
        ax4.yaxis.set_visible(False)
        ax4.xaxis.set_visible(False)

        ax5 = plt.subplot2grid((3,8), (0,5), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSixthHigh/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.93, 0.44, 0.39)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.93, 0.44, 0.39))
        ax5.yaxis.set_visible(False)
        ax5.xaxis.set_visible(False)

        ax6 = plt.subplot2grid((3,8), (0,6), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSeventhHigh/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.95, 0.58, 0.54)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.95, 0.58, 0.54))
        ax6.yaxis.set_visible(False)
        ax6.xaxis.set_visible(False)

        ax7 = plt.subplot2grid((3,8), (0,7), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountEighthHigh/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.96, 0.72, 0.69)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.96, 0.72, 0.69))
        ax7.yaxis.set_visible(False)
        ax7.xaxis.set_visible(False)

        """
        MIDDLE FREQUENCY
        """

        firstMid = beforeOddTrials[1::24]
        firstIndexLimits = indexLimitsEachTrial[:,firstMid]
        spikeCountFirstMid = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, firstIndexLimits, timeVec)

        secondMid = beforeOddTrials[4::24]
        secondIndexLimits = indexLimitsEachTrial[:,secondMid]
        spikeCountSecondMid = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, secondIndexLimits, timeVec)

        thirdMid = beforeOddTrials[7::24]
        thirdIndexLimits = indexLimitsEachTrial[:,thirdMid]
        spikeCountThirdMid = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, thirdIndexLimits, timeVec)

        fourthMid = beforeOddTrials[10::24]
        fourthIndexLimits = indexLimitsEachTrial[:,fourthMid]
        spikeCountFourthMid = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, fourthIndexLimits, timeVec)

        fifthMid = beforeOddTrials[13::24]
        fifthIndexLimits = indexLimitsEachTrial[:,fifthMid]
        spikeCountFifthMid = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, fifthIndexLimits, timeVec)

        sixthMid = beforeOddTrials[16::24]
        sixthIndexLimits = indexLimitsEachTrial[:,sixthMid]
        spikeCountSixthMid = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, sixthIndexLimits, timeVec)

        seventhMid = beforeOddTrials[19::24]
        seventhIndexLimits = indexLimitsEachTrial[:,seventhMid]
        spikeCountSeventhMid = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, seventhIndexLimits, timeVec)

        eighthMid = beforeOddTrials[22::24]
        eighthIndexLimits = indexLimitsEachTrial[:,eighthMid]
        spikeCountEighthMid = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, eighthIndexLimits, timeVec)

        ax8 = plt.subplot2grid((3,8), (1,0), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountFirstMid/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.09, 0.42, 0.23)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.09, 0.42, 0.23))
        ax8.xaxis.set_visible(False)
        ax8.tick_params(axis='y', which='both', right=False, left=False, labelleft=True) #vertical shading
        plt.ylabel('Firing Rate [Hz]', fontsize=10)

        ax9 = plt.subplot2grid((3,8), (1,1), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSecondMid/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.23, 0.51, 0.28)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.23, 0.51, 0.28))
        ax9.yaxis.set_visible(False)
        ax9.xaxis.set_visible(False)

        ax10 = plt.subplot2grid((3,8), (1,2), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountThirdMid/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.14, 0.61, 0.34)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.14, 0.61, 0.34))
        ax10.yaxis.set_visible(False)
        ax10.xaxis.set_visible(False)

        ax11 = plt.subplot2grid((3,8), (1,3), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountFourthMid/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.16, 0.71, 0.39)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.16, 0.71, 0.39))
        ax11.yaxis.set_visible(False)
        ax11.xaxis.set_visible(False)

        ax12 = plt.subplot2grid((3,8), (1,4), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountFifthMid/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.18, 0.8, 0.44)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.18, 0.8, 0.4))
        plt.xlabel('Time from event onset [s]', fontsize=9)
        ax12.yaxis.set_visible(False)
        ax12.xaxis.set_visible(False)

        ax13 = plt.subplot2grid((3,8), (1,5), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSixthMid/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.35, 0.84, 0.55)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.35, 0.84, 0.55))
        ax13.yaxis.set_visible(False)
        ax13.xaxis.set_visible(False)

        ax14 = plt.subplot2grid((3,8), (1,6), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSeventhMid/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.51, 0.88, 0.67)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.51, 0.88, 0.67))
        ax14.yaxis.set_visible(False)
        ax14.xaxis.set_visible(False)

        ax15 = plt.subplot2grid((3,8), (1,7), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountEighthMid/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.67, 0.92, 0.78)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.67, 0.92, 0.78))
        ax15.yaxis.set_visible(False)
        ax15.xaxis.set_visible(False)

        """
        LOW FREQUENCY
        """

        firstLow = beforeOddTrials[0::24]
        firstIndexLimits = indexLimitsEachTrial[:,firstLow]
        spikeCountFirstLow = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, firstIndexLimits, timeVec)

        secondLow = beforeOddTrials[3::24]
        secondIndexLimits = indexLimitsEachTrial[:,secondLow]
        spikeCountSecondLow = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, secondIndexLimits, timeVec)

        thirdLow = beforeOddTrials[6::24]
        thirdIndexLimits = indexLimitsEachTrial[:,thirdLow]
        spikeCountThirdLow = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, thirdIndexLimits, timeVec)

        fourthLow = beforeOddTrials[9::24]
        fourthIndexLimits = indexLimitsEachTrial[:,fourthLow]
        spikeCountFourthLow = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, fourthIndexLimits, timeVec)

        fifthLow = beforeOddTrials[12::24]
        fifthIndexLimits = indexLimitsEachTrial[:,fifthLow]
        spikeCountFifthLow = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, fifthIndexLimits, timeVec)

        sixthLow = beforeOddTrials[15::24]
        sixthIndexLimits = indexLimitsEachTrial[:,sixthLow]
        spikeCountSixthLow = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, sixthIndexLimits, timeVec)

        seventhLow = beforeOddTrials[18::24]
        seventhIndexLimits = indexLimitsEachTrial[:,seventhLow]
        spikeCountSeventhLow = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, seventhIndexLimits, timeVec)

        eighthLow = beforeOddTrials[21::24]
        eighthIndexLimits = indexLimitsEachTrial[:,eighthLow]
        spikeCountEighthLow = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, eighthIndexLimits, timeVec)

        ax16 = plt.subplot2grid((3,8), (2,0), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountFirstLow/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.11, 0.31, 0.45)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.11, 0.31, 0.45))
        ax16.xaxis.set_visible(False)
        ax16.tick_params(axis='y', which='both', right=False, left=False, labelleft=True) #vertical shading
        plt.ylabel('Firing Rate [Hz]', fontsize=10)

        ax17 = plt.subplot2grid((3,8), (2,1), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSecondLow/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.13, 0.38, 0.54)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.13, 0.38, 0.54))
        ax17.yaxis.set_visible(False)
        ax17.xaxis.set_visible(False)

        ax18 = plt.subplot2grid((3,8), (2,2), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountThirdLow/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.16, 0.45, 0.65)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.16, 0.45, 0.65))
        ax18.yaxis.set_visible(False)
        ax18.xaxis.set_visible(False)

        ax19 = plt.subplot2grid((3,8), (2,3), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountFourthLow/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.18, 0.53, 0.76)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.18, 0.53, 0.76))
        ax19.yaxis.set_visible(False)
        ax19.xaxis.set_visible(False)

        ax20 = plt.subplot2grid((3,8), (2,4), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountFifthLow/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.20, 0.60, 0.86)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.20, 0.60, 0.86))
        plt.xlabel('Time from event onset [s]', fontsize=9)
        ax20.yaxis.set_visible(False)
        ax20.xaxis.set_visible(False)

        ax21 = plt.subplot2grid((3,8), (2,5), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSixthLow/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.36, 0.68, 0.89)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.36, 0.68, 0.89))
        ax21.yaxis.set_visible(False)
        ax21.xaxis.set_visible(False)

        ax22 = plt.subplot2grid((3,8), (2,6), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountSeventhLow/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.52, 0.76, 0.91)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.52, 0.76, 0.91))
        ax22.yaxis.set_visible(False)
        ax22.xaxis.set_visible(False)

        ax23 = plt.subplot2grid((3,8), (2,7), sharey=ax0, frameon=False)
        extraplots.plot_psth(spikeCountEighthLow/binWidth, smoothWinSizePsth, timeVec, trialsEachCond=[], colorEachCond=[(0.68, 0.84, 0.95)], linestyle=None, linewidth=lwPsth, downsamplefactor=downsampleFactorPsth)
        plt.axvspan(0, 0.1, alpha=0.2, color=(0.68, 0.84, 0.95))
        ax23.yaxis.set_visible(False)
        ax23.xaxis.set_visible(False)
        plt.title('Oddball', fontsize=10, y=-0.2)

        """
        Saving the figure --------------------------------------------------------------
        """
        figFormat = 'png'
        figFilename ='{}_sequential_firing_rates_before_oddballs_by_freq_{}_{}_{}um_T{}_c{}.{}'.format(indRow,dbRow['subject'],dbRow['date'],dbRow['depth'], dbRow['tetrode'],dbRow['cluster'],figFormat)
        outputDir = os.path.join(settings.REPORTS_PATH, 'ascending')
        figFullpath = os.path.join(outputDir,figFilename)
        plt.savefig(figFullpath,format=figFormat)

        plt.gcf().set_size_inches([15,10])
        print('Finished {}/{}'.format(indRow, len(celldb)-1))
        plt.show()

#sequential_firing_rates_after_oddballs(responsivedb)
sequential_firing_rates_before_oddballs(responsivedb)
#sequential_firing_rates_by_freq(responsivedb)
