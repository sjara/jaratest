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


oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-12_10-13-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160412a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-13_11-34-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160413a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-14_11-33-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160414a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-15_11-34-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160415a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-16_15-10-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160416a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-18_11-38-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160418a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-19_11-10-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160419a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-20_13-51-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160420a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-21_13-19-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160421a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-22_17-28-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160422a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-23_16-00-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160423a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-24_13-36-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160424a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-25_11-49-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160425a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-26_14-14-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160426a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-27_11-21-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160427a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-28_11-28-44',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160428a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-29_11-07-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160429a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-04-30_16-28-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160430a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-02_11-49-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160502a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-03_11-16-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160503a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-04_11-22-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160504a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-05_11-20-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160505a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-06_11-28-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160506a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-09_15-30-51',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160509a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-10_16-05-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160510a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-11_16-52-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160511a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-12_14-17-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160512a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-17_15-23-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160517a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-18_17-07-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160518a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-19_16-51-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160519a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-20_17-36-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160520a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-21_18-16-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160521a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-22_17-24-28',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160522a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-23_17-35-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160523a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-24_16-00-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160524a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-25_16-33-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160525a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-26_14-44-25',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160526a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-27_16-23-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160527a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-31_16-46-11',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160531a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-01_16-08-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160601a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-02_15-11-46',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160602a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-03_15-49-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160603a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-07_15-14-50',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160607a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-08_16-09-27',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160608a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-09_15-07-54',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160609a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-10_16-00-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160610a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-13_15-59-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160613a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-14_16-42-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160614a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-15_16-58-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160615a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-17_16-57-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160617a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap020',
                 ephysSession = '2016-06-20_15-49-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160620a')
cellDB.append_session(oneES)
