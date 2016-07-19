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
 
exp = cellDB.Experiment(animalName='adap011', date ='2016-01-06', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp.add_site(depth=3540, tetrodes=[1,2,3,5,6,7,8]) 
site1.add_session('14-19-03', None, sessionTypes['nb']) #amp=0.15
site1.add_session('14-21-37', None, sessionTypes['nb']) #amp=0.15
site1.add_session('14-23-53', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('14-30-58', 'b', sessionTypes['tc']) #18-22kHz
site1.add_session('14-34-39', 'a', sessionTypes['2afc'], paradigm='2afc')

#sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,1], mainTCind=2, mainSTRind=2)
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=3, tetrodes=[1,2,3,5,8]) 
#sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=4, tetrodes=[3,5,8],trialLimit=[])
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=5, tetrodes=[3,5],trialLimit=[],choiceSide='both') 
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[5],trialLimit=[],choiceSide='left')
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[5],trialLimit=[],choiceSide='right')
