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

'''
exp = cellDB.Experiment(animalName='adap013', date ='2016-02-11', experimenter='billy', defaultParadigm='tuning_curve') 
site1 = exp.add_site(depth=0, tetrodes=[1,2,3,4,5,6,7,8])
#site1.add_session('', None, sessionTypes['nb']) 
site1.add_session('15-13-47', 'a', sessionTypes['tc']) 
site1.add_session('15-23-56', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap013', date ='2016-02-22', experimenter='billy', defaultParadigm='tuning_curve') 
site1 = exp.add_site(depth=0, tetrodes=[1,2,3,4,5,6,7,8])
#site1.add_session('', None, sessionTypes['nb']) 
site1.add_session('12-34-29', 'a', sessionTypes['tc']) 
site1.add_session('12-44-19', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap013', date ='2016-02-24', experimenter='billy', defaultParadigm='tuning_curve') 
site1 = exp.add_site(depth=0, tetrodes=[1,2,3,4,5,6,7,8])
#site1.add_session('', None, sessionTypes['nb']) 
site1.add_session('10-16-44', 'a', sessionTypes['tc']) 
site1.add_session('10-27-12', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap013', date ='2016-02-26', experimenter='billy', defaultParadigm='tuning_curve') 
site1 = exp.add_site(depth=0, tetrodes=[1,2,3,4,5,6,7,8])
#site1.add_session('', None, sessionTypes['nb']) 
site1.add_session('10-45-11', 'a', sessionTypes['tc']) 
site1.add_session('10-59-09', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap013', date ='2016-02-28', experimenter='billy', defaultParadigm='tuning_curve') 
site1 = exp.add_site(depth=0, tetrodes=[1,2,3,4,5,6,7,8])
#site1.add_session('', None, sessionTypes['nb']) 
site1.add_session('15-35-15', 'a', sessionTypes['tc']) 
site1.add_session('15-44-01', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)



exp = cellDB.Experiment(animalName='adap013', date ='2016-03-01', experimenter='billy', defaultParadigm='tuning_curve') 
site1 = exp.add_site(depth=0, tetrodes=[1,2,3,4,5,6,7,8])
#site1.add_session('', None, sessionTypes['nb']) 
site1.add_session('11-31-17', 'a', sessionTypes['tc']) 
site1.add_session('11-43-31', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap013', date ='2016-03-02', experimenter='billy', defaultParadigm='tuning_curve') 
site1 = exp.add_site(depth=0, tetrodes=[1,2,3,4,5,6,7,8])
#site1.add_session('', None, sessionTypes['nb']) 
site1.add_session('14-20-53', 'a', sessionTypes['tc']) 
site1.add_session('14-29-49', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)



exp = cellDB.Experiment(animalName='adap013', date ='2016-03-16', experimenter='billy', defaultParadigm='tuning_curve') 
site1 = exp.add_site(depth=0, tetrodes=[1,2,3,4,5,6,7,8])
#site1.add_session('', None, sessionTypes['nb']) 
site1.add_session('13-47-24', 'a', sessionTypes['tc']) 
site1.add_session('13-57-37', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)



exp = cellDB.Experiment(animalName='adap013', date ='2016-03-18', experimenter='billy', defaultParadigm='tuning_curve') 
site1 = exp.add_site(depth=0, tetrodes=[1,2,3,4,5,6,7,8])
#site1.add_session('', None, sessionTypes['nb']) 
site1.add_session('13-26-01', 'a', sessionTypes['tc']) 
site1.add_session('13-36-20', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap013', date ='2016-03-20', experimenter='billy', defaultParadigm='tuning_curve') 
site1 = exp.add_site(depth=0, tetrodes=[1,2,3,4,5,6,7,8])
#site1.add_session('', None, sessionTypes['nb']) 
site1.add_session('14-01-26', 'a', sessionTypes['tc']) 
site1.add_session('14-10-47', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap013', date ='2016-03-21', experimenter='billy', defaultParadigm='tuning_curve') 
site1 = exp.add_site(depth=0, tetrodes=[1,2,3,4,5,6,7,8])
#site1.add_session('', None, sessionTypes['nb']) 
site1.add_session('15-22-32', 'a', sessionTypes['tc']) 
site1.add_session('15-33-19', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
'''
