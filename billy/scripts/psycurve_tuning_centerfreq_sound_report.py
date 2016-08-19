'''
raster and histogram for switching task
Santiago Jaramillo and Billy Walker
'''
from jaratoolbox import celldatabase_quality_tuning as celldatabase
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import ephyscore
import os
import numpy as np
from jaratoolbox import behavioranalysis
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
import matplotlib.pyplot as plt
from jaratoolbox import spikesorting_ISI as spikesorting 
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

sizeRasters = (numRows-sizeClusterPlot)/3
sizeHists = (numRows-sizeClusterPlot)/6

SAMPLING_RATE=30000.0

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes

reportname = 'psycurve_report_centerfreq_sound'
outputDir = '/home/billywalker/Pictures/psyCurve_tuning_centerfreq_sound_reports/'
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.010 # Size of each bin in histogram in seconds

timeRange = [-0.3,0.7] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)
tuning_timeRange = [-0.2,0.5] # In seconds. Time range for tuning rastor plot to plot spikes (around some event onset as 0)

ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'
behaviorDir='/home/billywalker/data/behavior/' #Need this for the tuning curve behavior


class nestedDict(dict):#This is for maxZDict
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value

subject = allcells.cellDB[0].animalName
#########################Load MI File################################
processedDir = os.path.join(settings.EPHYS_PATH,subject+'_processed')
modIFilename = os.path.join(processedDir,'modIndex.txt')
modIFile = open(modIFilename, 'r')
modIDict = nestedDict() #stores all the modulation indices
modSigDict = nestedDict() #stores the significance of the modulation of each cell
behavName = ''
for line in modIFile:
    splitLine = line.split(':')
    if (splitLine[0] == 'Behavior Session'):
        behavName = splitLine[1][:-1]
    elif (splitLine[0] == 'modI'):
        frequency = splitLine[1]
        modIDict[behavName][frequency] = [float(x) for x in splitLine[2].split(',')[0:-1]]
    elif (splitLine[0] == 'modSig'):
        frequency = splitLine[1]
        modSigDict[behavName][frequency] = [float(x) for x in splitLine[2].split(',')[0:-1]]
modIFile.close()


numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
subject = ''
behavSession = ''
ephysSession = ''
tetrode = ''
cluster = ''



bdata = None
eventOnsetTimes = None
spikeTimesFromEventOnset = None
indexLimitsEachTrial = None
spikeTimesFromMovementOnset = None
indexLimitsEachMovementTrial = None
timeDiff = None ###############################!!!!!!!!!!!!!!!!!!!!!!!!!!!!

