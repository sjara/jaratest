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
 
exp1205 = cellDB.Experiment(animalName='adap011', date ='2015-12-05', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp1205.add_site(depth=2580, tetrodes=[2,3,5,6,7,8]) #TT4 did not have any spikes
site1.add_session('14-09-14', None, sessionTypes['nb']) #amp=0.15
site1.add_session('14-12-57', None, sessionTypes['nb']) #amp=0.25
site1.add_session('14-17-11', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('14-27-22', 'b', sessionTypes['tc']) #2-40Hz chords, 60dB
site1.add_session('14-39-32', 'a', sessionTypes['2afc'], paradigm='2afc')

sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,1], mainTCind=3, mainSTRind=3)

sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=4, tetrodes=[2,3,5,6,7,8]) #tetrode 8 sound responsive  

