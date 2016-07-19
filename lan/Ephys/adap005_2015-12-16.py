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
 
exp1216 = cellDB.Experiment(animalName='adap005', date ='2015-12-16', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp1216.add_site(depth=2420, tetrodes=[1,2,3,4,5,6,7,8]) 
site1.add_session('15-46-32', None, sessionTypes['nb']) #amp=0.15
site1.add_session('15-49-43', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('16-00-15', 'b', sessionTypes['tc']) #6.6to9.9kHz,50dB
site1.add_session('16-10-19', 'c', sessionTypes['tc']) #18to22kHz,50dB
site1.add_session('16-15-56', 'a', sessionTypes['2afc'], paradigm='2afc')
#sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0], mainTCind=1, mainSTRind=1)
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=4, tetrodes=[3,4,5,6,7,8]) 
#sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=4, tetrodes=[3,4,5,6,7,8],trialLimit=[0,1509])
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[4,5,6,7,8],trialLimit=[0,1509],choiceSide='both') 
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[3],trialLimit=[],choiceSide='left')
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[3],trialLimit=[],choiceSide='right')

