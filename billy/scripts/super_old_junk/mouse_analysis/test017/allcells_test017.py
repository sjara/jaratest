'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase
reload(celldatabase)
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-27_14-41-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150327a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-26_15-20-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150326a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-25_15-43-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150325a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-24_16-25-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150324a')
cellDB.append_session(oneES)

'''
oneES = eSession(animalName='test017',####################################################
                 ephysSession = '2015-03-23_16-27-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150323a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-22_20-31-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150322a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-21_14-06-46',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150321a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-20_13-05-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150320a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-19_13-35-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150319a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-18_17-16-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150318a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-17_14-21-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150317a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-16_17-21-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150316a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-15_14-33-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150315a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-13_13-28-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150313a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-12_15-10-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150312a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-11_14-48-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150311a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-10_16-21-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150310a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-09_16-51-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150309a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-06_14-12-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150306a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-05_15-48-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150305a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-04_14-56-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150304a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-03_18-44-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150303a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-02_15-32-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150302a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-01_18-37-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150301a')
cellDB.append_session(oneES)

'''
oneES = eSession(animalName='test017',#################################################
                 ephysSession = '2015-02-28_20-10-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150228a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-27_14-55-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150227a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-26_16-31-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150226a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-25_14-04-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150225a')
cellDB.append_session(oneES)

'''
#DID NOT SWITCH
oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-17_12-26-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150217a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-21_20-08-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150221a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-23_15-31-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150223a')
cellDB.append_session(oneES)


