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

oneES = eSession(animalName='adap024',
                 ephysSession = '2016-07-05_15-59-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160705a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap024',
                 ephysSession = '2016-07-07_14-28-46',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160707a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap024',
                 ephysSession = '2016-07-12_14-43-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160712a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap024',
                 ephysSession = '2016-07-13_16-22-44',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160713a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap024',
                 ephysSession = '2016-07-14_14-46-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160714a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap024',
                 ephysSession = '2016-07-20_15-55-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160720a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap024',
                 ephysSession = '2016-07-21_14-53-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160721a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap024',
                 ephysSession = '2016-07-22_16-19-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160722a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap024',
                 ephysSession = '2016-08-04_15-11-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160804a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap024',
                 ephysSession = '2016-08-05_16-18-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160805a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap024',
                 ephysSession = '2016-08-06_14-33-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160806a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap024',
                 ephysSession = '2016-08-09_15-42-44',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160809a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap024',
                 ephysSession = '2016-08-10_17-02-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160810a')
cellDB.append_session(oneES)
