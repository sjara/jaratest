'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase_quality as celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-18_13-00-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,4,3,1,3,2,2,2,1,4,4],2:[3,6,3,3,3,3,4,2,2,1,
		 behavSession = '20150918a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-29_10-26-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,3,4,2,2,1,4,3],2:[3,
		 behavSession = '20150729a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-31_14-40-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[1],2:[3,1,1,4,1,4,1,2,2,3,1],3:[3,1,4,1,2,1,1,1,3,2,4,4],4:[3,1,1,3,1,1,1,1,2,2,1],5:[3,2,2,1,1,4,1,1,1,1,1,4],6:[3,1,2,1,1,1,1,1,1,1,2,1],7:[3,1,1,1,2,2,2,1,1,3,1,1],8:[3,1,1,2,2,4,1,2,4,1,3,4]
		 behavSession = '20150731a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-24_13-32-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,1,2,1,3,1,1,2,1,2],2:[3,2,2,1,1,1,1,3,3,2,2,2],3:[3,2,2,1,1,1,1,1,1,1,1,1],4:[3,3,3,2,1,4,2,2,4,1,4,2],5:[3,2,3,4,2,1,4,3,1,3,2],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,1,2,2,1,1,1,2,2,4,3],8:[3,3,3,2,3,1,1,1,4,2,2,2]
		 behavSession = '20150924a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-21_12-23-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,4,2,4,4,3,3,1,4,2],2:[3,1,2,1,1,1,1,3,1,1,1,0],3:[3,3,1,1,1,1,1,1,1,4,3,1],4:[3,4,3,1,1,1,2,4,1,1,3,0],5:[3,4,1,4,1,1,1,1,4,3,3,3],6:[3,4,4,1,1,1,1,1,4,1,3,1],7:[3,4,3,4,1,1,2,4,3,1,1,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]
		 behavSession = '20150921a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-18_13-00-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,3,4,3,4,2,2,1,4,1],2:[3,3,2,4,3,1,1,4,3,3,1,1],3:[3,1,1,2,1,1,1,1,1,1,1,0],4:[3,3,3,3,1,1,1,1,2,1,4,2],5:[3,4,1,3,4,4,1,1,4,3,1,4],6:[3,3,1,1,1,2,1,1,1,1,1,1],7:[3,4,3,1,4,4,2,3,2,3,3,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]
		 behavSession = '20150918a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-17_14_19-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,3,2,3,3,2,1,1,3,2],2:[3,1,2,1,1,2,2,3,1,1,2,1],3:[3,3,1,1,1,1,1,4,1,1,1,4],4:[,,,,,,,,,,,],5:[3,4,1,3,4,4,1,1,4,3,1,4],6:[3,3,1,1,1,2,1,1,1,1,1,1],7:[3,4,3,1,4,4,2,3,2,3,3,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]
		 behavSession = '20150917a')
cellDB.append_session(oneES) 
