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


exp = cellDB.Experiment(animalName='test055', date ='2015-02-20', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.5, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-32-33', 'a', sessionTypes['tc'])
site1.add_session('11-42-48', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)


exp = cellDB.Experiment(animalName='test055', date ='2015-02-21', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.5, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('18-29-58', 'a', sessionTypes['tc'])
site1.add_session('18-38-13', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
'''
exp = cellDB.Experiment(animalName='test055', date ='2015-02-22', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('22-34-57', 'a', sessionTypes['tc'])
site1.add_session('22-42-06', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-02-23', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-14-28', 'a', sessionTypes['tc'])
site1.add_session('13-23-03', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-02-24', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=4.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-06-58', 'a', sessionTypes['tc'])
site1.add_session('13-19-06', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-02-25', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.0, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-27-27', 'a', sessionTypes['tc'])
site1.add_session('12-38-09', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-02-26', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.0, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-54-53', 'a', sessionTypes['tc'])
site1.add_session('13-06-01', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-02-27', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-03-38', 'a', sessionTypes['tc'])
site1.add_session('13-15-39', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-02-28', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.5, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('18-36-26', 'a', sessionTypes['tc'])
site1.add_session('19-02-10', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-01', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-43-54', 'a', sessionTypes['tc'])
site1.add_session('16-53-27', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)
'''
exp = cellDB.Experiment(animalName='test055', date ='2015-03-02', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-43-43', 'a', sessionTypes['tc'])
site1.add_session('13-35-20', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

'''
exp = cellDB.Experiment(animalName='test055', date ='2015-03-03', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-31-53', 'a', sessionTypes['tc'])
site1.add_session('11-42-14', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-04', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-49-30', 'a', sessionTypes['tc'])
site1.add_session('13-02-28', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-05', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-01-13', 'a', sessionTypes['tc'])
site1.add_session('14-12-36', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-06', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=5.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-20-11', 'a', sessionTypes['tc'])
site1.add_session('12-30-25', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-07', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('20-51-06', 'a', sessionTypes['tc'])
site1.add_session('21-00-17', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-08', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('20-56-29', 'a', sessionTypes['tc'])
site1.add_session('21-05-54', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)
'''
exp = cellDB.Experiment(animalName='test055', date ='2015-03-09', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-07-25', 'a', sessionTypes['tc'])
site1.add_session('15-15-58', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

'''
exp = cellDB.Experiment(animalName='test055', date ='2015-03-10', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-57-29', 'a', sessionTypes['tc'])
site1.add_session('14-08-40', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-11', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-12-49', 'a', sessionTypes['tc'])
site1.add_session('13-23-02', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-12', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('10-59-54', 'a', sessionTypes['tc'])
site1.add_session('11-39-19', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-13', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-43-58', 'a', sessionTypes['tc'])
site1.add_session('11-53-29', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-15', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-57-26', 'a', sessionTypes['tc'])
site1.add_session('13-08-56', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-16', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-05-34', 'a', sessionTypes['tc'])
site1.add_session('11-20-30', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)
'''
exp = cellDB.Experiment(animalName='test055', date ='2015-03-17', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-11-51', 'a', sessionTypes['tc'])
site1.add_session('12-21-27', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)

'''
exp = cellDB.Experiment(animalName='test055', date ='2015-03-18', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-32-16', 'a', sessionTypes['tc'])
site1.add_session('15-42-32', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-19', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-55-30', 'a', sessionTypes['tc'])
site1.add_session('15-04-52', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-20', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-24-44', 'a', sessionTypes['tc'])
site1.add_session('11-34-22', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-21', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-24-17', 'a', sessionTypes['tc'])
site1.add_session('15-33-38', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-22', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('18-51-29', 'a', sessionTypes['tc'])
site1.add_session('19-01-22', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-23', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-24-58', 'a', sessionTypes['tc'])
site1.add_session('12-39-08', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-24', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-18-08', 'a', sessionTypes['tc'])
site1.add_session('12-33-05', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-25', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=6.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-33-59', 'a', sessionTypes['tc'])
site1.add_session('12-44-37', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-26', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-08-11', 'a', sessionTypes['tc'])
site1.add_session('11-18-10', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-27', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-10-22', 'a', sessionTypes['tc'])
site1.add_session('12-31-11', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-28', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('20-21-59', 'a', sessionTypes['tc'])
site1.add_session('20-36-26', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-29', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('23-05-58', 'a', sessionTypes['tc'])
site1.add_session('23-16-17', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-30', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-22-02', 'a', sessionTypes['tc'])
site1.add_session('12-32-26', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-03-31', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-41-30', 'a', sessionTypes['tc'])
site1.add_session('11-50-55', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-01', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-55-00', 'a', sessionTypes['tc'])
site1.add_session('13-04-43', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-03', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-50-49', 'a', sessionTypes['tc'])
site1.add_session('15-03-35', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-06', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-04-36', 'a', sessionTypes['tc'])
site1.add_session('15-15-25', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-07', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('19-00-01', 'a', sessionTypes['tc'])
site1.add_session('19-08-51', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-08', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-01-40', 'a', sessionTypes['tc'])
site1.add_session('12-12-18', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-09', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-06-56', 'a', sessionTypes['tc'])
site1.add_session('12-17-28', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-10', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-21-47', 'a', sessionTypes['tc'])
site1.add_session('12-34-00', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-11', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('18-21-01', 'a', sessionTypes['tc'])
site1.add_session('18-30-24', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-13', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-37-20', 'a', sessionTypes['tc'])
site1.add_session('15-54-20', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-14', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-57-30', 'a', sessionTypes['tc'])
site1.add_session('12-09-18', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-15', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-16-31', 'a', sessionTypes['tc'])
site1.add_session('12-29-45', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-16', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-28-54', 'a', sessionTypes['tc'])
site1.add_session('13-38-38', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)
'''
exp = cellDB.Experiment(animalName='test055', date ='2015-04-17', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('16-01-57', 'a', sessionTypes['tc'])
site1.add_session('16-21-33', 'a', sessionTypes['2afc'], paradigm='2afc')
sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
'''

exp = cellDB.Experiment(animalName='test055', date ='2015-04-18', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-35-18', 'a', sessionTypes['tc'])
site1.add_session('15-43-54', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-19', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-14-01', 'a', sessionTypes['tc'])
site1.add_session('15-12-02', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-20', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=7.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-16-22', 'a', sessionTypes['tc'])
site1.add_session('13-31-52', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-21', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-34-05', 'a', sessionTypes['tc'])
site1.add_session('13-43-00', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-22', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-37-49', 'a', sessionTypes['tc'])
site1.add_session('13-47-04', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-23', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-55-57', 'a', sessionTypes['tc'])
site1.add_session('13-08-26', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-27', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-28-48', 'a', sessionTypes['tc'])
site1.add_session('15-41-55', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-28', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-37-26', 'a', sessionTypes['tc'])
site1.add_session('12-46-13', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-29', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-39-17', 'a', sessionTypes['tc'])
site1.add_session('12-48-20', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-04-30', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-49-03', 'a', sessionTypes['tc'])
site1.add_session('11-57-54', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-01', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-49-12', 'a', sessionTypes['tc'])
site1.add_session('12-59-12', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-05', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-42-29', 'a', sessionTypes['tc'])
site1.add_session('12-55-25', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-06', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-26-40', 'a', sessionTypes['tc'])
site1.add_session('12-38-47', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-07', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-39-06', 'a', sessionTypes['tc'])
site1.add_session('12-48-13', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-08', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.375, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-08-33', 'a', sessionTypes['tc'])
site1.add_session('17-17-43', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-09', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('20-23-03', 'a', sessionTypes['tc'])
site1.add_session('20-39-25', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-10', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('22-53-53', 'a', sessionTypes['tc'])
site1.add_session('23-03-22', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-11', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.50, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-14-31', 'a', sessionTypes['tc'])
site1.add_session('15-31-25', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-12', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-51-52', 'a', sessionTypes['tc'])
site1.add_session('13-01-27', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-13', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.625, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-56-55', 'a', sessionTypes['tc'])
site1.add_session('13-07-12', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-14', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-36-42', 'a', sessionTypes['tc'])
site1.add_session('12-46-29', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-15', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.75, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('11-54-55', 'a', sessionTypes['tc'])
site1.add_session('12-05-23', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-17', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('17-52-35', 'a', sessionTypes['tc'])
site1.add_session('18-01-31', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-18', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-03-21', 'a', sessionTypes['tc'])
site1.add_session('13-13-02', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-19', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-42-12', 'a', sessionTypes['tc'])
site1.add_session('12-54-16', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-26', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-03-01', 'a', sessionTypes['tc'])
site1.add_session('13-19-02', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-27', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=8.875, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-10-07', 'a', sessionTypes['tc'])
site1.add_session('12-20-52', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-28', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=9.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-39-39', 'a', sessionTypes['tc'])
site1.add_session('12-49-35', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-29', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=9.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-34-16', 'a', sessionTypes['tc'])
site1.add_session('14-00-38', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-05-30', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=9.00, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-37-32', 'a', sessionTypes['tc'])
site1.add_session('15-51-45', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-06-01', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=9.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('12-40-36', 'a', sessionTypes['tc'])
site1.add_session('12-51-07', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-06-02', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=9.125, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-21-15', 'a', sessionTypes['tc'])
site1.add_session('13-32-18', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-06-03', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=9.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('15-05-57', 'a', sessionTypes['tc'])
site1.add_session('15-16-32', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

exp = cellDB.Experiment(animalName='test055', date ='2015-06-04', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=9.25, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('14-52-58', 'a', sessionTypes['tc'])
site1.add_session('15-02-05', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)


print 'error with sessions: '
for badSes in badSessionList:
    print badSes
'''
