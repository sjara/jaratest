from jaratoolbox.test.nick.database import dataloader
from jaratoolbox.test.nick.database import dataplotter
from jaratoolbox.test.nick.database import cellDB
from jaratoolbox import spikesorting
from matplotlib import pyplot as plt
from jaratoolbox import spikesanalysis
figdb = cellDB.CellDB()
figdbFn = '/home/nick/data/database/figure_cells/figure_cells.json' #Change to path on your comp
figdb.load_from_json(figdbFn)
#This database has some cells that I gave santiago for the RO1 grant

#Below is a site with a good cortex cell that has a nice AM response


ac = cellDB.Experiment('pinp009', '2016-01-27', experimenter='nick', defaultParadigm='am_tuning_curve')
site2 = ac.add_site(depth=863, tetrodes=[4, 5, 6])
site2.add_session('17-14-57', None, 'noiseburst')
site2.add_session('17-17-35', None, 'laserpulse') #0.2-0.5mW
site2.add_session('17-19-44', None, 'lasertrain') #0.2-0.5mW
site2.add_session('17-23-19', 'acb', 'AM')
site2.add_session('17-42-52', None, 'laserpulse2') #0.2-0.5mW
site2.add_session('17-45-04', None, 'lasertrain2') #0.2-0.5mW
site2.add_session('17-49-18', 'acc', 'tuningCurve') #only 60dB
site2.add_session('17-53-22', 'acd', 'tuningCurve2') #30-60dB
site2.add_cluster(6, 2) #Unit with nice waveform and AM responses

figdb.add_clusters(site2.clusterList) #This cell is now cell 10 in the db

figdb[9].get_session_types()

spikeData, eventData, behavData = loader.get_cluster_data(figdb[10], 'AM')
spikeTimestamps = spikeData.timestamps
eventOnsetTimes = loader.get_event_onset_times(eventData)

currentFreq = behavData['currentFreq']
possibleFreq = np.unique(currentFreq)


##############################################
#This extracts the relevant spikes for each freq and plots the cycle histogram
freq = 4
select = flatnonzero(currentFreq==freq)

timeRange = [0, 0.5]
spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
    spikeTimestamps, eventOnsetTimes, timeRange)

selectspikes = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, select)]
selectinds = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, select)]

squeezedinds=array([list(unique(selectinds)).index(x) for x in selectinds])

plot(selectspikes, squeezedinds, 'k.')

#This plots the cycle histogram
radsPerSec=freq*2*np.pi
spikeRads = (selectspikes*radsPerSec)%(2*np.pi)
hist(spikeRads, bins=10*np.pi, histtype='stepfilled', color='k')
xlim([0, 2*np.pi])


#Calculating vector strength
strength, phase = vectorstrength(selectspikes, 1.0/freq)


#Loop for all freqs
#########################################################################
#This plots the vector strength as a function of the modulation frequency

def AM_vector_strength(spikeTimeStamps, eventOnsetTimes, behavData, timeRange):

    currentFreq = behavData['currentFreq']
    possibleFreq = np.unique(currentFreq)

    vs_array=array([])
    timeRange = [0, 0.5]
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeTimestamps, eventOnsetTimes, timeRange)

    for freq in possibleFreq:

        select = flatnonzero(currentFreq==freq)
        selectspikes = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, select)]
        selectinds = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, select)]
        squeezedinds=array([list(unique(selectinds)).index(x) for x in selectinds])
        strength, phase = vectorstrength(selectspikes, 1.0/freq)
        vs_array=np.concatenate((vs_array, array([strength])))

    return vs_array


timeRange = [0, 0.5]
vs_array = AM_vector_strength(spikeTimestamps, eventOnsetTimes, behavData, timeRange)

ax=subplot(111)
ax.plot(vs_array, 'k-', linewidth=3)
ax.set_xticks(range(len(possibleFreq)))
ax.set_xticklabels(['{:3.0f}'.format(x) for x in possibleFreq])
ax.set_xlabel('Modulation Frequency')
ax.set_ylabel('Vector Strength')




#####################################################################
#Plot the average evoked firing rate as a function of the modulation freq

def average_AM_firing_rate(spikeTimeStamps, eventOnsetTimes, behavData, timeRange):

    currentFreq = behavData['currentFreq']
    possibleFreq = np.unique(currentFreq)


    fr_array=array([])
    #Only need to calculate this once, the loop then selects for each freq
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
        spikeTimestamps, eventOnsetTimes, timeRange)

    for freq in possibleFreq:
        select = flatnonzero(currentFreq==freq)
        selectspikes = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, select)]
        selectinds = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, select)]
        selectlimits = indexLimitsEachTrial[:, select]


        numSpikesEachTrial = squeeze(diff(selectlimits, axis=0))
        spikeRateEachTrial = numSpikesEachTrial / float(timeRange[1]-timeRange[0])
        averageFR = spikeRateEachTrial.mean()

        fr_array=np.concatenate((fr_array, array([averageFR])))

    return fr_array


timeRange = [0, 0.5]
fr_array = average_AM_firing_rate(spikeTimestamps, eventOnsetTimes, behavData, timeRange)

