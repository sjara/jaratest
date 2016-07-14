'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()



oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-24_13-38-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150624a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-23_15-05-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150623b')
cellDB.append_session(oneES)

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-22_15-21-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150623a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-19_14-05-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150619a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-18_14-41-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150618a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test059',
                 ephysSession = '2015-06-17_21-36-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150617a')
cellDB.append_session(oneES)

