'''
raster and histogram for switching task ALIGNED TO SOUND AND CENTER POKE OUT
Santiago Jaramillo and Billy Walker
'''
from jaratoolbox import celldatabase_quality_tuning as celldatabase####################################3
#eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code#################################

from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import ephyscore
import os
import numpy as np
from jaratoolbox import behavioranalysis
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import spikesorting_ISI as spikesorting
import matplotlib.pyplot as plt
from pylab import argsort,plot,axvline,cumsum,axhline,mean,ylabel,title,xlabel
import sys
import importlib


mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName+'_quality'
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

numRows = 14
numCols = 6
sizeClusterPlot = 1

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes

sizeRasters = (numRows-sizeClusterPlot)/3
sizeHists = (numRows-sizeClusterPlot)/6
#smallHist = sizeHists-1

SAMPLING_RATE=30000.0

reportname = 'switch_report_block_allFreq'
outputDir = '/home/billywalker/Pictures/switching_tuning_block_allfreq_reports/'
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.010 # Size of each bin in histogram in seconds
Frequency = 1 #This chooses which frequency to look at, numbered out of possible frequencies starting with the lowest frequency as number 0

timeRange = [-0.3,0.7] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)
tuning_timeRange = [-0.2,0.5] # In seconds. Time range for tuning rastor plot to plot spikes (around some event onset as 0)

minBlockSize = 20 #This is so that if the last block is small, it wont be plotted

ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'
behaviorDir='/home/billywalker/data/behavior/' #Need this for the tuning curve behavior


if not os.path.exists(outputDir): #makes sure output folder exists
    os.makedirs(outputDir)

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
subject = ''
behavSession = ''
#########################Load MI File################################
processedDir = os.path.join(settings.EPHYS_PATH,mouseName+'_processed')
modIFilename = os.path.join(processedDir,'modIndex.txt')
modIFile = open(modIFilename, 'r')
modIDict = {} #stores all the modulation indices
modSigDict = {} #stores the significance of the modulation of each cell
modDirectionScoreDict = {} #stores the score of how often the direction of modulation changes
behavName = ''
for line in modIFile:
    splitLine = line.split(':')
    if (splitLine[0] == 'Behavior Session'):
        behavName = splitLine[1][:-1]
    elif (splitLine[0] == 'modI'):
        modIDict[behavName] = [float(x) for x in splitLine[1].split(',')[0:-1]]
    elif (splitLine[0] == 'modSig'):
        modSigDict[behavName] = [float(x) for x in splitLine[1].split(',')[0:-1]]
    elif (splitLine[0] == 'modDir'):
        modDirectionScoreDict[behavName] = [float(x) for x in splitLine[1].split(',')[0:-1]]
modIFile.close()

bdata = None
eventOnsetTimes = None
spikeTimesFromEventOnset = None
indexLimitsEachTrial = None
spikeTimesFromMovementOnset = None
indexLimitsEachMovementTrial = None
titleText = ''

badSessionList = []#prints bad sessions at end

