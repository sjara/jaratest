'''
List of all isolated units from one animal

Billy did this cluster quality

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


oneES = eSession(animalName='test059',
                 tuningSession = '2015-06-17_21-15-19',
                 ephysSession = '2015-06-17_21-36-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,2,11,4,1,1,2,1,3],2:[3,3,5,3,1,2,61,2,2,2,1,2],3:[3,2,3,3,2,2,2,2,2,2,2,2],4:[3,1,1,3,2,1,1,2,1,4,2,2],5:[3,2,2,2,2,2,5,1,3,2,2,2],6:[3,3,1,1,6,1,1,3,1,3,1,3],7:[3,1,1,1,1,1,1,1,1,1,1,1],8:[9,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.951,
                 tuningBehavior = '20150617a',
		 behavSession = '20150617a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test059',
                 tuningSession = '2015-06-18_14-19-46',
                 ephysSession = '2015-06-18_14-41-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,1,3,2,1,2,2,11,1],2:[3,1,2,2,5,2,1,1,2,3,2,2],3:[3,3,3,2,2,4,2,2,2,2,2,2],4:[3,1,1,1,2,1,1,1,3,1,2,0],5:[3,2,2,2,1,2,1,2,3,3,2,2],6:[3,3,1,3,3,1,3,3,1,3,1,3],7:[3,1,1,1,1,1,1,3,3,1,1,2],8:[9,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.951,
                 tuningBehavior = '20150618a',
		 behavSession = '20150618a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test059',
                 tuningSession = '2015-06-19_13-49-41',
                 ephysSession = '2015-06-19_14-05-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,11,2,11,2,2,2,1,1,1,2,2],2:[3,1,2,2,1,2,2,2,5,2,1,2],3:[3,3,2,2,2,1,2,2,2,2,3,2],4:[3,2,1,1,2,1,1,1,2,1,1,1],5:[3,2,2,2,2,2,2,2,2,2,3,0],6:[3,1,1,2,3,1,1,3,3,1,3,3],7:[3,1,1,1,1,1,1,1,2,1,1,1],8:[9,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.951,
                 tuningBehavior = '20150619a',
		 behavSession = '20150619a')
cellDB.append_session(oneES)  

oneES = eSession(animalName='test059',
                 tuningSession = '2015-06-22_15-01-08',
                 ephysSession = '2015-06-22_15-21-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,2,1,1,2,1,2,1,3,1],2:[3,2,2,3,2,2,2,1,1,2,2,1],3:[3,1,1,3,2,1,2,2,2,2,1,2],4:[3,2,1,2,1,1,2,2,1,2,1,1],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,2,2,2,1,3,1,1,3],7:[3,1,3,1,1,2,1,1,1,1,5,0],8:[3,2,2,1,2,2,3,2,1,2,1,5]},
                 depth = 2.991,
                 tuningBehavior = '20150622a',
		 behavSession = '20150622a')
cellDB.append_session(oneES)  

oneES = eSession(animalName='test059',
                 tuningSession = '2015-06-23_14-52-57',
                 ephysSession = '2015-06-23_15-05-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,11,1,3,1,1,1,12,2,1],2:[3,1,2,2,2,2,2,1,1,2,1,0],3:[3,2,2,12,2,3,1,2,2,2,1,0],4:[3,2,1,1,1,1,2,1,2,1,1,3],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,3,1,1,1,1,2,1,1,1,1],7:[3,1,1,1,3,2,2,1,1,1,1,1],8:[3,2,1,2,2,1,2,2,2,1,2,2]},
                 depth = 2.991,
                 tuningBehavior = '20150623a',
		 behavSession = '20150623a')
cellDB.append_session(oneES)  

oneES = eSession(animalName='test059',
                 tuningSession = '2015-06-24_13-23-53',
                 ephysSession = '2015-06-24_13-38-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,11,1,1,1,2,11,1,1,1,1,3],2:[3,1,2,1,1,1,2,2,2,2,2,2],3:[3,2,2,3,2,2,2,1,1,1,2,0],4:[3,1,1,1,1,1,2,2,1,1,2,0],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,2,2,1,1,1,1,1,1,1,1],7:[3,1,1,2,1,1,1,1,1,1,2,0],8:[3,2,2,2,1,2,1,2,2,1,1,2]},
                 depth = 2.991,
                 tuningBehavior = '20150624a',
		 behavSession = '20150624a')
cellDB.append_session(oneES)  

oneES = eSession(animalName='test059',
                 tuningSession = '2015-06-25_15-04-26',
                 ephysSession = '2015-06-25_15-22-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,2,11,2,1,2,3,1,1,1],2:[3,2,1,2,2,2,1,2,1,2,1,2],3:[3,2,2,1,2,2,2,1,2,1,1,1],4:[3,2,1,1,2,2,1,2,2,1,2,0],5:[3,2,2,2,1,2,2,1,2,2,2,2],6:[3,2,1,1,2,12,1,1,1,1,12,2],7:[3,3,1,1,2,1,1,1,1,1,1,2],8:[2,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.991,
                 tuningBehavior = '20150625a',
		 behavSession = '20150625a')
cellDB.append_session(oneES)  

oneES = eSession(animalName='test059',
                 tuningSession = '2015-06-26_15-28-39',
                 ephysSession = '2015-06-26_15-46-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,2,1,3,1,1,3,1,11],2:[3,1,2,2,2,1,2,2,2,2,1,2],3:[3,2,3,2,1,2,1,2,2,1,3,0],4:[3,2,1,2,2,1,2,1,12,3,1,2],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,1,1,2,2,1,1,1,0],7:[3,1,1,1,1,1,1,1,2,1,1,1],8:[3,2,2,2,1,2,3,2,3,1,1,1]},
                 depth = 2.991,
                 tuningBehavior = '20150626a',
		 behavSession = '20150626a')
cellDB.append_session(oneES)  

oneES = eSession(animalName='test059',
                 tuningSession = '2015-06-28_16-49-45',
                 ephysSession = '2015-06-28_17-10-44',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,1,1,1,11,2,3,1,1,1],2:[3,1,3,2,2,4,2,4,1,1,2,0],3:[3,1,2,2,1,1,1,3,2,2,2,0],4:[3,2,1,4,4,3,1,1,2,2,4,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,1,2,1,6,4,3,1,1],7:[3,1,1,1,1,1,1,3,2,1,2,0],8:[3,3,2,4,2,2,3,2,2,2,4,2]},
                 depth = 3.030,
                 tuningBehavior = '20150628a',
		 behavSession = '20150628a')
cellDB.append_session(oneES)  

oneES = eSession(animalName='test059',
                 tuningSession = '2015-06-29_17-45-01',
                 ephysSession = '2015-06-29_18-01-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,11,2,2,11,2,1,3,2,2],2:[3,1,1,1,2,1,12,3,2,2,2,2],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,2,3,1,3,2,2,1,2,2,1],5:[3,2,1,2,2,2,2,2,1,2,2,2],6:[3,1,1,1,1,1,3,1,3,1,3,0],7:[3,2,1,1,3,2,1,2,1,1,1,1],8:[3,1,2,2,1,2,6,3,2,6,2,2]},
                 depth = 3.030,
                 tuningBehavior = '20150629b',
		 behavSession = '20150629a')
cellDB.append_session(oneES)  

oneES = eSession(animalName='test059',
                 tuningSession = '2015-06-30_16-16-33',
                 ephysSession = '2015-06-30_16-34-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,3,1,1,3,1,2,2,1,12],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,3,3,2,2,2,2,3,2,1,2,1],4:[3,1,1,1,3,2,3,2,2,2,2,2],5:[3,3,2,3,2,2,2,1,1,2,2,2],6:[3,2,3,1,2,3,1,1,1,1,3,1],7:[3,2,1,2,1,2,2,1,1,3,1,1],8:[3,2,2,6,2,2,3,3,2,2,2,2]},
                 depth = 3.030,
                 tuningBehavior = '20150630a',
		 behavSession = '20150630a')
cellDB.append_session(oneES)  

oneES = eSession(animalName='test059',
                 tuningSession = '2015-07-01_15-10-20',
                 ephysSession = '2015-07-01_15-26-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,12,2,2,2,1,1,1,3,2,2],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,3,1,3,2,2,3,3,1,2,2,2],4:[3,2,1,2,1,1,2,3,1,2,4,2],5:[3,1,2,2,2,2,3,3,2,4,2,3],6:[3,2,12,2,1,1,1,1,1,1,3,1],7:[3,2,2,1,1,1,1,1,2,2,3,0],8:[3,1,2,2,3,2,2,2,2,1,2,2]},
                 depth = 3.030,
                 tuningBehavior = '20150701b',
                 behavSession = '20150701a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test059',
                 tuningSession = '2015-07-02_15-22-07',
                 ephysSession = '2015-07-02_15-37-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,2,1,1,1,1,2,1,2],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,3,2,2,2,1,2,1,1,2,2,0],4:[3,1,1,1,2,2,1,2,2,1,3,0],5:[3,1,2,1,2,2,1,2,1,6,2,2],6:[3,1,1,3,1,1,1,2,1,1,3,3],7:[3,1,2,1,1,1,2,1,2,2,2,0],8:[3,7,2,1,3,2,2,6,2,2,2,0]},
                 depth = 3.070,
                 tuningBehavior = '20150702a',
		 behavSession = '20150702a')
cellDB.append_session(oneES)  


