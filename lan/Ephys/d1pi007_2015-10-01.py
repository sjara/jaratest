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
 
exp0929 = cellDB.Experiment(animalName='d1pi007', date ='2015-10-01', experimenter='lan', defaultParadigm='laser_tuning_curve')


site1 = exp1001.add_site(depth = 2700, tetrodes = [3,4,6]) 
site1.add_session('14-45-24', None, sessionTypes['nb']) #amp=0.3
site1.add_session('14-47-21', None, sessionTypes['lp'])  #50ms, 1.5mW
site1.add_session('14-48-54', None, sessionTypes['nb']) #amp=0.5
site1.add_session('14-51-38', None, sessionTypes['lt']) 
site1.add_session('14-53-03', 'a', sessionTypes['str'])
site1.add_session('15-01-11', 'b', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0, 1, 2, 3], mainTCind=5, mainSTRind=4)


site2 = exp1001.add_site(depth = 2825, tetrodes = [3,4,6]) 
site2.add_session('15-17-04', None, sessionTypes['nb']) #amp=0.3
site2.add_session('15-19-02', None, sessionTypes['nb']) #amp=0.5
site2.add_session('15-21-10', None, sessionTypes['nb']) #amp=0.1
site2.add_session('15-22-28', None, sessionTypes['lp'])
site2.add_session('15-23-36', None, sessionTypes['lt'])
site2.add_session('15-25-34', 'c', sessionTypes['str'])
site2.add_session('15-33-28', 'd', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site2, 'site2', mainRasterInds=[0,1,3,4], mainTCind=6, mainSTRind=5)


site3 = exp1001.add_site(depth = 2950, tetrodes = [3,4,6]) 
site3.add_session('15-53-18', None, sessionTypes['nb']) #amp=0.3
site3.add_session('15-55-01', None, sessionTypes['lp']) 
site3.add_session('15-56-11', None, sessionTypes['lt']) 
site3.add_session('15-57-43', None, sessionTypes['nb']) #amp=0.5
site3.add_session('15-59-21', 'e', sessionTypes['str'])
site3.add_session('16-07-00', 'f', sessionTypes['tc'])

sitefuncs.nick_lan_daily_report(site3, 'site3', mainRasterInds=[0,1,2,3], mainTCind=5, mainSTRind=4)


site4 = exp1001.add_site(depth = 3075, tetrodes = [3,4,5,6])
site4.add_session('16-27-07', None, sessionTypes['nb']) 
site4.add_session('16-29-00', None, sessionTypes['nb'])
site4.add_session('16-31-05', None, sessionTypes['lp'])
site4.add_session('16-32-14', None, sessionTypes['lt']) 
site4.add_session('16-33-45', 'g', sessionTypes['str'])
site4.add_session('16-43-46', 'h', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site4, 'site4', mainRasterInds=[0,1,2,3], mainTCind=5, mainSTRind=4)


site5 = exp1001.add_site(depth = 3200, tetrodes = [3,4,5,6])
site5.add_session('17-08-06', None, sessionTypes['nb']) 
site5.add_session('17-10-26', None, sessionTypes['nb'])
site5.add_session('17-13-11', None, sessionTypes['lp'])
site5.add_session('17-14-57', None, sessionTypes['lt']) 
site5.add_session('17-17-01', 'i', sessionTypes['str'])
site5.add_session('17-25-02', 'j', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site5, 'site5', mainRasterInds=[0,1,2,3], mainTCind=5, mainSTRind=4)


site6 = exp1001.add_site(depth = 3325, tetrodes = [3,4,5,6])
site6.add_session('17-44-13', None, sessionTypes['nb'])
site6.add_session('17-46-16', None, sessionTypes['nb'])
site6.add_session('17-48-12', None, sessionTypes['lp']) 
site6.add_session('17-49-36', None, sessionTypes['lt'])
site6.add_session('17-51-44', 'k', sessionTypes['str'])
site6.add_session('18-00-12', 'l', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site6, 'site6', mainRasterInds=[0,1,2,3], mainSTRind=4, mainTCind=5) 


site7 = exp1001.add_site(depth = 3450, tetrodes = [3,4,5,6])
site7.add_session('18-20-19', None, sessionTypes['nb'])
site7.add_session('18-23-31', None, sessionTypes['nb']) 
site7.add_session('18-26-05', None, sessionTypes['lp']) 
site7.add_session('18-27-44', None, sessionTypes['lt']) 
site7.add_session('18-29-48', 'm', sessionTypes['str'])
site7.add_session('18-38-40', 'n', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site7, 'site7', mainRasterInds=[0,1,2,3], mainSTRind=4, mainTCind=5) 



