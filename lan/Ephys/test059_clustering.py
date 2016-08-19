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


exp = cellDB.Experiment(animalName='test059', date ='2015-06-24', experimenter='', defaultParadigm='tuning_curve')
site1 = exp.add_site(depth=2.991, tetrodes=[1,2,3,4,5,6,7,8])
site1.add_session('13-23-53', 'a', sessionTypes['tc'])
site1.add_session('13-38-31', 'a', sessionTypes['2afc'], paradigm='2afc')
try:
     sitefuncs.nick_lan_daily_report_v2(site1, 'site1', mainRasterInds=None, mainTCind=0)
except:
     badSessionList.append(exp.date)

