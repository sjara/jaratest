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


oneES = eSession(animalName='adap002',
                 ephysSession = '2015-10-12_15-08-17',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151012a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap002',
                 ephysSession = '2015-10-14_14-30-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151014a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap002',
                 ephysSession = '2015-10-15_12-23-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151015a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap002',
                 ephysSession = '2015-10-16_15-55-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151016a')
cellDB.append_session(oneES)
