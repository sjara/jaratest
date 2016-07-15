'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


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
'''

#This has one skipped trial at 1148
oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-19_10-33-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150619a')
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

#This has more than one skipped trial
oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-12_18-29-46',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150612a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-11_15-46-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150611a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test053',
                 ephysSession = '2015-06-10_14-44-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150610a')
cellDB.append_session(oneES)
'''

