'''
List of all isolated units from one animal

Billy did these

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

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-12_10-13-27',
                 tuningSession = '2016-04-12_10-04-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,1,1,3,2,1,2,1,1,1,2],2:[3,2,2,2,2,3,1,1,1,2,1,0],3:[3,2,3,3,2,1,1,3,3,1,3,0],4:[3,1,1,3,1,2,1,1,2,1,1,0],5:[3,2,1,1,2,1,3,1,2,3,1,6],6:[3,2,2,1,1,6,2,6,1,1,1,1],7:[3,2,3,1,1,1,2,1,1,2,1,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.634,
                 tuningBehavior = '20160412a',
                 behavSession = '20160412a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-13_11-34-15',
                 tuningSession = '2016-04-13_11-25-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,2,1,1,2,2,2,1,0],2:[3,2,2,1,1,2,3,2,3,0,0,0],3:[3,3,1,2,1,1,2,1,2,2,2,3],4:[3,1,3,1,1,1,3,1,3,1,2,2],5:[3,2,1,3,2,2,1,2,3,3,1,2],6:[3,2,1,1,6,1,3,1,1,6,3,1],7:[3,1,1,2,6,1,1,1,2,1,2,1],8:[9,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.634,
                 tuningBehavior = '20160413a',
                 behavSession = '20160413a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-14_11-33-59',
                 tuningSession = '2016-04-14_11-15-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,3,1,2,1,2,1,1,1,1],2:[3,1,2,1,3,2,1,3,2,1,0,0],3:[3,1,1,1,1,3,3,3,3,3,3,3],4:[3,1,1,1,1,2,1,1,3,1,2,3],5:[3,1,1,3,1,2,2,2,1,1,2,1],6:[3,1,1,1,6,3,2,2,1,2,6,3],7:[3,2,2,1,3,1,1,6,1,2,0,0],8:[2,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.634,
                 tuningBehavior = '20160414a',
                 behavSession = '20160414a')
cellDB.append_session(oneES)

'''
#THIS CRASHES FOR SOME REASON DURING CLUSTERING
oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-15_11-34-48',
                 tuningSession = '2016-04-15_11-22-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 2.673625,
                 tuningBehavior = '20160415a',
                 behavSession = '20160415a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-16_15-10-19',
                 tuningSession = '2016-04-16_15-00-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,1,1,1,2,1,2,0,0],2:[3,1,3,2,1,2,2,1,2,1,1,0],3:[3,3,3,1,1,3,3,2,3,3,3,3],4:[3,2,2,1,3,1,3,1,2,1,1,1],5:[3,2,1,3,3,1,3,1,3,1,1,1],6:[3,2,2,3,1,3,1,3,1,1,2,1],7:[3,1,3,1,2,1,2,1,1,1,1,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.71325,
                 tuningBehavior = '20160416a',
                 behavSession = '20160416a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-18_11-38-53',
                 tuningSession = '2016-04-18_11-30-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,1,1,1,2,2,1,0,0],2:[3,1,1,1,1,2,1,1,1,2,3,0],3:[3,2,1,3,1,3,3,3,2,1,3,0],4:[3,1,1,1,2,1,2,3,1,1,1,0],5:[3,2,1,1,2,1,2,1,1,1,1,3],6:[3,1,2,2,1,3,2,1,1,3,1,0],7:[3,1,3,3,1,1,1,3,1,1,1,0],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.752875,
                 tuningBehavior = '20160418a',
                 behavSession = '20160418a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-19_11-10-14',
                 tuningSession = '2016-04-19_11-00-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,6,6,2,6,6,3,2,6,1],2:[3,2,1,1,1,1,2,1,1,1,1,0],3:[3,1,3,2,2,1,3,1,4,3,3,2],4:[3,2,2,1,1,3,1,2,1,2,1,1],5:[3,2,1,1,1,2,1,2,2,1,3,3],6:[3,2,3,3,6,1,6,3,3,3,1,1],7:[3,1,3,2,3,2,1,1,1,1,0,0],8:[9,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.7925,
                 tuningBehavior = '20160419a',
                 behavSession = '20160419a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-20_13-51-59',
                 tuningSession = '2016-04-20_13-33-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,6,6,6,6,2,6,6,2,6,0],2:[3,2,1,1,2,2,1,3,2,1,2,1],3:[3,1,1,3,1,3,1,3,3,2,1,3],4:[3,1,1,1,1,1,1,1,1,2,1,1],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,2,1,3,1,2,1,1,1],7:[3,2,2,1,1,3,1,1,1,1,1,0],8:[3,6,2,1,2,1,2,2,1,3,1,2]},
                 depth = 2.832125,
                 tuningBehavior = '20160420a',
                 behavSession = '20160420a')
