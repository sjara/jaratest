from jaratoolbox.test.nick.ephysExperiments import ephys_experiment_v3 as ee3
reload(ee3)

#The session types to use for this kind of experiment
#Can use a dict like this or simply write the sesison types directly
#I used this to avoid typing errors and to save time
sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse'} 

'''
Impedence measurement

TT3 - 472, 576, 301, 510
TT4 - 285, 384, 383, 406
TT5 - 361, 355, 369, 326
TT6 - 550, 260, 270, 270


Laser calibration

1.9 - 1.0mW
2.15 - 1.5mW
2.4 - 2.0mW
2.65 - 2.5mW
2.92 - 3.0mW
3.15 - 3.5mW

1819hrs - mouse on the rig, tetrodes at 1010um. 
I am recording from the right well, more laterally than the last recordings but still in the middle of the well in the A-P direction. The bone is re-growing, so I am at the most medial possible site at this A-P location. The site is almost in the very center of the well. Additionally, the tetrodes are on the lateral side of the optical fiber, so this limits how close I will be able to get to the previous good recording sites.  
'''

today = ee3.RecordingDay(animalName = 'pinp003', date = '2015-07-13', experimenter = 'nick')

'''
At 1010 um there are good spikes on TT4 and some on TT5. It is hard to tell whether or not they are visually-responsive. THey have wide waveforms and are spiking very fast. 

At 1119 um there are visually-responsive spikes on TT5. THe spikes on TT4 went away. 

At 1772 um there are large spikes on TT6

at 1840um there was a ton of activity and screetching (cell death noises)

By 2060um it is much quieter. 

at 2435 there are spikes on TT6 again (the longest tetrode). I am going to wait here for 5 mins for the brain to settle and then start to evaluate sound responses. 

No sound responses here, moving further. 

Testing sound responses at 2564um

No sound responses yet. Moved to 3005um, waiting 5 mins for things to settle. 

There is a weak sound response at 3203um. It looks like it might be only a single cell or possibly noise artifact, although I do not hear any artifact through the speaker. It is on TT6. Testing laser responses. I see a single huge spike right after laser onset on all of the channels, so it is probably photovoltaic effect. File = 2015-07-13_19-05-32
The laser-evoked spike seems to be followed by a powerful silencing effect. I will record another noise-burst session and then a tuning curve here to see if we get anything. We are still shallow but i havent been to this area before so I dont't know what to expect. 

'''

site1 = ee3.RecordingSite(today, depth = 3203, goodTetrodes = [6])
s1s1 = site1.add_session('19-05-32', None, sessionTypes['lp']).set_plot_type('raster', report = 'extrarasters')

#The below ephys session is incorrectly named
s1s2 = site1.add_session('19-05-32', 'a', sessionTypes['nb']).set_plot_type('raster', report = 'extrarasters') #amp = 0.4


'''
THe sound response here is so weak/possibly not there that I am going to keep moving. 
'''
site2 = ee3.RecordingSite(today, depth = 3700, goodTetrodes = [5, 6])
site2.add_session('20-11-35', None, sessionTypes['nb']).set_plot_type('raster', report = 'main')
site2.add_session('20-21-34', None, sessionTypes['lp']).set_plot_type('raster', report = 'main') #Laser at 3mW
#site2.add_session('20-26-48', None, sessionTypes['lp']) #Laser at 1mW
site2.add_session('20-32-21', None, sessionTypes['lt']).set_plot_type('raster', report = 'main')
site2.add_session('20-37-10', 'b', sessionTypes['tc']).set_plot_type('tc_heatmap', report = 'main')
# site2.generate_main_report('site2')

'''
I am going to keep moving. 
'''
site3 = ee3.RecordingSite(today, depth = 3751, goodTetrodes = [5, 6])
site3.add_session('21-11-00', None, sessionTypes['nb']).set_plot_type('raster') #Responses on TT6, maybe TT5
 
site3.add_session('21-14-05', None, sessionTypes['lp']).set_plot_type('raster') #Laser at 1mW
site3.add_session('21-16-36', None, sessionTypes['lt']).set_plot_type('raster') #Laser at 1mW
site3.add_session('21-20-28', 'c', sessionTypes['tc']).set_plot_type('tc_heatmap') #regular TC
site3.add_session('21-34-28', 'd', sessionTypes['tc']) #zooming in on bf
#5000-22000, 16freqs, 20-50db, 4intensities, 0.1duration, 0.8isi
site3.generate_main_report('site3')


site4 = ee3.RecordingSite(today, depth = 3901, goodTetrodes = [5, 6])
site4.add_session('21-54-42', None, sessionTypes['nb']).set_plot_type('raster')
site4.add_session('21-58-54', 'e', sessionTypes['tc']).set_plot_type('tc_heatmap') #BF still between 5 and 9
site4.generate_main_report('site4')



'''
Still getting best frequencies around 5-9kHz. Removing the electrodes at 2210hrs and putting the mouse away
'''

#from jaratoolbox.test.nick.ephysExperiments import laserTCanalysis
#reload(laserTCanalysis)
#for indSite, site in enumerate(today.siteList):
    #laserTCanalysis.laser_tc_analysis(site, indSite+1)


