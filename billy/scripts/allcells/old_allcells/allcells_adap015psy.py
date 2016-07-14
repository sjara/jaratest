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


oneES = eSession(animalName='adap015',
                 ephysSession = '2016-03-16_10-04-37',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160316a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015', #CRASHES BECAUSE SKIPPED TRIAL IS LAST TRIAL
                 ephysSession = '2016-03-03_14-27-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160303a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-23_14-12-34',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160223a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-18_14-53-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160218a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-16_14-16-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160216a')
cellDB.append_session(oneES)

#skipped trial
oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-12_09-50-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160212a')
cellDB.append_session(oneES)

#skipped trial
oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-10_16-21-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160210a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',#THIS MAY BE A REWARD SWITCHING TRIAL
                 ephysSession = '2016-02-09_16-32-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160209a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-08_19-18-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160208a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-06_16-49-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160206a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-05_14-33-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160205a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-02-01_15-22-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160201a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-01-29_15-15-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160129a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-01-28_16-07-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160128a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-01-27_17-20-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160127a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-01-26_15-46-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160126a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap015',
                 ephysSession = '2016-01-22_16-39-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160122a')
cellDB.append_session(oneES)

