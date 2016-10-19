#from jaratest.nick.database import cellDB
#reload(cellDB)
from jaratest.lan.Ephys import sitefuncs_vlan as sitefuncs
reload(sitefuncs)
from jaratest.lan.analysis_photostim import photostim_ephys_behav_container as photostim
reload(photostim)
import pandas as pd

sessionTypes = {'nb':'noiseBurst',
                'lp':'laserPulse',
                'lt':'laserTrain',
                'tc':'tuningCurve',
                'bf':'bestFreq',
                '3p':'3mWpulse',
                '1p':'1mWpulse',
                '2afc':'2afc'}


##### Mapping tetrodes to hemisphere in each mice ######
tetrodesDict={'d1pi015_righthemi':[5,6,7,8], 'd1pi015_lefthemi':[1,2,3,4], 'd1pi016_righthemi':[1,2,7,8], 'd1pi016_lefthemi':[3,4,5,6], 'd1pi014_righthemi':[5,6,7,8], 'd1pi014_lefthemi':[1,2,3,4]}
########################################################
siteList = []

# -- D1pi014 -- #
session = photostim.PhotostimSession(animalName='d1pi014', date ='2016-09-30', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2100, tetrodes=tetrodesDict['d1pi014_lefthemi'], stimHemi='left')
site1.add_session('14-56-37', None, sessionTypes['nb'])
site1.add_session('14-58-48', 'b', sessionTypes['tc'])
site1.add_session('15-05-30', None, sessionTypes['lp'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,2],mainTCind=1)
site1.add_clusters(clusterDict = {1:[4,6,7],4:[3,4,7,8]})
#site1.daily_report(mainTCind=1, main2afcind=3)
siteList.append(site1)

session = photostim.PhotostimSession(animalName='d1pi014', date ='2016-10-02', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2140, tetrodes=tetrodesDict['d1pi014_righthemi'], stimHemi='right')
site1.add_session('16-05-52', None, sessionTypes['nb'])
site1.add_session('16-09-18', 'a', sessionTypes['tc'])
site1.add_session('16-17-00', 'b', sessionTypes['tc'])
site1.add_session('16-24-02', 'c', sessionTypes['tc'])
site1.add_session('16-26-33', None, sessionTypes['lp'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,4],mainTCind=1)
site1.add_clusters(clusterDict = {5:[2,3,5],6:[2,9,10,11,12],8:[6,8,9,10]})
#site1.daily_report(mainTCind=1, main2afcind=5)
siteList.append(site1)


