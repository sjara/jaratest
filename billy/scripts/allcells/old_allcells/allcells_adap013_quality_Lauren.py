'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-08_14-24-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160408a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-06_15-29-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160406a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-04_15-16-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160404a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-31_14-19-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160324a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-29_15-33-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160324a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-24_14-34-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160324a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-22_13-32-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160322a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-19_16-30-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160319a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-17_14-59-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160317a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-15_13-48-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160315a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-03_11-19-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160303a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-29_11-23-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160229a')
clusterQuality = {1:[3,3,3,3,2,1,3,2,3,2,3,3],2:[3,2,3,1,1,1,1,3,3,3,3,0],3:[3,3,1,3,2,3,1,2,3,3,2,3],4:[3,3,3,2,3,3,3,3,1,1,3,2],5:[3,3,3,3,1,3,3,3,3,3,3,3],6:[3,3,3,3,3,3,2,1,1,2,3,2],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,2,3,3,2,1,3,3,1,3,3]},
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-25_13-39-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160225a')
clusterQuality = {1:[]},

cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-23_10-39-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160223a')
clusterQuality = {1:[3,3,2,3,3,2,2,2,3,3,1,2],2:[3,4,2,2,1,1,4,3,3,2,2,0],3:[3,3,2,2,3,3,2,3,2,4,3,3],4:[3,1,2,3,2,3,3,1,2,3,2,3],5:[3,1,4,3,3,3,2,2,1,2,4,3],6:[3,3,3,2,2,2,2,3,2,2,2,0],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,3,3,2,2,2,4,3,2,2,2]},

cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-19_16-49-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160219a')
clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,4,2,3,2,2,3,2,2,2,2,2],3:[3,2,3,3,2,2,1,2,2,1,2,2],4:[3,4,2,3,2,3,2,2,2,2,2,3],5:[3,2,1,2,2,3,1,3,1,2,4,1],6:[3,2,3,3,2,3,2,2,3,2,1,0],7:[3,2,3,2,3,2,2,2,3,2,3,2],8:[3,2,2,1,1,3,3,2,4,2,2,3]},

cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-18_17-51-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160218a')
clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,2,2,3,3,4,2,2,2,2,0],3:[3,3,1,3,2,4,3,2,2,3,2,0],4:[3,2,2,2,2,2,2,3,2,4,2,3],5:[3,2,1,4,2,1,3,3,3,3,3,0],6:[3,2,2,2,2,2,3,3,3,3,3,0],7:[3,2,2,3,2,2,2,3,2,2,2,3],8:[3,3,2,2,2,2,2,3,3,3,2,2]},
cellDB.append_session(oneES)


oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-10_10-10-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160210a')
clusterQuality = {1:[3,2,2,3,2,2,2,3,2,2,2,2],2:[3,2,2,2,2,4,2,2,2,2,3,3],3:[3,2,2,3,3,4,3,2,2,2,3,0],4:[3,3,3,4,2,3,2,2,2,2,2,0],5:[3,3,2,4,2,3,4,2,2,2,2,3],6:[3,3,2,3,2,3,3,4,2,2,2,2],7:[3,4,2,2,2,3,2,2,2,3,2,2],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
cellDB.append_session(oneES)
