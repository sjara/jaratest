from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
import numpy as np
from pylab import *
import os

class EphysExperiment():
    def __init__(self, ephys_root, numTetrodes, behavior_directory=None, behav_filename=None):

        '''
        Accepts the root directory containing all of the ephys files
        relevant to a particular experiment, and the directory
        containing the behavior files if these are relevant to the
        experiment.

        Arguments

        ephys_root (string) - The parent directory of all individual
        recording session directories

        numTetrodes (int) - Number of tetrodes

        behavior_directory (string) - Directory containing behavior files
        '''

        self.ephys_root = ephys_root
        self.numTetrodes = numTetrodes

        if behavior_directory != None:
            self.behavior_directory = behavior_directory
            self.behav_filename = behav_filename
            behavDataFileName=os.path.join(behavior_directory,
                                           behav_filename)
            self.bdata=loadbehavior.BehaviorData(behavDataFileName, readmode='full')

    
    def plot_last_session_raster(self, sort=False, tuning=False):
        sessionName = os.listdir(self.ephys_root)[-1]
        self.plot_raster(sessionName, sort=sort, plot_tuning_curve=tuning)

    def plot_raster(self, sessionName, sort=False, plot_tuning_curve=False):

        '''
        Plots the spikes in a particular session with respect to a stimulus

        Arguments

        sessionName (string) - The name of the directory containing the .spikes and
        .events files

        sort (bool) - Whether to sort the spikes by frequency. Requires a behavior data file.

        plot_tuning_curve (bool) - Whether to plot frequency tuning curves.

        '''

        ephysSession=sessionName

        event_filename=os.path.join(ephysSession, 'all_channels.events')
        ev=loadopenephys.Events(self.event_filename)
        eventTimes=np.array(ev.timestamps)/SAMPLING_RATE
        evID=np.array(ev.eventID)
        eventOnsetTimes=eventTimes[evID==1]
        eventOnsetTimes=eventOnsetTimes[:-1] #Remove last started, but
                                             #not finished trial

        if sort:
            freqEachTrial = self.bdata['currentFreq']
            possibleFreq = np.unique(freqEachTrial)

            sortedTrials = []

            for indf,oneFreq in enumerate(possibleFreq):
                indsThisFreq = np.flatnonzero(freqEachTrial==oneFreq)
                sortedTrials = np.concatenate((sortedTrials,indsThisFreq))
            sortingInds = argsort(sortedTrials)

        for ind in range(numTetrodes):
            tetrodeID = ind+1
            spike_filename=os.path.join(ephysSession, 'Tetrode{0}.spikes'.format(tetrodeID))
            sp=loadopenephys.DataSpikes(spike_filename)
            try:  #FIXME: We should keep the code inside the try to a minimum. 
                spkTimeStamps=np.array(sp.timestamps)/SAMPLING_RATE
                (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

                subplot(numTetrodes,1,ind+1)

                if sort:
                    sortedIndexForEachSpike = sortingInds[trialIndexForEachSpike]
                    plot(spikeTimesFromEventOnset, sortedIndexForEachSpike, '.', ms=1)
                else:
                    plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')

                axvline(x=0, ymin=0, ymax=1, color='r')
                if ind == 0:
                    title(ephysSession)
                    #title('Channel {0} spikes'.format(ind+1))
            except AttributeError:  #Spikes files without any spikes will throw an error
                pass

        xlabel('time(sec)')






        
