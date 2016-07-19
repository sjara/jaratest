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
 
exp1214 = cellDB.Experiment(animalName='adap005', date ='2015-12-14', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp1214.add_site(depth=2260, tetrodes=[1,3,7]) 
site1.add_session('15-51-40', None, sessionTypes['nb']) #amp=0.15
site1.add_session('15-55-38', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('16-01-03', 'b', sessionTypes['tc']) #5.4,6.6,8.1kHz chords, 50dB
site1.add_session('16-05-18', None, sessionTypes['nb']) #amp=0.2
site1.add_session('16-08-53', 'c', sessionTypes['tc']) #6.2&9.9kHz chords, 50dB
site1.add_session('16-13-08', 'd', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('16-23-21', 'a', sessionTypes['2afc'], paradigm='2afc')
#sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,3], mainTCind=5, mainSTRind=5)
sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=6, tetrodes=[1,3,7]) 
#sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=6, tetrodes=[1,2,3,5,8],trialLimit=[])
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=6, tetrodes=[1,2,3,5,8],trialLimit=[,1508],choiceSide='both') 
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=6, tetrodes=[1,2,3,5,8],trialLimit=[],choiceSide='left')
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=6, tetrodes=[1,2,3,5,8],trialLimit=[],choiceSide='right')
