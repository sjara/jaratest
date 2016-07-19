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
 
exp1215 = cellDB.Experiment(animalName='adap011', date ='2015-12-15', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp1215.add_site(depth=2960, tetrodes=[1,2,3,5,6,7,8]) 
site1.add_session('15-38-09', None, sessionTypes['nb']) #amp=0.15
site1.add_session('15-41-44', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('15-50-14', None, sessionTypes['nb']) #amp=0.15
site1.add_session('15-54-14', 'b', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('15-58-33', 'c', sessionTypes['tc']) #6.2-19.2kHz, 8freqs, chords, 50dB
site1.add_session('16-07-30', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,2], mainTCind=3, mainSTRind=4)
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=6, tetrodes=[1,2,8]) 
#sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=5, tetrodes=[1,2,3,5,6,7,8],trialLimit=[])
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=6, tetrodes=[1,2,3,5,8],trialLimit=[,1508],choiceSide='both') 
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=6, tetrodes=[1,2,3,5,8],trialLimit=[],choiceSide='left')
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=6, tetrodes=[1,2,3,5,8],trialLimit=[],choiceSide='right')
