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


exp = cellDB.Experiment(animalName='adap013', date ='2016-02-10', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('09-57-50', 'a', sessionTypes['tc'])
site1.add_session('10-10-28', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

'''
exp = cellDB.Experiment(animalName='adap013', date ='2016-02-18', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-42-11', 'a', sessionTypes['tc'])
site1.add_session('17-51-19', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-02-19', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-40-09', 'a', sessionTypes['tc'])
site1.add_session('16-49-26', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-02-23', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('10-30-57', 'a', sessionTypes['tc'])
site1.add_session('10-39-53', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-02-25', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-30-18', 'a', sessionTypes['tc'])
site1.add_session('13-39-23', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-02-29', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-09-06', 'a', sessionTypes['tc'])
site1.add_session('11-23-17', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-03-03', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-09-22', 'a', sessionTypes['tc'])
site1.add_session('11-19-38', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-03-15', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-39-53', 'a', sessionTypes['tc'])
site1.add_session('13-48-39', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-03-17', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-47-48', 'a', sessionTypes['tc'])
site1.add_session('14-59-56', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-03-19', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-21-54', 'a', sessionTypes['tc'])
site1.add_session('16-30-36', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-03-22', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-17-21', 'a', sessionTypes['tc'])
site1.add_session('13-32-19', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-03-24', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.500, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-24-55', 'a', sessionTypes['tc'])
site1.add_session('14-34-32', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-03-29', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-18-08', 'a', sessionTypes['tc'])
site1.add_session('15-33-15', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-03-31', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-07-45', 'a', sessionTypes['tc'])
site1.add_session('14-19-16', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-04-04', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-05-52', 'a', sessionTypes['tc'])
site1.add_session('15-16-10', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-04-06', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-13-27', 'a', sessionTypes['tc'])
site1.add_session('15-29-50', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-04-08', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-14-07', 'a', sessionTypes['tc'])
site1.add_session('14-24-48', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-04-12', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-34-53', 'a', sessionTypes['tc'])
site1.add_session('15-44-55', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap013', date ='2016-04-13', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-14-11', 'a', sessionTypes['tc'])
site1.add_session('17-24-42', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)
'''

'''
print 'error with sessions: '
for badSes in badSessionList:
    print badSes
'''
