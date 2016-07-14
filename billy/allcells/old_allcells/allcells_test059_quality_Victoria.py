'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase_quality as celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-17_21-36-38 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,1,3,1,2,1,2,1],2:[3,1,2,3,6,2,1,1,3,4,3,4],3:[3,3,1,2,2,1,2,1,1,2,2,2],4:[3,1,2,2,3,1,1,2,1,2,1,1],5:[3,3,2,2,4,2,1,2,2,1,2,0],6:[3,6,6,1,1,6,1,1,1,3,3,3],7:[3,1,1,1,1,3,1,1,2,1,1,0],8:[3,4,4,4,2,2,4,2,1,2,1,3]},
		 behavSession = '20150702a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-18_14–41-21 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,1,1,1,1,1,1,1,1,3],2:[3,1,3,4,3,4,2,4,4,2,2,1],3:[3,2,2,1,3,2,2,3,1,1,2,1],4:[3,1,1,3,1,1,1,1,1,1,1,1],5:[3,2,2,2,2,3,4,3,4,1,1,1],6:[3,4,4,1,4,1,4,1,1,1,1,4],7:[3,1,1,1,1,1,1,1,4,1,1,1],8:[4,0,0,0,0,0,0,0,0,0,0,0]},
		 behavSession = '20150618a')
cellDB.append_session(oneES)  m

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-19_14–05-19 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,1,1,1,1,1,1,3,4],2:[3,3,2,3,2,4,2,4,2,1,1,1],3:[3,1,2,2,1,2,1,2,2,4,1,2],4:[3,1,1,1,1,1,1,1,1,1,1,0],5:[3,2,2,2,3,2,4,4,2,1,2,1],6:[3,4,1,1,1,1,1,1,1,4,1,4],7:[3,1,1,1,1,4,1,1,1,1,2,4],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
		 behavSession = '20150619a')
cellDB.append_session(oneES)  m

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-22_15–21-02 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,3,1,1,2,4,1,2,1,1,4,1],2:[3,1,2,3,2,4,2,1,1,1,2,0],3:[3,2,4,2,2,3,2,1,2,2,2,1],4:[3,1,1,2,1,1,4,2,1,1,1,4],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,4,1,1,1,1,1,1,1,1,3],7:[3,1,1,1,1,1,3,1,1,1,1,0],8:[3,2,3,1,1,1,3,5,2,2,1,2]},
		 behavSession = '20150622a')
cellDB.append_session(oneES)  m

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-23_15–05-47 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,1,2,3,1,1,1,1,1,4,1],2:[3,2,3,1,2,1,1,2,1,2,1,1],3:[3,1,2,1,2,2,2,3,1,2,2,3],4:[3,1,1,1,1,1,1,2,1,1,3,1],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,5,5,4,2,1,4,1,1,5,1,1],7:[3,1,1,1,1,1,1,1,1,1,1,1],8:[3,1,1,2,2,2,2,3,1,3,3,3]},
		 behavSession = '20150622a')
cellDB.append_session(oneES)  m

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-24_13–38-31 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,4,1,1,1,1,1,3,1,1,1],2:[3,1,2,1,1,2,2,1,2,4,4,0],3:[3,2,2,2,1,1,3,2,1,2,2,3],4:[3,1,1,1,3,1,2,1,2,1,1,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,3,4,5,1,4,1,4,1,1],7:[3,1,1,1,1,1,1,2,2,1,1,1],8:[3,2,1,2,2,1,2,3,3,4,1,1]},
		 behavSession = '20150624a')
cellDB.append_session(oneES)  m

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-25_15–22-32 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,4,1,3,1,3,1,1,2,4,3],2:[3,3,1,2,3,1,3,2,3,3,3,3],3:[3,2,2,1,3,3,1,1,3,1,2,3],4:[3,1,1,1,1,1,1,1,1,1,1,3],5:[3,2,3,2,3,2,2,2,4,2,3,3],6:[3,3,1,5,5,5,5,3,4,5,1,5],7:[3,1,1,1,3,1,1,1,1,3,3,1],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
		 behavSession = '20150625a')
