'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

'''
oneES = eSession(animalName='test055',#########################################################################
                 ephysSession = '2015-02-11_17-53-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150211a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',#########################################################################
                 ephysSession = '2015-02-12_12-51-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150212a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',#########################################################################
                 ephysSession = '2015-02-13_11-03-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150213a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',#########################################################################
                 ephysSession = '2015-02-14_14-13-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150214a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',#########################################################################
                 ephysSession = '2015-02-16_15-36-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150216a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',#########################################################################
                 ephysSession = '2015-02-17_17-35-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150217a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',#########################################################################
                 ephysSession = '2015-02-18_16-54-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150218a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',#########################################################################
                 ephysSession = '2015-02-19_17-44-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150219a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',#########################################################################
                 ephysSession = '2015-02-20_11-32-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150220a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-21_18-29-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150221a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-24_13-06-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150224a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-25_12-27-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150225a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',##################################################################
                 ephysSession = '2015-02-26_12-54-53 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150226a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-27_13-03-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150227a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-02-28_18-36-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150228a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-01_16-43-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150301a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-02_13-26-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150302a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-03_11-31-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150303a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-04_12-49-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150304a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-05_14-01-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150305a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-06_12-20-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150306a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-07_20-51-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150307a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-08_20-56-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150308a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',#########################################################################
                 ephysSession = '2015-03-09_15-07-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150309a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-10_13-57-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150310a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-11_13-12-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150311a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-12_10-59-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150312a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-13_11-43-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150313a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-15_12-57-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150315a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-16_11-05-34',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150316a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-17_12-11-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150317a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-18_15-32-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150318a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-19_14-55-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150319a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-20_11-24-44',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150320a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-21_15-24-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150321a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-22_18-51-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150322a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-23_12-24-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150323a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',#######################################################################3
                 ephysSession = '2015-03-24_12-18-08 ',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150324a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-25_12-33-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150325a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-26_11-08-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150326a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-27_12-10-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150327a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-28_20-21-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150328a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-29_23-05-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150329a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-30_12-22-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150330a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-03-31_11-41-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150331a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-01_12-55-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150401a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-03_14-50-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150403a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-06_15-04-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150406a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-07_19-00-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150407a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-08_12-01-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150408a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-09_12-06-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150409a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-10_12-21-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150410a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-11_18-21-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150411a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-13_00-04-10',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150412a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-13_15-37-20',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150413a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-14_11-57-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150414a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-15_12-16-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150415a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-16_13-28-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150416a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-17_16-01-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150417a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-18_15-35-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150418a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-19_14-14-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150419a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-20_13-16-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150420a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-21_13-34-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150421a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-22_13-37-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150422a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-23_12-55-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150423a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-27_15-28-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150427a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-28_12-37-26',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150428a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-04-29_12-39-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150429a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-01_12-49-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150501a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',####################################################################
                 ephysSession = '2015-05-02_13-44-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150502a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-05_12-42-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150505a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-06_12-26-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150506a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-07_12-39-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150507a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-08_17-08-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150508a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-09_20-23-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150509a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-10_22-53-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150510a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-11_15-14-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150511a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-12_12-51-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150512a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-13_12-56-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150513a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-14_12-36-42',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150514a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-15_11-54-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150515a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-17_17-52-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150517a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-18_13-03-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150518a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-19_12-42-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150519a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-26_13-03-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150526a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-27_12-10-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150527a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-28_12-39-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150528a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-29_13-34-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150529a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-05-30_15-37-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150530a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-06-01_12-40-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150601a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-06-02_13-21-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150602a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-06-03_15-05-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150603a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test055',
                 ephysSession = '2015-06-04_14-52-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150604a')
cellDB.append_session(oneES)