def main():
    global behavSession
    global subject
    global tetrode
    global cluster
    global tuningBehavior#behavior file name of tuning curve
    global tuningEphys#ephys session name of tuning curve
    global bdata
    global eventOnsetTimes
    global spikeTimesFromEventOnset
    global indexLimitsEachTrial
    global spikeTimesFromMovementOnset
    global indexLimitsEachMovementTrial
    global titleText

    print "switch_tuning_block_allfreq_report"
    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]
        try:
            if (behavSession != oneCell.behavSession):


                subject = oneCell.animalName
                behavSession = oneCell.behavSession
                ephysSession = oneCell.ephysSession
                tuningSession = oneCell.tuningSession
                ephysRoot = os.path.join(ephysRootDir,subject)
                tuningBehavior = oneCell.tuningBehavior
                tuningEphys = oneCell.tuningSession

                print behavSession

                # -- Load Behavior Data --
                behaviorFilename = loadbehavior.path_to_behavior_data(subject=subject,paradigm=paradigm,sessionstr=behavSession)
                bdata = loadbehavior.FlexCategBehaviorData(behaviorFilename)
                #bdata = loadbehavior.BehaviorData(behaviorFilename)
                numberOfTrials = len(bdata['choice'])

                # -- Load event data and convert event timestamps to ms --
                ephysDir = os.path.join(ephysRoot, ephysSession)
                eventFilename=os.path.join(ephysDir, 'all_channels.events')
                events = loadopenephys.Events(eventFilename) # Load events data
                eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 

                soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)

                eventOnsetTimes = eventTimes[soundOnsetEvents]
                soundOnsetTimeBehav = bdata['timeTarget']

                # Find missing trials
                missingTrials = behavioranalysis.find_missing_trials(eventOnsetTimes,soundOnsetTimeBehav)
                # Remove missing trials
                bdata.remove_trials(missingTrials)
                bdata.find_trials_each_block()


                ###############################################################################################
                centerOutTimes = bdata['timeCenterOut'] #This is the times that the mouse goes out of the center port
                soundStartTimes = bdata['timeTarget'] #This gives an array with the times in seconds from the start of the behavior paradigm of when the sound was presented for each trial
                timeDiff = centerOutTimes - soundStartTimes
                if (len(eventOnsetTimes) < len(timeDiff)):
                    timeDiff = timeDiff[:-1]
                    eventOnsetTimesCenter = eventOnsetTimes + timeDiff
                elif (len(eventOnsetTimes) > len(timeDiff)):
                    eventOnsetTimesCenter = eventOnsetTimes[:-1] + timeDiff
                else:
                    eventOnsetTimesCenter = eventOnsetTimes + timeDiff
                ###############################################################################################


            tetrode = oneCell.tetrode
            cluster = oneCell.cluster


            # -- Load Spike Data From Certain Cluster --
            spkData = ephyscore.CellData(oneCell)
            spkTimeStamps = spkData.spikes.timestamps

            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

            (spikeTimesFromMovementOnset,movementTrialIndexForEachSpike,indexLimitsEachMovementTrial) = \
                spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimesCenter,timeRange)


            plt.clf()
            if (len(spkTimeStamps)>0):
                ax1 = plt.subplot2grid((numRows,numCols), ((numRows-sizeClusterPlot),0), colspan = (numCols/3))
                spikesorting.plot_isi_loghist(spkData.spikes.timestamps)
                ax3 = plt.subplot2grid((numRows,numCols), ((numRows-sizeClusterPlot),(numCols/3)*2), colspan = (numCols/3))
                spikesorting.plot_events_in_time(spkTimeStamps)
                samples = spkData.spikes.samples.astype(float)-2**15
                samples = (1000.0/spkData.spikes.gain[0,0]) *samples
                ax2 = plt.subplot2grid((numRows,numCols), ((numRows-sizeClusterPlot),(numCols/3)), colspan = (numCols/3))
                spikesorting.plot_waveforms(samples)


            ###############################################################################
            ax4 = plt.subplot2grid((numRows,numCols), (0,0), colspan = (numCols/2), rowspan = 3*sizeRasters)
            #plt.setp(ax4.get_xticklabels(), visible=False)
            #fig.axes.get_xaxis().set_visible(False)
            raster_tuning(ax4)
            axvline(x=0, ymin=0, ymax=1, color='r')
            plt.gca().set_xlim(tuning_timeRange)

            ax6 = plt.subplot2grid((numRows,numCols), (0,(numCols/2)), colspan = (numCols/2), rowspan = sizeRasters)
            plt.setp(ax6.get_xticklabels(), visible=False)
            plt.setp(ax6.get_yticklabels(), visible=False)
            raster_sound_block_switching()
            plt.title('sound aligned, Top: middle freq in blocks, Bottom: all freqs')

            ax7 = plt.subplot2grid((numRows,numCols), (sizeRasters,(numCols/2)), colspan = (numCols/2), rowspan = sizeHists, sharex=ax6)
            hist_sound_block_switching(ax7)
            #plt.setp(ax7.get_yticklabels(), visible=False)
            ax7.yaxis.tick_right()
            ax7.yaxis.set_ticks_position('both')
            plt.setp(ax7.get_xticklabels(), visible=False)
            plt.gca().set_xlim(timeRange)


            ax10 = plt.subplot2grid((numRows,numCols), ((sizeRasters+sizeHists),(numCols/2)), colspan = (numCols/2), rowspan = sizeRasters) 
            plt.setp(ax10.get_xticklabels(), visible=False)
            plt.setp(ax10.get_yticklabels(), visible=False)
            raster_sound_allFreq_switching()
            

            ax11 = plt.subplot2grid((numRows,numCols), ((2*sizeRasters+sizeHists),(numCols/2)), colspan = (numCols/2), rowspan = sizeHists, sharex=ax10) 
            hist_sound_allFreq_switching(ax11)
            ax11.yaxis.tick_right()
            ax11.yaxis.set_ticks_position('both')
            ax11.set_xlabel('Time (sec)')
            #plt.setp(ax11.get_yticklabels(), visible=False)
            plt.gca().set_xlim(timeRange)

            ###############################################################################
            #plt.tight_layout()
            modulation_index_switching()
            plt.suptitle(titleText)

            tetrodeClusterName = 'T'+str(oneCell.tetrode)+'c'+str(oneCell.cluster)
            plt.gcf().set_size_inches((8.5,11))
            figformat = 'png' #'png' #'pdf' #'svg'
            filename = reportname+'_%s_%s_%s.%s'%(subject,behavSession,tetrodeClusterName,figformat)
            fulloutputDir = outputDir+subject +'/'
            fullFileName = os.path.join(fulloutputDir,filename)

            directory = os.path.dirname(fulloutputDir)
            if not os.path.exists(directory): #makes sure output folder exists
                os.makedirs(directory)
            #print 'saving figure to %s'%fullFileName
            plt.gcf().savefig(fullFileName,format=figformat)


        except:
            #print "error with session "+oneCell.behavSession
            if (oneCell.behavSession not in badSessionList):
                badSessionList.append(oneCell.behavSession)

    print 'error with sessions: '
    for badSes in badSessionList:
        print badSes


