'''
List of all isolated units from adap015, with cluster quality added.
Lan Guo 2016-03-25
'''
#using CellDatabase that contains laserSession for evaluating laser responsiveness

from jaratoolbox.test.lan.Ephys import celldatabase_quality_vlan as celldatabase
reload(celldatabase)


eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-04_15-41-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160204a',
                 clusterQuality = {1:[3,4,2,4,4,3,3,2,1,4,4,4],2:[3,1,3,2,1,2,6,2,6,6,2,0],3:[3,1,1,1,4,1,1,1,3,0,0,0],4:[3,2,2,1,1,2,4,4,1,1,1,0],5:[3,4,2,2,3,2,2,2,4,2,2,3],6:[3,7,1,2,2,2,2,2,2,2,3,7],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,2,2,2,2,2,2,1,2,4]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-07_15-27-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160207a',
                 trialLimit=[0,854],
                 clusterQuality = {1:[3,4,4,4,4,4,1,2,4,3,0,0],2:[3,3,2,3,3,4,2,2,2,2,4,0],3:[3,2,2,1,3,4,4,4,2,1,1,1],4:[3,1,1,1,2,1,1,1,1,1,1,4],5:[3,2,4,2,4,4,2,2,2,3,2,2],6:[3,2,2,7,1,2,2,1,1,2,3,7],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,2,1,2,4,2,1,6,2,2]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-11_17-18-34',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160211a',
                 trialLimit=[0,598],
                 clusterQuality = {1:[3,2,3,2,4,4,4,4,4,4,4,0],2:[3,2,3,3,6,4,6,2,2,2,2,3],3:[3,4,4,4,2,1,4,6,4,4,1,0],4:[3,2,1,7,6,1,1,2,2,6,1,1],5:[9,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,1,4,1,4,2,1,2,1,1,4],7:[3,2,2,4,4,4,4,4,4,4,3,2],8:[3,3,2,2,2,2,2,2,2,2,2,2]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-15_15-40-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160215a',
                 clusterQuality = {1:[3,2,2,4,2,4,1,4,4,2,3,0],2:[3,1,2,2,6,2,2,1,4,2,3,2],3:[3,4,4,1,4,1,6,2,1,1,1,0],4:[3,4,3,4,2,4,1,4,4,4,1,4],5:[3,2,2,2,2,3,2,2,2,2,3,2],6:[3,3,6,4,6,7,4,6,2,2,6,6],7:[3,2,2,2,2,2,2,3,7,2,2,2],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
cellDB.append_session(oneES)
#TT6c3&5 may be same cell, each cluster active half of the session, same for TT6c11&12 

'''
oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-17_16-15-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160217a',
                 clusterQuality = {1:[3,1,1,3,1,2,2,2,3,1,2,2],2:[3,6,6,6,2,3,2,2,6,2,3,2],3:[3,1,1,1,1,1,1,1,1,1,2,2],4:[3,2,2,1,2,2,1,3,4,2,1,3],5:[3,2,3,1,2,1,4,1,4,2,2,2],6:[3,2,2,6,3,2,3,2,6,4,2,6],7:[3,2,4,1,2,2,2,4,4,4,2,2],8:[9,0,0,0,0,0,0,0,0,0,0,0]})
#cellDB.append_session(oneES)
#start in 'same_reward' and because automation mode is 'left-right-left', stuck in same_reward block for the entire session
'''

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-19_10-42-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160219a',
                 clusterQuality = {1:[3,2,2,2,2,2,2,4,2,2,2,4],2:[3,6,1,2,3,2,6,6,2,6,6,2],3:[3,1,1,1,7,1,1,4,1,4,2,1],4:[3,4,1,4,6,3,4,2,2,2,1,0],5:[3,3,6,4,3,4,2,3,2,2,3,2],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,2,2,3,2,3,4,4,2,7,2],8:[3,4,2,3,4,1,2,2,6,2,7,7]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-22_17-55-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160222a',
                 clusterQuality = {1:[3,4,6,7,4,2,3,2,4,3,1,2],2:[3,2,2,3,3,3,3,2,3,2,2,3],3:[3,3,1,1,2,4,1,1,1,4,4,1],4:[3,2,2,4,2,2,3,2,2,2,1,3],5:[3,1,2,3,3,1,2,2,3,1,3,2],6:[3,7,6,6,2,2,6,3,3,3,3,2],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,1,3,2,2,2,2,3,1,3,2]})
