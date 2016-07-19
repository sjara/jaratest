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
 
exp1004 = cellDB.Experiment(animalName='d1pi007', date ='2015-10-04', experimenter='lan', defaultParadigm='laser_tuning_curve')


site1 = exp1004.add_site(depth = 2650, tetrodes = [3]) 
site1.add_session('15-52-02', None, sessionTypes['nb']) #amp=0.3
site1.add_session('15-54-32', None, sessionTypes['nb'])  #amp=0.15
site1.add_session('15-56-36', None, sessionTypes['lp']) 
site1.add_session('15-57-56', None, sessionTypes['lt']) 
site1.add_session('15-59-39', 'a', sessionTypes['tc'])
site1.add_session('16-14-01', 'b', sessionTypes['str'])
sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0, 1, 2, 3], mainTCind=4, mainSTRind=5)


site2 = exp1004.add_site(depth = 2800, tetrodes = [3,4]) 
site2.add_session('16-24-56', None, sessionTypes['nb']) #amp=0.3
site2.add_session('16-26-55', None, sessionTypes['nb']) #amp=0.1
site2.add_session('16-28-56', None, sessionTypes['lp'])
site2.add_session('16-30-26', None, sessionTypes['lt'])
site2.add_session('16-32-14', 'c', sessionTypes['str'])
site2.add_session('16-39-48', 'd', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site2, 'site2', mainRasterInds=[0,1,2,3], mainTCind=5, mainSTRind=4)


site3 = exp1004.add_site(depth = 2925, tetrodes = [3,4,6]) 
site3.add_session('16-57-28', None, sessionTypes['nb']) #amp=0.3
site3.add_session('17-00-00', None, sessionTypes['nb']) 
site3.add_session('17-01-33', None, sessionTypes['lp']) 
site3.add_session('17-02-43', None, sessionTypes['lt']) 
site3.add_session('17-04-40', 'e', sessionTypes['str'])
site3.add_session('17-13-15', 'f', sessionTypes['tc'])

sitefuncs.nick_lan_daily_report(site3, 'site3', mainRasterInds=[0,1,2,3], mainTCind=5, mainSTRind=4)


site4 = exp1004.add_site(depth = 3050, tetrodes = [3,4,6])
site4.add_session('17-29-03', None, sessionTypes['nb']) 
site4.add_session('17-32-16', None, sessionTypes['nb'])
site4.add_session('17-34-23', None, sessionTypes['lp'])
site4.add_session('17-35-42', None, sessionTypes['lt']) 
site4.add_session('17-37-09', 'g', sessionTypes['str'])
site4.add_session('17-42-37', 'h', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site4, 'site4', mainRasterInds=[0,1,2,3], mainTCind=5, mainSTRind=4)


site5 = exp1004.add_site(depth = 3175, tetrodes = [3,4,6])
site5.add_session('17-59-48', None, sessionTypes['nb']) 
site5.add_session('18-02-31', None, sessionTypes['nb'])
site5.add_session('18-05-12', None, sessionTypes['lp'])
site5.add_session('18-07-15', None, sessionTypes['lt']) 
site5.add_session('18-08-44', 'i', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site5, 'site5', mainRasterInds=[0,1,2,3], mainTCind=4, mainSTRind=None)



