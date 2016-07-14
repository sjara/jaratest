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

badSessionList = []#prints bad sessions at end
'''
exp = cellDB.Experiment(animalName='test017', date ='2015-02-21', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.5, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('20-01-33', 'a', sessionTypes['tc'])
site1.add_session('20-08-51', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

'''
#SOMETHING WENT WRONG WHILE CLUSTERING
exp = cellDB.Experiment(animalName='test017', date ='2015-02-23', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-16-40', 'a', sessionTypes['tc'])
site1.add_session('15-31-40', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)
'''
exp = cellDB.Experiment(animalName='test017', date ='2015-02-25', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.5, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-54-31', 'a', sessionTypes['tc'])
site1.add_session('14-04-30', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test017', date ='2015-02-26', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.5, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-08-23', 'a', sessionTypes['tc'])
site1.add_session('16-31-05', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test017', date ='2015-02-27', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-43-54', 'a', sessionTypes['tc'])
site1.add_session('14-55-39', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test017', date ='2015-02-28', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.0, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('20-01-25', 'a', sessionTypes['tc'])
site1.add_session('20-10-50', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)
'''
exp = cellDB.Experiment(animalName='test017', date ='2015-03-01', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.0, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-20-55', 'a', sessionTypes['tc'])
site1.add_session('18-37-39', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
'''

exp = cellDB.Experiment(animalName='test017', date ='2015-03-02', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.0, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-04-46', 'a', sessionTypes['tc'])
site1.add_session('15-32-56', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
'''
exp = cellDB.Experiment(animalName='test017', date ='2015-03-03', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.0, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-34-27', 'a', sessionTypes['tc'])
site1.add_session('18-44-50', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-04', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.0, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-45-03', 'a', sessionTypes['tc'])
site1.add_session('14-56-53', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-05', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.0, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-27-06', 'a', sessionTypes['tc'])
site1.add_session('15-48-15', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-06', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-01-56', 'a', sessionTypes['tc'])
site1.add_session('14-12-25', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
'''
exp = cellDB.Experiment(animalName='test017', date ='2015-03-09', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-41-59', 'a', sessionTypes['tc'])
site1.add_session('16-51-45', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-10', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-08-00', 'a', sessionTypes['tc'])
site1.add_session('16-21-40', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-11', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-39-13', 'a', sessionTypes['tc'])
site1.add_session('14-48-20', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-12', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-53-38', 'a', sessionTypes['tc'])
site1.add_session('15-10-08', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-13', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-10-58', 'a', sessionTypes['tc'])
site1.add_session('13-28-00', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-15', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-24-29', 'a', sessionTypes['tc'])
site1.add_session('14-33-42', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-16', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-09-50', 'a', sessionTypes['tc'])
site1.add_session('17-21-11', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-17', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-12-01', 'a', sessionTypes['tc'])
site1.add_session('14-21-17', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-18', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-05-56', 'a', sessionTypes['tc'])
site1.add_session('17-16-40', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-19', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-23-11', 'a', sessionTypes['tc'])
site1.add_session('13-35-17', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-20', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-55-43', 'a', sessionTypes['tc'])
site1.add_session('13-05-06', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)
'''
exp = cellDB.Experiment(animalName='test017', date ='2015-03-21', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-56-55', 'a', sessionTypes['tc'])
site1.add_session('14-06-46', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-22', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('20-20-51', 'a', sessionTypes['tc'])
site1.add_session('20-31-12', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-23', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-13-40', 'a', sessionTypes['tc'])
site1.add_session('16-27-01', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-24', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-14-30', 'a', sessionTypes['tc'])
site1.add_session('16-25-09', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-25', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-17-16', 'a', sessionTypes['tc'])
site1.add_session('15-43-55', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-26', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-10-30', 'a', sessionTypes['tc'])
site1.add_session('15-20-29', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test017', date ='2015-03-27', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-32-19', 'a', sessionTypes['tc'])
site1.add_session('14-41-56', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)




print 'error with sessions: '
for badSes in badSessionList:
    print badSes
