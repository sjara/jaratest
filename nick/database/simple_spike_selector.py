from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from matplotlib import pyplot as plt
from jaratoolbox.test.nick.database import dataplotter
reload(dataplotter)
from jaratoolbox.test.nick.database import dataloader
reload(dataloader)



# spikeData = loader.get_session_spikes('20-41-13', 4, cluster=3)
# events = loader.get_session_events('20-41-13')
# eventOnsetTimes=loader.get_event_onset_times(events)

# spikeTimes=spikeData.timestamps
# waveforms=spikeData.samples

# plt.figure()
# dataplotter.plot_raster(spikeTimes, eventOnsetTimes)
# plt.show()

# dataplotter.plot_waveforms_in_event_locked_timerange(waveforms, spikeTimes, eventOnsetTimes, [-0.2, 0])
# dataplotter.plot_waveforms_in_event_locked_timerange(waveforms, spikeTimes, eventOnsetTimes, [0, 0.1])



# plt.figure()
# dataplotter.plot_raster(spikeTimes, eventOnsetTimes)
# plt.show()

# plt.figure()
# dataplotter.plot_waveforms_in_event_locked_timerange(waveforms, spikeTimes, eventOnsetTimes, [-0.2, 0])
# plt.show()

# plt.figure()
# dataplotter.plot_waveforms_in_event_locked_timerange(waveforms, spikeTimes, eventOnsetTimes, [0.1, 0.2])
# plt.show()

def compare_session_spike_waveforms(spikeSamples, spikeTimes, eventOnsetTimes, rasterTimeRange, timeRangeList):
    
    fig=plt.figure()
    plt.subplot2grid((3, 2), (0, 0), rowspan=2, colspan=2) 
    dataplotter.plot_raster(spikeTimes, eventOnsetTimes, timeRange=rasterTimeRange)

    for ind, tr in enumerate( timeRangeList ):
        
        plt.subplot2grid((3, 2), (2, ind), rowspan=1, colspan=1)
        dataplotter.plot_waveforms_in_event_locked_timerange(spikeSamples, spikeTimes, eventOnsetTimes, tr)

    plt.subplots_adjust(hspace = 0.7)

if __name__=="__main__":
    loader=dataloader.DataLoader('online', 'pinp005', '2015-07-30', 'laser_tuning_curve')
    spikeData = loader.get_session_spikes('22-10-33', 4, cluster=8)
    events = loader.get_session_events('22-10-33')
    eventOnsetTimes=loader.get_event_onset_times(events)

    spikeTimes=spikeData.timestamps
    waveforms=spikeData.samples
    compare_session_spike_waveforms(waveforms, spikeTimes, eventOnsetTimes, [-0.5, 1], [[-0.2, 0], [0, 0.1]])

#TODO: It would be awesome if we could show the spikes on the raster in a color that corresponds to the waveforms