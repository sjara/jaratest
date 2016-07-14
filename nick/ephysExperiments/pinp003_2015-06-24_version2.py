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

today = ee3.RecordingDay(animalName = 'pinp003', date = '2015-06-24', experimenter = 'nick')

site1 = ee3.RecordingSite(today, depth = 3543, goodTetrodes = [6])
s1s1 = site1.add_session('15-22-29', None, sessionTypes['nb'])
s1s1.set_plot_type('raster')

site1.add_session('15-25-08', None, sessionTypes['lp']).set_plot_type('raster')
site1.add_session('15-27-37', None, sessionTypes['lt']).set_plot_type('raster')
site1.add_session('15-31-48', 'a', sessionTypes['tc']).set_plot_type('tc_heatmap')
site1.add_session('15-45-22', 'b', sessionTypes['bf']).set_plot_type('raster')
site1.generate_main_report('site1')

site2 = ee3.RecordingSite(today, depth = 3623, goodTetrodes = [6])
site2.add_session('15-54-56', None, sessionTypes['nb']).set_plot_type('raster')
site2.add_session('15-57-33', None, sessionTypes['lp']).set_plot_type('raster')
site2.add_session('16-00-02', None, sessionTypes['lt']).set_plot_type('raster')
site2.add_session('16-04-48', 'c', sessionTypes['tc']).set_plot_type('tc_heatmap')
site2.add_session('16-17-30', 'd', sessionTypes['bf']).set_plot_type('raster')
site2.add_session('16-20-11', None, sessionTypes['3p'])
site2.add_session('16-22-37', None, sessionTypes['1p'])
site2.generate_main_report('site2')

site3 = ee3.RecordingSite(today, depth = 3700, goodTetrodes = [6])
site3.add_session('16-40-44', None, sessionTypes['nb']).set_plot_type('raster')
site3.add_session('16-44-01', None, sessionTypes['lp']).set_plot_type('raster')
site3.add_session('16-46-20', None, sessionTypes['lt']).set_plot_type('raster')
site3.add_session('16-50-03', 'e', sessionTypes['tc']).set_plot_type('tc_heatmap')
site3.add_session('17-03-10', None, sessionTypes['bf']).set_plot_type('raster')
site3.add_session('17-06-10', None, sessionTypes['3p'])
site3.add_session('17-09-06', None, sessionTypes['1p'])
site3.generate_main_report('site3')

site4 = ee3.RecordingSite(today, depth = 3757, goodTetrodes = [3, 6])
site4.add_session('17-15-58', None, sessionTypes['nb']).set_plot_type('raster')
site4.add_session('17-18-57', None, sessionTypes['lp']).set_plot_type('raster')
site4.add_session('17-21-29', None, sessionTypes['lt']).set_plot_type('raster')
site4.add_session('17-25-16', 'g', sessionTypes['tc']).set_plot_type('tc_heatmap')
site4.add_session('17-37-45', 'af', sessionTypes['bf']).set_plot_type('raster')
site4.add_session('17-41-31', None, sessionTypes['3p'])
site4.add_session('17-44-25', None, sessionTypes['1p'])
site4.generate_main_report('site4')

site5 = ee3.RecordingSite(today, depth = 3805, goodTetrodes = [3, 6])
site5.add_session('17-59-53', None, sessionTypes['nb']).set_plot_type('raster')
site5.add_session('18-03-50', None, sessionTypes['lp']).set_plot_type('raster')
site5.add_session('18-06-31', None, sessionTypes['lt']).set_plot_type('raster')
site5.add_session('18-10-38', 'h', sessionTypes['tc']).set_plot_type('tc_heatmap')
site5.add_session('18-24-47', None, sessionTypes['bf']).set_plot_type('raster')
site5.add_session('18-29-24', None, sessionTypes['3p'])
site5.add_session('18-33-08', None, sessionTypes['1p'])
site5.generate_main_report('site5')

site6 = ee3.RecordingSite(today, depth = 3855, goodTetrodes = [6])
site6.add_session('18-44-21', None, sessionTypes['nb']).set_plot_type('raster')
site6.add_session('18-47-59', None, sessionTypes['lp']).set_plot_type('raster')
site6.add_session('18-51-29', None, sessionTypes['lt']).set_plot_type('raster')
site6.add_session('18-55-40', 'i', sessionTypes['tc']).set_plot_type('tc_heatmap')
site6.add_session('19-10-27', None, sessionTypes['bf']).set_plot_type('raster')
site6.add_session('19-13-33', None, sessionTypes['3p'])
site6.add_session('19-16-41', None, sessionTypes['1p'])
site6.generate_main_report('site6')

#from jaratoolbox.test.nick.ephysExperiments import laserTCanalysis
#reload(laserTCanalysis)
#for indSite, site in enumerate(today.siteList):
    #laserTCanalysis.laser_tc_analysis(site, indSite+1)
