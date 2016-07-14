'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

'''
oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-17_12-03-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150217a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-18_13-44-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150218a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-23_14-59-44',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150223a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-24_14-54-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150224a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-25_13-54-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150225a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-26_16-08-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150226a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-27_14-43-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150227a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-02-28_20-01-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150228a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-01_18-20-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150301b')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-02_15-04-46',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150302a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-03_16-50-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150303b')
cellDB.append_session(oneES)


oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-04_14-34-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150304a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-05_15-27-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150305a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-06_13-52-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150306a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-09_16-41-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150309a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-10_15-59-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150310a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-11_14-39-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150311a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-12_14-53-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150312a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-13_13-10-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150313a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-15_14-24-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150315a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-16_17-09-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150316a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-17_14-02-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150317a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-18_17-05-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150318a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-19_13-23-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150319a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-20_12-55-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150320a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-21_13-45-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150321a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-22_20-20-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150322a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-23_16-13-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150323a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-24_16-14-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150324a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-25_14-17-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150325a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test017',
                 ephysSession = '2015-03-26_15-10-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150326a')
cellDB.append_session(oneES)
'''

oneES = eSession(animalName='test017',#######################################################################
                 ephysSession = '2015-03-27_14-32-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150327a')
cellDB.append_session(oneES)
