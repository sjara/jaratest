'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase_quality as celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()
'''
oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-18_13-00-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,4,3,1,3,2,2,2,1,4,4],2:[3,6,3,3,3,3,4,2,2,1,
		 behavSession = '20150918a')
cellDB.append_session(oneES) 
'''

'''
oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-14_18-02-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,
		 behavSession = '20150914a')
cellDB.append_session(oneES) 
'''

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-13_16-00-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,2,3,3,3,3,3,3,3,2,3],2:[3,3,6,3,3,3,2,3,3,3,3,1],3:[3,4,3,1,1,1,3,1,4,1,3,4],4:[3,1,3,2,2,4,3,4,3,4,1,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,4,1,4,3,3,1,1,1],7:[3,4,3,6,1,3,3,3,4,2,3,3],8:[3,2,3,3,3,3,3,3,3,1,3,3]},
		 behavSession = '20150913a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-11_12-33-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,2,2,3,7,3,3,4,4,1,2],2:[3,3,3,4,2,1,1,1,4,1,4,0],3:[3,1,1,3,1,1,1,3,1,2,4,0],4:[3,1,4,4,2,4,1,2,2,3,4,2],5:[1,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,3,1,1,1,4,4,4,1,1,1],7:[3,3,1,2,2,3,4,3,3,2,1,1],8:[3,3,1,3,1,2,1,1,3,1,3,0]},
		 behavSession = '20150911a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-10_12-37-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,4,3,3,1,1,3,2,1,3],2:[3,1,1,3,1,3,1,3,3,3,2,3],3:[3,1,1,3,2,1,3,1,1,3,1,1],4:[3,1,2,1,3,2,3,3,1,1,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,1,3,1,1,1,1,3,1],7:[3,3,3,2,4,6,3,3,3,3,6,2],8:[3,2,6,3,3,1,3,3,1,3,3,3]},
		 behavSession = '20150910a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-09_13-29-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,3,2,1,1,1,3,2,1,4],2:[3,2,3,6,4,1,3,3,1,4,1,4],3:[3,3,1,1,2,1,4,4,1,4,3,0],4:[3,4,2,3,2,4,2,4,3,4,3,2],5:[4,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,1,4,1,3,4,1,1,1],7:[3,6,3,3,3,3,2,4,4,4,3,1],8:[3,2,2,3,3,1,4,1,3,3,2,2]},
		 behavSession = '20150909a')
cellDB.append_session(oneES) 

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-02_14-34-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,1,1,4,4,2,6,1,0],2:[3,1,3,1,2,1,1,1,1,6,1,1],3:[3,1,1,1,6,4,2,1,4,1,1,3],4:[3,4,3,1,2,2,1,1,1,1,5,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,2,1,1,1,1,1,1,1],7:[3,2,6,4,2,1,1,4,1,1,3,1],8:[3,4,6,4,1,1,6,1,2,3,4,0]},
		 behavSession = '20150902a')
cellDB.append_session(oneES) 


oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-01_14-06-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,4,2,1,1,1,2,1,4],2:[3,1,2,1,1,1,1,1,6,1,1,1],3:[3,2,4,4,1,1,1,1,2,1,1,4],4:[3,1,1,4,1,4,4,4,1,2,1,2],5:[1,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,1,1,1,1,1,1,1,1],7:[3,1,4,4,2,2,1,1,2,1,2,1],8:[3,4,2,4,1,4,2,1,1,2,1,2]},
		 behavSession = '20150901a')
cellDB.append_session(oneES) 


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-28_11-14-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,1,2,1,2,3,1,3,0],2:[3,1,1,2,4,1,1,4,3,1,1,1],3:[3,2,4,4,1,4,1,1,1,1,1,1],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,2,2,1,3,1,5,1,4,2,2],6:[3,1,1,1,1,1,1,1,1,1,4,1],7:[3,2,1,1,4,2,2,1,3,4,4,3],8:[3,2,1,1,1,3,2,1,2,4,3,3]},
		 behavSession = '20150828a')
cellDB.append_session(oneES) 


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-27_11-56-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,4,1,1,1,1,1,2,1,3,1],2:[3,1,1,2,1,1,3,1,1,1,1,1],3:[3,2,1,1,1,1,1,1,1,1,1,1],4:[2,0,0,0,0,0,0,0,0,0,0,0],5:[3,1,2,1,3,2,2,1,2,2,1,0],6:[3,1,1,1,1,1,1,1,1,1,1,1],7:[3,2,5,5,2,3,2,4,2,1,1,2],8:[3,2,1,3,1,2,1,4,2,2,1,4]},
		 behavSession = '20150827a')
cellDB.append_session(oneES) 


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-21_16-54-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,4,1,3,4,4,2,1,2,1,4],2:[3,1,1,1,1,1,4,3,1,1,2,1],3:[3,1,4,4,4,4,4,2,7,4,4,4],4:[3,4,2,2,2,2,4,4,2,2,2,3],5:[6,0,0,0,0,0,0,0,0,0,0,0],6:[3,4,4,1,1,2,4,1,4,1,4,1],7:[3,2,1,1,1,5,2,3,2,2,2,3],8:[3,4,1,1,3,2,2,1,3,1,1,3]},
		 behavSession = '20150821a')
