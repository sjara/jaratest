from jaratoolbox.test.nick.database import cellDB
reload(cellDB)
from jaratoolbox.test.lan.Ephys import sitefuncs_vlan as sitefuncs
reload(sitefuncs)


sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse',
                '2afc':'2afc'}
 
exp1207 = cellDB.Experiment(animalName='adap011', date ='2015-12-07', experimenter='lan', defaultParadigm='laser_tuning_curve') 


#site1 = exp1207.add_site(depth=2820, tetrodes=[3,6,7]) 
#site1.add_session('11-36-15', None, sessionTypes['nb']) #amp=0.2
#site1.add_session('11-40-45', None, sessionTypes['nb']) #amp=0.25
#site1.add_session('11-44-19', 'a', sessionTypes['tc']) #2-40Hz chords, 50-70dB
#site1.add_session('12-06-48', 'a', sessionTypes['2afc'], paradigm='2afc')

#sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,1], mainTCind=2, mainSTRind=2)

#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=3, tetrodes=[3,6,7]) #tetrode 8 sound responsive  


site2 = exp1207.add_site(depth=2820, tetrodes=[1,2,3,5,6,7,8]) 
site2.add_session('15-15-59', 'b', sessionTypes['tc'])#2-40Hz chords, 50-70dB
site2.add_session('15-29-59', None, sessionTypes['nb']) #amp=0.2
site2.add_session('15-40-21', 'c', sessionTypes['tc']) #22&26.8kHz chords
site2.add_session('15-44-53', 'd', sessionTypes['tc']) #8.1&9.9kHz chords
site2.add_session('15-50-48', 'e', sessionTypes['tc']) #32.8&40kHz chords
site2.add_session('15-58-16', 'f', sessionTypes['tc']) #18&22kHz chords
site2.add_session('16-06-39', 'g', sessionTypes['tc']) #9&20kHz chords
site2.add_session('16-11-10', None, sessionTypes['nb']) #amp=0.3
site2.add_session('16-23-36', 'h', sessionTypes['tc']) #20,28.3&40kHz chords
site2.add_session('16-28-04', 'b', sessionTypes['2afc'], paradigm='2afc')

sitefuncs.nick_lan_daily_report(site2, 'site2', mainRasterInds=[1,7], mainTCind=0, mainSTRind=0)

#sitefuncs.lan_2afc_ephys_plots(site2, 'site2', main2afcind=9, tetrodes=[1,2,3,5,6,7,8]) 