cellDB.append_session(oneES)

'''
#THIS DID NOT CLUSTER PROPERLY
oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-21_13-19-14',
                 tuningSession = '2016-04-21_13-02-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 2.832125,
                 tuningBehavior = '20160421a',
                 behavSession = '20160421a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-22_17-28-59',
                 tuningSession = '2016-04-22_17-19-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,2,6,3,6,1,1,1,3,3],2:[3,1,3,1,3,3,1,3,1,2,3,3],3:[3,1,3,3,2,1,3,1,3,3,1,2],4:[3,3,1,3,3,3,3,2,3,3,1,3],5:[3,1,1,1,3,1,3,1,1,3,3,2],6:[3,1,3,1,1,1,3,2,3,1,1,1],7:[3,1,2,3,1,2,1,1,2,1,3,2],8:[2,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.87175,
                 tuningBehavior = '20160422a',
                 behavSession = '20160422a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-23_16-00-54',
                 tuningSession = '2016-04-23_15-49-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,2,1,2,1,1,1,1,2,1],2:[3,3,1,2,1,1,2,2,1,2,1,2],3:[3,1,3,4,1,3,3,1,1,1,2,1],4:[3,2,2,3,2,1,1,3,1,2,4,0],5:[3,1,1,1,1,1,2,1,1,2,1,1],6:[3,6,1,2,1,6,2,2,1,1,1,2],7:[3,2,1,1,1,2,1,2,1,1,1,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.911375,
                 tuningBehavior = '20160423a',
                 behavSession = '20160423a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-24_13-36-15',
                 tuningSession = '2016-04-24_13-18-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,1,1,2,7,1,2,1,7],2:[3,2,2,1,1,2,1,2,2,2,2,1],3:[3,3,3,2,1,1,1,1,1,3,3,3],4:[3,1,1,4,3,1,2,2,1,1,7,2],5:[3,1,2,1,1,1,1,1,1,1,1,2],6:[3,2,2,2,1,1,1,1,1,3,1,1],7:[3,1,4,3,1,1,2,2,2,1,1,0],8:[9,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.951,
                 tuningBehavior = '20160424a',
                 behavSession = '20160424a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-25_11-49-47',
                 tuningSession = '2016-04-25_11-35-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,2,3,6,2,2,1,2,0],2:[3,2,2,3,1,1,1,1,2,3,1,0],3:[3,1,3,1,2,2,2,1,6,1,3,3],4:[3,1,3,2,4,1,6,1,2,6,2,1],5:[3,1,2,1,3,1,1,1,1,1,1,1],6:[3,6,1,1,2,1,1,2,1,2,1,1],7:[3,1,1,1,1,1,1,1,2,2,1,3],8:[9,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.951,
                 tuningBehavior = '20160425a',
                 behavSession = '20160425a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-26_14-14-28',
                 tuningSession = '2016-04-26_14-05-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,2,3,1,1,1,1,2,7,1],2:[3,1,2,2,2,1,1,1,1,2,2,0],3:[3,3,1,3,3,4,1,1,1,3,6,3],4:[3,3,1,1,1,6,6,6,3,1,3,3],5:[3,1,2,3,2,1,1,1,1,3,1,1],6:[3,2,6,1,2,1,1,1,2,1,1,0],7:[3,1,3,1,1,1,3,1,1,1,2,2],8:[9,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.990625,
                 tuningBehavior = '20160426a',
                 behavSession = '20160426a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-27_11-21-16',
                 tuningSession = '2016-04-27_11-04-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,2,1,2,2,1,1,1,0],2:[3,2,1,2,2,4,2,1,1,1,0,0],3:[3,3,1,2,6,1,2,3,1,4,3,1],4:[3,1,3,6,3,1,1,6,6,2,1,6],5:[3,1,1,1,2,2,1,3,2,2,3,6],6:[3,2,1,3,1,3,1,2,1,1,1,0],7:[3,3,1,1,1,1,1,1,3,1,2,0],8:[2,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.03025,
                 tuningBehavior = '20160427a',
                 behavSession = '20160427a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-28_11-28-44',
                 tuningSession = '2016-04-28_11-16-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,1,1,1,1,2,1,0,0],2:[3,1,1,2,1,1,2,2,1,1,3,0],3:[3,2,4,2,3,2,3,3,3,1,1,0],4:[3,2,1,1,3,1,3,2,3,3,1,6],5:[3,3,3,3,3,1,1,1,1,1,2,3],6:[3,3,1,1,1,2,1,1,2,1,1,2],7:[3,1,2,1,3,1,1,1,2,3,6,0],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.069875,
                 tuningBehavior = '20160428a',
                 behavSession = '20160428a')
cellDB.append_session(oneES)
'''
#THIS SESSION CRASHED DURING CLUSTERING
oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-29_11-07-51',
                 tuningSession = '2016-04-29_10-58-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.1095,
                 tuningBehavior = '20160429a',
                 behavSession = '20160429a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-30_16-28-23',
                 tuningSession = '2016-04-30_16-09-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,6,1,2,1,3,6,2,4,7,4],2:[3,1,1,2,2,1,2,1,2,1,0,0],3:[3,1,3,3,2,2,1,3,3,2,2,2],4:[3,1,2,1,2,2,2,2,1,1,3,1],5:[3,6,2,1,6,3,2,6,1,3,1,1],6:[3,6,2,1,3,3,2,2,2,1,1,2],7:[3,2,6,1,1,1,1,1,1,3,6,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.1095,
                 tuningBehavior = '20160430a',
                 behavSession = '20160430a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-02_11-49-55',
                 tuningSession = '2016-05-02_11-30-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,6,2,1,6,1,6,2,3,0],2:[3,1,3,2,2,1,1,1,1,1,0,0],3:[3,1,2,3,3,3,1,3,2,3,1,2],4:[3,1,2,1,1,3,3,1,2,3,0,0],5:[3,2,4,2,1,1,2,1,3,1,2,0],6:[3,1,3,1,1,1,2,2,1,1,1,0],7:[3,1,2,1,1,1,1,1,2,2,1,1],8:[2,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.149125,
                 tuningBehavior = '20160502a',
                 behavSession = '20160502a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-03_11-16-08',
                 tuningSession = '2016-05-03_10-50-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,6,1,2,6,6,3,2,6,6,2],2:[3,1,2,1,3,1,1,1,2,1,1,0],3:[3,1,2,2,3,1,2,2,2,1,2,0],4:[3,1,1,1,2,3,1,1,3,2,4,0],5:[3,2,2,2,1,3,1,1,1,1,1,0],6:[3,1,1,1,1,1,1,1,1,2,3,3],7:[3,1,6,3,2,1,1,1,3,1,3,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.149125,
                 tuningBehavior = '20160503a',
                 behavSession = '20160503a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-04_11-22-25',
                 tuningSession = '2016-05-04_11-13-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,2,2,2,1,2,2,3,3,2],2:[3,2,2,1,2,1,1,3,2,3,2,0],3:[3,3,1,1,3,3,1,3,2,1,2,2],4:[3,2,2,1,2,1,1,1,3,2,2,3],5:[3,1,1,1,3,1,2,3,3,2,3,1],6:[3,3,1,1,1,2,1,2,2,1,1,0],7:[3,1,1,3,2,1,1,6,6,1,1,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.18875,
                 tuningBehavior = '20160504a',
                 behavSession = '20160504a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-05_11-20-48',
                 tuningSession = '2016-05-05_11-02-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,2,1,2,3,2,3,3,0,0],2:[3,1,3,1,2,1,1,3,2,2,3,0],3:[3,2,3,1,1,2,2,2,2,3,2,0],4:[3,1,1,1,3,1,1,2,2,1,2,3],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,2,1,6,1,2,1,1,1,0],7:[3,6,2,3,2,1,3,1,1,1,2,2],8:[3,3,3,2,2,1,3,3,2,3,1,2]},
                 depth = 3.228375,
                 tuningBehavior = '20160505b',
                 behavSession = '20160505a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-06_11-28-57',
                 tuningSession = '2016-05-06_11-11-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,2,3,2,3,2,2,2,2,2],2:[3,3,2,1,2,3,3,1,1,3,1,2],3:[3,3,3,1,1,3,2,2,2,2,2,1],4:[3,2,1,3,1,1,2,1,3,1,1,0],5:[3,3,6,2,2,1,1,1,2,2,3,1],6:[3,2,3,1,3,1,1,1,2,4,2,0],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,3,1,2,1,2,1,3,2,2,0]},
                 depth = 3.268,
                 tuningBehavior = '20160506a',
                 behavSession = '20160506a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-09_15-30-51',
                 tuningSession = '2016-05-09_15-15-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,6,3,3,3,2,3,1,3,6,3],2:[3,3,1,2,2,3,1,3,3,2,3,2],3:[3,3,3,3,3,2,3,2,3,3,3,2],4:[3,3,2,3,2,3,1,3,2,3,1,1],5:[3,3,2,3,6,3,6,2,6,2,2,3],6:[3,2,1,1,4,3,3,3,2,2,2,2],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,3,1,3,3,3,1,1,3,3,1]},
                 depth = 3.268,
                 tuningBehavior = '20160509a',
                 behavSession = '20160509a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-10_16-05-15',
                 tuningSession = '2016-05-10_15-56-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.268,
                 tuningBehavior = '20160510a',
                 behavSession = '20160510a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-11_16-52-49',
                 tuningSession = '2016-05-11_16-42-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.268,
                 tuningBehavior = '20160511a',
                 behavSession = '20160511a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-12_14-17-17',
                 tuningSession = '2016-05-12_14-03-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,3,2,2,1,3,2,2,3,2],2:[3,3,1,1,2,1,1,1,2,1,0,0],3:[3,2,2,3,2,4,4,2,3,1,2,2],4:[3,3,1,1,1,1,4,2,1,1,1,1],5:[3,2,1,2,1,1,3,2,4,2,2,1],6:[3,1,1,2,2,1,1,2,1,1,1,0],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,1,3,2,1,3,3,1,3,2,4,0]},
                 depth = 3.268,
                 tuningBehavior = '20160512a',
                 behavSession = '20160512a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-17_15-23-11',
                 tuningSession = '2016-05-17_14-52-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,3,3,3,3,3,3,3,1,3,3],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,1,3,3,3,1,3,3,3,1,3,3],5:[3,3,3,3,3,3,3,3,3,3,3,2],6:[3,2,3,3,1,2,3,3,3,3,1,3],7:[3,2,1,3,3,3,1,3,3,3,3,2],8:[3,3,1,2,3,3,3,3,3,3,2,1]},
                 depth = 3.268,
                 tuningBehavior = '20160517b',
                 behavSession = '20160517a')
