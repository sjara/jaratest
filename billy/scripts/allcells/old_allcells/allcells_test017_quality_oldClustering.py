'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase_quality as celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-27_14-41-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,12),5:range(1,13),6:range(1,13),7:range(1,12),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,2,1,1,1,2,1,1,1,4],2:[3,3,2,2,2,3,2,2,3,2,2,2],3:[3,2,1,3,2,3,6,1,3,1,1,6],4:[3,2,2,1,2,1,2,2,2,3,3,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,1,2,2,3,2,1,2,1,3,2],7:[3,2,1,3,1,2,1,1,1,1,1,0],8:[3,4,6,6,2,6,3,6,2,2,3,6]},
                 behavSession = '20150327a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-26_15-20-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,2,3,1,3,3,3,1,1],2:[3,2,1,2,3,2,1,2,3,3,2,3],3:[3,3,3,3,3,3,6,3,3,3,3,3],4:[3,2,2,3,3,3,3,2,3,3,2,1],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,3,2,2,3,3,3,3,3,3],7:[3,3,1,2,6,4,1,3,3,1,6,6],8:[3,3,6,6,3,6,2,3,3,3,2,6]},
                 behavSession = '20150326a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-25_15-43-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,4,2,2,3,1,1,4,3,3,3],2:[3,3,1,3,2,3,3,2,3,2,3,3],3:[3,6,3,3,3,3,3,3,3,3,3,3],4:[3,3,2,3,3,3,5,3,4,2,3,6],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,2,3,3,3,2,2,3,3,3],7:[3,3,3,4,3,3,3,1,1,4,1,3],8:[3,1,1,2,2,3,3,3,6,3,6,3]},
                 behavSession = '20150325a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-24_16-25-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,4,2,3,4,3,2,1,3,4,4],2:[3,3,1,5,3,2,3,2,2,2,3,1],3:[3,3,4,3,3,6,6,3,2,3,3,3],4:[3,2,2,4,8,3,7,1,6,6,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,3,5,2,2,4,3,3,3,3],7:[3,1,2,3,4,4,6,3,3,4,2,1],8:[3,3,3,2,6,6,3,4,2,3,2,3]},
                 behavSession = '20150324a')
cellDB.append_session(oneES)

