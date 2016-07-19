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

''' 
exp = cellDB.Experiment(animalName='adap012', date ='2016-03-23', experimenter='lan', defaultParadigm='laser_tuning_curve') 

site1 = exp.add_site(depth=2940, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-47-28', None, sessionTypes['nb']) #amp=0.1
site1.add_session('12-49-37', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('12-57-54', 'a', sessionTypes['2afc'], paradigm='2afc')

sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=[0], mainTCind=1)
#sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=2, tetrodes=[1,2,3,4,5,6,7,8],trialLimit=[]) 
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=2, tetrodes=[1,2,3,4,5,6,7,8],trialLimit=[],choiceSide='left')
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=2, tetrodes=[1,2,3,4,5,6,7,8],trialLimit=[],choiceSide='right')


exp = cellDB.Experiment(animalName='adap012', date ='2016-03-24', experimenter='lan', defaultParadigm='laser_tuning_curve') 

site1 = exp.add_site(depth=2940, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-54-33', None, sessionTypes['nb']) #amp=0.1
site1.add_session('13-56-41', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('14-01-29', 'a', sessionTypes['2afc'], paradigm='2afc')

sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=[0], mainTCind=1)


exp = cellDB.Experiment(animalName='adap012', date ='2016-03-28', experimenter='lan', defaultParadigm='laser_tuning_curve') 

site1 = exp.add_site(depth=2980, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-55-48', None, sessionTypes['nb']) #amp=0.1
site1.add_session('12-58-04', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('13-05-09', 'a', sessionTypes['2afc'], paradigm='2afc')

sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=[0], mainTCind=1)


exp = cellDB.Experiment(animalName='adap012', date ='2016-03-29', experimenter='lan', defaultParadigm='laser_tuning_curve') 

site1 = exp.add_site(depth=2980, tetrodes=[1,2,3,4,5,6,7])
site1.add_session('14-01-04', None, sessionTypes['nb']) #amp=0.1
site1.add_session('14-03-20', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('14-07-57', 'a', sessionTypes['2afc'], paradigm='2afc')

sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=[0], mainTCind=1)


exp = cellDB.Experiment(animalName='adap012', date ='2016-03-31', experimenter='lan', defaultParadigm='laser_tuning_curve') 

site1 = exp.add_site(depth=3020, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-08-18', None, sessionTypes['nb']) #amp=0.1
site1.add_session('13-10-45', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('13-16-33', 'a', sessionTypes['2afc'], paradigm='2afc')

sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=[0], mainTCind=1)


exp = cellDB.Experiment(animalName='adap012', date ='2016-04-04', experimenter='lan', defaultParadigm='laser_tuning_curve') 
#Has 3 frequencies
site1 = exp.add_site(depth=3060, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-04-51', None, sessionTypes['nb']) #amp=0.1
site1.add_session('15-07-14', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('15-19-01', 'a', sessionTypes['2afc'], paradigm='2afc')

sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=[0], mainTCind=1)
'''

exp = cellDB.Experiment(animalName='adap012', date ='2016-04-05', experimenter='lan', defaultParadigm='laser_tuning_curve') 
#Has 3 frequencies
site1 = exp.add_site(depth=3060, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-34-22', None, sessionTypes['nb']) #amp=0.1
site1.add_session('12-37-38', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('12-43-43', 'a', sessionTypes['2afc'], paradigm='2afc')

sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=[0], mainTCind=1)
