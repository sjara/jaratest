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


oneES = eSession(animalName='test089',
                 ephysSession = '2016-02-03_11-39-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160203a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-02-02_10-53-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160202a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-02-01_13-53-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160201a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 441
oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-30_13-10-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160130a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-29_12-07-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160129a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-28_14-23-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160128a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-27_15-41-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160127a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-26_14-28-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160126a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-25_15-03-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160125a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-24_16-46-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160124a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-23_16-18-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160123a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-22_14-54-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160122a')
cellDB.append_session(oneES)

#this session has a skipped trial at trial 684
oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-21_14-03-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160121a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-20_16-44-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160120a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-18_16-03-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160118a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-16_15-12-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160116a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-15_11-03-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160115a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-14_10-45-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160114a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-13_15-41-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160113a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 155
oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-12_13-52-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160112a')
cellDB.append_session(oneES)

#This session has two skipped trials. The first one is at 169
oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-11_16-55-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160111a')
cellDB.append_session(oneES)

#skipped trial on trial 1641
oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-23_14-22-34',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151223a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-22_15-06-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151222a')
cellDB.append_session(oneES)

#skipped trial on trial 1507
oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-21_12-45-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151221a')
cellDB.append_session(oneES)

#skipped trial on trial 298
oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-18_13-41-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151218a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-17_14-16-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151217a')
cellDB.append_session(oneES)

#skipped trial on trial 2000
oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-16_15-56-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151216a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-14_14-22-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151214a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-13_18-54-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151213a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-11_11-31-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151211a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-10_11-43-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151210a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-09_11-22-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151209a')
cellDB.append_session(oneES)

#skipped trial on trial 1362
oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-08_11-37-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151208a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-07_11-45-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151207a')
cellDB.append_session(oneES)

#skipped trial on trial 605
oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-04_20-16-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151204a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-02_11-20-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151202a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-10-09_11-41-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151009a')
cellDB.append_session(oneES)

#skipped trial on trial 1648
oneES = eSession(animalName='test089',
                 ephysSession = '2015-10-08_13-51-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151008a')
cellDB.append_session(oneES)

#skipped trial on trial 1137
oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-26_14-03-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150926a')
cellDB.append_session(oneES)

#skipped trial on trial 1641
oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-25_12-41-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150925a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-24_13-32-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150924a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-21_12-23-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150921a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-18_13-00-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150918a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-17_14-19-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150917a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-15_12-41-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150915a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-14_18-02-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150914a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-13_16-00-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150913a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-11_12-33-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150911a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-10_12-37-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150910a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-09_13-29-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150909a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-02_14-34-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150902a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-01_14-06-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150901a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-27_11-56-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150827a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-19_12-53-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150819a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-18_17-32-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150818a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-17_15-22-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150817a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-14_13-12-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150814a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-11_11-14-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150811a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-07_16-05-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150807a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-03_16-12-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150803a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-31_14-40-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150731a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-29_10-26-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150729a')
cellDB.append_session(oneES)


#This session has a skipped trial at trial 1641
oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-25_12-41-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150925a')
cellDB.append_session(oneES)

#This session has more than one skipped trial
oneES = eSession(animalName='test089',
                 ephysSession = '2015-09-23_12-45-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150923a')
cellDB.append_session(oneES)


#This session has a skipped trial at trial 1445
oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-28_11-14-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150828a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 429
oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-21_16-54-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150821a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 490
oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-13_16-59-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150813a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 731
oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-12_23-22-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150812a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 924
oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-10_15-17-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150810a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 884
oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-06_13-29-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150806a')
cellDB.append_session(oneES)

#This session has two skipped trials
oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-04_11-21-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150804a')
cellDB.append_session(oneES)

#This session has two skipped trials
oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-01_13-35-46',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150801a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 243
oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-30_16-33-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150730a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 82
oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-28_13-54-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150728a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 375
oneES = eSession(animalName='test089',
                 ephysSession = '2015-07-27_16-03-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150727a')
cellDB.append_session(oneES)


'''
#THIS SESSION IS MESSED UP. there are 1479 behavior trials and only 1454 ephys trials. more than one skipped trial. First skipped trial on trial 444
oneES = eSession(animalName='test089',
                 ephysSession = '2015-12-15_16-29-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151215a')
cellDB.append_session(oneES)

#This session might have a skipped trial as the last trial. This session has a skipped trial at trial 1654
oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-05_16-44-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150805a')
cellDB.append_session(oneES)

#THIS SESSION IS MESSED UP. it crashes while clustering
oneES = eSession(animalName='test089',
                 ephysSession = '2016-01-19_17-27-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160119a')
cellDB.append_session(oneES)

#THIS SESSION IS MESSED UP. it crashes while clustering
oneES = eSession(animalName='test089',
                 ephysSession = '2015-08-31_16-14-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150831a')
cellDB.append_session(oneES)

'''