cellDB.append_session(oneES) 


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-19_12-53-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,2,1,1,1,2,3,0],2:[3,1,1,1,1,1,4,1,2,1,1,1],3:[3,3,3,2,4,1,2,1,7,1,3,4],4:[3,2,2,3,8,4,8,2,4,2,6,1],5:[6,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,4,1,4,1,1,4,4,1,1,3],7:[3,3,2,7,2,4,2,2,2,2,2,3],8:[3,2,3,3,2,2,6,2,2,4,2,3]},
		 behavSession = '20150819a')
cellDB.append_session(oneES) 


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-18_17-32-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,3,1,2,1,1,1,3,1,2],2:[3,1,1,4,1,2,1,1,1,4,3,1],3:[3,3,2,2,1,1,1,4,1,1,3,0],4:[3,8,2,1,3,3,6,1,4,1,1,2],5:[6,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,1,1,1,1,1,1,1,1,1,0],7:[3,1,2,2,5,4,2,5,5,5,3,6],8:[3,2,2,1,3,2,3,1,3,3,2,3]},
		 behavSession = '20150818a')
cellDB.append_session(oneES) 


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-17_15-22-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,6,1,1,1,3,2,2,4,3],2:[3,4,4,2,1,4,1,1,3,1,3,2],3:[3,4,1,4,4,1,4,3,2,4,4,4],4:[3,2,4,3,2,7,2,6,3,1,3,3],5:[1,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,1,1,4,4,1,1,4,3],7:[3,3,3,1,6,4,2,2,5,2,1,0],8:[3,3,2,4,4,3,3,3,3,3,2,2]},
		 behavSession = '20150817a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-14_13-12-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,1,3,1,1,3,2,2,3,1],2:[3,1,3,1,4,1,1,1,2,4,1,3],3:[4,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,1,4,2,3,2,2,1,2,3,2],5:[3,3,7,7,3,2,7,3,4,2,6,3],6:[3,4,1,1,1,3,4,4,4,1,2,0],7:[3,4,2,2,4,7,2,3,3,3,3,7],8:[3,3,3,3,3,2,3,3,3,2,3,3]},
		 behavSession = '20150814a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-13_16-59-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,1,3,2,3,4,7,2,3,0],2:[3,1,4,3,3,1,2,2,1,4,3,4],3:[3,4,1,4,2,4,3,3,3,4,2,4],4:[3,2,3,2,2,4,6,3,2,4,1,6],5:[6,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,1,1,3,3,1,1,1,3],7:[3,3,3,2,2,1,2,7,2,4,3,3],8:[3,3,3,3,2,3,3,3,2,3,3,3]},
		 behavSession = '20150813a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-12_11-14-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,3,3,3,1,1,3,2,3,2,4],2:[3,2,3,3,1,1,3,1,3,4,1,1],3:[3,3,3,4,6,2,3,1,4,1,3,0],4:[3,2,3,2,1,3,3,8,2,3,1,1],5:[6,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,2,3,3,1,3,1,2,1,3],7:[3,7,6,3,3,3,3,3,2,2,3,3],8:[3,2,3,3,2,3,3,1,2,3,3,3]},
		 behavSession = '20150812a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-11_11-14-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,3,1,1,2,1,2,4,4,2,2],2:[3,1,1,3,4,1,2,1,1,4,3,0],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,3,3,7,3,2,1,3,7,7,1,2],5:[3,2,2,3,2,3,3,7,3,7,7,2],6:[3,8,4,7,7,1,4,3,4,1,4,0],7:[3,2,1,3,3,1,3,1,3,1,2,3],8:[3,4,3,3,3,3,4,7,2,3,4,0]},
		 behavSession = '20150811a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-10_15-17-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,2,1,1,1,1,1,1,2,4,2],2:[3,1,1,1,1,1,1,2,3,1,3,0],3:[3,1,6,1,1,1,4,2,3,3,4,4],4:[3,2,2,3,2,3,3,2,2,2,1,7],5:[6,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,1,3,4,1,1,1,1,3,1],7:[3,5,2,4,1,2,1,2,3,3,2,4],8:[3,4,1,1,1,3,2,4,2,3,3,3]},
		 behavSession = '20150810a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-07_16-05-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[4,0,0,0,0,0,0,0,0,0,0,0],2:[3,4,7,3,3,2,3,4,1,1,1,1],3:[3,4,2,6,4,2,6,3,7,1,3,6],4:[3,3,1,1,1,1,1,2,1,3,1,1],5:[3,5,2,3,3,3,2,7,1,6,2,2],6:[3,3,2,4,1,4,1,4,1,1,3,1],7:[3,3,2,2,2,3,7,5,3,2,4,0],8:[3,2,3,3,2,4,3,3,2,2,2,3]},
		 behavSession = '20150807a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-06_13-29-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,4,7,4,1,2,2,1,1,3,2],2:[4,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,4,1,3,1,4,1,4,2,3,1],4:[3,1,2,5,3,1,1,1,2,2,1,1],5:[3,5,2,2,3,6,2,1,2,1,2,0],6:[3,4,2,1,1,3,1,1,1,2,2,0],7:[3,7,2,5,8,2,7,3,1,2,3,2],8:[3,1,1,2,2,3,2,4,2,2,3,4]},
		 behavSession = '20150806a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-04_11-21-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,4,2,1,2,3,3,3,2,0],2:[3,1,4,4,2,2,3,3,2,2,2,1],3:[3,1,1,3,4,4,4,2,4,3,1,4],4:[3,1,2,1,2,4,1,1,2,2,1,3],5:[3,2,2,2,6,4,6,3,3,2,1,2],6:[3,1,4,2,1,3,1,2,2,1,1,1],7:[3,4,4,2,1,3,1,3,2,2,7,0],8:[2,0,0,0,0,0,0,0,0,0,0,0]},
		 behavSession = '20150804a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-03_16-12-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,4,2,2,3,4,2,2,4,2,2],2:[3,2,3,4,4,2,2,4,2,2,3,2],3:[3,2,1,4,2,1,1,2,3,1,1,3],4:[3,1,2,3,2,1,6,4,4,2,1,2],5:[3,1,4,3,6,4,2,3,2,6,2,0],6:[3,2,2,2,2,1,1,1,2,3,1,2],7:[3,1,3,1,2,5,4,7,2,4,2,3],8:[2,0,0,0,0,0,0,0,0,0,0,0]},
		 behavSession = '20150803a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-01_13-35-46',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,2,3,7,2,1,2,1,1,2,0],2:[3,4,2,3,7,2,1,4,1,4,2,0],3:[3,2,2,1,3,4,6,2,1,1,3,2],4:[3,4,2,6,3,4,6,2,2,4,0,0],5:[3,2,6,1,2,3,1,4,1,1,4,5],6:[3,4,1,1,2,1,1,5,2,1,4,3],7:[3,8,2,5,2,1,8,4,2,7,1,2],8:[2,0,0,0,0,0,0,0,0,0,0,0]},
		 behavSession = '20150801a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-31_14-40-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[4,0,0,0,0,0,0,0,0,0,0,0,0],2:[3,2,4,3,3,2,3,2,2,1,3,2],3:[3,3,1,4,1,3,3,2,5,3,2,5],4:[3,1,1,2,1,1,1,2,1,1,1,0],5:[3,1,1,3,1,1,4,3,2,2,4,3],6:[3,1,1,4,1,3,2,1,6,1,4,3],7:[3,3,4,1,2,2,7,7,4,3,2,6],8:[3,1,3,3,4,2,3,4,3,2,3,0]},
		 behavSession = '20150731a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-30_16-33-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[1,0,0,0,0,0,0,0,0,0,0,0,0],2:[3,1,3,1,4,3,1,2,2,2,2,2],3:[3,1,1,4,4,2,2,3,4,2,1,4],4:[3,1,5,2,2,1,4,1,4,1,4,0],5:[3,4,3,2,7,6,2,2,1,1,2,2],6:[3,2,2,2,1,4,4,3,4,2,4,1],7:[3,1,3,2,1,6,1,6,8,2,2,1,2],8:[3,3,5,4,4,2,1,2,2,3,2,6]},
		 behavSession = '20150730a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-29_10-26-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,8,2,3,1,2,4,3,3,2,4],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,3,2,4,3,2,3,2,2,4,3,4],4:[3,1,2,1,2,3,3,1,2,4,3,0],5:[3,3,3,2,2,4,3,4,1,2,2,3],6:[3,2,2,3,3,4,4,4,2,4,2,0],7:[3,3,3,7,3,8,2,7,2,7,2,7],8:[3,3,1,1,3,2,3,3,2,3,2,2]},
		 behavSession = '20150729a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-28_13-54-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,4,2,1,2,4,3,4,4,2,2],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,3,4,5,4,2,1,2,3,2,2,1],4:[3,1,2,1,6,2,3,4,2,4,4,0],5:[3,2,4,2,2,4,5,2,1,3,3,0],6:[3,3,2,4,2,2,4,1,2,4,2,0],7:[3,2,6,2,7,1,6,6,2,2,2,0],8:[3,2,3,1,2,3,2,2,2,4,5,1]},
		 behavSession = '20150728a')
cellDB.append_session(oneES)  


oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-27_16-03-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,4,4,4,2,4,4,2,2,2,3],2:[2,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,2,1,2,4,4,2,5,3,2,2],4:[3,4,1,2,2,4,4,1,1,4,0,0],5:[3,2,4,4,4,2,1,2,2,2,2,4],6:[3,4,2,4,4,2,2,4,2,1,2,1],7:[3,2,2,2,1,2,1,2,4,2,4,0],8:[3,2,4,5,3,3,1,1,4,2,4,3]},
		 behavSession = '20150727a')
cellDB.append_session(oneES)  


