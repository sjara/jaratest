'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase_quality as celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-18_10-49-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,3,3,2,2,3,3,1,1,3],2:[3,1,5,1,2,2,3,3,3,5,3,3],3:[3,1,3,3,3,3,2,3,1,2,6,3],4:[3,3,3,3,2,2,2,1,3,3,3,2],5:[3,3,2,3,2,2,3,2,2,2,0,0],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,2,2,2,2,3,2,2,3,2,3],8:[3,2,3,1,3,2,3,1,2,2,3,3]
		 behavSession = '20160318a')
cellDB.append_session(oneES

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-16_10-04-37',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,3,3,3,3,3,3,1,3,2],2:[3,3,3,3,2,2,3,2,2,1,3,3],3:[3,2,3,2,2,3,1,6,3,3,3,3],4:[3,2,2,3,3,3,2,2,3,3,3,2],5:[3,3,3,3,2,3,3,3,3,3,3,3],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,3,3,2,3,3,3,3,3,2,3],8:[3,3,2,3,3,3,1,3,3,3,3,2]
		 behavSession = '20160316a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-03_14-27-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,2,2,3,3,1,2,1,2,3],2:[3,3,1,3,2,2,3,2,2,2,3,3],3:[3,1,3,2,2,1,2,3,1,3,2,1],4:[3,1,3,1,4,3,1,1,2,2,2,3],5:[3,2,2,3,2,3,3,2,2,2,2,3],6:[3,2,2,2,2,2,2,2,3,3,3,2],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,1,2,2,3,2,2,2,2,3,2]
		 behavSession = '20160303a')
