'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase_quality_depth as celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

#Relative tetrode lengths
#    TT2: 0mm
#    TT3,TT4,TT5: 209um
#    TT7: 459um
#    TT1,TT8: 504um
#    TT6: 705um


oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-17_12-26-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,12),5:range(1,13),6:range(1,13),7:range(1,12),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0,],2:[3,2,1,4,2,3,1,3,4,3,3,1],3:[3,3,3,2,2,1,2,3,2,2,3,3],4:[3,2,3,3,2,2,3,2,2,2,2,1],5:[3,3,2,3,2,1,3,2,4,1,2,3],6:[3,4,2,3,3,3,2,2,3,3,2,2],7:[3,2,3,3,2,3,3,3,3,2,2,3],8:[3,3,3,2,1,2,2,1,1,3,2,0]},
                 depth = 2.159,
                 behavSession = '20150217a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-21_20-08-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,2,3,2,3,3,3,3,3,3,3],3:[3,3,2,3,3,3,3,3,3,3,3,0],4:[3,4,2,3,3,1,2,3,2,3,3,3],5:[3,3,3,3,3,2,3,2,3,2,3,3],6:[3,3,1,3,3,3,3,1,3,2,3,2],7:[3,3,3,2,3,2,3,3,3,3,1,1],8:[3,2,3,2,3,2,2,2,3,3,3,2]},
                 depth = 3.110,
		 behavSession = '20150221a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-23_15-31-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,3,3,3,3,3,2,2,3,3,3],2:[3,3,3,3,3,3,1,2,3,3,3,3],3:[3,3,2,3,3,3,3,3,3,3,3,3],4:[3,3,1,3,3,3,3,3,1,3,3,2],5:[3,3,3,3,1,3,3,3,3,2,3,3],6:[3,1,1,3,1,3,3,3,3,4,3,3],7:[3,3,3,3,3,3,3,3,1,3,3,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.268,
		 behavSession = '20150223a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-25_14-04-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,2,3,3,4,3,3,3,3,3,3],3:[3,3,3,4,3,1,1,3,3,1,3,3],4:[3,3,3,3,3,3,3,3,1,3,1,3],5:[3,3,3,3,1,3,3,3,3,2,3,3],6:[3,3,1,1,1,1,3,1,3,1,3,1],7:[3,3,3,3,3,3,3,3,3,3,3,3],8:[3,3,3,3,2,3,3,3,3,2,3,2]},
                 depth = 3.427,
		 behavSession = '20150225a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-26_16-31-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,2,3,1,3,1,3,3,3,2,2],2:[3,4,4,1,3,3,3,3,3,1,3,3],3:[3,3,3,3,3,3,4,3,3,3,3,3],4:[3,3,3,3,2,3,3,3,3,2,3,0],5:[3,2,3,3,3,3,3,3,1,3,3,3],6:[3,1,1,1,3,1,1,1,1,1,1,1],7:[3,2,3,1,3,1,1,3,3,2,3,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.427,
		 behavSession = '20150226a')
cellDB.append_session(oneES)  

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-27_14-55-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,1,3,3,3,3,3,3,3],2:[3,3,3,1,3,3,3,3,3,3,3,3],3:[3,3,3,3,3,3,3,3,3,2,3,3],4:[3,3,2,3,2,3,3,2,2,2,3,0],5:[3,3,2,3,3,3,2,2,3,3,2,3],6:[3,3,3,3,3,1,1,3,3,3,3,3],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,2,1,2,2,3,3,2,2,3,2,3]},
                 depth = 3.506,
		 behavSession = '20150227a')
cellDB.append_session(oneES)  

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-28_20-10-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,3,3,3,3,3,3,2,3,3],2:[3,3,3,3,3,3,3,3,4,3,3,3],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,3,3,3,3,3,3,3,3,3,3,3],5:[3,3,3,3,3,3,3,3,3,2,4,3],6:[3,3,3,3,3,3,1,3,3,3,3,3],7:[3,2,3,2,2,3,3,3,3,3,3,0],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.585,
		 behavSession = '20150228a')
