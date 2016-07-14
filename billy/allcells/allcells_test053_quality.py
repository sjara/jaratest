'''
List of all isolated units from one animal

Quality rated by Billy (05-11 thru 05-13) and Phoebe (all sessions after 05-13).

oneES = eSession(animalName='ANIMAL_NAME', #THIS IS THE ANIMAL NAME
                 ephysSession = '2016-02-10_10-10-28', #THIS IS THE EPHYS SESSION NAME FOR THE TASK
                 tuningSession = '2016-02-10_09-57-50', #THIS IS THE EPHYS NAME FOR THE TUNING SESSION
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)}, #THIS SAYS WHICH TETRODES AND CLUSTERS TO LOOK AT
                 clusterQuality = {1:[]}, #THIS IS THE QUALITY OF EACH CLUSTER IN EACH TETRODE. LOOK AT WIKI PAGE "Report 2015-06-29: Numbering System of Cluster Quality"
                 depth = 2.39625, #THIS IS DEPTH (in mm) OF LONGEST TETRODE FOR THIS SITE. THE DIFFERENCE IN LENGTH OF TETRODES IS IN WIKI ANIMAL PAGE. 0mm IS THE BRAIN SURFACE AT IMPLANTING
                 tuningBehavior = '20160210a',#THIS IS THE NAME OF THE TUNING SESSION BEHAVIOR
                 behavSession = '20160210a') #THIS IS THE NAME OF THE TASK BEHAVIOR SESSION
cellDB.append_session(oneES) #ADD THIS SESSION TO THE LIST OF ALLCELLS
'''
from jaratoolbox import celldatabase_quality_tuning as celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

