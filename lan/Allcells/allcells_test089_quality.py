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

from jaratest.billy.scripts import celldatabase_quality_tuning as celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-27_16-03-24',
                 tuningSession = '2015-07-27_15-48-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,1,1,2,3,1,2,2,6,1],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,3,3,2,1,2,1,3,1,3,0],4:[3,1,1,3,1,2,1,1,1,2,1,2],5:[3,3,1,2,3,3,3,3,1,2,2,2],6:[3,1,1,1,1,1,1,1,2,1,1,3],7:[3,1,2,2,3,2,2,1,1,2,3,3],8:[3,3,1,1,3,1,6,2,7,1,1,1]},
                 depth = 2.39625,
                 tuningBehavior = '20150727a',
                 behavSession = '20150727a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-28_13-54-29',
                 tuningSession = '2015-07-28_13-39-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,2,3,1,3,1,2,1,1,1],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,3,2,2,1,1,3,3,3,3,1,2],4:[3,3,1,1,1,2,2,2,1,3,1,0],5:[3,3,1,3,3,1,3,2,1,1,2,3],6:[3,1,1,1,2,2,2,1,2,2,2,1],7:[3,3,3,6,3,3,3,1,6,3,2,1],8:[3,1,1,3,1,1,2,2,1,1,6,3]},
                 depth = 2.435875,
                 tuningBehavior = '20150728a',
                 behavSession = '20150728a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-29_10-26-08',
                 tuningSession = '2015-07-29_10-02-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,3,3,1,3,2,3,2,3,1],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,3,2,3,2,3,1,1,1,2,3],4:[3,3,1,1,1,3,3,1,1,1,2,0],5:[3,2,3,1,3,2,3,3,1,3,2,3],6:[3,2,1,1,1,3,1,1,3,2,2,2],7:[3,6,2,1,2,1,3,3,3,2,2,2],8:[3,1,1,3,3,1,1,3,3,3,3,3]},
                 depth = 2.435875,
                 tuningBehavior = '20150729a',
                 behavSession = '20150729a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-30_16-33-35',
                 tuningSession = '2015-07-30_16-14-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[9,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,3,3,2,1,2,1,1,1,2,2],3:[3,1,2,2,2,3,1,3,1,1,3,3],4:[3,1,1,2,2,2,1,2,1,1,2,0],5:[3,1,1,1,3,3,3,1,2,1,2,0],6:[3,2,1,2,1,1,1,1,1,1,2,0],7:[3,2,1,2,1,3,1,1,1,2,3,1],8:[3,2,2,1,3,3,3,1,1,1,3,3]},
                 depth = 2.435875,
                 tuningBehavior = '20150730c',
                 behavSession = '20150730a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-31_14-40-40',
                 tuningSession = '2015-07-31_14-27-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[9,0,0,0,0,0,0,0,0,0,0,0],2:[3,6,3,2,1,1,2,2,1,3,1,2],3:[3,1,3,3,2,3,1,1,1,1,3,1],4:[3,2,1,2,1,1,1,1,2,1,1,3],5:[3,1,2,3,2,3,2,3,1,1,1,1],6:[3,3,3,1,1,2,1,2,1,2,1,0],7:[3,1,6,1,2,1,1,3,3,1,1,3],8:[3,1,1,1,1,3,1,1,3,3,1,3]},
                 depth = 2.435875,
                 tuningBehavior = '20150731a',
                 behavSession = '20150731a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-01_13-35-46',
                 tuningSession = '2015-08-01_13-24-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,3,1,3,3,2,2,3,0],2:[3,2,1,1,1,2,3,1,2,3,2,0],3:[3,3,2,3,2,1,3,1,3,1,3,1],4:[3,1,1,3,3,3,1,1,3,2,0,0],5:[3,1,1,2,1,3,3,1,1,1,2,3],6:[3,3,2,1,2,3,1,3,1,2,1,1],7:[3,1,1,4,2,2,1,1,1,2,1,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.435875,
                 tuningBehavior = '20150801a',
                 behavSession = '20150801a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-03_16-12-32',
                 tuningSession = '2015-08-03_15-53-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,2,3,2,3,1,2,2,2,2],2:[3,3,2,3,3,3,3,1,1,1,3,0],3:[3,2,1,1,1,1,2,3,1,3,3,3],4:[3,1,3,1,3,1,2,3,1,4,3,0],5:[3,2,3,1,3,3,3,1,1,3,2,0],6:[3,3,3,2,3,3,1,2,3,1,1,0],7:[3,1,2,1,3,3,1,1,1,2,1,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.435875,
                 tuningBehavior = '20150803a',
                 behavSession = '20150803a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-04_11-21-11',
                 tuningSession = '2015-08-04_11-10-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,3,3,1,2,2,2,3,1,1],2:[3,2,1,3,3,1,3,1,2,1,2,2],3:[3,2,3,3,1,2,3,1,3,2,4,0],4:[3,1,1,1,2,3,3,1,1,3,2,0],5:[3,3,1,2,1,3,1,3,3,1,2,2],6:[3,1,1,2,1,3,2,2,1,3,1,1],7:[3,3,4,4,3,3,1,1,1,2,2,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.55475,
                 tuningBehavior = '20150804a',
                 behavSession = '20150804a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-05_16-44-02',
                 tuningSession = '2015-08-05_16-31-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,2,3,3,3,3,2,1,2,0],2:[3,2,1,2,1,1,2,1,1,2,2,1],3:[3,3,2,2,3,3,1,1,1,1,2,0],4:[3,3,1,1,1,3,3,2,1,2,3,1],5:[3,2,1,3,1,3,2,3,2,1,2,1],6:[3,3,1,2,1,1,1,2,2,2,3,1],7:[3,3,1,3,1,2,2,1,3,2,2,0],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.55475,
                 tuningBehavior = '20150805a',
                 behavSession = '20150805a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-06_13-29-50',
                 tuningSession = '2015-08-06_13-04-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,3,3,2,2,1,2,1,2,3],2:[9,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,2,4,1,3,1,1,3,2],4:[3,2,1,1,1,2,3,3,1,1,3,1],5:[3,1,1,3,1,2,2,2,3,2,1,0],6:[3,1,1,1,1,1,2,1,2,2,1,3],7:[3,1,6,2,3,1,1,3,3,1,1,2],8:[3,1,2,1,2,3,3,3,1,1,2,2]},
                 depth = 2.55475,
                 tuningBehavior = '20150806a',
                 behavSession = '20150806a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-07_16-05-00',
                 tuningSession = '2015-08-07_15-47-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[9,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,1,1,1,3,1,1,2,1,3,1],3:[3,3,1,1,1,1,2,2,1,2,1,3],4:[3,2,1,2,3,1,2,2,1,3,2,0],5:[3,3,3,3,2,1,1,2,1,3,3,3],6:[3,2,1,1,3,2,1,1,2,1,3,1],7:[3,6,1,3,3,3,2,3,1,6,2,3],8:[3,3,3,1,3,1,2,3,3,3,3,0]},
                 depth = 2.594375,
                 tuningBehavior = '20150807a',
                 behavSession = '20150807a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-10_15-17-29',
                 tuningSession = '2015-08-10_15-06-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,1,1,1,1,3,3,3,1],2:[3,3,2,1,3,1,1,3,2,1,1,1],3:[3,3,3,1,3,1,1,6,1,1,2,1],4:[3,2,1,6,2,2,2,1,2,2,2,2],5:[9,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,2,3,2,1,1,1,2,1,1,3],7:[3,1,1,3,3,3,3,2,2,3,3,2],8:[3,3,1,2,2,1,1,1,3,1,3,3]},
                 depth = 2.594375,
                 tuningBehavior = '20150810a',
                 behavSession = '20150810a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-11_11-14-14',
                 tuningSession = '2015-08-11_11-04-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,2,2,1,1,2,1,2,2,1],2:[3,1,3,1,3,3,1,1,1,4,1,2],3:[9,0,0,0,0,0,0,0,0,0,0,0],4:[3,2,1,1,3,1,1,2,1,2,2,2],5:[3,1,4,4,3,3,1,2,1,4,3,2],6:[3,1,2,2,3,3,1,1,2,1,1,2],7:[3,1,2,2,2,3,3,2,1,1,2,2],8:[3,1,2,2,3,2,1,2,3,1,3,1]},
                 depth = 2.634,
                 tuningBehavior = '20150811a',
                 behavSession = '20150811a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-12_23-22-12',
                 tuningSession = '2015-08-12_23-11-37',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,1,2,1,3,3,1,2,3,1],2:[3,2,3,1,1,1,3,1,3,1,3,1],3:[3,1,2,3,3,1,1,1,3,1,1,3],4:[3,1,1,2,1,1,3,1,2,3,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,2,1,2,1,3,1,1,3,1,3],7:[3,1,3,6,2,3,2,3,2,3,3,2],8:[3,3,1,3,3,2,1,2,1,1,3,3]},
                 depth = 2.634,
                 tuningBehavior = '20150812a',
                 behavSession = '20150812a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-13_16-59-59',
                 tuningSession = '2015-08-13_16-45-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,3,2,2,2,2,3,3],2:[3,1,1,1,2,2,1,1,1,3,1,1],3:[3,2,3,1,1,1,3,3,3,3,1,2],4:[3,1,2,1,1,1,1,2,2,3,1,0],5:[9,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,2,3,3,6,1,1,1,1,1,1],7:[3,2,2,6,2,3,1,2,2,4,6,1],8:[3,3,2,1,1,1,1,4,1,2,3,2]},
                 depth = 2.673625,
                 tuningBehavior = '20150813a',
                 behavSession = '20150813a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-14_13-12-32',
                 tuningSession = '2015-08-14_13-03-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,3,2,1,1,1,1,1,3,0],2:[3,1,1,1,2,3,1,1,2,1,1,1],3:[9,0,0,0,0,0,0,0,0,0,0,0],4:[3,1,2,2,2,1,3,3,1,2,2,1],5:[3,1,1,2,1,2,3,1,1,3,1,3],6:[3,1,2,1,1,1,2,1,1,1,1,4],7:[3,3,3,3,4,2,3,2,2,1,3,2],8:[3,3,3,4,2,2,3,1,1,1,2,1]},
                 depth = 2.673625,
                 tuningBehavior = '20150814b',
                 behavSession = '20150814a')