badSessionList = []#prints bad sessions at end
print 'psycurve_tuning_centerfreq_sound_report'
def main():
    global behavSession
    global subject
    global ephysSession
    global tetrode
    global cluster
    global bdata
    global eventOnsetTimes
    global spikeTimesFromEventOnset
    global indexLimitsEachTrial
    global spikeTimesFromMovementOnset
    global indexLimitsEachMovementTrial
    global tuningBehavior#behavior file name of tuning curve
    global tuningEphys#ephys session name of tuning curve

    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]
        try:
            if (behavSession != oneCell.behavSession):


                subject = oneCell.animalName
                behavSession = oneCell.behavSession
                ephysSession = oneCell.ephysSession
                ephysRoot = os.path.join(ephysRootDir,subject)
                tuningBehavior = oneCell.tuningBehavior
                tuningEphys = oneCell.tuningSession

                print behavSession

                # -- Load Behavior Data --
                behaviorFilename = loadbehavior.path_to_behavior_data(subject=subject,paradigm=paradigm,sessionstr=behavSession)
                bdata = loadbehavior.BehaviorData(behaviorFilename)
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


                possibleFreq = np.unique(bdata['targetFrequency'])
                numberOfFrequencies = len(possibleFreq)
                centerFrequencies = [(numberOfFrequencies/2-1),numberOfFrequencies/2]

                #################################################################################################
                centerOutTimes = bdata['timeCenterOut'] #This is the times that the mouse goes out of the center port
                soundStartTimes = bdata['timeTarget'] #This gives an array with the times in seconds from the start of the behavior paradigm of when the sound was presented for each trial
                timeDiff = centerOutTimes - soundStartTimes
                
                if (len(eventOnsetTimes) < len(timeDiff)):
                    eventOnsetTimesCenter = eventOnsetTimes + timeDiff[:-1]
                elif (len(eventOnsetTimes) > len(timeDiff)):
                    eventOnsetTimesCenter = eventOnsetTimes[:-1] + timeDiff
                else:
                    eventOnsetTimesCenter = eventOnsetTimes + timeDiff
                #################################################################################################


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
                spikesorting.plot_events_in_time(spkData.spikes.timestamps)
                samples = spkData.spikes.samples.astype(float)-2**15
                samples = (1000.0/spkData.spikes.gain[0,0]) *samples
                ax2 = plt.subplot2grid((numRows,numCols), ((numRows-sizeClusterPlot),(numCols/3)), colspan = (numCols/3))
                spikesorting.plot_waveforms(samples)


            ###############################################################################
            ax4 = plt.subplot2grid((numRows,numCols), (0,0), colspan = (numCols/2), rowspan = 3*sizeRasters)
            #plt.setp(ax4.get_xticklabels(), visible=False)
            #raster_sound_psycurve(centerFrequencies[0])
            raster_tuning(ax4)
            axvline(x=0, ymin=0, ymax=1, color='r')
            plt.gca().set_xlim(tuning_timeRange)

            #ax5 = plt.subplot2grid((7,6), (2,0), colspan = 3, sharex=ax4)
            #hist_sound_psycurve(centerFrequencies[0])

            ax6 = plt.subplot2grid((numRows,numCols), (0,(numCols/2)), colspan = (numCols/2), rowspan = sizeRasters)
            plt.setp(ax6.get_xticklabels(), visible=False)
            plt.setp(ax6.get_yticklabels(), visible=False)
            raster_sound_psycurve(centerFrequencies[0])
            plt.title('Frequency Top: '+str(possibleFreq[centerFrequencies[0]])+'Hz Bottom: '+str(possibleFreq[centerFrequencies[1]])+'Hz')
            
            ax7 = plt.subplot2grid((numRows,numCols), (sizeRasters,(numCols/2)), colspan = (numCols/2), rowspan = sizeHists, sharex=ax6)
            hist_sound_psycurve(centerFrequencies[0],ax7)
            ax7.yaxis.tick_right()
            ax7.yaxis.set_ticks_position('both')
            plt.setp(ax7.get_xticklabels(), visible=False)
            plt.gca().set_xlim(timeRange)

            #ax8 = plt.subplot2grid((7,6), (3,0), colspan = 3, rowspan = 2)
            #plt.setp(ax8.get_xticklabels(), visible=False)
            #raster_movement_psycurve(centerFrequencies[0])
            #ax9 = plt.subplot2grid((7,6), (5,0), colspan = 3, sharex=ax8)
            #hist_movement_psycurve(centerFrequencies[0])

            ax10 = plt.subplot2grid((numRows,numCols), ((sizeRasters+sizeHists),(numCols/2)), colspan = (numCols/2), rowspan = sizeRasters)
            plt.setp(ax10.get_xticklabels(), visible=False)
            plt.setp(ax10.get_yticklabels(), visible=False)
            raster_sound_psycurve(centerFrequencies[1])

            ax11 = plt.subplot2grid((numRows,numCols), ((2*sizeRasters+sizeHists),(numCols/2)), colspan = (numCols/2), rowspan = sizeHists, sharex=ax10)
            hist_sound_psycurve(centerFrequencies[1],ax11)
            plt.xlabel('Time from sound onset (s)')
            ax11.yaxis.tick_right()
            ax11.yaxis.set_ticks_position('both')
            #plt.setp(ax11.get_yticklabels(), visible=False)
            plt.gca().set_xlim(timeRange)
            ###############################################################################
            #plt.tight_layout()
            
            modulation_index_psycurve(centerFrequencies)
            plt.suptitle(titleText)

            tetrodeClusterName = 'T'+str(oneCell.tetrode)+'c'+str(oneCell.cluster)
            plt.gcf().set_size_inches((8.5,11))
            figformat = 'png' #'png' #'pdf' #'svg'
            filename = reportname+'_%s_%s_%s.%s'%(subject,behavSession,tetrodeClusterName,figformat)
            fulloutputDir = outputDir+subject +'/'
            fullFileName = os.path.join(fulloutputDir,filename)

            directory = os.path.dirname(fulloutputDir)
            if not os.path.exists(directory):
                os.makedirs(directory)
            #print 'saving figure to %s'%fullFileName
            plt.gcf().savefig(fullFileName,format=figformat)

            #plt.show()

        except:
            if (oneCell.behavSession not in badSessionList):
                badSessionList.append(oneCell.behavSession)

    print 'error with sessions: '
    for badSes in badSessionList:
        print badSes