'''
#THE DAYS IN MAY WERE ON SWITCHING TASK
oneES = eSession(animalName='test053',
                 ephysSession = '2015-05-11_17-16-31',
                 tuningSession = '2015-05-11_17-06-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,3,3,1,6,3,1,1,3,2,1],2:[3,3,1,3,4,2,3,1,1,1,3,3],3:[3,3,3,3,3,2,1,3,3,3,3,2],4:[3,2,3,2,3,1,1,3,1,2,2,2],5:[3,2,1,3,3,1,2,1,2,2,2,3],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,1,1,2,2,1,2,2,1,2,0],8:[3,3,2,3,1,3,3,3,1,3,3,2]},
                 depth = 2.317,
                 tuningBehavior = '20150511a',
                 behavSession = '20150511a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-05-12_15-41-58',
                 tuningSession = '2015-05-12_15-32-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,1,1,3,1,1,1,1,3,1],2:[3,1,2,2,2,2,2,1,1,3,2,2],3:[3,3,1,2,3,3,3,3,3,3,1,3],4:[3,1,1,1,3,2,1,3,2,1,2,3],5:[3,1,1,3,2,3,2,3,1,2,3,2],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,1,2,3,1,2,1,1,2,2,0],8:[3,2,3,2,1,3,3,3,1,2,2,0]},
                 depth = 2.317,
                 tuningBehavior = '20150512a',
                 behavSession = '20150512a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-05-13_14-47-47',
                 tuningSession = '2015-05-13_14-37-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,1,1,1,3,3,1,3,1],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,2,3,2,2,2,2,2,1,2,3],4:[3,1,1,1,2,1,1,3,3,3,1,2],5:[3,3,1,2,2,2,3,2,2,2,2,3],6:[3,2,2,3,2,3,2,3,2,2,3,2],7:[3,1,3,1,1,3,2,1,1,1,1,0],8:[3,2,2,2,3,1,3,1,2,2,2,2]},
                 depth = 2.317,
                 tuningBehavior = '20150513a',
                 behavSession = '20150513a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-05-14_14-30-14',
                 tuningSession = '2015-05-14_14-19-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,3,1,1,1,2,2,1,2,1],2:[3,2,2,2,2,1,2,3,1,2,1,0],3:[3,2,1,2,2,2,3,2,1,3,2,0],4:[3,2,1,1,2,2,3,2,1,2,2,2],5:[3,4,1,2,2,2,1,2,2,2,1,2],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,1,1,4,1,1,2,2,2,1,0],8:[3,2,1,1,2,2,2,1,2,3,2,0]},
                 depth = 2.317,
                 tuningBehavior = '20150514a',
                 behavSession = '20150514a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-05-15_13-47-59',
                 tuningSession = '2015-05-15_13-37-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,1,2,2,3,1,1,1],2:[3,2,1,3,2,4,1,1,1,1,2,2],3:[3,3,2,1,2,2,5,3,1,2,1,2],4:[3,2,2,2,3,1,2,2,1,1,1,0],5:[3,2,2,1,2,3,2,2,2,2,3,2],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,2,1,2,1,2,3,1,1,1,0],8:[3,2,2,2,2,2,3,1,1,1,3,3]},
                 depth = 2.317,
                 tuningBehavior = '20150515a',
                 behavSession = '20150515a')
cellDB.append_session(oneES)
'''
'''
oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-10_14-44-24',
                 tuningSession = '2015-06-10_13-37-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 2.317,
                 tuningBehavior = '20150610a',
                 behavSession = '20150610a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-11_15-46-05',
                 tuningSession = '2015-06-11_15-25-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,6,1,1,1,2,3,1,1,1,1],2:[3,2,4,1,2,2,2,2,2,1,1,4],3:[3,1,2,4,2,5,2,2,1,1,1,0],4:[2,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,2,2,2,3,2,2,1,2,2,2],6:[3,1,2,2,2,2,2,1,2,2,3,1],7:[3,1,2,1,3,2,2,2,2,2,2,0],8:[3,2,1,2,2,2,1,2,3,2,2,2]},
                 depth = 2.317,
                 tuningBehavior = '20150611a',
                 behavSession = '20150611a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-12_18-29-46',
                 tuningSession = '2015-06-12_18-16-46',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,1,1,1,2,1,2,1],2:[3,2,1,2,4,2,1,1,3,2,2,1],3:[3,4,2,2,2,1,2,1,4,1,2,2],4:[2,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,2,1,4,2,2,5,2,2,3,2],6:[3,3,2,1,2,1,1,2,3,2,2,2],7:[3,6,1,4,2,2,2,1,2,3,2,1],8:[3,1,1,5,2,4,2,2,2,3,2,2]},
                 depth = 2.317,
                 tuningBehavior = '20150612a',
                 behavSession = '20150612a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-15_16-05-58',
                 tuningSession = '2015-06-15_15-40-34',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,1,1,1,1,1,2,2,1,0],2:[3,3,2,2,2,1,1,2,2,2,2,2],3:[3,5,1,2,1,2,4,2,2,2,1,2],4:[2,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,5,2,2,2,1,2,2,2,1,2],6:[3,2,3,2,2,2,1,2,3,1,1,2],7:[3,2,2,2,1,2,1,2,2,3,2,1],8:[3,2,2,2,2,2,1,2,2,1,2,2]},
                 depth = 2.317,
                 tuningBehavior = '20150615a',
                 behavSession = '20150615a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-17_10-40-01',
                 tuningSession = '2015-06-17_10-21-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,1,2,1,2,1,2,1,1,2],2:[3,2,5,2,2,1,3,1,2,2,2,1],3:[3,2,3,3,1,2,2,2,1,2,2,2],4:[2,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,3,2,2,5,2,2,2,2,2,0],6:[3,5,2,2,1,2,2,2,2,3,2,2],7:[3,2,1,2,2,2,2,2,2,1,1,2],8:[3,1,2,2,2,2,2,1,1,2,2,2]},
                 depth = 2.317,
                 tuningBehavior = '20150617a',
                 behavSession = '20150617a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-18_10-34-39',
                 tuningSession = '2015-06-18_10-10-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,1,1,2,2,1,1,2,2,0],2:[3,2,2,3,2,2,3,2,1,2,1,2],3:[3,2,2,2,2,2,2,3,2,5,1,0],4:[2,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,2,2,2,1,2,2,2,1,3,3],6:[3,2,1,2,2,3,2,2,2,1,2,2],7:[3,1,2,2,3,2,2,1,2,2,1,0],8:[3,1,2,2,1,2,2,2,3,1,2,2]},
                 depth = 2.317,
                 tuningBehavior = '20150618a',
                 behavSession = '20150618a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-19_10-33-57',
                 tuningSession = '2015-06-19_10-18-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,1,3,1,1,2,2,1,2,2],2:[3,2,2,2,1,2,1,2,1,1,2,3],3:[3,2,3,2,4,1,2,2,4,4,2,0],4:[2,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,2,2,2,2,2,2,2,3,2],6:[3,1,2,2,2,2,1,1,2,3,1,1],7:[3,1,2,2,1,2,2,3,1,2,2,1],8:[3,1,2,2,3,1,2,1,2,1,2,2]},
                 depth = 2.317,
                 tuningBehavior = '20150619a',
                 behavSession = '20150619a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-22_11-41-15',
                 tuningSession = '2015-06-22_11-24-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,2,2,1,1,1,3,3],2:[3,3,2,2,3,2,2,1,1,3,1,2],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,1,2,2,2,2,1,1,2,3,1,0],5:[3,2,4,3,1,2,1,2,2,2,2,2],6:[3,1,1,2,6,1,2,3,2,6,2,1],7:[3,3,1,1,6,1,2,2,2,2,1,3],8:[3,1,2,2,1,1,2,1,1,3,1,2]},
                 depth = 2.356625,
                 tuningBehavior = '20150622b',
                 behavSession = '20150622a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-25_11-42-24',
                 tuningSession = '2015-06-25_11-27-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,1,2,1,2,1,1,2,0],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,2,2,2,2,2,2,1,1,2,1],4:[3,2,1,1,2,2,1,2,1,2,2,0],5:[3,4,1,2,2,2,2,2,2,2,1,0],6:[3,2,1,1,2,2,2,1,2,2,1,2],7:[3,2,1,2,1,1,2,1,1,2,2,1],8:[3,1,2,1,1,2,1,2,2,6,2,5]},
                 depth = 2.356625,
                 tuningBehavior = '20150625a',
                 behavSession = '20150625a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-26_11-25-16',
                 tuningSession = '2015-06-26_11-02-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,1,2,1,2,1,2,1,0],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,1,2,2,1,3,2,2,2,1,2],4:[3,2,2,2,1,2,2,1,2,2,1,1],5:[3,2,2,2,1,2,1,2,1,2,2,0],6:[3,2,2,1,2,1,2,2,2,1,2,2],7:[3,1,1,1,1,1,2,2,2,2,2,0],8:[3,4,2,4,2,2,2,2,1,1,2,1]},
                 depth = 2.356625,
                 tuningBehavior = '20150626a',
                 behavSession = '20150626a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-29_11-30-24',
                 tuningSession = '2015-06-29_11-18-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,2,1,1,1,1,1,1,1],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,3,2,2,2,2,2,2,2,2],4:[3,2,1,1,2,2,2,2,1,6,2,3],5:[3,2,2,2,2,2,2,1,2,3,1,0],6:[3,1,1,1,2,1,2,1,2,1,1,3],7:[3,1,1,2,2,2,2,1,1,2,1,0],8:[3,1,1,2,1,1,2,2,1,1,1,1]},
                 depth = 2.39625,
                 tuningBehavior = '20150629a',
                 behavSession = '20150629a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-01_11-17-27',
                 tuningSession = '2015-07-01_11-03-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,2,1,1,1,1,3,1,1],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,1,2,2,2,2,3,2,1,2,2],4:[3,3,6,1,1,2,6,2,2,1,1,3],5:[3,1,1,1,5,2,2,3,2,2,1,2],6:[3,1,2,1,2,2,1,1,2,1,1,2],7:[3,1,1,1,2,2,2,2,1,2,1,0],8:[3,1,2,3,2,1,2,1,1,2,1,1]},
                 depth = 2.4755,
                 tuningBehavior = '20150701a',
                 behavSession = '20150701a')
cellDB.append_session(oneES)

'''
oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-02_12-12-03',
                 tuningSession = '2015-07-02_11-53-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 2.4755,
                 tuningBehavior = '20150702a',
                 behavSession = '20150702a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-03_16-50-19',
                 tuningSession = '2015-07-03_16-41-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,2,1,2,6,2,2,1,1,2,2],2:[3,2,2,2,2,1,2,2,2,2,2,1],3:[2,0,0,0,0,0,0,0,0,0,0,0],4:[3,1,4,2,1,1,1,1,2,1,1,2],5:[3,2,1,2,1,3,2,2,2,1,1,2],6:[3,5,1,1,3,1,1,1,2,2,3,2],7:[3,2,2,1,1,3,2,2,2,1,2,2],8:[3,2,1,1,2,2,1,2,1,1,2,1]},
                 depth = 2.4755,
                 tuningBehavior = '20150703a',
                 behavSession = '20150703a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-06_11-35-54',
                 tuningSession = '2015-07-06_11-21-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,3,2,2,1,1,2,4,2,1],2:[3,2,2,3,2,2,2,2,1,2,2,2],3:[2,0,0,0,0,0,0,0,0,0,0,0],4:[3,2,1,2,6,2,2,3,6,6,1,6],5:[3,2,2,2,2,3,1,1,2,2,2,0],6:[3,1,6,2,6,2,6,2,1,1,1,6],7:[3,1,1,1,2,2,1,3,2,2,1,1],8:[3,2,2,1,1,1,1,2,2,1,1,2]},
                 depth = 2.4755,
                 tuningBehavior = '20150706a',
                 behavSession = '20150706a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-07_17-21-43',
                 tuningSession = '2015-07-07_17-08-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,1,1,6,2,2,3,2,1],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,2,2,3,2,3,2,1,1,2,3],4:[3,3,3,2,6,6,6,6,2,3,2,0],5:[3,1,1,2,1,6,2,6,2,3,1,2],6:[3,2,1,6,1,1,1,2,1,1,3,2],7:[3,2,3,2,2,2,2,1,3,1,3,2],8:[3,1,1,1,2,1,2,3,2,2,1,1]},
                 depth = 2.515125,
                 tuningBehavior = '20150707a',
                 behavSession = '20150707a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-08_13-06-14',
                 tuningSession = '2015-07-08_12-49-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,3,2,1,2,2,2,1,1,2],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,2,2,2,2,2,3,2,2,3,0],4:[3,1,1,2,2,2,2,2,1,2,6,3],5:[3,1,6,1,6,3,6,2,2,1,1,2],6:[3,1,1,1,6,1,1,1,2,2,6,2],7:[3,3,3,2,1,1,1,2,1,2,2,1],8:[3,2,1,2,1,2,1,1,3,1,2,6]},
                 depth = 2.515125,
                 tuningBehavior = '20150708a',
                 behavSession = '20150708a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-09_17-02-43',
                 tuningSession = '2015-07-09_16-46-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,2,2,1,3,1,2,1,2],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,3,2,2,2,2,3,2,2,2,0],4:[3,1,1,2,1,6,6,3,2,2,2,0],5:[3,1,1,1,1,2,2,2,6,2,1,1],6:[3,1,6,1,2,2,1,1,3,2,1,6],7:[3,3,2,2,1,1,2,3,1,1,1,0],8:[3,1,2,1,2,1,2,3,1,1,1,2]},
                 depth = 2.515125,
                 tuningBehavior = '20150709a',
                 behavSession = '20150709a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-10_13-33-33',
                 tuningSession = '2015-07-10_13-17-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,2,2,1,1,1,3,1,1],2:[3,2,2,2,2,2,1,1,1,2,2,3],3:[3,2,1,2,2,1,2,3,2,3,2,0],4:[3,2,2,3,2,1,2,6,1,3,2,2],5:[3,2,1,3,1,2,2,2,6,1,4,1],6:[3,1,3,2,1,6,1,2,1,3,1,1],7:[2,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,3,2,1,2,1,1,1,2,1,3]},
                 depth = 2.515125,
                 tuningBehavior = '20150710a',
                 behavSession = '20150710a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-13_13-40-41',
                 tuningSession = '2015-07-13_13-25-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,2,1,1,2,1,1,1,1,2,1],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,2,2,3,2,2,2,2,1,3,2],4:[3,4,2,2,1,6,6,2,6,1,2,6],5:[3,2,6,1,1,1,2,1,2,2,6,0],6:[3,3,1,1,1,1,2,1,2,1,1,1],7:[3,2,2,3,1,1,4,2,2,3,2,0],8:[3,2,1,1,2,1,6,2,1,2,1,2]},
                 depth = 2.55475,
                 tuningBehavior = '20150713a',
                 behavSession = '20150713a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-15_16-09-03',
                 tuningSession = '2015-07-15_15-56-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,6,2,1,2,1,1,1,1,1,2],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,2,2,2,2,2,1,2,2,2,3],4:[3,6,1,3,2,6,2,1,2,2,2,6],5:[3,1,2,2,2,1,2,6,2,2,1,1],6:[3,1,3,2,6,2,2,1,2,1,2,2],7:[3,2,2,2,1,1,3,1,3,2,2,2],8:[3,2,1,1,1,1,1,1,1,1,1,6]},
                 depth = 2.594375,
                 tuningBehavior = '20150715a',
                 behavSession = '20150715a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-16_14-08-07',
                 tuningSession = '2015-07-16_13-50-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,2,6,1,6,1,2,2,1,3],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,2,1,2,2,2,3,2,2,2,0],4:[3,2,3,6,6,1,1,1,6,2,2,3],5:[3,2,4,2,2,3,6,1,2,2,6,2],6:[3,1,3,2,2,2,1,2,2,1,2,1],7:[3,5,1,1,2,2,2,2,3,2,1,2],8:[3,2,1,1,1,1,2,1,1,6,1,1]},
                 depth = 2.634,
                 tuningBehavior = '20150716a',
                 behavSession = '20150716a')