def raster_sound_switching():
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    correctRightward = rightward & correct
    correctLeftward = leftward & correct

    possibleFreq = np.unique(bdata['targetFrequency'])

    Freq = possibleFreq[Frequency]
    oneFreq = bdata['targetFrequency'] == Freq

    trialsToUseRight = rightward & oneFreq
    trialsToUseLeft = leftward & oneFreq

    trialsEachCond = np.c_[trialsToUseLeft,trialsToUseRight]; colorEachCond = ['r','g']
    extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
    
    #plt.ylabel('Trials')
    plt.title('Frequency: '+str(Freq))

def hist_sound_switching():
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    correctRightward = rightward & correct
    correctLeftward = leftward & correct

    possibleFreq = np.unique(bdata['targetFrequency'])

    Freq = possibleFreq[Frequency]
    oneFreq = bdata['targetFrequency'] == Freq

    trialsToUseRight = rightward & oneFreq
    trialsToUseLeft = leftward & oneFreq

    trialsEachCond = np.c_[trialsToUseLeft,trialsToUseRight]; colorEachCond = ['r','g']

    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    smoothWinSize = 3
    extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,
                         colorEachCond=colorEachCond,linestyle=None,linewidth=2,downsamplefactor=1)

    #plt.xlabel('Time from sound onset (s)')
    #plt.ylabel('Firing rate (spk/sec)')


