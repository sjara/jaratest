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
                'str':'sortedTuningRaster'}
 
exp0910 = cellDB.Experiment(animalName='arch003', date ='2015-09-10', experimenter='lan', defaultParadigm='laser_tuning_curve')

'''
site1 = exp0910.add_site(depth = 2150, tetrodes = [3,4]) 
site1.add_session('11-50-41', None, sessionTypes['nb']) #amp=0.1
site1.add_session('11-55-15', None, sessionTypes['nb']) 
site1.add_session('11-57-38', None, sessionTypes['lp']) #
site1.add_session('12-00-16', None, sessionTypes['lt']) #
site1.add_session('12-02-22', 'a', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[1,2,3], mainTCind=4, mainSTRind=None)


site2 = exp0910.add_site(depth = 2250, tetrodes = [3,4])  
site2.add_session('12-25-24', None, sessionTypes['nb'])
site2.add_session('12-27-58', None, sessionTypes['lp']) #1mW
site2.add_session('12-30-18', None, sessionTypes['lp']) #1.5mW
site2.add_session('12-32-25', None, sessionTypes['lt']) #1.5mW
 
sitefuncs.nick_lan_daily_report(site2, 'site2', mainRasterInds=[0, 1, 2, 3], mainTCind=None, mainSTRind=None)


site3 = exp0910.add_site(depth = 2340, tetrodes = [3,4,6]) 
site3.add_session('12-38-22', None, sessionTypes['nb']) 
site3.add_session('12-40-51', None, sessionTypes['lp']) #2mW
site3.add_session('12-43-11', None, sessionTypes['lt']) #2mW
site3.add_session('12-46-34', None, sessionTypes['lp']) #1mW
site3.add_session('12-49-13', 'b', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site3, 'site3', mainRasterInds=[0,1,2,3], mainTCind=4, mainSTRind=None)


site4 = exp0910.add_site(depth = 2440, tetrodes = [3,4,6])
site4.add_session('13-11-19', None, sessionTypes['nb']) 
site4.add_session('13-13-47', None, sessionTypes['lp'])#1.5mW
site4.add_session('13-16-28', None, sessionTypes['lt'])#1.5mW
site4.add_session('13-19-37', None, sessionTypes['lp']) #50ms pulses,1.5mW
site4.add_session('13-27-25', 'c', sessionTypes['str']) #tuningAM
site4.add_session('13-39-04', None, sessionTypes['lp'])#2.0mW
sitefuncs.nick_lan_daily_report(site4, 'site4', mainRasterInds=[0,1,2,3], mainTCind= None, mainSTRind=4)


site5 = exp0910.add_site(depth = 2500, tetrodes = [3,4,6])
site5.add_session('13-44-13', None, sessionTypes['nb'])
site5.add_session('13-46-54', None, sessionTypes['lp'])
site5.add_session('13-49-24', None, sessionTypes['lt'])
site5.add_session('13-52-37', 'd', sessionTypes['str'])#tuningAM
site5.add_session('14-09-10', None, sessionTypes['lp']) #50ms pulses,2mW
site5.add_session('14-12-15', 'e', sessionTypes['tc'])
site5.add_session('14-29-32', None, sessionTypes['lp'])
sitefuncs.nick_lan_daily_report(site5, 'site5', mainRasterInds=[0,1,2,4], mainSTRind=3, mainTCind=5) 
'''

site6 = exp0910.add_site(depth = 2600, tetrodes = [3,4,6])
site6.add_session('14-35-07', None, sessionTypes['nb'])
site6.add_session('14-37-36', None, sessionTypes['lp']) 
site6.add_session('14-40-19', None, sessionTypes['lt']) #BL FR decreased
site6.add_session('14-44-19', None, sessionTypes['lp']) #50ms pulses@1Hz; BL FR low.
site6.add_session('14-47-16', None, sessionTypes['lp']) #50ms pulses@0.5Hz; BL FR low.
site6.add_session('14-49-47', None, sessionTypes['nb']) #BL FR increased
site6.add_session('14-52-29', 'f', sessionTypes['str'])

sitefuncs.nick_lan_daily_report(site6, 'site6', mainRasterInds=[0,1,2,3], mainSTRind=6, mainTCind=None) 


site7 = exp0910.add_site(depth = 2700, tetrodes = [3,4,6])
site7.add_session('15-06-40', None, sessionTypes['nb'])
site7.add_session('15-09-30', None, sessionTypes['lp']) #2mW,50ms pulses@0.5Hz
site7.add_session('15-13-36', None, sessionTypes['lt']) #2mW,@0.5Hz
site7.add_session('15-18-07', 'g', sessionTypes['str'])
site7.add_session('15-36-42', 'h', sessionTypes['tc'])

sitefuncs.nick_lan_daily_report(site7, 'site7', mainRasterInds=[0,1,2], mainSTRind=3, mainTCind=4) 

site8 = exp0910.add_site(depth = 2800, tetrodes = [3,4,6])
site8.add_session('16-01-40', None, sessionTypes['nb'])
site8.add_session('16-04-26', None, sessionTypes['lp']) #1mW,50ms pulses@0.5Hz
site8.add_session('16-07-45', None, sessionTypes['lt']) #1mW,@0.5Hz
site8.add_session('16-11-43', 'i', sessionTypes['str'])
site8.add_session('16-28-30', 'j', sessionTypes['tc'])

sitefuncs.nick_lan_daily_report(site8, 'site8', mainRasterInds=[0,1,2], mainSTRind=3, mainTCind=4)


site9 = exp0910.add_site(depth = 2900, tetrodes = [3,4,6])
site9.add_session('16-46-49', None, sessionTypes['nb'])
site9.add_session('16-49-06', None, sessionTypes['lp']) #1mW,50ms pulses@0.5Hz
site9.add_session('16-51-58', None, sessionTypes['lt']) #1mW,@0.5Hz
site9.add_session('16-55-46', 'k', sessionTypes['tc'])

sitefuncs.nick_lan_daily_report(site9, 'site9', mainRasterInds=[0,1,2], mainSTRind=None, mainTCind=3)


