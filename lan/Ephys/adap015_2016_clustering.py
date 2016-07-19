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

exp = cellDB.Experiment(animalName='adap015', date ='2016-02-04', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.250, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-30-47', 'a', sessionTypes['tc'])
site1.add_session('15-41-31', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap015', date ='2016-02-07', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-16-27', 'a', sessionTypes['tc'])
site1.add_session('15-27-13', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap015', date ='2016-02-11', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-08-56', 'a', sessionTypes['tc'])
site1.add_session('17-18-34', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap015', date ='2016-02-15', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-21-04', 'a', sessionTypes['tc'])
site1.add_session('15-40-25', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap015', date ='2016-02-17', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-01-53', 'a', sessionTypes['tc'])
site1.add_session('16-15-41', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap015', date ='2016-02-19', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('10-29-18', 'a', sessionTypes['tc'])
site1.add_session('10-42-16', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap015', date ='2016-02-22', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-40-12', 'a', sessionTypes['tc'])
site1.add_session('17-55-18', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap015', date ='2016-02-24', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-06-29', 'a', sessionTypes['tc'])
site1.add_session('17-21-23', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap015', date ='2016-02-25', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-03-50', 'a', sessionTypes['tc'])
site1.add_session('17-13-16', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap015', date ='2016-02-29', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-46-11', 'a', sessionTypes['tc'])
site1.add_session('15-55-06', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap015', date ='2016-03-01', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-01-59', 'a', sessionTypes['tc'])
site1.add_session('14-12-01', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap015', date ='2016-03-17', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-03-39', 'a', sessionTypes['tc'])
site1.add_session('11-13-12', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap015', date ='2016-03-18', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('10-40-02', 'a', sessionTypes['tc'])
site1.add_session('10-49-54', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