def raster_movement_switching():
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    correctRightward = rightward & correct
    correctLeftward = leftward & correct

    possibleFreq = np.unique(bdata['targetFrequency'])

    Freq = possibleFreq[Frequency]
    oneFreq = bdata['targetFrequency'] == Freq

    trialsToUseRight = rightward & oneFreq
    trialsToUseLeft = leftward & oneFreq

    trialsEachCond = np.c_[trialsToUseLeft,trialsToUseRight]; colorEachCond = ['r','g']
    extraplots.raster_plot(spikeTimesFromMovementOnset,indexLimitsEachMovementTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
    
    #plt.ylabel('Trials')
    #plt.title('Movement Aligned')

def hist_movement_switching():
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    correctRightward = rightward & correct
    correctLeftward = leftward & correct

    possibleFreq = np.unique(bdata['targetFrequency'])

    Freq = possibleFreq[Frequency]
    oneFreq = bdata['targetFrequency'] == Freq

    trialsToUseRight = rightward & oneFreq
    trialsToUseLeft = leftward & oneFreq

    trialsEachCond = np.c_[trialsToUseLeft,trialsToUseRight]; colorEachCond = ['r','g']

    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromMovementOnset,indexLimitsEachMovementTrial,timeVec)

    smoothWinSize = 3
    extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,
                         colorEachCond=colorEachCond,linestyle=None,linewidth=2,downsamplefactor=1)

    #plt.xlabel('Time from center poke out (s)')
    #plt.ylabel('Firing rate (spk/sec)')




def raster_sound_allFreq_switching():
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    correctRightward = rightward & correct
    correctLeftward = leftward & correct

    possibleFreq = np.unique(bdata['targetFrequency'])

    Freq = possibleFreq[Frequency]
    oneFreq = bdata['targetFrequency'] == Freq

    trialsToUseRight = rightward & oneFreq
    trialsToUseLeft = leftward & oneFreq

    lowFreq = ((bdata['targetFrequency'] == possibleFreq[0]) & correct)
    highFreq = ((bdata['targetFrequency'] == possibleFreq[2]) & correct)

    trialsEachCond = np.c_[lowFreq,trialsToUseRight,trialsToUseLeft,highFreq]; colorEachCond = ['y','g','r','b']

    extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
    



def hist_sound_allFreq_switching(ax):
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    correctRightward = rightward & correct
    correctLeftward = leftward & correct

    possibleFreq = np.unique(bdata['targetFrequency'])

    Freq = possibleFreq[Frequency]
    oneFreq = bdata['targetFrequency'] == Freq

    trialsToUseRight = rightward & oneFreq
    trialsToUseLeft = leftward & oneFreq

    lowFreq = ((bdata['targetFrequency'] == possibleFreq[0]) & correct)
    highFreq = ((bdata['targetFrequency'] == possibleFreq[2]) & correct)

    trialsEachCond = np.c_[lowFreq,trialsToUseRight,trialsToUseLeft,highFreq]; colorEachCond = ['y','g','r','b']

    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    smoothWinSize = 3
    extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,
                         colorEachCond=colorEachCond,linestyle=None,linewidth=2,downsamplefactor=1)
    ax.axvspan(0.0, 0.1, color=[0.8,0.8,0.8], alpha=0.5, lw=0)

    #plt.xlabel('Time from sound onset (s)')
    #plt.ylabel('Firing rate (spk/sec)')


def raster_movement_allFreq_switching():
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    correctRightward = rightward & correct
    correctLeftward = leftward & correct

    possibleFreq = np.unique(bdata['targetFrequency'])

    Freq = possibleFreq[Frequency]
    oneFreq = bdata['targetFrequency'] == Freq

    trialsToUseRight = rightward & oneFreq
    trialsToUseLeft = leftward & oneFreq

    lowFreq = ((bdata['targetFrequency'] == possibleFreq[0]) & correct)
    highFreq = ((bdata['targetFrequency'] == possibleFreq[2]) & correct)

    trialsEachCond = np.c_[lowFreq,trialsToUseRight,trialsToUseLeft,highFreq]; colorEachCond = ['y','g','r','b']

    extraplots.raster_plot(spikeTimesFromMovementOnset,indexLimitsEachMovementTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
    



def hist_movement_allFreq_switching(ax):
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    correctRightward = rightward & correct
    correctLeftward = leftward & correct

    possibleFreq = np.unique(bdata['targetFrequency'])

    Freq = possibleFreq[Frequency]
    oneFreq = bdata['targetFrequency'] == Freq

    trialsToUseRight = rightward & oneFreq
    trialsToUseLeft = leftward & oneFreq

    lowFreq = ((bdata['targetFrequency'] == possibleFreq[0]) & correct)
    highFreq = ((bdata['targetFrequency'] == possibleFreq[2]) & correct)

    trialsEachCond = np.c_[lowFreq,trialsToUseRight,trialsToUseLeft,highFreq]; colorEachCond = ['y','g','r','b']

    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromMovementOnset,indexLimitsEachMovementTrial,timeVec)

    smoothWinSize = 3
    extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,
                         colorEachCond=colorEachCond,linestyle=None,linewidth=2,downsamplefactor=1)

    ax.axvline(x=0, ymin=0, ymax=1, color='r')
    #plt.xlabel('Time from sound onset (s)')
    #plt.ylabel('Firing rate (spk/sec)')



