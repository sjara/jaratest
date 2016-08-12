'''
List of all isolated units from one animal

Quality rated by Phoebe

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

from jaratest.billy.scripts import celldatabase_quality_tuning as celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

'''
oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-13_11-16-20',
                 tuningSession = '2015-02-13_11-03-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 1.4755,
                 tuningBehavior = '20150213a',
                 behavSession = '20150213a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-14_14-24-36',
                 tuningSession = '2015-02-14_14-13-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 1.634,
                 tuningBehavior = '20150214a',
                 behavSession = '20150214a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-16_15-50-57',
                 tuningSession = '2015-02-16_15-36-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 2.34725,
                 tuningBehavior = '20150216a',
                 behavSession = '20150216a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-20_11-42-48',
                 tuningSession = '2015-02-20_11-32-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 2.4265,
                 tuningBehavior = '20150220a',
                 behavSession = '20150220a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-21_18-38-13',
                 tuningSession = '2015-02-21_18-29-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[2,0,0,0,0,0,0,0,0,0,0,0],2:[3,4,4,2,4,4,3,4,2,1,2,2],3:[},
                 depth = 2.4265,
                 tuningBehavior = '20150221a',
                 behavSession = '20150221a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-22_22-42-06',
                 tuningSession = '2015-02-22_22-34-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,5,5,5,2,3,2,2,2],2:[3,1,1,5,2,2,4,2,1,1,1,2],3:[3,3,2,2,2,4,4,1,1,4,1,4],4:[3,1,1,2,1,1,1,1,4,1,3,4],5:[5,6,2,4,1,1,5,2,2,1,3,2],6:[3,4,1,2,2,1,3,1,1,1,1,0],7:[5,4,3,3,1,1,2,1,1,2,4,2],8:[1,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.466125,
                 tuningBehavior = '20150222a',
                 behavSession = '20150222a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-23_13-23-03',
                 tuningSession = '2015-02-23_13-14-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[2,0,0,0,0,0,0,0,0,0,0,0],2:[0,4,1,3,3,3,4,2,2,3,2,3],3:[3,4,4,2,4,1,2,2,1,3,1,3],4:[3,1,4,1,1,2,4,1,4,1,1,3],5:[3,4,2,3,1,2,1,2,3,4,2,3],6:[3,1,3,1,4,4,2,4,4,3,4,4],7:[3,2,2,4,6,4,4,4,1,2,1,3],8:[3,4,2,3,1,1,4,1,4,1,2,4]},
                 depth = 2.50575,
                 tuningBehavior = '20150223a',
                 behavSession = '20150223a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-24_13-19-06',
                 tuningSession = '2015-02-24_13-06-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[2,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,3,2,2,1,3,3,3,1,3,0],3:[3,1,2,2,4,2,1,1,3,1,1,1],4:[3,1,1,1,1,1,1,1,4,2,2,1],5:[3,2,3,1,2,2,2,1,3,2,1,1],6:[3,4,1,1,2,1,3,1,1,1,3,2],7:[3,1,1,2,1,2,1,1,1,1,2,1],8:[3,2,5,1,3,1,1,1,3,1,2,0]},
                 depth = 2.545375,
                 tuningBehavior = '20150224a',
                 behavSession = '20150224a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-25_12-38-09',
                 tuningSession = '2015-02-25_12-27-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[2,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,5,2,1,3,1,1,2,2,1,5],3:[3,1,1,2,1,1,1,1,2,3,1,1],4:[3,1,2,1,1,1,1,1,1,2,1,1],5:[3,2,3,1,1,1,3,2,2,1,1,2],6:[3,1,2,1,1,1,1,1,3,3,2,1],7:[3,1,1,1,2,1,2,1,1,1,1,1],8:[3,1,2,1,2,1,1,1,1,1,1,1]},
                 depth = 2.585,
                 tuningBehavior = '20150225a',
                 behavSession = '20150225a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-26_13-06-01',
                 tuningSession = '2015-02-26_12-54-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,1,2,1,1,2,1,0,0,0],2:[3,4,3,1,1,2,3,1,1,2,1,2],3:[3,1,3,1,4,2,1,2,1,1,1,1],4:[3,1,3,1,1,1,2,1,1,2,0,0],5:[3,4,2,1,1,2,2,2,1,1,2,3],6:[3,1,2,2,2,1,2,1,1,1,2,1],7:[3,2,3,3,1,2,1,1,1,2,1,0],8:[1,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.585,
                 tuningBehavior = '20150226a',
                 behavSession = '20150226a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-27_13-15-39',
                 tuningSession = '2015-02-27_13-03-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[2,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,2,1,1,1,2,1,1,3,2,2],3:[3,4,1,2,1,2,1,1,6,1,4,2],4:[3,1,1,1,1,1,1,1,1,2,1,1],5:[3,2,1,2,2,1,1,2,1,3,2,0],6:[3,1,3,2,1,4,3,4,1,2,2,7],7:[3,1,1,1,1,1,2,2,1,1,4,2],8:[3,1,1,1,2,1,2,1,1,3,2,2]},
                 depth = 2.66425,
                 tuningBehavior = '20150227a',
                 behavSession = '20150227a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-28_19-02-10',
                 tuningSession = '2015-02-28_18-36-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,6,1,2,1,1,1,3,1,1,1],2:[3,1,1,1,1,2,3,1,2,2,1,1],3:[3,2,2,1,2,2,2,1,4,4,2,1],4:[3,4,1,5,1,2,4,2,1,1,1,2],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,2,2,1,2,4,2,1,1,2,5],7:[3,1,4,1,1,2,1,1,2,1,3,2],8:[3,2,1,1,4,1,2,4,5,2,2,1]},
                 depth = 2.7435,
                 tuningBehavior = '20150228a',
                 behavSession = '20150228a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-01_16-53-27',
                 tuningSession = '2015-03-01_16-43-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,3,1,1,2,1,6,1,1,6],2:[3,1,1,1,2,1,1,1,4,5,1,2],3:[3,1,1,2,2,2,1,2,1,3,1,2],4:[3,1,1,4,1,2,3,2,1,1,1,1],5:[3,4,2,1,3,2,1,1,1,2,1,2],6:[3,3,1,1,1,2,4,2,2,1,3,2],7:[3,3,2,2,3,1,1,2,2,1,1,2],8:[1,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.82275,
                 tuningBehavior = '20150301a',
                 behavSession = '20150301a')
cellDB.append_session(oneES)

