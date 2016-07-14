from jaratoolbox.test.nick.ephysExperiments import ephys_experiment_v3 as ee3
reload(ee3)

#The session types to use for this kind of experiment
#Can use a dict like this or simply write the sesison types directly
#I used this to avoid typing errors and to save time
sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tc_heatmap',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse'}

impedence = {
'TT3' : [369, 389, 327, 362],
'TT4' : [356, 284, 291, 363],
'TT5' : [350, 334, 348, 292],
'TT6' : [428, 185, 242, 232]}


laserCalibration = {
'1.0mW':2.3,
'1.5mW':2.8,
'2.0mW':3.2,
'2.5mW':3.5,
'3.0mW':4.1,
'3.5mW':4.45}

comments = []

paradigm = 'laser_tuning_curve'
today = ee3.RecordingDay(animalName = 'pinp003', date = '2015-07-20', experimenter = 'nick')

comments.append('0919hrs - mouse on rig with tetrodes at 1002um. I am in the previous best location, in the middle of the well (AP) and as close as possible to the medial wall. I have coated the electrodes with DiI and I will try to get as much good data from this site as possible this morning.')

comments.append('0936hrs - tetrodes are at 3004um, holding for 5 mins. No spikes from hippocampus on any tetrode on the way down - damaged tract from many recordings? I will keep moving deeper than I have gone today looking for sound and laser responses')

comments.append('0958hrs - there are tiny spikes at 3206um that appear to be responsive to the laser, not much response to 0.4amp noise. Re-testing with 0.5amp and more trials.  - Not obviously responsive, moving on')

site1 = ee3.RecordingSite(today, depth = 3425, goodTetrodes = [4, 5, 6])
site1.add_session('10-21-34', None, 'NB0.5').set_plot_type('raster', report='main')
site1.add_session('10-24-16', None, 'LP2.5').set_plot_type('raster', report='main')
site1.add_session('10-26-57', None, 'LT2.5').set_plot_type('raster', report='main')
site1.add_session('10-30-48', 'a', 'TC_2k-40k_16f_40-70_4ints').set_plot_type('tc_heatmap', report='main')
# site1.generate_main_report('site1')


comments.append('site 2 has a reference for the spikes as well as the LFPs. spikes = channel 14, lfp = channel 11')
site2 = ee3.RecordingSite(today, depth = 3451, goodTetrodes = [5, 6])
site2.add_session('10-58-42', None, 'LP2.5').set_plot_type('raster', report='main')
site2.add_session('11-01-08', None, 'LT2.5').set_plot_type('raster', report='main')
site2.add_session('11-05-29', None, 'NB0.3').set_plot_type('raster', report='main')
site2.add_session('11-08-42', 'b', 'TC_2k-40k_16f_40-70_4ints').set_plot_type('tc_heatmap', report='main')
#site2.add_session('11-08-42', 'b', 'TC_2k-40k_16f_40-70_4ints').set_plot_type('tc_heatmap', report='tcComparison')
site2.add_session('11-23-51', 'c', 'TC_3k-13k_16f_20-50_4ints').set_plot_type('tc_heatmap', report='tcComparison')
# site2.generate_main_report('site2')


site3 = ee3.RecordingSite(today, depth = 3602, goodTetrodes = [5, 6])
site3.add_session('11-51-31', None, 'NB0.3').set_plot_type('raster', report='main')
site3.add_session('11-54-05', None, 'LP2.5').set_plot_type('raster', report='main')
site3.add_session('11-56-36', None, 'LT2.5').set_plot_type('raster', report='main')
site3.generate_main_report('site3')
#synaptic excitation if anything at all, moving on

comments.append('1230hrs - no more sound responses at 4000um. I am removing the electrodes')