def raster_movement_block_switching():
    correct = bdata['outcome']==bdata.labels['outcome']['correct']

    possibleFreq = np.unique(bdata['targetFrequency'])

    Freq = possibleFreq[Frequency]
    oneFreq = bdata['targetFrequency'] == Freq

    correctOneFreq = oneFreq & correct
    trialsEachBlock = bdata.blocks['trialsEachBlock']
    correctTrialsEachBlock = trialsEachBlock & correctOneFreq[:,np.newaxis]
    correctBlockSizes = sum(correctTrialsEachBlock)
    if (correctBlockSizes[-1] < minBlockSize): #Just a check to see if last block is too small to plot
        blockSizes = sum(trialsEachBlock)
        numBlocks = len(trialsEachBlock[0])
        sumBlocks = sum(blockSizes)
        newTrialsLastBlock = np.zeros((blockSizes[-1],numBlocks), dtype=np.bool)
        correctTrialsEachBlock[(sumBlocks-blockSizes[-1]):] = newTrialsLastBlock #if the last block is too small, make the condition for the last trial all false
        #correctTrialsEachBlock = trialsEachBlock & correctOneFreq[:,np.newaxis]

    trialsEachCond = correctTrialsEachBlock;

    if bdata['currentBlock'][0]==bdata.labels['currentBlock']['low_boundary']:
        colorEachBlock = 4*['g','r']
    else:
        colorEachBlock = 4*['r','g']

    extraplots.raster_plot(spikeTimesFromMovementOnset,indexLimitsEachMovementTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachBlock,fillWidth=None,labels=None)
    
    #plt.ylabel('Trials')
    #plt.title('Blocks Movement Aligned')

def hist_movement_block_switching():
    correct = bdata['outcome']==bdata.labels['outcome']['correct']

    possibleFreq = np.unique(bdata['targetFrequency'])

    Freq = possibleFreq[Frequency]
    oneFreq = bdata['targetFrequency'] == Freq

    correctOneFreq = oneFreq & correct
    trialsEachBlock = bdata.blocks['trialsEachBlock']
    correctTrialsEachBlock = trialsEachBlock & correctOneFreq[:,np.newaxis]
    correctBlockSizes = sum(correctTrialsEachBlock)
    if (correctBlockSizes[-1] < minBlockSize): #Just a check to see if last block is too small to plot
        blockSizes = sum(trialsEachBlock)
        numBlocks = len(trialsEachBlock[0])
        sumBlocks = sum(blockSizes)
        newTrialsLastBlock = np.zeros((blockSizes[-1],numBlocks), dtype=np.bool)
        correctTrialsEachBlock[(sumBlocks-blockSizes[-1]):] = newTrialsLastBlock #if the last block is too small, make the condition for the last trial all false
        #correctTrialsEachBlock = trialsEachBlock & correctOneFreq[:,np.newaxis]

    trialsEachCond = correctTrialsEachBlock;

    if bdata['currentBlock'][0]==bdata.labels['currentBlock']['low_boundary']:
        colorEachBlock = 4*['g','r']
    else:
        colorEachBlock = 4*['r','g']
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromMovementOnset,indexLimitsEachMovementTrial,timeVec)

    smoothWinSize = 3
    extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,
                         colorEachCond=colorEachBlock,linestyle=None,linewidth=2,downsamplefactor=1)

    #plt.xlabel('Time from center out poke (s)')
    #plt.ylabel('Firing rate (spk/sec)')


