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
 
exp1203 = cellDB.Experiment(animalName='adap011', date ='2015-12-03', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp1203.add_site(depth=2500, tetrodes=range(1,9)) 
site1.add_session('13-27-16', None, sessionTypes['nb']) #amp=0.1
site1.add_session('13-30-41', None, sessionTypes['nb']) #amp=0.2
site1.add_session('13-34-44', 'a', sessionTypes['2afc'], paradigm='2afc')#need to specific paradigm to overwrite the default since it's a different paradigm; also need to put behav file in lan folder. 

#sitefuncs.nick_lan_daily_report_short(site1, 'site1', mainRasterInds=[0,1])

sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=2, tetrodes=[1,8]) #tetrode 1&8 sound responsive  