cellDB.append_session(oneES)

'''
#THIS SESSION DID NOT FINISH CLUSTERING PROPERLY
oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-17_15-22-05',
                 tuningSession = '2015-08-17_15-13-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 2.673625,
                 tuningBehavior = '20150817a',
                 behavSession = '20150817a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-18_17-32-48',
                 tuningSession = '2015-08-18_17-20-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,2,1,2,2,1,1,1,2,3],2:[3,1,1,1,1,1,1,1,1,2,1,3],3:[3,2,2,2,2,1,1,1,1,1,3,1],4:[3,1,1,2,6,6,1,1,2,6,2,6],5:[9,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,2,1,1,2,1,3,1,1],7:[3,2,2,2,2,6,2,3,2,2,1,0],8:[3,1,3,3,3,1,2,2,2,2,2,3]},
                 depth = 2.71325,
                 tuningBehavior = '20150818a',
                 behavSession = '20150818a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-19_12-53-30',
                 tuningSession = '2015-08-19_12-44-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,2,1,1,2,1,1,2,1,2],2:[3,1,1,1,1,2,1,1,1,1,1,1],3:[3,1,1,2,1,2,2,2,6,3,3,3],4:[3,6,6,1,2,1,6,1,2,2,1,0],5:[9,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,2,1,1,1,1,1,1,1,1,0],7:[3,1,3,1,2,2,2,2,1,2,2,0],8:[3,1,2,1,1,3,2,4,2,2,1,3]},
                 depth = 2.71325,
                 tuningBehavior = '20150819a',
                 behavSession = '20150819a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-20_12-51-26',
                 tuningSession = '2015-08-20_12-39-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,1,1,1,2,2,1,3,1],2:[3,2,1,2,1,1,2,3,1,1,1,4],3:[3,1,1,2,2,1,2,3,2,3,1,1],4:[3,6,3,6,1,2,2,6,3,4,1,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,1,1,1,1,1,3,2,1],7:[3,1,3,2,4,2,1,1,2,2,3,0],8:[3,1,2,1,3,2,1,2,1,2,2,2]},
                 depth = 2.71325,
                 tuningBehavior = '20150820a',
                 behavSession = '20150820a')
cellDB.append_session(oneES)
'''

