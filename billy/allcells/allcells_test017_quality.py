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

from jaratoolbox import celldatabase_quality_tuning as celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


'''
THESE WERE NOT DONE BECAUSE THE BEHAVIOR WAS NOT GOOD ENOUGH
oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-17_12-26-10',
                 tuningSession = '2015-02-17_12-03-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 2.1585,
                 tuningBehavior = '20150217a',
                 behavSession = '20150217a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-21_20-08-51',
                 tuningSession = '2015-02-21_20-01-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.1095,
                 tuningBehavior = '20150221a',
                 behavSession = '20150221a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-23_15-31-40',
                 tuningSession = '2015-02-23_15-16-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.268,
                 tuningBehavior = '20150223b',
                 behavSession = '20150223a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-25_14-04-30',
                 tuningSession = '2015-02-25_13-54-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.4265,
                 tuningBehavior = '20150225a',
                 behavSession = '20150225a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-26_16-31-05',
                 tuningSession = '2015-02-26_16-08-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,1,2,3,3,3,2,1,2,3],2:[3,3,3,1,1,3,1,1,3,1,2,3],3:[3,3,3,3,3,2,1,3,3,3,3,3],4:[3,3,3,2,2,1,1,1,3,3,3,2],5:[3,2,2,2,2,3,1,3,3,3,1,3],6:[3,1,2,1,1,1,1,1,2,1,3,1],7:[3,3,6,3,3,3,6,2,2,2,3,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.4265,
                 tuningBehavior = '20150226a',
                 behavSession = '20150226a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-27_14-55-39',
                 tuningSession = '2015-02-27_14-43-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,6,2,3,6,3,2,2,3,2,3],2:[3,1,1,3,3,3,1,3,3,3,2,3],3:[3,3,2,3,2,3,3,3,3,3,3,3],4:[3,3,3,2,3,2,1,2,2,1,3,3],5:[3,3,3,3,3,2,2,2,2,3,2,1],6:[3,6,6,6,1,6,2,1,6,3,3,0],7:[2,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,3,3,3,3,3,3,3,2,3,3]},
                 depth = 3.50575,
                 tuningBehavior = '20150227a',
                 behavSession = '20150227a')
cellDB.append_session(oneES)
'''
THESE WERE NOT DONE BECAUSE THE BEHAVIOR WAS NOT GOOD ENOUGH
oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-28_20-10-50',
                 tuningSession = '2015-02-28_20-01-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.585,
                 tuningBehavior = '20150228a',
                 behavSession = '20150228a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-01_18-37-39',
                 tuningSession = '2015-03-01_15-20-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.585,
                 tuningBehavior = '20150302b',
                 behavSession = '20150302a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-02_15-32-56',
                 tuningSession = '2015-03-02_15-04-46',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.585,
                 tuningBehavior = '20150302a',
                 behavSession = '20150302a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-03_18-44-50',
                 tuningSession = '2015-03-03_17-34-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.585,
                 tuningBehavior = '20150303c',
                 behavSession = '20150303a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-04_14-56-53',
                 tuningSession = '2015-03-04_14-45-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.585,
                 tuningBehavior = '20150304b',
                 behavSession = '20150304a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-05_15-48-15',
                 tuningSession = '2015-03-05_15-27-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.585,
                 tuningBehavior = '20150305a',
                 behavSession = '20150305a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-06_14-12-25',
                 tuningSession = '2015-03-06_14-01-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.624625,
                 tuningBehavior = '20150306b',
                 behavSession = '20150306a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-09_16-51-45',
                 tuningSession = '2015-03-09_16-41-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,2,1,6,3,2,3,1,3,3],2:[3,3,3,2,2,2,2,3,1,3,1,1],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,3,1,2,2,1,2,3,1,2,1,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,1,3,3,2,6,3,3,2,1,1],7:[3,3,2,2,3,3,3,3,3,2,1,2],8:[3,2,3,2,3,3,3,3,3,2,3,3]},
                 depth = 3.624625,
                 tuningBehavior = '20150309a',
                 behavSession = '20150309a')
