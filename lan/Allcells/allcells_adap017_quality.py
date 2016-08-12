'''
List of all isolated units from one animal

Billy did these cluster qualities on 2016-06-20
Phoebe did 2016-04-20 onward, on 2016-07-12



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

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-02-25_15-29-36',
                 tuningSession = '2016-02-25_15-10-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,2,1,3,1,2,1,3,1,1],2:[3,2,2,2,1,3,1,2,2,2,1,1],3:[3,6,1,2,1,3,1,3,2,1,3,1],4:[3,3,2,2,2,3,1,1,3,3,3,0],5:[3,1,1,2,2,3,1,3,3,2,1,0],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,3,2,1,1,1,3,2,3,1,3],8:[3,3,6,2,2,3,1,2,3,3,0,0]},
                 depth = 2.55475,
                 tuningBehavior = '20160225a',
                 behavSession = '20160225a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-02-29_17-55-07',
                 tuningSession = '2016-02-29_17-45-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,3,2,4,1,1,3,1,2,3],2:[3,3,3,2,3,3,1,2,2,2,1,3],3:[3,3,6,3,1,3,4,4,3,3,3,3],4:[3,2,1,1,3,2,3,2,2,3,1,3],5:[3,3,2,2,2,3,1,2,3,2,2,2],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,2,6,3,6,2,1,3,1,4,3],8:[3,2,2,2,3,3,3,3,2,2,3,1]},
                 depth = 2.634,
                 tuningBehavior = '20160229a',
                 behavSession = '20160229a')
cellDB.append_session(oneES)
'''
#HAS A BUNCH OF MISSING TRIALS FROM BEHAVIOR (28). NOT SURE WHY
oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-03_16-12-31',
                 tuningSession = '2016-03-03_15-54-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,3,3,3,1,2,3,3,3,2,3],3:[3,1,1,6,1,1,3,3,1,1,3,3],4:[3,3,3,1,3,2,1,3,3,3,3,3],5:[3,3,3,3,2,3,3,3,3,2,3,2],6:[3,3,3,3,3,3,3,3,1,3,3,3],7:[3,3,3,2,3,3,3,1,1,1,2,1],8:[3,3,1,1,1,2,3,2,3,3,2,0]},
                 depth = 2.87175,
                 tuningBehavior = '20160303b',
                 behavSession = '20160303a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-15_15-17-43',
                 tuningSession = '2016-03-15_15-09-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,1,1,1,3,1,3,3,3,2],2:[3,3,3,1,1,1,3,2,1,3,3,3],3:[3,1,3,1,1,2,3,2,1,2,2,2],4:[3,3,3,1,3,1,3,2,3,3,2,1],5:[3,2,3,1,2,1,3,1,2,3,2,3],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,2,3,1,3,3,2,2,2,3,0],8:[3,2,3,2,1,4,2,1,3,1,1,0]},
                 depth = 2.87175,
                 tuningBehavior = '20160315a',
                 behavSession = '20160315a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-17_16-22-52',
                 tuningSession = '2016-03-17_16-14-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,3,3,1,2,3,3,1,3,3],2:[3,1,3,1,2,3,1,3,3,3,3,3],3:[3,1,6,2,1,3,2,3,6,1,3,3],4:[3,1,3,2,1,2,3,6,3,3,2,1],5:[3,3,1,3,3,3,2,3,1,3,1,3],6:[3,6,3,3,3,3,3,1,3,3,6,0],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,1,3,2,3,3,1,2,2,1]},
                 depth = 2.911375,
                 tuningBehavior = '20160317a',
                 behavSession = '20160317a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-21_16-59-16',
                 tuningSession = '2016-03-21_16-48-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,1,1,1,1,3],2:[3,3,3,3,2,6,1,3,3,3,3,1],3:[3,1,3,2,2,2,1,1,1,1,3,2],4:[3,1,1,2,3,1,1,3,3,1,2,1],5:[3,3,3,3,3,3,3,2,2,3,2,3],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,3,3,3,3,1,1,3,2,3,3],8:[3,3,6,3,3,6,6,1,1,2,2,2]},
                 depth = 2.951,
                 tuningBehavior = '20160321a',
                 behavSession = '20160321a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-23_15-33-17',
                 tuningSession = '2016-03-23_15-24-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,2,3,1,2,3,1,3,0],2:[3,3,1,3,3,2,3,3,3,1,3,3],3:[3,2,1,2,1,1,1,2,1,1,1,3],4:[3,2,1,2,3,3,1,2,3,3,3,1],5:[3,3,3,3,2,2,2,2,3,3,2,0],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,6,6,3,3,3,1,3,1,3,2,0],8:[3,3,6,2,6,3,3,1,2,3,6,1]},
                 depth = 2.990625,
                 tuningBehavior = '20160323a',
                 behavSession = '20160323a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-28_15-44-42',
                 tuningSession = '2016-03-28_15-35-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,6,2,3,1,3,1,3,3,3,3],2:[3,3,3,2,3,1,3,1,3,3,3,3],3:[3,3,3,1,2,3,1,3,1,3,2,1],4:[3,1,2,1,3,3,2,2,1,3,3,3],5:[3,3,3,3,1,2,3,2,3,3,3,3],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,3,2,3,2,3,3,6,6,6,3],8:[3,1,3,3,1,3,1,6,3,1,3,3]},
                 depth = 3.03025,
                 tuningBehavior = '20160328a',
                 behavSession = '20160328a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-30_14-56-23',
                 tuningSession = '2016-03-30_14-47-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,6,6,2,3,3,2,1,3,2],2:[3,1,2,3,1,3,3,3,3,3,3,0],3:[3,3,1,3,3,6,1,1,6,3,1,0],4:[3,3,3,1,1,3,1,2,1,2,1,0],5:[3,3,2,3,1,3,3,3,2,3,6,3],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,6,3,3,3,3,6,3,6,6,3],8:[3,4,2,2,6,2,1,3,3,3,2,6]},
                 depth = 3.069875,
                 tuningBehavior = '20160330a',
                 behavSession = '20160330a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-01_16-08-05',
                 tuningSession = '2016-04-01_15-54-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,1,3,3,3,1,1,3,3,1,3],2:[3,3,3,1,3,3,3,1,1,3,3,1],3:[3,3,3,1,3,1,1,2,3,2,1,3],4:[3,1,1,3,3,3,1,1,1,1,3,2],5:[3,3,3,3,3,3,2,1,2,3,1,1],6:[3,3,3,3,6,1,3,3,3,3,1,3],7:[3,3,3,3,3,6,1,3,1,3,3,1],8:[9,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.1095,
                 tuningBehavior = '20160401a',
                 behavSession = '20160401a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-05_16-24-18',
                 tuningSession = '2016-04-05_16-15-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,6,1,3,3,3,3,2,2,3,3],2:[3,3,1,2,3,3,3,3,3,3,3,3],3:[3,3,2,3,2,2,1,3,2,6,3,2],4:[3,6,2,3,1,3,3,6,1,2,1,1],5:[3,1,2,2,1,2,3,2,3,3,3,0],6:[3,1,3,3,3,3,3,3,6,3,3,1],7:[3,1,1,1,1,1,3,6,1,1,6,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.149125,
                 tuningBehavior = '20160405a',
                 behavSession = '20160405a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-07_16-07-14',
                 tuningSession = '2016-04-07_15-54-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[2,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,1,3,2,3,1,3,3,3,1,6],3:[3,2,6,3,2,1,1,6,3,6,3,2],4:[3,1,1,3,1,2,1,3,1,2,3,3],5:[3,3,3,3,2,1,1,2,3,3,3,3],6:[3,1,1,3,3,3,1,3,3,1,3,3],7:[3,3,3,1,3,6,1,2,3,6,3,3],8:[3,3,1,2,3,3,2,6,2,3,3,6]},
                 depth = 3.18875,
                 tuningBehavior = '20160407a',
                 behavSession = '20160407a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-11_17-40-24',
                 tuningSession = '2016-04-11_17-31-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[9,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,2,3,3,3,3,3,3,1,3,0],3:[3,2,2,1,3,3,6,3,3,1,1,2],4:[3,3,6,2,2,3,2,3,3,3,3,1],5:[3,2,3,3,1,1,2,3,3,3,3,2],6:[3,1,3,1,1,3,1,3,1,1,3,2],7:[3,3,6,6,3,1,1,1,3,3,3,1],8:[3,6,6,3,3,3,3,3,3,3,3,3]},
                 depth = 3.18875,
                 tuningBehavior = '20160411a',
                 behavSession = '20160411a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-12_14-09-06',
                 tuningSession = '2016-04-12_13-58-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,2,3,3,3,3,2,3,1,3],2:[3,3,3,1,3,3,3,1,1,3,3,3],3:[3,1,3,3,1,1,1,6,3,3,3,1],4:[3,6,1,3,1,3,2,2,3,2,2,3],5:[3,2,1,3,3,3,3,3,3,2,2,0],6:[3,3,1,1,1,3,1,1,3,3,3,1],7:[6,1,3,1,3,6,3,1,6,1,6,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.228375,
                 tuningBehavior = '20160412a',
                 behavSession = '20160412a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-14_14-41-07',
                 tuningSession = '2016-04-14_14-30-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,2,3,6,2,3,6,3],2:[3,3,3,1,3,3,3,3,3,3,3,3],3:[3,3,6,3,3,6,1,1,1,1,6,2],4:[3,6,1,3,1,1,3,3,1,6,1,3],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,2,1,1,1,3,1,1,1,3],7:[6,1,1,1,2,2,6,3,2,3,3,1],8:[3,3,3,3,3,3,2,3,2,3,2,0]},
                 depth = 3.268,
                 tuningBehavior = '20160414a',
                 behavSession = '20160414a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-18_17-09-56',
                 tuningSession = '2016-04-18_16-53-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,6,6,3,3,3,3,3,6,3],2:[3,2,3,3,3,3,3,3,3,3,3,3],3:[3,1,2,1,1,2,3,6,2,1,3,3],4:[3,3,3,3,1,3,3,1,6,2,6,3],5:[3,3,1,3,2,2,2,3,3,6,2,1],6:[3,1,3,1,3,3,3,3,1,1,3,1],7:[3,6,3,1,1,1,1,1,1,1,1,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.307625,
                 tuningBehavior = '20160418a',
                 behavSession = '20160418a')
