'''
[For all cells in DB] create cell reports include the following plots for three sessions:
noiseburst: raster, PSTH, ISI, waverform, sparks over time
laserpulse: raster, PSTH, ISI, waveform, sparks over time
TuningCurve: raster plot(for one intensity), waveform

You have to specify the name of the subject you want to generate the reports for,
and give answer to question which duplicated session do you want to use to plot in\
case you have more than one same sessions such as laserpulse
'''

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from jaratoolbox import settings
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import spikesorting
from jaratoolbox import ephyscore
from jaratoolbox import celldatabase
from jaratoolbox import behavioranalysis
# from jaratest.common.2019astrpi import studyparams

#-----------parameters----------------
timeRange = [-0.5, 0.5]
binWidth = 0.010
timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
smoothWinSizePsth = 3 # smoothWinSizePsth2 = 3
lwPsth = 2
downsampleFactorPsth = 1
msRaster = 2
#---------subplot adjust------------
bottom = 0.05
top = 0.93
hspace = 0.4
wspace = 0.65
left=0.1
right=0.88
countreport = 0 # count the number of reports generated
#---------------------------------------------------------------------------
fig = plt.gcf()
fig.clf()
#subject = raw_input('what is the name of subject? ')
#pathtoDB = os.path.join(pathtosubject,subject)
# pathtosubject = '/home/jarauser/src/jaratest/allison/d1pi032'
# pathtoDB = os.path.join(pathtosubject,'celldb.h5')
# celldb = pd.read_hdf(pathtoDB)
subject = ['d1pi033']#studyparams.SINGLE_MOUSE
studyname = '2019astrpi'
celldb = celldatabase.generate_cell_database_from_subjects(subject)
outputDir = '/mnt/jarahubdata/reports/2019astrpi'#os.path.join(settings.FIGURES_DATA_PATH, studyname, 'output')#figparams.FIGURE_OUTPUT_DIR

answer = raw_input('if there\'s any duplicated sessions, do you want to use the first one[0] \
or the last one[1]? If you don\'t care, put any number ')

