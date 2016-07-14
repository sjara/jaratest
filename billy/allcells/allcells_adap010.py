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


oneES = eSession(animalName='adap010',
                 ephysSession = '2016-01-15_14-31-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160115a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2016-01-13_11-00-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160113a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2016-01-12_11-14-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160112a')
cellDB.append_session(oneES)

'''
oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-23_16-00-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151223a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-22_16-43-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151222a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-21_14-42-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151221a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-20_20-50-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151220a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-19_17-48-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151219a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-18_15-08-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151218a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-17_16-09-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151217a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-16_20-53-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151216a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-15_17-46-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151215a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-14_16-01-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151214a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-12_20-51-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151212a')
cellDB.append_session(oneES)

#skipped trial at trial 588
oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-11_17-06-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151211a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-10_16-00-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151210a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-09_15-20-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151209a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-08_17-13-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151208a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-07_19-17-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151207a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-06_17-25-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151206a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-05_19-22-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151205a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-04_16-35-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151204a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-03_15-22-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151203a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-02_20-46-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151202a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap010',
                 ephysSession = '2015-12-01_17-49-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151201a')
cellDB.append_session(oneES)
'''
