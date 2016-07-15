'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-01_15-22-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,3,3,2,3,3,3,3,3,3,3,3],2:[3,3,2,3,3,2,2,2,1,2,3,2],3:[3,1,1,3,3,3,4,3,2,4,1,0],4:[3,3,1,1,1,1,3,3,2,3,3,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,2,3,2,3,4,3,3,3,2],7:[3,2,3,2,2,3,2,3,2,3,2,2],8:[3,2,3,3,2,2,3,3,3,2,3,2]},
                 behavSession = '20160201a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-01-29_15-15-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,3,2,3,3,3,3,3,3,3,2,3],2:[3,2,1,2,2,1,3,2,3,2,1,2],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,2,2,2,1,2,2,2,2,2,0,0],5:[3,2,2,2,3,3,2,2,2,2,2,2],6:[3,2,2,3,3,3,3,3,2,3,3,3],7:[3,2,2,3,2,2,3,2,2,2,2,2],8:[3,1,4,4,2,2,2,4,4,1,3,0]},
                 behavSession = '20160129a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-01-28_16-07-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,3,3,3,3,3,2,4,3,3,3,3],2:[3,1,2,2,1,2,2,2,1,3,2],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,2,3,2,2,2,2,2,2,2,2,3],5:[3,2,2,2,3,2,2,2,2,3,2,2],6:[3,1,2,1,1,1,2,4,3,4,1,2],7:[3,2,2,2,2,2,2,2,2,2,3,2],8:[3,2,1,2,3,3,3,1,4,2,3,0]},
                 behavSession = '20160128a')
cellDB.append_session(oneES)


