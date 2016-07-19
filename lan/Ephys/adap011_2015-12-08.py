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
 
exp1208 = cellDB.Experiment(animalName='adap011', date ='2015-12-08', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp1208.add_site(depth=2820, tetrodes=[1,2,3,5,6,7,8]) 
site1.add_session('11-19-50', None, sessionTypes['nb']) #amp=0.2
site1.add_session('11-22-54', None, sessionTypes['nb']) #amp=0.3
site1.add_session('11-26-03', 'a', sessionTypes['tc']) #2-40Hz chords, 50-70dB
site1.add_session('11-37-46', 'b', sessionTypes['tc']) #8.1&24kHz chords, 70dB
site1.add_session('11-42-02', 'c', sessionTypes['tc']) #8.1&26kHz chords, 70dB
site1.add_session('11-46-07', 'a', sessionTypes['2afc'], paradigm='2afc')

sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,1], mainTCind=2, mainSTRind=4)

sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=5, tetrodes=[1,2,3,5,6,7,8]) #tetrode 8 sound responsive  