session = photostim.PhotostimSession(animalName='d1pi014', date ='2016-10-03', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2140, tetrodes=tetrodesDict['d1pi014_lefthemi'], stimHemi='left')
site1.add_session('15-54-33', None, sessionTypes['nb'])
site1.add_session('15-57-04', 'a', sessionTypes['tc'])
site1.add_session('16-03-44', 'b', sessionTypes['tc'])
site1.add_session('16-06-37', None, sessionTypes['lp'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=1)
site1.add_clusters(clusterDict = {3:[2,3,6],4:[4,5]})
#site1.daily_report(mainTCind=1, main2afcind=4)
siteList.append(site1)


session = photostim.PhotostimSession(animalName='d1pi014', date ='2016-10-04', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2180, tetrodes=tetrodesDict['d1pi014_righthemi'], stimHemi='right')
site1.add_session('13-02-45', None, sessionTypes['nb'])
site1.add_session('13-04-50', 'a', sessionTypes['tc'])
site1.add_session('13-12-16', 'b', sessionTypes['tc'])
site1.add_session('13-15-53', None, sessionTypes['lp'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=1)
site1.add_clusters(clusterDict = {5:[2,4,6,8],6:[2,4,5,6,7,8,11,12]})
#site1.daily_report(mainTCind=1, main2afcind=4)
siteList.append(site1)

session = photostim.PhotostimSession(animalName='d1pi014', date ='2016-10-06', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2180, tetrodes=tetrodesDict['d1pi014_righthemi'], stimHemi='right')
site1.add_session('13-12-58', None, sessionTypes['nb'])
site1.add_session('13-15-31', 'a', sessionTypes['tc'])
site1.add_session('13-22-01', 'b', sessionTypes['tc'])
site1.add_session('13-27-03', None, sessionTypes['lp'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=1)
site1.add_clusters(clusterDict = {5:[2,3,5,8],6:[4,6,7]})
#site1.daily_report(mainTCind=1, main2afcind=4)
siteList.append(site1)

session = photostim.PhotostimSession(animalName='d1pi014', date ='2016-10-07', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2180, tetrodes=tetrodesDict['d1pi014_lefthemi'], stimHemi='left')
site1.add_session('13-38-29', None, sessionTypes['nb'])
site1.add_session('13-40-55', 'a', sessionTypes['tc'])
#site1.add_session('', None, sessionTypes['lp'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0],mainTCind=1)
site1.add_clusters(clusterDict = {4:[2,3,5]})
#site1.daily_report(mainTCind=1, main2afcind=2)
siteList.append(site1)

session = photostim.PhotostimSession(animalName='d1pi014', date ='2016-10-08', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2220, tetrodes=tetrodesDict['d1pi014_righthemi'], stimHemi='right')
site1.add_session('16-47-33', None, sessionTypes['nb'])
site1.add_session('16-50-02', 'a', sessionTypes['tc'])
site1.add_session('16-59-37', 'b', sessionTypes['tc'])
site1.add_session('17-05-56', 'c', sessionTypes['tc'])
site1.add_session('17-09-10', None, sessionTypes['lp'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,4],mainTCind=1)
site1.add_clusters(clusterDict = {6:[5,6,8,9,11,12],8:[2,4,6]})
#site1.daily_report(mainTCind=1, main2afcind=5)
siteList.append(site1)

session = photostim.PhotostimSession(animalName='d1pi014', date ='2016-10-10', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2220, tetrodes=tetrodesDict['d1pi014_lefthemi'], stimHemi='left')
site1.add_session('12-22-52', None, sessionTypes['nb'])
site1.add_session('12-25-09', 'a', sessionTypes['tc'])
site1.add_session('12-31-38', 'b', sessionTypes['tc'])
site1.add_session('12-34-42', None, sessionTypes['lp'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=1)
site1.add_clusters(clusterDict = {4:[3]})
#site1.daily_report(mainTCind=1, main2afcind=4)
siteList.append(site1)

session = photostim.PhotostimSession(animalName='d1pi014', date ='2016-10-11', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2260, tetrodes=tetrodesDict['d1pi014_righthemi'], stimHemi='right')
site1.add_session('13-24-03', None, sessionTypes['nb'])
site1.add_session('13-26-23', 'a', sessionTypes['tc'])
site1.add_session('13-34-50', 'b', sessionTypes['tc'])
site1.add_session('13-40-28', None, sessionTypes['lp'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {5:[4,6,7,10],6:[2,4,6,7,12],8:[4,5,7,8]})
site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)

session = photostim.PhotostimSession(animalName='d1pi014', date ='2016-10-12', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2260, tetrodes=tetrodesDict['d1pi014_righthemi'], stimHemi='right')
site1.add_session('14-21-31', None, sessionTypes['nb'])
site1.add_session('14-24-14', 'a', sessionTypes['tc'])
site1.add_session('14-31-43', 'b', sessionTypes['tc'])
site1.add_session('14-37-09', None, sessionTypes['lp'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
#site1.add_clusters(clusterDict = {5:[4,6,7,10],6:[2,4,6,7,12],8:[4,5,7,8]})
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)


session = photostim.PhotostimSession(animalName='d1pi014', date ='2016-10-13', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2260, tetrodes=tetrodesDict['d1pi014_lefthemi'], stimHemi='left')
site1.add_session('13-29-52', None, sessionTypes['nb'])
site1.add_session('13-32-14', 'a', sessionTypes['tc'])
site1.add_session('13-51-23', None, sessionTypes['lp'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,2],mainTCind=1)
#site1.add_clusters(clusterDict = {5:[4,6,7,10],6:[2,4,6,7,12],8:[4,5,7,8]})
#site1.daily_report(mainTCind=1, main2afcind=3)
siteList.append(site1)


session = photostim.PhotostimSession(animalName='d1pi014', date ='2016-10-17', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2260, tetrodes=tetrodesDict['d1pi014_righthemi'], stimHemi='right')
site1.add_session('15-19-40', None, sessionTypes['nb'])
site1.add_session('15-22-03', 'a', sessionTypes['tc'])
site1.add_session('15-30-55', 'b', sessionTypes['tc'])
site1.add_session('15-35-41', None, sessionTypes['lp'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=1)
#site1.add_clusters(clusterDict = {5:[4,6,7,10],6:[2,4,6,7,12],8:[4,5,7,8]})
#site1.daily_report(mainTCind=1, main2afcind=4)
siteList.append(site1)


# -- D1pi016 -- #
session = photostim.PhotostimSession(animalName='d1pi016', date ='2016-07-29', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2100, tetrodes=tetrodesDict['d1pi016_righthemi'], stimHemi='right')
site1.add_session('13-36-13', None, sessionTypes['nb'])
site1.add_session('13-44-18', 'a', sessionTypes['tc'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0],mainTCind=1)
site1.add_clusters(clusterDict = {1:[1],2:[3,4,8],7:[6,12],8:[8]})
#site1.daily_report(mainTCind=1, main2afcind=2)
siteList.append(site1)

session = photostim.PhotostimSession(animalName='d1pi016', date ='2016-07-30', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2100, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
site1.add_session('12-44-24', None, sessionTypes['nb'])
site1.add_session('12-48-38', None, sessionTypes['lp'])
site1.add_session('12-58-22', 'a', sessionTypes['tc'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,1],mainTCind=2)
#site1.add_clusters(clusterDict = {4:[3,7],5:[8,10]})
#site1.daily_report(mainTCind=2, main2afcind=3)
siteList.append(site1)


session = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-01', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2100, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
site1.add_session('13-44-05', None, sessionTypes['nb'])
site1.add_session('13-51-14', 'a', sessionTypes['tc'])
site1.add_session('13-58-16', 'b', sessionTypes['tc'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0],mainTCind=1)
site1.add_clusters(clusterDict = {4:[3,7],5:[8,10]})
#site1.daily_report(mainTCind=1, main2afcind=3)
siteList.append(site1)

session = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-02', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = session.add_site(depth=2100, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
site1.add_session('14-26-07', None, sessionTypes['nb'])
site1.add_session('14-29-07', 'a', sessionTypes['tc'])
#site1.add_session('16-07-25', None, sessionTypes['lp']) #left hemi #ISI<0 at transition
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0],mainTCind=1)
site1.add_clusters(clusterDict = {4:[2,5],5:[2,4]})
#site1.daily_report(mainTCind=1, main2afcind=2)
siteList.append(site1)

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
#site1.daily_report(mainTCind=2, main2afcind=3)
siteList.append(site1)

exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-04', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2180, tetrodes=tetrodesDict['d1pi016_righthemi'], stimHemi='right')
site1.add_session('16-15-43', 'd', sessionTypes['tc'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=None,mainTCind=0)
site1.add_clusters(clusterDict = {2:[2],7:[4]})
#site1.daily_report(mainTCind=0, main2afcind=1)
siteList.append(site1)

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
#site1.daily_report(mainTCind=1, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=1, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=1, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=1, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)

exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-16', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2340, tetrodes=[3,4,5,6], stimHemi='left') 
site1.add_session('16-42-10', None, sessionTypes['nb'])
site1.add_session('17-04-42', 'c', sessionTypes['tc'])
site1.add_session('17-08-40', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,2],mainTCind=1)
site1.add_clusters(clusterDict = {4:[1],5:[2,3]})
#site1.daily_report(mainTCind=1, main2afcind=3)
siteList.append(site1)

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
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=1, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=1, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=1, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)

exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-24', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2540, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
site1.add_session('15-01-17', None, sessionTypes['nb'])
site1.add_session('15-12-06', 'a', sessionTypes['tc'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0],mainTCind=1)
site1.add_clusters(clusterDict = {5:[3],6:[4,6,8]})
#site1.daily_report(mainTCind=1, main2afcind=2)
siteList.append(site1)

exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-25', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2620, tetrodes=tetrodesDict['d1pi016_righthemi'], stimHemi='right')
site1.add_session('14-20-10', None, sessionTypes['nb'])
site1.add_session('14-22-15', 'a', sessionTypes['tc'])
site1.add_session('14-31-42', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,2],mainTCind=1)
site1.add_clusters(clusterDict = {7:[3,7],8:[2,3,5,7,8,10]})
#site1.daily_report(mainTCind=1, main2afcind=3)
siteList.append(site1)

exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-26', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2580, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
site1.add_session('13-36-20', None, sessionTypes['nb'])
site1.add_session('13-39-06', 'a', sessionTypes['tc'])
site1.add_session('13-45-53', 'b', sessionTypes['tc'])
site1.add_session('13-49-19', None, sessionTypes['lp'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {4:[3,4,5,7,8,9],5:[5,6],6:[2,5,6,7,9,12]})
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-29', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2660, tetrodes=tetrodesDict['d1pi016_righthemi'], stimHemi='right')
site1.add_session('17-17-17', None, sessionTypes['nb'])
site1.add_session('17-20-23', 'a', sessionTypes['tc'])
site1.add_session('17-28-57', 'b', sessionTypes['tc'])
site1.add_session('17-34-50', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {7:[2,5,10,12],8:[7,9]})
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-08-31', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2580, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
site1.add_session('16-04-11', None, sessionTypes['nb'])
site1.add_session('16-07-41', 'a', sessionTypes['tc'])
site1.add_session('16-28-18', None, sessionTypes['lp'])
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,2],mainTCind=1)
site1.add_clusters(clusterDict = {4:[5,6,7,8],5:[3,4,8,9],6:[9]})
#site1.daily_report(mainTCind=1, main2afcind=3)
siteList.append(site1)


exp = photostim.PhotostimSession(animalName='d1pi016', date ='2016-09-02', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2660, tetrodes=tetrodesDict['d1pi016_righthemi'], stimHemi='right')
site1.add_session('12-30-07', None, sessionTypes['nb'])
site1.add_session('12-33-29', 'a', sessionTypes['tc'])
site1.add_session('12-41-27', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,2],mainTCind=1)
site1.add_clusters(clusterDict = {7:[2,4,6,12]})
#site1.daily_report(mainTCind=1, main2afcind=3)
siteList.append(site1)



###################################################################################
# -- D1pi015 -- #
exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-03', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2100, tetrodes=tetrodesDict['d1pi015_righthemi'], stimHemi='right')
site1.add_session('12-25-11', None, sessionTypes['nb'])
site1.add_session('12-28-05', 'a', sessionTypes['tc'])
site1.add_session('12-38-02', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0],mainTCind=1)
site1.add_clusters(clusterDict = {6:[2,3,4,5,6],7:[2,3,4,5,6,7,8,9,10,11,12],8:[2,3,4,5,6,7,8,9,10]})
#site1.daily_report(mainTCind=1, main2afcind=3)
siteList.append(site1)

exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-04', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2100, tetrodes=tetrodesDict['d1pi015_lefthemi'], stimHemi='left')
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
#very few spikes no tuning, did not cluster recordings
siteList.append(site1)

exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-05', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2180, tetrodes=tetrodesDict['d1pi015_righthemi'], stimHemi='right')
site1.add_session('12-26-37', None, sessionTypes['nb'])
site1.add_session('12-29-14', 'a', sessionTypes['tc'])
site1.add_session('12-39-39', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0],mainTCind=1)
site1.add_clusters(clusterDict = {5:[2,3,8],6:[4],7:[3,5,6,7,8],8:[5,6,7,8,10,12]})
#site1.daily_report(mainTCind=1, main2afcind=3)
siteList.append(site1)

exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-07', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2180, tetrodes=tetrodesDict['d1pi015_righthemi'],stimHemi='right')
site1.add_session('16-45-43', None, sessionTypes['nb'])
site1.add_session('16-48-07', 'a', sessionTypes['tc'])
site1.add_session('16-58-03', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,2],mainTCind=1)
site1.add_clusters(clusterDict = {5:[3,5],6:[7,8],7:[5,6,7,8,9,11],8:[3,4,5,7,10]})
#site1.daily_report(mainTCind=1, main2afcind=3)
siteList.append(site1)

exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-09', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2180, tetrodes=tetrodesDict['d1pi015_righthemi'],stimHemi='right')
site1.add_session('13-52-58', None, sessionTypes['nb'])
site1.add_session('13-55-29', 'a', sessionTypes['tc'])
site1.add_session('14-04-54', 'b', sessionTypes['tc'])
site1.add_session('14-09-09', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
#site1.add_clusters(clusterDict = {5:[3,5],6:[7,8],7:[5,6,7,8,9,11],8:[3,4,5,7,10]})
#site1.daily_report(mainTCind=2, main2afcind=3)
siteList.append(site1)

exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-10', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2180, tetrodes=tetrodesDict['d1pi015_lefthemi'], stimHemi='left')
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
#very few spikes no tuning, did not cluster recordings
siteList.append(site1)

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
#site1.daily_report(mainTCind=1, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)

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
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)

exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-26', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2420, tetrodes=tetrodesDict['d1pi015_righthemi'],stimHemi='right')
site1.add_session('15-30-27', None, sessionTypes['nb'])
site1.add_session('15-32-47', 'a', sessionTypes['tc'])
site1.add_session('15-39-59', 'b', sessionTypes['tc'])
site1.add_session('15-48-24', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {6:[2,3,5],7:[2,3,4,6,7,8,9,10,11,12],8:[2,3,5,7]})
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-29', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2420, tetrodes=tetrodesDict['d1pi015_lefthemi'],stimHemi='left')
site1.add_session('15-52-09', None, sessionTypes['nb'])
site1.add_session('15-54-35', 'a', sessionTypes['tc'])
site1.add_session('16-03-05', 'b', sessionTypes['tc'])
site1.add_session('16-06-20', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {1:[4,10],2:[2]})
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-30', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2420, tetrodes=tetrodesDict['d1pi015_righthemi'],stimHemi='right')
site1.add_session('15-13-06', None, sessionTypes['nb'])
site1.add_session('15-14-42', 'a', sessionTypes['tc'])
site1.add_session('15-21-25', 'b', sessionTypes['tc'])
site1.add_session('15-26-01', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {7:[3,6,7,9,10]})
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-08-31', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2420, tetrodes=tetrodesDict['d1pi015_lefthemi'],stimHemi='left')
site1.add_session('14-33-56', None, sessionTypes['nb'])
site1.add_session('14-36-26', 'a', sessionTypes['tc'])
site1.add_session('14-42-11', 'b', sessionTypes['tc'])
site1.add_session('14-49-49', None, sessionTypes['lp']) 
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=1)
site1.add_clusters(clusterDict = {1:[3],2:[2,3,7]})
#site1.daily_report(mainTCind=1, main2afcind=4)
siteList.append(site1)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-09-01', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2420, tetrodes=tetrodesDict['d1pi015_righthemi'],stimHemi='right')
site1.add_session('17-13-25', None, sessionTypes['nb'])
site1.add_session('17-15-49', 'a', sessionTypes['tc'])
site1.add_session('17-24-25', 'b', sessionTypes['tc'])
site1.add_session('17-27-32', None, sessionTypes['lp']) #right hemi
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {7:[3,4,6,7,8,9,11]})
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-09-02', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2460, tetrodes=tetrodesDict['d1pi015_lefthemi'],stimHemi='left')
site1.add_session('15-32-38', None, sessionTypes['nb'])
site1.add_session('15-35-22', 'a', sessionTypes['tc'])
site1.add_session('15-44-10', 'b', sessionTypes['tc'])
site1.add_session('15-47-27', None, sessionTypes['lp']) 
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {1:[4,5],4:[2,3,4,5]})
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-09-03', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2460, tetrodes=tetrodesDict['d1pi015_righthemi'],stimHemi='right')
site1.add_session('18-26-20', None, sessionTypes['nb'])
site1.add_session('18-28-33', 'a', sessionTypes['tc'])
site1.add_session('18-36-08', 'b', sessionTypes['tc'])
site1.add_session('18-39-58', None, sessionTypes['lp']) 
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {7:[5,6]})
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-09-06', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2500, tetrodes=tetrodesDict['d1pi015_lefthemi'],stimHemi='left')
site1.add_session('15-54-52', None, sessionTypes['nb'])
site1.add_session('15-57-49', 'a', sessionTypes['tc'])
site1.add_session('16-04-16', 'b', sessionTypes['tc'])
site1.add_session('16-08-27', None, sessionTypes['lp']) 
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {1:[2,3,5],3:[8]})
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-09-07', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2500, tetrodes=tetrodesDict['d1pi015_righthemi'],stimHemi='right')
site1.add_session('14-41-55', None, sessionTypes['nb'])
site1.add_session('14-44-03', 'a', sessionTypes['tc'])
site1.add_session('14-50-43', 'b', sessionTypes['tc'])
site1.add_session('14-56-20', None, sessionTypes['lp']) 
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {7:[2,3,4,9],8:[2]})
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-09-09', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2540, tetrodes=tetrodesDict['d1pi015_lefthemi'],stimHemi='left')
site1.add_session('14-35-57', None, sessionTypes['nb'])
site1.add_session('14-38-51', 'a', sessionTypes['tc'])
site1.add_session('14-45-24', 'b', sessionTypes['tc'])
site1.add_session('14-54-45', None, sessionTypes['lp']) 
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {1:[3,7],2:[5,6,7,10],4:[3,5,6,7]})
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)


