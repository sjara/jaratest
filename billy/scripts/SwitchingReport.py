'''
raster and histogram for switching task ALIGNED TO CENTER POKE OUT
Santiago Jaramillo and Billy Walker
'''


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
import sys
import importlib

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

numRows = 13
numCols = 6
sizeClusterPlot = 1

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes

sizeRasters = (numRows-sizeClusterPlot)/3
sizeHists = (numRows-sizeClusterPlot)/6


SAMPLING_RATE=30000.0

outputDir = '/home/billywalker/Pictures/switching_reports/'
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.010 # Size of each bin in histogram in seconds
Frequency = 1 #This chooses which frequency to look at, numbered out of possible frequencies starting with the lowest frequency as number 0

timeRange = [-0.3,0.7] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)
minBlockSize = 20 #This is so that if the last block is small, it wont be plotted

ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'

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
    global bdata
    global eventOnsetTimes
    global spikeTimesFromEventOnset
    global indexLimitsEachTrial
    global spikeTimesFromMovementOnset
    global indexLimitsEachMovementTrial
    global titleText

    print "SwitchingReport"
    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]
        try:
            if (behavSession != oneCell.behavSession):


                subject = oneCell.animalName
                behavSession = oneCell.behavSession
                ephysSession = oneCell.ephysSession
                ephysRoot = os.path.join(ephysRootDir,subject)

                print behavSession

                # -- Load Behavior Data --
                behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
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
            ax4 = plt.subplot2grid((numRows,numCols), (0,0), colspan = (numCols/2), rowspan = sizeRasters)
            plt.setp(ax4.get_xticklabels(), visible=False)
            raster_sound_block_switching()
            ax5 = plt.subplot2grid((numRows,numCols), (sizeRasters,0), colspan = (numCols/2), rowspan = sizeHists, sharex=ax4)
            hist_sound_block_switching()
            ax6 = plt.subplot2grid((numRows,numCols), (0,(numCols/2)), colspan = (numCols/2), rowspan = sizeRasters)
            plt.setp(ax6.get_xticklabels(), visible=False)
            raster_movement_block_switching()
            ax7 = plt.subplot2grid((numRows,numCols), (sizeRasters,(numCols/2)), colspan = (numCols/2), rowspan = sizeHists, sharex=ax6)
            hist_movement_block_switching()

            ax8 = plt.subplot2grid((numRows,numCols), ((sizeRasters+sizeHists),0), colspan = (numCols/2), rowspan = sizeRasters)
            plt.setp(ax8.get_xticklabels(), visible=False)
            raster_sound_allFreq_switching()     
            ax9 = plt.subplot2grid((numRows,numCols), ((2*sizeRasters+sizeHists),0), colspan = (numCols/2), rowspan = sizeHists, sharex=ax8)
            hist_sound_allFreq_switching()
            ax10 = plt.subplot2grid((numRows,numCols), ((sizeRasters+sizeHists),(numCols/2)), colspan = (numCols/2), rowspan = sizeRasters) 
            plt.setp(ax10.get_xticklabels(), visible=False)
            raster_sound_switching()
            ax11 = plt.subplot2grid((numRows,numCols), ((2*sizeRasters+sizeHists),(numCols/2)), colspan = (numCols/2), rowspan = sizeHists, sharex=ax10) 
            hist_sound_switching()
            ###############################################################################
            #plt.tight_layout()
            modulation_index_switching()
            plt.suptitle(titleText)

            tetrodeClusterName = 'T'+str(oneCell.tetrode)+'c'+str(oneCell.cluster)
            plt.gcf().set_size_inches((8.5,11))
            figformat = 'png' #'png' #'pdf' #'svg'
            filename = 'report_%s_%s_%s.%s'%(subject,behavSession,tetrodeClusterName,figformat)
            fulloutputDir = outputDir+subject +'/'
            fullFileName = os.path.join(fulloutputDir,filename)

            directory = os.path.dirname(fulloutputDir)
            if not os.path.exists(directory): #makes sure output folder exists
                os.makedirs(directory)
            #print 'saving figure to %s'%fullFileName
            plt.gcf().savefig(fullFileName,format=figformat)

            #plt.show()

        except:
            print "error with session "+oneCell.behavSession
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
    
    plt.ylabel('Trials')
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

    plt.xlabel('Time from sound onset (s)')
    plt.ylabel('Firing rate (spk/sec)')


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
    
    plt.ylabel('Trials')
    plt.title('Movement Aligned')

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

    plt.xlabel('Time from center poke out (s)')
    plt.ylabel('Firing rate (spk/sec)')




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

    trialsEachCond = np.c_[highFreq,trialsToUseLeft,trialsToUseRight,lowFreq]; colorEachCond = ['b','r','g','y']

    extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
    
    plt.ylabel('Trials')
    plt.title('All Frequencies')

def hist_sound_allFreq_switching():
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

    trialsEachCond = np.c_[highFreq,trialsToUseLeft,trialsToUseRight,lowFreq]; colorEachCond = ['b','r','g','y']

    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    smoothWinSize = 3
    extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,
                         colorEachCond=colorEachCond,linestyle=None,linewidth=2,downsamplefactor=1)

    plt.xlabel('Time from sound onset (s)')
    plt.ylabel('Firing rate (spk/sec)')

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
    
    plt.ylabel('Trials')
    plt.title('Blocks Movement Aligned')

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

    plt.xlabel('Time from center out poke (s)')
    plt.ylabel('Firing rate (spk/sec)')


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
    
    plt.ylabel('Trials')
    plt.title('Blocks')

def hist_sound_block_switching():
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

    plt.xlabel('Time from sound onset (s)')
    plt.ylabel('Firing rate (spk/sec)')



def modulation_index_switching():
    global titleText
    global modIDict
    global modSigDict
    global modDirectionScoreDict
    clusterNumber = (tetrode-1)*clusNum+(cluster-1)

    titleText = 'Mod Index: '+str(round(modIDict[behavSession][clusterNumber],3))+', sig (p val): '+str(round(modSigDict[behavSession][clusterNumber],3))+', Mod Direction Score: '+str(modDirectionScoreDict[behavSession][clusterNumber])


            

main()