cellDB.append_session(oneES)
#TT6c3&4 may be same cell, each cluster active half of the session


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-24_17-21-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160224a',
                 trialLimit=[0,776],
                 clusterQuality = {1:[3,7,3,2,4,2,2,2,3,2,7,2],2:[3,2,3,2,2,2,2,2,2,1,3,2],3:[3,2,3,2,1,7,7,7,2,1,2,7],4:[3,2,2,2,3,1,1,1,2,4,2,2],5:[3,3,3,1,2,2,1,2,3,2,2,3],6:[3,2,1,2,2,1,3,3,1,4,2,4],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,1,2,2,2,2,2,1,2,2,1]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-17_11-13-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160317a',
                 clusterQuality = {1:[3,3,2,3,3,3,3,3,3,3,3,3],2:[3,3,3,3,3,3,3,4,3,4,3,0],3:[3,3,3,3,2,3,3,3,3,2,7,3],4:[3,3,3,3,3,3,3,3,3,2,3,3],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,3,3,3,2,3,3,3,3,7,3],8:[3,3,3,3,3,3,3,3,3,4,3,3]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-18_10-49-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160318a',
                 clusterQuality = {1:[3,2,3,2,3,4,3,4,4,3,1,3],2:[3,3,3,3,3,4,3,1,3,3,3,3],3:[3,7,7,3,3,3,3,6,6,2,2,2],4:[3,3,3,4,3,1,3,3,3,3,4,2],5:[3,3,3,3,2,2,2,3,3,3,2,0],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,7,7,4,3,2,2,4,2,3,3],8:[3,7,4,7,4,3,2,4,2,2,3,0]})
cellDB.append_session(oneES)


'''
oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-25_17-13-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160225a',
                 clusterQuality = {1:[3,3,2,1,2,4,2,2,2,3,2,3],2:[3,4,1,2,3,2,2,2,2,2,2,3],3:[3,1,1,7,6,6,1,1,2,1,3,6],4:[3,1,4,4,1,3,1,1,2,4,4,2],5:[3,2,3,2,7,2,1,1,3,3,5,4],6:[3,4,3,3,3,3,2,2,3,3,2,2],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,2,2,3,2,1,3,1,4,2]})
cellDB.append_session(oneES)
#behav length 1100 ephys length 1099 not corrected by remove_missing_trials

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-29_15-55-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160229a',
                 clusterQuality = {1:[3,2,3,2,2,2,1,3,3,2,4,3],2:[3,2,1,3,3,2,2,2,2,4,4,3],3:[3,1,1,1,4,4,2,1,1,2,7,4],4:[3,4,3,1,2,3,1,1,2,2,2,0],5:[9,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,3,2,2,2,3,3,3,2,3],7:[3,2,2,6,3,3,3,2,1,2,3,2],8:[3,3,2,2,2,3,3,3,7,1,2,2]})
#cellDB.append_session(oneES)
#start in 'same_reward' and because automation mode is 'left-right-left', stuck in same_reward block for the entire session


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-01_14-12-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160301a',
                 clusterQuality = {1:[3,2,2,2,3,1,2,1,1,1,2,3],2:[3,3,7,2,2,2,2,2,7,2,2,2],3:[3,3,2,2,2,3,1,1,1,2,2,1],4:[3,1,4,3,1,3,2,1,1,2,1,0],5:[3,2,3,3,2,3,3,2,3,2,2,0],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,2,3,2,7,2,1,2,2,4,0],8:[3,2,3,2,2,3,2,1,2,2,2,3]})
#cellDB.append_session(oneES)
#start in 'same_reward' and because automation mode is 'left-right-left', stuck in same_reward block for the entire session
'''