'''
oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-02_13-35-20',
                 tuningSession = '2015-03-02_14-43-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 2.82275,
                 tuningBehavior = '20150302b',
                 behavSession = '20150302a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-03_11-42-14',
                 tuningSession = '2015-03-03_11-31-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,1,1,1,6,3,2,1,1,6,1],2:[3,1,2,2,2,1,1,1,3,1,3,1],3:[3,2,1,1,2,2,1,3,3,3,2,2],4:[3,2,1,3,2,1,1,2,2,1,2,0],5:[3,1,1,2,1,1,2,3,3,1,2,1],6:[3,1,1,2,1,2,1,1,4,3,2,1],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,1,1,2,2,1,1,2,1,2,1,0]},
                 depth = 2.82275,
                 tuningBehavior = '20150303a',
                 behavSession = '20150303a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-04_13-02-28',
                 tuningSession = '2015-03-04_12-49-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,3,1,1,2,3,2,1,1,7,1],2:[3,2,2,3,1,1,3,3,1,1,2,1],3:[3,2,3,2,3,1,1,1,2,3,2,3],4:[3,1,4,2,1,1,2,1,3,4,2,2],5:[3,1,2,1,4,3,3,5,2,1,1,1],6:[3,2,2,3,1,1,1,1,2,3,1,1],7:[2,0,0,0,0,0,0,0,0,0,0,0],8:[3,1,1,6,1,6,2,2,6,1,1,1]},
                 depth = 2.862375,
                 tuningBehavior = '20150304a',
                 behavSession = '20150304a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-05_14-12-36',
                 tuningSession = '2015-03-05_14-01-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,3,6,2,7,4,1,1,3,1],2:[3,2,2,6,1,2,6,5,3,2,1,0],3:[3,2,1,3,2,3,2,2,2,5,1,3],4:[3,1,1,1,2,2,4,3,1,1,2,4],5:[3,1,2,4,2,1,2,3,3,2,2,2],6:[3,1,2,3,1,1,3,2,1,1,2,1],7:[2,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,4,4,1,1,2,2,2,7,2,1]},
                 depth = 2.862375,
                 tuningBehavior = '20150305a',
                 behavSession = '20150305a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-06_12-30-25',
                 tuningSession = '2015-03-06_12-20-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,1,1,1,6,2,1,2,1],2:[3,2,2,2,1,2,2,3,6,6,2,2],3:[3,2,2,2,2,2,3,2,5,4,3,1],4:[3,2,1,2,2,4,1,2,2,5,1,2],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,2,3,1,1,2,1,2,2,2,2],7:[3,1,2,1,2,1,1,2,2,3,1,4],8:[3,6,2,2,1,4,3,1,1,1,1,2]},
                 depth = 2.862375,
                 tuningBehavior = '20150306a',
                 behavSession = '20150306a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-07_21-00-17',
                 tuningSession = '2015-03-07_20-51-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,1,2,1,1,2,1,1,1,0],2:[3,3,6,2,2,2,6,6,6,2,2,6],3:[3,1,2,2,2,1,1,3,2,1,2,2],4:[3,1,1,1,1,1,2,2,2,3,1,1],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,6,1,3,2,7,1,1,2,4,1,1],7:[3,2,4,2,6,2,1,3,4,1,2,0],8:[3,2,1,1,1,1,1,3,1,1,2,1]},
                 depth = 2.902,
                 tuningBehavior = '20150307a',
                 behavSession = '20150307a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-08_21-05-54',
                 tuningSession = '2015-03-08_20-56-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,2,3,1,1,1,1,1,1,0],2:[3,2,6,2,3,2,2,6,6,2,2,3],3:[3,1,2,3,2,1,1,3,1,1,2,3],4:[3,1,3,1,2,1,2,2,4,1,2,0],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,2,1,2,3,1,1,1,1,1],7:[3,1,2,6,1,1,1,3,1,2,1,2],8:[3,6,1,1,2,1,6,1,1,3,2,1]},
                 depth = 2.902,
                 tuningBehavior = '20150308a',
                 behavSession = '20150308a')
cellDB.append_session(oneES)

'''
oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-09_15-15-58',
                 tuningSession = '2015-03-09_15-07-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,3,1,1,1,1,2,2],2:[]},
                 depth = 2.941625,
                 tuningBehavior = '20150309c',
                 behavSession = '20150309a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-10_14-08-40',
                 tuningSession = '2015-03-10_13-57-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,2,2,1,1,2,1,1,1,6,0],2:[3,2,4,1,3,6,6,2,2,6,3,0],3:[3,1,1,2,2,1,2,1,2,2,3,1],4:[3,2,2,1,4,2,2,1,1,1,2,1],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,1,1,2,6,1,6,2,2,2,6],7:[3,2,6,1,2,2,2,1,1,1,2,0],8:[3,4,1,2,1,3,1,1,4,1,1,4]},
                 depth = 2.941625,
                 tuningBehavior = '20150310a',
                 behavSession = '20150310a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-11_13-23-02',
                 tuningSession = '2015-03-11_13-12-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,4,2,1,1,1,4,1,1,1,2],2:[3,7,6,2,2,3,2,2,7,1,2,3],3:[3,4,4,2,4,1,2,1,2,2,3,2],4:[3,2,2,1,3,1,1,2,2,2,2,2],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,6,6,1,2,1,1,1,6,1,3,2],7:[3,1,2,6,1,5,2,1,2,1,2,4],8:[3,1,1,1,1,1,1,1,1,2,1,0]},
                 depth = 2.98125,
                 tuningBehavior = '20150311a',
                 behavSession = '20150311a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-12_11-39-19',
                 tuningSession = '2015-03-12_10-59-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,2,1,1,1,2,2,1,1],2:[3,2,2,4,1,1,2,4,1,2,3,1],3:[3,1,2,4,3,2,2,2,1,2,1,1],4:[3,4,2,2,2,1,4,3,6,2,2,2],5:[3,2,2,2,1,3,4,1,4,1,2,2],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,2,1,2,1,3,1,2,4,6,0],8:[3,1,3,1,1,1,1,2,2,1,1,2]},
                 depth = 2.98125,
                 tuningBehavior = '20150312a',
                 behavSession = '20150312a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-13_11-53-29',
                 tuningSession = '2015-03-13_11-43-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,1,6,1,1,1,1,3,6],2:[3,2,2,2,3,2,6,1,3,6,6,5],3:[3,1,1,5,5,2,1,2,3,2,1,1],4:[3,2,1,2,2,1,1,2,2,1,3,2],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,2,6,6,1,2,1,1,2,1],7:[3,1,3,1,1,6,2,1,2,2,1,3],8:[3,1,3,2,1,1,1,1,2,1,1,1]},
                 depth = 2.98125,
                 tuningBehavior = '20150313a',
                 behavSession = '20150313a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-15_13-08-56',
                 tuningSession = '2015-03-15_12-57-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,2,1,1,1,1,3,1,1],2:[3,6,4,7,2,2,2,2,6,3,1,6],3:[3,1,1,1,2,1,5,2,2,1,3,0],4:[3,1,2,2,2,4,3,2,3,2,2,0],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,2,2,1,1,3,1,2,1,1,1],7:[3,6,2,6,6,1,1,2,2,3,2,1],8:[3,2,1,2,1,1,1,1,1,1,1,1]},
                 depth = 2.98125,
                 tuningBehavior = '20150315a',
                 behavSession = '20150315a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-16_11-20-30',
                 tuningSession = '2015-03-16_11-05-34',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,6,1,2,1,1,3,1,2,1],2:[3,6,2,2,1,4,6,1,2,2,2,3],3:[3,1,1,2,2,3,3,1,2,1,1,1],4:[3,4,2,4,3,3,1,2,2,4,2,1],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,4,2,3,2,2,1,1,1,1,0],7:[3,2,7,3,2,2,2,2,4,6,1,0],8:[3,3,1,1,1,1,1,1,1,1,1,1]},
                 depth = 3.020875,
                 tuningBehavior = '20150316a',
                 behavSession = '20150316a')
