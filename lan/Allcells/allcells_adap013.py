'''
List of all isolated units from adap013, with cluster quality added.
Lan Guo 2016-03-21
'''
#using CellDatabase that contains laserSession for evaluating laser responsiveness

from jaratoolbox.test.lan.Ephys import celldatabase_quality_vlan as celldatabase
reload(celldatabase)


eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-11_15-23-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160211a',
                 clusterQuality = {1:[3,2,3,2,3,2,2,2,3,2,2,2],2:[3,4,4,3,2,4,2,2,4,2,4,0],3:[3,2,3,2,4,2,2,2,2,4,4,4],4:[3,3,2,2,2,2,2,2,2,2,3,4],5:[3,3,3,2,2,2,4,0,0,0,0,0],6:[3,2,2,2,2,2,4,2,4,2,3,2],7:[3,3,2,3,2,2,2,2,2,2,2,2],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)

'''
oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-22_12-44-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160222a',
                 clusterQuality = {1:[3,2,4,3,2,2,2,2,2,2,4,4],2:[3,4,1,2,2,2,2,2,2,2,3,0],3:[3,4,4,2,2,2,3,4,2,2,2,0],4:[3,2,4,4,4,2,3,2,2,2,2,0],5:[3,2,4,2,4,2,2,2,4,4,2,4],6:[3,3,2,2,3,2,2,2,3,2,2,4],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,1,1,2,2,2,2,2,2,4,3,2]})
#cellDB.append_session(oneES)
#start in 'same_reward' and because automation mode is 'left-right-left', stuck in same_reward block for the entire session
'''

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-24_10-27-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160224a',
                 clusterQuality = {1:[3,1,2,4,4,2,4,2,2,3,2,0],2:[3,3,1,4,2,2,1,2,4,0,0,0],3:[3,2,2,4,3,2,2,3,2,4,1,0],4:[3,2,3,3,4,1,2,2,2,3,2,2],5:[3,2,3,1,1,1,3,2,1,2,4,1],6:[3,2,2,4,2,2,2,2,3,2,2,3],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,2,2,2,2,2,3,1,2,0]})
cellDB.append_session(oneES)



oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-26_10-59-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160226a',
                 trialLimit=[0,460],
                 clusterQuality = {1:[3,3,1,2,3,2,3,2,2,3,2,3],2:[3,1,4,2,1,1,2,4,3,1,1,0],3:[3,3,4,2,3,2,2,3,2,2,1,1],4:[3,3,3,2,1,2,2,3,2,1,4,0],5:[3,3,3,2,2,1,1,3,2,0,0,0],6:[3,2,3,2,1,2,2,2,2,2,3,2],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,3,2,2,4,1,2,2,2,2,0]})
cellDB.append_session(oneES)



oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-28_15-44-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160228a',
                 clusterQuality = {1:[3,2,3,7,2,1,3,3,2,4,2,3],2:[3,4,1,1,1,4,1,3,1,1,2,0],3:[3,2,2,4,3,4,4,3,3,3,4,3],4:[3,1,1,2,2,4,2,3,2,1,3,3],5:[3,1,3,4,4,3,2,4,3,0,0,0],6:[3,2,2,3,7,2,2,3,2,3,2,2],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,2,2,7,3,2,2,2,2,3,2]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-01_11-43-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160301a',
                 clusterQuality = {1:[3,1,2,3,2,3,2,2,2,2,3,2],2:[3,1,1,1,1,1,3,1,1,1,0,0],3:[3,3,2,2,4,4,2,1,2,2,3,2],4:[3,1,2,2,1,1,2,1,2,1,3,0],5:[3,1,1,3,1,1,1,1,3,0,0,0],6:[3,2,2,2,7,6,2,2,2,2,2,2],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,1,1,2,4,2,2,7,2,1]})
cellDB.append_session(oneES)

'''
oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-02_14-29-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160302a',
                 clusterQuality = {1:[3,3,3,3,2,3,3,2,3,4,4,2],2:[3,1,1,1,4,4,4,4,1,2,0,0],3:[3,2,2,4,3,4,2,4,2,4,2,1],4:[3,3,4,2,4,4,4,1,2,1,4,2],5:[3,1,1,1,1,4,4,2,3,3,1,4],6:[3,4,2,2,3,2,2,2,3,2,4,0],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,6,4,4,4,4,1,2,2,2,3,2]})
#cellDB.append_session(oneES)
#start in 'same_reward' and because automation mode is 'left-right-left', stuck in same_reward block for the entire session
'''

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-16_13-57-37',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160316a',
                 clusterQuality = {1:[3,4,4,2,2,2,4,4,5,1,4,0],2:[3,1,1,1,4,1,1,1,1,1,4,0],3:[3,2,2,2,2,2,2,1,2,1,2,1],4:[3,4,2,1,3,2,2,1,2,2,4,0],5:[3,4,1,1,1,1,1,1,1,0,0,0],6:[3,2,2,2,2,2,1,2,2,1,2,1],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[4,1,1,1,2,7,1,1,1,4,1,0]})