cellDB.append_session(oneES)
'''
#THE BEHAVIOR WAS SWITCHED FROM SWITCHING TO PSYCURVE MIDWAY THROUGH
oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-17_14-39-27',
                 tuningSession = '2015-07-17_14-20-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,1,2,1,1,1,6,2,2,1,1],2:[9,0,0,0,0,0,0,0,0,0,0,0],3:[3,3,3,2,2,1,2,2,2,2,2,1],4:[3,2,1,2,2,1,1,2,2,1,2,2],5:[3,2,6,4,1,3,5,6,2,2,5,2],6:[3,1,2,2,5,2,6,1,2,3,2,2],7:[3,2,3,3,3,2,2,5,1,2,1,0],8:[3,2,1,1,1,6,1,1,2,6,1,6]},
                 depth = 2.71325,
                 tuningBehavior = '20150717a',
                 behavSession = '20150717a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-22_16-20-38',
                 tuningSession = '2015-07-22_16-03-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,2,1,2,1,3,2,6,1,1],2:[3,2,2,4,4,4,4,4,4,3,4,4],3:[3,1,6,2,3,4,1,2,2,1,3,2],4:[3,1,2,3,1,2,1,2,4,4,2,1],5:[3,4,4,1,3,2,4,1,2,2,1,4],6:[3,1,6,2,1,2,2,4,2,4,2,3],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,1,1,1,2,1,1,1,1,1,0]},
                 depth = 2.7925,
                 tuningBehavior = '20150722a',
                 behavSession = '20150722a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-23_17-31-28',
                 tuningSession = '2015-07-23_17-18-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,5,5,1,2,5,3,3,5,2,5],3:[3,1,3,1,1,2,1,1,1,1,1,2],4:[3,4,2,5,2,2,2,3,5,1,2,0],5:[5,1,1,1,1,5,5,1,2,2,1,2],6:[3,3,3,2,2,4,1,6,2,2,2,2],7:[3,5,3,1,1,5,3,1,3,3,3,3],8:[3,1,3,2,2,5,5,2,2,2,1,0]},
                 depth = 2.87175,
                 tuningBehavior = '20150723a',
                 behavSession = '20150723a')
cellDB.append_session(oneES)
'''
#THE BEHAVIOR FILE IS MISSING FOR THIS SESSION
oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-24_11-56-39',
                 tuningSession = '2015-07-24_11-04-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,4,2,3,2,3,3,4,2,4,2,5],3:[3,1,1,1,1,2,1,2,1,6,1,2],4:[3,2,1,2,5,1,3,2,2,2,1,2],5:[3,2,1,3,2,2,1,2,2,1,1,3],6:[3,7,2,6,2,2,6,1,1,2,1,1],7:[3,3,3,1,1,1,1,1,2,1,1,1],8:[3,2,2,7,2,3,2,5,2,3,5,0]},
                 depth = 3.069875,
                 tuningBehavior = '20150724a',
                 behavSession = '20150724a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-27_13-57-32',
                 tuningSession = '2015-07-27_13-37-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,5,2,2,2,2,1,2,2,3,2],2:[3,2,2,2,2,2,1,2,3,2,2,0],3:[3,1,2,5,1,2,1,1,1,2,1,2],4:[2,0,0,0,0,0,0,0,0,0,0,0],5:[3,1,1,2,1,2,3,2,2,2,2,0],6:[3,1,1,2,6,6,1,1,6,1,1,1],7:[3,1,2,2,3,2,2,2,3,1,1,2],8:[3,2,1,1,2,2,2,1,1,2,3,2]},
                 depth = 3.085725,
                 tuningBehavior = '20150727a',
                 behavSession = '20150727a')
cellDB.append_session(oneES)