#THIS SESSION IS NOT CLUSTERED
oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-21_16-54-19',
                 tuningSession = '2015-08-21_16-42-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 2.71325,
                 tuningBehavior = '20150821a',
                 behavSession = '20150821a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-27_11-56-32',
                 tuningSession = '2015-08-27_11-47-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,2,1,1,3,1,2,1,2,0],2:[3,1,1,1,1,1,2,1,1,1,1,1],3:[3,1,2,1,1,2,1,2,2,1,1,1],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,2,2,2,1,1,2,2,1,2,3],6:[3,1,1,1,1,2,1,1,1,2,1,1],7:[1,2,2,2,3,2,3,1,1,2,2,3],8:[3,1,2,2,3,2,2,1,2,1,3,0]},
                 depth = 2.71325,
                 tuningBehavior = '20150827a',
                 behavSession = '20150827a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-28_11-14-17',
                 tuningSession = '2015-08-28_11-04-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,1,1,1,1,3,1,2,2],2:[3,3,1,4,2,4,1,1,1,1,1,1],3:[3,1,1,3,2,1,2,2,1,1,1,3],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,3,2,3,3,2,1,1,1,1,3],6:[3,1,1,1,1,1,2,1,1,1,1,1],7:[3,1,2,2,2,2,1,3,2,2,2,2],8:[3,2,2,3,2,1,2,1,3,1,2,3]},
                 depth = 2.71325,
                 tuningBehavior = '20150828a',
                 behavSession = '20150828a')
cellDB.append_session(oneES)

