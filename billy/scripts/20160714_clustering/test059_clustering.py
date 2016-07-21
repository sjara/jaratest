from jaratoolbox.test.nick.database import cellDB
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
exp = cellDB.Experiment(animalName='test059', date ='2015-06-17', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('21-15-19', 'a', sessionTypes['tc'])
site1.add_session('21-36-38', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test059', date ='2015-06-18', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-19-46', 'a', sessionTypes['tc'])
site1.add_session('14-41-21', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test059', date ='2015-06-19', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-49-41', 'a', sessionTypes['tc'])
site1.add_session('14-05-19', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test059', date ='2015-06-22', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-01-08', 'a', sessionTypes['tc'])
site1.add_session('15-21-02', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test059', date ='2015-06-23', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-52-57', 'a', sessionTypes['tc'])
site1.add_session('15-05-47', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test059', date ='2015-06-24', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-23-53', 'a', sessionTypes['tc'])
site1.add_session('13-38-31', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test059', date ='2015-06-25', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-04-26', 'a', sessionTypes['tc'])
site1.add_session('15-22-32', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test059', date ='2015-06-26', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-28-39', 'a', sessionTypes['tc'])
site1.add_session('15-46-23', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test059', date ='2015-06-28', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-49-45', 'a', sessionTypes['tc'])
site1.add_session('17-10-44', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test059', date ='2015-06-29', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-45-01', 'b', sessionTypes['tc'])
site1.add_session('18-01-08', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test059', date ='2015-06-30', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-16-33', 'a', sessionTypes['tc'])
site1.add_session('16-34-20', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test059', date ='2015-07-01', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-10-20', 'b', sessionTypes['tc'])
site1.add_session('15-26-17', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test059', date ='2015-07-02', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-22-07', 'a', sessionTypes['tc'])
site1.add_session('15-37-40', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
'''
