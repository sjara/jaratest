from jaratoolbox.test.nick.database import dataloader
from jaratoolbox.test.nick.database import dataplotter
from jaratoolbox.test.nick.database import cellDB
from jaratoolbox import spikesorting
from matplotlib import pyplot as plt
figdb = cellDB.CellDB()
figdbFn = '/home/nick/data/database/figure_cells/figure_cells.json' #Change to path on your comp
figdb.load_from_json(figdbFn)

'''
This file will load the cluster database and show methods for getting the data from the clusters and plotting it.
I recommend running the file in parts, since plots will clear the current figure and only the last plot will be shown if the file is run all at once. 



The plots that we need to make are:

B/C/D: The thalamus sound response, laser response, and tuning curve
E: The AM modulation plot
G/H/I: The cortex sound response, laser response, and tuning curve
J: Direct laser activation raster
K: Indirect laser activation raster
L: Waveforms for the laser-responsive units

The figure database has comments explaining what each cell is good for
If you run `print figdb` you will get the following: 


Cell 0
ID: pinp003_2015-06-24_3543_TT6_3
Comments: B/C/D Option -  site 1 T6c3 (Thalamus)

Cell 1
ID: pinp003_2015-06-24_3855_TT6_3
Comments: B/C/D (our favorite so far), also possibly J - site 6 T6c3 (Thalamus)

Cell 2
ID: pinp003_2015-07-06_3654_TT3_10
Comments: J - site4 T3c10 (Thalamus)

Cell 3
ID: pinp003_2015-06-24_3543_TT6_6
Comments: K - site1 T6c6 (Thalamus)

Cell 4
ID: pinp005_2015-08-10_1655_TT5_4
Comments: G/H/I - site4 T5c4 (Cortex)

Cell 5
ID: pinp005_2015-08-10_1655_TT5_9
Comments: K - site4 T5c9 (Cortex)

Cell 6
ID: pinp005_2015-08-10_1655_TT6_2
Comments: J - site4 T6c2 (Cortex)

Cell 7
ID: pinp005_2015-08-10_1491_TT5_7
Comments: Good J example - site2 T5c7 (Cortex)

Cell 8
ID: pinp005_2015-08-10_1491_TT5_8
Comments: K - site2 T5c8 (Cortex)

Cell 9
ID: pinp005_2015-08-13_3970_TT3_3
Comments: Best unit for AM modulation. Also sound/laser responsive thalamus unit for B/C/D

In the directory I gave you there are the .png reports for each of these cells. 

##############

You need the data from the following mice/days:

pinp003: 2014-06-24, 2015-07-06
pinp005: 2015-08-10, 2015-08-13

##############
'''

#You can easily get the data from the clusters by initializing an offline instance of a data loading class.

loader = dataloader.DataLoader('offline', experimenter='nick')

# - If you do not know the string for the session type that you want, it will prompt you:
spikeData, eventData, behavData = loader.get_cluster_data(figdb[0])
# - The dataspikes object will contain only the spikes and samples for this cluster

# - You can also specify the session type:
spikeData, eventData, behavData = loader.get_cluster_data(figdb[0], 'noiseBurst')
# - I tried to keep the session types somewhat consistent but they are not all the same

## ------ Plotting a raster----------

#I usually use plotting functions that live in my dataplotter module.
#These fns take spiketimes and eventOnsetTimes and take care of calling
#spikesanalysis and behavioranalysis methods, and then use extraplots methods to do the plotting

#Lets look at the noise burst response from the first cluster
spikeData, eventData, behavData = loader.get_cluster_data(figdb[0], 'noiseBurst')
spikeTimestamps = spikeData.timestamps
eventOnsetTimes = loader.get_event_onset_times(eventData)

plt.clf()
dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes)
plt.show()

#All rasters in the reports are plotted this way. 

## ------ Plotting a sorted raster ----

#The nice thing about the raster plotting methods is that they can accept an array to sort by
#Lets look at the AM responses from the last cluster (9)

spikeData, eventData, behavData = loader.get_cluster_data(figdb[9], 'AM')

spikeTimestamps = spikeData.timestamps
eventOnsetTimes = loader.get_event_onset_times(eventData)
currentFreq = behavData['currentFreq']

plt.clf()
dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray = currentFreq, timeRange = [-0.1, 0.6], fillWidth=0)
plt.show()


## ------ Tuning Curve Heatmaps ----
## Plotting the heatmaps requires a bit more code
## Lets look at the tuning curve from the last cell, since it is a thalamus cell that
## seems directly activated and (I think) it has a nicer tuning than the
## other thalamus cell we were going to use for plots B, C, and D

spikeData, eventData, behavData = loader.get_cluster_data(figdb[9], 'TuningCurve')

spikeTimestamps = spikeData.timestamps
eventOnsetTimes = loader.get_event_onset_times(eventData)
freqEachTrial = behavData['currentFreq']
intensityEachTrial = behavData['currentIntensity']

possibleFreq = np.unique(freqEachTrial)

possibleIntensity = np.unique(intensityEachTrial)

xlabel='Frequency (kHz)'
ylabel='Intensity (dB SPL)'

freqLabels = ["%.1f" % freq for freq in possibleFreq/1000.0]
intenLabels = ["%.1f" % inten for inten in possibleIntensity]

plt.clf()
dataplotter.two_axis_heatmap(spikeTimestamps,
                             eventOnsetTimes,
                             firstSortArray=intensityEachTrial,
                             secondSortArray=freqEachTrial,
                             firstSortLabels=intenLabels,
                             secondSortLabels=freqLabels,
                             timeRange=[0, 0.1])

plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.show()

### I think that the only other plot you need for the figure that you gave me is the spike waveform plot
##The waveforms for cell 9, the one with the good amp modulation

plt.clf()
spikesorting.plot_waveforms(spikeData.samples)
plt.show()

#The plot_waveforms method currently computes the average over only the 40 selected spikes.
#Spikes are selected and then aligned, and the the aligned ones are used to calculate the average.
#We should think about calculating the average over all the spikes if it isn't too much to align them all. 


spikeData, eventData, behavData = loader.get_cluster_data(figdb[9], 'AM')


spikeTimestamps = spikeData.timestamps
eventOnsetTimes = loader.get_event_onset_times(eventData)
currentFreq = behavData['currentFreq']
dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray = currentFreq)

plt.clf()


currentFreq

from jaratoolbox import spikesanalysis

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
