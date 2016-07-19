'''
List of all isolated units from d1pi001, with cluster quality added.
IMPORTANT: these experiments are PINP in head-fixed mouse, no 2afc behavior; ephysSession correspond to noiseburst session. laserSession correspond to laser burst session.
Lan Guo 2016-03-29 -NOT COMPLETED
'''
#using CellDatabase that contains laserSession for evaluating laser responsiveness

from jaratoolbox.test.lan.Ephys import celldatabase_quality_laser as celldatabase
reload(celldatabase)


eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='d1pi001',
                 ephysSession = '2015-07-01_19-09-42',
                 laserSession = '2015-07-01_19-13-36',
                 clustersEachTetrode = {3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13)},
                 behavSession = '20150701c', #Here behavSession keeps the date and site (site3=c)
                 clusterQuality = {3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,3,3,3,3,3,3,3,3,3,3,3],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[2,1,1,1,1,2,2,2,2,2,1,2]}) #had only reclustered and assessed quality on TT6 since others don't appear to have good cells
cellDB.append_session(oneES)


oneES = eSession(animalName='d1pi001',
                 ephysSession = '2015-07-01_19-52-08',
                 laserSession = '2015-07-01_19-49-07',
                 clustersEachTetrode = {3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13)},
                 behavSession = '20150701d',
                 clusterQuality = {3:[3,3,3,3,3,3,3,3,3,3,3,3],4:[3,3,3,3,3,3,3,3,3,3,3,3],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[]})
cellDB.append_session(oneES)


oneES = eSession(animalName='d1pi001',
                 ephysSession = '2015-07-01_20-31-44',
                 laserSession = '2015-07-01_20-25-09',
                 clustersEachTetrode = {3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13)},
                 behavSession = '20150701e',
                 clusterQuality = {3:[3],4:[3,3,3,3,3,3,3,3,3,3,3,3],5:[3,3,3,3,3,3,3,3,3,3,3,3],6:[3,]})
cellDB.append_session(oneES)
