'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase_quality as celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

oneES = eSession(animalName='adap002',
                 ephysSession = '2015-10-12_15-08-17',
                  clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,2,3,4,4,1,2,2,2,2],2:[3,2,4,2,4,1,4,4,1,2,3,4],3:[3,2,3,4,2,2,1,1,2,2,2,3],4:[3,5,1,1,1,1,5,5,5,1,3,4],5:[3,2,1,4,1,4,2,2,2,1,1,1],6:[3,5,3,3,3,5,3,1,4,5,3,4],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,4,4,6,3,2,1,3,2,4,6]},
		 behavSession = '20151012a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='adap002',
                 ephysSession = '2015-10-15_14-30-16',
                  clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,1,3,4,3,3,4,3,1,2],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,3,3,3,4,4,4,4,4,3,3],4:[3,4,1,1,4,4,2,3,2,3,5,2],5:[3,1,4,4,4,4,2,3,4,4,4,1],6:[3,3,1,3,1,1,4,4,3,4,1,1],7:[3,2,4,4,3,3,4,3,1,4,2,3],8:[3,2,4,4,3,3,1,1,1,4,3,0]},
		 behavSession = '20151015a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='adap002',
                 ephysSession = '2015-10-15_12-23-22',
                  clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,1,2,1,1,1,2,2,3,0],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,1,1,4,2,2,1,2,3,1,4],4:[3,1,1,1,2,1,2,2,1,1,1,1],5:[3,2,2,4,4,1,1,1,2,4,1,2],6:[3,1,1,3,1,1,1,1,1,1,1,1],7:[3,2,3,1,2,4,3,4,2,4,2,2],8:[3,1,2,1,4,4,1,1,4,3,1,1]},
		 behavSession = '20151015a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='adap002',
                 ephysSession = '2015-10-16_15-55-41',
                  clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,1,1,1,1,3,2,2,2],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,4,1,3,2,3,2,1,2,2,2,0],4:[3,4,4,2,1,2,1,4,4,1,2,2],5:[3,3,2,4,1,2,2,2,1,4,2,1],6:[3,1,1,1,4,1,1,1,1,1,3,4],7:[3,1,2,2,2,2,3,4,2,4,3,1],8:[3,2,3,2,3,3,3,4,4,3,3,2]},
		 behavSession = '20151016a')
cellDB.append_session(oneES) 


