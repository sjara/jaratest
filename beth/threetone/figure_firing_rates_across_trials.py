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

# -- Database file name for single animal --
dbFilename = os.path.join(dbPath,'newresponsivedb_{}_A.h5'.format(studyparams.STUDY_NAME))

# -- Load the database of cells --
responsivedb = celldatabase.load_hdf(dbFilename)

# -- Variables --
timeRange = [-0.05, 0.2]  # In seconds
binWidth = 0.010
timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
smoothWinSizePsth = 2
lwPsth = 2
downsampleFactorPsth = 1

for indRow,dbRow in responsivedb.iterrows():
#for indRow,dbRow in responsivedb[0:1].iterrows():

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
    figFilename ='{}_sequential_firing_rates_{}_{}_{}um_T{}_c{}.{}'.format(indRow,dbRow['subject'],dbRow['date'],dbRow['depth'], dbRow['tetrode'],dbRow['cluster'],figFormat)
    outputDir = os.path.join(settings.REPORTS_PATH, 'ascending')
    figFullpath = os.path.join(outputDir,figFilename)
    plt.savefig(figFullpath,format=figFormat)

    plt.gcf().set_size_inches([12,4])
    print('Finished {}/{}'.format(indRow, len(responsivedb)-1))
    plt.show()
