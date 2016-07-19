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
 
exp1217 = cellDB.Experiment(animalName='adap005', date ='2015-12-17', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp1217.add_site(depth=2420, tetrodes=[8]) 
site1.add_session('15-02-53', None, sessionTypes['nb']) #amp=0.15
site1.add_session('15-05-44', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('15-10-44', 'b', sessionTypes['tc']) #6.6to9.9kHz,50dB
site1.add_session('15-14-40', 'c', sessionTypes['tc']) #18to22kHz,50dB
site1.add_session('15-19-45', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0], mainTCind=1, mainSTRind=1)
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=4, tetrodes=[1,3,4,5,6,7,8]) 
#sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=4, tetrodes=[8],trialLimit=[])
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[3,4,5,6,7,8],trialLimit=[],choiceSide='both') 
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[8],trialLimit=[],choiceSide='left')
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[8],trialLimit=[],choiceSide='right')

