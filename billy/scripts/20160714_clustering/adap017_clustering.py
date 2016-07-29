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

badSessionList = []#prints bad sessions at end

'''
exp = cellDB.Experiment(animalName='adap017', date ='2016-02-25', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-10-21', 'a', sessionTypes['tc'])
site1.add_session('15-29-36', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-02-29', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-45-23', 'a', sessionTypes['tc'])
site1.add_session('17-55-07', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-03-03', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-54-33', 'a', sessionTypes['tc'])
site1.add_session('16-12-31', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-03-15', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-09-19', 'a', sessionTypes['tc'])
site1.add_session('15-17-43', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-03-17', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-14-16', 'a', sessionTypes['tc'])
site1.add_session('16-22-52', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-03-21', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-48-08', 'a', sessionTypes['tc'])
site1.add_session('16-59-16', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-03-23', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-24-10', 'a', sessionTypes['tc'])
site1.add_session('15-33-17', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-03-28', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-35-03', 'a', sessionTypes['tc'])
site1.add_session('15-44-42', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-03-30', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-47-20', 'a', sessionTypes['tc'])
site1.add_session('14-56-23', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-04-01', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-54-26', 'a', sessionTypes['tc'])
site1.add_session('16-08-05', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-04-05', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-15-23', 'a', sessionTypes['tc'])
site1.add_session('16-24-18', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-04-07', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-54-50', 'a', sessionTypes['tc'])
site1.add_session('16-07-14', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-04-11', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-31-02', 'a', sessionTypes['tc'])
site1.add_session('17-40-24', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-04-12', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-58-54', 'a', sessionTypes['tc'])
site1.add_session('14-09-06', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-04-14', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-30-40', 'a', sessionTypes['tc'])
site1.add_session('14-41-07', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-04-18', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-53-03', 'a', sessionTypes['tc'])
site1.add_session('17-09-56', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-04-20', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-15-19', 'a', sessionTypes['tc'])
site1.add_session('16-27-10', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-04-22', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('19-04-31', 'a', sessionTypes['tc'])
site1.add_session('19-14-45', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-04-23', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('18-29-35', 'a', sessionTypes['tc'])
site1.add_session('18-38-57', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-04-25', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-43-27', 'a', sessionTypes['tc'])
site1.add_session('15-53-36', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-04-27', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-39-43', 'a', sessionTypes['tc'])
site1.add_session('15-50-12', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-04-29', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-57-28', 'a', sessionTypes['tc'])
site1.add_session('18-06-54', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-05-03', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-32-10', 'a', sessionTypes['tc'])
site1.add_session('17-42-53', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap017', date ='2016-05-06', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-55-51', 'a', sessionTypes['tc'])
site1.add_session('17-05-09', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)




print 'error with sessions: '
for badSes in badSessionList:
    print badSes
'''
