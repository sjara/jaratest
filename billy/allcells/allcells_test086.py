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

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-31_11-43-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150731a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-30_12-24-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150730a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-29_16-14-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150729a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-28_11-32-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150728a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-27_10-57-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150727a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-23_14-56-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150723a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-22_14-08-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150722a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-16_12-12-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150716a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-14_13-25-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150714a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-10_11-01-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150710a')
cellDB.append_session(oneES)

####################################
oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-09_11-37-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150709a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-08_11-23-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150708a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-06_13-46-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150706a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-03_11-10-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150703a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-02_13-52-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150702a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-01_13-00-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150701a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-26_13-50-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150626a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-25_13-35-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150625a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-23_13-14-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150623a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-22_13-55-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150622a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-19_12-26-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150619a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-18_12-18-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150618a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-16_14-12-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150616a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-15_12-03-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150615a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-12_17-02-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150612a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-11_13-47-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150611a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-09_16-38-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150609a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-08_18-10-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150608a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-05_16-20-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150605a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-04_16-53-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150604a')
cellDB.append_session(oneES)


#This session has a skipped trial at trial 584
oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-24_14-10-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150724a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 2
oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-17_10-57-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150717a')
cellDB.append_session(oneES)

#This has a skipped trial at trial 1006
oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-15_13-31-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150715a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 623
oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-13_16-57-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150713a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 839
oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-29_15-57-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150629a')
cellDB.append_session(oneES)


#This session has a skipped trial at trial 761
oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-24_12-04-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150624a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 736
oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-17_17-00-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150617a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 1335
oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-10_13-11-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150610a')
cellDB.append_session(oneES)

