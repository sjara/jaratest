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


oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-18_17-09-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160418a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-14_14-41-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160414a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-12_14-09-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160412a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-11_17-40-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160411a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-07_16-07-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160407a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-05_16-24-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160405a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-01_16-08-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160401a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-30_14-56-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160330a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-28_15-44-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160328a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-23_15-33-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160323a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-21_16-59-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160321a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-17_16-22-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160317a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-15_15-17-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160315a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',#something weird going on. many trials missing (28)
                 ephysSession = '2016-03-03_16-12-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160303a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-02-29_17-55-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160229a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-02-25_15-29-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160225a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-19_17-23-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160419a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-20_16-27-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160420a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-21_15-24-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160421a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-22_19-14-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160422a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-23_18-38-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160423a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-24_14-57-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160424a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-25_15-53-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160425a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-26_18-01-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160426a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-27_15-50-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160427a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-28_14-23-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160428a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-29_18-06-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160429a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-05-02_17-17-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160502a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-05-03_17-42-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160503a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-05-04_16-17-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160504a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-05-05_15-47-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160505a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-05-06_17-05-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160506a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap017',
                 ephysSession = '2016-05-09_17-46-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160509a')
cellDB.append_session(oneES)
'''
