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
 
exp = cellDB.Experiment(animalName='adap011', date ='2015-12-21', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp.add_site(depth=3340, tetrodes=[1,2,3,5,6,7,8]) 
site1.add_session('13-36-24', None, sessionTypes['nb']) #amp=0.15
site1.add_session('13-44-15', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('13-50-03', None, sessionTypes['nb']) #amp=0.18
site1.add_session('13-54-05', 'a', sessionTypes['2afc'], paradigm='2afc')
site1.add_session('15-12-08', None, sessionTypes['nb']) #amp=0.15
sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,2,3], mainTCind=1, mainSTRind=1)
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=3, tetrodes=[1,2,3,5,8]) 
sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=3, tetrodes=[1,2,3,5,8],trialLimit=[])
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=5, tetrodes=[3,5],trialLimit=[],choiceSide='both') 
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=3, tetrodes=[1,2,3,5,8],trialLimit=[],choiceSide='left')
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=3, tetrodes=[1,2,3,5,8],trialLimit=[],choiceSide='right')