def raster_sound_block_switching():
    correct = bdata['outcome']==bdata.labels['outcome']['correct']

    possibleFreq = np.unique(bdata['targetFrequency'])

    Freq = possibleFreq[Frequency]
    oneFreq = bdata['targetFrequency'] == Freq


    correctOneFreq = oneFreq & correct
    trialsEachBlock = bdata.blocks['trialsEachBlock']
    correctTrialsEachBlock = trialsEachBlock & correctOneFreq[:,np.newaxis]
    correctBlockSizes = sum(correctTrialsEachBlock)
    if (correctBlockSizes[-1] < minBlockSize): #Just a check to see if last block is too small to plot
        blockSizes = sum(trialsEachBlock)
        numBlocks = len(trialsEachBlock[0])
        sumBlocks = sum(blockSizes)
        newTrialsLastBlock = np.zeros((blockSizes[-1],numBlocks), dtype=np.bool)
        correctTrialsEachBlock[(sumBlocks-blockSizes[-1]):] = newTrialsLastBlock #if the last block is too small, make the condition for the last trial all false
        #correctTrialsEachBlock = trialsEachBlock & correctOneFreq[:,np.newaxis]

    trialsEachCond = correctTrialsEachBlock;

    if bdata['currentBlock'][0]==bdata.labels['currentBlock']['low_boundary']:
        colorEachBlock = 4*['g','r']
    else:
        colorEachBlock = 4*['r','g']

    extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachBlock,fillWidth=None,labels=None)
    
    #plt.ylabel('Trials')
    plt.title('Sound Aligned (Top) and Movement Aligned (Bottom)')

def hist_sound_block_switching(ax):
    correct = bdata['outcome']==bdata.labels['outcome']['correct']

    possibleFreq = np.unique(bdata['targetFrequency'])

    Freq = possibleFreq[Frequency]
    oneFreq = bdata['targetFrequency'] == Freq

    correctOneFreq = oneFreq & correct
    trialsEachBlock = bdata.blocks['trialsEachBlock']
    correctTrialsEachBlock = trialsEachBlock & correctOneFreq[:,np.newaxis]
    correctBlockSizes = sum(correctTrialsEachBlock)
    if (correctBlockSizes[-1] < minBlockSize): #Just a check to see if last block is too small to plot
        blockSizes = sum(trialsEachBlock)
        numBlocks = len(trialsEachBlock[0])
        sumBlocks = sum(blockSizes)
        newTrialsLastBlock = np.zeros((blockSizes[-1],numBlocks), dtype=np.bool)
        correctTrialsEachBlock[(sumBlocks-blockSizes[-1]):] = newTrialsLastBlock #if the last block is too small, make the condition for the last trial all false
        #correctTrialsEachBlock = trialsEachBlock & correctOneFreq[:,np.newaxis]

    trialsEachCond = correctTrialsEachBlock;

    if bdata['currentBlock'][0]==bdata.labels['currentBlock']['low_boundary']:
        colorEachBlock = 4*['g','r']
    else:
        colorEachBlock = 4*['r','g']
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    smoothWinSize = 3
    extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,
                         colorEachCond=colorEachBlock,linestyle=None,linewidth=2,downsamplefactor=1)

    ax.axvspan(0.0, 0.1, color=[0.8,0.8,0.8], alpha=0.5, lw=0)

    #plt.xlabel('Time from sound onset (s)')
    #plt.ylabel('Firing rate (spk/sec)')


def modulation_index_switching():
    global titleText
    global modIDict
    global modSigDict
    global modDirectionScoreDict
    clusterNumber = (tetrode-1)*clusNum+(cluster-1)

    #titleText = 'Mod Index: '+str(round(modIDict[behavSession][clusterNumber],3))+', sig (p val): '+str(round(modSigDict[behavSession][clusterNumber],3))+', Mod Direction Score: '+str(modDirectionScoreDict[behavSession][clusterNumber])
    titleText = 'Mod Index: '+str(round(modIDict[behavSession][clusterNumber],3))+', (p='+str(round(modSigDict[behavSession][clusterNumber],3))+'), Number of consistent activity changes: '+str(modDirectionScoreDict[behavSession][clusterNumber])+'\n blue = high freq, green = middle freq going to the right, red = middle freq going to the left, yellow = low freq'


