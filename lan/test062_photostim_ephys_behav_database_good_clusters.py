#from jaratest.nick.database import cellDB
#reload(cellDB)
from jaratest.lan.Ephys import sitefuncs_vlan as sitefuncs
reload(sitefuncs)
from jaratest.lan import test053_photostim_ephys_behav_container as photostim
reload(photostim)

sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse',
                '2afc':'2afc'}


##### Mapping tetrodes to hemisphere in each mice ######
tetrodesDict={'d1pi015_righthemi':[5,6,7,8], 'd1pi015_lefthemi':[1,2,3,4], 'd1pi016_righthemi':[1,2,7,8], 'd1pi016_lefthemi':[3,4,5,6]}
########################################################

# -- D1pi016 -- #
'''
session = photostim.PhotostimSession(animalName='d1pi016', date ='2016-07-29', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2100, tetrodes=tetrodesDict['d1pi016_righthemi'], stimHemi='right')
site1.add_session('13-36-13', None, sessionTypes['nb'])
site1.add_session('13-44-18', 'a', sessionTypes['tc'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0],mainTCind=1)
site1.add_clusters(clusterDict = {1:[1],2:[3,4,8],7:[6,12],8:[8]})
site1.daily_report(mainTCind=1, main2afcind=2)


session = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-01', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2100, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
site1.add_session('13-44-05', None, sessionTypes['nb'])
site1.add_session('13-51-14', 'a', sessionTypes['tc'])
site1.add_session('13-58-16', 'b', sessionTypes['tc'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0],mainTCind=1)
site1.add_clusters(clusterDict = {4:[3,7],5:[8,10]})
site1.daily_report(mainTCind=1, main2afcind=3)


session = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-02', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2100, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
site1.add_session('14-26-07', None, sessionTypes['nb'])
site1.add_session('14-29-07', 'a', sessionTypes['tc'])
#site1.add_session('16-07-25', None, sessionTypes['lp']) #left hemi #ISI<0 at transition
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0],mainTCind=1)
site1.add_clusters(clusterDict = {4:[2,5],5:[2,4]})
site1.daily_report(mainTCind=1, main2afcind=2)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-03', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2180, tetrodes=tetrodesDict['d1pi016_righthemi'], stimHemi='right')
site1.add_session('14-04-51', None, sessionTypes['nb'])
site1.add_session('14-07-35', 'a', sessionTypes['tc'])
site1.add_session('14-19-09', 'b', sessionTypes['tc'])
#site1.add_session('14-28-12', None, sessionTypes['lp']) #right hemi  #ISI<0 at transition
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
#site1.raster_reports_all_clusters(mainRasterInds=[0],mainTCind=2)
site1.add_clusters(clusterDict = {1:[4],2:[4,8]})
site1.daily_report(mainTCind=2, main2afcind=3)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-04', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2180, tetrodes=tetrodesDict['d1pi016_righthemi'], stimHemi='right')
site1.add_session('16-15-43', 'd', sessionTypes['tc'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=None,mainTCind=0)
site1.add_clusters(clusterDict = {2:[2],7:[4]})
site1.daily_report(mainTCind=0, main2afcind=1)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-05', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2260, tetrodes=tetrodesDict['d1pi016_righthemi'],stimHemi='right')
site1.add_session('14-08-24', None, sessionTypes['nb'])
site1.add_session('14-10-47', 'a', sessionTypes['tc'])
site1.add_session('14-26-21', 'd', sessionTypes['tc'])
site1.add_session('14-31-09', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=1)
site1.add_clusters(clusterDict = {2:[5,6]})
site1.daily_report(mainTCind=1, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-06', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2260, tetrodes=tetrodesDict['d1pi016_righthemi'],stimHemi='right')
site1.add_session('16-50-41', None, sessionTypes['nb'])
site1.add_session('16-54-56', 'a', sessionTypes['tc'])
site1.add_session('17-06-06', 'c', sessionTypes['tc'])
site1.add_session('17-11-04', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=1)
site1.add_clusters(clusterDict = {2:[3,5],7:[2]})
site1.daily_report(mainTCind=1, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-08', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2260, tetrodes=tetrodesDict['d1pi016_lefthemi'],stimHemi='left')
site1.add_session('15-52-27', None, sessionTypes['nb'])
site1.add_session('15-55-03', 'a', sessionTypes['tc'])
site1.add_session('16-01-36', 'b', sessionTypes['tc'])
site1.add_session('16-06-21', None, sessionTypes['lp']) #left hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=1)
site1.add_clusters(clusterDict = {4:[2,6],5:[4,6,7,8,10]})
site1.daily_report(mainTCind=1, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-09', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2260, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
site1.add_session('15-34-32', None, sessionTypes['nb'])
site1.add_session('15-37-22', 'a', sessionTypes['tc'])
site1.add_session('15-44-24', 'b', sessionTypes['tc'])
site1.add_session('15-47-50', None, sessionTypes['lp']) #left hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {5:[4,6,7,9,12]})
site1.daily_report(mainTCind=2, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-10', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2340, tetrodes=tetrodesDict['d1pi016_righthemi'], stimHemi='right')
site1.add_session('13-41-12', None, sessionTypes['nb'])
site1.add_session('13-43-26', 'a', sessionTypes['tc'])
site1.add_session('13-49-27', 'b', sessionTypes['tc'])
site1.add_session('13-53-34', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {1:[4,6],2:[2,3]})
site1.daily_report(mainTCind=2, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-11', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2340, tetrodes=tetrodesDict['d1pi016_righthemi'], stimHemi='right')
site1.add_session('15-12-08', None, sessionTypes['nb'])
site1.add_session('15-23-31', 'a', sessionTypes['tc'])
site1.add_session('15-27-36', 'b', sessionTypes['tc'])
site1.add_session('15-31-40', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {1:[4,5],2:[2,3],8:[4]})
site1.daily_report(mainTCind=2, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-12', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2340, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
site1.add_session('16-58-16', None, sessionTypes['nb'])
site1.add_session('17-06-26', 'b', sessionTypes['tc'])
site1.add_session('17-10-41', 'c', sessionTypes['tc'])
site1.add_session('17-14-25', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=1)
site1.add_clusters(clusterDict = {4:[1],5:[3,8]})
site1.daily_report(mainTCind=1, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-13', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2260, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
site1.add_session('16-05-25', None, sessionTypes['nb'])
site1.add_session('16-07-52', 'a', sessionTypes['tc'])
site1.add_session('16-15-26', 'b', sessionTypes['tc'])
site1.add_session('16-19-25', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {3:[2,5,7],5:[4,6,10,11,12]})
site1.daily_report(mainTCind=2, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-16', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2340, tetrodes=[3,4,5,6], stimHemi='left') 
site1.add_session('16-42-10', None, sessionTypes['nb'])
site1.add_session('17-04-42', 'c', sessionTypes['tc'])
site1.add_session('17-08-40', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,2],mainTCind=1)
site1.add_clusters(clusterDict = {4:[1],5:[2,3]})
site1.daily_report(mainTCind=1, main2afcind=3)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-17', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2420, tetrodes=tetrodesDict['d1pi016_righthemi'], stimHemi='right')
site1.add_session('16-04-20', 'a', sessionTypes['tc'])
site1.add_session('16-11-24', None, sessionTypes['nb'])
site1.add_session('16-15-04', 'b', sessionTypes['tc'])
site1.add_session('16-20-42', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[1,3],mainTCind=2)
site1.add_clusters(clusterDict = {1:[5,6],7:[3,4]})
site1.daily_report(mainTCind=2, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-18', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2420, tetrodes=tetrodesDict['d1pi016_righthemi'], stimHemi='right')
site1.add_session('16-53-40', None, sessionTypes['nb'])
site1.add_session('16-56-24', 'a', sessionTypes['tc'])
site1.add_session('17-08-22', 'c', sessionTypes['tc'])
site1.add_session('17-12-09', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=1)
site1.add_clusters(clusterDict = {1:[2,3,5,6],7:[5],8:[2]})
site1.daily_report(mainTCind=1, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-19', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2420, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
site1.add_session('13-46-19', None, sessionTypes['nb'])
site1.add_session('13-48-30', 'a', sessionTypes['tc'])
site1.add_session('13-54-51', 'b', sessionTypes['tc'])
site1.add_session('14-04-25', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=1)
site1.add_clusters(clusterDict = {3:[5],4:[12],5:[4,6,10,11]})
site1.daily_report(mainTCind=1, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-22', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2420, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
site1.add_session('12-59-42', None, sessionTypes['nb'])
site1.add_session('13-20-53', 'c', sessionTypes['tc'])
site1.add_session('13-33-03', None, sessionTypes['lp']) #right hemi
site1.add_session('13-35-18', 'e', sessionTypes['tc'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,2],mainTCind=1)
site1.add_clusters(clusterDict = {4:[2,5,6,7,10],5:[3]})
site1.daily_report(mainTCind=1, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-23', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2540, tetrodes=tetrodesDict['d1pi016_righthemi'], stimHemi='right')
site1.add_session('14-48-54', None, sessionTypes['nb'])
site1.add_session('14-52-05', 'a', sessionTypes['tc'])
site1.add_session('15-03-46', 'c', sessionTypes['tc'])
site1.add_session('15-07-30', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {1:[2,4,5,7],7:[5]})
site1.daily_report(mainTCind=2, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-24', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2540, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
site1.add_session('15-01-17', None, sessionTypes['nb'])
site1.add_session('15-12-06', 'a', sessionTypes['tc'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0],mainTCind=1)
site1.add_clusters(clusterDict = {5:[3],6:[4,6,8]})
site1.daily_report(mainTCind=1, main2afcind=2)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-25', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2620, tetrodes=tetrodesDict['d1pi016_righthemi'], stimHemi='right')
site1.add_session('14-20-10', None, sessionTypes['nb'])
site1.add_session('14-22-15', 'a', sessionTypes['tc'])
site1.add_session('14-31-42', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,2],mainTCind=1)
site1.add_clusters(clusterDict = {7:[3,7],8:[2,3,5,7,8,10]})
site1.daily_report(mainTCind=1, main2afcind=3)


# -- D1pi015 -- #

exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-05', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2180, tetrodes=tetrodesDict['d1pi015_righthemi'], stimHemi='right')
site1.add_session('12-26-37', None, sessionTypes['nb'])
site1.add_session('12-29-14', 'a', sessionTypes['tc'])
site1.add_session('12-39-39', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0],mainTCind=1)
site1.add_clusters(clusterDict = {5:[2,3,8],6:[4],7:[3,5,6,7,8],8:[5,6,7,8,10,12]})
site1.daily_report(mainTCind=1, main2afcind=3)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-07', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2180, tetrodes=tetrodesDict['d1pi015_righthemi'],stimHemi='right')
site1.add_session('16-45-43', None, sessionTypes['nb'])
site1.add_session('16-48-07', 'a', sessionTypes['tc'])
site1.add_session('16-58-03', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,2],mainTCind=1)
site1.add_clusters(clusterDict = {5:[3,5],6:[7,8],7:[5,6,7,8,9,11],8:[3,4,5,7,10]})
site1.daily_report(mainTCind=1, main2afcind=3)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-15', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2180, tetrodes=tetrodesDict['d1pi015_righthemi'],stimHemi='right')
site1.add_session('13-06-44', None, sessionTypes['nb'])
site1.add_session('13-08-29', 'a', sessionTypes['tc'])
site1.add_session('13-17-45', 'b', sessionTypes['tc'])
site1.add_session('13-22-10', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=1)
site1.add_clusters(clusterDict = {7:[2,3,4,5,9,10,11],8:[2,4,6,7,8]})
site1.daily_report(mainTCind=1, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-16', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2260, tetrodes=tetrodesDict['d1pi015_lefthemi'],stimHemi='left')
site1.add_session('14-52-25', None, sessionTypes['nb'])
site1.add_session('14-54-50', 'a', sessionTypes['tc'])
site1.add_session('15-01-41', 'b', sessionTypes['tc'])
site1.add_session('15-07-03', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {1:[5],3:[6]})
site1.daily_report(mainTCind=2, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-17', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2260, tetrodes=[6,7,8],stimHemi='right') #for some reason T5 has no spikes in all sessions
site1.add_session('14-06-20', None, sessionTypes['nb'])
site1.add_session('14-08-39', 'a', sessionTypes['tc'])
site1.add_session('14-14-36', 'b', sessionTypes['tc'])
site1.add_session('14-19-21', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {7:[2,3,5,6,11,12],8:[2,3,7]})
site1.daily_report(mainTCind=2, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-19', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2340, tetrodes=tetrodesDict['d1pi015_righthemi'],stimHemi='right')
site1.add_session('11-23-32', 'a', sessionTypes['tc'])
site1.add_session('11-30-59', None, sessionTypes['nb'])
site1.add_session('11-37-08', 'b', sessionTypes['tc'])
site1.add_session('11-41-45', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[1,3],mainTCind=2)
site1.add_clusters(clusterDict = {7:[2,3,4,5,6,7,9,10,12]})
site1.daily_report(mainTCind=2, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-22', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2340, tetrodes=tetrodesDict['d1pi015_righthemi'],stimHemi='right')
site1.add_session('17-26-43', None, sessionTypes['nb'])
site1.add_session('17-28-45', 'a', sessionTypes['tc'])
site1.add_session('17-35-26', 'b', sessionTypes['tc'])
site1.add_session('17-39-04', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {6:[2,5],7:[2,3,4,5,6,8,9,10,12]})
site1.daily_report(mainTCind=2, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-23', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2340, tetrodes=tetrodesDict['d1pi015_righthemi'],stimHemi='right')
site1.add_session('16-46-24', None, sessionTypes['nb'])
site1.add_session('16-48-33', 'a', sessionTypes['tc'])
site1.add_session('17-09-54', 'b', sessionTypes['tc'])
site1.add_session('17-13-28', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {6:[4,6],7:[3,6,8,10]})
site1.daily_report(mainTCind=2, main2afcind=4)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-24', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2420, tetrodes=tetrodesDict['d1pi015_lefthemi'],stimHemi='left')
site1.add_session('16-45-11', None, sessionTypes['nb'])
site1.add_session('16-48-54', 'a', sessionTypes['tc'])
site1.add_session('16-58-53', 'b', sessionTypes['tc'])
site1.add_session('17-04-06', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {1:[5,7,10],2:[4,5],4:[5]})
site1.daily_report(mainTCind=2, main2afcind=4)
'''

exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-25', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2420, tetrodes=tetrodesDict['d1pi015_lefthemi'],stimHemi='left')
site1.add_session('15-52-34', None, sessionTypes['nb'])
site1.add_session('15-55-46', 'a', sessionTypes['tc'])
site1.add_session('16-06-29', 'b', sessionTypes['tc'])
site1.add_session('16-10-18', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {1:[2,3],2:[2],4:[2]})
site1.daily_report(mainTCind=2, main2afcind=4)