cellDB.append_session(oneES)
'''
#CRASHED DURING CLUSTERING FOR SOME REASON
oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-18_17-07-55',
                 tuningSession = '2016-05-18_16-50-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.268,
                 tuningBehavior = '20160518b',
                 behavSession = '20160518a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-19_16-51-16',
                 tuningSession = '2016-05-19_16-37-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[2,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,1,3,2,3,1,3,1,1,3,2],3:[3,1,1,2,2,3,2,3,2,3,2,0],4:[3,1,1,1,3,1,1,1,1,1,1,0],5:[3,2,1,2,1,2,2,2,3,3,1,2],6:[3,1,1,1,1,1,1,3,1,1,3,0],7:[3,1,2,1,1,1,3,1,2,1,1,3],8:[3,2,2,2,2,1,3,2,1,3,3,0]},
                 depth = 3.307625,
                 tuningBehavior = '20160519a',
                 behavSession = '20160519a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-20_17-36-11',
                 tuningSession = '2016-05-20_17-26-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,1,3,2,1,2,1,1,1,3,1,3],3:[3,2,2,2,3,3,3,1,3,3,1,0],4:[3,1,3,1,1,4,1,1,1,1,3,1],5:[3,1,6,2,1,3,2,1,2,2,2,0],6:[3,1,1,3,1,2,1,1,1,2,2,3],7:[3,3,1,3,2,1,1,2,1,2,2,1],8:[3,2,2,2,3,2,1,1,3,3,3,2]},
                 depth = 3.307625,
                 tuningBehavior = '20160520a',
                 behavSession = '20160520a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-21_18-16-27',
                 tuningSession = '2016-05-21_18-05-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,1,1,1,3,1,1,3,1,1,0],3:[3,3,6,2,2,1,3,3,3,3,2,3],4:[3,1,1,1,1,1,3,2,1,2,1,1],5:[3,3,1,3,2,3,2,1,1,6,2,2],6:[3,1,3,1,3,2,1,1,2,2,1,2],7:[3,1,1,2,1,1,1,3,3,1,2,3],8:[3,3,1,3,3,3,1,3,3,3,3,1]},
                 depth = 3.34725,
                 tuningBehavior = '20160521a',
                 behavSession = '20160521a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-22_17-24-28',
                 tuningSession = '2016-05-22_17-11-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[2,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,3,3,1,3,1,1,3,6,1,1],3:[3,2,3,1,1,3,2,2,2,3,2,2],4:[3,1,1,2,1,1,2,1,1,1,1,0],5:[3,3,3,1,2,2,2,1,2,2,1,1],6:[3,2,1,2,2,1,1,2,1,1,1,0],7:[3,1,2,1,1,3,1,2,2,1,1,1],8:[3,3,3,3,1,3,3,1,1,1,3,6]},
                 depth = 3.34725,
                 tuningBehavior = '20160522a',
                 behavSession = '20160522a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-23_17-35-02',
                 tuningSession = '2016-05-23_17-21-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,1,1,1,3,1,3,1,1,2,1,3],3:[3,3,3,3,1,2,2,2,2,1,3,1],4:[3,1,1,1,4,1,1,2,1,1,1,1],5:[3,2,2,1,3,3,2,1,1,3,1,1],6:[3,1,1,1,1,1,1,3,1,3,1,1],7:[3,1,1,3,1,1,2,1,1,2,0,0],8:[3,3,2,3,2,2,1,1,2,2,2,3]},
                 depth = 3.34725,
                 tuningBehavior = '20160523a',
                 behavSession = '20160523a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-24_16-00-48',
                 tuningSession = '2016-05-24_15-51-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[2,0,0,0,0,0,0,0,0,0,0,0],2:[3,1,3,2,2,6,3,3,6,1,1,1],3:[3,3,3,2,2,2,2,3,3,1,2,0],4:[3,1,2,1,1,1,1,1,1,2,1,1],5:[3,2,3,1,3,2,2,1,3,2,1,0],6:[3,2,1,1,2,1,2,1,1,1,3,3],7:[3,1,1,3,1,1,1,2,1,3,3,1],8:[3,3,2,3,2,3,1,3,2,1,2,2]},
                 depth = 3.34725,
                 tuningBehavior = '20160524a',
                 behavSession = '20160524a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-25_16-33-09',
                 tuningSession = '2016-05-25_16-22-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[2,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,2,1,1,1,6,1,3,3,2,2],3:[3,1,6,3,3,3,2,3,2,2,3,2],4:[3,1,2,1,1,1,1,2,1,1,1,1],5:[3,2,2,2,2,2,2,3,1,1,2,2],6:[3,1,1,1,1,2,1,2,2,1,1,1],7:[3,1,2,1,3,2,1,1,1,2,2,3],8:[3,2,3,3,3,3,3,1,3,2,2,3]},
                 depth = 3.34725,
                 tuningBehavior = '20160525a',
                 behavSession = '20160525a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-26_14-44-25',
                 tuningSession = '2016-05-26_14-34-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,1,1,6,1,3,3,3,6,3,1,1],3:[3,2,2,2,2,3,2,3,3,2,2,0],4:[3,2,1,1,4,4,1,4,2,2,1,1],5:[3,2,3,2,2,2,2,2,2,2,3,1],6:[3,1,2,2,1,1,1,1,1,1,3,0],7:[3,3,3,3,2,2,1,2,3,1,1,1],8:[3,2,1,3,3,3,2,2,1,3,3,3]},
                 depth = 3.386875,
                 tuningBehavior = '20160526a',
                 behavSession = '20160526a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-27_16-23-47',
                 tuningSession = '2016-05-27_16-07-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,1,1,6,6,3,3,1,1,6,3],3:[3,3,3,2,3,2,3,2,2,3,3,2],4:[3,1,2,1,1,1,1,3,1,1,1,1],5:[3,3,2,2,2,2,3,1,2,2,3,2],6:[3,3,1,1,1,1,2,1,3,1,1,1],7:[3,1,1,1,1,1,3,1,2,2,1,3],8:[3,3,3,2,3,2,2,1,3,1,3,2]},
                 depth = 3.386875,
                 tuningBehavior = '20160527a',
                 behavSession = '20160527a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-31_16-46-11',
                 tuningSession = '2016-05-31_16-32-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[2,0,0,0,0,0,0,0,0,0,0,0],2:[3,1,2,1,1,2,3,1,1,1,3,1],3:[3,3,3,3,3,3,3,3,2,4,3,3],4:[3,3,1,1,1,1,3,1,1,1,1,1],5:[3,3,2,2,2,2,3,2,2,2,2,1],6:[3,1,2,2,1,1,1,1,1,1,1,4],7:[3,1,1,2,1,2,1,1,1,3,2,3],8:[3,3,3,3,3,2,2,2,3,1,3,3]},
                 depth = 3.386875,
                 tuningBehavior = '20160531a',
                 behavSession = '20160531a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-01_16-08-40',
                 tuningSession = '2016-06-01_15-52-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,1,6,6,1,1,3,2,3,3,6,6],3:[3,2,3,2,3,3,3,3,2,2,3,0],4:[3,2,1,1,2,2,1,3,1,1,1,0],5:[3,3,2,3,2,2,2,3,1,1,2,2],6:[3,1,1,1,1,6,3,2,1,1,1,1],7:[3,3,2,1,1,1,2,3,1,1,3,2],8:[3,3,6,3,3,3,3,3,6,3,2,1]},
                 depth = 3.4265,
                 tuningBehavior = '20160601a',
                 behavSession = '20160601a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-02_15-11-46',
                 tuningSession = '2016-06-02_15-01-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,1,1,2,2,1,3,6,3,6,1,3],3:[3,6,3,3,2,3,3,3,6,3,3,3],4:[3,3,3,1,2,1,1,1,1,1,4,1],5:[3,2,3,2,3,1,3,3,3,3,3,2],6:[3,2,6,1,2,1,1,6,2,2,1,1],7:[3,2,2,2,3,1,1,2,1,3,2,1],8:[3,3,3,3,3,1,3,2,3,3,3,3]},
                 depth = 3.4265,
                 tuningBehavior = '20160602a',
                 behavSession = '20160602a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-03_15-49-24',
                 tuningSession = '2016-06-03_15-39-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,2,3,3,3,2,2,1,1,6,3],3:[3,2,3,3,3,3,3,3,3,3,3,3],4:[3,3,3,3,2,1,1,1,3,2,1,3],5:[3,3,3,3,3,3,2,2,3,2,3,0],6:[3,2,3,6,2,6,1,1,1,6,1,0],7:[3,3,1,3,2,1,2,3,1,1,3,2],8:[3,3,3,3,3,1,3,3,2,3,3,0]},
                 depth = 3.466125,
                 tuningBehavior = '20160603a',
                 behavSession = '20160603a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-07_15-14-50',
                 tuningSession = '2016-06-07_15-06-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,1,3,3,1,3,2,2,3,2],2:[3,3,3,2,1,3,2,2,3,1,2,3],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,2,2,2,2,1,3,1,3,1,3,1],5:[3,3,3,1,3,3,3,3,2,3,3,3],6:[3,3,1,1,1,1,2,1,1,2,1,1],7:[3,3,2,2,3,3,3,1,2,2,2,0],8:[3,1,3,2,3,3,2,3,1,3,3,3]},
                 depth = 3.50575,
                 tuningBehavior = '20160607a',
                 behavSession = '20160607a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-08_16-09-27',
                 tuningSession = '2016-06-08_15-47-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,1,1,3,3,3,3,3,3,1],2:[3,6,3,3,2,6,2,3,2,3,3,3],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,2,2,2,1,3,3,2,1,2,1],5:[3,2,2,1,2,3,3,3,2,3,2,2],6:[3,6,3,1,1,1,1,3,6,1,1,1],7:[3,2,3,3,2,2,3,3,2,3,2,3],8:[3,3,2,3,3,3,1,3,2,6,1,3]},
                 depth = 3.545375,
                 tuningBehavior = '20160608a',
                 behavSession = '20160608a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-09_15-07-54',
                 tuningSession = '2016-06-09_14-54-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,3,3,2,3,1,2,2,1,1],2:[3,3,2,3,2,3,3,1,2,3,3,3],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,1,2,2,1,1,3,3,3,3,3],5:[3,3,3,3,3,2,3,2,3,3,3,2],6:[3,1,2,1,2,1,2,2,3,1,3,0],7:[3,3,3,3,2,3,2,3,3,2,2,0],8:[3,2,2,2,3,2,2,3,1,3,2,2]},
                 depth = 3.585,
                 tuningBehavior = '20160609a',
                 behavSession = '20160609a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-10_16-00-02',
                 tuningSession = '2016-06-10_15-44-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,1,3,3,3,2,3,3,3,2],2:[3,3,3,2,3,3,3,3,2,1,6,2],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,1,3,1,1,1,3,2,3,2,2],5:[3,3,3,3,3,3,3,1,2,3,3,3],6:[3,2,2,1,1,1,2,3,2,1,3,3],7:[3,3,3,2,2,3,3,2,3,2,3,3],8:[3,2,1,2,3,2,3,3,1,3,2,3]},
                 depth = 3.624625,
                 tuningBehavior = '20160610a',
                 behavSession = '20160610a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-13_15-59-04',
                 tuningSession = '2016-06-13_15-43-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,1,1,1,2,2,2,3,2,3,2,3],3:[3,2,2,2,3,1,2,3,3,2,2,3],4:[3,1,1,2,1,1,2,3,2,2,1,6],5:[3,3,2,3,2,3,6,1,3,2,2,2],6:[3,1,6,1,3,1,2,2,1,1,1,0],7:[3,2,4,2,2,2,3,3,3,1,3,2],8:[3,3,2,2,3,2,1,3,3,2,2,2]},
                 depth = 3.66425,
                 tuningBehavior = '20160613a',
                 behavSession = '20160613a')
cellDB.append_session(oneES)

'''
#THIS SESSION DOES NOT HAVE A TUNING CURVE
oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-14_16-42-17',
                 tuningSession = '2016-06-14_16-31-34',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.66425,
                 tuningBehavior = '20160614a',
                 behavSession = '20160614a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-15_16-58-40',
                 tuningSession = '2016-06-15_16-48-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,3,2,2,3,2,3,3,3,2],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,3,3,2,1,3,1,2,3,3,2],4:[3,1,1,3,3,2,6,2,2,3,3,2],5:[3,2,3,3,1,2,3,2,3,3,3,3],6:[3,3,1,1,1,2,2,1,2,1,1,1],7:[3,3,3,3,1,1,1,3,3,3,1,3],8:[3,2,2,1,2,2,3,2,2,2,6,3]},
                 depth = 3.66425,
                 tuningBehavior = '20160615a',
                 behavSession = '20160615a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-17_16-57-58',
                 tuningSession = '2016-06-17_16-42-44',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.703875,
                 tuningBehavior = '20160617a',
                 behavSession = '20160617a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-20_15-49-04',
                 tuningSession = '2016-06-20_15-39-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,3,1,2,3,2,3,1,3,6],2:[3,3,3,2,3,3,2,3,3,3,3,3],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,1,1,1,2,3,2,3,1,3,2,2],5:[3,3,2,1,6,3,3,3,2,3,2,3],6:[3,3,1,1,1,1,1,3,1,2,1,1],7:[3,2,1,1,3,6,2,3,3,1,2,6],8:[3,1,3,1,2,3,1,3,3,6,3,3]},
                 depth = 3.703875,
                 tuningBehavior = '20160620a',
                 behavSession = '20160620a')
cellDB.append_session(oneES)

