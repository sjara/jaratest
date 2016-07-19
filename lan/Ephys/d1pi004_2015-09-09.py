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
 
exp0909 = cellDB.Experiment(animalName='d1pi004', date ='2015-09-09', experimenter='lan', defaultParadigm='laser_tuning_curve')


site1 = exp0909.add_site(depth = 3040, tetrodes = range(1,9)) #laser-responsive, not sound-responsive
site1.add_session('10-49-06', None, sessionTypes['nb']) #amp=0.1
site1.add_session('10-54-12', None, sessionTypes['nb'])  #amp=0.15
site1.add_session('10-58-43', None, sessionTypes['lp']) #ref=chan6
site1.add_session('11-03-37', None, sessionTypes['lp']) #ref=chan26
site1.add_session('11-16-49', None, sessionTypes['lt']) #ref=chan26
sitefuncs.nick_lan_daily_report_short(site1, 'site1', mainRasterInds=[1, 2, 3, 4])


