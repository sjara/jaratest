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

exp = cellDB.Experiment(animalName='test053', date ='2015-05-11', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-06-28', 'a', sessionTypes['tc'])
site1.add_session('17-16-31', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-05-12', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-32-11', 'a', sessionTypes['tc'])
site1.add_session('15-41-58', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-05-13', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-37-50', 'a', sessionTypes['tc'])
site1.add_session('14-47-47', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-05-14', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-19-45', 'a', sessionTypes['tc'])
site1.add_session('14-30-14', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-05-15', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-37-43', 'a', sessionTypes['tc'])
site1.add_session('13-47-59', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)
'''
exp = cellDB.Experiment(animalName='test053', date ='2015-06-10', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-37-43', 'a', sessionTypes['tc'])
site1.add_session('14-44-24', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

'''
exp = cellDB.Experiment(animalName='test053', date ='2015-06-11', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-25-27', 'a', sessionTypes['tc'])
site1.add_session('15-46-05', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-06-12', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('18-16-46', 'a', sessionTypes['tc'])
site1.add_session('18-29-46', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-06-15', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-40-34', 'a', sessionTypes['tc'])
site1.add_session('16-05-58', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-06-17', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('10-21-24', 'a', sessionTypes['tc'])
site1.add_session('10-40-01', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-06-18', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('10-10-17', 'a', sessionTypes['tc'])
site1.add_session('10-34-39', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-06-19', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('10-18-26', 'a', sessionTypes['tc'])
site1.add_session('10-33-57', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-06-22', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-24-05', 'a', sessionTypes['tc'])
site1.add_session('11-41-15', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-06-25', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-27-19', 'a', sessionTypes['tc'])
site1.add_session('11-42-24', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-06-26', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-02-35', 'a', sessionTypes['tc'])
site1.add_session('11-25-16', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-06-29', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.250, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-18-05', 'a', sessionTypes['tc'])
site1.add_session('11-30-24', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-07-01', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.5, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-03-39', 'a', sessionTypes['tc'])
site1.add_session('11-17-27', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)
'''
exp = cellDB.Experiment(animalName='test053', date ='2015-07-02', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.5, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-53-07', 'a', sessionTypes['tc'])
site1.add_session('12-12-03', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

'''
exp = cellDB.Experiment(animalName='test053', date ='2015-07-03', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.5, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-41-36', 'a', sessionTypes['tc'])
site1.add_session('16-50-19', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-07-06', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.5, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-21-17', 'a', sessionTypes['tc'])
site1.add_session('11-35-54', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-07-07', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-08-31', 'a', sessionTypes['tc'])
site1.add_session('17-21-43', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-07-08', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-49-36', 'a', sessionTypes['tc'])
site1.add_session('13-06-14', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-07-09', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-46-39', 'a', sessionTypes['tc'])
site1.add_session('17-02-43', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-07-10', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-17-45', 'a', sessionTypes['tc'])
site1.add_session('13-33-33', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-07-13', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-25-52', 'a', sessionTypes['tc'])
site1.add_session('13-40-41', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

#THIS SESSION DOES NOT HAVE A TUNING SESSION BECUAUSE THERE WAS NO SOUND RESPONSE
exp = cellDB.Experiment(animalName='test053', date ='2015-07-14', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-36-39', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='test053', date ='2015-07-15', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-56-39', 'a', sessionTypes['tc'])
site1.add_session('16-09-03', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-07-16', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-50-13', 'a', sessionTypes['tc'])
site1.add_session('14-08-07', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-07-17', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-20-47', 'a', sessionTypes['tc'])
site1.add_session('14-39-27', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-07-22', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.5, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-03-32', 'a', sessionTypes['tc'])
site1.add_session('16-20-38', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-07-23', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-18-43', 'a', sessionTypes['tc'])
site1.add_session('17-31-28', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-07-24', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-04-47', 'a', sessionTypes['tc'])
site1.add_session('11-56-39', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test053', date ='2015-07-27', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.425, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-37-18', 'a', sessionTypes['tc'])
site1.add_session('13-57-32', 'a', sessionTypes['2afc'], paradigm='2afc')
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
