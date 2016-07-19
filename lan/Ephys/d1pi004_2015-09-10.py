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
 
exp0910 = cellDB.Experiment(animalName='d1pi004', date ='2015-09-10', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp0910.add_site(depth = 3040, tetrodes = range(1,9)) #not laser-responsive, TT7 weakly sound-responsive
site1.add_session('16-04-48', None, sessionTypes['nb']) #amp=0.1
site1.add_session('16-13-01', None, sessionTypes['lp']) #1mW,10ms
site1.add_session('16-17-28', None, sessionTypes['lp']) #1mW, 30ms
site1.add_session('16-19-33', None, sessionTypes['lt']) #1mW
site1.add_session('16-23-12', 'a', sessionTypes['2afc'], paradigm='2afc')#need to specific paradigm to overwrite the default since it's a different paradigm 
site1.add_session('18-00-49', None, sessionTypes['lp']) #1mW,50ms
site1.add_session('18-03-18', None, sessionTypes['nb']) #amp=0.15

#sitefuncs.nick_lan_daily_report_short(site1, 'site1', mainRasterInds=[0,1,2,3])

sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=4)
#soundOnsetTimes has length 188 while there are 189 trials, leading to indexing error
