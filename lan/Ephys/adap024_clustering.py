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

badSessionList=[]

'''
exp = cellDB.Experiment(animalName='adap024', date ='2016-07-05', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=0.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-44-11', 'a', sessionTypes['tc'])
site1.add_session('15-59-24', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap024', date ='2016-07-07', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=0.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-07-08', 'a', sessionTypes['tc'])
site1.add_session('14-28-46', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap024', date ='2016-07-08', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=0.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-13-18', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap024', date ='2016-07-09', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=0.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('18-50-30', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap024', date ='2016-07-12', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=0.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-26-16', 'a', sessionTypes['tc'])
site1.add_session('14-43-36', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap024', date ='2016-07-13', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=0.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-09-10', 'a', sessionTypes['tc'])
site1.add_session('16-22-44', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

'''

exp = cellDB.Experiment(animalName='adap024', date ='2016-07-14', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-35-05', 'a', sessionTypes['tc'])
site1.add_session('14-46-01', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

'''
exp = cellDB.Experiment(animalName='adap024', date ='2016-07-20', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-41-54', 'a', sessionTypes['tc'])
site1.add_session('15-55-39', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap024', date ='2016-07-21', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=1.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-24-01', 'a', sessionTypes['tc'])
site1.add_session('14-53-43', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)
'''
