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

badSessionList = []#prints bad sessions at end

'''
exp = cellDB.Experiment(animalName='adap024', date ='2016-08-04', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-01-28', 'a', sessionTypes['tc'])
site1.add_session('15-11-26', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
#     badSessionList.append(exp.date)
'''
exp = cellDB.Experiment(animalName='adap024', date ='2016-08-05', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-03-56', 'a', sessionTypes['tc'])
site1.add_session('16-18-09', 'a', sessionTypes['2afc'], paradigm='2afc')
#try:
     #sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
#except:
     #badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap024', date ='2016-08-06', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-08-30', 'a', sessionTypes['tc'])
site1.add_session('14-33-23', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap024', date ='2016-08-09', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-34-03', 'a', sessionTypes['tc'])
site1.add_session('15-42-44', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)
'''
exp = cellDB.Experiment(animalName='adap024', date ='2016-08-10', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-46-39', 'a', sessionTypes['tc'])
site1.add_session('17-02-23', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)
'''
print 'error with sessions: '
for badSes in badSessionList:
    print badSes