'''
#THIS IS NOT CLUSTERED
oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-31_16-14-28',
                 tuningSession = '2015-08-31_15-59-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 2.752875,
                 tuningBehavior = '20150831a',
                 behavSession = '20150831a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-01_14-06-28',
                 tuningSession = '2015-09-01_13-56-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,2,2,3,1,1,2,2,1],2:[3,1,1,1,1,2,1,1,1,1,2,6],3:[3,1,1,3,2,1,1,2,1,1,3,0],4:[3,2,3,3,1,2,2,2,2,2,1,2],5:[9,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,1,1,1,1,1,2,1,1],7:[3,3,3,1,2,3,2,2,1,3,2,3],8:[3,2,3,2,1,1,3,2,3,2,2,3]},
                 depth = 2.752875,
                 tuningBehavior = '20150901a',
                 behavSession = '20150901a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-02_14-34-43',
                 tuningSession = '2015-09-02_14-25-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,2,1,2,2,2,1,1,1,2],2:[3,1,3,1,1,1,1,2,1,1,2,1],3:[3,1,2,3,2,2,1,1,1,2,1,0],4:[3,2,2,1,1,2,1,2,2,1,2,0],5:[9,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,2,1,1,2,1,1,3,1],7:[3,6,1,1,3,2,1,3,3,2,1,3],8:[3,3,1,2,3,3,3,3,1,1,1,6]},
                 depth = 2.7925,
                 tuningBehavior = '20150902a',
                 behavSession = '20150902a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-09_13-29-23',
                 tuningSession = '2015-09-09_13-19-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,1,2,1,3,1,1,2,1],2:[3,1,1,3,3,3,1,2,3,1,1,1],3:[3,2,2,1,1,1,1,1,3,3,1,3],4:[3,3,2,1,3,4,3,1,3,3,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,2,1,1,1,1,1,1,1],7:[3,4,4,3,3,1,3,3,3,3,3,1],8:[3,1,2,2,3,1,3,1,1,2,2,3]},
                 depth = 2.7925,
                 tuningBehavior = '20150909a',
                 behavSession = '20150909a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-10_12-37-41',
                 tuningSession = '2015-09-10_12-24-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,2,3,3,1,1,3,3,3,1],2:[3,3,3,1,1,3,2,1,1,3,1,3],3:[3,1,1,1,3,3,1,1,2,1,1,0],4:[3,3,1,3,1,3,2,3,2,3,3,2],5:[9,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,1,1,2,1,1,2,1,3,1],7:[3,3,2,3,6,3,3,1,3,3,3,3],8:[3,1,1,3,3,1,3,6,3,3,2,3]},
                 depth = 2.832125,
                 tuningBehavior = '20150910a',
                 behavSession = '20150910a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-11_12-33-17',
                 tuningSession = '2015-09-11_12-19-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,6,3,4,6,1,1,3,2,2,4],2:[3,3,1,1,3,2,1,1,4,1,1,4],3:[3,1,1,3,2,1,2,1,1,6,2,3],4:[3,2,2,2,1,1,1,2,2,3,2,3],5:[9,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,1,1,1,1,1,1,1,1],7:[3,3,1,3,4,3,1,3,1,2,3,3],8:[3,1,3,3,3,3,1,1,1,2,2,3]},
                 depth = 2.832125,
                 tuningBehavior = '20150911a',
                 behavSession = '20150911a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-13_16-00-43',
                 tuningSession = '2015-09-13_15-49-37',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,2,3,2,3],2:[3,3,2,3,1,1,2,3,3,3,3,0],3:[3,1,2,1,1,1,3,2,3,1,1,3],4:[3,2,2,3,2,3,1,3,2,3,1,3],5:[2,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,3,2,1,1,1,1,2,1,3],7:[3,3,3,1,3,3,2,3,3,3,3,3],8:[3,1,2,3,3,3,3,3,3,3,3,3]},
                 depth = 2.87175,
                 tuningBehavior = '20150913a',
                 behavSession = '20150913a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-14_18-02-42',
                 tuningSession = '2015-09-14_17-50-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,2,2,3,1,2,3,3,3,3],2:[3,3,6,1,2,3,1,3,1,1,3,2],3:[3,1,3,1,6,1,1,2,3,1,2,0],4:[3,2,2,1,2,1,3,1,2,2,2,0],5:[3,3,3,3,1,1,1,2,3,1,1,2],6:[3,1,1,1,1,1,1,1,1,1,1,1],7:[3,3,3,3,2,1,3,1,3,3,1,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.87175,
                 tuningBehavior = '20150914a',
                 behavSession = '20150914a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-15_12-41-17',
                 tuningSession = '2015-09-15_12-23-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,2,1,2,2,3,3,3,3,2],2:[3,1,2,2,3,3,1,1,1,1,2,3],3:[3,4,1,1,2,2,1,1,1,3,6,0],4:[3,2,1,2,3,1,2,1,2,3,6,1],5:[3,1,1,1,3,3,1,1,1,3,1,3],6:[3,1,1,1,1,1,2,1,1,1,1,1],7:[3,1,1,2,3,1,3,3,1,3,1,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.87175,
                 tuningBehavior = '20150915a',
                 behavSession = '20150915a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-17_14-19-06',
                 tuningSession = '2015-09-17_14-06-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,2,1,2,3,3,1,2,2,2],2:[3,2,2,2,2,2,3,2,2,2,1,2],3:[3,2,3,2,1,1,2,2,1,2,3,1],4:[3,3,2,2,3,2,2,2,2,2,2,2],5:[3,2,3,2,3,2,1,2,3,3,1,3],6:[3,2,1,2,1,2,3,1,1,1,2,1],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,2,1,2,3,2,3,3,2,6,2]},
                 depth = 2.911375,
                 tuningBehavior = '20150917c',
                 behavSession = '20150917a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-18_13-00-00',
                 tuningSession = '2015-09-18_12-50-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,1,1,2,3,1,3,3,1,1],2:[3,1,2,6,2,2,3,1,3,2,2,1],3:[3,1,2,1,1,1,2,1,1,1,1,1],4:[3,3,2,2,2,1,3,2,1,2,3,0],5:[3,3,3,2,3,1,3,1,1,3,1,3],6:[3,2,1,1,3,1,1,2,1,2,1,1],7:[3,1,2,2,1,4,3,1,1,2,3,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.911375,
                 tuningBehavior = '20150918a',
                 behavSession = '20150918a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-21_12-23-48',
                 tuningSession = '2015-09-21_12-08-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,1,3,3,3,3,3,3,3],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,3,3,1,3,3,3,3,3,3,3,3],4:[3,3,3,3,1,3,3,3,3,3,3,3],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,3,1,3,3,3,1,3,1,3,3,3],7:[3,3,3,3,3,3,3,3,3,3,1,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.911375,
                 tuningBehavior = '20150921a',
                 behavSession = '20150921a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-23_12-45-45',
                 tuningSession = '2015-09-23_12-32-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,3,2,3,2,3,3,3],2:[3,1,3,2,3,3,1,3,1,1,2,3],3:[3,1,1,1,1,1,2,1,2,2,1,2],4:[3,3,2,3,3,3,3,2,2,3,1,3],5:[3,1,1,1,3,3,2,3,2,1,3,3],6:[3,1,1,1,2,1,3,3,2,1,1,1],7:[3,3,3,1,3,1,1,3,1,1,3,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.911375,
                 tuningBehavior = '20150923a',
                 behavSession = '20150923a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-24_13-32-28',
                 tuningSession = '2015-09-24_13-23-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,2,1,3,1,3,1,2,1,3],2:[3,1,2,2,1,3,1,1,2,1,1,1],3:[3,2,2,2,1,2,1,1,1,4,1,1],4:[3,1,1,2,2,2,2,3,3,3,4,3],5:[3,3,3,3,3,2,2,3,1,1,2,1],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,1,2,2,1,2,1,3,1,2,2],8:[3,2,2,1,3,3,3,2,1,3,3,3]},
                 depth = 2.951,
                 tuningBehavior = '20150924a',
                 behavSession = '20150924a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-25_12-41-02',
                 tuningSession = '2015-09-25_12-30-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,1,3,3,3,3,3,3,3,3],2:[3,1,2,3,3,3,3,3,3,3,3,3],3:[3,1,2,3,3,1,2,3,2,3,3,3],4:[3,3,2,3,3,3,2,3,3,3,1,3],5:[3,3,3,3,3,3,2,3,2,3,3,3],6:[3,3,3,2,1,3,3,3,2,3,1,3],7:[3,3,3,3,1,3,3,3,3,3,3,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.951,
                 tuningBehavior = '20150925a',
                 behavSession = '20150925a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-10-08_13-51-27',
                 tuningSession = '2015-10-08_13-37-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,2,3,3,1,3,3,2,3,3],2:[3,3,3,1,2,3,3,3,2,3,2,3],3:[3,3,3,2,3,1,6,1,2,1,1,1],4:[3,3,2,3,3,3,3,3,3,3,3,3],5:[3,2,1,3,3,1,3,3,2,3,1,3],6:[3,3,3,3,1,2,3,1,3,1,3,1],7:[3,3,2,3,1,2,1,3,1,1,2,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.951,
                 tuningBehavior = '20151008a',
                 behavSession = '20151008a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-10-09_11-41-20',
                 tuningSession = '2015-10-09_11-25-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,1,3,3,3,6,1,3,3],2:[3,3,3,3,3,3,3,3,3,3,2,3],3:[3,3,1,3,3,6,1,3,1,3,3,3],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,3,2,3,1,3,3,1,3,0],6:[3,3,3,1,3,3,2,1,2,3,1,3],7:[3,3,3,2,3,3,1,1,1,3,3,3],8:[3,3,3,3,2,3,3,1,1,3,3,3]},
                 depth = 2.951,
                 tuningBehavior = '20151009a',
                 behavSession = '20151009a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-10-14_11-09-05',
                 tuningSession = '2015-10-14_11-00-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,2,3,2,3,3,3,3,3],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,3,3,3,3,3,2,3,3,3,3,1],4:[3,2,3,3,3,3,3,3,3,3,3,3],5:[3,3,3,3,3,3,3,3,3,3,3,2],6:[3,1,1,1,3,3,3,3,3,3,3,1],7:[3,4,3,3,3,3,1,3,3,3,1,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.951,
                 tuningBehavior = '20151014a',
                 behavSession = '20151014a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-02_11-20-25',
                 tuningSession = '2015-12-02_11-05-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,1,3,1,3,3,3,3],2:[3,3,3,1,1,3,3,1,1,3,2,3],3:[3,1,1,3,3,2,2,1,1,1,2,3],4:[3,3,2,1,3,1,1,3,1,3,3,2],5:[3,2,3,3,3,1,3,3,1,1,3,3],6:[3,1,1,1,3,1,1,2,2,3,2,3],7:[3,3,3,1,3,3,3,3,3,3,3,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 2.951,
                 tuningBehavior = '20151202a',
                 behavSession = '20151202a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-04_20-16-21',
                 tuningSession = '2015-12-04_20-07-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,3,3,3,1,3,3,3,2,3],2:[3,3,3,1,1,3,3,3,3,1,1,2],3:[3,3,1,1,3,1,3,3,3,3,1,1],4:[3,2,3,1,3,3,1,3,1,3,1,3],5:[3,3,3,3,1,1,3,3,3,2,3,1],6:[3,3,1,3,1,1,1,3,3,1,3,1],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,6,3,1,3,3,3,3,3,3,1,3]},
                 depth = 2.951,
                 tuningBehavior = '20151204a',
                 behavSession = '20151204a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-07_11-45-08',
                 tuningSession = '2015-12-07_11-36-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,1,3,1,3,3],2:[3,1,2,2,2,1,1,1,1,1,2,3],3:[3,3,2,3,3,1,1,3,3,2,1,2],4:[3,1,1,3,1,3,1,1,1,1,3,3],5:[3,6,1,1,3,6,3,3,3,3,1,1],6:[3,1,3,1,1,3,2,1,1,1,3,3],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,3,3,3,6,3,3,3,3,3,3]},
                 depth = 2.951,
                 tuningBehavior = '20151207a',
                 behavSession = '20151207a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-08_11-37-49',
                 tuningSession = '2015-12-08_11-29-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,3,1,3,3,1,3,1,3],2:[3,2,2,2,3,2,3,3,3,1,1,1],3:[3,3,3,3,1,3,2,3,2,3,3,0],4:[3,3,3,1,3,3,3,3,3,1,1,3],5:[3,3,1,1,3,6,1,2,3,3,1,6],6:[3,1,3,2,1,6,3,1,1,1,3,3],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,3,6,3,3,3,3,3,3,2,3]},
                 depth = 2.990625,
                 tuningBehavior = '20151208a',
                 behavSession = '20151208a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-09_11-22-28',
                 tuningSession = '2015-12-09_11-13-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,2,2,3,2,2,2,3,3,3],2:[9,0,0,0,0,0,0,0,0,0,0,0],3:[3,3,2,1,3,2,3,3,2,3,2,1],4:[3,4,1,2,1,1,3,3,3,3,1,3],5:[3,6,1,6,6,1,3,3,1,3,6,1],6:[3,6,1,3,6,1,1,1,2,3,6,3],7:[3,1,2,3,3,3,6,2,1,3,3,7],8:[3,3,2,3,3,3,3,6,3,3,3,3]},
                 depth = 3.03025,
                 tuningBehavior = '20151209a',
                 behavSession = '20151209a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-10_11-43-39',
                 tuningSession = '2015-12-10_11-34-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,6,6,2,1,6,6,3,3,3,3],3:[3,3,3,3,1,3,3,1,3,1,3,3],4:[3,4,2,1,3,1,3,2,3,1,3,2],5:[3,3,3,6,1,3,1,3,3,6,6,0],6:[3,1,6,1,1,6,2,1,1,3,3,0],7:[3,1,1,1,3,6,3,1,6,3,3,1],8:[3,3,6,3,3,3,3,3,3,3,3,3]},
                 depth = 3.069875,
                 tuningBehavior = '20151210a',
                 behavSession = '20151210a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-11_11-31-06',
                 tuningSession = '2015-12-11_11-22-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,6,6,6,3,3,6,6,3,6,6,3],3:[3,3,3,3,3,3,3,3,2,3,3,3],4:[3,1,1,1,3,2,1,3,2,1,3,2],5:[3,3,3,6,6,6,3,3,3,3,3,6],6:[3,3,1,3,6,3,6,3,3,2,1,1],7:[3,3,3,3,3,1,3,3,1,2,3,0],8:[3,3,3,3,3,3,1,3,3,3,3,0]},
                 depth = 3.1095,
                 tuningBehavior = '20151211a',
                 behavSession = '20151211a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-13_18-54-08',
                 tuningSession = '2015-12-13_18-44-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,6,6,3,6,3,6,6,6,3,3,3],3:[3,3,3,3,3,4,3,3,3,3,3,0],4:[3,3,3,1,1,1,2,3,3,3,3,3],5:[3,3,3,6,3,6,3,6,6,6,3,3],6:[3,3,3,6,6,6,6,3,6,6,3,6],7:[3,1,3,3,1,3,3,3,3,3,3,3],8:[3,3,3,3,4,3,3,3,1,3,3,3]},
                 depth = 3.149125,
                 tuningBehavior = '20151213a',
                 behavSession = '20151213a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-14_14-22-50',
                 tuningSession = '2015-12-14_14-11-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,3,3,3,3,3,3,3,1,3],2:[3,3,3,3,3,3,6,3,3,6,6,6],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,3,3,3,3,1,3,2,6,1,2],5:[3,3,6,6,6,6,6,3,3,3,3,3],6:[3,3,3,6,3,6,3,6,6,6,6,6],7:[3,3,3,3,3,3,1,3,3,3,3,3],8:[3,1,1,3,1,3,3,3,3,1,3,1]},
                 depth = 3.149125,
                 tuningBehavior = '20151214a',
                 behavSession = '20151214a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-15_16-29-48',
                 tuningSession = '2015-12-15_16-20-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,3,3,3],2:[3,6,3,3,3,3,2,3,3,3,6,3],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,3,3,1,3,3,3,3,3,3,3],5:[3,6,3,3,3,3,3,3,6,3,3,3],6:[3,6,6,3,3,3,3,6,6,3,3,2],7:[3,3,3,3,3,3,3,3,3,1,3,3],8:[3,3,3,3,3,3,3,3,1,3,4,3]},
                 depth = 3.18875,
                 tuningBehavior = '20151215a',
                 behavSession = '20151215a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-16_15-56-35',
                 tuningSession = '2015-12-16_15-47-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,1,3,3,3,3,3,4,3,3],2:[3,3,6,3,6,3,3,3,6,1,2,3],3:[3,3,0,0,0,0,0,0,0,0,0,0],4:[3,3,3,2,2,3,1,3,3,3,2,0],5:[3,3,3,1,3,3,3,3,6,6,3,1],6:[3,6,6,6,3,3,3,6,6,3,3,0],7:[3,3,3,3,6,3,3,3,1,3,2,3],8:[3,6,6,3,3,3,1,3,3,1,1,0]},
                 depth = 3.18875,
                 tuningBehavior = '20151216a',
                 behavSession = '20151216a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-17_14-16-40',
                 tuningSession = '2015-12-17_14-08-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,3,3,3,1,3,3,3,3],2:[3,2,2,2,6,2,3,6,3,3,3,3],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,1,2,1,3,2,3,2,6,3,3,2],5:[3,1,3,6,3,3,1,1,3,3,4,6],6:[6,3,3,6,3,1,2,2,6,3,6,0],7:[3,3,1,1,3,1,2,3,2,1,3,3],8:[3,3,4,3,1,6,3,6,3,3,3,3]},
                 depth = 3.18875,
                 tuningBehavior = '20151217a',
                 behavSession = '20151217a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-18_13-41-51',
                 tuningSession = '2015-12-18_13-33-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,2,3,2,3,3,3,3,2,3],2:[3,3,3,3,3,2,3,6,3,3,3,3],3:[3,3,3,3,3,3,3,3,3,2,3,3],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,3,1,2,1,3,1,1,3,3],6:[3,3,1,3,3,6,3,1,3,6,3,1],7:[3,2,3,3,1,3,3,3,3,3,3,3],8:[3,3,6,3,3,3,3,3,3,3,6,3]},
                 depth = 3.18875,
                 tuningBehavior = '20151218a',
                 behavSession = '20151218a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-21_12-45-50',
                 tuningSession = '2015-12-21_12-36-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,2,3,2,2,2,3,2,2],2:[3,2,3,2,1,2,2,6,3,2,1,3],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,3,1,2,2,2,2,2,3,3,3],5:[3,1,1,1,1,6,1,1,3,3,3,3],6:[6,6,1,3,3,2,3,1,1,2,1,0],7:[3,1,3,1,3,3,1,1,3,1,3,2],8:[3,3,3,3,6,6,2,1,3,3,3,2]},
                 depth = 3.18875,
                 tuningBehavior = '20151220a',
                 behavSession = '20151220a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-22_15-06-18',
                 tuningSession = '2015-12-22_14-57-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,6,3,2,2,3,2],2:[3,2,6,2,3,2,2,2,2,6,2,3],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,4,3,3,3,1,3,3,2,2,0],5:[3,1,1,3,1,1,6,1,3,1,3,3],6:[3,1,6,2,3,6,1,3,3,6,6,6],7:[3,3,2,2,1,3,1,1,3,2,2,1],8:[3,3,3,3,1,1,6,3,3,3,1,0]},
                 depth = 3.18875,
                 tuningBehavior = '20151222a',
                 behavSession = '20151222a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-23_14-22-34',
                 tuningSession = '2015-12-23_14-14-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,3,3,2,6,3,3,3,3],2:[3,1,3,3,1,2,1,3,1,3,3,2],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,1,1,1,2,2,3,1,3,3,4,2],5:[3,3,1,1,3,3,1,6,3,1,1,3],6:[3,2,3,6,3,3,6,1,2,1,1,1],7:[3,3,1,1,1,2,3,1,2,1,3,3],8:[3,3,6,3,1,3,3,1,3,1,3,6]},
                 depth = 3.18875,
                 tuningBehavior = '20151223a',
                 behavSession = '20151223a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-11_16-55-08',
                 tuningSession = '2016-01-11_16-44-37',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,3,2,2,3,3,3,6,3,6,2],2:[3,3,3,1,2,3,2,1,1,1,2,3],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,6,1,3,3,2,3,1,1,1,1,0],5:[3,3,3,3,3,3,3,3,3,2,3,3],6:[3,1,3,1,6,2,6,3,2,2,6,3],7:[3,3,3,3,3,1,1,3,3,1,3,3],8:[3,3,3,3,3,3,4,2,1,3,3,3]},
                 depth = 3.18875,
                 tuningBehavior = '20160111a',
                 behavSession = '20160111a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-12_13-52-50',
                 tuningSession = '2016-01-12_13-44-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,3,3,6,6,3,2,1,6,2,6],2:[3,2,3,2,6,3,1,2,2,3,1,0],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,1,2,1,3,6,1,3,3,1,2,6],5:[3,3,3,3,3,2,3,3,3,3,6,3],6:[3,3,3,3,1,3,2,1,6,6,6,0],7:[3,6,2,2,2,1,2,2,1,2,1,0],8:[3,3,3,3,2,3,3,3,2,3,1,3]},
                 depth = 3.18875,
                 tuningBehavior = '20160112a',
                 behavSession = '20160112a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-13_15-41-48',
                 tuningSession = '2016-01-13_15-33-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,2,3,3,3,3,3,3,3,3],2:[3,2,3,3,3,2,3,1,3,1,1,0],3:[3,2,3,3,3,3,3,3,3,3,3,3],4:[3,1,6,3,6,6,1,3,6,6,1,2],5:[3,3,3,3,3,3,2,3,3,6,3,3],6:[3,1,1,3,3,3,3,1,1,3,3,3],7:[3,2,1,1,3,3,3,3,3,1,1,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.228375,
                 tuningBehavior = '20160113a',
                 behavSession = '20160113a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-14_10-45-25',
                 tuningSession = '2016-01-14_10-35-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,6,3,3,3,3,2,3],2:[3,3,3,6,6,3,1,3,6,3,3,6],3:[3,3,3,3,3,3,3,3,3,3,3,4],4:[3,3,6,3,3,6,3,1,6,2,2,3],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,2,1,1,3,1,6,3,2,3,3,0],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,2,3,3,3,3,3,2,1,3,3]},
                 depth = 3.268,
                 tuningBehavior = '20160114a',
                 behavSession = '20160114a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-15_11-03-35',
                 tuningSession = '2016-01-15_10-52-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,3,3,3],2:[3,1,6,2,1,6,3,3,3,6,3,6],3:[3,2,2,2,2,2,3,3,2,3,6,3],4:[3,1,2,3,3,6,1,6,6,6,6,0],5:[3,3,3,3,3,3,0,0,0,0,0,0],6:[3,2,2,6,6,6,3,3,3,3,3,3],7:[3,1,2,2,2,3,3,6,2,3,3,3],8:[3,6,3,3,3,1,3,3,3,3,3,3]},
                 depth = 3.307625,
                 tuningBehavior = '20160115a',
                 behavSession = '20160115a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-16_15-12-13',
                 tuningSession = '2016-01-16_15-03-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,2,2,3,3,3,2,3,3,3],2:[3,1,3,3,6,3,6,6,7,3,2,6],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,1,3,6,2,6,6,3,3,3,3,3],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,6,3,3,3,3,2,3,3,3,3,0],7:[3,3,1,3,4,3,3,3,3,3,3,3],8:[3,3,3,3,3,3,6,6,2,3,2,0]},
                 depth = 3.34725,
                 tuningBehavior = '20160116a',
                 behavSession = '20160116a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-18_16-03-39',
                 tuningSession = '2016-01-18_15-55-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,2,6,3,3,1,3,6,1,3,1],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,3,3,3,3,6,3,3,3,4,3,3],5:[3,2,3,3,3,3,3,3,3,3,3,3],6:[3,3,3,1,3,3,6,3,3,3,3,2],7:[3,3,3,3,3,6,3,1,3,3,3,6],8:[3,6,3,1,2,6,6,3,3,3,6,3]},
                 depth = 3.34725,
                 tuningBehavior = '20160118a',
                 behavSession = '20160118a')
cellDB.append_session(oneES)

'''
#THIS SESSION DID NOT CLUSTER
oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-19_17-27-25',
                 tuningSession = '2016-01-19_17-18-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.34725,
                 tuningBehavior = '20160119a',
                 behavSession = '20160119a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-20_16-44-25',
                 tuningSession = '2016-01-20_16-35-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,3,3,6],2:[3,2,3,3,3,3,6,6,3,6,3,0],3:[3,3,3,3,3,3,3,2,2,3,2,2],4:[3,1,3,3,3,3,6,3,3,6,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,3,6,3,3,3,1,3,3,3],7:[3,3,3,1,1,3,3,1,3,3,1,3],8:[3,3,3,3,3,6,3,6,1,3,3,3]},
                 depth = 3.34725,
                 tuningBehavior = '20160120a',
                 behavSession = '20160120a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-21_14-03-15',
                 tuningSession = '2016-01-21_13-54-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,2,3,3,6,3,3,3,3,3,3],2:[3,1,3,3,6,3,3,6,2,3,6,3],3:[3,3,2,2,3,3,3,3,3,3,2,3],4:[3,3,6,6,3,6,3,2,3,3,6,6],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,2,6,3,3,6,3,3,3,3,6],7:[3,3,3,3,3,3,3,1,1,1,1,0],8:[3,3,3,1,3,3,3,3,3,2,3,3]},
                 depth = 3.34725,
                 tuningBehavior = '20160121a',
                 behavSession = '20160121a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-22_14-54-43',
                 tuningSession = '2016-01-22_14-46-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,6,3,3,3,2,3,3,3,3,3,3],2:[3,6,2,6,6,3,6,6,6,1,3,3],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,6,3,2,6,3,3,6,1,3,2,6],5:[3,3,3,3,3,3,3,1,3,3,2,0],6:[3,2,3,3,1,3,4,3,3,3,3,3],7:[3,1,1,1,1,3,2,3,1,3,3,0],8:[3,3,3,3,3,3,3,3,3,1,3,3]},
                 depth = 3.34725,
                 tuningBehavior = '20160122a',
                 behavSession = '20160122a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-23_16-18-45',
                 tuningSession = '2016-01-23_16-09-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,2,3,3,3],2:[3,3,6,3,3,1,3,6,2,3,6,3],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,3,1,2,6,3,6,2,2,2,3],5:[3,3,1,3,3,1,2,2,3,3,3,3],6:[3,3,2,6,3,2,3,2,3,3,2,6],7:[3,1,3,3,1,3,1,1,1,3,1,0],8:[3,3,3,3,3,3,3,1,2,1,2,3]},
                 depth = 3.386875,
                 tuningBehavior = '20160123a',
                 behavSession = '20160123a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-24_16-46-10',
                 tuningSession = '2016-01-24_16-37-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,2,3,3,3,3,3,3,2,2],2:[3,6,3,3,6,2,1,6,6,1,3,0],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,3,6,3,6,3,6,3,3,3,2],5:[3,3,3,3,3,3,3,2,3,2,3,3],6:[3,3,3,3,3,2,3,3,3,1,6,3],7:[3,1,1,2,3,1,3,1,1,3,3,1],8:[3,3,1,1,3,3,3,1,2,3,3,0]},
                 depth = 3.4265,
                 tuningBehavior = '20160124a',
                 behavSession = '20160124a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-25_15-03-55',
                 tuningSession = '2016-01-25_14-55-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,2,1,2,3,3,3,3],2:[3,2,6,3,2,3,2,3,1,6,3,3],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,6,6,4,3,3,3,3,3,3,3],5:[3,3,3,7,3,3,3,3,3,3,1,3],6:[3,1,2,3,3,3,3,3,3,2,3,3],7:[3,1,1,1,3,1,3,1,3,1,3,3],8:[3,3,3,1,3,3,1,3,6,3,3,0]},
                 depth = 3.4265,
                 tuningBehavior = '20160125a',
                 behavSession = '20160125a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-26_14-28-41',
                 tuningSession = '2016-01-26_14-20-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,2,3,3,3,3,3],2:[3,1,6,3,1,1,6,6,6,2,3,3],3:[2,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,3,3,1,3,6,6,3,6,2,2],5:[3,3,3,3,3,1,3,3,3,2,3,3],6:[3,6,2,3,3,3,1,2,6,3,3,3],7:[3,1,2,3,3,6,3,3,1,3,3,1],8:[3,3,3,3,3,3,1,3,3,3,1,3]},
                 depth = 3.466125,
                 tuningBehavior = '20160126a',
                 behavSession = '20160126a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-27_15-41-59',
                 tuningSession = '2016-01-27_15-33-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,3,3,3],2:[3,7,3,2,1,3,6,3,6,3,6,6],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,2,6,2,6,2,3,3,3,3,3,3],5:[3,3,3,3,4,3,3,3,3,3,3,3],6:[3,3,7,2,3,3,2,4,3,3,2,6],7:[3,3,3,1,1,1,3,1,4,3,3,1],8:[3,3,3,2,3,2,1,4,3,3,3,3]},
                 depth = 3.466125,
                 tuningBehavior = '20160127a',
                 behavSession = '20160127a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-28_14-23-09',
                 tuningSession = '2016-01-28_14-11-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,3,3,3,3,3,6,6,3,3],2:[3,1,3,1,2,3,1,3,6,3,3,0],3:[2,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,3,3,3,1,3,3,3,3,3,0],5:[3,1,3,3,3,3,3,3,3,3,2,3],6:[3,3,3,3,3,1,3,3,1,3,3,0],7:[3,3,3,3,1,2,1,1,1,1,3,3],8:[3,3,1,3,1,3,1,3,3,3,3,3]},
                 depth = 3.466125,
                 tuningBehavior = '20160128a',
                 behavSession = '20160128a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-29_12-07-45',
                 tuningSession = '2016-01-29_11-57-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,2,2,1,3,1,3,3,3,3],2:[3,3,3,3,3,3,1,1,3,1,1,1],3:[2,0,0,0,0,0,0,0,0,0,0,0],4:[3,1,2,1,2,1,3,1,3,6,2,2],5:[3,3,3,3,3,3,3,3,2,1,3,3],6:[3,3,2,3,3,3,3,3,2,3,6,3],7:[3,3,1,1,1,3,1,3,1,3,1,0],8:[3,2,1,2,1,3,3,3,2,3,1,0]},
                 depth = 3.50575,
                 tuningBehavior = '20160129a',
                 behavSession = '20160129a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-30_13-10-40',
                 tuningSession = '2016-01-30_13-01-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,3,3,3,3,3,3,1,3,1],2:[3,1,1,1,3,1,6,1,6,1,3,3],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,3,6,2,3,3,3,6,3,3,3],5:[3,3,6,2,3,3,3,1,3,3,3,6],6:[3,3,3,3,4,3,3,3,3,3,3,0],7:[3,1,3,3,6,2,3,1,1,1,2,2],8:[3,1,3,1,3,1,3,3,3,3,3,3]},
                 depth = 3.50575,
                 tuningBehavior = '20160130a',
                 behavSession = '20160130a')