cellDB.append_session(oneES)



oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-18_13-36-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160318a',
                 clusterQuality = {1:[3,3,2,3,2,2,4,2,4,2,2,2],2:[3,1,1,1,1,1,1,1,1,1,1,0],3:[3,3,3,2,2,2,1,2,2,2,2,2],4:[3,2,1,2,3,2,2,2,1,1,1,1],5:[3,1,3,1,1,1,1,1,1,3,1,1],6:[3,2,2,3,2,2,2,1,1,2,2,2],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,1,1,2,4,2,1,1,2,4,1]})
cellDB.append_session(oneES)



oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-20_14-10-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160320a',
                 clusterQuality = {1:[3,1,4,2,2,1,2,2,4,2,2,0],2:[3,1,1,1,1,1,1,1,1,1,0,0],3:[3,3,3,1,2,1,2,2,2,2,4,2],4:[3,2,2,2,2,1,1,3,1,4,1,0],5:[3,1,1,1,4,4,4,1,4,1,0,0],6:[3,2,2,3,3,1,2,2,1,1,2,0],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,1,2,1,1,1,1,1,1,1,1,1]})
cellDB.append_session(oneES)



oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-21_15-33-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160321a',
                 trialLimit=[0,530],
                 clusterQuality = {1:[3,2,1,4,1,4,1,4,1,2,3,2],2:[3,4,1,1,1,1,1,1,1,1,1,0],3:[3,2,2,2,4,2,3,4,2,2,2,3],4:[3,2,1,1,1,4,1,6,4,2,6,3],5:[3,1,1,1,1,1,1,1,1,1,1,1],6:[3,1,2,2,2,1,2,2,2,4,4,0],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,1,1,1,1,1,6,1,1,1,2,2]})
cellDB.append_session(oneES)


'''
oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-23_14-27-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160323a',
                 trialLimit=[],
                 clusterQuality = {1:[3,4,3,2,4,2,4,4,4,1,4,1],2:[3,1,1,2,1,1,1,2,1,1,1,0],3:[3,3,3,2,2,3,3,4,2,2,4,2],4:[3,4,7,6,3,2,7,4,4,4,2,0],5:[3,4,1,4,1,1,1,1,1,1,1,0],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,4,4,4,1,2,2,3,2,2,2,3],8:[3,2,4,2,4,4,2,2,2,4,4,4]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-28_13-57-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160328a',
                 trialLimit=[],
                 clusterQuality = {1:[3,],2:[3,],3:[3,],4:[3,],5:[3,],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,],8:[3,]})
#cellDB.append_session(oneES)


oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-30_13-58-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160330a',
                 trialLimit=[],
                 clusterQuality = {1:[3,1,1,3,1,4,2,3,2,3,1,3],2:[3,1,1,1,1,1,1,1,1,1,1,4],3:[3,3,3,3,2,2,2,2,2,3,2,0],4:[3,2,1,2,1,1,1,4,3,3,1,0],5:[3,4,1,1,1,1,7,1,1,1,1,4],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,2,1,1,3,2,2,2,1,4,4],8:[3,1,1,1,1,2,1,1,2,1,2,2]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-01_15-06-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160401a',
                 trialLimit=[],
                 clusterQuality = {1:[3,3,3,2,4,4,2,1,3,1,4,1],2:[3,1,1,2,1,1,1,1,1,1,2,2],3:[3,2,2,3,2,2,2,2,2,2,3,0],4:[3,3,1,4,2,2,1,2,1,1,4,1],5:[3,1,1,7,1,1,1,1,2,1,1,0],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,4,2,2,3,3,1,3,3,4,2,2],8:[3,3,2,2,7,6,2,2,1,2,2,2]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-05_14-27-44',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160405a',
                 trialLimit=[],
                 clusterQuality = {1:[9,0,0,0,0,0,0,0,0,0,0,0],2:[3,1,1,2,1,2,1,1,1,1,4,1],3:[3,2,2,2,2,2,2,3,2,2,2,2],4:[3,2,2,2,2,2,1,3,2,2,2,3],5:[3,6,2,4,4,1,1,4,1,2,1,2],6:[3,3,3,1,2,7,2,2,2,7,3,2],7:[3,2,2,3,2,3,2,3,2,1,3,3],8:[3,1,3,1,2,3,2,2,2,2,2,0]})
cellDB.append_session(oneES)



oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-7_14-34-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160407a',
                 trialLimit=[],
                 clusterQuality = {1:[3,],2:[3,],3:[3,],4:[3,],5:[3,],6:[3,],7:[9,],8:[3,]})
#cellDB.append_session(oneES)
'''
