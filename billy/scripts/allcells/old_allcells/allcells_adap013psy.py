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


oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-13_17-24-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160413a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-12_15-44-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160412a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-08_14-24-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160408a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-06_15-29-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160406a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-04-04_15-16-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160404a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-31_14-19-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160331a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-29_15-33-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160329a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-24_14-34-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160324a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-22_13-32-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160322a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-19_16-30-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160319a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-17_14-59-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160317a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-15_13-48-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160315a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-03-03_11-19-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160303a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-29_11-23-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160229a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-25_13-39-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160225a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-23_10-39-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160223a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-19_16-49-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160219a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-18_17-51-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160218a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap013',
                 ephysSession = '2016-02-10_10-10-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160210a')
cellDB.append_session(oneES)

