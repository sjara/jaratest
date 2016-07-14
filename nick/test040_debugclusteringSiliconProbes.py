from jaratoolbox.test.nick.database import ephysinterface
from jaratoolbox.test.nick.database import dataplotter

ei = ephysinterface.EphysInterface('pinp013', '2016-05-25', 'nick', 'am_tuning_curve')
bdata = ei.loader.get_session_behavior('a')

plotTitle = ei.loader.get_session_filename(site1.get_mouse_relative_ephys_filenames()[1])

#Why is this giving an error
eventData = ei.loader.get_session_events(site1.get_mouse_relative_ephys_filenames()[1])

eventData = ei.loader.get_session_events('14-41-52')
spikeData = ei.loader.get_session_spikes('14-41-52', 1)
cluster=5
spikeTimestamps = spikeData.timestamps[spikeData.clusters==cluster]
eventOnsetTimes = ei.loader.get_event_onset_times(eventData)

freqEachTrial = bdata['currentFreq']
intensityEachTrial = bdata['currentIntensity']

possibleFreq = np.unique(freqEachTrial)
possibleIntensity = np.unique(intensityEachTrial)

xlabel='Frequency (kHz)'
ylabel='Intensity (dB SPL)'

freqLabels = ["%.1f" % freq for freq in possibleFreq/1000.0]
intenLabels = ["%.1f" % inten for inten in possibleIntensity]

dataplotter.two_axis_heatmap(spikeTimestamps=spikeTimestamps,
                            eventOnsetTimes=eventOnsetTimes,
                            firstSortArray=intensityEachTrial,
                            secondSortArray=freqEachTrial,
                            firstSortLabels=intenLabels,
                            secondSortLabels=freqLabels,
                            xlabel=xlabel,
                            ylabel=ylabel,
                            plotTitle=plotTitle,
                            flipFirstAxis=True,
                            flipSecondAxis=False,
                            timeRange=[0, 0.1])

##The problem was that I was passing the first/second sort labels as the possible values, screwing up the finding each trial combo

