'''
List of all isolated units from adap012, with cluster quality added.
Lan Guo 2016-02-03
'''
#using CellDatabase that contains laserSession for evaluating laser responsiveness

from jaratoolbox.test.lan.Ephys import celldatabase_quality_vlan as celldatabase
reload(celldatabase)


eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-03_13-13-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160203a',
                 clusterQuality = {1:[3,1,4,2,1,4,4,2,3,4,3,2],2:[3,4,4,3,3,4,4,4,4,4,2,1],3:[3,2,1,1,4,1,1,4,1,3,1,4],4:[3,3,4,4,4,4,4,4,4,3,4,3],5:[3,4,4,4,4,4,4,2,4,3,4,4],6:[3,3,4,3,4,4,4,1,3,3,0,0],7:[3,3,4,4,4,1,1,1,4,4,3,4],8:[3,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-04_12-41-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160204a',
                 clusterQuality = {1:[3,3,1,3,4,2,4,3,3,1,1,3],2:[3,3,3,2,3,4,1,3,3,4,3,1],3:[3,1,1,1,1,3,1,2,1,1,4,1],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,1,2,2,3,1,1,1,3,4],6:[3,3,1,3,3,1,3,3,3,1,4,1],7:[3,1,1,3,2,3,1,2,3,3,3,1],8:[3,1,3,3,3,1,3,3,2,3,3,3]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-05_13-14-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160205a',
                 clusterQuality = {1:[3,2,1,4,1,1,2,3,3,4,4,3],2:[3,3,3,4,4,4,2,4,3,4,4,3],3:[3,2,1,4,1,4,3,4,1,4,3,4],4:[3,3,2,3,1,3,2,4,2,1,1,4],5:[3,4,4,1,4,4,3,3,4,3,4,4],6:[3,1,4,3,4,1,1,3,1,4,4,3],7:[3,4,2,2,4,1,1,4,1,3,3,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-06_14-45-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160206a',
                 clusterQuality = {1:[3,4,1,4,2,1,1,3,3,1,1,4],2:[3,3,4,3,4,3,3,2,4,4,1,0],3:[3,1,3,1,1,1,4,4,1,3,4,0],4:[3,1,4,1,2,1,2,4,4,4,4,3],5:[3,1,4,4,2,3,4,4,4,3,4,4],6:[3,4,1,3,1,3,4,1,1,1,4,0],7:[3,3,2,4,3,4,4,2,1,2,4,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-07_15-23-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160207a',
                 clusterQuality = {1:[3,4,4,1,2,3,2,1,1,4,4,1],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,4,1,1,1,1,3,4,4,1,1,4],4:[3,1,1,2,3,1,1,1,4,1,4,4],5:[3,2,4,4,2,4,4,2,1,3,1,4],6:[3,1,3,4,1,1,1,4,1,1,1,4],7:[3,4,1,1,4,4,3,1,4,1,1,3],8:[3,1,3,4,4,4,3,3,4,1,1,3]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-08_12-05-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160208a',
                 trialLimit=[0,1321],
                 clusterQuality = {1:[3,4,2,4,2,4,7,4,4,4,7,4],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,1,2,1,4,1,1,2,4,4,1],4:[3,1,1,4,2,4,2,1,1,4,1,1],5:[3,2,2,4,1,4,1,1,2,2,2,1],6:[3,1,1,1,1,1,1,1,1,1,1,1],7:[3,2,2,2,2,2,1,1,3,1,1,3],8:[3,1,4,1,1,2,2,1,3,1,1,1]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-09_13-05-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160209a',
                 clusterQuality = {1:[3,2,4,1,4,4,7,2,4,2,1,4],2:[9,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,4,1,1,4,1,1,1,1,0],4:[3,2,4,2,1,2,1,4,1,1,1,1],5:[3,2,2,1,2,2,4,3,3,4,1,2],6:[3,1,3,2,6,6,1,1,6,6,4,1],7:[3,2,1,3,4,1,1,2,2,3,2,0],8:[3,4,4,2,1,2,1,4,3,3,1,2]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-10_13-40-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160210a',
                 clusterQuality = {1:[3,3,2,4,2,2,4,4,2,3,2,2],2:[3,4,4,2,2,3,4,3,1,4,1,1],3:[3,2,3,2,4,1,1,2,1,1,4,1],4:[3,1,1,1,1,1,1,1,1,1,1,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,6,2,1,1,7,1,1,6,1,4,0],7:[3,4,4,1,1,2,3,4,1,1,1,0],8:[3,1,4,2,3,3,4,4,4,4,1,3]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-11_10-09-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160211a',
                 clusterQuality = {1:[4,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,1,1,1,1,2,2,4,4,2,1],3:[3,1,1,1,2,1,1,1,3,1,1,2],4:[3,1,2,1,1,1,2,1,3,2,2,1],5:[3,3,1,2,2,3,2,2,2,2,2,4],6:[3,1,1,1,1,6,6,1,6,1,2,2],7:[3,2,2,3,2,1,4,1,3,1,1,0],8:[3,2,1,1,3,3,1,1,3,4,2,0]}) #behav num of trials > ephys num of trials
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-12_11-45-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160212a',
                 clusterQuality = {1:[3,4,4,7,2,2,1,1,1,4,1,4],2:[9,0,0,0,0,0,0,0,0,0,0,0],3:[3,4,1,1,1,1,1,1,1,4,2,0],4:[3,1,1,1,1,1,1,1,1,1,1,1],5:[3,2,4,1,1,1,1,1,4,4,4,2],6:[3,1,4,4,1,4,1,3,6,1,1,1],7:[3,1,1,1,4,1,1,1,1,1,4,1],8:[3,4,4,3,1,3,2,1,1,1,4,4]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-13_16-08-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160213a',
                 clusterQuality = {1:[3,1,1,1,2,3,1,1,1,1,4,4],2:[3,2,2,1,4,4,4,2,3,1,4,1],3:[3,4,4,1,1,1,1,1,1,3,1,1],4:[3,1,1,1,1,1,1,1,1,1,1,1],5:[3,2,4,4,4,4,2,4,4,4,4,2],6:[3,1,4,1,1,1,1,4,1,1,1,4],7:[3,1,1,1,1,4,1,4,1,1,1,1],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-15_12-28-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160215a',
                 clusterQuality = {1:[3,1,1,2,1,3,1,2,2,2,4,4],2:[3,2,2,2,4,2,2,3,4,2,4,2],3:[3,2,1,2,1,1,1,2,4,1,2,4],4:[3,4,2,4,1,1,2,2,4,1,1,0],5:[3,2,4,4,1,4,4,1,2,2,4,1],6:[3,2,1,1,1,4,1,4,4,4,1,1],7:[3,1,4,1,1,4,1,1,1,1,4,4],8:[1,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-16_13-55-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160216a',
                 clusterQuality = {1:[3,1,1,2,1,2,3,4,1,1,1,0],2:[3,4,2,2,4,1,2,2,3,2,1,1],3:[3,2,1,1,1,1,1,1,1,2,1,1],4:[3,1,1,4,1,1,2,4,1,1,2,2],5:[3,4,2,4,1,1,1,1,1,4,1,2],6:[3,1,1,1,4,1,1,4,1,1,1,1],7:[3,1,1,1,1,1,1,1,1,1,1,0],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-17_12-52-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160217a',
                 clusterQuality = {1:[3,4,2,2,2,1,1,1,3,2,2,1],2:[3,4,3,2,2,3,2,1,1,1,2,2],3:[3,2,1,1,1,2,1,1,1,1,1,1],4:[3,1,1,1,1,1,1,1,1,2,1,1],5:[3,1,1,1,4,1,4,2,2,1,1,3],6:[3,4,4,2,2,4,4,1,1,4,3,4],7:[3,1,1,1,1,2,1,4,1,1,1,0],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
#behav trials more than ephys, not plotted
cellDB.append_session(oneES)

oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-18_13-04-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160218a',
                 trialLimit=[0,986],
                 clusterQuality = {1:[3,1,4,3,1,2,2,1,2,1,4,3],2:[3,4,4,2,4,3,2,1,4,2,2,2],3:[3,2,3,1,1,1,1,1,1,2,1,1],4:[3,1,4,4,2,1,1,1,1,1,1,4],5:[3,2,1,4,4,2,4,4,1,1,1,4],6:[3,1,1,4,1,1,4,1,1,1,1,1],7:[3,1,4,1,4,1,4,4,2,1,4,4],8:[4,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-20_15-02-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160220a',
                 clusterQuality = {1:[3,1,1,2,2,1,1,2,1,1,2,0],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,2,1,1,1,1,1],4:[3,2,1,1,1,1,1,1,4,1,2,0],5:[3,1,1,4,2,1,1,1,1,2,1,1],6:[3,1,1,1,4,4,1,1,4,1,4,0],7:[3,4,4,1,1,3,2,1,1,1,1,4],8:[3,1,1,3,1,2,2,2,1,2,3,1]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-21_14-27-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160221a',
                 trialLimit=[0,1061],
                 clusterQuality = {1:[3,1,1,2,1,2,4,1,2,2,2,1],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,4,1,1,2,1,1,1],4:[3,1,1,1,1,1,1,1,1,1,1,7],5:[3,1,1,1,1,1,2,1,1,2,1,1],6:[3,1,1,1,1,1,1,1,1,1,1,0],7:[3,1,1,1,1,3,1,1,2,2,2,3],8:[3,1,2,3,2,3,1,2,2,2,1,2]})
cellDB.append_session(oneES)
#trialLimit=[0,1061]


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-22_16-04-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160222a',
                 clusterQuality = {1:[3,1,4,1,4,1,1,2,1,1,2,1],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,2,1,1,1],4:[3,2,1,1,1,1,1,1,1,1,2,1],5:[3,1,1,1,1,3,2,2,2,2,4,1],6:[3,3,1,1,1,2,4,1,1,1,2,4],7:[3,1,1,1,1,4,1,1,3,2,4,2],8:[3,2,2,3,1,2,2,2,2,4,3,1]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-02-25_14-07-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160225a',
                 trialLimit=[0,914],
                 clusterQuality = {1:[3,1,3,1,1,2,2,1,1,2,1,1],2:[3,2,3,2,2,4,3,2,2,2,1,2],3:[3,1,1,1,1,1,1,1,1,1,1,1],4:[3,1,1,1,1,1,1,2,1,1,1,1],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,6,6,1,1,1,4,6,1,1],7:[3,1,1,1,1,1,4,1,1,1,1,1],8:[3,1,4,2,2,2,1,2,1,2,3,1]})
cellDB.append_session(oneES)
#trialLimit=[0,914]

oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-01_13-56-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160301a',
                 trialLimit=[0,1142],
                 clusterQuality = {1:[3,2,1,1,1,3,1,1,2,7,2,1],2:[2,2,3,4,4,2,2,4,4,3,2,0],3:[3,2,4,1,1,1,1,1,1,1,3,2],4:[3,1,2,1,1,1,4,3,2,2,2,1],5:[3,3,2,2,6,3,4,2,4,4,2,4],6:[3,1,3,4,1,1,1,2,1,4,2,3],7:[3,1,1,1,4,1,1,2,1,2,2,2],8:[2,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)
#trialLimit=[1142]

oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-02_15-27-46',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160302a',
                 clusterQuality = {1:[3,2,3,2,4,4,2,4,3,1,4,0],2:[2,3,4,3,2,3,2,2,3,2,2,2],3:[3,3,2,1,2,1,1,2,1,4,3,1],4:[3,1,4,2,3,2,1,2,1,1,1,1],5:[3,6,4,2,1,3,2,6,2,3,2,4],6:[3,4,2,3,2,4,4,1,1,4,4,0],7:[3,1,4,1,1,1,2,4,4,3,2,4],8:[3,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-04_15-23-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160304a',
                 trialLimit=[0,1359],
                 clusterQuality = {1:[3,2,4,3,3,2,2,1,3,4,2,4],2:[9,0,0,0,0,0,0,0,0,0,0,0],3:[3,4,3,1,2,1,4,1,4,1,1,3],4:[3,6,4,4,1,1,3,1,1,1,2,1],5:[3,4,6,1,1,1,1,3,3,4,4,7],6:[3,4,4,3,4,2,1,4,7,7,7,7],7:[3,1,4,1,4,3,3,4,1,4,1,4],8:[3,3,3,3,3,3,3,1,4,3,3,2]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-07_12-31-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160307a',
                 trialLimit=[0,1145],
                 clusterQuality = {1:[3,1,2,1,1,1,1,2,1,4,1,2],2:[9,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,4,1,1,4,1,1,2,1,1,1],4:[3,1,1,1,1,1,1,1,1,1,1,1],5:[3,6,6,6,6,2,1,1,1,2,2,0],6:[3,1,1,1,1,1,1,1,1,1,1,1],7:[3,2,1,2,1,1,1,2,4,1,1,0],8:[3,2,3,3,1,3,3,2,3,2,1,4]})
cellDB.append_session(oneES)
#trialLimit=[0,1145]

oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-08_13-29-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160308a',
                 trialLimit=[0,1137],
                 clusterQuality = {1:[3,1,1,1,1,4,1,3,1,2,1,1],2:[3,3,3,1,1,3,3,3,3,2,2,2],3:[3,1,1,1,3,1,1,1,1,4,1,2],4:[3,1,1,2,1,1,1,1,4,1,1,1],5:[3,1,3,1,1,1,7,2,1,1,2,4],6:[3,2,1,1,1,1,1,4,1,1,4,1],7:[3,1,1,1,4,1,1,4,1,1,1,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)
#trialLimit=[0,1137]

oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-09_14-04-44',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160309a',
                 clusterQuality = {1:[3,1,1,1,2,1,2,1,2,1,2,1],2:[9,0,0,0,0,0,0,0,0,0,0,0],3:[3,6,6,1,6,2,6,1,2,1,6,1],4:[3,1,2,2,1,1,4,1,1,1,2,1],5:[3,1,2,1,3,4,5,1,2,1,1,0],6:[3,1,6,1,1,2,3,2,1,1,4,2],7:[3,4,4,1,4,4,4,1,1,1,3,2],8:[3,3,3,5,2,4,2,3,1,2,4,4]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-11_13-37-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160311a',
                 clusterQuality = {1:[3,4,3,1,1,4,1,2,1,4,4,1],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,3,2,2,2,1,1,1,1],4:[3,1,1,1,1,1,1,1,1,1,1,0],5:[3,1,4,2,4,3,7,4,1,1,4,3],6:[3,1,1,4,1,1,4,4,4,4,1,4],7:[3,4,3,1,1,2,4,4,4,4,1,0],8:[3,6,6,3,6,6,2,6,4,3,3,2]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-15_13-26-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160315a',
                 clusterQuality = {1:[3,1,4,1,1,1,1,2,2,1,4,0],2:[9,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,2,1,4,1,4,2,1,0],4:[3,1,1,1,1,1,1,1,1,1,1,1],5:[3,3,2,1,1,2,1,1,2,2,6,2],6:[3,2,4,1,4,4,1,1,1,4,4,2],7:[3,2,1,1,1,1,1,2,4,4,4,0],8:[3,2,5,2,3,2,1,2,2,3,4,3]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-16_12-51-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160316a',
                 trialLimit=[0,1423],
                 clusterQuality = {1:[3,2,3,1,1,1,1,1,1,1,1,1],2:[3,1,2,1,1,3,2,1,2,3,2,0],3:[3,1,1,1,2,1,4,1,4,4,1,2],4:[3,1,4,1,1,1,1,1,1,1,4,1],5:[3,4,1,4,6,2,4,2,3,1,4,2],6:[3,1,1,4,1,4,1,4,1,1,4,1],7:[3,1,1,1,4,4,1,1,1,1,1,1],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-17_14-43-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160317a',
                 clusterQuality = {1:[3,1,4,1,1,1,3,1,1,1,1,4],2:[3,3,1,2,3,1,4,2,4,1,1,0],3:[3,3,1,1,1,1,1,4,2,1,1,2],4:[3,4,4,1,4,1,1,1,1,1,1,1],5:[3,6,1,1,2,4,7,6,4,4,2,4],6:[3,2,1,1,1,1,1,1,2,4,1,0],7:[3,1,1,2,2,1,1,1,1,1,1,0],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-18_13-26-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160318a',
                 clusterQuality = {1:[3,1,2,1,1,3,1,1,1,1,6,2],2:[3,3,4,1,2,1,4,3,2,2,1,2],3:[3,1,1,1,4,1,3,1,1,1,2,1],4:[3,2,4,1,1,1,1,4,1,1,1,6],5:[3,6,2,1,4,2,2,2,2,4,2,0],6:[3,1,1,1,1,1,7,1,1,1,1,6],7:[3,4,1,1,1,1,1,4,1,1,1,1],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-21_13-43-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160321a',
                 trialLimit=[0,1051],
                 clusterQuality = {1:[3,1,1,1,3,4,1,1,4,1,1,1],2:[3,4,4,3,1,2,1,1,4,1,1,3],3:[3,2,4,4,1,4,6,4,2,2,3,4],4:[3,2,1,4,1,1,1,1,1,1,1,1],5:[3,4,4,4,4,2,2,1,2,2,4,4],6:[3,1,4,4,1,4,1,6,1,2,1,1],7:[3,1,1,4,4,1,1,1,2,1,1,1],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)



oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-22_13-07-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160322a',
                 clusterQuality = {1:[3,1,1,4,4,1,1,3,1,1,1,1],2:[3,1,2,3,1,1,1,1,2,3,2,3],3:[3,3,2,1,1,7,7,2,1,6,2,1],4:[3,4,1,1,2,2,1,1,1,1,1,1],5:[3,2,3,2,4,1,3,2,4,1,2,1],6:[3,1,4,1,1,4,6,1,6,4,1,4],7:[3,1,1,1,4,1,1,1,1,1,1,1],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-23_12-57-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160323a',
                 clusterQuality = {1:[3,1,2,4,1,3,4,1,1,4,3,1],2:[3,4,4,2,3,4,1,4,4,4,4,4],3:[3,3,4,2,4,1,7,4,4,4,4,1],4:[3,2,1,1,1,1,1,1,1,1,1,1],5:[3,4,4,4,2,1,2,4,4,4,2,2],6:[3,4,6,6,1,4,4,1,4,1,1,1],7:[3,1,2,4,4,1,2,4,1,1,4,1],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-24_14-01-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160324a',
                 clusterQuality = {1:[3,1,4,4,1,3,2,4,2,1,1,0],2:[3,4,2,4,7,4,3,3,3,7,3,4],3:[3,4,4,3,4,1,1,3,7,2,2,4],4:[3,1,1,2,4,3,1,6,4,6,4,4],5:[3,1,4,1,4,4,4,4,3,2,4,0],6:[3,4,4,1,4,6,4,4,6,3,4,1],7:[3,1,1,4,1,1,1,1,4,1,4,4],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-28_13-05-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160328a',
                 clusterQuality = {1:[3,1,1,1,1,4,2,4,1,1,4,0],2:[3,2,4,4,4,1,2,2,2,2,2,3],3:[3,4,1,2,2,4,1,2,2,3,4,4],4:[3,4,4,4,4,2,4,4,4,1,2,4],5:[3,1,2,2,2,2,2,4,4,1,2,2],6:[3,1,1,4,4,1,4,4,1,1,1,6],7:[3,1,4,1,1,1,4,4,1,4,1,0],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)



oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-29_14-07-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160329a',
                 clusterQuality = {1:[3,4,2,2,4,4,2,2,2,3,2,2],2:[3,6,3,1,2,2,2,6,2,6,2,2],3:[3,4,4,4,1,1,1,4,4,4,1,4],4:[3,2,4,2,4,4,4,4,4,2,1,2],5:[3,2,2,4,2,4,4,4,1,2,4,4],6:[3,4,1,1,4,4,1,4,6,7,6,3],7:[3,4,2,4,4,1,1,1,1,1,2,1],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-03-31_13-16-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160331a',
                 clusterQuality = {1:[3,4,2,2,4,4,2,4,2,3,4,4],2:[3,2,1,1,1,4,1,1,3,4,1,1],3:[3,4,4,1,5,4,4,4,4,4,5,1],4:[3,2,2,4,2,1,4,4,2,4,4,4],5:[3,4,2,4,4,7,2,6,4,4,2,1],6:[3,1,6,1,1,4,2,1,6,4,4,1],7:[3,1,1,1,1,4,1,1,1,1,4,1],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-04-04_15-19-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160404a',
                 clusterQuality = {1:[3,1,1,1,1,1,1,2,3,4,4,1],2:[3,4,4,1,1,2,4,2,4,6,1,1],3:[3,4,4,4,3,4,4,1,1,4,1,3],4:[3,1,6,4,1,6,2,1,7,6,4,1],5:[3,2,7,2,7,2,2,2,2,2,2,2],6:[3,1,4,4,4,1,1,4,4,4,4,3],7:[3,1,4,4,1,4,1,1,1,1,4,4],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap012',
                 ephysSession = '2016-04-05_12-43-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160405a',
                 trialLimit=[0,1520],
                 clusterQuality = {1:[3,2,1,4,7,3,2,4,7,6,4,1],2:[3,2,2,2,1,4,1,1,1,2,4,1],3:[3,1,4,4,4,1,3,1,4,1,1,1],4:[3,7,1,1,4,4,4,4,1,1,3,7],5:[3,4,4,4,4,4,4,4,3,7,4,4],6:[3,2,4,1,1,1,1,6,6,4,1,1],7:[3,4,1,4,1,4,1,1,1,1,4,1],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)
