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
 
exp = cellDB.Experiment(animalName='d1pi003', date ='2016-02-07', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp.add_site(depth=2880, tetrodes=[1,2,3,4,5,6,7]) #TT8 is ref
site1.add_session('16-50-16', None, sessionTypes['nb']) #amp=0.15
site1.add_session('16-52-42', None, sessionTypes['lp']) #power=1.5mW
site1.add_session('16-54-09', None, sessionTypes['lt']) #power=1.5mW
site1.add_session('16-56-16', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('17-03-27', 'a', sessionTypes['2afc'], paradigm='2afc')
#site1.add_session('18-44-10', None, sessionTypes['lt']) #power=1.5mW

#sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,1,2], mainTCind=3, mainSTRind=3)
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=3, tetrodes=[1,2,3,5,8]) 
sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=4, tetrodes=[1,2,3,4,5,6,7],trialLimit=[]) #ephys length > behav length, not analyzed
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=5, tetrodes=[3,5],trialLimit=[],choiceSide='both') 
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[1,4,5,6,7],trialLimit=[],choiceSide='left')
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[1,4,5,6,7],trialLimit=[],choiceSide='right')
