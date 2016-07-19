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
 
exp0915 = cellDB.Experiment(animalName='arch003', date ='2015-09-15', experimenter='lan', defaultParadigm='laser_tuning_curve')


site1 = exp0915.add_site(depth = 2300, tetrodes = [3,4]) 
site1.add_session('12-06-54', None, sessionTypes['nb']) #amp=0.1
site1.add_session('12-10-13', 'a', sessionTypes['ls'], paradigm='lasersounds') #1mW, laser front&back overhang=0.01s, ITI=0.9s
site1.add_session('12-13-27', 'b', sessionTypes['ls'], paradigm='lasersounds') #1mW, laser front&back overhang=0.05s, ITI=0.5s
site1.add_session('12-15-41', 'c', sessionTypes['ls'], paradigm='lasersounds') #1mW, laser front&back overhang=0.05s, ITI=1.5s
site1.add_session('12-19-30', None, sessionTypes['lp']) #1mW
sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,1,3,4], mainTCind=None, mainSTRind=None)


site2 = exp0915.add_site(depth = 2400, tetrodes = [3,4,6])  
site2.add_session('12-27-19', None, sessionTypes['nb'])
site2.add_session('12-29-31', 'd', sessionTypes['ls'], paradigm='lasersounds') #1mW, laser front&back overhang=0.05s, ITI=1.5s
site2.add_session('12-33-19', 'e', sessionTypes['ls'], paradigm='lasersounds') #1.5mW,laser front&back overhang=0.05s, ITI=1.5s
site2.add_session('12-37-13', 'f', sessionTypes['ls'], paradigm='lasersounds') #2mW,laser front&back overhang=0.05s, ITI=1.5s
site2.add_session('12-39-24', 'a', sessionTypes['tc']) 
sitefuncs.nick_lan_daily_report(site2, 'site2', mainRasterInds=[0,1,2,3], mainTCind=4, mainSTRind=None)


site3 = exp0915.add_site(depth = 2600, tetrodes = [3,4,6]) 
site3.add_session('13-00-07', None, sessionTypes['nb']) 
site3.add_session('13-02-24', 'g', sessionTypes['ls'],paradigm='lasersounds') #1.5mW, laser front&back overhang=0.05s, ITI=1.5s
site3.add_session('13-06-58', 'h', sessionTypes['ls'],paradigm='lasersounds') #1.5mW, laser front overhang=0.08s, back overhang=0.05s, ITI=1.5s
site3.add_session('13-09-44', None, sessionTypes['lp']) #1.5mW
site3.add_session('13-14-04', None, sessionTypes['lt']) #1.5mW, ITI=2s
site3.add_session('13-19-31', 'i', sessionTypes['ls'],paradigm='lasersounds') #2.5mW, laser front overhang=0.05s, back overhang=0.05s, ITI=2s. 
site3.add_session('13-26-54', 'j', sessionTypes['ls'],paradigm='lasersounds') #2.0mW, laser front overhang=0.05s, back overhang=0.05s, ITI=1.5s.
sitefuncs.nick_lan_daily_report(site3, 'site3', mainRasterInds=[0,1,3,4], mainTCind=None, mainSTRind=None)


site4 = exp0915.add_site(depth = 2800, tetrodes = [3,4,6])
site4.add_session('13-34-09', None, sessionTypes['nb']) 
site4.add_session('13-36-30', None, sessionTypes['lp'])#2mW
site4.add_session('13-38-16', 'k', sessionTypes['ls'] ,paradigm='lasersounds')#2.0mW, laser front overhang=0.05s, back overhang=0.05s, ITI=1.5s
site4.add_session('13-42-14', 'l', sessionTypes['ls'] ,paradigm='lasersounds')#2.0mW, laser front overhang=0.10s, back overhang=0.01s, ITI=1.5s
sitefuncs.nick_lan_daily_report(site4, 'site4', mainRasterInds=[0,1,2,3], mainTCind= None, mainSTRind=None)


site5 = exp0915.add_site(depth = 2900, tetrodes = [3,4,6])
site5.add_session('13-49-00', None, sessionTypes['nb'])
site5.add_session('13-51-39', None, sessionTypes['lp'])
site5.add_session('13-54-56', 'm', sessionTypes['ls'], paradigm='lasersounds') #2.0mW, laser front overhang=0.05s, back overhang=0.05s, ITI=1.5s.
sitefuncs.nick_lan_daily_report(site5, 'site5', mainRasterInds=[0,1,2], mainSTRind=None, mainTCind=None) 


