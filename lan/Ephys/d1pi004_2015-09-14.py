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
 
exp0914 = cellDB.Experiment(animalName='d1pi004', date ='2015-09-14', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp0914.add_site(depth = 3040, tetrodes = range(1,9)) #all TTs laser-responsive, TT7 clearly sound-responsive
site1.add_session('10-41-47', None, sessionTypes['lp']) #1mW,10ms
site1.add_session('10-44-04', None, sessionTypes['nb']) #amp=0.1
site1.add_session('10-48-08', None, sessionTypes['lt'])
site1.add_session('10-51-08', 'a', sessionTypes['tc']) 
site1.add_session('11-24-34', 'a', sessionTypes['2afc'], paradigm='2afc')#need to specific paradigm to overwrite the default since it's a different paradigm 

sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0,1,2], mainTCind=3, mainSTRind=None)

sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=4)

