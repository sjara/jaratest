#WARNING! Turns do not match for 2016-03-21: 3.000 , 2.875
#WARNING! Turns do not match for 2016-03-23: 3.00 , 3.125

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
exp = cellDB.Experiment(animalName='adap017', date ='2016-03-16', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-39-32', 'a', sessionTypes['tc'])
site1.add_session('17-49-15', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap017', date ='2016-03-18', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-17-33', 'a', sessionTypes['tc'])
site1.add_session('17-27-07', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap017', date ='2016-03-22', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-33-18', 'a', sessionTypes['tc'])
site1.add_session('14-43-23', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap017', date ='2016-03-24', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-35-15', 'a', sessionTypes['tc'])
site1.add_session('15-47-08', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap017', date ='2016-03-29', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-46-07', 'a', sessionTypes['tc'])
site1.add_session('16-56-05', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap017', date ='2016-03-31', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-18-46', 'a', sessionTypes['tc'])
site1.add_session('15-45-00', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap017', date ='2016-04-04', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-46-52', 'a', sessionTypes['tc'])
site1.add_session('16-57-16', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap017', date ='2016-04-06', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-25-26', 'a', sessionTypes['tc'])
site1.add_session('17-36-02', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
'''

exp = cellDB.Experiment(animalName='adap017', date ='2016-04-08', experimenter='billy', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('18-32-00', 'a', sessionTypes['tc'])
site1.add_session('18-49-50', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