cellDB.append_session(oneES)  

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-01_18-37-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,2,2,3,3],2:[3,3,3,3,3,4,3,3,3,3,3,2],3:[3,3,3,3,3,3,3,3,3,2,3,3],4:[3,3,3,2,3,2,3,3,3,3,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,1,4,1,1,1,1,1,3,3,1],7:[3,2,3,3,3,2,3,3,3,3,3,3],8:[3,3,3,3,3,3,3,2,2,1,3,3]},
                 depth = 3.585,
		 behavSession = '20150301a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-02_15-32-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,3,3,2,3,2,2,2,3,1],2:[3,2,2,3,3,1,3,3,1,3,3,3],3:[3,3,3,2,3,3,3,3,3,3,3,3],4:[3,2,3,2,2,3,3,3,3,3,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0,],6:[3,4,4,1,4,3,3,4,3,3,2,2],7:[3,3,3,3,2,2,3,3,3,2,2,0],8:[3,1,2,3,3,3,3,1,3,2,1,2]},
                 depth = 3.585,
		 behavSession = '20150302a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-03_18-44-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,3,3,3,3,3,2,2,3,1,3],2:[3,3,3,3,3,3,3,3,3,1,3,3],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,3,3,2,3,3,2,3,2,3,3,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,1,3,1,3,1,3,1,1,1,1],7:[3,2,2,3,3,2,3,3,2,3,2,3],8:[3,3,1,3,3,1,3,3,3,3,3,3]},
                 depth = 3.585,
		 behavSession = '20150303a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-04_14-56-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,1,3,3,2,3,3,3,2,1],2:[3,4,3,3,3,3,3,3,3,3,3,3],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,2,3,3,3,3,3,3,3,2,3,1],5:[3,3,3,3,3,3,2,3,3,3,3,0],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,3,3,3,3,3,3,3,2,2,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.585,
		 behavSession = '20150304a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-05_15-48-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,2,3,3,2,3,3,3,3,3,0],2:[3,1,3,3,1,3,3,3,3,3,3,3],3:[3,3,3,3,2,3,3,3,3,2,3,0],4:[3,3,3,1,3,2,3,1,1,3,1,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,3,3,3,4,1,4,2,4,4],7:[3,2,3,3,2,3,3,3,2,3,2,3],8:[3,4,3,3,2,4,3,3,3,4,2,2]},
                 depth = 3.585,
		 behavSession = '20150305a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-06_14-12-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,2,3,1,2,2,3,1,3,3],2:[3,1,3,2,3,3,3,3,3,3,3,3],3:[3,3,3,3,3,3,3,3,3,2,3,0],4:[3,1,3,2,1,3,3,3,1,1,1,0],5:[3,3,3,2,3,3,3,2,3,3,2,3],6:[3,3,1,4,4,2,3,2,3,3,3,3],7:[3,1,3,2,4,3,3,3,2,2,2,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.623,
		 behavSession = '20150306a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-09_16-51-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,1,3,4,3,3,3,2,3,1],2:[3,3,2,3,2,3,3,3,2,4,3,1],3:[3,3,3,3,3,3,3,3,3,2,3,3],4:[3,3,3,3,3,3,3,1,3,2,2,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,4,2,3,1,2,2,1,7,2],7:[3,3,2,3,4,2,3,3,3,3,2,3],8:[3,2,3,3,3,2,2,3,3,2,2,3]},
                 depth = 3.623,
		 behavSession = '20150309a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-10_15-59-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,2,3,3,2,1,3,3,3],2:[3,2,3,3,2,2,2,2,3,3,3,0],3:[3,3,2,3,3,3,2,3,3,3,3,0],4:[3,2,3,2,2,2,3,3,1,1,3,0],5:[3,3,2,3,2,3,2,3,3,3,3,3],6:[3,1,1,3,1,3,3,3,1,2,2,3],7:[3,3,2,3,2,2,1,2,1,3,1,0],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.664,
		 behavSession = '20150310a')