def raster_sound_psycurve(Frequency):
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']

    possibleFreq = np.unique(bdata['targetFrequency'])

    Freq = possibleFreq[Frequency]
    oneFreq = bdata['targetFrequency'] == Freq

    trialsToUseRight = rightward & oneFreq
    trialsToUseLeft = leftward & oneFreq

    trialsEachCond = np.c_[trialsToUseLeft,trialsToUseRight]; colorEachCond = ['r','g']
    extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
    
    #plt.ylabel('Trials')
    #plt.title('Frequency: '+str(Freq))




def hist_sound_psycurve(Frequency,ax):
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']

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
                         colorEachCond=colorEachCond,linestyle=None,linewidth=3,downsamplefactor=1)

    ax.axvspan(0.0, 0.1, color=[0.8,0.8,0.8], alpha=0.5, lw=0)
    #plt.xlabel('Time from sound onset (s)')
    #plt.ylabel('Firing rate (spk/sec)')


def raster_movement_psycurve(Frequency):
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']

    possibleFreq = np.unique(bdata['targetFrequency'])

    Freq = possibleFreq[Frequency]
    oneFreq = bdata['targetFrequency'] == Freq

    trialsToUseRight = rightward & oneFreq
    trialsToUseLeft = leftward & oneFreq

    trialsEachCond = np.c_[trialsToUseLeft,trialsToUseRight]; colorEachCond = ['r','g']
    extraplots.raster_plot(spikeTimesFromMovementOnset,indexLimitsEachMovementTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
    
    #plt.ylabel('Trials')



def hist_movement_psycurve(Frequency):
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']

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
                         colorEachCond=colorEachCond,linestyle=None,linewidth=3,downsamplefactor=1)

    #plt.xlabel('Time from center poke out (s)')
    #plt.ylabel('Firing rate (spk/sec)')


    '''
    if ((Frequency == numberOfFrequencies/2) or (Frequency == (numberOfFrequencies/2 - 1))):
            freqFile = 'Center_Frequencies'
    else:
            freqFile = 'Outside_Frequencies'

            
    tetrodeClusterName = 'T'+str(oneCell.tetrode)+'c'+str(oneCell.cluster)
    plt.gcf().set_size_inches((8.5,11))
    figformat = 'png' #'png' #'pdf' #'svg'
    filename = 'rast_%s_%s_%s_%s.%s'%(subject,behavSession,Freq,tetrodeClusterName,figformat)
    fulloutputDir = outputDir+subject+'/'+ freqFile +'/'
    fullFileName = os.path.join(fulloutputDir,filename)
    
    directory = os.path.dirname(fulloutputDir)
    if not os.path.exists(directory):
        os.makedirs(directory)
    print 'saving figure to %s'%fullFileName
    #plt.gcf().savefig(fullFileName,format=figformat)
    '''



def modulation_index_psycurve(centerFrequencies):
    global titleText
    global modIDict
    global modSigDict
    global cluster
    global tetrode
    clusterNumber = (tetrode-1)*clusNum+(cluster-1)

    possibleFreq = np.unique(bdata['targetFrequency'])
    Freq1 = str(possibleFreq[centerFrequencies[0]])
    firstCenterMI = str(round(modIDict[behavSession][Freq1][clusterNumber],3))
    firstCenterMSig = str(round(modSigDict[behavSession][Freq1][clusterNumber],3))

    Freq2 = str(possibleFreq[centerFrequencies[1]])
    secondCenterMI = str(round(modIDict[behavSession][Freq2][clusterNumber],3))
    secondCenterMSig = str(round(modSigDict[behavSession][Freq2][clusterNumber],3))
    titleText = 'Low Center Freq: Mod Index: '+firstCenterMI+', (p='+firstCenterMSig+'),  High Center Freq: Mod Index: '+secondCenterMI+', (p='+secondCenterMSig+')'


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