cellDB.append_session(oneES

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-01_14-12-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,1,3,1,3,2,1,1,3,2],2:[3,2,3,2,2,2,2,2,2,2,2,3],3:[3,1,6,2,1,2,3,1,2,4,4,6],4:[3,2,1,2,1,4,1,3,3,1,1,0],5:[3,2,3,2,3,2,2,2,2,2,3,2],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,2,2,2,2,2,3,2,2,2,3],8:[3,2,3,2,3,2,2,2,1,2,5,2]
		 behavSession = '20160301a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-29_15-55-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,3,3,3,3,3,3,2,0],2:[3,3,2,3,3,3,3,2,2,2,2,3],3:[3,4,1,1,1,2,1,5,2,2,1,2],4:[3,3,1,2,2,2,1,2,3,3,2,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,3,3,2,3,2,3,2,2,2],7:[3,3,2,2,2,3,2,3,2,2,2,0],8:[3,3,2,2,3,2,1,3,2,7,3,2]
		 behavSession = '20160229a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-25_17-13-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,5,3,2,2,3,3,3,3],2:[3,3,3,2,2,2,3,2,2,2,2,2],3:[3,2,1,5,1,6,8,3,1,5,2,1],4:[3,2,2,2,1,2,3,1,1,2,2,2],5:[3,4,3,2,3,3,2,3,1,2,3,2],6:[3,3,3,3,3,3,2,2,3,3,2,3],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,3,1,2,2,2,2,3,3,2,1]
		 behavSession = '20160225a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-24_17-21-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,4,3,2,2,3,3,2,2,3],2:[3,2,2,3,2,2,2,3,2,2,2,2],3:[3,1,1,2,3,6,2,1,4,1,1,6],4:[3,2,2,2,2,1,3,4,2,2,2,2],5:[3,3,3,2,2,2,3,3,3,3,3,3],6:[3,3,3,3,3,2,2,3,3,3,3,3],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,3,2,2,3,2,2,1,2,2,2]
		 behavSession = '20160224a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-23_14-12-34',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,2,2,3,8,4,8,3],2:[3,3,2,3,2,3,8,3,2,2,3,2],3:[3,5,3,2,4,1,1,2,1,4,2,0],4:[3,1,2,1,2,1,2,3,3,2,3,4],5:[3,3,3,3,3,3,3,3,2,3,2,3],6:[3,3,3,2,3,3,2,3,3,3,3,3],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,2,2,2,3,1,2,3,2,3,3]
		 behavSession = '20160223a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-22_17-55-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,4,2,2,3,2,3,3,2],2:[3,3,3,2,2,3,2,3,3,3,3,0],3:[3,1,2,1,1,1,1,1,3,1,1,1],4:[3,1,2,3,3,2,1,2,2,3,2,0],5:[3,3,2,3,3,3,3,4,2,2,2,3],6:[3,3,3,3,2,3,2,3,3,3,3,2],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,1,2,3,2,2,2,3,1,2]
		 behavSession = '20160222a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-19_10-42-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,2,2,3,2,2,2,2,3,2],2:[3,2,2,2,2,2,2,3,2,2,2,0],3:[3,1,1,3,3,1,1,1,1,1,1,0],4:[3,2,1,2,4,1,1,2,1,2,3,1],5:[3,3,2,2,2,2,3,2,1,1,3,2],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,2,3,3,3,3,2,3,2,3,3],8:[3,2,2,3,2,6,2,2,6,1,2,2]
		 behavSession = '20160219a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-18_14-53-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,3,3,3,3,2,3,2,2,0],2:[3,2,2,2,2,2,2,2,3,2,2,2],3:[3,1,3,1,1,1,1,1,1,1,1,0],4:[3,1,1,3,1,1,2,1,1,2,1,3],5:[3,3,3,2,2,4,2,3,2,2,3,0],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,2,2,2,3,3,2,7,2,2]
		 behavSession = '20160218a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-17_16-15-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,3,3,1,2,2,2,2,2],2:[3,2,2,2,3,2,2,2,2,2,3,2],3:[3,1,1,1,1,1,1,2,1,1,1,3],4:[3,1,1,1,2,3,1,2,1,2,2,3],5:[3,2,1,1,3,1,1,2,2,1,2,3],6:[3,3,3,3,3,2,3,2,3,2,3,3],7:[3,2,2,2,2,2,3,2,2,2,2,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]
		 behavSession = '20160217a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-16_14-16-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,3,1,3,3,2,3,1,2,4],2:[3,3,3,2,2,2,3,2,2,2,2,2],3:[3,1,1,3,1,1,1,1,1,2,1,1],4:[3,2,3,1,4,1,2,3,1,1,2,1],5:[3,3,2,4,2,3,2,3,2,3,3,3],6:[3,3,2,2,2,1,2,3,1,2,2,0],7:[3,2,2,2,2,2,2,2,3,2,2,2],8:[3,0,0,0,0,0,0,0,0,0,0,0]
		 behavSession = '20160216a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-15_15-40-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,3,1,2,3,1,1,1,3],2:[3,1,1,3,3,3,2,2,2,1,1,3],3:[3,1,1,1,3,1,2,1,1,2,1,1],4:[3,1,2,2,1,1,1,1,1,3,1,1],5:[3,2,2,2,2,2,2,3,2,2,2,3],6:[3,1,1,2,2,6,7,2,6,2,3,6],7:[3,2,3,2,2,2,3,2,2,2,2,2],8:[3,0,0,0,0,0,0,0,0,0,0,0]
		 behavSession = '20160215a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-12_09-50-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,2,4,2,1,1,2,2,1,0],2:[3,2,2,2,2,2,3,2,2,2,2,3],3:[3,1,3,6,1,1,1,1,2,2,1,2],4:[3,1,1,1,3,5,1,1,1,1,1,0],5:[3,2,2,3,2,2,3,2,2,3,2,0],6:[3,3,6,2,1,6,2,3,2,6,2,3],7:[3,2,3,3,2,2,1,3,1,2,2,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]
		 behavSession = '20160212a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-11_17-18-34',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,2,2,2,3,3,3,3,0],2:[3,2,2,2,3,2,3,3,3,2,2,0],3:[3,1,1,1,1,1,2,2,1,1,7,0],4:[3,3,1,1,4,8,1,1,1,5,8,1],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,2,1,2,3,7,7,2,1,3],7:[3,2,1,1,2,2,2,2,3,2,3,2],8:[3,2,2,2,2,3,2,2,2,1,2,3]
		 behavSession = '20160211a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-10_16-21-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,1,3,2,2,1,1,2,3,0],2:[3,2,2,3,2,2,3,2,2,3,3,0],3:[3,1,1,3,1,2,1,1,6,1,1,4],4:[3,1,1,1,6,1,1,1,1,1,5,5],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,2,6,1,2,1,2,2,3,3],7:[3,2,2,3,2,2,2,2,2,2,2,0],8:[3,2,2,2,2,2,2,1,3,2,1,3]
		 behavSession = '20160210a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-09_16-32-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,3,2,2,1,1,1,2,2,3],2:[3,2,2,2,3,3,2,2,2,3,3,2],3:[3,2,3,1,2,1,2,1,1,1,1,1],4:[3,1,3,2,1,2,1,1,1,1,1,1],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,3,3,2,6,3,2,1,3,3],7:[3,3,3,3,3,2,3,3,2,3,2,2],8:[3,2,3,3,2,2,1,2,2,2,2,0]
		 behavSession = '20160209a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-08_19-18-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,3,1,2,2,2,3,2,0],2:[3,2,3,3,2,3,3,2,2,3,2,3],3:[3,2,1,2,2,1,2,1,2,1,3,1],4:[3,,1,1,1,1,1,1,1,1,1,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,2,1,1,3,6,3,2,2,2],7:[3,2,2,3,2,1,1,3,2,1,3,3],8:[3,1,2,1,2,2,1,2,2,3,1,3]
		 behavSession = '20160208a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-07_15-27-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,2,3,1,1,2,3,2],2:[3,3,3,3,3,3,2,2,2,2,2,2],3:[3,3,1,2,2,1,2,1,2,1,2,0],4:[3,1,1,1,1,1,1,1,1,1,1,1],5:[3,2,2,2,3,2,2,2,2,2,2,3],6:[3,2,3,2,1,2,7,1,6,6,2,2],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,4,1,1,1,2,2,1,2,6]
		 behavSession = '20160207a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-06_16-49-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,2,1,1,2,1,2,3,1,1],2:[3,3,2,2,2,2,2,2,2,2,3,0],3:[3,2,2,1,2,2,2,1,3,1,1,1],4:[3,1,3,1,1,1,1,1,1,1,1,1],5:[3,2,3,2,2,2,2,3,3,2,2,1],6:[3,2,3,7,2,4,1,2,6,2,2,3],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,2,2,2,2,2,2,1,2,2]
		 behavSession = '20160206a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-05_14-33-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,2,1,1,1,1,2,1,2,3],2:[3,3,1,4,2,1,1,2,1,2,2,2],3:[3,1,1,3,1,1,1,2,1,1,1,0],4:[3,1,3,3,1,1,1,2,1,1,1,4],5:[3,2,2,2,3,2,3,2,2,2,2,3],6:[3,2,4,2,1,4,2,2,1,2,3,2],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,1,2,1,1,2,2,2,2,1]
		 behavSession = '20160205a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-04_15-41-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,1,1,2,1,1,1,2,1],2:[3,1,1,2,1,2,3,1,2,2,2,1],3:[3,1,2,1,3,1,1,1,1,0,0,0],4:[3,2,1,1,1,1,1,1,1,3,1,2],5:[3,3,2,2,2,3,3,3,3,2,3,2],6:[3,2,2,3,2,2,3,2,1,1,2,1],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,2,1,4,2,2,2,2,2,3]
		 behavSession = '20160204a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-01_15-22-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,2,3,1,1,1,1,1,1,1],2:[3,3,2,1,3,2,2,2,1,2,3,1],3:[3,1,1,1,1,1,1,3,2,1,1,0],4:[3,1,1,1,1,1,1,1,1,1,1,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,3,1,2,1,1,1,4,4,2],7:[3,2,3,2,2,3,2,3,2,3,2,2],8:[3,2,1,4,3,2,1,1,3,2,1,2]
		 behavSession = '20160201a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-01-29_15-15-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,1,4,1,1,4,1,2,1],2:[3,1,1,2,2,1,3,2,3,2,1,2],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,2,1,2,1,1,2,2,2,2,0,0],5:[3,2,3,1,1,3,2,2,2,2,2,2],6:[3,2,2,4,1,1,3,1,2,3,1,7],7:[3,3,2,1,2,2,3,2,2,2,2,2],8:[3,1,1,1,2,2,2,1,1,1,3,0]
		 behavSession = '20160129a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-01-28_16-07-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,3,2,1,1,1,1,1],2:[3,1,2,2,1,2,2,1,1,3,2,0],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,2,2,2,2,2,2,1,1,2,1],5:[3,2,1,2,1,1,2,2,2,3,2,2],6:[3,2,2,1,1,1,2,1,1,1,1,2],7:[3,2,2,2,2,2,2,2,2,2,3,3],8:[3,2,1,2,4,3,1,1,1,1,4,0]
		 behavSession = '20160128a')
