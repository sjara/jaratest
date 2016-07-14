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
exp = cellDB.Experiment(animalName='adap015', date ='2016-01-22', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-39-00', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap015', date ='2016-01-26', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-46-51', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap015', date ='2016-01-27', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.250, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-20-28', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap015', date ='2016-01-28', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.500, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-07-27', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap015', date ='2016-01-29', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.750, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-15-40', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap015', date ='2016-02-01', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-22-38', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap015', date ='2016-02-05', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.250, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-25-12', 'a', sessionTypes['tc'])
site1.add_session('14-33-42', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap015', date ='2016-02-06', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-41-12', 'a', sessionTypes['tc'])
site1.add_session('16-49-55', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap015', date ='2016-02-08', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.500, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('19-09-24', 'a', sessionTypes['tc'])
site1.add_session('19-18-04', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

#CLUSTERING CRASH: raise 'Times of events are not ordered (or there is at least one repeated).'
#TypeError: exceptions must be old-style classes or derived from BaseException, not str
exp = cellDB.Experiment(animalName='adap015', date ='2016-02-09', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.500, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-17-04', 'a', sessionTypes['tc'])
site1.add_session('16-32-35', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='adap015', date ='2016-02-10', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-12-03', 'a', sessionTypes['tc'])
site1.add_session('16-21-25', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)
'''
#CLUSTERING CRASH: CANNOT ALLOCATE MEMORY
exp = cellDB.Experiment(animalName='adap015', date ='2016-02-12', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('09-41-26', 'a', sessionTypes['tc'])
site1.add_session('09-50-06', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

'''
exp = cellDB.Experiment(animalName='adap015', date ='2016-02-16', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-07-20', 'a', sessionTypes['tc'])
site1.add_session('14-16-04', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap015', date ='2016-02-18', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-44-00', 'a', sessionTypes['tc'])
site1.add_session('14-53-11', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap015', date ='2016-02-23', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-03-27', 'a', sessionTypes['tc'])
site1.add_session('14-12-34', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap015', date ='2016-03-03', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-12-40', 'a', sessionTypes['tc'])
site1.add_session('14-27-14', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap015', date ='2016-03-16', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('09-55-57', 'a', sessionTypes['tc'])
site1.add_session('10-04-37', 'a', sessionTypes['2afc'], paradigm='2afc')
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