for indRow, dbRow in celldb.iterrows():
    oneCell = ephyscore.Cell(dbRow)

    rast1 = []
    rast2 = []
    spkMat = []
    spikeT = []
    waveF = []
    ax = []

    sessionCell= [con  for (i, con) in enumerate(dbRow['sessionType'])] #if con == 'sessiontype']
    sessionUC = pd.Series(sessionCell).unique() #sessionUC = list(set(sessionCell)) even numpy changes the sequence
    sessionsOrig = [ss for ss in sessionUC if (ss == 'noiseburst') or (ss == 'laserpulse') or (ss == 'tuningCurve')]#
    sessions = np.copy(sessionsOrig)

    for sessiontype in sessionsOrig:

        sessionInds= [ind  for (ind, con) in enumerate(dbRow['sessionType']) if con == sessiontype]
        randomchoice = random.choice(sessionInds)
        sessionIndToUse = sessionInds[0] if answer=='0' else (sessionInds[-1] if answer == '1'  else sessionInds[randomchoice])
        ephysData, bdata = oneCell.load_by_index(sessionIndToUse)# behavClass=behavClass you may need to include that while doing tuning curve

        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['stimOn']

        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)
        #--------------------------Tuning curve------------------------------------------
        ## ----------tuning curve variables
        if sessiontype == 'tuningCurve':
            currentFreq = bdata['currentFreq']
            trialsEachType = behavioranalysis.find_trials_each_type(currentFreq,np.unique(currentFreq))
            uniqFreq = np.unique(currentFreq)
            b = np.array(["%.0f" %i for i in uniqFreq]) # this is unique frequencies
            freqTicks = [str(b[i])+" ["+str(i)+"]" for i , con in enumerate(b)]
            nTrialsEachCond = [trialsEachType[:,i].sum() for i in range(trialsEachType.shape[1])]
            new_tick_locations = np.cumsum(nTrialsEachCond)
    #-----------------------PSTH spikecountmatrix ---------------------------------------
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
    #-------------------------Getting ready for plotting--------------------------------
        rast1.append(spikeTimesFromEventOnset)
        rast2.append(indexLimitsEachTrial)
        spkMat.append(spikeCountMat)
        spikeT.append(spikeTimes)
        waveF.append(ephysData['samples'])

    #plt.plot(spikeTimesFromEventOnset,trialIndexForEachSpike,'.')
    #-----------------------Plot variables-----------------------------
    tetnum = dbRow['tetrode']
    chanum = dbRow['cluster']
    j = 0
    scaleGrid = (4,9)
    #np.arange(0,2000,120) # for TC. #//np.linspace(0,2000,16) there are 16 frequencies
    #-------------------------end of set variable-----------------------------------
    #-----------------------Raster,PSTH,ISI,WaveForm,EventTime------------------------
    for i, con in enumerate(sessions) :
        if con != 'tuningCurve':

            ax1 = plt.subplot2grid(scaleGrid, (0, j), colspan=3)
            ax.append(ax1)
            plt.subplots_adjust(bottom=bottom, top=top,hspace = hspace, wspace = wspace,left = left, right = right)
        #pRaster comes here
            pRaster, hcond, zline = extraplots.raster_plot(rast1[i],rast2[i],timeRange,trialsEachCond=[])
            plt.setp(pRaster, ms=msRaster)
            plt.setp(hcond,zorder=3)
            plt.ylabel('Trial')
            plt.title(con.title())

        # ------------------------------- Plot PSTH  --
            ax2 = plt.subplot2grid(scaleGrid, (1, j), colspan=3,sharex = ax1)
            plt.subplots_adjust(bottom=bottom, top=top,hspace = hspace, wspace = wspace)
            pPSTH = extraplots.plot_psth(spkMat[i]/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
            #plt.plot(spikeTimesFromEventOnset,trialIndexForEachSpike,'.', markersize = '3')
            extraplots.boxoff(plt.gca())
            plt.ylabel('Firing rate\n(spk/s)')
            plt.xlabel('time from onset of the sound(s)')

        # --------ISI plot----------------
            ax31 = plt.subplot2grid(scaleGrid, (2+j/3, 0),colspan=2)
            plt.subplots_adjust(bottom=bottom, top=top,hspace = hspace)
            spikesorting.plot_isi_loghist(spikeT[i])

            # -- Plot waveforms --
            ax32 = plt.subplot2grid(scaleGrid, (2+j/3, 2),colspan=2)
            plt.subplots_adjust(bottom=bottom, top=top,hspace = hspace)
            if waveF[i].any():
                spikesorting.plot_waveforms(waveF[i])

            # -- Plot events in time --
            ax33 = plt.subplot2grid(scaleGrid, (2+j/3, 4),colspan=2)
            plt.subplots_adjust(bottom=bottom, top=top,hspace = hspace)
            if spikeT[i].any():
                spikesorting.plot_events_in_time(spikeT[i])
            j = j + 3
    ################################################################################
    # -----------------------------Tuning Curve Raster Plot-------------------------
        else:
            #----------if the length doesn't match, abandon last one from trialsEachType
            while indexLimitsEachTrial.shape[1] < trialsEachType.shape[0]:
                trialsEachType = np.delete(trialsEachType,-1,0)

            ax11 = plt.subplot2grid(scaleGrid,(0,6),colspan = 3, rowspan=3)
            #plt.subplots_adjust(bottom=bottom, top=top,hspace = hspace, left = left, right = right)
            pRaster, hcond, zline = extraplots.raster_plot(rast1[i],rast2[i],timeRange,trialsEachCond=trialsEachType)
            #-------------plot--------------
            plt.setp(pRaster, ms=msRaster)
            plt.setp(hcond,zorder=3)
            plt.ylabel('Trial')
            ax11.set_yticks(new_tick_locations)
            ax11.set_yticklabels(new_tick_locations)
            plt.title(con.title())
            # still raster plot, plotting frequency levels
            ax112 = ax11.twinx()
            ax112.set_yticks(new_tick_locations)
            ax112.set_yticklabels(freqTicks)
            ax112.set_ylabel('Frequency(Hz)')

            #--------------------------Waveform------------------------------------
            ax12 = plt.subplot2grid(scaleGrid, (3,6),colspan=3)
            plt.subplots_adjust(bottom=bottom, top=top,hspace = hspace, right = right)
            if waveF[i].any():
                spikesorting.plot_waveforms(waveF[i])
    ################################################################################333
    title = '[{5}]{0}, {1}, {2}um, T{3}c{4}, session ={6}'.format(dbRow['subject'],dbRow['date'], dbRow['depth'], tetnum,chanum,dbRow.name,sessionCell)
    plt.suptitle(title,fontsize = 15,fontname="Times New Roman Bold")
    fig.set_size_inches([20, 10])
    pathtoPng = os.path.join(outputDir,'cellreport/')
    fig.savefig(pathtoPng +'[c#%s] %s_%s_tetrode%s_cluster%s.png' %(dbRow.name,dbRow['subject'],dbRow['depth'],tetnum,chanum))
    plt.clf()
    countreport += 1