cellDB.append_session(oneES)

#EPHYS FROZE DURING THIS SESSION
oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-20_16-27-10',
                 tuningSession = '2016-04-20_16-15-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,6,2,6,2,6,1,4,1,2,6],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,4,1,3,2,2,6,2,2,1,2],4:[3,4,1,2,2,1,3,1,1,1,1,0],5:[3,3,2,2,2,3,2,1,2,2,2,2],6:[3,3,2,3,3,3,1,3,3,3,3,2],7:[3,1,3,1,1,1,1,1,1,2,1,1],8:[3,2,2,2,2,2,3,2,2,3,1,0]},
                 depth = 3.34725,
                 tuningBehavior = '20160420a',
                 behavSession = '20160420a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-22_19-14-45',
                 tuningSession = '2016-04-22_19-04-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,2,2,2,1,2,1,2,1],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,6,6,2,2,6,2,3,6,2,0],4:[3,2,2,6,2,5,2,1,1,1,3,1],5:[3,2,2,3,3,1,2,2,2,2,2,0],6:[3,1,1,1,1,2,3,3,3,3,2,2],7:[3,2,1,1,2,6,3,2,1,1,2,2],8:[3,2,2,1,1,2,2,3,2,2,2,2]},
                 depth = 3.386875,
                 tuningBehavior = '20160422a',
                 behavSession = '20160422a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-23_18-38-57',
                 tuningSession = '2016-04-23_18-29-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,1,4,3,2,2,1,2,1,2],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,1,1,6,3,2,2,3,2,1,0],4:[3,2,3,3,3,1,1,1,2,2,2,3],5:[3,2,2,3,3,3,2,2,3,2,1,3],6:[3,1,3,3,3,3,2,6,3,1,3,4],7:[3,1,2,1,2,2,1,2,3,2,1,3],8:[3,2,2,3,3,2,3,2,2,2,2,2]},
                 depth = 3.386875,
                 tuningBehavior = '20160423b',
                 behavSession = '20160423a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-25_15-53-36',
                 tuningSession = '2016-04-25_15-43-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,3,6,2,2,1,2,1,0],2:[3,1,3,2,1,3,3,3,3,3,2,3],3:[3,2,1,2,2,1,1,1,3,1,1,0],4:[3,3,1,2,2,2,2,2,1,2,2,2],5:[3,2,3,2,2,2,2,2,2,2,2,2],6:[3,3,1,3,2,1,3,6,2,3,3,1],7:[3,2,1,1,2,2,2,2,2,1,1,2],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.4265,
                 tuningBehavior = '20160425b',
                 behavSession = '20160425a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-27_15-50-12',
                 tuningSession = '2016-04-27_15-39-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[2,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,3,3,3,3,3,3,3,3,1,3],3:[3,3,2,6,1,1,1,3,1,2,1,6],4:[3,3,3,3,1,4,2,2,3,2,3,3],5:[3,2,2,6,6,3,6,6,1,2,3,3],6:[3,3,3,6,3,1,3,2,2,3,3,3],7:[3,1,2,2,3,2,6,3,6,2,1,2],8:[3,3,4,1,3,2,4,2,2,2,2,0]},
                 depth = 3.466125,
                 tuningBehavior = '20160427a',
                 behavSession = '20160427a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-29_18-06-54',
                 tuningSession = '2016-04-29_17-57-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,2,2,2,2,2,3,3,5,2,2],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,3,5,5,2,1,3,1,1,1,2,1],4:[3,3,2,1,3,3,2,2,2,6,1,3],5:[3,3,3,3,2,3,3,6,6,6,2,3],6:[3,3,3,2,2,3,6,2,3,3,1,2],7:[3,1,2,1,2,3,1,6,6,3,2,2],8:[3,1,2,1,2,1,2,2,2,2,1,6]},
                 depth = 3.50575,
                 tuningBehavior = '20160429a',
                 behavSession = '20160429a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-05-03_17-42-53',
                 tuningSession = '2016-05-03_17-32-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,3,6,2,3,2,3,3,2,2],2:[3,3,3,3,3,3,3,3,3,3,3,0],3:[3,3,2,6,6,2,2,3,2,2,2,0],4:[3,3,5,3,3,3,3,3,2,3,3,3],5:[3,3,0,0,0,0,0,0,0,0,0,0],6:[3,6,3,2,2,3,3,3,3,1,3,2],7:[3,2,2,2,3,3,3,2,3,3,3,3],8:[3,2,1,2,2,3,2,2,2,2,3,1]},
                 depth = 3.545375,
                 tuningBehavior = '20160503a',
                 behavSession = '20160503a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-05-06_17-05-09',
                 tuningSession = '2016-05-06_16-55-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,2,3,3,1,3,2,2,5,0],2:[3,3,3,3,6,5,3,2,3,3,3,0],3:[3,3,3,2,3,2,3,2,3,3,3,3],4:[3,3,2,1,5,3,2,3,4,2,6,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,3,3,3,2,2,3,2,3,3],7:[3,3,2,3,3,3,2,5,3,2,2,2],8:[3,1,1,2,1,1,2,2,6,2,2,3]},
                 depth = 3.585,
                 tuningBehavior = '20160506a',
                 behavSession = '20160506a')
cellDB.append_session(oneES)

