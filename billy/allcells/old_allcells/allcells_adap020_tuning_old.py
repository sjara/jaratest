'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

#THIS WAS JUST A SPEAKER NOISE TEST NOT A REAL TUNING CURVE
oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-04_15-55-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160504c')
cellDB.append_session(oneES)

#THIS WAS JUST A SPEAKER NOISE TEST NOT A REAL TUNING CURVE
oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-04_15-49-24',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160504b')
cellDB.append_session(oneES)

#THIS WAS JUST A SPEAKER NOISE TEST NOT A REAL TUNING CURVE
oneES = eSession(animalName='adap020',
                 ephysSession = '2016-05-04_15-58-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160504a')
cellDB.append_session(oneES)
