'''
loadEphysData.py
Load ephys events
author: Billy Walker
'''


import allcells_test055 as allcells
from jaratoolbox import ephyscore
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
import numpy as np
from pylab import * #I SHOULD CHANGE THIS. EFFECTS ARGSORT
import os

###########################
#ASSUMPTIONS
#There is a sound onset in every trial
###########################

#####################################################################################################################################################################
#PARAMETERS
#####################################################################################################################################################################

outputDir = '/home/billywalker/Pictures/psyCurve/'

timeLabeling = 'Time from sound Onset (sec)'

ephysRootDir='/home/billywalker/data/ephys/'
ephysSessionArray = ['2015-02-17_12-26-10','2015-02-21_20-08-51','2015-02-23_15-31-40']#['2014-12-19_14-36-45','2014-12-22_11-42-00','2014-12-23_15-50-14','2014-12-24_17-11-53','2014-12-26_18-07-12']#'2014-12-20_22-37-24','2014-12-26_18-07-12'

#subject = 'test017'
experimenter = 'santiago'
paradigm = '2afc'
sessionstrArray = ['20150217a','20150221a','20150223a']#['20141219a','20141222a','20141223a','20141224a','20141226a']#'20141220a','20141226a'

#tetrodeID = 1 #Which tetrode to plot
numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
responseRange = [0.10,0.40] #range of time to count spikes in after event onset
timeRange=[-0.5,1] #In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)
binTime = 0.1 #Size of each bin in histogram in seconds
nametrialsToUse = 'AllFreq'
Frequency = 0 #This chooses which frequency to look at, numbered out of possible frequencies starting with the lowest frequency as number 0
eventID = 0 #THIS IS THE CHANNEL THAT YOU CARE ABOUT. for example, channel 0 could be the sound presentation and channel 1 could be the trial period
#####################################################################################################################################################################
#####################################################################################################################################################################


# -- Global variables --
SAMPLING_RATE=30000.0



