'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-28_15-44-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,3,2,2,1,1,2,3,2,3,1,2],2:[3,5,2,2,3,3,2,3,3,3,3,0],3:[3,3,3,1,2,2,4,1,2,2,3,1],4:[3,1,3,1,2,3,1,1,1,3,2,3],5:[3,3,1,2,1,3,3,2,2,2,2,3],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,3,2,2,6,6,3,2,3,3,2],8:[3,2,2,3,2,2,3,1,1,3,1,1]
                 behavSession = '20160328a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-23_15-33-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,2,3,1,1,1,2,3,2,3,3,2],2:[3,3,1,3,3,1,3,1,2,3,5,1],3:[3,1,1,3,1,1,1,3,2,2,1,4],4:[3,3,1,3,5,3,1,2,5,2,2,2],5:[3,2,2,2,2,2,3,2,3,2,2,3],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,5,2,1,2,7,2,2,2,3,3,7],8:[3,2,8,2,2,3,2,2,2,2,1,2]
                 behavSession = '20160323a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-21_16-59-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,2,2,2,1,3,3,2,3,1,3,2],2:[3,2,3,5,3,2,3,3,5,1,2,3],3:[3,1,2,1,1,2,1,1,1,1,3,2],4:[3,1,2,2,1,1,3,1,2,2,5,1],5:[3,2,2,2,3,3,2,2,1,4,2,2],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,2,2,2,1,2,1,2,2,3,2],8:[3,2,1,3,8,2,3,2,8,8,2,1]
                 behavSession = '20160321a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-17_16-22-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,2,3,3,3,1,3,1,3,1,2,0],2:[3,5,5,2,1,5,3,3,1,3,2,3],3:[3,2,2,3,3,3,1,1,1,1,1,3],4:[3,2,2,2,3,3,3,1,2,1,3,0],5:[3,3,1,3,1,3,2,3,2,2,3,1],6:[3,3,2,2,2,2,1,2,3,3,2,1],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,2,2,1,1,2,2,1,2,1,2]
                 behavSession = '20160317a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-15_15-17-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,3,2,3,6,1,2,3,1,2,2,0],2:[3,1,1,1,1,3,6,2,3,6,6,3],3:[3,1,1,1,2,3,1,3,1,2,1,3],4:[3,3,1,2,1,1,3,1,1,1,2,1],5:[3,1,2,2,3,2,3,3,1,1,2,3],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,2,1,1,2,3,2,3,2,2,2],8:[3,1,2,2,3,1,2,2,2,1,2,2]
                 behavSession = '20160315a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-03_16-12-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,3,3,2,3,2,2,2,3,2,3],3:[3,1,1,1,3,1,1,2,1,3,2,3],4:[3,2,2,2,2,2,2,3,3,3,5,1],5:[3,2,3,2,3,2,2,3,3,3,2,1],6:[3,5,3,3,1,3,3,2,2,3,3,2],7:[3,3,1,2,3,3,3,1,1,1,2,0],8:[3,1,2,1,1,1,1,1,1,3,3,0]
                 behavSession = '20160303a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-02-29_17-55-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,3,2,3,2,2,2,2,3,1,1,1],2:[3,3,3,3,3,2,1,2,3,5,1,1],3:[3,2,3,3,2,2,3,1,2,1,2,1],4:[3,2,1,2,2,2,2,3,2,1,1,1],5:[3,2,3,2,1,3,1,3,2,2,2,0],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,8,1,1,2,3,1,2,1,3,5],8:[3,1,2,2,2,2,2,3,2,2,2,3]
                 behavSession = '20160229a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-02-25_15-29-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,2,1,3,3,1,1,2,2,1,2,1],2:[3,2,2,2,1,1,2,5,1,2,3,1],3:[3,1,5,4,2,5,1,1,1,1,4,1],4:[3,1,2,3,2,1,2,1,2,1,4,0],5:[3,2,2,1,2,1,3,1,1,2,2,4],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,1,3,1,2,2,2,1,3,1,1,0],8:[3,3,2,3,1,2,3,1,2,2,6,2]
                 behavSession = '20160225a')
cellDB.append_session(oneES)
'''
