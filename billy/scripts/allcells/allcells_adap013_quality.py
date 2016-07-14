'''
List of all isolated units from one animal

Lan 20160620

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
oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-10_10-10-28',
                 tuningSession = '2016-02-10_09-57-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 2.39625,
                 tuningBehavior = '20160210a',
                 behavSession = '20160210a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-18_17-51-19',
                 tuningSession = '2016-02-18_17-42-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[9,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,3,2,4,2,2,4,2,4,2,0],3:[3,2,4,2,2,2,3,4,3,3,3,2],4:[3,2,1,2,2,3,2,2,2,3,0,0],5:[3,4,2,4,4,3,4,1,3,0,0,0],6:[3,2,2,3,2,4,3,4,3,2,2,0],7:[3,2,2,2,3,2,3,2,3,3,2,0],8:[3,3,2,2,3,2,2,4,3,2,2,4]},
                 depth = 2.39625,
                 tuningBehavior = '20160218a',
                 behavSession = '20160218a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-19_16-49-26',
                 tuningSession = '2016-02-19_16-40-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[9,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,2,2,3,2,2,2,2,1,2,3],3:[3,2,2,1,3,3,2,2,3,2,2,3],4:[3,2,3,3,2,2,2,4,2,2,2,0],5:[3,2,2,3,1,1,1,3,2,2,1,0],6:[3,3,3,2,2,2,3,2,2,2,2,0],7:[3,2,3,3,2,2,2,3,3,3,2,3],8:[3,1,4,3,2,2,2,2,2,2,2,0]},
                 depth = 2.435875,
                 tuningBehavior = '20160219a',
                 behavSession = '20160219a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-23_10-39-53',
                 tuningSession = '2016-02-23_10-30-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,3,2,2,2,2,2,1,2,3],2:[3,3,3,4,4,2,2,4,4,2,0,0],3:[3,3,1,1,3,2,3,3,3,2,2,2],4:[3,2,2,4,3,4,2,3,2,2,2,0],5:[3,2,2,2,4,3,2,4,3,3,2,4],6:[3,3,2,3,2,3,2,2,2,3,2,3],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,3,4,4,2,4,2,2,3,3]},
                 depth = 2.4755,
                 tuningBehavior = '20160223a',
                 behavSession = '20160223a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-25_13-39-23',
                 tuningSession = '2016-02-25_13-30-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,4,2,2,2,3,3,2,2,2],2:[3,3,4,4,2,4,1,1,4,4,0,0],3:[3,1,1,2,4,2,3,2,4,1,3,0],4:[3,2,3,2,1,2,2,3,4,4,3,0],5:[3,1,1,4,4,7,4,3,3,1,0,0],6:[3,3,2,2,3,2,2,3,2,7,2,2],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,3,2,2,3,2,2,2,2,2,0]},
                 depth = 2.515125,
                 tuningBehavior = '20160225a',
                 behavSession = '20160225a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-29_11-23-17',
                 tuningSession = '2016-02-29_11-09-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,4,3,3,2,3,3,3,2,3],2:[3,2,2,1,2,2,2,1,2,2,3,2],3:[3,2,2,3,2,2,2,2,2,2,3,2,0],4:[3,2,2,1,3,2,1,2,2,3,3,0],5:[3,2,3,1,1,1,1,4,5,4,2,2],6:[3,2,2,2,2,2,2,2,2,2,3,2],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,2,2,2,2,2,3,1,2,0]},
                 depth = 2.55475,
                 tuningBehavior = '20160229a',
                 behavSession = '20160229a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-03_11-19-38',
                 tuningSession = '2016-03-03_11-09-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,2,2,3,3,2,2,2,4],2:[3,1,1,4,1,4,1,2,1,1,2,1],3:[3,2,1,2,2,2,1,1,2,2,3,0],4:[3,2,2,1,4,2,2,1,1,2,2,0],5:[3,4,1,4,1,1,1,4,4,4,4,0],6:[3,2,2,2,2,2,2,2,7,2,1,2],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,4,1,6,2,2,2,2,2,7,2,1]},
                 depth = 2.594375,
                 tuningBehavior = '20160303a',
                 behavSession = '20160303a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-15_13-48-39',
                 tuningSession = '2016-03-15_13-39-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,2,3,2,2,1,4,4,4,2],2:[3,1,3,1,1,4,1,1,4,1,1,1],3:[3,4,4,4,2,2,3,2,3,3,3,2],4:[3,4,2,3,4,2,2,2,2,2,2,2],5:[3,3,3,1,1,1,4,4,1,1,1,1],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,3,1,2,2,1,2,1,2,2,0],8:[3,1,2,1,1,1,2,1,4,1,1,2]},
                 depth = 2.594375,
                 tuningBehavior = '20160315a',
                 behavSession = '20160315a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-17_14-59-56',
                 tuningSession = '2016-03-17_14-47-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,3,2,2,2,4,2,3,3],2:[3,1,2,1,1,1,1,2,1,1,4,0],3:[3,3,2,2,2,3,4,2,2,2,3,2],4:[3,2,3,2,2,2,2,2,2,1,1,1],5:[3,1,1,4,1,1,4,1,1,1,1,0],6:[3,1,2,4,2,1,1,2,2,2,2,2],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,1,1,4,1,1,4,1,1,1]},
                 depth = 2.634,
                 tuningBehavior = '20160317b',
                 behavSession = '20160317a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-19_16-30-36',
                 tuningSession = '2016-03-19_16-21-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,3,4,2,2,2,3,2,2],2:[3,2,2,2,1,1,1,1,1,1,4,4],3:[3,2,2,3,2,2,3,2,2,1,2,2],4:[3,2,2,2,2,2,2,2,2,1,1,2],5:[3,4,1,1,1,1,1,1,4,4,4,1],6:[3,4,2,2,2,2,2,2,2,2,2,0],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,1,2,2,1,2,1,1,2,1,2]},
                 depth = 2.673625,
                 tuningBehavior = '20160319a',
                 behavSession = '20160319a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-22_13-32-19',
                 tuningSession = '2016-03-22_13-17-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,3,2,1,3,3,2,1],2:[3,1,4,1,1,1,2,1,1,1,1,0],3:[9,0,0,0,0,0,0,0,0,0,0,0],4:[3,2,3,1,4,4,2,3,3,1,6,1],5:[3,1,1,1,1,1,1,1,1,4,1,1],6:[3,2,2,2,4,4,2,3,2,2,2,2],7:[3,2,3,4,2,1,4,4,2,3,2,4],8:[3,1,2,1,1,1,1,3,2,2,2,4]},
                 depth = 2.752875,
                 tuningBehavior = '20160322a',
                 behavSession = '20160322a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-24_14-34-32',
                 tuningSession = '2016-03-24_14-24-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,4,3,4,2,2,4,3,2,2,4],2:[3,1,1,2,2,1,2,1,1,6,1,1],3:[3,3,2,2,2,2,3,2,3,2,3,2],4:[3,4,7,4,4,1,4,4,4,7,7,4],5:[3,4,1,4,4,1,1,2,1,4,4,1],6:[3,4,4,4,2,4,4,4,4,4,4,3],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,7,6,7,4,4,4,4,4,2,2,2]},
                 depth = 2.7925,
                 tuningBehavior = '20160324a',
                 behavSession = '20160324a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-29_15-33-15',
                 tuningSession = '2016-03-29_15-18-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,2,1,1,1,2,4,4,1,1],2:[3,1,1,1,1,1,1,1,1,2,1,1],3:[3,2,3,2,2,3,2,2,2,2,2,3],4:[3,1,4,2,2,1,2,1,1,4,2,2],5:[3,1,7,1,1,1,1,1,1,1,4,1],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,1,4,3,1,2,2,2,1,2,2],8:[3,1,1,1,2,1,1,2,2,2,1,1]},
                 depth = 2.832125,
                 tuningBehavior = '20160329a',
                 behavSession = '20160329a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-31_14-19-16',
                 tuningSession = '2016-03-31_14-07-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,2,2,2,2,3,1,1,4,3],2:[3,1,2,1,1,1,2,1,1,1,1,1],3:[3,3,2,3,3,2,2,2,2,2,3,2],4:[3,2,2,2,1,1,1,3,2,1,1,3],5:[3,3,3,1,1,2,1,1,1,7,1,2],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,3,1,3,2,2,1,2,2,1,4],8:[3,1,1,2,7,1,1,1,2,2,2,2]},
                 depth = 2.87175,
                 tuningBehavior = '20160331a',
                 behavSession = '20160331a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-04_15-16-10',
                 tuningSession = '2016-04-04_15-05-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,2,2,2,2,2,2,1,3,2],2:[3,2,1,1,1,1,1,1,2,1,1,1],3:[9,0,0,0,0,0,0,0,0,0,0,0],4:[3,6,1,1,1,2,1,2,2,2,1,2],5:[3,1,1,1,1,1,1,1,1,1,1,1],6:[3,2,3,2,2,2,3,2,2,1,2,1],7:[3,2,1,2,3,1,2,2,3,1,2,0],8:[3,1,3,1,1,1,1,2,7,2,7,2]},
                 depth = 2.911375,
                 tuningBehavior = '20160404a',
                 behavSession = '20160404a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-06_15-29-50',
                 tuningSession = '2016-04-06_15-13-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,2,2,2,2,3,2,2,2,2],2:[3,1,1,1,2,1,1,1,1,1,1,0],3:[3,7,3,2,2,1,1,1,1,2,2,3],4:[3,2,1,2,2,2,2,2,2,2,3,0],5:[3,1,3,1,2,1,1,1,4,1,1,1],6:[3,1,4,2,1,6,2,4,2,2,1,2],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,1,2,2,2,1,1,2,1,3]},
                 depth = 2.951,
                 tuningBehavior = '20160406b',
                 behavSession = '20160406a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-08_14-24-48',
                 tuningSession = '2016-04-08_14-14-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,2,3,2,2,2,2,3,3],2:[3,2,6,1,1,1,2,1,1,1,1,1],3:[3,3,3,4,4,4,4,2,1,2,2,2],4:[9,0,0,0,0,0,0,0,0,0,0,0],5:[3,1,1,1,6,4,6,1,1,1,1,0],6:[3,6,2,2,4,2,3,2,2,6,2,2],7:[3,6,2,1,3,7,3,2,2,2,2,1],8:[3,1,1,1,1,1,2,2,2,3,4,2]},
                 depth = 2.990625,
                 tuningBehavior = '20160408a',
                 behavSession = '20160408a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-12_15-44-55',
                 tuningSession = '2016-04-12_15-34-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,4,4,3,3,3,2,2,3,2],2:[3,1,1,1,1,1,1,6,1,1,1,1],3:[3,4,4,1,2,2,4,2,1,3,7,0],4:[9,0,0,0,0,0,0,0,0,0,0,0],5:[3,4,1,1,6,1,6,1,1,4,7,1],6:[3,2,3,6,7,3,3,3,7,6,6,7],7:[3,4,3,2,2,1,3,3,1,3,1,2],8:[3,2,2,2,2,1,2,1,3,2,1,1]},
                 depth = 3.03025,
                 tuningBehavior = '20160412a',
                 behavSession = '20160412a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-13_17-24-42',
                 tuningSession = '2016-04-13_17-14-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,2,3,3,3,3,2,2,2,0],2:[3,1,2,1,1,1,1,1,1,2,1,1],3:[3,3,3,2,3,1,2,2,2,7,3,2],4:[3,4,3,6,3,2,1,2,2,2,2,2],5:[3,7,1,4,1,4,1,4,2,1,1,7],6:[3,3,5,7,2,2,3,2,7,7,2,6],7:[3,6,1,2,2,2,3,7,2,1,1,0],8:[9,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.069875,
                 tuningBehavior = '20160413a',
                 behavSession = '20160413a')
cellDB.append_session(oneES)