# -- Make np.array of time ranges for bins
startTime = float(timeRange[0]) #makes sure that these are floats so division works as expected
endTime = float(timeRange[1])
fullTime = endTime - startTime
numberOfBins = int((fullTime//binTime)+1)
binTimeRanges = np.empty([numberOfBins,2]) #Gives np.array of time ranges for each bin
xCoordinatesPlot = np.empty(numberOfBins)
for indBin in range(0,numberOfBins):
    xCoordinatesPlot[indBin]=startTime+indBin*binTime
    binTimeRanges[indBin]=np.array([(startTime+indBin*binTime),(startTime+(indBin+1)*binTime)])




subject = ''
behavSession = ''
ephysSession = ''



	
for cellID in range(0,numOfCells):
	
	oneCell = allcells.cellDB[cellID]

	if (behavSession != oneCell.behavSession):

		subject = oneCell.animalName
		behavSession = oneCell.behavSession
		ephysSession = oneCell.ephysSession
                ephysRoot = ephysRootDir+subject+'/'

		# -- Load Behavior Data --
		behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
		bdata = loadbehavior.BehaviorData(behaviorFilename)

		numberOfTrials = len(bdata['choice'])
		targetFreqs = bdata['targetFrequency']

		#This gives an array of all frequencies presented
		possibleFreq = np.unique(bdata['targetFrequency'])

		#This gives an array with true and indices where the mouse made a correct decision
		correct = bdata['outcome']==bdata.labels['outcome']['correct']
		#This gives an array with true and indices where the mouse made a incorrect decision
		incorrect = bdata['outcome']==bdata.labels['outcome']['error']

		#This gives an array with true at indices of trials that are correct and went right
		rightward = bdata['choice']==bdata.labels['choice']['right']
		correctRightward = correct*rightward

		#This gives an array with true at indices of trials that are correct and went left
		leftward = bdata['choice']==bdata.labels['choice']['left']
		correctLeftward = correct*leftward

		#This gives an array with true at indices of trials that are incorrect and went right
		incorrectRightward = incorrect*rightward

		#This gives an array with true at indices of trials that are incorrect and went left
		incorrectLeftward = incorrect*leftward


		###############################################################################################################################################################################
		trialsToUse1 = leftward #This is an array of 1's and 0's to decide which trials to count spikes in and compare to the other trials
		trialsToUse2 = rightward #This is an array of 1's and 0's to decide which trials to count spikes in and compare to the other trials
		##################################################################################################################################################################################



		# -- Load event data and convert event timestamps to ms --
		ephysDir = os.path.join(ephysRoot, ephysSession)
		eventFilename=os.path.join(ephysDir, 'all_channels.events')
		events = loadopenephys.Events(eventFilename) # Load events data
		eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 
		multipleEventOnset=np.array(events.eventID)  #loads the onset times of all events (matches up with eventID to say if event 1 went on (1) or off (0)
		eventChannel = np.array(events.eventChannel) #loads the ID of the channel of the event. For example, 0 is sound event, 1 is trial event, 2 ...


	# -- Load Spike Data From Certain Cluster --
	spkData = ephyscore.CellData(oneCell)
	spkTimeStamps = spkData.spikes.timestamps



	# -- Only use event onset times of one event --
	oneEvent = eventChannel==eventID #This picks out which channel you care about if there is more that one event
	eventOnset = multipleEventOnset*oneEvent #This keeps the correct size of the array to match eventTimes and picks out the onset of the channel you want

	while (numberOfTrials < np.sum(eventOnset)):
		eventOnset = eventOnset[:-1]

	eventOnsetTimes = eventTimes[eventOnset == 1] #This gives only the times of the onset of the channel you want

	eventOnsetTimesTrials1 = eventOnsetTimes[trialsToUse1==1]
	eventOnsetTimesTrials2 = eventOnsetTimes[trialsToUse2==1]



	# -- Convert spike data into np.array's --
	(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)
	(spikeTimesFromEventOnsetTrials1,trialIndexForEachSpikeTrials1,indexLimitsEachTrialTrials1) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimesTrials1,timeRange)
	(spikeTimesFromEventOnsetTrials2,trialIndexForEachSpikeTrials2,indexLimitsEachTrialTrials2) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimesTrials2,timeRange)
	''' spikesanalysis.eventlocked_spiketimes
	    Create a vector with the spike timestamps w.r.t. events onset.

	    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = 
		eventlocked_spiketimes(timeStamps,eventOnsetTimes,timeRange)

	    timeStamps: (np.array) the time of each spike.
	    eventOnsetTimes: (np.array) the time of each instance of the event to lock to.
	    timeRange: (list or np.array) two-element array specifying time-range to extract around event.

	    spikeTimesFromEventOnset: 1D array with time of spikes locked to event.
	    trialIndexForEachSpike: 1D array with the trial corresponding to each spike.
	       The first spike index is 0.
	    indexLimitsEachTrial: [2,nTrials] range of spikes for each trial. Note that
	       the range is from firstSpike to lastSpike+1 (like in python slices)
	    spikeIndices
	'''


	# -- Find the number of spikes in each bin --
	spikeNumberInBinPerTrial = np.empty([numberOfBins,numberOfTrials])
	for i,binRange in enumerate(binTimeRanges):
	    spikeNumberInBinPerTrial[i] = spikesanalysis.count_spikes_in_range(spikeTimesFromEventOnset,indexLimitsEachTrial,binRange) #array of the number of spikes in range for each trial
	''' spikesanalysis.count_spikes_in_range
	    Count number of spikes on each trial in a given time range.

	       spikeTimesFromEventOnset: vector of spikes timestamps with respect
		 to the onset of the event.
	       indexLimitsEachTrial: each column contains [firstInd,lastInd+1] of the spikes on a trial.
	       timeRange: time range to evaluate. Spike times exactly at the limits are not counted.

	       returns nSpikes
	'''

	######################################################################################################################
	#THIS IS FOR ALL FREQUENCIES
	# -- Pick which trials you care about in counting spikes --
	spikeMeanInBin1 = np.empty(numberOfBins) #This will hold the mean number of spikes in each bin or time range for the trialsToUse1
	spikeMeanInBin2 = np.empty(numberOfBins) #This will hold the mean number of spikes in each bin or time range for the trialsToUse2
	for indBin, spikeCounts in enumerate(spikeNumberInBinPerTrial):
	    spikeMeanInBin1[indBin] = np.mean(np.append(spikeCounts[trialsToUse1==1],0))  #The append 0 is just for the edge case that there are no trials to use so np.mean does not give a nan.
	    spikeMeanInBin2[indBin] = np.mean(np.append(spikeCounts[trialsToUse2==1],0))
	######################################################################################################################






	###################################################################################################################################################################################
	#####################################################THIS IS FOR THE RASTOR PLOT###################################################################################################
	###################################################################################################################################################################################

	targetFreqsTrials1 = targetFreqs[trialsToUse1==1]
	targetFreqsTrials2 = targetFreqs[trialsToUse2==1]


	sortedTrials1 = [] #array that sorts trials for different frequencies
	for indf1,oneFreq1 in enumerate(possibleFreq): #indf is index of this freq and oneFreq is the frequency
	    indsThisFreq1 = np.flatnonzero(targetFreqsTrials1==oneFreq1) #this gives indices of this frequency
	    sortedTrials1.append(indsThisFreq1) #adds all indices to a list called sortedTrials
	

	sortedTrials2 = [] #array that sorts trials for different frequencies
	for indf2,oneFreq2 in enumerate(possibleFreq): #indf is index of this freq and oneFreq is the frequency
	    indsThisFreq2 = np.flatnonzero(targetFreqsTrials2==oneFreq2) #this gives indices of this frequency
	    sortedTrials2.append(indsThisFreq2) #adds all indices to a list called sortedTrials
            
            
        colorEachFreq = []
        strPossibleFreq = []
        for indFreq, Freq in enumerate(possibleFreq):
            colorEachFreq.append('b')
            colorEachFreq.append('g')
            strPossibleFreq.append(str(Freq))

	clf()
	rastorFreq1 = plt.subplot2grid((3,4), (0, 0), colspan=2, rowspan=2)
	extraplots.raster_plot(spikeTimesFromEventOnsetTrials1, indexLimitsEachTrialTrials1, timeRange, sortedTrials1, labels=strPossibleFreq,colorEachCond = colorEachFreq)

	rastorFreq2 = plt.subplot2grid((3,4), (0, 2), colspan=2, rowspan=2)
	extraplots.raster_plot(spikeTimesFromEventOnsetTrials2, indexLimitsEachTrialTrials2, timeRange, sortedTrials2, labels=strPossibleFreq,colorEachCond = colorEachFreq)
	


	###################################################################################################################################################################################
	#####################################################THIS IS FOR THE HISTOGRAM#####################################################################################################
	###################################################################################################################################################################################

	histogram3 = plt.subplot2grid((3,4), (2, 0), colspan=2)
	bar(xCoordinatesPlot,spikeMeanInBin1, width=binTime)
	ylabel('trialsToUse1, Average number of spikes in bin size {} sec'.format(binTime))
	xlabel(timeLabeling)

	histogram4 = plt.subplot2grid((3,4), (2, 2), colspan=2)
	bar(xCoordinatesPlot,spikeMeanInBin2, width=binTime)
	ylabel('trialsToUse2, Average number of spikes in bin size {} sec'.format(binTime))
	xlabel(timeLabeling)

	#show()

	tetrodeID = oneCell.tetrode
	#clusterName = 'cluster'+str(oneCell.cluster)
	#tetrodeName = 'TT'+str(tetrodeID)
	tetrodeClusterName = 'T'+str(tetrodeID)+'c'+str(oneCell.cluster)
	plt.gcf().set_size_inches((8.5,11))
	figformat = 'png' #'png' #'pdf' #'svg'
	filename = 'psy_%s_%s_%s_%s.%s'%(subject,behavSession,tetrodeClusterName,nametrialsToUse,figformat)
	fulloutputDir = outputDir+subject+'/'+'cluster'+'/'
	fullFileName = os.path.join(fulloutputDir,filename)
	print 'saving figure to %s'%fullFileName
	plt.gcf().savefig(fullFileName,format=figformat)
