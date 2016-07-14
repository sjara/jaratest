'''
List of all isolated units from one animal

Victoria did adap015


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

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-05_14-33-42',
                 tuningSession = '2016-02-05_14-25-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,1,1,1,1,2,1,1,0],2:[3,2,2,2,2,2,2,1,1,1,2,2],3:[3,2,1,1,1,1,1,1,3,1,1,1],4:[3,1,1,1,1,3,1,1,4,1,2,1],5:[3,2,3,2,2,2,2,3,2,3,2,3],6:[3,2,2,2,1,2,1,3,2,1,2,2],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,1,2,2,2,2,1,2,2,2,2,2]},
                 depth = 3.03025,
                 tuningBehavior = '20160205a',
                 behavSession = '20160205a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-06_16-49-55',
                 tuningSession = '2016-02-06_16-41-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,1,1,1,1,2,1,2,3],2:[3,3,3,3,2,3,2,2,2,2,2,2],3:[3,2,2,3,1,2,2,2,2,1,1,3],4:[3,5,1,5,1,1,2,1,1,5,1,3],5:[3,3,3,3,1,2,3,3,2,2,2,0],6:[3,1,2,2,1,2,3,2,2,1,7,6],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,1,2,2,2,2,2,2,2,2,2,2]},
                 depth = 3.069875,
                 tuningBehavior = '20160206a',
                 behavSession = '20160206a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-08_19-18-04',
                 tuningSession = '2016-02-08_19-09-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,4,1,2,1,3,3,2,2],2:[3,2,2,3,2,2,3,2,3,3,3,3],3:[3,3,3,2,1,1,1,2,2,1,2,1],4:[3,1,2,2,5,1,1,6,6,1,1,1],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,1,1,3,6,1,1,2,3,2,2],7:[3,2,3,3,3,2,3,2,3,2,2,3],8:[3,1,1,2,2,2,2,2,2,3,2,0]},
                 depth = 3.1095,
                 tuningBehavior = '20160208a',
                 behavSession = '20160208a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-09_16-32-35',
                 tuningSession = '2016-02-09_16-17-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[]},
                 depth = 3.1095,
                 tuningBehavior = '20160209a',
                 behavSession = '20160209a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-10_16-21-25',
                 tuningSession = '2016-02-10_16-12-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,2,4,4,3,2,3,3,3,0],2:[3,2,2,2,3,3,2,2,2,3,2,3],3:[3,1,1,1,2,7,1,3,1,4,7,1],4:[3,1,1,1,1,1,1,2,1,5,5,1],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,1,3,3,2,3,4,2,3,2,1],7:[3,2,2,2,3,2,3,3,2,2,2,2],8:[3,2,2,2,2,3,2,1,2,2,2,1]},
                 depth = 3.149125,
                 tuningBehavior = '20160210a',
                 behavSession = '20160210a')
cellDB.append_session(oneES)
'''
#THIS SESSION DOESNT CLUSTER PROPERLY
oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-12_09-50-06',
                 tuningSession = '2016-02-12_09-41-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,2,3,2,3,3,2,3,3,2],2:[3,2,2,2,2,2,2,2,2,3,2,2],3:[3,1,3,1,1,2,1,1,2,1,1,1],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[0,0,0,0,0,0,0,0,0,0,0,0],6:[0,0,0,0,0,0,0,0,0,0,0,0],7:[0,0,0,0,0,0,0,0,0,0,0,0],8:[0,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.18875,
                 tuningBehavior = '20160212a',
                 behavSession = '20160212a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-16_14-16-04',
                 tuningSession = '2016-02-16_14-07-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,2,3,1,5,1,4,2,4],2:[3,2,1,1,1,2,3,2,2,3,2,2],3:[3,1,1,2,3,1,1,1,1,1,1,0],4:[3,1,1,4,2,2,1,4,3,2,1,1],5:[3,3,4,2,3,2,3,2,2,2,2,3],6:[3,5,6,2,2,3,3,6,5,6,2,2],7:[3,2,2,2,2,3,2,2,3,2,2,2],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.228375,
                 tuningBehavior = '20160216a',
                 behavSession = '20160216a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-18_14-53-11',
                 tuningSession = '2016-02-18_14-44-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,2,1,3,2,2,3,2,3,2],2:[3,2,2,2,2,2,2,3,2,3,2,2],3:[3,1,1,1,1,1,1,1,3,1,3,1],4:[3,3,3,1,2,1,2,1,1,1,1,4],5:[3,3,3,3,3,3,3,3,2,2,3,0],6:[3,2,3,3,2,2,2,3,3,3,3,2],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,2,4,2,6,3,2,3,6,2]},
                 depth = 3.268,
                 tuningBehavior = '20160218a',
                 behavSession = '20160218a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-23_14-12-34',
                 tuningSession = '2016-02-23_14-03-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,1,3,3,3,2,3,3,3,0],2:[3,3,3,3,3,3,3,2,3,3,3,3],3:[3,2,3,3,3,1,6,2,3,1,1,3],4:[3,2,3,3,3,2,2,2,2,1,2,1],5:[3,2,2,2,1,3,2,3,3,3,3,3],6:[3,2,2,3,1,3,3,3,3,2,3,3],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,1,3,3,1,2,2,1,3,3,2,3]},
                 depth = 3.307625,
                 tuningBehavior = '20160223a',
                 behavSession = '20160223a')
cellDB.append_session(oneES)

'''
#THE EPHYS AND BEHAVIOR DONT LINE UP. NOT SURE WHY THIS DOESNT RUN PROPERLY IN PLOT_MODINDEX
oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-03_14-27-14',
                 tuningSession = '2016-03-03_14-12-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,2,3,2,1,1,2,2,3,2],2:[3,2,3,2,3,3,2,3,3,1,2,3],3:[3,2,2,1,1,1,4,1,3,3,2,2],4:[3,2,2,1,2,1,1,1,3,3,3,1],5:[3,2,2,2,2,3,2,3,3,2,2,3],6:[3,3,3,3,3,2,2,3,3,3,3,2],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,2,2,2,3,2,2,2,2,1,2]},
                 depth = 3.34725,
                 tuningBehavior = '20160303a',
                 behavSession = '20160303a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-16_10-04-37',
                 tuningSession = '2016-03-16_09-55-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,3,3,3,2,3,2,3,3,3],2:[3,1,3,3,2,2,3,3,3,3,3,3],3:[3,3,4,3,3,2,3,4,1,1,2,3],4:[3,3,2,1,2,4,3,3,3,3,2,3],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,3,3,3,3,2,3,2,3,3,3],8:[3,1,3,4,2,1,3,3,2,3,4,5]},
                 depth = 3.34725,
                 tuningBehavior = '20160316a',
                 behavSession = '20160316a')
cellDB.append_session(oneES)
