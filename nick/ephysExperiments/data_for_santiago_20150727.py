'''
This file will contain an example showing how to use EphysExperiment to process data from an experiment
'''
import jaratoolbox
import jaratoolbox.test.nick.ephysExperiments.ephys_experiment_v3 as ee3
import jaratoolbox.test.nick.ephysExperiments.recordingday as rd
from jaratoolbox import spikesanalysis
import matplotlib.pyplot as plt
reload(ee3)

#Initialize a Recording object to hold the session info 
#The recording session from pinp003 on 2015-06-24 had good responses. 
recording_experiment = rd.Recording(animalName='pinp003',
                                    date='2015-06-24',
                                    experimenter='nick',
                                    paradigm='laser_tuning_curve')

#Site 1 from this day has good sound and laser responses
site1 = recording_experiment.add_site(depth = 3543, goodTetrodes = [6])

#Handles to the sessions that were recorded at this site (for easy access to the session info)
s1NB = site1.add_session('15-22-29', None, 'Noise bursts at 0.3amp')
s1LP = site1.add_session('15-25-08', None, 'Laser pulses at 1mW')
s1LT = site1.add_session('15-27-37', None, 'Trains of laser pulses at 1mW')
s1TC = site1.add_session('15-31-48', 'a', 'Tuning curve, 4fpo from 2kHz to 40kHz, 4 ints between 40-70dB')
s1BF = site1.add_session('15-45-22', 'b', 'Best freq (~9kHz) at 70dB')

###Good clusters at this site: TT6c3, which is sound and laser responsive,  and TT6c6, which looks like it is indirectly excited by the laser. 




#Initialize an EphysExperiment object to retrieve the data
ex0624 = ee3.EphysExperiment('pinp003', '2015-06-24', experimenter = 'nick')

#We can use the EphysExperiment to retrieve spike data, event data, and behavior data. 

#We can pass session handles directly to the EphysExperiment object and get data
#Spike data for the noise burst session
#This method automatically converts spike times to seconds unless you tell it not to.
spikeDataNB = ex0624.get_session_spike_data_one_tetrode(s1NB, tetrode=6)

#Event data for the noise burst session. These timestamps are NOT automatically converted to seconds
eventDataNB = ex0624.get_session_event_data(s1NB)

#Find the event onset times. This method converts the times to seconds unless you tell it not to.
#This method also excludes event onset times that are seperated by less than 0.5sec, and this is 
#hard coded for now. 
eventOnsetTimes = ex0624.get_event_onset_times(eventDataNB)

#Plot a raster plot for the noise burst session

spikeTimestamps = spikeDataNB.timestamps

#The spikeData object will have clusters if clustering has been performed, so we can limit to a single cluster here. 
#Lets look at the sound and laser responsive cluster TT6c3

spikeTimestamps = spikeTimestamps[spikeDataNB.clusters==3]

timeRange = [-0.5, 1]
spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimes,timeRange)

plt.figure()
plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.', ms=1)

plt.show()



#Will plot the waveforms of spikes in a certain time range after an event
from jaratoolbox import spikesorting

indexTR = [0, 0.1]
spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial, spikeIndex = spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimes,indexTR, spikeindex=True)
waves = spikeDataNB.samples[spikeIndex]

figure()
spikesorting.plot_waveforms(waves)


 

#For a session that has behavior data, we can use the object to get the behavior data
#This is the behavior data for the best frequency presentation. 
#At this site, the TC and BF sessions have saved behavior data
bdata = ex0624.get_session_behav_data(s1BF)


#We can also pass ephys filenames, with or without the date attached, to the object instead of handles. 
#Lets look at the LP session for TT6c3
spikeDataLP = ex0624.get_session_spike_data_one_tetrode('2015-06-24_15-25-08', 6)
spikeTimesLP = spikeDataLP.timestamps[spikeDataLP.clusters==3]

#Since the object knows the date, we can also do:
spikeDataLP = ex0624.get_session_spike_data_one_tetrode('15-25-08', 6)

#All of the methods to get data (get_session_spike_data_one_tetrode, get_event_data, and get_session_behav_data
#can take either a session object, a full session filename string with the date, or a string with the 
#time stamp only. NOTE that if you are passing a session filename string to get_session_behav_data, you must 
#also pass the behavior file identifier. When passing an object this info is passed as well. 

#Getting the behavior data for the tuning curve session by passing a full filename string:

bdata_tc = ex0624.get_session_behav_data('2015-06-24_15-31-48', 'a')



