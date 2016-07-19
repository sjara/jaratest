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
 
exp0911 = cellDB.Experiment(animalName='d1pi004', date ='2015-09-11', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp0911.add_site(depth = 3040, tetrodes = range(1,9)) #all TTs laser-responsive, TT7 weakly sound-responsive
site1.add_session('14-41-04', None, sessionTypes['nb']) #amp=0.1
site1.add_session('14-44-43', None, sessionTypes['lp']) #1mW,10ms
site1.add_session('14-49-22', 'a', sessionTypes['2afc'], paradigm='2afc')#need to specific paradigm to overwrite the default since it's a different paradigm 
site1.add_session('15-54-50', None, sessionTypes['lt']) #1mW

#sitefuncs.nick_lan_daily_report_short(site1, 'site1', mainRasterInds=[0,1,2,3])

sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=2)

#sitefuncs.lan_2afc_ephys_plots_debug(site1, 'site1', main2afcind=2)
