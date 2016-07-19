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
 
exp1211 = cellDB.Experiment(animalName='adap011', date ='2015-12-11', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp1211.add_site(depth=2880, tetrodes=[1,2,3,5,6,7,8]) 
site1.add_session('14-06-01', 'a', sessionTypes['2afc'], paradigm='2afc')
site1.add_session('15-50-20', None, sessionTypes['nb']) #amp=0.15
site1.add_session('15-52-50', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('16-02-03', 'b', sessionTypes['tc']) #6.2&15kHz chords, 50dB

#sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[1], mainTCind=2, mainSTRind=2)
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=0, tetrodes=[1,2,8]) 
#sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=0, tetrodes=[1,2,3,5,8],trialLimit=[0,1508])
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=0, tetrodes=[1,2,3,5,8],trialLimit=[,1508],choiceSide='both') #block1-4 (eliminate block5 due to few trials)
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=0, tetrodes=[5],trialLimit=[],choiceSide='left')
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=0, tetrodes=[5],trialLimit=[],choiceSide='right')
