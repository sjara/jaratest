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
 
exp = cellDB.Experiment(animalName='d1pi003', date ='2016-01-28', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp.add_site(depth=2640, tetrodes=[1,2,3,4,5,6,7,8]) #TT5 is ref
site1.add_session('09-47-12', None, sessionTypes['nb']) #amp=0.15
site1.add_session('09-49-32', None, sessionTypes['lp']) #power=1mW
site1.add_session('09-51-00', None, sessionTypes['lp']) #power=2mW
site1.add_session('09-52-32', None, sessionTypes['lt']) #power=1mW
site1.add_session('09-54-35', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('10-00-18', 'b', sessionTypes['tc'])
site1.add_session('10-06-46', 'a', sessionTypes['2afc'], paradigm='2afc')

#sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,1,3], mainTCind=4, mainSTRind=4)
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=3, tetrodes=[1,2,3,5,8]) 
sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=6, tetrodes=[1,2,3,4,5,6,7,8],trialLimit=[])
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=5, tetrodes=[3,5],trialLimit=[],choiceSide='both') 
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=6, tetrodes=[1,3,4,5,6,7],trialLimit=[],choiceSide='left')
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=6, tetrodes=[1,3,4,5,6,7],trialLimit=[],choiceSide='right')
