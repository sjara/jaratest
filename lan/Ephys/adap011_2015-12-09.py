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
 
exp1209 = cellDB.Experiment(animalName='adap011', date ='2015-12-09', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp1209.add_site(depth=2820, tetrodes=[1,2,3,5,6,7,8]) 
site1.add_session('11-23-20', None, sessionTypes['nb']) #amp=0.15
site1.add_session('11-27-07', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('11-37-29', 'b', sessionTypes['tc']) #14.7&18kHz chords, 50dB
site1.add_session('11-43-14', 'c', sessionTypes['tc']) #15&19kHz chords, 50dB
site1.add_session('11-49-36', 'a', sessionTypes['2afc'], paradigm='2afc')

#sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0], mainTCind=1, mainSTRind=3)
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=4, tetrodes=[1,3,5,6,7,8]) 
sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=4, tetrodes=[2],trialLimit=[0,886]) 
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[2],trialLimit=[0,886],choiceSide='both') #block1-4 (eliminate block5 due to few trials)
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[2],trialLimit=[0,886],choiceSide='left')
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[2],trialLimit=[0,886],choiceSide='right')
