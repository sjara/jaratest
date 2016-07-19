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
                'str':'sortedTuningRaster',
		'ls':'lasersounds'}
 
exp0918 = cellDB.Experiment(animalName='arch003', date ='2015-09-18', experimenter='lan', defaultParadigm='laser_tuning_curve')

'''
site1 = exp0918.add_site(depth = 2200, tetrodes = [3,4]) 
site1.add_session('12-41-22', None, sessionTypes['nb']) #amp=0.1
site1.add_session('12-43-56', None, sessionTypes['lp']) #2mW,50ms
site1.add_session('12-46-49', None, sessionTypes['lp']) #2mW,100ms
site1.add_session('12-48-29', None, sessionTypes['nb']) #amp=0.2
sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,1,2,3], mainTCind=None, mainSTRind=None)


site2 = exp0918.add_site(depth = 2300, tetrodes = [3,4])  
site2.add_session('12-52-15', None, sessionTypes['nb'])
site2.add_session('12-54-29', None, sessionTypes['lp']) #2mW
site2.add_session('12-57-34', 'a', sessionTypes['ls'], paradigm='lasersounds') #2mW, laser front&back overhang=0.05s, ITI=1.5s

sitefuncs.nick_lan_daily_report(site2, 'site2', mainRasterInds=[0,1,2], mainTCind=None, mainSTRind=None)


site3 = exp0918.add_site(depth = 2400, tetrodes = [3,4]) 
site3.add_session('13-13-17', None, sessionTypes['nb']) 
site3.add_session('13-15-52', None, sessionTypes['lp']) #2mW
site3.add_session('13-19-09', None, sessionTypes['nb']) 
site3.add_session('13-21-02', 'b', sessionTypes['ls'],paradigm='lasersounds') #2mW, laser front&back overhang=0.05s, ITI=1.5s
site3.add_session('13-27-07', None, sessionTypes['lp']) #3mW
site3.add_session('13-29-32', 'c', sessionTypes['ls'],paradigm='lasersounds') #3mW, laser front overhang=0.05s, back overhang=0.05s, ITI=1.5s

sitefuncs.nick_lan_daily_report(site3, 'site3', mainRasterInds=[2,3,4,5], mainTCind=None, mainSTRind=None)


site4 = exp0918.add_site(depth = 2500, tetrodes = [3,4])
site4.add_session('13-37-59', None, sessionTypes['nb']) 
site4.add_session('13-40-37', None, sessionTypes['lp'])#3mW
site4.add_session('13-43-54', 'd', sessionTypes['ls'] ,paradigm='lasersounds')#3.0mW, laser front overhang=0.05s, back overhang=0.05s, ITI=1.5s

sitefuncs.nick_lan_daily_report(site4, 'site4', mainRasterInds=[0,1,2], mainTCind= None, mainSTRind=None)


site5 = exp0918.add_site(depth = 2650, tetrodes = [3,4])
site5.add_session('13-50-00', None, sessionTypes['lp'])
site5.add_session('13-52-15', None, sessionTypes['nb']) #amp=0.1
site5.add_session('13-54-13', None, sessionTypes['nb']) #amp=0.2
site5.add_session('13-56-14', 'e', sessionTypes['ls'], paradigm='lasersounds') #2.0mW, laser front overhang=0.05s, back overhang=0.05s, ITI=1.5s.
sitefuncs.nick_lan_daily_report(site5, 'site5', mainRasterInds=[0,2,3], mainSTRind=None, mainTCind=None) 
'''

site6 = exp0918.add_site(depth = 2800, tetrodes = [3,4])
site6.add_session('14-22-28', None, sessionTypes['nb'])
site6.add_session('14-25-29', None, sessionTypes['lp']) 
site6.add_session('14-29-57', 'f', sessionTypes['ls'], paradigm='lasersounds')#2.0mW, laser front overhang=0.05s, back overhang=0.05s, ITI=1.5s

sitefuncs.nick_lan_daily_report(site6, 'site6', mainRasterInds=[0,1,2], mainSTRind=None, mainTCind=None) 


site7 = exp0918.add_site(depth = 2950, tetrodes = [3,4,6])
site7.add_session('14-37-08', None, sessionTypes['lp'])
site7.add_session('14-39-55', None, sessionTypes['nb'])
site7.add_session('14-42-46', 'g', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.05s, back overhang=0.05s, ITI=1.5s

sitefuncs.nick_lan_daily_report(site7, 'site7', mainRasterInds=[0,1,2], mainSTRind=None, mainTCind=None) 


site8 = exp0918.add_site(depth = 3050, tetrodes = [3,4,6])
site8.add_session('14-52-16', None, sessionTypes['lp'])#3mW,100ms pulses
site8.add_session('14-54-43', None, sessionTypes['nb']) 
site8.add_session('14-57-51', 'h', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.025s, back overhang=0.025s, ITI=1.5s
site8.add_session('15-03-46', 'a', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site8, 'site8', mainRasterInds=[0,1,2], mainSTRind=None, mainTCind=3)


site9 = exp0918.add_site(depth = 3150, tetrodes = [3,4,6])
site9.add_session('15-23-41', None, sessionTypes['lp']) #3mW, 50ms@1Hz
site9.add_session('15-25-41', None, sessionTypes['nb']) 
site9.add_session('15-28-28', 'i', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.025s, back overhang=0.025s, ITI=1.5s
site9.add_session('15-34-16', 'j', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.01s, back overhang=0.01s, ITI=1.5s
sitefuncs.nick_lan_daily_report(site9, 'site9', mainRasterInds=[0,1,2,3], mainSTRind=None, mainTCind=None)


site10 = exp0918.add_site(depth = 3250, tetrodes = [3,4,6])
site10.add_session('15-43-14', None, sessionTypes['lp'])#3mW,100ms pulses
site10.add_session('15-45-38', None, sessionTypes['nb']) 
site10.add_session('15-47-59', 'k', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.01s, back overhang=0.01s, ITI=1.5s
site10.add_session('15-53-53', 'l', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.05s, back overhang=0.01s, ITI=1.5s
site10.add_session('15-57-22', 'b', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site10, 'site10', mainRasterInds=[0,1,2,3], mainSTRind=None, mainTCind=4)


site11 = exp0918.add_site(depth = 3350, tetrodes = [3,4,6])
site11.add_session('16-17-29', None, sessionTypes['lp']) #3mW,50ms pulses
site11.add_session('16-19-29', None, sessionTypes['nb']) 
site11.add_session('16-21-45', 'm', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.01s, back overhang=0.01s, ITI=1.5s
site11.add_session('16-29-45', 'n', sessionTypes['ls'], paradigm='lasersounds') #restarted OE here. 3.0mW, laser front overhang=0.05s, back overhang=0.01s, ITI=1.5s
site11.add_session('16-37-13', 'c', sessionTypes['tc'])
sitefuncs.nick_lan_daily_report(site11, 'site11', mainRasterInds=[0,1,2,3], mainSTRind=None, mainTCind=4)


site12 = exp0918.add_site(depth = 3350, tetrodes = [3,4,6])
site12.add_session('16-56-37', None, sessionTypes['lp']) #3mW,50ms pulses
site12.add_session('16-58-47', None, sessionTypes['nb']) 
site12.add_session('17-01-46', 'o', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.01s, back overhang=0.01s, ITI=1.5s