cellDB.append_session(oneES) 
'''
oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-10_16-21-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,1,3,3,2,3,1,1,2,0],2:[3,3,2,2,3,2,3,3,3,1,3,0],3:[3,3,2,3,2,3,3,3,3,3,2,3],4:[3,1,3,2,1,3,2,1,3,2,1,1],5:[3,3,3,3,3,3,3,3,2,3,3,3],6:[3,3,1,1,3,3,3,1,3,3,3,3],7:[3,2,2,2,3,1,3,2,3,3,2,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
		 behavSession = '20150310a')
cellDB.append_session(oneES) 
'''
oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-11_14-39-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,2,3,2,3,1,3,1,3,0],2:[3,3,3,2,3,3,3,2,3,3,0,0],3:[3,3,3,3,3,3,3,3,0,0,0,0],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,3,3,3,3,3,3,3,3,3,0],6:[3,1,1,2,2,1,3,1,1,3,3,0],7:[3,2,2,3,2,2,3,3,2,3,3,0],8:[3,2,2,3,3,2,3,3,3,3,0,0]},
                 depth = 3.664,
		 behavSession = '20150311a')
cellDB.append_session(oneES) 
'''
oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-11_14-48-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,3,3,3,3,3,3,3,3],2:[3,3,3,3,3,3,3,2,3,3,3,3],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[9,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,2,3,3,3,3,3,3,3,3,3],6:[3,1,3,3,1,3,3,3,3,3,1,3],7:[3,3,2,2,3,3,3,3,3,3,3,2],8:[3,2,2,3,3,2,2,3,3,3,2,3]},
		 behavSession = '20150311a')
cellDB.append_session(oneES) 
'''
oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-12_15-10-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,2,1,3,3,1,1,1,1,3,3],2:[3,3,3,2,3,2,3,3,3,3,3,2],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,3,3,1,1,1,3,1,3,4,3,0],7:[3,2,3,3,3,3,2,2,3,3,2,3],8:[3,2,3,4,1,4,2,3,3,2,3,2]},
                 depth = 3.704,
		 behavSession = '20150312a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-13_13-28-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,2,3,3,3,3,1,3,3,3],2:[3,3,3,3,2,2,3,3,3,3,2,0],3:[3,3,3,3,3,3,3,2,3,3,3,3],4:[3,2,2,3,2,3,3,3,3,1,3,4],5:[3,3,3,3,3,3,3,3,2,3,3,3],6:[3,1,3,2,1,3,3,3,3,3,3,3],7:[3,3,2,3,3,3,3,2,3,2,2,0],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 depth = 3.704,
		 behavSession = '20150313a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-15_14-33-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,3,3,3,3,3,3,3,3,0],2:[3,3,3,2,3,3,3,3,3,3,3,0],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,3,3,3,2,3,3,3,3,3,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,4,4,3,2,3,3,2,2,4,3,0],7:[3,2,2,2,3,3,3,3,3,3,3,3],8:[3,3,3,2,3,3,2,3,2,3,2,2]},
                 depth = 3.744,
		 behavSession = '20150315a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-16_17-21-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,2,3,0],2:[3,3,3,3,3,3,3,2,3,3,3,3],3:[3,3,2,3,3,3,3,3,3,3,3,3],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,3,3,3,2,3,3,3,3,3],6:[3,4,3,3,4,3,2,1,3,3,4,4],7:[3,3,3,3,3,3,3,2,3,3,3,3],8:[3,2,3,2,2,2,3,2,3,3,3,0]},
                 depth = 3.783,
		 behavSession = '20150316a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-17_14-21-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,3,2,1,4,3,3,3,3,3],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,2,3,3,3,3,3,3,3,3,3,3],4:[3,2,2,3,3,2,3,3,2,2,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,3,2,3,3,3,3,3,3,3],7:[3,3,3,2,2,2,3,3,3,3,3,2],8:[3,3,3,3,3,3,3,2,2,3,2,3]},
                 depth = 3.823,
		 behavSession = '20150317a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-18_17-16-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,3,3,3,3,2,1,1,3,3],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,2,2,2,3,3,3,3,3,3,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,3,1,3,3,3,3,2,3,3],7:[3,2,3,3,3,2,3,2,3,2,3,3],8:[3,3,2,1,2,3,3,2,3,3,3,3]},
                 depth = 3.823,
		 behavSession = '20150318a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-19_13-35-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,3,1,1,1,2,1,2,3],2:[3,3,3,2,3,3,2,3,3,3,3,3],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,3,2,3,3,3,3,3,3,3,3,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,4,3,3,3,3,2,3,3,3,0],7:[3,3,3,3,3,2,3,2,3,3,3,3],8:[3,3,2,3,3,3,3,3,2,3,3,3]},
                 depth = 3.862,
		 behavSession = '20150319a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-20_13-05-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,3,2,3,3,3,3,1,4,1],2:[3,3,3,3,2,3,2,3,3,3,2,2],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,2,3,3,2,2,3,2,3,3,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,3,3,3,3,3,3,3,3,3],7:[3,3,3,2,3,3,2,3,3,3,2,3],8:[3,3,3,2,2,3,1,3,3,3,2,2]},
                 depth = 3.862,
		 behavSession = '20150320a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-21_14-06-46',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,3,3,3,1,3,2,3,3,3],2:[3,3,2,3,3,1,3,3,3,3,2,0],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,2,3,3,3,3,2,3,3,2,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,3,2,3,3,3,2,3,2,3],7:[3,3,1,3,3,3,2,2,3,2,3,3],8:[3,2,3,2,3,2,1,3,2,3,3,0]},
                 depth = 3.862,
		 behavSession = '20150321a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-22_20-31-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,3,3,3,3,3,3,2,1,2],2:[3,3,3,3,3,3,3,2,3,3,2,3],3:[3,3,2,3,3,3,3,3,3,3,3,2],4:[3,2,2,3,2,3,3,3,2,3,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,2,3,3,3,3,3,3,3,3,3],7:[3,3,2,3,2,3,3,3,3,3,3,3],8:[3,4,2,1,3,2,3,2,3,3,3,3]},
                 depth = 3.902,
		 behavSession = '20150322a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-23_16-27-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,4,3,1,2,3,2,3,3,3,4],2:[3,3,3,3,3,3,2,2,3,3,3,3],3:[3,3,3,3,3,3,3,3,2,2,3,3],4:[3,3,2,3,4,3,3,2,2,4,2,4],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,3,1,3,2,2,2,3,2,3],7:[3,3,3,3,3,3,4,2,4,3,1,1],8:[3,3,1,2,1,3,2,2,3,2,2,0]},
                 depth = 3.902,
		 behavSession = '20150323a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-24_16-25-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,1,2,3,2,3,3,1,3,4,1],2:[3,3,3,3,3,3,3,2,2,2,3,2],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,3,3,2,3,3,3,2,2,3,3,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,4,2,2,2,3,3,3,3,3,2,2],7:[3,3,3,2,3,3,3,3,3,3,3,0],8:[3,3,3,3,3,3,3,3,3,3,3,3]},
                 depth = 3.902,
		 behavSession = '20150324a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-25_15-43-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,3,3,2,3,3,1,3,3,3,3],2:[3,3,3,3,3,3,3,2,3,3,3,3],3:[3,3,3,2,3,3,3,3,3,3,3,3],4:[3,3,2,3,3,3,3,3,3,2,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,2,3,3,3,2,2,3,3,3],7:[3,3,3,3,3,3,3,3,1,3,1,3],8:[3,1,3,2,2,3,3,3,3,3,3,3]},
                 depth = 3.902,
		 behavSession = '20150325a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-26_15-20-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,4,3,1,4,3,1,3,3,2,3],2:[3,3,3,3,3,3,3,2,3,3,2,3],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,2,3,3,2,3,3,3,3,2,3,4],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,3,1,2,3,3,3,2,3,3],7:[3,2,3,3,1,3,3,3,3,3,3,3],8:[3,3,3,3,1,3,3,2,3,3,3,3]},
                 depth = 3.902,
		 behavSession = '20150326a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-27_14-41-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,4,3,1,1,1,1,1,1,3,4],2:[3,2,3,2,2,2,3,3,3,3,2,3],3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,1,2,2,2,1,2,2,1,2,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,2,2,1,2,1,3,2,1,2],7:[3,1,1,2,1,2,3,3,1,3,1,1],8:[3,3,1,3,3,3,3,3,2,3,3,3]},
                 depth = 3.902,
		 behavSession = '20150327a')
cellDB.append_session(oneES)  
