
'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase_quality as celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-04_16-53-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[4,0,0,0,0,0,0,0,0,0,0,0],2:[3,1,2,1,1,3,4,4,1,1,2,1],3:[3,1,1,1,1,1,2,1,1,1,1,1],4:[3,4,3,1,1,4,1,1,1,1,4,4],5:[3,2,2,3,2,3,3,2,2,2,2,0],6:[3,1,1,1,1,1,1,6,1,6,1,1],7:[3,4,1,4,1,1,1,1,1,1,1,1],8:[3,4,2,2,3,2,2,4,3,4,2,1]},
		 behavSession = '20150604a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-05_16-20-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,4,1,1,2,2,1,4,1,4,0],3:[3,1,1,1,1,1,2,1,1,1,1,1],4:[3,3,2,4,2,1,1,1,4,4,1,4],5:[3,2,2,2,2,4,2,2,2,2,4,2],6:[3,1,1,1,1,1,1,6,1,1,1,1],7:[3,1,4,1,1,1,1,4,1,1,4,1],8:[3,4,4,4,4,4,3,2,1,4,1,2]},
		 behavSession = '20150605a')
cellDB.append_session(oneES)



oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-08_18-10-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,2,4,1,4,3,1,4,1,4,4],3:[3,1,1,6,3,2,4,4,6,1,4,0],4:[3,2,1,1,3,1,3,2,1,1,1,4],5:[3,4,2,2,2,2,1,2,2,2,2,2],6:[3,1,1,1,1,1,1,1,1,1,1,1],7:[3,4,1,3,4,1,4,1,1,1,4,1],8:[3,2,4,2,4,3,2,3,1,1,1,2,]},
		 behavSession = '20150608a')
cellDB.append_session(oneES)



oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-09_16-38-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,1,4,1,4,4,4,6,2,4,4],3:[3,1,4,3,2,6,6,2,1,6,1,4],4:[3,4,4,2,1,4,6,3,3,1,3,2],5:[3,2,1,3,2,2,2,3,2,2,2,0],6:[3,1,1,1,1,1,1,1,1,1,1,3],7:[3,1,1,1,1,1,1,1,1,1,4,3],8:[3,2,1,2,2,2,4,4,3,1,2,0]},
		 behavSession = '20150609a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-10_13-11-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,1,1,1,4,1,2,4,2,1,1],3:[3,2,1,1,1,1,2,6,1,2,1,4],4:[3,2,1,2,1,3,1,1,1,1,3,2],5:[3,4,2,2,3,2,2,1,2,2,2,4],6:[3,1,1,1,1,1,2,1,1,1,1,1],7:[3,1,1,1,1,1,4,1,1,1,4,2],8:[3,1,1,2,2,1,2,3,1,3,3,2]},
		 behavSession = '20150610a')
cellDB.append_session(oneES)



oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-11_13-47-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,4,2,4,1,6,2,2,6,6,2,6],3:[3,4,6,1,2,1,4,1,2,1,1,0],4:[3,4,4,1,1,1,1,4,1,3,1,4],5:[3,2,1,2,1,2,2,1,1,1,4,2],6:[3,5,5,5,3,1,1,1,1,3,3,2],7:[3,2,1,3,2,1,2,3,1,2,4,7],8:[3,1,2,2,1,4,2,4,3,2,1,3]},
		 behavSession = '20150611a')
cellDB.append_session(oneES)



oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-12_17-02-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,1,1,1,1,1,1,2,3,2,2],3:[3,1,1,1,3,2,1,6,3,1,1,1],4:[3,1,1,4,2,2,1,1,2,3,3,0],5:[3,2,1,1,2,2,2,2,1,2,2,1],6:[3,1,1,1,1,1,1,3,1,3,2,1],7:[3,4,3,2,2,3,3,2,1,2,4,1],8:[3,2,1,3,3,2,2,1,1,3,3,0]},
		 behavSession = '20150612a')
cellDB.append_session(oneES)

cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-15_12-03-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,3,4,0],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,1,1,4,1,1,1,1,1,2,1],4:[3,4,3,2,1,3,2,2,4,1,1,4],5:[3,1,1,1,1,1,2,1,1,1,3,1],6:[3,1,4,1,3,1,1,1,1,1,1,1],7:[3,4,1,2,2,2,2,2,1,4,2,4],8:[3,2,4,1,1,1,1,1,2,4,4,3]},
		 behavSession = '20150615a')
cellDB.append_session(oneES)

cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-16_14-12-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,3,3,3,3,3,4,3,3,3,3],3:[3,1,1,3,1,1,1,1,1,1,1,1],4:[3,3,2,2,3,3,3,3,3,3,3,3],5:[3,1,3,1,1,1,3,1,1,1,1,1],6:[3,1,3,1,1,1,1,1,1,4,1,1],7:[3,2,2,4,4,2,4,1,4,2,3,2],8:[3,1,4,4,3,1,4,2,1,4,1,3]},
		 behavSession = '20150616a')
cellDB.append_session(oneES)



oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-17_17-00-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,1,4,4,2,2,4,4,1,2,3],3:[3,1,1,1,1,2,1,1,1,1,1,1],4:[3,2,2,1,2,4,4,2,4,1,3,1],5:[3,1,1,1,1,1,1,1,1,1,1,4],6:[3,1,1,6,1,1,1,1,1,1,1,1],7:[3,1,4,2,1,2,1,3,4,1,1,1],8:[3,3,2,1,1,1,4,2,1,1,1,1]},
		 behavSession = '20150617a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-18_12-18-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,3,2,3,3,3,3,3,0],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,2,1,2,1,1,1,1,1],4:[3,2,3,2,4,1,4,1,4,1,1,0],5:[3,2,1,1,1,1,1,1,1,1,1,1],6:[3,1,1,1,1,1,1,1,1,1,1,1],7:[3,2,1,2,1,2,1,2,4,2,2,1],8:[3,1,4,3,4,1,1,1,1,4,1,0]},
		 behavSession = '20150618a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-19_12-26-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,2,2,2,2,2,2,2],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,2,1,1,1,1,1,1,1,1,0],4:[3,2,1,3,1,1,4,3,3,3,4,3],5:[3,1,1,1,1,1,1,1,1,2,2,1],6:[3,1,2,1,1,1,1,1,1,6,1,1],7:[3,4,4,4,1,4,1,3,3,2,1,1],8:[3,3,1,1,1,1,2,1,1,1,3,1]},
		 behavSession = '20150619a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-22_13-55-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,4,3,1,3,1,2,3,4,1],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,1,1,1,1],4:[3,4,3,1,1,1,4,4,2,4,4,4],5:[3,2,1,1,1,1,1,1,1,1,1,1],6:[3,2,1,1,1,1,1,1,1,1,1,2],7:[3,2,1,3,1,1,2,2,2,4,6,1],8:[3,1,4,1,2,1,1,2,4,4,2,1]},
		 behavSession = '20150622a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-23_13-14-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,3,4,1,2,4,1,2,3,1],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,1,1,1,1],4:[3,4,1,3,1,4,3,1,2,4,4,3],5:[3,2,1,1,1,1,1,1,1,1,4,1],6:[3,1,1,1,1,1,1,1,2,1,1,0],7:[3,1,4,2,1,1,4,1,1,2,1,1],8:[3,2,1,3,2,1,1,1,1,1,1,4]},
		 behavSession = '20150623a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-24_12-04-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,4,2,3,3,3,4,2,2],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,1,1,1,4],4:[3,3,1,4,2,4,1,1,1,1,1,0],5:[3,1,1,4,1,1,2,1,1,2,1,1],6:[3,1,1,1,1,1,1,1,1,1,1,1],7:[3,2,2,3,2,2,1,1,1,4,1,0],8:[3,1,1,4,1,1,1,2,1,1,4,4]},
		 behavSession = '20150624a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-25_13-35-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,2,4,4,2,3,2,2,3,3],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,1,1,1,1],4:[3,2,3,1,1,2,3,3,3,1,1,1],5:[3,1,1,1,1,1,2,6,1,2,1,1],6:[3,2,1,1,1,1,1,1,1,1,1,1],7:[3,2,2,2,1,2,1,2,2,1,1,1],8:[3,1,1,1,1,3,2,1,1,1,1,1]},
		 behavSession = '20150625a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-26_13-50-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,4,1,1,3,2,4,3,2,3,3],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,1,1,1,1],4:[3,4,4,4,1,1,3,3,2,2,4,1],5:[3,1,2,1,4,1,1,2,1,1,2,0],6:[3,1,1,1,1,1,1,1,1,1,1,1],7:[3,1,1,2,4,2,4,4,1,2,1,1],8:[3,1,1,1,1,1,1,2,1,3,1,2]},
		 behavSession = '20150626a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-29_15-57-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,3,3,3],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,1,1,1,1],4:[3,4,1,3,3,1,1,1,3,3,3,3],5:[3,1,3,1,4,1,1,1,3,2,3,1],6:[3,3,3,1,1,3,1,1,1,1,1,1],7:[3,3,3,3,3,3,3,3,3,3,2,2],8:[3,1,1,3,3,1,1,1,1,2,4,4]},
		 behavSession = '20150629a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-30_11-38-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,0,0,0,0],2:[3,3,3,3,3,3,3,3,3,0,0,0],3:[3,1,1,1,1,1,1,1,1,1,1,1],4:[3,1,1,1,3,1,1,3,1,4,3,3],5:[3,1,2,1,1,1,1,1,1,1,1,2],6:[3,1,1,1,1,1,1,1,1,1,1,1],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,4,1,1,1,4,1,1,4,4,1,1]},
		 behavSession = '20150630a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-01_13-00-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,2,3,3,0],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,1,1,1,1],4:[3,3,2,1,3,4,4,4,1,3,1,1],5:[3,1,1,2,1,1,1,1,2,1,1,0],6:[3,1,1,1,1,1,1,1,1,1,1,0],7:[3,3,2,3,2,2,2,3,3,3,3,3],8:[3,1,1,1,3,1,1,2,1,4,1,1]},
		 behavSession = '20150701a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-02_13-52-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,2,2,2,2,2,2,2,2,2],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,1,1,1,1],4:[3,3,3,4,2,2,1,4,3,1,1,1],5:[3,1,1,1,1,1,2,1,1,1,1,1],6:[3,1,1,1,1,1,1,1,1,1,1,3],7:[3,2,2,2,2,2,3,2,2,2,2,2],8:[3,2,1,1,1,1,1,1,3,1,1,1]},
		 behavSession = '20150702a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-03_11-10-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,2,2,2,2,2,2,2,3,2],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,1,1,1,1],4:[3,4,4,3,4,3,3,1,1,3,2,4],5:[3,2,1,1,1,1,1,4,1,1,1,1],6:[3,4,1,1,1,1,1,1,1,1,1,1],7:[3,3,3,3,3,3,3,3,3,3,3,3],8:[3,1,1,1,1,3,4,1,1,1,1,1]},
		 behavSession = '20150703a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-06_13-46-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,2,3,3,3,3],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,1,4,1,1,2,1,1,1,1,1],4:[3,1,3,1,3,1,1,1,3,4,1,0],5:[3,2,2,1,1,1,1,4,1,1,1,1],6:[3,1,1,2,1,1,1,1,1,2,1,1],7:[3,3,3,3,3,3,3,3,3,3,3,3],8:[3,1,1,4,1,1,1,1,1,2,1,1]},
		 behavSession = '20150706a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-08_11-23-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,3,3,3],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,1,1,1,2],4:[3,1,2,3,3,1,1,1,1,3,1,1],5:[3,1,4,4,2,1,2,1,1,1,2,1],6:[3,1,1,6,1,1,1,1,1,1,1,3],7:[3,3,2,2,2,3,2,2,2,3,2,2],8:[3,1,4,1,1,1,3,1,1,1,2,2]},
		 behavSession = '20150708a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-09_11-37-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,2,2,2,2,2,3,2,2,2,2],3:[3,1,1,1,1,1,1,1,1,2,1,1],4:[3,4,1,1,2,1,3,4,1,3,1,1],5:[3,1,1,1,2,1,1,2,1,1,4,1],6:[3,2,1,1,1,6,1,1,1,1,1,1],7:[3,2,2,2,3,3,2,3,2,2,2,3],8:[3,3,2,6,1,1,1,4,6,6,1,6]},
		 behavSession = '20150709a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-10_11-01-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,3,3,2,3,2,2,3,2,2],2:[3,4,2,2,2,2,4,2,2,2,3,2],3:[3,1,1,1,1,1,1,2,1,2,1,1],4:[3,3,3,2,1,1,1,3,1,1,1,2],5:[3,1,1,2,1,1,1,1,1,1,1,2],6:[3,1,6,1,1,1,1,1,1,3,1,0],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,6,2,1,1,2,1,1,3,1,4,2]},
		 behavSession = '20150710a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-13_16-57-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,4,2,2,3,2,2,2,4,1,4,0],3:[3,1,1,1,1,1,1,2,1,1,1,1],4:[3,3,2,3,1,1,6,1,1,3,3,1],5:[3,1,1,4,4,4,1,2,1,4,1,1],6:[3,1,1,4,1,1,1,1,2,6,6,1],7:[3,3,3,3,3,3,2,2,2,2,3,2],8:[3,4,2,2,1,1,4,1,3,2,1,1]},
		 behavSession = '20150713a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-14_13-25-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,2,2,2,4,3,2,3,2,1,0],3:[3,1,1,1,1,1,4,2,2,1,1,1],4:[3,3,3,1,1,1,3,1,2,1,3,2],5:[3,1,1,1,1,1,1,1,4,1,2,1],6:[3,4,1,1,4,6,1,1,1,1,1,6],7:[3,2,3,2,2,2,2,2,3,3,2,2],8:[3,1,1,3,2,1,1,1,1,2,1,1]},
		 behavSession = '20150714a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-15_13-31-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,3,2,2,2,3,4,2,2,2,2],3:[3,1,1,1,1,1,1,2,1,1,2,1],4:[3,1,1,3,1,1,3,6,1,1,3,3],5:[3,1,1,1,1,1,1,1,1,1,1,1],6:[3,1,1,1,6,1,1,1,1,1,1,2],7:[3,3,3,3,3,2,3,3,3,3,3,3],8:[3,1,2,4,1,1,1,2,1,1,4,4]},
		 behavSession = '20150715a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-16_12-12-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,3,2,4,2,2,2,2,3,2,2],3:[3,1,2,1,1,1,2,1,1,2,1,0],4:[3,1,3,1,3,1,3,1,1,1,1,1],5:[3,1,1,1,1,1,1,1,1,2,1,1],6:[3,6,1,1,1,1,1,1,1,1,1,0],7:[3,2,2,2,3,2,3,3,3,3,0,0],8:[3,3,2,1,1,1,1,1,1,1,1,2]},
		 behavSession = '20150716a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-17_10-57-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,2,2,2,2,2,2,1,2,3,2],3:[3,1,1,1,1,1,1,1,2,2,1,1],4:[3,1,6,3,4,4,3,1,1,1,1,3],5:[3,1,1,1,1,4,1,1,1,1,4,0],6:[3,1,1,1,6,4,4,1,1,1,1,1],7:[3,3,3,3,2,3,3,3,2,2,2,2],8:[3,1,2,1,1,1,2,1,1,4,2,1]},
		 behavSession = '20150717a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-22_14-08-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,3,2,2,2,2,3,2,0],2:[3,2,2,2,2,2,2,2,2,3,2,2],3:[3,1,1,1,1,1,1,2,2,1,1,1],4:[3,3,1,3,3,1,2,1,2,1,1,3],5:[3,1,1,1,1,4,1,1,1,1,1,2],6:[3,1,2,1,1,1,6,1,1,1,1,1],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,1,2,2,1,1,1,1,1,2,4,1]},
		 behavSession = '20150722a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-23_14-56-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,2,3,2,2,2,2,2,2,2],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,1,1,1,1],4:[3,2,1,3,3,4,3,1,1,3,2,1],5:[3,1,1,4,1,1,1,1,1,1,2,1],6:[3,1,1,1,6,6,4,4,1,1,2,2],7:[3,2,2,2,2,2,3,3,3,2,3,2],8:[3,1,1,1,1,2,1,1,1,2,3,4]},
		 behavSession = '20150723a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-24_14-10-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,2,3,2,3,3,2,2,2],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,3,2,1,1,1,1,2],4:[3,3,3,3,2,6,3,3,1,2,4,4],5:[3,1,6,1,3,1,4,4,1,1,1,1],6:[3,3,2,4,1,3,4,1,3,1,6,1],7:[3,2,2,2,3,3,3,2,2,2,3,2],8:[3,1,1,3,1,1,1,1,2,3,4,4]},
		 behavSession = '20150724a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-27_10-57-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,3,3,3,3,4,2,2,2,3],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,1,1,1,1],4:[3,3,3,2,1,1,3,2,1,1,1,0],5:[3,4,2,1,4,6,6,4,4,1,1,0],6:[3,4,4,4,6,1,2,6,1,4,1,0],7:[3,3,2,2,2,2,2,2,3,2,2,0],8:[3,1,3,4,2,4,4,1,1,2,2,0]},
		 behavSession = '20150727a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-28_11-32-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,2,3,2,3,3,3,4,1,3],2:[3,1,2,1,1,2,1,3,2,6,1,2],3:[3,1,1,1,1,1,1,1,1,1,1,1],4:[3,1,2,3,3,3,2,1,3,1,2,0],5:[3,2,4,4,3,2,1,2,1,1,2,4],6:[3,3,1,4,1,2,4,4,4,4,1,0],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,1,1,2,2,3,4,1,4,1,1,2]},
		 behavSession = '20150728a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-29_16-14-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,2,2,2,4,3,1,4,2,2,2],3:[3,1,1,2,1,1,2,1,1,1,2,2],4:[3,3,3,3,1,2,3,2,3,4,2,3],5:[3,2,3,2,1,4,4,2,1,2,2,1],6:[3,4,1,1,4,1,1,1,1,4,4,2],7:[3,2,2,2,3,2,2,2,2,2,2,2],8:[3,2,1,3,3,3,1,2,1,2,4,3]},
		 behavSession = '20150729a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-30_12-24-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,6,1,2,2,2,2,2,2,2,2,0],3:[3,4,1,1,2,4,4,4,4,2,1,0],4:[3,1,2,2,3,1,3,1,3,3,2,2],5:[3,4,3,1,2,2,2,2,1,4,2,4],6:[3,1,1,4,1,6,1,6,4,1,1,4],7:[3,3,3,3,2,4,3,2,2,2,4,3],8:[3,1,2,2,3,3,1,1,1,4,1,4]},
		 behavSession = '20150730a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-31_11-43-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,1,2,2,6,2,2,2,4,2,2,2],3:[3,1,3,1,4,1,4,1,2,1,4,2],4:[3,3,3,1,1,2,1,3,3,3,3,2],5:[3,2,2,2,1,2,1,2,1,1,4,0],6:[3,6,1,1,1,1,1,1,1,1,4,1],7:[3,2,2,2,1,2,2,2,4,3,6,2],8:[3,2,3,4,3,3,4,2,4,4,3,4]},
		 behavSession = '20150731a')
cellDB.append_session(oneES)
