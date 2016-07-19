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
 
exp1210 = cellDB.Experiment(animalName='adap011', date ='2015-12-10', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp1210.add_site(depth=2820, tetrodes=[2]) 
site1.add_session('12-53-51', None, sessionTypes['nb']) #amp=0.15
site1.add_session('12-58-23', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('13-05-55', 'b', sessionTypes['tc']) #15&19kHz chords, 50dB
site1.add_session('13-09-06', 'c', sessionTypes['tc']) #5&6.2kHz chords, 50dB
site1.add_session('13-12-38', 'a', sessionTypes['2afc'], paradigm='2afc')

#sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0], mainTCind=1, mainSTRind=1)
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=4, tetrodes=[2]) 
sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=4, tetrodes=[2], trialLimit=[498,1232]) #remove first two blocks due to poor behavior, last two blocks due to decrease in spontaneous activity of TT9c9
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[2],choiceSide='both',trialLimit=[498,1232]) 
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[2],choiceSide='right',trialLimit=[498,1232])
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=4, tetrodes=[2],choiceSide='left',trialLimit=[498,1232]) 