cellDB.append_session(oneES)  m

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-26_15–28-39 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,3,1,1,3,2,1,1,1,1,3],2:[3,4,1,2,1,2,5,2,3,1,2,2],3:[3,2,3,2,2,2,2,1,1,2,4,0],4:[3,1,1,1,2,1,1,1,2,3,1,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,4,1,4,4,5,4,8,5,8,4,5],7:[3,1,1,2,1,1,2,1,5,1,4,4],8:[3,1,1,4,2,2,2,2,1,3,1,0]},
		 behavSession = '20150626a')
cellDB.append_session(oneES)  m

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-26_15–46-23 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,4,1,1,1,2,4,3,1,3,1,4],2:[3,2,1,2,1,2,3,3,3,3,3,3,0],3:[3,1,3,3,2,1,2,3,3,2,1,3],4:[3,3,1,2,1,1,1,1,1,1,1,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,1,3,5,1,5,5,3,3,3,3],7:[3,2,2,1,1,3,2,1,1,1,1,1],8:[3,2,3,3,2,2,2,1,3,3,3,3]},
		 behavSession = '20150626a')
cellDB.append_session(oneES)  m

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-28_17–10-44 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,4,3,3,1,1,1,1,2,3,2],2:[3,1,4,3,1,3,2,1,2,2,4,0],3:[3,2,3,2,2,2,3,1,3,1,0,0],4:[3,4,4,4,2,2,3,4,4,4,4,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,5,1,1,3,2,5,5,5,5,5,5],7:[3,1,1,1,3,1,2,2,3,2,2,4],8:[3,2,2,3,3,4,4,3,4,3,4,3]},
		 behavSession = '20150628a')
cellDB.append_session(oneES)  m

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-29_18–01-08 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,2,1,1,3,4,1,1,4,3,2,1],2:[3,5,1,4,3,2,2,3,1,2,4,2],3:[3,0,0,0,0,0,0,0,0,0,0,0],4:[3,2,4,2,1,4,1,1,1,2,3,2],5:[3,3,2,4,1,1,2,4,2,1,3,0],6:[3,5,3,5,5,1,4,3,4,5,5,3],7:[3,1,1,4,1,1,1,1,1,1,1,2],8:[3,3,4,3,3,3,3,3,2,3,2,2]},
		 behavSession = '20150629a')
cellDB.append_session(oneES)  m

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-30_16–34-20 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,3,1,1,2,3,1,1,4,3],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,2,3,2,3,1,2,2,2,1,3],4:[3,3,2,2,2,4,2,3,3,1,1,2],5:[3,1,4,4,3,3,3,2,2,3,3,2],6:[3,5,5,5,2,5,4,3,5,3,5,5],7:[3,3,22,2,1,1,1,2,1,3,1,1],8:[3,3,4,3,3,1,2,3,2,2,2,0]},
		 behavSession = '20150630a')
cellDB.append_session(oneES)  m

oneES = eSession(animalName='test059',
                 ephysSession = '2015-07-01_15–26-17 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[,,,,,,,,,,,],2:[,,,,,,,,,,,],3:[,,,,,,,,,,,],4:[,,,,,,,,,,,],5:[,,,,,,,,,,,],6:[,,,,,,,,,,,],7:[,,,,,,,,,,,],8:[,,,,,,,,,,,]},
		 behavSession = '20150701a')
cellDB.append_session(oneES)  m

oneES = eSession(animalName='test059',
                 ephysSession = '2015-07-02_15–37-40 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 clusterQuality = {1:[3,1,2,1,1,1,2,2,1,3,1,1],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,3,1,2,2,1,2,1,1,2,2,2],4:[3,4,2,2,3,1,1,2,1,2,3,1],5:[3,3,2,2,3,2,3,2,2,1,2,0],6:[3,5,1,1,1,1,2,1,4,4,3,3],7:[3,1,1,1,1,3,1,1,2,4,1,0],8:[3,3,4,3,2,2,3,2,1,2,2,3]},
		 behavSession = '20150702a')
cellDB.append_session(oneES)  m
