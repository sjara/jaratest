'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase_quality as celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='test087',
                 ephysSession = '2015-10-08_15-30-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,2,3,3,3,3,3,2,3,4],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,1,3,3,3,1,1,1,1,1,1,3],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,1,3,1,1,1,3,1,1,3,3,3],8:[3,3,3,3,3,3,3,3,3,3,3,3]},
		 behavSession = '20151015a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-10-09_15-02-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,4,3,2,2,3,3,3,3,3],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,3,2,3,1,3,3,3,4,3,3,3],4:[3,3,3,3,3,3,3,3,3,3,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,1,1,3,4,1,1,1,1,3,3],8:[3,3,3,3,3,3,3,3,3,3,3,3]},
		 behavSession = '20151009a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-10-13_14-12-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,1,3,3,2,1,3,3,3,1,2,1],4:[3,3,3,3,3,3,3,3,3,3,3,3],5:[3,3,3,3,3,3,3,3,3,3,2,3],6:[3,3,3,3,2,3,3,3,3,2,3,3],7:[3,3,2,3,3,3,3,3,4,1,1,3],8:[3,3,3,3,3,3,3,3,3,3,3,3]},
		 behavSession = '20151013a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-10-21_17-03-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,3,3,3],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,3,3,3,3,3,3,3,3,3,2,3],4:[3,3,3,3,3,3,3,3,3,3,2,3],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,3,3,4,3,3,3,3,3,3,3],8:[3,3,4,3,3,3,3,3,3,3,2,3]},
		 behavSession = '20151021a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test087',
                 ephysSession = '2015-10-22_17-26-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,2,4,3,3,3,2,3,3,3],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,3,3,3,3,3,2,3,3,3,3,0],4:[3,3,3,3,3,3,3,3,3,3,3,3],5:[3,3,3,3,3,4,3,3,3,3,3,3],6:[3,3,3,3,3,2,4,3,3,3,3,2],7:[3,3,3,1,1,1,1,1,1,1,1,1],8:[3,3,3,3,3,3,3,3,3,3,3,3]},
		 behavSession = '20151022a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-05_17-10-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,3,3,3,2,3,3,2,3,3,3,3],4:[3,3,3,3,3,3,3,3,3,3,3,3],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,1,1,1,1,1,3,3,3,3,3,1],8:[3,3,3,3,3,3,3,3,3,3,3,3]},
		 behavSession = '20151105a')

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-17-12-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,3,3,3,3,3,3,3,3,3,0],3:[3,2,3,3,2,1,3,3,3,3,3,3],4:[3,3,3,3,3,3,3,3,3,3,3,3],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,3,1,1,3,3,3,3,3,3,3,3],7:[3,3,3,3,3,4,4,4,4,4,3,1],8:[3,3,3,3,3,3,3,2,3,3,3,3]},
		 behavSession = '20151117a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-07_20-47-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,3,3,3,3,3,3,3,3,3],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,3,3,3,3,1,3,1,3,2,3,3],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,3,1,3,4,1,1,1,1,1,3],8:[3,3,3,3,3,3,3,3,3,3,3,3]},
		 behavSession = '20151107a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-09_18-26-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,2,3,3,0],2:[3,3,3,3,3,3,3,3,3,3,3,0],3:[3,3,1,3,3,1,3,3,3,1,1,3],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,3,3,3,3,3,3,3,3,0],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,3,3,4,3,3,4,3,3,3,3],8:[3,3,3,3,3,3,3,3,3,3,3,0]},
		 behavSession = '20151109a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-10_16-44-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,3,3,3],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,3,3,1,1,3,3,3,3,3,3,3],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,4,3,1,1,3,3,3,3,4,3],8:[3,3,3,3,3,3,3,3,3,3,3,3]},
		 behavSession = '20151110a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-11_17-21-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,3,3,3],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,3,3,4,3,3,3,3,1,3,3,3],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,4,3,3,1,4,3,3,3,3,3,3],8:[3,3,3,3,3,3,3,3,3,3,3,3]},
		 behavSession = '20151111a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-13_14-55-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,3,3,0],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,3,3,1,3,1,1,1,3,1,1,1],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,1,3,3,3,3,3,3,3,1,3,3],7:[3,3,3,1,3,3,1,1,3,1,1,1],8:[3,3,3,3,3,3,3,3,3,3,3,3]},
		 behavSession = '20151113a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-16_17-16-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,3,3,3],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,3,3,3,3,3,1,1,3,1,2,3],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,3,3,2,3,3,3,3,3,3,3,3],7:[3,3,1,1,1,3,3,2,3,3,3,3],8:[3,3,3,3,3,2,3,3,3,3,3,3]},
		 behavSession = '20151116a')
cellDB.append_session(oneES) 