exp = photostim.PhotostimSession(animalName='d1pi015', date ='2016-09-12', experimenter='', defaultParadigm='laser_tuning_curve')
site1 = exp.add_site(depth=2540, tetrodes=tetrodesDict['d1pi015_righthemi'],stimHemi='right')
site1.add_session('16-15-36', None, sessionTypes['nb'])
site1.add_session('16-18-31', 'a', sessionTypes['tc'])
site1.add_session('16-24-29', 'b', sessionTypes['tc'])
site1.add_session('16-29-32', None, sessionTypes['lp']) 
site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
site1.cluster_photostim_session() 
site1.raster_reports_all_clusters(mainRasterInds=[0,3],mainTCind=2)
site1.add_clusters(clusterDict = {7:[4,10]})
#site1.daily_report(mainTCind=2, main2afcind=4)
siteList.append(site1)


'''
from jaratest.lan.analysis_photostim import plot_psycurve_by_tuning as plotter
reload(plotter)
import matplotlib.pyplot as plt
tuningFilename = '/home/languo/data/behavior_reports/photostim_response_freq_summary.csv' 

plotter.plot_best_freq_n_tuning_range_all_sites(siteList, tuningFilename=tuningFilename)
plt.show()

plotter.plot_psycurve_by_cond_n_tuning(siteList, tuningFilename=tuningFilename, aggregateFunc='mean',byHemi=True)
plt.show()

plotter.plot_psycurve_by_cond_n_tuning(siteList, tuningFilename=tuningFilename, aggregateFunc='median',byHemi=True)
plt.show()


####################### Summary Plots ##############################################
# -- ave performance for high and low freq under dif stim conditions -- #
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#avePercentCorrectByTypeByFreq = pd.DataFrame(columns=['freq_label','stim_type','ave_percent_correct_baseline','ave_percent_correct_stim'])
#percentCorrectEachFreqEachCond = pd.DataFrame()
avePercentRightwardByTypeByFreq = pd.DataFrame()
tuningDf = pd.read_csv('/home/languo/data/behavior_reports/photostim_response_freq_summary.csv')

plt.style.use(['seaborn-white', 'seaborn-talk']) 


for site in siteList:
    # -- ave performance for low vs high freqs in baseline vs stim -- #
    avePercentRightwardThisSite = site.calculate_ave_percent_rightward_lhfreqs_each_cond()
    avePercentRightwardByTypeByFreq=pd.concat([avePercentRightwardByTypeByFreq,avePercentRightwardThisSite], ignore_index=True)

    # -- change in performance as function of distance to best freq -- #
    #percentRightwardDfThisSite = site.calculate_percent_rightward_each_freq_each_cond()
    #tuningThisSite = tuningDf.loc[(tuningDf['animalName']==site.animalName)&(tuningDf['session']==site.date)]
    #if np.any(tuningThisSite):
    #    bestFreqThisSite = tuningThisSite['most_responsive_freq'].values
    #    log2distance = np.log2(1000*bestFreqThisSite)-np.log2(percentRightwardDfThisSite['freqs']) 
    #    percentPerfChange = percentRightwardDfThisSite.ix[:,1] - percentRightwardDfThisSite.ix[:,0] #stim minus baseline 

     #   plt.plot(log2distance, percentPerfChange, 'o-')
     #   plt.hold(True)
     #else:
         #continue

#plt.xlabel('Log2 distance to most responsive frequency\n photostim freq - sound freq')
#plt.ylabel('Change in % rightward choice\n Stimulation - Baseline')

#plt.show()

photostim.plot_ave_performance_lhfreqs_each_cond(avePercentRightwardByTypeByFreq)


# -- make a plot of all psycurves -- #
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#nPlots = len(siteList)
gs = gridspec.GridSpec(5,10,left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.5, hspace=0.3)
tuningDf = pd.read_csv('/home/languo/data/behavior_reports/photostim_response_freq_summary.csv')

# -- get tuned sites and responsive freqs, plot psychometric -- #
for ind,site in enumerate(siteList):
    ax=plt.subplot(gs[ind/10,ind%10])
    main2afcind = site.get_session_types().index('2afc')
    site.plot_photostim_psycurve(main2afcind)
    tuningThisSite = tuningDf.loc[(tuningDf['animalName']==site.animalName)&(tuningDf['session']==site.date)]
    if np.any(tuningThisSite):
        bestFreqThisSite = tuningThisSite['most_responsive_freq'].values
        tuningRangeThisSite = tuningThisSite['responsive_freqs'].values
        #pbd.set_trace()
        if ~np.isnan(bestFreqThisSite):
            plt.vlines(x=bestFreqThisSite,ymin=0,ymax=100,colors='red',linestyles='solid')
            plt.vlines(x=tuningRangeThisSite[0].split(',')[0],ymin=0,ymax=100,colors='grey',linestyles='dashed')
            try: 
                plt.vlines(x=tuningRangeThisSite[0].split(',')[1],ymin=0,ymax=100,colors='grey',linestyles='dashed')
            except:
                continue
        
        #plt.annotate('best freq: %skHz\n responsive range %skHz'%(bestFreqThisSite,tuningRangeThisSite), xy=(0.1,0.7), xycoords='axes fraction',fontsize=8)
        
#gs.tight_layout(plt.gcf(),h_pad=0.3,w_pad=0.4)


# -- Fit psy curves and plot curve params for all sites -- #
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from jaratest.lan import test053_photostim_ephys_behav_container as test053
reload(test053)

plt.style.use(['seaborn-white', 'seaborn-talk'])


curveParamDf = pd.DataFrame()
for ind,site in enumerate(siteList):
    curveParamDfThisSite = site.fit_psycuve()
    curveParamDf = pd.concat([curveParamDf,curveParamDfThisSite],ignore_index=True)
    
bias = curveParamDf.set_index(['animal','session','photostim']).unstack(level=-1)['bias']
slope = curveParamDf.set_index(['animal','session','photostim']).unstack(level=-1)['slope']
upper = curveParamDf.set_index(['animal','session','photostim']).unstack(level=-1)['upper']
lower = curveParamDf.set_index(['animal','session','photostim']).unstack(level=-1)['lower']

ax1 = plt.subplot2grid((4,2),(0,0))
maskLeft = np.isfinite(bias['laser_left'])
test053.paired_dot_plot_with_lines(bias['no_laser'][maskLeft],bias['laser_left'][maskLeft])
plt.ylabel('Frequency (kHz)')
plt.title('Bias: left hemisphere photostim')
plt.xticks([1,2],['Baseline','Photostim'])
ax2 = plt.subplot2grid((4,2),(0,1))
maskRight = np.isfinite(bias['laser_right'])
test053.paired_dot_plot_with_lines(bias['no_laser'][maskRight],bias['laser_right'][maskRight])
plt.ylabel('Frequency (kHz)')
plt.xticks([1,2],['Baseline','Photostim'])
plt.title('Bias: right hemisphere photostim')

ax3 = plt.subplot2grid((4,2),(1,0))
test053.paired_dot_plot_with_lines(slope['no_laser'][maskLeft],slope['laser_left'][maskLeft])
plt.ylabel('Slope')
plt.title('Slope: left hemisphere photostim')
plt.xticks([1,2],['Baseline','Photostim'])
ax4 = plt.subplot2grid((4,2),(1,1))
test053.paired_dot_plot_with_lines(slope['no_laser'][maskRight],slope['laser_right'][maskRight])
plt.ylabel('Slope')
plt.title('Slope: right hemisphere photostim')
plt.xticks([1,2],['Baseline','Photostim'])

ax5 = plt.subplot2grid((4,2),(2,0))
test053.paired_dot_plot_with_lines(upper['no_laser'][maskLeft],upper['laser_left'][maskLeft])
plt.ylabel('Upper asymptote\n(% rightward)')
plt.title('Upper asymptote: left hemisphere photostim')
plt.xticks([1,2],['Baseline','Photostim'])
ax6 = plt.subplot2grid((4,2),(2,1))
test053.paired_dot_plot_with_lines(upper['no_laser'][maskRight],upper['laser_right'][maskRight])
plt.ylabel('Upper asymptote\n(% rightward)')
plt.title('Upper asymptote: right hemisphere photostim')
plt.xticks([1,2],['Baseline','Photostim'])

ax7 = plt.subplot2grid((4,2),(3,0))
test053.paired_dot_plot_with_lines(lower['no_laser'][maskLeft],lower['laser_left'][maskLeft])
plt.ylabel('Lower asymptote\n(% rightward)')
plt.title('Lower: left hemisphere photostim')
plt.xticks([1,2],['Baseline','Photostim'])
ax8 = plt.subplot2grid((4,2),(3,1))
test053.paired_dot_plot_with_lines(lower['no_laser'][maskRight],lower['laser_right'][maskRight])
plt.ylabel('Lower asymptote\n(% rightward)')
plt.title('Lower: right hemisphere photostim')
plt.xticks([1,2],['Baseline','Photostim'])

#plt.subplots_adjust(top=0.85)
plt.suptitle('Psy curve params under baseline and photostim',fontsize=16)
plt.tight_layout()
plt.show()

'''
