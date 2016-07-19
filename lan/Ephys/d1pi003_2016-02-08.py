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
 
exp = cellDB.Experiment(animalName='d1pi003', date ='2016-02-08', experimenter='lan', defaultParadigm='laser_tuning_curve') 

'''
site1 = exp.add_site(depth=2960, tetrodes=[1,2,3,4,5,6,7]) #TT8 is ref
site1.add_session('15-24-05', None, sessionTypes['nb']) #amp=0.15
site1.add_session('15-26-48', None, sessionTypes['lp']) #power=1.5mW
site1.add_session('15-28-17', None, sessionTypes['lt']) #power=1.5mW
site1.add_session('15-30-20', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('15-35-37', 'b', sessionTypes['tc']) 
#had to cluster ephys and lt separately because open-ephy crashed and messed up timestamp order
#site1.add_session('15-40-40', 'a', sessionTypes['2afc'], paradigm='2afc') 
#site1.add_session('17-26-43', None, sessionTypes['lt']) #power=1.5mW

sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,1,2,4], mainTCind=3, mainSTRind=3)
'''

site2 = exp.add_site(depth=2960, tetrodes=[1,2,3,4,5,6,7])
site2.add_session('15-40-40', 'a', sessionTypes['2afc'], paradigm='2afc') 
site2.add_session('17-26-43', None, sessionTypes['lt']) #power=1.5mW
sitefuncs.nick_lan_daily_report_short(site2, 'site2', mainRasterInds=[1])
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=3, tetrodes=[1,2,3,5,8]) 
#sitefuncs.lan_2afc_ephys_plots_each_type(site2, 'site2', main2afcind=0, tetrodes=[1,2,3,4,5,6,7],trialLimit=[0,1353])
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=5, tetrodes=[3,5],trialLimit=[],choiceSide='both') 
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site2, 'site2', main2afcind=0, tetrodes=[1,3,4,6,7],trialLimit=[0,1353],choiceSide='left')
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site2, 'site2', main2afcind=0, tetrodes=[1,3,4,6,7],trialLimit=[0,1353],choiceSide='right')