cellDB.append_session(oneES) 


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-01-27_17-20-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,1,1,3,2,1,1,1],2:[3,2,1,2,1,2,2,2,1,3,2,1],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,1,2,2,2,2,2,3,1,1,3,0],5:[3,2,3,3,3,2,2,2,2,2,2,2],6:[3,1,1,1,1,1,1,1,1,2,1,2],7:[3,3,2,2,2,3,2,2,1,2,1,2],8:[3,1,1,2,1,1,1,1,1,2,2,0]
		 behavSession = '20160127a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-01-26_15-46-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
		clusterQuality = {1:[3,1,1,1,1,1,1,1,1,3,1,0],2:[3,3,1,3,1,2,2,2,2,2,1,2],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,2,2,2,3,2,2,2,2,2,2,3],5:[3,2,1,2,1,1,2,2,3,2,2,2],6:[3,1,1,1,1,2,1,1,1,1,0,0],7:[3,3,3,2,2,2,1,2,2,1,2,1],8:[3,1,1,1,1,3,1,1,1,1,2,2] 
                 behavSession = '20160126a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-01-22_16-39-00'
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,3,2,2,1,1,1,0],2:[3,2,2,2,2,3,2,2,2,1,2,2],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,2,3,2,2,2,2,2,2,2,3,2],5:[3,1,2,2,1,3,2,1,1,1,3,0],6:[3,1,1,2,2,1,2,2,1,2,0,0],7:[3,2,2,3,2,2,2,2,3,2,2,1],8:[3,1,1,2,2,2,1,1,1,3,1,2]
		 behavSession = '20160122a')
cellDB.append_session(oneES)


