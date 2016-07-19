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
 
exp1204 = cellDB.Experiment(animalName='adap011', date ='2015-12-04', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp1204.add_site(depth=2580, tetrodes=[2,3,5,6,7,8]) #TT4 did not have any spikes
site1.add_session('14-41-11', None, sessionTypes['nb']) #amp=0.15
site1.add_session('14-48-13', None, sessionTypes['nb']) #amp=0.15
site1.add_session('14-50-16', 'b', sessionTypes['2afc'], paradigm='2afc')
site1.add_session('15-25-14', None, sessionTypes['nb']) #amp=0.2
site1.add_session('15-27-37', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB

sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[1,3], mainTCind=4, mainSTRind=4)

sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=2, tetrodes=[1,8]) #tetrode 1&8 sound responsive  