cellDB.append_session(oneES)
'''
THESE WERE NOT DONE BECAUSE THE BEHAVIOR WAS NOT GOOD ENOUGH
oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-10_16-21-40',
                 tuningSession = '2015-03-10_16-08-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.66425,
                 tuningBehavior = '20150310b',
                 behavSession = '20150310a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-11_14-48-20',
                 tuningSession = '2015-03-11_14-39-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,2,1,6,6,3,1,2,2],2:[3,3,3,2,1,1,3,3,3,3,3,1],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[2,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,3,3,3,3,3,3,3,1,3],6:[3,1,3,1,3,1,1,2,2,1,1,1],7:[3,2,2,3,3,1,3,3,3,3,3,3],8:[3,2,2,2,2,2,2,4,3,4,3,3]},
                 depth = 3.66425,
                 tuningBehavior = '20150311a',
                 behavSession = '20150311a')
cellDB.append_session(oneES)
'''
THESE WERE NOT DONE BECAUSE THE BEHAVIOR WAS NOT GOOD ENOUGH
oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-12_15-10-08',
                 tuningSession = '2015-03-12_14-53-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.703875,
                 tuningBehavior = '20150312a',
                 behavSession = '20150312a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-13_13-28-00',
                 tuningSession = '2015-03-13_13-10-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,4,1,2,1,2,3,1,3,1,1],2:[3,3,3,3,3,3,3,3,1,3,1,3],3:[3,3,3,3,3,3,3,2,3,3,3,3],4:[3,3,2,2,2,2,3,2,2,2,2,2],5:[3,3,3,6,3,2,3,3,3,2,3,3],6:[3,1,1,1,1,1,3,1,2,1,1,1],7:[3,1,3,1,6,3,1,3,3,3,1,2],8:[2,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.703875,
                 tuningBehavior = '20150313a',
                 behavSession = '20150313a')
cellDB.append_session(oneES)
'''
THESE WERE NOT DONE BECAUSE THE BEHAVIOR WAS NOT GOOD ENOUGH
oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-15_14-33-42',
                 tuningSession = '2015-03-15_14-24-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.7435,
                 tuningBehavior = '20150315a',
                 behavSession = '20150315a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-16_17-21-11',
                 tuningSession = '2015-03-16_17-09-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,1,1,3,3,1,6,1,2,1],2:[3,3,1,6,6,1,3,1,3,2,1,1],3:[3,3,3,3,3,3,3,3,3,3,3,0],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,3,3,2,3,3,1,3,3,0],6:[3,3,1,3,1,2,1,3,3,1,3,1],7:[3,3,3,6,2,3,2,2,1,1,3,3],8:[3,3,3,2,3,3,3,3,3,1,3,2]},
                 depth = 3.783125,
                 tuningBehavior = '20150316a',
                 behavSession = '20150316a')
cellDB.append_session(oneES)
'''
THESE WERE NOT DONE BECAUSE THE BEHAVIOR WAS NOT GOOD ENOUGH
oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-17_14-21-17',
                 tuningSession = '2015-03-17_14-12-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.82275,
                 tuningBehavior = '20150317b',
                 behavSession = '20150317a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-18_17-16-40',
                 tuningSession = '2015-03-18_17-05-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.82275,
                 tuningBehavior = '20150318a',
                 behavSession = '20150318a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-19_13-35-17',
                 tuningSession = '2015-03-19_13-23-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.862375,
                 tuningBehavior = '20150319a',
                 behavSession = '20150319a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-20_13-05-06',
                 tuningSession = '2015-03-20_12-55-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.862375,
                 tuningBehavior = '20150320a',
                 behavSession = '20150320a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-21_14-06-46',
                 tuningSession = '2015-03-21_13-56-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.862375,
                 tuningBehavior = '20150321b',
                 behavSession = '20150321a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-22_20-31-12',
                 tuningSession = '2015-03-22_20-20-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.902,
                 tuningBehavior = '20150322a',
                 behavSession = '20150322a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-23_16-27-01',
                 tuningSession = '2015-03-23_16-13-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.902,
                 tuningBehavior = '20150323a',
                 behavSession = '20150323a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-24_16-25-09',
                 tuningSession = '2015-03-24_16-14-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.902,
                 tuningBehavior = '20150324a',
                 behavSession = '20150324a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-25_15-43-55',
                 tuningSession = '2015-03-25_14-17-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.902,
                 tuningBehavior = '20150325a',
                 behavSession = '20150325a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-26_15-20-29',
                 tuningSession = '2015-03-26_15-10-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.902,
                 tuningBehavior = '20150326a',
                 behavSession = '20150326a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-27_14-41-56',
                 tuningSession = '2015-03-27_14-32-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.902,
                 tuningBehavior = '20150327a',
                 behavSession = '20150327a')
cellDB.append_session(oneES)
'''
