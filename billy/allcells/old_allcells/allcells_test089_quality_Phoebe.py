'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase_quality as celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-27_15-41-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160127a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-26_14-28-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160126a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-25_15-03-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160125a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-24_16-46-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160124a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-23_16-18-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160123a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-22_14-54-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160122a')
cellDB.append_session(oneES)

#this session has a skipped trial at trial 684
oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-21_14-03-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160121a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-20_16-44-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160120a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-19_17-27-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160119a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-18_16-03-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
		 clusterQuality = {1:[2,0,0,0,0,0,0,0,0,0,0,0],2:[3,4,4,4,2,4,1,1,2,6,3,3],3:[3,1,1,3,2,5,2,2,4,2,3,2],4:[
                 behavSession = '20160118a')
cellDB.append_session(oneES)

cellDB = celldatabase.CellDatabase()

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-16_15-12-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
		 clusterQuality = {1:[3,2,3,3,2,2,2,2,2,4,4,4],2:[3,7,4,4,6,2,6,2,2,3,4,7],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,4,7,2,2,2,7,7,4,4,4,1],5:[3,2,3,2,3,5,4,4,1,2,2,3],6:[3,4,4,4,4,4,4,2,3,2,2,3],7:[3,1,4,4,4,2,4,1,3,2,1,3],8:[3,2,1,4,4,4,1,4,2,4,3,2]},
                 behavSession = '20160116a')
cellDB.append_session(oneES)

cellDB = celldatabase.CellDatabase()

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-15_11-03-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
		 clusterQuality = {1:[3,3,1,1,4,4,1,3,2,2,3,3],2:[3,2,1,2,1,1,6,1,1,3,2,1],3:[3,2,2,7,2,3,1,1,2,2,2,1],4:[3,4,3,1,1,6,6,6,1,3,3,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,3,6,3,1,2,1,1,3,6,6],7:[3,3,3,2,2,1,3,6,1,1,3,0],8:[3,1,1,1,4,2,3,2,1,3,2,3]},
                 behavSession = '20160115a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-14_10-45-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
		 clusterQuality = {1:[3,4,2,3,3,3,3,3,4,2,4,4],2:[3,6,2,3,2,2,4,2,3,1,3,2],3:[3,4,2,4,3,3,4,4,2,4,3,3],4:[3,2,2,2,4,1,6,4,1,6,2,4],5:[3,3,3,3,4,4,2,4,3,4,4,4],6:[3,2,4,1,1,3,4,1,3,4,4,4],7:[1,0,0,0,0,0,0,0,0,0,0,0],8:[3,4,4,4,4,3,3,4,2,3,4,2]},
                 behavSession = '20160114a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-13_15-41-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
		 clusterQuality = {1:[3,3,3,3,2,3,3,3,2,2,2,3],2:[3,5,4,4,3,3,2,2,2,1,1,1],3:[3,2,3,3,3,3,3,2,2,3,2,3],4:[3,6,1,2,2,6,1,6,1,2,7,3],5:[3,2,4,1,1,2,2,3,2,4,1,3],6:[3,1,3,3,4,1,1,2,3,3,3,3],7:[3,1,7,1,2,1,2,3,4,4,3,3],8:[2,0,0,0,0,0,0,0,0,0,0,0]},
                 behavSession = '20160113a')
cellDB.append_session(oneES)