'''
oneES = eSession(animalName='test017',####################################################
                 ephysSession = '2015-03-23_16-27-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[4,3,3,4,3,3,1,3,4,4,3,2],2:[4,2,2,2,4,4,3,3,3,3,3,1],3:[4,4,4,4,4,4,4,4,3,4,4,4],4:[4,2,3,2,2,4,2,3,3,5,3,5],5:[4],6:[4,4,3,4,3,4,3,3,3,4,3,4],7:[4,4,2,3,2,4,2,3,2,4,2,1],8:[4,4,2,3,2,4,3,3,4,3,3]},
                 behavSession = '20150323a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-22_20-31-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,1,2,4,2,4,3,4,3,2],2:[3,4,3,3,1,3,2,2,2,1,4,3],3:[3,3,3,3,2,3,3,3,3,2,3,3],4:[3,3,2,2,3,3,2,2,2,2,4,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,4,2,4,3,4,4,2,4,3,6,4],7:[3,2,3,2,4,3,3,3,3,2,2,3],8:[3,2,2,6,3,4,2,2,5,5,2,6]},
                 behavSession = '20150322a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-21_14-06-46',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,3,3,4,3,1,2,3,2,4],2:[3,3,2,3,1,2,1,3,2,2,1,1],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,3,4,2,3,3,4,2,3,3,5,4],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,2,6,6,3,3,7,7,4,4,2],7:[3,2,6,3,3,3,3,2,3,2,3,7],8:[3,2,4,4,2,2,4,3,4,7,2,3]},
                 behavSession = '20150321a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-20_13-05-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,3,2,2,3,2,3,1,3,2],2:[3,1,1,2,3,3,3,1,2,2,2,3],3:[3,3,3,3,3,3,3,3,3,3,2,3],4:[3,3,3,3,3,4,3,3,2,2,4,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,1,3,6,2,6,3,3,3,3,1],7:[3,1,3,2,2,2,2,3,6,2,3,4],8:[3,3,3,3,2,3,3,3,3,2,2,2]},
                 behavSession = '20150320a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-19_13-35-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,2,4,3,3,1,1,3,2,2],2:[3,3,3,4,4,3,2,2,4,2,2,3],3:[3,3,2,3,3,2,3,3,3,3,3,0],4:[3,3,3,3,3,3,2,2,4,6,3,4],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,6,2,3,1,1,3,2,6,6,3],7:[3,2,3,2,3,4,3,2,3,3,6,1],8:[3,2,2,3,3,1,4,2,1,2,3,4]},
                 behavSession = '20150319a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-18_17-16-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,6,1,2,6,3,2,3,6,6,0],2:[3,4,3,2,1,1,2,3,2,3,4,2],3:[3,3,3,3,7,3,3,3,3,3,3,3],4:[3,5,3,6,2,2,4,5,2,3,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,4,1,4,2,2,1,2,3,3],7:[3,3,2,2,3,2,3,3,3,4,4,2],8:[3,3,2,2,3,4,2,2,3,2,3,2]},
                 behavSession = '20150318a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-17_14-21-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,2,6,1,2,6,4,4,4,0],2:[3,7,3,2,2,3,2,1,4,4,3,0],3:[3,3,3,2,3,3,2,3,3,3,3,3],4:[3,2,2,2,2,2,3,2,2,2,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,3,4,4,3,4,1,3,3,1],7:[3,1,3,3,2,2,3,3,3,3,3,2],8:[3,4,3,3,3,2,4,3,3,3,3,2]},
                 behavSession = '20150317a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-16_17-21-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:[1],5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,5,2,4,7,1,6,3,4,3,1,4],2:[3,2,4,7,3,3,3,3,1,2,4,3],3:[3,3,3,3,3,2,3,3,3,3,2,3],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,2,4,3,4,3,3,3,4,3,3],6:[3,2,3,4,3,1,3,1,1,6,2,2],7:[3,6,2,2,1,3,3,3,2,1,4,3],8:[3,3,7,5,2,3,2,2,2,2,4,5]},
                 behavSession = '20150316a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-15_14-33-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,4,4,1,1,3,1,7,7,1,2],2:[3,3,3,3,4,3,4,3,2,2,2,4],3:[3,3,3,3,3,3,3,3,3,2,3,2],4:[3,3,2,4,3,3,5,3,3,2,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,4,7,5,1,2,3,4,2,2,2,3],7:[3,2,2,7,3,2,4,2,7,3,3,1],8:[3,3,2,3,4,3,2,4,2,3,2,3]},
                 behavSession = '20150315a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-13_13-28-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:(1,13)},
                 clusterQuality = {1:[3,3,1,3,1,3,7,4,3,3,3,1],2:[3,5,2,1,2,5,4,2,3,3,4,2],3:[3,3,3,3,4,4,4,2,3,3,3,3],4:[3,4,2,3,2,2,3,2,2,1,2,2],5:[3,4,2,3,3,3,3,3,3,3,2,8],6:[3,1,1,1,1,1,4,1,1,1,2,1],7:[3,3,1,5,2,1,4,2,7,2,4,7],8:[2,0,0,0,0,0,0,0,0,0,0,0]},
                 behavSession = '20150313a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-12_15-10-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,4,1,6,3,7,3,7,2,4,7],2:[3,3,3,3,3,2,3,3,1,3,3,3],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,1,2,4,6,1,1,1,1,7,7,1],7:[3,3,2,3,4,4,2,2,2,3,3,2],8:[3,3,3,3,2,3,5,2,2,1,3,3]},
                 behavSession = '20150312a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-11_14-48-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,12),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,2,4,6,2,1,3,4,3,1,1],2:[3,1,3,5,3,1,2,2,4,3,5,3],3:[3,3,3,3,2,3,3,3,3,3,3,3],4:[1,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,4,2,4,3,3,1,3,2,4,2],6:[3,4,2,4,1,1,1,1,1,4,3,0],7:[3,2,2,1,1,2,2,2,1,3,3,1],8:[3,3,2,3,4,2,2,2,2,2,3,4]},
                 behavSession = '20150311a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-10_15-59-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,12),4:range(1,12),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,8,5,3,2,8,8,2,6,5,8,3],2:[3,2,3,3,2,2,2,5,2,5,3,0],3:[3,3,2,3,3,3,2,3,2,3,2,0],4:[3,2,3,2,2,2,5,3,5,5,1,0],5:[3,3,2,3,2,3,2,5,3,3,3,3],6:[3,5,6,8,5,1,5,3,5,2,2,1],7:[3,5,2,5,2,2,5,2,5,3,5,0],8:[2,0,0,0,0,0,0,0,0,0,0,0]},
                 behavSession = '20150310a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-09_16-51-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,4,3,4,3,7,3,6,2,3,1],2:[3,4,3,3,3,1,4,3,3,3,3,3],3:[3,3,3,3,3,3,3,3,3,2,3,3],4:[3,1,1,1,1,3,2,1,1,2,3,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,3,3,2,4,2,7,2,2,1],7:[3,3,2,3,2,3,2,3,1,2,2,3],8:[3,2,2,3,3,2,2,2,2,3,3,3]},
                 behavSession = '20150309a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-06_14-12-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,12),4:range(1,13),5:range(1,13),6:range(1,12),7:range(1,12),8:range(1,13)},
                 clusterQuality = {1:[3,3,5,1,3,4,2,4,3,2,2,4],2:[3,4,3,3,3,3,3,3,3,5,5,3],3:[3,3,3,3,3,3,3,3,3,2,3,0],4:[3,3,3,3,1,1,1,1,4,2,3,2],5:[3,3,2,2,3,3,3,3,3,3,3,2],6:[3,4,7,4,3,6,2,2,3,2,4,0],7:[3,5,5,5,2,3,2,2,1,2,1,0],8:[1,0,0,0,0,0,0,0,0,0,0,0]},
                 behavSession = '20150306a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-05_15-48-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,2,3,3,2,3,2,2,3,4],2:[3,3,3,3,4,3,3,3,4,2,3,4],3:[3,3,3,3,3,3,2,3,3,3,3,2],4:[3,1,3,3,3,2,2,3,2,3,1,4],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,4,2,7,7,3,2,4,2,4,7,4],7:[3,3,2,3,1,3,3,2,1,3,3,2],8:[3,2,2,4,4,1,3,2,3,3,3,3]},
                 behavSession = '20150305a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-04_14-56-53',
                 clustersEachTetrode = {1:range(1,12),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,7,3,2,3,2,3,3,2,0],2:[3,3,3,3,4,3,3,2,3,3,3,3],3:[3,3,3,3,3,2,3,3,3,3,3,3],4:[3,3,3,1,3,3,3,3,2,4,3,2],5:[3,3,2,3,3,3,3,3,3,3,2,3],6:[3,7,3,7,3,3,3,3,2,1,3,6],7:[3,3,4,3,3,3,3,2,3,1,2,2],8:[6,0,0,0,0,0,0,0,0,0,0,0]},
                 behavSession = '20150304a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-03_18-44-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,2,3,3,3,1,2,3,2,2],2:[3,5,1,2,3,3,3,3,3,3,3,5],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,3,2,3,3,2,2,3,3,3,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,7,6,6,6,1,4,2,1,6,3,3],7:[3,2,2,3,3,3,3,3,2,2,2,2],8:[3,2,2,3,4,1,4,3,3,3,3,1]},
                 behavSession = '20150303a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-02_15-32-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,2,3,3,3,2,1,3,2,2],2:[3,2,4,3,1,3,3,3,2,5,3,3],3:[3,3,2,3,3,3,3,3,3,3,3,3],4:[3,4,3,2,4,2,3,2,3,2,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,7,1,7,2,3,7,1,3,6,1,1],7:[3,3,3,3,3,2,2,2,2,2,3,2],8:[3,3,3,1,2,3,1,1,1,3,4,2]},
                 behavSession = '20150302a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-01_18-37-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,2,3,3,3,3,2,2,3,3],2:[3,3,3,3,1,3,3,2,3,3,3,4],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,2,2,3,3,3,3,3,2,3,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,5,3,6,2,7,7,1,1,7,4,6],7:[3,2,3,3,3,3,3,3,2,3,3,3],8:[3,3,4,2,3,2,2,3,3,3,3,1]},
                 behavSession = '20150301a')
cellDB.append_session(oneES)

'''
oneES = eSession(animalName='test017',#################################################
                 ephysSession = '2015-02-28_20-10-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150228a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-27_14-55-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,6,6,4,2,3,3,3,3,6],2:[3,3,3,4,3,3,1,3,2,1,3,3],3:[3,3,3,2,3,3,3,3,3,3,3,3],4:[3,5,2,2,2,5,3,3,3,3,2,3],5:[3,3,3,3,3,3,3,2,2,2,2,3],6:[3,6,4,6,1,6,6,6,6,7,1,1],7:[1,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,3,2,5,3,3,2,2,2,2,0]},
                 behavSession = '20150227a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-26_16-31-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,4,2,2,3,1,3,3,2,2,3],2:[3,2,3,1,4,5,3,3,3,3,2,3],3:[3,3,3,3,3,2,3,2,2,3,2,3],4:[3,3,2,2,2,3,5,3,3,3,3,3],5:[3,5,3,2,3,2,2,3,2,3,1,3],6:[3,4,4,1,1,1,6,4,1,4,1,1],7:[3,2,6,3,2,3,3,2,2,2,3,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 behavSession = '20150226a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-25_14-04-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,12),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,1,3,5,3,4,3,3,4,2,3,0],3:[3,2,3,2,3,3,3,3,3,3,3,3],4:[3,3,3,3,3,3,3,2,1,1,2,3],5:[3,4,1,4,3,2,3,3,1,3,3,3],6:[3,1,1,4,4,6,4,3,1,1,3,4],7:[3,3,3,3,2,3,6,3,2,3,3,1],8:[3,3,3,2,2,2,2,3,3,3,3,2]},
                 behavSession = '20150225a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-23_15-31-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,3,3,3,3,2,2,2,3,3],2:[3,3,3,4,3,3,3,3,3,3,4,2],3:[3,3,3,2,3,2,3,3,3,3,4,3],4:[3,3,2,2,1,4,3,3,3,3,1,4],5:[3,2,1,3,3,4,3,3,2,3,3,3],6:[3,1,1,1,3,3,4,3,3,3,4,3],7:[3,6,4,3,2,3,7,3,3,3,2,4],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 behavSession = '20150223a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-21_20-08-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,2,3,1,3,3,2,3,2,3,2],3:[3,3,1,2,3,2,3,3,1,3,3,3],4:[3,3,2,3,2,2,3,3,3,3,2,3],5:[3,2,2,2,2,3,1,3,3,1,3,3],6:[3,3,3,3,1,3,2,3,3,5,3,3],7:[3,3,3,4,2,3,2,3,3,3,3,4],8:[3,2,3,2,3,2,2,3,3,3,2,3]},
                 behavSession = '20150221a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-17_12-26-10',
                 clustersEachTetrode = {1:(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,1,2,3,3,2,3,3,2,2,1],3:[3,3,3,2,2,5,2,3,2,2,3,3],4:[3,4,3,3,2,2,3,2,2,2,2,1],5:[3,3,2,3,2,4,3,2,3,4,2,3],6:[3,3,3,3,3,3,2,2,3,3,2,2],7:[3,2,3,4,3,3,3,3,3,2,2,3],8:[3,3,2,3,3,3,2,3,3,3,2,0]},
                 behavSession = '20150217a')
cellDB.append_session(oneES)

