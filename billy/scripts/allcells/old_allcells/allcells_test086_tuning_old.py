'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

'''
oneES = eSession(animalName='test086',
                 ephysSession = '2015-04-15_15-51-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150415a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-04-21_16-34-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150421a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-04-22_16-35-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150422a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-04_16-33-46',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150604a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-05_16-03-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150605a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-08_17-54-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150608a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-09_16-14-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150609a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-10_12-55-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150610a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-11_13-32-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150611a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-12_16-53-34',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150612a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-15_13-09-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150615a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-16_13-41-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150616a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-17_16-38-37',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150617a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-18_12-04-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150618a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-19_12-11-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150619a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-22_13-37-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150622a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-23_12-56-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150623a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-24_11-48-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150624a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-25_13-12-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150625a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-06-26_13-38-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150626a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',###################################################
                 ephysSession = '2015-06-29_15-21-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150629a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',###################################################
                 ephysSession = '2015-06-30_11-38-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150630a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-01_12-48-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150701a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-02_13-38-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150702a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-03_10-55-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150703a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-06_13-24-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150706a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-08_11-00-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150708a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-09_11-21-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150709a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-10_10-45-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150710a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-13_16-40-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150713a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-14_13-11-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150714a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-16_12-02-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150716a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-17_10-41-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150717a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-22_13-50-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150722a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-23_14-09-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150723a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-24_13-50-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150724a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-27_10-35-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150727a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-28_11-00-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150728a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-29_15-51-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150729a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-30_12-10-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150730a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test086',
                 ephysSession = '2015-07-31_11-28-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150731a')
cellDB.append_session(oneES)
