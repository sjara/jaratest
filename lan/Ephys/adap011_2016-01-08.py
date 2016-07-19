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
 
exp = cellDB.Experiment(animalName='adap011', date ='2016-01-08', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp.add_site(depth=3700, tetrodes=[1,2,3,5,6,7,8]) 
site1.add_session('16-17-06', None, sessionTypes['nb']) #amp=0.1
site1.add_session('16-25-46', None, sessionTypes['nb']) #amp=0.15
site1.add_session('16-37-25', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('18-06-29', 'a', sessionTypes['2afc'], paradigm='2afc')#actually did not record...

#sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,1], mainTCind=2, mainSTRind=2)
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=3, tetrodes=[1,2,3,5,8]) 
#sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=4, tetrodes=[3,5,8],trialLimit=[])
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=5, tetrodes=[3,5],trialLimit=[],choiceSide='both') 
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[3],trialLimit=[],choiceSide='left')
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[3],trialLimit=[],choiceSide='right')