ax=subplot(111)
ax.plot(fr_array, 'k-', linewidth=3)
ax.set_xticks(range(len(possibleFreq)))
ax.set_xticklabels(['{:3.0f}'.format(x) for x in possibleFreq])
ax.set_xlabel('Modulation Frequency')
ax.set_ylabel('Average Firing Rate (spks/sec)')



#############################################################################
timeRange=[0, 0.5]
spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimes,timeRange)

from jaratoolbox import behavioranalysis

trialsEachType = behavioranalysis.find_trials_each_type(currentFreq, np.unique(currentFreq))

#I want to get the raster for one frequency. I am certain I am re-inventing
#the wheel here but it has been a while. 

#Trials where the freq was 4


#Indices of spikes that came from that trial




# np.flatnonzero(trialIndexForEachSpike==8)

# #Spiketimes from event onset for trial 8
# spikesTrial8 = spikeTimesFromEventOnset[np.flatnonzero(trialIndexForEachSpike==8)]
# trial=ones([len(spikesTrial8)])
# plot(spikesTrial8, trial, '.')



freq4trials = np.flatnonzero(currentFreq==4)
freq4spikes = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, freq4trials)]
freq4inds = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, freq4trials)]
plot(freq4spikes, freq4inds, '.')

radsPerSec=8*np.pi
spikeRads = (freq4spikes*radsPerSec)%(2*np.pi)

hist(spikeRads, bins=50)





freqEachTrial = behavData['currentFreq']
possibleFreq = np.unique(freqEachTrial)


vsall=np.empty(len(possibleFreq))
orientationall = np.empty(len(possibleFreq))

gridsize=(len(possibleFreq), 2)

for ind, freq in enumerate(possibleFreq):

    freqTrials = np.flatnonzero(currentFreq==freq)
    freqSpikes = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, freqTrials)]

    #Disregard the first 50ms
    freqSpikes = freqSpikes[freqSpikes>0.05]

    freqInds = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, freqTrials)]
    freqInds = freqInds[freqSpikes>0.05]

    ax1 = subplot2grid(gridsize, (ind, 0))
    plot(freqSpikes, freqInds, '.')

    radsPerSec=freq*2*np.pi
    spikeRads = (freqSpikes*radsPerSec)%(2*np.pi)

    ax2=subplot2grid(gridsize, (ind, 1), polar=True)

    n, bins, patches = hist(spikeRads, bins=50)

    vs = vectorstrength(freqSpikes, 1/freq)

    ax2.arrow(0, 0, vs[1], vs[0]*np.max(n), lw=2, edgecolor='red', zorder=100)

    vsall[ind] = vs[0]
    orientationall[ind]=vs[1]




def vectorstrength(events, period):
    '''
    Determine the vector strength of the events corresponding to the given
    period.
    The vector strength is a measure of phase synchrony, how well the
    timing of the events is synchronized to a single period of a periodic
    signal.
    If multiple periods are used, calculate the vector strength of each.
    This is called the "resonating vector strength".
    Parameters
    ----------
    events : 1D array_like
        An array of time points containing the timing of the events.
    period : float or array_like
        The period of the signal that the events should synchronize to.
        The period is in the same units as `events`.  It can also be an array
        of periods, in which case the outputs are arrays of the same length.
    Returns
    -------
    strength : float or 1D array
        The strength of the synchronization.  1.0 is perfect synchronization
        and 0.0 is no synchronization.  If `period` is an array, this is also
        an array with each element containing the vector strength at the
        corresponding period.
    phase : float or array
        The phase that the events are most strongly synchronized to in radians.
        If `period` is an array, this is also an array with each element
        containing the phase for the corresponding period.
    References
    ----------
    van Hemmen, JL, Longtin, A, and Vollmayr, AN. Testing resonating vector
        strength: Auditory system, electric fish, and noise.
        Chaos 21, 047508 (2011);
        doi: 10.1063/1.3670512
    van Hemmen, JL.  Vector strength after Goldberg, Brown, and von Mises:
        biological and mathematical perspectives.  Biol Cybern.
        2013 Aug;107(4):385-96. doi: 10.1007/s00422-013-0561-7.
    van Hemmen, JL and Vollmayr, AN.  Resonating vector strength: what happens
        when we vary the "probing" frequency while keeping the spike times
        fixed.  Biol Cybern. 2013 Aug;107(4):491-94.
        doi: 10.1007/s00422-013-0560-8
    '''
    events = asarray(events)
    period = asarray(period)
    if events.ndim > 1:
        raise ValueError('events cannot have dimensions more than 1')
    if period.ndim > 1:
        raise ValueError('period cannot have dimensions more than 1')

    # we need to know later if period was originally a scalar
    scalarperiod = not period.ndim

    events = atleast_2d(events)
    period = atleast_2d(period)
    if (period <= 0).any():
        raise ValueError('periods must be positive')

    # this converts the times to vectors
    vectors = exp(dot(2j*pi/period.T, events))

    # the vector strength is just the magnitude of the mean of the vectors
    # the vector phase is the angle of the mean of the vectors
    vectormean = mean(vectors, axis=1)
    strength = abs(vectormean)
    phase = angle(vectormean)

    # if the original period was a scalar, return scalars
    if scalarperiod:
        strength = strength[0]
        phase = phase[0]
    return strength, phase