site6 = exp0915.add_site(depth = 3000, tetrodes = [3,4,6])
site6.add_session('14-05-05', None, sessionTypes['nb'])
site6.add_session('14-07-29', None, sessionTypes['lp']) 
site6.add_session('14-11-33', 'n', sessionTypes['ls'], paradigm='lasersounds')#2.0mW, laser front overhang=0.05s, back overhang=0.05s, ITI=1.5s
site6.add_session('14-15-58', 'o', sessionTypes['ls'], paradigm='lasersounds')#3.0mW, laser front overhang=0.05s, back overhang=0.05s, ITI=1.5s
site6.add_session('14-22-21', 'p', sessionTypes['ls'], paradigm='lasersounds')#3.0mW, laser front overhang=0.10s, back overhang=0.01s, ITI=1.5s
sitefuncs.nick_lan_daily_report(site6, 'site6', mainRasterInds=[0,1,2,3], mainSTRind=None, mainTCind=None) 


site7 = exp0915.add_site(depth = 3100, tetrodes = [3,4,6])
site7.add_session('14-28-43', None, sessionTypes['nb'])
site7.add_session('14-38-35', 'q', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.05s, back overhang=0.05s, ITI=1.5s
site7.add_session('14-54-01', None, sessionTypes['lp']) #3mW,50ms
site7.add_session('14-58-08', 'b', sessionTypes['tc'])
site7.add_session('15-28-38', 'r', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.10s, back overhang=0.05s, ITI=1.5s 
sitefuncs.nick_lan_daily_report(site7, 'site7', mainRasterInds=[0,1,2,4], mainSTRind=None, mainTCind=3) 


site8 = exp0915.add_site(depth = 3200, tetrodes = [3,4,6])
site8.add_session('15-36-25', None, sessionTypes['nb'])
site8.add_session('15-39-14', None, sessionTypes['lp']) #3mW,50ms pulses
site8.add_session('15-41-43', 's', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.05s, back overhang=0.05s, ITI=1.5s

sitefuncs.nick_lan_daily_report(site8, 'site8', mainRasterInds=[0,1,2], mainSTRind=None, mainTCind=None)


site9 = exp0915.add_site(depth = 3300, tetrodes = [3,4,6])
site9.add_session('15-49-00', None, sessionTypes['nb'])
site9.add_session('15-51-12', None, sessionTypes['lp']) #3mW,50ms pulses
site9.add_session('15-53-37', 't', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.01s, back overhang=0.01s, ITI=1.5s
site9.add_session('15-56-24', 'u', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.05s, back overhang=0.01s, ITI=1.5s
sitefuncs.nick_lan_daily_report(site9, 'site9', mainRasterInds=[0,1,2,3], mainSTRind=None, mainTCind=None)


site10 = exp0915.add_site(depth = 3400, tetrodes = [3,4,6])
site10.add_session('16-05-27', None, sessionTypes['nb'])
site10.add_session('16-07-35', None, sessionTypes['lp']) #3mW,50ms pulses
site10.add_session('16-11-03', 'v', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.01s, back overhang=0.01s, ITI=1.5s
site10.add_session('16-14-04', 'w', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.05s, back overhang=0.01s, ITI=1.5s
sitefuncs.nick_lan_daily_report(site10, 'site10', mainRasterInds=[0,1,2,3], mainSTRind=None, mainTCind=None)


site11 = exp0915.add_site(depth = 3500, tetrodes = [3,4,6])
site11.add_session('16-22-42', None, sessionTypes['nb'])
site11.add_session('16-25-17', None, sessionTypes['lp']) #3mW,50ms pulses
site11.add_session('16-27-09', 'x', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.01s, back overhang=0.01s, ITI=1.5s
site11.add_session('16-29-56', 'y', sessionTypes['ls'], paradigm='lasersounds') #3.0mW, laser front overhang=0.05s, back overhang=0.01s, ITI=1.5s
sitefuncs.nick_lan_daily_report(site11, 'site11', mainRasterInds=[0,1,2,3], mainSTRind=None, mainTCind=None)

