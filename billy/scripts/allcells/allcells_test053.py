'''
List of all isolated units from one animal

oneES = eSession(animalName='ANIMAL_NAME', #name of the animal
                 ephysSession = '2015-10-12_15-08-17', #name of the task ephys session
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)}, #which clusters and tetrodes to look at
                 behavSession = '20151012a') #behavior session name corresponding to ephys session
cellDB.append_session(oneES) #add this cell to the list of allcells
'''

from jaratoolbox import celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-27_13-57-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150727a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-23_17-31-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150723a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-22_16-20-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150722a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-16_14-08-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150716a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-15_16-09-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150715a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-14_11-36-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150714a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-13_13-40-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150713a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-10_13-33-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150710a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-09_17-02-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150709a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-08_13-06-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150708a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-06_11-35-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150706a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-03_16-50-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150703a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-01_11-17-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150701a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-29_11-30-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150629a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-25_11-42-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150625a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-22_11-41-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150622a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-18_10-34-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150618a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-17_10-40-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150617a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-15_16-05-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150615a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-10_14-44-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150610a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 574
oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-17_14-39-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150717a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 700
oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-07_17-21-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150707a')
cellDB.append_session(oneES)

#This has one skipped trial at 405
oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-26_11-25-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150626a')
cellDB.append_session(oneES)

#This has one skipped trial at 1148
oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-19_10-33-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150619a')
cellDB.append_session(oneES)

#This has more than one skipped trial
oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-12_18-29-46',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150612a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 1097
oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-11_15-46-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150611a')
cellDB.append_session(oneES)
'''
#THIS SESSION IS MESSED UP. This session could not cluster properly for an unknown reason
oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-02_12-12-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150702a')
cellDB.append_session(oneES)

#The behavior file is missing for this session
oneES = eSession(animalName='test053',
                 ephysSession = '2015-07-24_11-56-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150724a')
cellDB.append_session(oneES)
'''