cellDB.append_session(oneES)
'''
'''
oneES = eSession(animalName='test089',
                 ephysSession = '2016-02-01_13-53-07',
                 tuningSession = '2016-02-01_13-44-37',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
		 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,1,3,3,3,2,3,2,3,3,2],3:[3,1,2,3,2,2,3,3,3,3,1,6],4:[3,6,3,3,3,3,3,3,2,2,3,0],5:[3,3,3,2,2,3,1,3,2,3,2,3],6:[3,3,1,2,3,2,3,3,2,3,3,3],7:[3,1,1,2,3,3,3,2,1,2,1,1],8:[3,1,2,3,2,1,2,1,3,2,3,0]},
                 depth = 3.50575,
                 tuningBehavior = '20160201a',
                 behavSession = '20160201a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-02-02_10-53-55',
                 tuningSession = '2016-02-02_10-45-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
		 clusterQuality = {1:[3,2,3,3,1,3,2,3,3,1,1,3],2:[3,1,2,2,2,2,1,2,2,2,2,0],3:[2,0,0,0,0,0,0,0,0,0,0,0],4:[3,1,2,6,6,3,3,3,3,1,2,3],5:[3,3,3,2,2,3,1,3,2,1,2,0],6:[3,3,3,3,2,1,1,3,2,3,3,0],7:[3,1,1,2,2,2,2,1,1,1,2,2],8:[3,2,1,3,3,1,1,3,3,2,2,1]},
                 depth = 3.50575,
                 tuningBehavior = '20160202a',
                 behavSession = '20160202a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-02-03_11-39-32',
                 tuningSession = '2016-02-03_11-29-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
		 clusterQuality = {1:[3,1,1,1,1,1,1,1,1,3,1,1],2:[3,3,2,1,2,1,3,2,2,1,2,0],3:[2,0,0,0,0,0,0,0,0,0,0,0],4:[3,2,4,3,6,1,3,3,3,6,3,2],5:[3,3,2,2,3,3,1,3,2,1,3,3],6:[3,7,6,3,6,6,1,1,3,3,1,3],7:[1,1,2,2,1,1,1,1,3,3,2,1],8:[3,3,1,3,1,3,1,1,3,3,1,0]},
                 depth = 3.50575,
                 tuningBehavior = '20160203a',
                 behavSession = '20160203a')
cellDB.append_session(oneES)

'''

oneES = eSession(animalName='test089',
                 ephysSession = '2016-02-08_10-49-39',
                 tuningSession = '2016-02-08_10-38-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.50575,
                 tuningBehavior = '20160208a',
                 behavSession = '20160208a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-02-09_14-08-15',
                 tuningSession = '2016-02-09_13-59-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.50575,
                 tuningBehavior = '20160208a',
                 behavSession = '20160208a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-02-10_14-30-58',
                 tuningSession = '2016-02-10_14-22-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.50575,
                 tuningBehavior = '20160210a',
                 behavSession = '20160210a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-02-15_11-29-46',
                 tuningSession = '2016-02-15_11-20-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.50575,
                 tuningBehavior = '20160215a',
                 behavSession = '20160215a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-02-16_10-31-15',
                 tuningSession = '2016-02-16_10-21-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.545375,
                 tuningBehavior = '20160216a',
                 behavSession = '20160216a')
cellDB.append_session(oneES)
'''
