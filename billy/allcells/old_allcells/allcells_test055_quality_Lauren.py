'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()
'''
#This is clustering for tuning curves
oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-17_17-52-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = 'test055_tuning_curve_20150517a.h5')
cellDB.append_session(oneES)

#This is clustering for tuning curves
oneES = eSession(animalName='test055',
                 ephysSession = '2015-06-01_12-40-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = 'test055_tuning_curve_20150601a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-20_13-31-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,1,2,2,2,3,2,3,3,3,3,3],2:[3,3,3,2,2,3,2,4,4,2,3,0],3:[3,2,2,2,1,2,2,2,2,3,2,2],4:[3,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,2,3,2,3,2,3,3,3,3,3],6:[3,3,2,2,2,2,3,2,2,2,2,2],7:[3,2,2,2,3,2,3,3,2,2,2,2],8:[3,1,1,2,3,4,1,3,1,1,1,1]},
                 behavSession = '20150420a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-19_15-12-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,4,3,3,3,2,2,2,3,3,3],2:[3,2,3,3,4,4,2,3,3,3,2,3],3:[3,4,2,4,3,3,1,4,2,2,4,3],4:[3,3,3,2,3,3,3,3,3,3,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,2,2,3,2,2,2,2,2,2],7:[3,2,2,2,3,2,2,2,2,2,2,2],8:[3,1,1,4,1,2,3,3,3,1,1,1]},
                 behavSession = '20150419a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-18_15-43-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
\clusterQuality ={1:[3,3,2,2,2,3,3,3,1,1,3,3],2:[3,3,2,4,3,3,3,3,3,3,3,2],3:[3,2,3,3,2,3,3,2,3,2,3,3],4:[3,3,2,3,2,3,3,3,3,3,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,2,2,2,3,2,3,2,3,3,3],7:[3,3,3,2,3,2,2,3,2,4,2,2],8:[3,3,1,4,3,3,3,3,1,3,1,2]},
                 behavSession = '20150418a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-14_12-09-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,3,2,3,4,3,3,3,3,2,0],2:[3,2,3,3,3,3,3,3,2,2,2,1],3:[3,2,3,1,2,3,2,3,3,3,3,0],4:[3,2,3,2,3,2,3,2,3,3,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,2,3,3,2,2,3,2,2,3,2],7:[3,2,2,2,3,2,2,2,3,3,3,2],8:[3,3,3,1,3,3,3,3,1,1,3,4]},
                 behavSession = '20150414a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-13_00-14-37',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,3,3,3,4,3,3,3,3,3,0],2:[3,2,3,2,3,3,3,3,4,2,3,0],3:[3,2,3,3,2,2,1,1,4,3,2,3],4:[3,3,3,2,3,2,2,2,2,3,3,2],5:[3,2,3,2,2,2,2,2,3,2,3,2],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,2,3,2,3,2,2,2,2,2,2],8:[3,2,4,3,3,3,3,3,2,3,3,3]},
                 behavSession = '20150412a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-11_18-30-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,4,1,4,4,3,3,2,3,2,3],2:[3,3,3,4,2,3,3,3,3,3,3,3],3:[3,3,3,2,2,3,3,3,4,2,1,2],4:[3,3,2,2,2,3,2,2,2,3,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,2,3,3,2,3,2,3,2,2],7:[3,2,3,2,3,3,2,2,3,3,2,3],8:[3,3,1,3,3,1,3,1,1,1,3,1]},
                 behavSession = '20150411a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-10_12-34-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,3,2,3,4,3,4,4,3,3,3],2:[3,1,2,3,3,3,1,3,3,2,3,3],3:[3,2,3,2,3,3,1,1,1,3,2,3],4:[3,2,3,3,4,2,3,2,2,2,2,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,2,3,2,2,2,2,2,3,0],7:[3,2,3,2,2,3,2,2,3,2,4,2],8:[3,3,1,1,1,3,3,3,3,3,3,3]},
                 behavSession = '20150410a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-09_12-17-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,3,3,3,3,3,3,3,1,3,3],2:[3,2,3,3,2,3,4,1,3,3,3,3],3:[3,4,2,3,3,4,4,3,3,2,3,0],4:[3,2,2,2,2,3,3,2,3,3,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,2,2,3,2,2,2,2,3,3,3],7:[3,2,2,3,3,2,2,2,2,3,3,0],8:[3,3,1,2,1,4,1,3,4,4,3,3]},
                 behavSession = '20150409a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-08_12-12-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,3,3,3,3,3,3,3,3,3,3],2:[3,3,3,3,3,3,3,3,1,3,3,3],3:[3,4,2,3,3,4,2,2,3,3,3,2],4:[3,2,3,3,3,2,3,2,1,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,3,3,3,3,2,2,3,3,2],7:[3,3,3,3,2,3,2,3,1,4,2,2],8:[3,3,2,4,1,1,1,3,1,3,1,1]},
                 behavSession = '20150408a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-07_19-08-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,3,3,4,2,3,3,3,3,3,3],2:[3,1,1,3,3,2,2,3,3,3,3,2],3:[3,2,2,3,2,2,2,3,3,4,2,3],4:[3,3,3,2,3,3,2,3,3,3,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,2,4,3,3,2,3,2,2,2],7:[3,3,3,3,3,2,2,2,3,2,3,2],8:[3,3,1,1,1,3,3,3,3,3,1,3]},
                 behavSession = '20150407a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-06_15-15-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,1,4,4,2,3,3,3,3,3,0],2:[3,3,2,2,2,3,3,3,3,4,3,0],3:[3,2,2,2,2,3,3,3,3,2,2,3],4:[3,3,2,3,3,2,3,2,3,2,3,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,3,3,3,2,2,3,2,3,3],7:[3,3,3,2,3,3,2,3,2,2,3,2],8:[3,3,1,1,2,3,4,3,3,3,3,3]},
                 behavSession = '20150406a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-31_11-50-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,3,3,2,3,3,3,3,3,3,3],2:[3,3,3,2,4,3,2,1,4,3,2,3],3:[3,2,3,2,3,4,2,3,3,4,2,3],4:[3,2,3,3,4,3,3,2,2,3,2,2],5:[3,2,2,2,2,3,3,3,2,3,3,2],6:[3,3,3,2,3,2,3,2,3,2,3,2],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,4,3,3,1,3,3,1,1,4,1]},
                 behavSession = '20150331a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-30_12-32-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,1,2,1,3,3,3,4,3,3,2,3],2:[3,3,3,2,1,2,3,1,3,3,3,2],3:[3,2,2,3,3,2,3,2,3,3,2,3],4:[3,3,2,3,3,3,3,2,3,3,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,3,3,3,2,2,2,2,2,3],7:[3,2,3,3,2,3,2,3,2,3,3,3],8:[3,3,3,3,2,3,3,1,1,3,3,3]},

                 behavSession = '20150330a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-27_12-31-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,3,2,3,3,3,3,3,3,3,0],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,2,3,2,2,2,2,3,2,3,3,3],4:[3,1,2,2,3,2,3,2,2,2,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,3,2,2,3,4,2,2,2,2],7:[3,2,3,2,2,3,2,3,3,2,3,0],8:[3,3,3,3,3,3,3,2,3,3,3,3]},
                 behavSession = '20150327a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-26_11-18-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,2,3,3,3,3,3,3,3,3,3],2:[3,3,3,3,3,3,3,3,3,3,3,3],3:[3,2,2,3,2,2,3,2,3,3,2,2],4:[3,2,2,3,3,3,3,3,2,2,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,3,2,3,3,3,3,2,3,2],7:[3,2,2,3,2,3,3,3,2,2,3,2],8:[3,3,3,3,3,3,3,3,3,3,3,3]},
                 behavSession = '20150326a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-25_12-44-37',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,4,1,2,2,3,3,2,3,2,3,3],2:[3,3,3,3,3,4,3,3,1,4,2,3],3:[3,2,3,2,3,2,2,2,3,3,2,3],4:[3,1,3,3,2,3,3,1,2,3,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,3,3,2,2,2,2,2,2,3],7:[3,2,2,2,2,3,2,2,2,3,2,2,],8:[3,3,1,3,2,3,3,1,1,3,3,4,]},
                 behavSession = '20150325a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-24_12-33-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,2,4,2,3,3,3,3,3,3,3,3],2:[3,2,3,3,3,3,3,2,3,3,3,3],3:[3,3,2,2,2,3,2,3,2,3,2,2],4:[3,3,3,3,3,3,3,3,2,2,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,2,2,3,2,2,3,2,3,2],7:[3,2,3,2,2,2,2,3,2,3,2,0],8:[3,2,3,2,3,3,3,3,3,3,3,3]},
                 behavSession = '20150324a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-23_12-39-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,3,1,4,4,3,3,3,2,4,3],2:[3,1,3,4,3,3,3,3,4,3,3,3],3:[3,3,3,3,2,2,2,2,2,3,2,2],4:[3,3,2,3,1,4,1,2,2,2,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,3,2,3,3,3,2,2,3,2],7:[3,3,2,2,2,2,3,3,3,3,3,2],8:[3,4,2,1,3,4,4,3,3,3,2,3]},

                 behavSession = '20150323a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-22_19-01-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,3,2,3,3,3,3,3,3,3,3],2:[3,3,3,3,3,3,3,3,3,2,3,0],3:[3,2,3,2,2,2,3,3,2,2,3,3],4:[3,2,3,3,1,2,2,2,3,3,2,1],5:[3,2,3,2,2,2,2,2,2,2,3,3],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,3,3,2,3,2,3,2,2,3,2],8:[3,1,1,4,3,3,3,1,2,3,4,4]},
                 behavSession = '20150322a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-21_15-33-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,2,3,3,3,2,2,3,4,3,3,3],2:[3,3,3,3,1,1,3,3,4,2,3,3],3:[3,2,2,2,3,3,3,2,2,2,2,3],4:[3,4,3,2,3,2,2,3,3,2,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,1,2,3,2,3,3,3,2,3,2,2],7:[3,3,3,2,2,3,3,2,2,3,2,3],8:[3,3,3,3,1,2,3,3,3,1,1,3]},
                 behavSession = '20150321a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-19_15-04-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,3,3,3,3,3,3,2,3,2,2],2:[3,1,3,4,2,1,4,3,2,2,1,1],3:[3,2,2,2,2,2,3,3,3,3,2,2],4:[3,3,3,3,3,2,3,2,2,2,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,3,1,3,3,2,3,3,2,2],7:[3,3,3,3,2,3,2,2,1,2,3,2],8:[3,1,1,2,2,3,3,1,1,4,1,1]},
                 behavSession = '20150319a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-18_15-42-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,2,3,3,3,3,2,3,3,3,3,3],2:[3,3,3,2,3,3,3,3,3,2,2,3],3:[3,2,3,3,3,2,2,2,2,2,2,2],4:[3,3,2,3,2,3,2,2,1,3,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,3,3,3,3,2,3,3,2,2],7:[3,3,2,2,2,3,3,3,2,3,3,0],8:[3,3,1,4,1,3,3,1,4,2,3,3]},
                 behavSession = '20150318a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-16_11-20-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,2,3,3,3,3,3,3,2,3,3,3],2:[3,3,3,2,2,3,2,3,3,2,2,0],3:[3,3,3,3,3,3,2,3,2,3,3,3],4:[3,2,2,3,2,2,2,2,3,2,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,2,3,3,3,3,3,3,2,2,],7:[3,3,3,3,3,3,2,1,3,3,3,2],8:[3,1,1,3,1,1,1,1,3,3,3,2]},
                 behavSession = '20150316a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-15_13-08-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,4,3,2,3,2,3,3,3,2,3],2:[3,3,2,2,3,3,3,3,2,4,3,2],3:[3,2,2,3,3,3,3,2,2,2,3,3],4:[3,3,2,2,3,4,3,2,3,3,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,3,3,3,2,3,3,3,3,3],7:[3,2,2,3,3,3,2,2,3,3,3,3],8:[3,1,2,3,3,4,3,1,3,3,4,2]},
                 behavSession = '20150315a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-13_11-53-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,2,2,3,3,4,3,1,2,3,2],2:[3,2,4,4,2,3,3,3,1,3,3,3],3:[3,3,2,3,3,3,3,3,2,3,3,3],4:[3,2,2,2,2,3,3,3,3,3,2,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,2,3,4,3,3,2,2,3,2,3],7:[3,3,2,2,3,3,3,2,3,3,3,2],8:[3,1,1,1,1,1,3,1,3,1,3,3]},
                 behavSession = '20150313a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-12_11-39-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,2,3,3,3,3,3,3,3,3,3],2:[3,2,3,3,2,3,3,2,3,3,2,3],3:[3,2,3,3,3,3,2,3,2,3,3,3],4:[3,2,2,2,3,3,3,2,3,3,3,3],5:[3,2,3,3,3,3,3,2,2,3,3,3],6:[3,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,3,3,3,3,2,2,3,3,2,3],8:[3,3,3,3,1,1,1,4,1,2,1,1]},
                 behavSession = '20150312a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-11_13-23-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,4,3,1,1,3,2,3,1,1,4,4],2:[3,2,3,3,3,3,3,2,2,3,2,1],3:[3,3,3,2,2,2,3,3,3,3,3,2],4:[3,3,2,3,3,2,2,3,1,,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,1,3,2,3,3,3,4,3,3],7:[3,2,2,3,3,3,3,3,3,2,2,3],8:[3,3,1,4,2,1,2,4,1,1,1,1]},
                 behavSession = '20150311a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-10_14-08-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality ={1:[3,3,3,3,4,1,4,4,3,2,3,0],2:[3,2,3,3,2,2,2,3,2,3,3,3],3:[3,2,2,2,3,2,3,3,3,2,2,3],4:[3,3,2,3,3,3,2,3,2,2,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,3,3,2,2,2,3,3,2,0],7:[3,2,2,2,2,1,4,3,3,3,3,0],8:[3,1,2,4,1,1,3,3,2,3,3,3]},
                 behavSession = '20150310a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-09_15-15-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,4,1,1,1,4,1,1,2,3,2,3],2:[3,3,3,3,2,2,3,2,2,3,3,0],3:[3,3,3,3,3,2,1,3,2,3,2,3],4:[3,3,3,2,3,2,3,3,3,3,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,2,1,3,3,3,2,3,3,3],7:[3,2,3,3,2,3,2,3,3,3,3,3],8:[3,4,1,3,2,3,3,3,4,1,1,1]},
                 behavSession = '20150309a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-07_21-00-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,1,1,1,1,4,3,2,3,3,3,2],2:[3,3,2,2,3,3,3,3,2,2,3,3],3:[3,3,2,3,3,3,2,2,3,2,2,3],4:[3,3,3,3,3,3,2,2,2,2,3,0],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,2,3,2,3,3,3,3,3,3,0],7:[3,3,3,2,3,3,3,3,2,3,2,3],8:[3,1,1,1,1,2,3,2,1,1,2,3]
                 behavSession = '20150307a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-06_12-30-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,4,1,1,1,1,3,3,2,3,2,0],2:[3,3,3,2,2,3,2,3,2,3,2,0],3:[3,2,2,3,2,2,3,3,3,3,3,0],4:[3,3,3,3,3,3,3,3,3,2,3,3],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,1,3,2,3,2,3,3,2,3,2],7:[3,2,2,2,2,3,3,3,2,3,3,2],8:[3,2,1,2,2,1,3,3,1,2,2,3]},
                 behavSession = '20150306a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-04_13-02-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,1,3,3,2,4,4,3,3,3,3,3],2:[3,2,3,3,2,3,3,3,3,3,2,3],3:[3,2,3,3,3,2,3,3,2,3,3,3],4:[3,3,3,3,3,2,3,3,2,3,3,2],5:[3,3,3,2,3,3,3,3,3,3,2,2],6:[3,3,3,3,3,3,2,1,1,2,2,3],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,3,2,3,3,4,3,3,3,3,3]},
                 behavSession = '20150304a')
cellDB.append_session(oneES)
oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-03_11-42-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,1,3,1,3,3,2,3,2,3,3,0],2:[3,2,1,2,3,1,1,2,3,3,3,2],3:[3,2,3,3,3,3,3,2,3,2,3,3],4:[3,3,3,2,2,3,2,2,3,3,3,3],5:[3,3,3,3,3,2,2,3,3,2,3,3],6:[3,2,3,13,2,3,1,1,2,2,3],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,1,2,2,3,1,2,4,3,3,3,4]},
                 behavSession = '20150303a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-02_13-35-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,2,3,3,3,2,3,3,3,3,3,3],2:[3,1,2,3,3,3,3,2,3,2,3,3],3:[3,3,3,3,3,3,3,3,3,2,3,2],4:[3,2,2,3,2,3,2,3,2,3,3,3],5:[3,3,3,3,2,3,2,2,3,3,2,3],6:[3,3,2,3,3,3,3,1,3,3,3,3],7:[3,0,0,0,0,0,0,0,0,0,0,0],8:[3,3,3,3,3,1,3,3,2,3,3,0]},
                 behavSession = '20150302a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test055',##############EPHYS IS ONE TRIAL LONGER THAN BEHAVIOR###############
                 ephysSession = '2015-03-01_16-53-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150301a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-28_19-02-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,3,3,3,1,3,3,3,1,3,1,4],2:[3,3,3,2,3,1,2,1,1,3,3,0],3:[3,3,3,3,2,3,3,2,3,2,2,3],4:[3,2,3,3,2,2,3,3,3,3,3,2],5:[3,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,1,1,4,1,2,3,2,2,3,2],7:[3,3,3,3,3,3,3,3,2,3,3,3],8:[3,1,2,2,2,3,3,3,3,3,3,3]
                 behavSession = '20150228a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-26_13-06-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,3,2,3,3,2,3,3,4,4,3,3],2:[3,3,3,3,2,3,3,3,3,3,3,3],3:[3,3,3,2,3,3,3,3,3,3,3,3],4:[3,3,3,2,3,2,3,1,3,3,3,0],5:[3,2,2,3,3,3,2,2,2,3,2,3],6:[3,3,2,1,3,1,1,2,1,2,1,0],7:[3,2,3,3,3,3,2,2,3,3,3,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},
                 behavSession = '20150226a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-25_12-38-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,1,3,3,3,2,3,2,3,3,3],3:[3,3,3,4,3,3,2,3,3,2,3,2],4:[3,2,3,3,3,3,3,3,3,3,3,3],5:[3,2,3,2,3,3,2,2,3,,2,3],6:[3,3,3,3,3,3,3,2,3,1,3,3],7:[3,3,3,3,2,2,2,3,1,1,2,3],8:[3,1,2,2,1,2,3,2,4,3,3,0]},
                 behavSession = '20150225a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-23_13-23-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,1,3,2,3,3,3,3,3,2,3],3:[3,2,3,2,3,3,3,3,3,3,3,0],4:[3,1,1,3,2,3,3,3,3,3,1,3],5:[3,3,3,3,3,2,3,3,3,3,2,3],6:[3,1,3,3,3,3,2,3,3,3,3,3],7:[3,3,3,3,3,2,3,3,3,3,3,3],8:[3,1,3,3,2,3,3,3,2,3,3,4]},
                 behavSession = '20150223a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-22_22-42-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,2,3,3,3,2,3,1,2,3,1,3],2:[3,3,1,3,2,2,1,3,3,2,3,3],3:[3,3,3,3,3,3,2,2,3,3,3,3],4:[3,3,3,3,3,3,3,3,3,3,1,3],5:[3,2,3,3,3,3,1,1,2,2,3,3],6:[3,3,3,3,3,3,3,3,3,2,3,3],7:[3,3,3,3,3,3,3,2,2,3,3,3],8:[3,0,0,0,0,0,0,0,0,0,0,0]},

                 behavSession = '20150222a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-20_11-42-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
clusterQuality = {1:[3,1,1,2,2,1,3,3,3,3,2,3],2:[3,3,1,1,3,1,3,1,2,2,3,2],3:[3,3,3,2,3,3,3,3,2,3,3,2],4:[3,1,3,1,3,1,2,3,3,2,1,1],5:[3,2,2,3,3,3,3,3,3,3,2,3],6:[3,3,3,2,1,1,3,2,1,3,1,3],7:[3,3,3,3,3,2,3,2,3,2,2,0],8:[3,0,0,0,0,0,0,0,0,0,0,0]},

                 behavSession = '20150220a')
cellDB.append_session(oneES)

'''
#This session has a skipped trial at trial 1158
oneES = eSession(animalName='test055',
                 ephysSession = '2015-06-02_13-32-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150602a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 282
oneES = eSession(animalName='test055',
                 ephysSession = '2015-06-03_15-16-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150603a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',###########################################3
                 ephysSession = '2015-05-06_12-38-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150506a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',###########################################
                 ephysSession = '2015-05-10_23-03-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150510a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',############################################
                 ephysSession = '2015-05-09_20-39-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150509a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',#########################################
                 ephysSession = '2015-05-14_12-46-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150514a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',################################
                 ephysSession = '2015-05-29_14-00-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:[1],7:range(1,13),8:range(1,13)},
                 behavSession = '20150529a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',########################################
                 ephysSession = '2015-05-01_12-59-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150501a')
cellDB.append_session(oneES)

#THIS SESSION IS MESSED UP
oneES = eSession(animalName='test055',##################################
                 ephysSession = '2015-04-30_11-57-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150430a')
cellDB.append_session(oneES)

#HAS TWO SKIPPED TRIALS
oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-28_12-46-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150428a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',###################################
                 ephysSession = '2015-04-21_13-43-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150421a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',#######################################
                 ephysSession = '2015-04-16_13-38-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150416a')
