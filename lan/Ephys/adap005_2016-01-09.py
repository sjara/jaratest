from jaratoolbox.test.nick.database import cellDB
reload(cellDB)
from jaratoolbox.test.lan.Ephys import sitefuncs_vlan as sitefuncs
reload(sitefuncs)
from jaratoolbox.test.lan import test012_add_good_clusters as test012

sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse',
                '2afc':'2afc'}
 
exp = cellDB.Experiment(animalName='adap005', date ='2016-01-09', experimenter='lan', defaultParadigm='laser_tuning_curve') 


site1 = exp.add_site(depth=2520, tetrodes=[1,2,3,4,5,6,7,8]) 
site1.add_session('14-02-54', None, sessionTypes['nb']) #amp=0.15
site1.add_session('14-10-44', 'a', sessionTypes['tc']) #2-40Hz chords, 50dB
site1.add_session('14-21-47', 'a', sessionTypes['2afc'], paradigm='2afc')

#sitefuncs.nick_lan_daily_report(site1, 'site1', mainRasterInds=[0], mainTCind=1, mainSTRind=1)
#sitefuncs.lan_2afc_ephys_plots(site1, 'site1', main2afcind=2, tetrodes=[1,2,3,4,5,6,7,8]) 
#sitefuncs.lan_2afc_ephys_plots_each_type(site1, 'site1', main2afcind=2, tetrodes=[5,6,7,8],trialLimit=[])
#sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=2, tetrodes=[3,4,5,6,7,8],trialLimit=[],choiceSide='both') 
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=2, tetrodes=[1,3,4,5,6,7,8],trialLimit=[],choiceSide='left')
sitefuncs.lan_2afc_ephys_plots_each_block_each_type(site1, 'site1', main2afcind=2, tetrodes=[1,3,4,5,6,7,8],trialLimit=[],choiceSide='right')

clusterQuality={1:[3,1,4,1,1,1,1,1,2,4,2,1],2:[4,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,4,1,2,4,1,1,1,2,1],4:[3,1,1,1,1,1,2,1,1,1,1,1],5:[3,1,1,1,1,1,1,1,1,1,1,0],6:[3,4,4,1,1,4,4,4,3,3,2,1],7:[3,4,3,4,2,4,4,2,4,2,1,2],8:[3,1,4,1,1,4,1,1,1,1,1,4]}

clustersEachTetrode=test012.add_good_cluster_cellDB(clusterQuality)

print clustersEachTetrode
