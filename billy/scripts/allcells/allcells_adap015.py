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


'''
oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-04_15-41-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160204a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-05_14-33-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160205a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-06_16-49-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160206a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-07_15-27-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160207a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-08_19-18-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160208a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-09_16-32-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160209a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-10_16-21-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160210a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-11_17-18-34',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160211a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-12_09-50-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160212a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-15_15-40-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160215a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-16_14-16-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160216a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-17_16-15-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160217a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-18_14-53-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160218a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-19_10-42-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160219a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-22_17-55-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160222a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-23_14-12-34',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160223a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-24_17-21-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160224a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-25_17-13-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160225a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-29_15-55-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160229a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-01_14-12-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160301a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-03_14-27-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160303a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-16_10-04-37',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160316a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-17_11-13-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160317a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-18_10-49-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160318a')
cellDB.append_session(oneES)
'''
