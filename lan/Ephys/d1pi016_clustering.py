from jaratest.nick.database import cellDB
reload(cellDB)
from jaratest.lan.Ephys import sitefuncs_vlan as sitefuncs
reload(sitefuncs)

sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse',
                '2afc':'2afc'}

'''
exp = cellDB.Experiment(animalName='d1pi016', date ='2016-08-01', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2100, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-51-14', 'a', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='d1pi016', date ='2016-08-03', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2180, tetrodes=[1,2,3,4,5,6,7,8])
#site1.add_session('14-07-35', 'a', sessionTypes['tc'])
site1.add_session('14-19-09', 'b', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='d1pi015', date ='2016-08-05', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2180, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-29-14', 'a', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='d1pi016', date ='2016-08-05', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2260, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-08-24', None, sessionTypes['nb'])
site1.add_session('14-10-47', 'a', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=[0], mainTCind=1)

exp = cellDB.Experiment(animalName='d1pi015', date ='2016-08-07', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2180, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-45-43', None, sessionTypes['nb'])
site1.add_session('16-48-07', 'a', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=[0], mainTCind=1)


exp = cellDB.Experiment(animalName='d1pi016', date ='2016-08-08', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2260, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-52-27', None, sessionTypes['nb'])
site1.add_session('15-55-03', 'a', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=[0], mainTCind=1)


exp = cellDB.Experiment(animalName='d1pi016', date ='2016-08-09', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2260, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-34-32', None, sessionTypes['nb'])
site1.add_session('15-44-24', 'b', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=[0], mainTCind=1)
'''

exp = cellDB.Experiment(animalName='d1pi016', date ='2016-08-09', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2260, tetrodes=[3,4,5,6]) #left hemi tetrodes
site1.add_session('15-34-32', None, sessionTypes['nb']) 
site1.add_session('15-37-22', 'a', sessionTypes['tc'])
site1.add_session('15-47-50', None, sessionTypes['lp']) #left hemi
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=[0,2], mainTCind=1)
