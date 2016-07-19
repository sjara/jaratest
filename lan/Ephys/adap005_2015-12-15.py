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
 
exp1215 = cellDB.Experiment(animalName='adap005', date ='2015-12-15', experimenter='lan', defaultParadigm='laser_tuning_curve') 


#site1 = exp1215.add_site(depth=2260, tetrodes=[1,2,3,4,5,6,7,8]) 
#site1.add_session('13-30-00', None, sessionTypes['nb']) #amp=0.15
#site1.add_session('13-33-21', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
#site1.add_session('13-55-21', 'c', sessionTypes['tc']) #4.4to9.9kHz, 5 freqs chords, 50dB
#site1.add_session('14-02-08', 'a', sessionTypes['2afc'], paradigm='2afc')
#sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,2], mainTCind=1, mainSTRind=1)
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=3, tetrodes=[1,2,3,4,5,6,7,8]) 
#sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=3, tetrodes=[1,2,3,4,5,6,7,8],trialLimit=[])
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=3, tetrodes=[5,6],trialLimit=[],choiceSide='both') 
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=6, tetrodes=[1,2,3,5,8],trialLimit=[],choiceSide='left')
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=6, tetrodes=[1,2,3,5,8],trialLimit=[],choiceSide='right')

site2 = exp1215.add_site(depth=2260, tetrodes=[1,2,3,4,5,6,7,8]) #these recordings were done at site1 but removed ref channel
site2.add_session('13-39-33', None, sessionTypes['nb']) #amp=0.15
site2.add_session('13-43-22', 'b', sessionTypes['tc']) #2-40Hz chords, 50dB
sitefuncs.nick_lan_daily_report(site2, 'site2', mainRasterInds=[0], mainTCind=1, mainSTRind=1)