cellDB.append_session(oneES)

'''
oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-17_12-21-27',
                 tuningSession = '2015-03-17_12-11-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.020875,
                 tuningBehavior = '20150317a',
                 behavSession = '20150317a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-18_15-42-32',
                 tuningSession = '2015-03-18_15-32-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,1,1,1,2,2,3,2],2:[3,2,2,2,1,2,1,1,1,1,1,3],3:[3,2,2,2,1,2,2,2,2,2,2,3],4:[3,1,2,2,1,2,2,1,1,3,2,2],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,1,1,1,1,3,1,1,1,2,2],7:[3,2,4,1,2,1,2,1,2,3,2,0],8:[3,1,1,1,6,2,1,1,1,1,1,1]},
                 depth = 3.0605,
                 tuningBehavior = '20150318a',
                 behavSession = '20150318a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-19_15-04-52',
                 tuningSession = '2015-03-19_14-55-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,1,1,1,2,2,4,2,1,4],2:[3,1,1,1,1,2,1,6,2,1,3,1],3:[3,2,3,2,1,5,2,2,1,3,2,0],4:[3,1,1,1,1,2,1,1,1,1,2,1],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,3,1,6,1,2,2,1,1,3,1],7:[3,3,4,2,1,2,2,1,1,1,3,2],8:[3,1,1,1,1,1,3,1,1,1,2,1]},
                 depth = 3.0605,
                 tuningBehavior = '20150319a',
                 behavSession = '20150319a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-20_11-34-22',
                 tuningSession = '2015-03-20_11-24-44',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,4,4,1,2,1,1,6,1,0],2:[3,1,6,2,1,1,6,6,3,2,1,6],3:[3,2,2,2,3,2,3,1,1,2,2,2],4:[3,1,1,2,2,2,1,7,2,1,2,1],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,3,2,2,1,2,1,1,1,2,2],7:[3,2,3,2,2,6,2,2,2,2,1,0],8:[3,1,1,2,1,1,1,1,1,3,1,1]},
                 depth = 3.100125,
                 tuningBehavior = '20150320a',
                 behavSession = '20150320a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-21_15-33-38',
                 tuningSession = '2015-03-21_15-24-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,1,4,4,1,4,1,3,2],2:[3,7,4,7,1,1,1,3,2,1,6,4],3:[3,2,2,5,2,5,6,5,2,3,2,2],4:[3,1,2,1,1,1,2,7,1,1,1,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,2,2,2,2,3,3,1,1,1,3],7:[3,1,2,1,3,2,2,1,6,2,2,3],8:[3,1,2,2,1,2,1,1,1,2,1,3]},
                 depth = 3.100125,
                 tuningBehavior = '20150321a',
                 behavSession = '20150321a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-22_19-01-22',
                 tuningSession = '2015-03-22_18-51-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.13975,
                 tuningBehavior = '20150322a',
                 behavSession = '20150322a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-23_12-39-08',
                 tuningSession = '2015-03-23_12-24-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,1,2,1,1,1,2,1,3],2:[3,6,1,1,1,6,1,2,2,3,6,1],3:[3,2,2,2,3,2,2,1,3,2,2,0],4:[3,1,1,2,2,2,1,3,1,2,2,2],5:[3,2,2,2,2,1,2,2,3,2,2,2],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,6,4,5,2,1,2,1,2,2,1,6],8:[3,1,1,1,1,1,2,1,1,1,3,1]},
                 depth = 3.13975,
                 tuningBehavior = '20150323a',
                 behavSession = '20150323a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-24_12-33-05',
                 tuningSession = '2015-03-24_12-18-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,2,1,1,1,2,3,2],2:[3,2,1,1,1,1,1,1,1,1,4,1],3:[3,5,2,2,3,2,2,3,2,2,2,2],4:[3,1,1,1,1,2,1,5,1,2,1,2],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,2,1,2,5,2,3,3,1,2,1],7:[3,3,3,2,2,2,3,2,2,2,2,1],8:[3,2,1,1,1,1,1,1,1,1,1,3]},
                 depth = 3.179375,
                 tuningBehavior = '20150324a',
                 behavSession = '20150324a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-25_12-44-37',
                 tuningSession = '2015-03-25_12-33-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,1,6,1,2,1,3,1],2:[3,4,1,1,1,1,1,3,1,2,1,0],3:[3,2,2,2,2,1,1,5,3,2,6,1],4:[3,1,1,1,1,2,2,1,2,1,1,1],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,2,2,2,2,1,3,2,1,7,3],7:[3,2,3,2,1,2,1,2,3,2,2,0],8:[3,1,1,2,1,1,1,1,1,1,1,1]},
                 depth = 3.179375,
                 tuningBehavior = '20150325a',
                 behavSession = '20150325a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-26_11-18-10',
                 tuningSession = '2015-03-26_11-08-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,2,1,1,1,1,2,1,1],2:[3,1,1,2,1,1,1,6,1,1,1,2],3:[3,3,6,2,5,4,4,2,2,3,1,2],4:[3,1,1,1,1,1,1,1,2,2,2,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,5,1,2,3,3,2,3,2,3,8,2],7:[3,2,3,1,3,2,3,2,1,2,2,3],8:[3,1,1,1,2,1,1,1,1,1,2,1]},
                 depth = 3.219,
                 tuningBehavior = '20150326a',
                 behavSession = '20150326a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-27_12-31-11',
                 tuningSession = '2015-03-27_12-10-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,1,1,1,1,1,1,3],2:[3,2,1,1,1,1,1,1,1,1,1,1],3:[3,2,2,2,2,2,1,3,2,2,2,2],4:[3,2,1,2,2,1,2,2,1,6,6,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,5,3,3,2,2,2,2,1,2],7:[3,3,2,2,1,5,2,1,2,3,2,1],8:[3,1,1,1,1,1,1,1,2,1,1,1]},
                 depth = 3.219,
                 tuningBehavior = '20150327a',
                 behavSession = '20150327a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-28_20-36-26',
                 tuningSession = '2015-03-28_20-21-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,1,1,1,1,1,3,1,1,2,1],2:[3,1,1,4,3,1,3,1,2,1,1,1],3:[3,3,3,2,3,2,3,2,3,4,2,2],4:[3,1,2,3,3,1,2,1,7,1,1,4],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,2,1,3,1,2,6,3,3,2],7:[3,2,2,3,3,2,3,4,3,2,4,1],8:[3,4,1,4,1,2,1,3,1,1,1,4]},
                 depth = 3.258625,
                 tuningBehavior = '20150328a',
                 behavSession = '20150328a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-29_23-16-17',
                 tuningSession = '2015-03-29_23-05-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,1,1,1,1,1,2,1],2:[3,1,4,1,2,1,1,2,3,1,1,1],3:[3,1,2,2,2,2,2,7,2,5,2,0],4:[3,1,1,1,2,1,1,2,1,1,1,2],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,8,2,2,2,2,2,8,4,2,2,2],7:[3,2,2,2,2,2,3,2,2,3,1,2],8:[3,2,3,1,1,2,4,1,1,1,1,3]},
                 depth = 3.258625,
                 tuningBehavior = '20150329a',
                 behavSession = '20150329a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-30_12-32-26',
                 tuningSession = '2015-03-30_12-22-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,1,3,1,1,2,1,1,1],2:[3,1,1,1,1,2,1,1,3,2,1,0],3:[3,2,2,1,1,3,2,3,8,2,6,3],4:[3,2,2,1,1,1,2,1,3,1,2,1],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,2,3,5,3,2,2,3,2,2,0],7:[3,2,3,2,3,3,2,1,3,1,2,1],8:[3,1,6,6,1,2,6,1,1,3,1,1]},
                 depth = 3.258625,
                 tuningBehavior = '20150330a',
                 behavSession = '20150330a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-31_11-50-55',
                 tuningSession = '2015-03-31_11-41-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,3,1,1,2,1,1,1,1],2:[3,1,2,2,4,3,6,4,1,1,3,0],3:[3,5,2,3,3,2,3,1,2,8,1,8],4:[3,1,1,2,2,3,3,1,2,3,2,2],5:[3,3,3,2,2,3,3,1,2,2,3,2],6:[3,2,3,2,5,3,3,3,2,3,2,2],7:[2,0,0,0,0,0,0,0,0,0,0,0],8:[3,1,3,1,1,1,1,1,1,2,1,0]},
                 depth = 3.29825,
                 tuningBehavior = '20150331a',
                 behavSession = '20150331a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-01_13-04-43',
                 tuningSession = '2015-04-01_12-55-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,1,4,1,1,1,1,1,1,1,3],2:[3,4,2,3,1,2,4,3,1,4,1,2],3:[3,2,3,4,3,2,1,2,2,2,2,0],4:[3,2,1,3,2,2,1,2,1,1,6,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,2,2,3,3,3,3,2,2,2,3],7:[3,2,3,3,3,3,2,3,2,2,5,3],8:[3,4,1,1,1,3,1,2,1,1,1,0]},
                 depth = 3.29825,
                 tuningBehavior = '20150401a',
                 behavSession = '20150401a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-03_15-03-35',
                 tuningSession = '2015-04-03_14-50-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,1,1,2,1,2,1,1,1],2:[3,2,3,2,3,4,3,1,1,2,2,4],3:[3,1,1,3,6,3,2,2,3,1,2,2],4:[3,1,3,2,4,4,4,1,1,6,2,0],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,2,3,3,2,3,2,2,2,3],7:[3,3,2,6,3,3,4,2,3,2,2,3],8:[3,2,1,3,1,6,2,6,1,2,1,0]},
                 depth = 3.337875,
                 tuningBehavior = '20150403a',
                 behavSession = '20150403a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-06_15-15-25',
                 tuningSession = '2015-04-06_15-04-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,4,1,1,1,1,1,3,1,1],2:[3,4,3,2,2,5,2,3,3,2,7,0],3:[3,6,2,2,1,2,2,3,3,1,1,1],4:[3,6,2,3,5,6,2,3,6,1,2,2],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,2,3,2,2,2,3,3,2,3],7:[3,4,3,3,3,3,1,2,3,2,1,0],8:[3,1,2,1,1,1,1,3,1,1,1,6]},
                 depth = 3.337875,
                 tuningBehavior = '20150406a',
                 behavSession = '20150406a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-07_19-08-51',
                 tuningSession = '2015-04-07_19-00-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,4,1,1,6,1,1,7,1,6],2:[3,6,4,3,2,1,7,2,1,2,1,0],3:[3,1,2,3,2,3,6,3,3,2,2,1],4:[3,1,2,2,1,6,1,3,1,1,2,2],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,2,3,2,2,2,2,3,3,2],7:[3,2,1,5,2,3,1,3,1,2,2,2],8:[3,1,1,1,1,6,3,1,2,1,1,6]},
                 depth = 3.337875,
                 tuningBehavior = '20150407a',
                 behavSession = '20150407a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-08_12-12-18',
                 tuningSession = '2015-04-08_12-01-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,1,6,6,3,1,1,3,1,2,0],2:[3,1,1,1,6,1,1,1,3,6,3,2],3:[3,2,2,1,3,1,3,2,1,6,2,2],4:[3,3,4,4,1,2,1,4,2,1,2,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,2,2,2,3,2,3,3,5,2],7:[3,1,2,2,4,1,1,3,3,3,2,3],8:[3,6,1,3,1,1,1,1,2,6,1,3]},
                 depth = 3.3775,
                 tuningBehavior = '20150408a',
                 behavSession = '20150408a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-09_12-17-28',
                 tuningSession = '2015-04-09_12-06-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,6,1,6,6,1,2,6,1,1],2:[3,1,1,1,3,1,1,2,1,1,1,3],3:[3,2,1,2,1,2,1,3,1,2,6,0],4:[3,1,2,2,2,2,2,2,4,6,1,0],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,2,3,3,2,2,2,2,1,3,2],7:[3,2,2,2,1,2,2,3,1,3,2,2],8:[3,1,6,1,1,1,3,6,1,1,1,1]},
                 depth = 3.3775,
                 tuningBehavior = '20150409a',
                 behavSession = '20150409a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-10_12-34-00',
                 tuningSession = '2015-04-10_12-21-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,2,1,1,2,1,1,3,0],2:[3,2,2,3,2,4,1,1,1,6,3,6],3:[3,1,1,1,2,2,3,2,6,2,1,1],4:[3,6,6,2,2,4,2,2,2,2,1,0],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,2,2,2,2,2,2,3,2,3,2],7:[3,3,2,2,1,2,2,3,2,1,2,2],8:[3,1,1,1,1,1,6,2,3,1,1,1]},
                 depth = 3.417125,
                 tuningBehavior = '20150410a',
                 behavSession = '20150410a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-11_18-30-24',
                 tuningSession = '2015-04-11_18-21-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,6,1,6,1,6,1,1,1,2],2:[3,3,1,3,7,2,3,3,6,3,2,1],3:[3,1,6,1,2,2,2,1,3,1,2,1],4:[3,2,2,6,3,2,2,2,2,1,2,6],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,3,2,2,2,2,2,2,3,1],7:[3,2,2,2,3,3,3,2,2,2,3,1],8:[3,3,1,1,3,3,1,1,6,1,1,1]},
                 depth = 3.417125,
                 tuningBehavior = '20150411a',
                 behavSession = '20150411a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-13_15-54-20',
                 tuningSession = '2015-04-13_15-37-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,6,1,3,1,1,2,3,2],2:[3,1,3,1,1,3,1,1,2,3,2,0],3:[3,3,1,2,3,1,2,1,2,1,1,1],4:[3,4,3,2,6,1,2,2,2,2,3,2],5:[3,2,6,2,2,6,2,2,2,3,2,2],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,2,2,2,2,2,3,2,2,2,0],8:[3,6,1,3,1,2,1,1,1,2,6,1]},
                 depth = 3.45675,
                 tuningBehavior = '20150413a',
                 behavSession = '20150413a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-14_12-09-18',
                 tuningSession = '2015-04-14_11-57-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,2,1,3,1,1,1,2,3,1,1],2:[3,2,6,3,4,3,2,4,4,2,1,6],3:[3,1,2,1,3,2,1,1,6,3,2,4],4:[3,2,2,3,2,3,1,3,2,1,6,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,6,3,3,3,2,3,3,3,2,2],7:[3,2,2,3,3,2,2,3,2,3,2,0],8:[3,6,2,1,3,1,1,1,1,6,1,1]},
                 depth = 3.45675,
                 tuningBehavior = '20150414a',
                 behavSession = '20150414a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-15_12-29-45',
                 tuningSession = '2015-04-15_12-16-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,4,1,1,3,1,2,1,2,2,0],2:[3,2,3,5,2,3,3,3,2,3,3,6],3:[3,1,6,1,1,1,2,3,1,3,2,1],4:[3,6,3,6,2,2,2,2,3,2,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,2,2,3,3,2,3,3,3,2],7:[3,3,3,2,4,2,2,3,6,3,2,3],8:[3,1,1,3,3,3,3,1,6,1,1,3]},
                 depth = 3.496375,
                 tuningBehavior = '20150415a',
                 behavSession = '20150415a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-16_13-38-38',
                 tuningSession = '2015-04-16_13-28-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,1,1,2,3,1,2,2,3],2:[3,3,5,3,3,2,2,2,7,5,3,4],3:[3,1,1,3,2,1,1,1,1,2,2,1],4:[3,3,2,4,6,2,3,2,6,2,6,4],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,2,2,2,3,3,2,2,3,2,0],7:[3,2,3,3,3,3,3,2,1,3,2,3],8:[3,3,1,1,1,1,1,6,1,1,1,2]},
                 depth = 3.496375,
                 tuningBehavior = '20150416a',
                 behavSession = '20150416a')
cellDB.append_session(oneES)

'''
oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-17_16-21-33',
                 tuningSession = '2015-04-17_16-01-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.496375,
                 tuningBehavior = '20150417a',
                 behavSession = '20150417a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-18_15-43-54',
                 tuningSession = '2015-04-18_15-35-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,4,2,1,2,2,3,1,1,1,1],2:[3,7,2,2,3,1,2,6,3,3,2,3],3:[3,1,1,2,2,2,3,1,4,1,2,1],4:[3,1,1,1,7,1,1,2,2,3,1,1],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,2,5,2,3,5,3,3,2,3,2],7:[3,2,2,2,3,2,6,3,2,3,1,2],8:[3,1,1,2,1,1,1,1,1,3,1,1]},
                 depth = 3.496375,
                 tuningBehavior = '20150418a',
                 behavSession = '20150418a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-19_15-12-02',
                 tuningSession = '2015-04-19_14-14-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,1,1,1,1,2,3,2,1,1],2:[3,2,6,3,2,3,2,1,1,2,1,3],3:[3,1,2,2,1,2,1,1,1,3,1,2],4:[3,2,2,1,6,2,4,3,3,1,1,1],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,2,2,2,2,2,2,3,3,3,2],7:[3,2,2,2,1,2,2,2,3,2,2,3],8:[3,1,2,1,3,2,1,1,6,1,1,1]},
                 depth = 3.496375,
                 tuningBehavior = '20150419a',
                 behavSession = '20150419a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-20_13-31-52',
                 tuningSession = '2015-04-20_13-16-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,3,2,1,1,1,2,1,1],2:[3,3,3,2,3,3,1,2,2,2,7,0],3:[3,1,2,2,2,3,2,2,2,2,2,1],4:[9,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,3,2,2,7,1,6,1,2,2,3],6:[3,2,2,1,2,2,2,2,3,2,3,2],7:[3,3,3,6,2,2,2,2,2,2,2,0],8:[3,1,2,1,1,3,1,1,1,1,1,2]},
                 depth = 3.496375,
                 tuningBehavior = '20150420a',
                 behavSession = '20150420a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-21_13-43-00',
                 tuningSession = '2015-04-21_13-34-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,3,1,1,2,2,3,1],2:[3,6,2,2,2,6,2,6,2,3,2,0],3:[3,1,2,1,1,3,2,2,2,2,1,0],4:[9,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,2,2,2,2,2,1,2,2,7,2],6:[3,2,2,1,3,2,2,2,2,3,2,2],7:[3,2,2,3,2,2,1,1,2,2,1,0],8:[3,1,1,3,2,1,2,2,1,1,1,1]},
                 depth = 3.536,
                 tuningBehavior = '20150421a',
                 behavSession = '20150421a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-22_13-47-04',
                 tuningSession = '2015-04-22_13-37-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,3,1,2,1,1,1,2,1],2:[3,2,6,2,1,2,3,6,3,2,1,2],3:[3,3,2,2,1,1,2,2,2,1,2,1],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,6,2,2,6,2,3,2,1,2,0],6:[3,2,3,2,2,2,2,2,2,3,3,2],7:[3,3,2,2,2,3,2,2,2,2,1,2],8:[3,3,1,1,1,1,1,2,2,1,2,0]},
                 depth = 3.536,
                 tuningBehavior = '20150422a',
                 behavSession = '20150422a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-23_13-08-26',
                 tuningSession = '2015-04-23_12-55-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,4,2,1,2,3,1,3,1,1],2:[3,3,4,2,1,2,3,1,2,1,3,1],3:[3,2,1,2,2,4,2,2,2,4,6,1],4:[3,6,4,1,1,1,2,6,6,2,2,1],5:[3,2,6,7,4,3,6,2,2,2,2,0],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,2,2,2,2,3,2,1,2,1,2],8:[3,1,4,3,1,1,1,1,1,2,4,2]},
                 depth = 3.575625,
                 tuningBehavior = '20150423a',
                 behavSession = '20150423a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-27_15-41-55',
                 tuningSession = '2015-04-27_15-28-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,1,1,3,3,1,1,1,1],2:[3,3,1,3,2,2,1,3,2,2,2,1],3:[3,3,1,2,2,2,1,1,1,2,3,1],4:[3,1,1,2,2,1,2,6,3,2,1,2],5:[3,2,2,3,3,4,2,3,3,6,3,3],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,2,3,3,2,3,3,3,2,2,2],8:[3,1,1,1,3,1,1,1,1,3,2,0]},
                 depth = 3.575625,
                 tuningBehavior = '20150427a',
                 behavSession = '20150427a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-28_12-46-13',
                 tuningSession = '2015-04-28_12-37-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,1,3,1,2,1,1,1],2:[3,2,2,1,3,2,2,1,3,2,2,6],3:[3,1,1,1,1,2,2,2,2,2,2,3],4:[3,3,2,2,1,4,2,6,6,3,2,2],5:[3,2,7,2,7,7,2,3,2,7,7,2],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,6,2,2,2,2,2,2,2,2,3,0],8:[3,1,1,4,2,3,1,1,1,1,1,2]},
                 depth = 3.575625,
                 tuningBehavior = '20150428a',
                 behavSession = '20150428a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-29_12-48-20',
                 tuningSession = '2015-04-29_12-39-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,2,1,3,4,4,1,1,2,4],2:[3,4,2,1,2,1,2,3,2,2,2,2],3:[3,2,2,2,1,2,3,2,2,2,4,2],4:[3,2,6,2,3,2,1,2,2,6,2,4],5:[3,6,7,2,2,2,6,1,6,7,2,2],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,3,1,6,1,3,3,3,2,2,0],8:[3,4,1,4,1,4,1,1,1,1,1,3]},
                 depth = 3.575625,
                 tuningBehavior = '20150429a',
                 behavSession = '20150429a')