cellDB.append_session(oneES)

#THIS SESSION IS MESSED UP
oneES = eSession(animalName='test055',######################################
                 ephysSession = '2015-04-17_16-21-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150417a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 281
oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-15_12-29-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150415a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',################################################
                 ephysSession = '2015-04-13_15-54-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150413a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',####################################################
                 ephysSession = '2015-04-03_15-03-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150403a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',######################################################
                 ephysSession = '2015-04-01_13-04-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150401a')
cellDB.append_session(oneES)

#THIS SESSION IS MESSED UP
oneES = eSession(animalName='test055',####################################################
                 ephysSession = '2015-03-28_20-36-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150328a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',####################################################
                 ephysSession = '2015-03-29_23-16-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150329a')
cellDB.append_session(oneES)

#THIS SESSION IS MESSED UP
oneES = eSession(animalName='test055',############################################################
                 ephysSession = '2015-03-17_12-21-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150317a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',###########################################################
                 ephysSession = '2015-03-20_11-34-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150320a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',############################################################
                 ephysSession = '2015-03-08_21-05-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150308a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',#################################################################
                 ephysSession = '2015-03-05_14-12-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150305a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',##################################################
                 ephysSession = '2015-02-27_13-15-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150227a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',###############################################################
                 ephysSession = '2015-02-24_13-19-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150224a')
cellDB.append_session(oneES)

#THIS BEHAVIOR SESSION IS MESSED UP
oneES = eSession(animalName='test055',#######################################################################
                 ephysSession = '2015-02-21_18-38-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150221a')
cellDB.append_session(oneES)
'''
