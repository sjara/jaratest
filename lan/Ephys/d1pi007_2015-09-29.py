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
                'str':'sortedTuningRaster'}
 
exp0929 = cellDB.Experiment(animalName='d1pi007', date ='2015-09-29', experimenter='lan', defaultParadigm='laser_tuning_curve')


site1 = exp0929.add_site(depth = 3050, tetrodes = [3,4,6]) 
site1.add_session('17-36-42', None, sessionTypes['nb']) #amp=0.1
site1.add_session('17-38-53', None, sessionTypes['nb'])  #amp=0.3
site1.add_session('17-43-28', None, sessionTypes['lp']) #50ms, 1.5mW
site1.add_session('17-45-45', None, sessionTypes['lt']) 
site1.add_session('17-53-40', 'a', sessionTypes['str'])
site1.add_session('18-02-52', 'b', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[1, 2, 3], mainTCind=5, mainSTRind=4)


site2 = exp0929.add_site(depth = 3150, tetrodes = [3,4,6]) 
site2.add_session('18-23-55', None, sessionTypes['nb']) #amp=0.3
site2.add_session('18-27-05', None, sessionTypes['lp'])
site2.add_session('18-29-19', None, sessionTypes['lt'])
site2.add_session('18-32-13', 'c', sessionTypes['str'])
site2.add_session('18-40-02', 'd', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site2, 'site2', mainRasterInds=[0, 1, 2], mainTCind=4, mainSTRind=3)