cellDB.append_session(oneES)
'''
#BEHAVIOR SESSION DOES NOT EXIST FOR THIS SESSION
oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-30_11-57-54',
                 tuningSession = '2015-04-30_11-49-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,2,1,1,3,1,6,1],2:[3,6,2,1,2,2,2,2,1,2,1,3],3:[3,2,2,1,2,1,1,2,6,3,2,4],4:[3,2,2,7,1,1,1,4,4,2,2,6],5:[3,3,6,2,6,6,2,6,2,2,2,6],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,2,2,1,6,2,2,1,1,3,2],8:[3,1,1,1,1,3,1,1,1,1,1,1]},
                 depth = 3.61525,
                 tuningBehavior = '20150430a',
                 behavSession = '20150430a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-01_12-59-12',
                 tuningSession = '2015-05-01_12-49-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,1,1,2,1,1,3,2],2:[3,2,4,1,2,2,4,3,1,2,4,5],3:[3,2,2,1,4,2,4,6,3,1,2,0],4:[3,2,3,3,7,6,1,2,6,6,7,6],5:[3,7,7,1,2,1,1,2,1,3,3,2],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,2,3,2,2,2,1,1,2,1,0],8:[3,1,1,4,4,1,1,1,1,1,2,3]},
                 depth = 3.61525,
                 tuningBehavior = '20150501a',
                 behavSession = '20150501a')
cellDB.append_session(oneES)

'''
oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-02_14-16-31',
                 tuningSession = '2015-05-02_13-44-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.61525,
                 tuningBehavior = '20150502a',
                 behavSession = '20150502a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-05_12-55-25',
                 tuningSession = '2015-05-05_12-42-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,2,1,1,2,1,6,1,1,1],2:[9,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,2,3,2,2,2,1,2],4:[3,1,2,6,3,6,6,1,6,6,2,0],5:[3,1,2,2,2,2,3,1,3,1,2,0],6:[3,2,3,3,3,2,2,2,2,3,3,2],7:[3,2,3,2,1,3,2,2,5,2,1,2],8:[3,2,4,2,3,4,1,1,1,1,1,0]},
                 depth = 3.61525,
                 tuningBehavior = '20150505a',
                 behavSession = '20150505a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-06_12-38-47',
                 tuningSession = '2015-05-06_12-26-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,1,2,1,1,1,1,1,1,1],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,2,1,3,2,1,3,2,1,0],4:[3,2,1,1,6,2,3,6,2,2,4,0],5:[3,2,3,1,3,3,2,2,2,2,2,3],6:[3,2,2,1,2,2,3,2,3,3,3,2],7:[3,1,3,1,2,2,2,3,1,2,1,3],8:[3,1,4,4,4,2,3,1,1,1,3,0]},
                 depth = 3.654875,
                 tuningBehavior = '20150506a',
                 behavSession = '20150506a')