def raster_tuning(ax):

    fullbehaviorDir = behaviorDir+subject+'/'
    behavName = subject+'_tuning_curve_'+tuningBehavior+'.h5'
    tuningBehavFileName=os.path.join(fullbehaviorDir, behavName)


    tuning_bdata = loadbehavior.BehaviorData(tuningBehavFileName,readmode='full')
    freqEachTrial = tuning_bdata['currentFreq']
    possibleFreq = np.unique(freqEachTrial)
    numberOfTrials = len(freqEachTrial)

    # -- The old way of sorting (useful for plotting sorted raster) --
    sortedTrials = []
    numTrialsEachFreq = []  #Used to plot lines after each group of sorted trials
    for indf,oneFreq in enumerate(possibleFreq): #indf is index of this freq and oneFreq is the frequency
        indsThisFreq = np.flatnonzero(freqEachTrial==oneFreq) #this gives indices of this frequency
        sortedTrials = np.concatenate((sortedTrials,indsThisFreq)) #adds all indices to a list called sortedTrials
        numTrialsEachFreq.append(len(indsThisFreq)) #finds number of trials each frequency has
    sortingInds = argsort(sortedTrials) #gives array of indices that would sort the sortedTrials

    # -- Load event data and convert event timestamps to ms --
    tuning_ephysDir = os.path.join(settings.EPHYS_PATH, subject,tuningEphys)
    tuning_eventFilename=os.path.join(tuning_ephysDir, 'all_channels.events')
    tuning_ev=loadopenephys.Events(tuning_eventFilename) #load ephys data (like bdata structure)
    tuning_eventTimes=np.array(tuning_ev.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 
    tuning_evID=np.array(tuning_ev.eventID)  #loads the onset times of events (matches up with eventID to say if event 1 went on (1) or off (0)
    tuning_eventOnsetTimes=tuning_eventTimes[tuning_evID==1] #array that is a time stamp for when the chosen event happens.
    #ev.eventChannel woul load array of events like trial start and sound start and finish times (sound event is 0 and trial start is 1 for example). There is only one event though and its sound start
    while (numberOfTrials < len(tuning_eventOnsetTimes)):
        tuning_eventOnsetTimes = tuning_eventOnsetTimes[:-1]

    #######################################################################################################
    ###################THIS IS SUCH A HACK TO GET SPKDATA FROM EPHYSCORE###################################
    #######################################################################################################

    thisCell = celldatabase.CellInfo(animalName=subject,############################################
                 ephysSession = tuningEphys,
                 tuningSession = 'DO NOT NEED THIS',
                 tetrode = tetrode,
                 cluster = cluster,
                 quality = 1,
                 depth = 0,
                 tuningBehavior = 'DO NOT NEED THIS',
		 behavSession = tuningBehavior)
    
    tuning_spkData = ephyscore.CellData(thisCell)
    tuning_spkTimeStamps = tuning_spkData.spikes.timestamps

    (tuning_spikeTimesFromEventOnset,tuning_trialIndexForEachSpike,tuning_indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(tuning_spkTimeStamps,tuning_eventOnsetTimes,tuning_timeRange)

    #print 'numTrials ',max(tuning_trialIndexForEachSpike)#####################################
    '''
        Create a vector with the spike timestamps w.r.t. events onset.

        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = 
            eventlocked_spiketimes(timeStamps,eventOnsetTimes,timeRange)

        timeStamps: (np.array) the time of each spike.
        eventOnsetTimes: (np.array) the time of each instance of the event to lock to.
        timeRange: (list or np.array) two-element array specifying time-range to extract around event.

        spikeTimesFromEventOnset: 1D array with time of spikes locked to event.
    o    trialIndexForEachSpike: 1D array with the trial corresponding to each spike.
           The first spike index is 0.
        indexLimitsEachTrial: [2,nTrials] range of spikes for each trial. Note that
           the range is from firstSpike to lastSpike+1 (like in python slices)
        spikeIndices
    '''

    tuning_sortedIndexForEachSpike = sortingInds[tuning_trialIndexForEachSpike] #Takes values of trialIndexForEachSpike and finds value of sortingInds at that index and makes array. This array gives an array with the sorted index of each trial for each spike


    # -- Calculate tuning --
    #nSpikes = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange) #array of the number of spikes in range for each trial
    '''Count number of spikes on each trial in a given time range.

           spikeTimesFromEventOnset: vector of spikes timestamps with respect
             to the onset of the event.
           indexLimitsEachTrial: each column contains [firstInd,lastInd+1] of the spikes on a trial.
           timeRange: time range to evaluate. Spike times exactly at the limits are not counted.

           returns nSpikes
    '''
    '''
    meanSpikesEachFrequency = np.empty(len(possibleFreq)) #make empty array of same size as possibleFreq

    # -- This part will be replace by something like behavioranalysis.find_trials_each_type --
    trialsEachFreq = []
    for indf,oneFreq in enumerate(possibleFreq):
        trialsEachFreq.append(np.flatnonzero(freqEachTrial==oneFreq)) #finds indices of each frequency. Appends them to get an array of indices of trials sorted by freq

    # -- Calculate average firing for each freq --
    for indf,oneFreq in enumerate(possibleFreq):
        meanSpikesEachFrequency[indf] = np.mean(nSpikes[trialsEachFreq[indf]])
    '''
    #clf()
    #if (len(tuning_spkTimeStamps)>0):
        #ax1 = plt.subplot2grid((4,4), (3, 0), colspan=1)
        #spikesorting.plot_isi_loghist(spkData.spikes.timestamps)
        #ax3 = plt.subplot2grid((4,4), (3, 3), colspan=1)
        #spikesorting.plot_events_in_time(tuning_spkTimeStamps)
        #samples = tuning_spkData.spikes.samples.astype(float)-2**15
        #samples = (1000.0/tuning_spkData.spikes.gain[0,0]) *samples
        #ax2 = plt.subplot2grid((4,4), (3, 1), colspan=2)
        #spikesorting.plot_waveforms(samples)
    #ax4 = plt.subplot2grid((4,4), (0, 0), colspan=3,rowspan = 3)
    plot(tuning_spikeTimesFromEventOnset, tuning_sortedIndexForEachSpike, '.', ms=3)
    #axvline(x=0, ymin=0, ymax=1, color='r')

    #The cumulative sum of the list of specific frequency presentations, 
    #used below for plotting the lines across the figure. 
    numTrials = cumsum(numTrialsEachFreq)

    #Plot the lines across the figure in between each group of sorted trials
    for indf, num in enumerate(numTrials):
        ax.axhline(y = num, xmin = 0, xmax = 1, color = '0.90', zorder = 0)
       
    
    tickPositions = numTrials - mean(numTrialsEachFreq)/2
    tickLabels = ["%0.2f" % (possibleFreq[indf]/1000) for indf in range(len(possibleFreq))]
    ax.set_yticks(tickPositions)
    ax.set_yticklabels(tickLabels)
    ax.set_ylim([-1,numberOfTrials])
    ylabel('Frequency Presented (kHz), {} total trials'.format(numTrials[-1]))
    #title(ephysSession+' T{}c{}'.format(tetrodeID,clusterID))
    xlabel('Time (sec)')
    '''

    ax5 = plt.subplot2grid((4,4), (0, 3), colspan=1,rowspan=3)
    ax5.set_xscale('log')
    plot(possibleFreq,meanSpikesEachFrequency,'o-')
    ylabel('Avg spikes in window {0}-{1} sec'.format(*responseRange))
    xlabel('Frequency')
    '''
    #show()

    '''
    tetrodeClusterName = 'T'+str(tetrodeID)+'c'+str(clusterID)
    plt.gcf().set_size_inches((8.5,11))
    figformat = 'png' #'png' #'pdf' #'svg'
    filename = 'tuning_%s_%s_%s.%s'%(subject,behavSession,tetrodeClusterName,figformat)
    fullFileName = os.path.join(fulloutputDir,filename)
    print 'saving figure to %s'%fullFileName
    plt.gcf().savefig(fullFileName,format=figformat)
    '''
            

main()
