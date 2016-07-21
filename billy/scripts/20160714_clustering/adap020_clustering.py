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
exp = cellDB.Experiment(animalName='adap020', date ='2016-04-12', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('10-04-19', 'a', sessionTypes['tc'])
site1.add_session('10-13-27', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap020', date ='2016-04-13', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-25-33', 'a', sessionTypes['tc'])
site1.add_session('11-34-15', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap020', date ='2016-04-14', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-15-11', 'a', sessionTypes['tc'])
site1.add_session('11-33-59', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

#THIS CRASHES FOR SOME REASON
exp = cellDB.Experiment(animalName='adap020', date ='2016-04-15', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-22-20', 'a', sessionTypes['tc'])
site1.add_session('11-34-48', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap020', date ='2016-04-16', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-00-47', 'a', sessionTypes['tc'])
site1.add_session('15-10-19', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap020', date ='2016-04-18', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-30-09', 'a', sessionTypes['tc'])
site1.add_session('11-38-53', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap020', date ='2016-04-19', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-00-55', 'a', sessionTypes['tc'])
site1.add_session('11-10-14', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap020', date ='2016-04-20', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-33-22', 'a', sessionTypes['tc'])
site1.add_session('13-51-59', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
'''
#CLUSTERING CRASH: MEMORYERROR
exp = cellDB.Experiment(animalName='adap020', date ='2016-04-21', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-02-10', 'a', sessionTypes['tc'])
site1.add_session('13-19-14', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
'''
exp = cellDB.Experiment(animalName='adap020', date ='2016-04-22', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-19-38', 'a', sessionTypes['tc'])
site1.add_session('17-28-59', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap020', date ='2016-04-23', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-49-20', 'a', sessionTypes['tc'])
site1.add_session('16-00-54', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap020', date ='2016-04-24', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-18-13', 'a', sessionTypes['tc'])
site1.add_session('13-36-15', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap020', date ='2016-04-25', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.000, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-35-26', 'a', sessionTypes['tc'])
site1.add_session('11-49-47', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap020', date ='2016-04-26', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-05-27', 'a', sessionTypes['tc'])
site1.add_session('14-14-28', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap020', date ='2016-04-27', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-04-19', 'a', sessionTypes['tc'])
site1.add_session('11-21-16', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

exp = cellDB.Experiment(animalName='adap020', date ='2016-04-28', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-16-41', 'a', sessionTypes['tc'])
site1.add_session('11-28-44', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
'''
#CRASHED DURING CLUSTERING FOR SOME REASON
exp = cellDB.Experiment(animalName='adap020', date ='2016-04-29', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('10-58-59', 'a', sessionTypes['tc'])
site1.add_session('11-07-51', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
'''
exp = cellDB.Experiment(animalName='adap020', date ='2016-04-30', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-09-26', 'a', sessionTypes['tc'])
site1.add_session('16-28-23', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-02', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-30-31', 'a', sessionTypes['tc'])
site1.add_session('11-49-55', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-03', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('10-50-06', 'a', sessionTypes['tc'])
site1.add_session('11-16-08', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-04', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-13-26', 'a', sessionTypes['tc'])
site1.add_session('11-22-25', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-05', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=3.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-02-53', 'a', sessionTypes['tc'])
site1.add_session('11-20-48', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-06', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-11-39', 'a', sessionTypes['tc'])
site1.add_session('11-28-57', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-09', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-15-29', 'a', sessionTypes['tc'])
site1.add_session('15-30-51', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
    sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
    badSessionList.append(exp.date)
'''
exp = cellDB.Experiment(animalName='adap020', date ='2016-05-10', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-56-28', 'a', sessionTypes['tc'])
site1.add_session('16-05-15', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

#THIS SESSION CRASHED WHILE CLUSTERING
exp = cellDB.Experiment(animalName='adap020', date ='2016-05-11', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-42-18', 'a', sessionTypes['tc'])
site1.add_session('16-52-49', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
'''

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-12', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-03-18', 'a', sessionTypes['tc'])
site1.add_session('14-17-17', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-17', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-52-15', 'a', sessionTypes['tc'])
site1.add_session('15-23-11', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)
'''
#THIS CRASHES BECAUSE THERE ARE MORE TRIALS IN EITHER EPHYS OR BEHAVIOR (index 962 is out of bounds for 948)
exp = cellDB.Experiment(animalName='adap020', date ='2016-05-18', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-50-39', 'a', sessionTypes['tc'])
site1.add_session('17-07-55', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

'''
exp = cellDB.Experiment(animalName='adap020', date ='2016-05-19', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-37-19', 'a', sessionTypes['tc'])
site1.add_session('16-51-16', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-20', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-26-35', 'a', sessionTypes['tc'])
site1.add_session('17-36-11', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-21', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('18-05-58', 'a', sessionTypes['tc'])
site1.add_session('18-16-27', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-22', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-11-47', 'a', sessionTypes['tc'])
site1.add_session('17-24-28', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-23', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-21-25', 'a', sessionTypes['tc'])
site1.add_session('17-35-02', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-24', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-51-12', 'a', sessionTypes['tc'])
site1.add_session('16-00-48', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-25', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-22-14', 'a', sessionTypes['tc'])
site1.add_session('16-33-09', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-26', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-34-55', 'a', sessionTypes['tc'])
site1.add_session('14-44-25', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-27', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-07-26', 'a', sessionTypes['tc'])
site1.add_session('16-23-47', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-05-31', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-32-45', 'a', sessionTypes['tc'])
site1.add_session('16-46-11', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-06-01', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.500, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-52-49', 'a', sessionTypes['tc'])
site1.add_session('16-08-40', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-06-02', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.500, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-01-09', 'a', sessionTypes['tc'])
site1.add_session('15-11-46', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-06-03', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-39-15', 'a', sessionTypes['tc'])
site1.add_session('15-49-24', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-06-07', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-06-16', 'a', sessionTypes['tc'])
site1.add_session('15-14-50', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-06-08', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-47-54', 'a', sessionTypes['tc'])
site1.add_session('16-09-27', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-06-09', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-54-58', 'a', sessionTypes['tc'])
site1.add_session('15-07-54', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-06-10', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-44-32', 'a', sessionTypes['tc'])
site1.add_session('16-00-02', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-06-13', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-43-24', 'a', sessionTypes['tc'])
site1.add_session('15-59-04', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

#THIS SESSION DOES NOT HAVE A TUNING CURVE
exp = cellDB.Experiment(animalName='adap020', date ='2016-06-14', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-31-34', 'a', sessionTypes['tc'])
site1.add_session('16-42-17', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='adap020', date ='2016-06-15', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-48-55', 'a', sessionTypes['tc'])
site1.add_session('16-58-40', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)
'''
exp = cellDB.Experiment(animalName='adap020', date ='2016-06-17', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-42-44', 'a', sessionTypes['tc'])
site1.add_session('16-57-58', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

'''
exp = cellDB.Experiment(animalName='adap020', date ='2016-06-20', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-39-42', 'a', sessionTypes['tc'])
site1.add_session('15-49-04', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)
'''

print 'error with sessions: '
for badSes in badSessionList:
    print badSes