cellDB.append_session(oneES)
'''
#OPEN EPHYS CRASHED DURING RECORDING
oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-07_12-48-13',
                 tuningSession = '2015-05-07_12-39-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,1,6,2,2,2,1,1,0],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,2,3,2,1,1,2,2,2,2,3],4:[3,1,3,1,1,2,6,3,2,2,1,1],5:[3,2,2,3,3,3,3,2,1,2,2,2],6:[3,1,2,2,1,2,2,2,3,3,3,1],7:[3,2,2,3,2,2,3,2,1,2,2,2],8:[3,1,1,1,3,2,1,1,1,1,1,1]},
                 depth = 3.654875,
                 tuningBehavior = '20150507a',
                 behavSession = '20150507a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-08_17-17-43',
                 tuningSession = '2015-05-08_17-08-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,1,1,2,6,1,1,1,1,0],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,1,2,2,1,1,1,2,1,2,2],4:[3,2,1,6,1,1,1,6,1,1,1,1],5:[3,2,2,1,2,2,3,2,2,3,3,2],6:[3,2,3,2,2,3,2,2,2,2,3,2],7:[3,2,2,2,1,1,3,2,3,6,1,0],8:[3,1,4,1,3,2,2,3,1,1,2,0]},
                 depth = 3.654875,
                 tuningBehavior = '20150508a',
                 behavSession = '20150508a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-09_20-39-25',
                 tuningSession = '2015-05-09_20-23-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,2,4,6,2,2,4,4,2,0],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,4,2,2,4,2,2,4,4,2,1],4:[3,1,4,1,1,2,1,3,4,2,4,2],5:[3,2,2,7,2,2,2,2,2,3,4,2],6:[3,2,1,2,3,2,2,3,3,2,3,0],7:[3,2,1,1,2,3,2,2,1,3,6,6],8:[3,4,1,1,1,1,1,2,3,1,2,0]},
                 depth = 3.6945,
                 tuningBehavior = '20150509a',
                 behavSession = '20150509a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-10_23-03-22',
                 tuningSession = '2015-05-10_22-53-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,1,2,1,1,1,2,2,1],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,2,2,2,1,1,3,1,2,1,0],4:[3,2,1,1,3,1,1,4,2,2,1,0],5:[3,1,2,2,1,2,2,2,2,3,3,1],6:[3,2,2,2,2,3,2,2,3,3,2,2],7:[3,6,6,2,2,2,2,3,2,1,1,2],8:[3,2,1,1,4,1,1,1,3,1,1,1]},
                 depth = 3.6945,
                 tuningBehavior = '20150510a',
                 behavSession = '20150510a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-11_15-31-25',
                 tuningSession = '2015-05-11_15-14-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,1,2,1,2,1,1,2,0],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,2,3,2,2,1,2,2,1,1,3],4:[3,1,1,1,4,2,1,3,1,2,1,0],5:[3,1,2,2,2,2,3,3,1,1,2,2],6:[3,2,2,3,3,2,2,2,2,4,3,2],7:[3,1,2,1,2,3,1,3,1,2,1,2],8:[3,2,1,3,2,1,1,1,1,1,4,3]},
                 depth = 3.6945,
                 tuningBehavior = '20150511a',
                 behavSession = '20150511a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-12_13-01-27',
                 tuningSession = '2015-05-12_12-51-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,6,2,3,1,2,6,2,2,6,1],2:[3,2,2,2,2,3,2,5,2,3,2,2],3:[3,3,1,1,2,2,1,1,1,2,2,0],4:[3,2,2,1,2,1,3,1,1,2,2,2],5:[3,2,2,2,6,2,2,3,3,1,2,2],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,1,1,1,2,1,2,1,3,1,2],8:[3,1,1,1,4,2,1,2,1,1,1,2]},
                 depth = 3.734125,
                 tuningBehavior = '20150512a',
                 behavSession = '20150512a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-13_13-07-12',
                 tuningSession = '2015-05-13_12-56-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,2,2,3,6,6,6,2,1,1,2],2:[3,3,2,2,3,3,2,2,2,2,2,2],3:[3,2,1,2,1,2,1,3,2,1,1,1],4:[3,1,1,2,2,2,2,1,2,3,2,3],5:[3,3,2,2,2,2,2,2,6,1,3,3],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,2,1,1,2,1,1,1,1,3,3],8:[3,1,1,1,1,1,2,1,1,1,1,2]},
                 depth = 3.734125,
                 tuningBehavior = '20150513a',
                 behavSession = '20150513a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-14_12-46-29',
                 tuningSession = '2015-05-14_12-36-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,6,6,6,1,1,3,1,3,2,0],2:[3,1,4,5,2,2,1,3,2,2,5,2],3:[3,1,2,1,1,3,1,2,2,1,1,2],4:[3,1,3,2,2,2,1,2,2,1,3,2],5:[3,2,2,2,2,2,1,3,2,2,5,3],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,3,1,1,1,2,1,1,2,2,3],8:[3,2,1,1,1,1,1,1,1,3,1,1]},
                 depth = 3.77375,
                 tuningBehavior = '20150514a',
                 behavSession = '20150514a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-15_12-05-23',
                 tuningSession = '2015-05-15_11-54-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,2,2,6,3,2,6,6,1,1,1],2:[3,1,1,2,2,1,2,2,3,1,2,2],3:[3,2,2,1,2,1,1,2,3,2,1,1],4:[3,2,1,2,2,1,3,1,2,1,2,6],5:[3,2,2,2,1,2,2,1,3,2,2,1],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,4,1,1,1,3,1,1,2,1,1],8:[3,1,1,1,2,1,1,1,1,1,2,1]},
                 depth = 3.77375,
                 tuningBehavior = '20150515a',
                 behavSession = '20150515a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-17_18-01-31',
                 tuningSession = '2015-05-17_17-52-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,2,6,6,3,6,7,2,1,6],2:[3,3,2,3,1,2,2,3,3,2,6,2],3:[3,1,6,2,1,2,1,1,6,2,2,3],4:[3,2,2,3,2,1,2,1,2,1,2,3],5:[3,2,2,2,1,2,2,3,2,3,2,1],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,2,1,1,1,1,1,3,1,1,1],8:[3,1,1,1,1,1,1,1,6,1,1,1]},
                 depth = 3.813375,
                 tuningBehavior = '20150517a',
                 behavSession = '20150517a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-18_13-13-02',
                 tuningSession = '2015-05-18_13-03-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,6,1,6,3,1,6,2,1,1,3],2:[3,2,2,2,2,3,2,2,1,1,3,3],3:[3,3,1,2,1,1,7,1,2,1,1,1],4:[3,1,1,2,1,2,2,1,1,2,2,3],5:[3,2,2,2,2,3,5,2,3,2,2,2],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,1,1,2,6,3,2,6,3,1,1],8:[3,1,1,1,2,1,1,2,2,1,1,1]},
                 depth = 3.813375,
                 tuningBehavior = '20150518a',
                 behavSession = '20150518a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-19_12-54-16',
                 tuningSession = '2015-05-19_12-42-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,6,2,6,6,1,6,1,2,2],2:[3,3,2,2,3,2,2,2,1,3,1,2],3:[3,1,1,1,1,2,2,2,1,1,1,1],4:[3,1,1,1,2,3,6,2,2,1,1,2],5:[3,2,2,2,2,2,2,3,2,3,2,2],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,1,1,1,3,1,2,1,1,1,2],8:[3,1,2,1,1,1,2,2,1,2,6,2]},
                 depth = 3.813375,
                 tuningBehavior = '20150519a',
                 behavSession = '20150519a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-26_13-19-02',
                 tuningSession = '2015-05-26_13-03-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,2,3,1,2,2,1,6,2,1],2:[3,1,6,1,2,2,3,3,3,3,6,1],3:[3,1,2,1,2,3,3,2,1,3,1,1],4:[3,2,1,2,2,3,1,6,2,2,1,1],5:[3,3,2,2,1,3,2,3,3,2,2,2],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,1,1,3,1,2,3,1,1,1,0],8:[3,2,3,3,2,2,3,2,3,2,2,0]},
                 depth = 3.813375,
                 tuningBehavior = '20150526a',
                 behavSession = '20150526a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-27_12-20-52',
                 tuningSession = '2015-05-27_12-10-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,3,1,2,2,2,2,6,1,0],2:[3,1,3,2,1,2,2,3,2,1,3,3],3:[3,3,1,1,2,1,1,1,1,1,2,2],4:[3,1,2,1,2,3,4,1,1,2,2,2],5:[3,2,2,3,2,3,2,3,2,3,2,2],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,2,1,1,1,3,1,1,1,3,1],8:[3,2,2,1,5,2,2,2,3,1,3,1]},
                 depth = 3.813375,
                 tuningBehavior = '20150527a',
                 behavSession = '20150527a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-28_12-49-35',
                 tuningSession = '2015-05-28_12-39-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,3,1,3,6,1,2,6,1,1],2:[3,2,2,6,3,2,3,3,2,3,3,3],3:[3,1,3,3,2,1,1,2,1,1,1,2],4:[3,1,3,1,1,1,1,2,2,1,3,2],5:[3,3,2,3,2,3,2,2,3,2,3,3],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,1,1,3,3,1,1,1,2,1,2],8:[3,2,2,2,3,3,1,3,3,6,1,2]},
                 depth = 3.853,
                 tuningBehavior = '20150528a',
                 behavSession = '20150528a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-29_14-00-38',
                 tuningSession = '2015-05-29_13-34-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,3,6,1,2,2,2,2,1,0],2:[3,2,2,2,2,2,2,2,6,3,3,2],3:[3,4,1,1,3,1,1,2,2,2,1,0],4:[3,2,2,1,7,1,2,2,2,7,2,3],5:[3,2,3,2,1,2,3,1,3,2,2,2],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,1,2,1,1,1,2,1,1,1,0],8:[3,5,2,6,2,1,6,3,1,1,1,6]},
                 depth = 3.853,
                 tuningBehavior = '20150529a',
                 behavSession = '20150529a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-30_15-51-45',
                 tuningSession = '2015-05-30_15-37-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,6,2,3,1,1,3,2,1,2,2],2:[3,2,2,1,2,3,3,2,3,3,2,2],3:[3,1,2,1,2,3,1,2,1,1,2,1],4:[3,2,2,2,1,2,2,1,1,3,2,2],5:[3,2,1,3,2,2,3,3,2,3,2,1],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,1,1,1,2,1,1,2,1,1,3],8:[3,1,6,2,6,6,6,1,1,2,3,3]},
                 depth = 3.853,
                 tuningBehavior = '20150530a',
                 behavSession = '20150530a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-06-01_12-51-07',
                 tuningSession = '2015-06-01_12-40-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,2,2,6,1,1,2,3,1],2:[3,3,2,3,3,2,2,2,6,2,2,2],3:[3,1,1,4,1,1,1,2,2,1,1,3],4:[3,6,1,2,1,1,2,1,2,1,2,1],5:[3,1,2,2,1,2,2,2,2,2,3,2],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,1,2,1,1,1,1,1,1,1,2],8:[3,1,1,1,2,1,1,2,1,1,2,1]},
                 depth = 3.892625,
                 tuningBehavior = '20150601a',
                 behavSession = '20150601a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-06-02_13-32-18',
                 tuningSession = '2015-06-02_13-21-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,1,1,2,1,1,2,2,1,3],2:[3,2,2,2,2,2,2,2,3,3,2,2],3:[3,1,1,2,1,3,2,1,1,1,2,0],4:[3,1,2,1,1,2,3,1,1,1,2,2],5:[3,3,2,3,3,2,2,2,1,2,3,2],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,2,2,3,2,2,2,3,1,2,2],8:[3,2,1,2,1,1,3,2,2,1,1,2]},
                 depth = 3.892625,
                 tuningBehavior = '20150602a',
                 behavSession = '20150602a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-06-03_15-16-32',
                 tuningSession = '2015-06-03_15-05-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,2,2,1,3,3,2,3,2,6],2:[3,2,6,3,2,1,2,2,2,2,6,0],3:[3,1,1,1,3,2,1,1,2,1,1,1],4:[3,3,2,6,1,1,1,3,2,6,1,2],5:[3,2,2,2,1,3,2,2,2,1,2,3],6:[2,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,2,1,2,1,1,2,3,2,2,2],8:[3,5,2,1,2,2,2,2,2,2,3,2]},
                 depth = 3.93225,
                 tuningBehavior = '20150603a',
                 behavSession = '20150603a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-06-04_15-02-05',
                 tuningSession = '2015-06-04_14-52-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,7,1,1,2,3,6,2,2,6],2:[3,2,6,2,2,2,6,1,3,3,2,0],3:[3,2,1,1,1,3,1,1,2,1,1,3],4:[3,1,2,3,2,2,1,2,1,2,1,1],5:[3,2,1,3,2,2,2,2,2,3,2,2],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,1,2,2,2,1,1,3,2,2,1],8:[3,2,2,3,2,1,1,2,3,2,2,0]},
                 depth = 3.93225,
                 tuningBehavior = '20150604a',
                 behavSession = '20150604a')
cellDB.append_session(oneES)

