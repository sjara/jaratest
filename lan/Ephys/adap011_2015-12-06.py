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
 
exp1206 = cellDB.Experiment(animalName='adap011', date ='2015-12-06', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp1206.add_site(depth=2820, tetrodes=[1,2,3,4,5,6,7,8]) 
site1.add_session('15-58-45', 'a', sessionTypes['2afc'], paradigm='2afc')
site1.add_session('16-42-55', None, sessionTypes['nb']) #amp=0.2
site1.add_session('16-45-35', 'a', sessionTypes['tc']) #2-40Hz chords, 60-70dB
sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[1], mainTCind=2, mainSTRind=2)

sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=0, tetrodes=[1,2,3,4,5,6,7,8]) #tetrode 8 sound responsive  

