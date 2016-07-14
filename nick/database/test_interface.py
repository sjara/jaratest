def setup():
    from jaratoolbox.test.nick.database import ephysinterface
    reload(ephysinterface)

    global interface
    interface = ephysinterface.EphysInterface('pinp003',
                                            '2015-06-24',
                                            'nick',
                                            'laser_tuning_curve')
    global spikeTimestamps
    global events
    global eventOnsetTimes
    global bdata
    spikeTimestamps=interface.loader.get_session_spikes('15-31-48', 6).timestamps
    events=interface.loader.get_session_events('15-31-48')
    eventOnsetTimes=interface.loader.get_event_onset_times(events)
    bdata=interface.loader.get_session_behavior('a')

setup()

#Ephys Interface plotting functions
interface.plot_array_raster('15-31-48')
interface.plot_session_raster('15-31-48', 6)
interface.plot_sorted_tuning_raster('15-31-48', 6, 'a')
interface.plot_session_tc_heatmap('15-31-48', 6, 'a')
interface.plot_array_freq_tuning('15-31-48', 'a')
interface.plot_am_tuning('15-31-48', 6, 'a')

#This is working now but needs to have some return object
flipper=interface.flip_tetrode_tuning('15-31-48', 'a', tetrodes=[3, 4, 5, 6])


#Dataplotter base plotting functions
from jaratoolbox.test.nick.database import dataplotter
reload(dataplotter)

#Test plot_raster
dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray=bdata['currentFreq'])

#Test two_axis_sorted_raster
dataplotter.two_axis_sorted_raster(spikeTimestamps,
                                   eventOnsetTimes,
                                   bdata['currentFreq'],
                                   bdata['currentIntensity'])

#Test two_axis_heatmap - have to reverse first and second array
dataplotter.two_axis_heatmap(spikeTimestamps,
                             eventOnsetTimes,
                             bdata['currentIntensity'],
                             bdata['currentFreq'])

#Test one_axis_tc_or_rlf
#TC
dataplotter.one_axis_tc_or_rlf(spikeTimestamps,
                               eventOnsetTimes,
                               sortArray=bdata['currentFreq'])
#RLF
dataplotter.one_axis_tc_or_rlf(spikeTimestamps,
                               eventOnsetTimes,
                               sortArray=bdata['currentIntensity'])

#Plot waveforms in event locked timerange

import matplotlib.pyplot as plt
plt.close('all')
