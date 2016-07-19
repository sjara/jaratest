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
 
exp1218 = cellDB.Experiment(animalName='adap005', date ='2015-12-18', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp1218.add_site(depth=2420, tetrodes=[1,2,3,4,5,6,7,8]) 
site1.add_session('13-31-21', None, sessionTypes['nb']) #amp=0.15
site1.add_session('13-34-39', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('13-43-35', 'b', sessionTypes['tc']) #8to12kHz,50dB
site1.add_session('13-50-13', 'a', sessionTypes['2afc'], paradigm='2afc')
#sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0], mainTCind=1, mainSTRind=1)
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=3, tetrodes=[1,2,3,4,5,6,7,8]) 
sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=3, tetrodes=[1,3,4,5,7,8],trialLimit=[])
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=3, tetrodes=[3,4,5,6,7,8],trialLimit=[],choiceSide='both') 
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=3, tetrodes=[1,3,4,5,7,8],trialLimit=[],choiceSide='left')
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=3, tetrodes=[1,3,4,5,7,8],trialLimit=[],choiceSide='right')

