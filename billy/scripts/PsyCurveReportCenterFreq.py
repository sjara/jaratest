'''
raster and histogram for switching task
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
import matplotlib.pyplot as plt
from jaratoolbox import spikesorting_ISIValues as spikesorting #CHANGE THIS?????
import sys
import importlib

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)


SAMPLING_RATE=30000.0

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes

outputDir = '/home/billywalker/Pictures/psyCurve_reports/centerFreq/'
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.010 # Size of each bin in histogram in seconds

timeRange = [-0.3,0.7] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'



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
print "PsyCurveReportCenterFreq"
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

    for cellID in range(0,numOfCells):
            oneCell = allcells.cellDB[cellID]##########!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #try:#######################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if (behavSession != oneCell.behavSession):


                subject = oneCell.animalName
                behavSession = oneCell.behavSession
                ephysSession = oneCell.ephysSession
                ephysRoot = os.path.join(ephysRootDir,subject)

                print behavSession

                # -- Load Behavior Data --
                behaviorFilename = loadbehavior.path_to_behavior_data(subject=subject,paradigm=paradigm,sessionstr=behavSession)
                bdata = loadbehavior.BehaviorData(behaviorFilename)
                numberOfTrials = len(bdata['choice'])
                #print 'numberTrials ',numberOfTrials############################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
                #print 'missing ',len(missingTrials)############################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # Remove missing trials
                bdata.remove_trials(missingTrials)


                possibleFreq = np.unique(bdata['targetFrequency'])
                numberOfFrequencies = len(possibleFreq)
                centerFrequencies = [(numberOfFrequencies/2-1),numberOfFrequencies/2]

                #################################################################################################
                centerOutTimes = bdata['timeCenterOut'] #This is the times that the mouse goes out of the center port
                soundStartTimes = bdata['timeTarget'] #This gives an array with the times in seconds from the start of the behavior paradigm of when the sound was presented for each trial
                timeDiff = centerOutTimes - soundStartTimes
                #print 'timeDiff ',len(timeDiff)############################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                #print 'eventOnsetTimes ',len(eventOnsetTimes)############################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
                ax1 = plt.subplot2grid((7,6), (6,0), colspan = 2)
                spikesorting.plot_isi_loghist(spkData.spikes.timestamps)
                ax3 = plt.subplot2grid((7,6), (6,4), colspan = 2)
                spikesorting.plot_events_in_time(spkData.spikes.timestamps)
                samples = spkData.spikes.samples.astype(float)-2**15
                samples = (1000.0/spkData.spikes.gain[0,0]) *samples
                ax2 = plt.subplot2grid((7,6), (6,2), colspan = 2)
                spikesorting.plot_waveforms(samples)


            ###############################################################################
            ax4 = plt.subplot2grid((7,6), (0,0), colspan = 3, rowspan = 2)
            plt.setp(ax4.get_xticklabels(), visible=False)
            raster_sound_psycurve(centerFrequencies[0])
            ax5 = plt.subplot2grid((7,6), (2,0), colspan = 3, sharex=ax4)
            hist_sound_psycurve(centerFrequencies[0])
            ax6 = plt.subplot2grid((7,6), (0,3), colspan = 3, rowspan = 2)
            plt.setp(ax6.get_xticklabels(), visible=False)
            raster_sound_psycurve(centerFrequencies[1])
            ax7 = plt.subplot2grid((7,6), (2,3), colspan = 3, sharex=ax6)
            hist_sound_psycurve(centerFrequencies[1])

            ax8 = plt.subplot2grid((7,6), (3,0), colspan = 3, rowspan = 2)
            plt.setp(ax8.get_xticklabels(), visible=False)
            raster_movement_psycurve(centerFrequencies[0])
            ax9 = plt.subplot2grid((7,6), (5,0), colspan = 3, sharex=ax8)
            hist_movement_psycurve(centerFrequencies[0])
            ax10 = plt.subplot2grid((7,6), (3,3), colspan = 3, rowspan = 2)
            plt.setp(ax10.get_xticklabels(), visible=False)
            raster_movement_psycurve(centerFrequencies[1])
            ax11 = plt.subplot2grid((7,6), (5,3), colspan = 3, sharex=ax10)
            hist_movement_psycurve(centerFrequencies[1])
            ###############################################################################
            #plt.tight_layout()
            
            modulation_index_psycurve(centerFrequencies)
            plt.suptitle(titleText)

            tetrodeClusterName = 'T'+str(oneCell.tetrode)+'c'+str(oneCell.cluster)
            plt.gcf().set_size_inches((8.5,11))
            figformat = 'png' #'png' #'pdf' #'svg'
            filename = 'report_centerFreq_%s_%s_%s.%s'%(subject,behavSession,tetrodeClusterName,figformat)
            fulloutputDir = outputDir+subject +'/'
            fullFileName = os.path.join(fulloutputDir,filename)

            directory = os.path.dirname(fulloutputDir)
            if not os.path.exists(directory):
                os.makedirs(directory)
            #print 'saving figure to %s'%fullFileName
            plt.gcf().savefig(fullFileName,format=figformat)

            #plt.show()

        #except:##############################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #print "error with session "+oneCell.behavSession
            #if (oneCell.behavSession not in badSessionList):####################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                #badSessionList.append(oneCell.behavSession)#######################!!!!!!!!!!!!!!!!!!!!!!

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
    
    plt.ylabel('Trials')
    plt.title('Frequency: '+str(Freq))





def hist_sound_psycurve(Frequency):
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

    plt.xlabel('Time from sound onset (s)')
    plt.ylabel('Firing rate (spk/sec)')


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
    
    plt.ylabel('Trials')



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

    plt.xlabel('Time from center poke out (s)')
    plt.ylabel('Firing rate (spk/sec)')


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
    titleText = 'Small Center Freq: Mod Index: '+firstCenterMI+', sig (p value): '+firstCenterMSig+',  Large Center Freq: Mod Index: '+secondCenterMI+', sig (p value): '+secondCenterMSig


main()
