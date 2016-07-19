'''
List of all isolated units from adap017, with cluster quality added.
Lan Guo 2016-03-25
'''
#using CellDatabase that contains laserSession for evaluating laser responsiveness

from jaratoolbox.test.lan.Ephys import celldatabase_quality_vlan as celldatabase
reload(celldatabase)


eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()


oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-16_17-49-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160316a',
                 clusterQuality = {1:[3,1,2,2,2,1,4,2,3,1,4,1],2:[3,4,1,7,4,4,1,3,3,2,1,1],3:[3,2,4,4,4,4,2,1,2,3,1,2],4:[3,3,1,4,5,2,2,1,2,2,4,1],5:[3,2,2,2,1,2,2,2,3,2,1,3],6:[3,2,2,4,3,2,2,1,2,2,2,2],7:[9,0,0,0,0,0,0,0,0,0,0,0],8:[3,1,1,2,2,2,3,2,2,2,2,4]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-18_17-27-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160318a',
                 clusterQuality = {1:[3,2,2,2,2,1,4,2,1,3,3,2],2:[3,1,1,1,4,3,3,3,3,3,3,3],3:[3,4,1,1,2,2,4,2,1,1,2,3],4:[3,2,3,3,3,2,2,4,2,1,2,2],5:[3,2,2,2,1,2,2,2,4,4,2,3],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,2,2,2,3,2,2,2,2,1,3],8:[3,2,4,2,2,1,1,2,3,2,2,2]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-22_14-43-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160322a',
                 clusterQuality = {1:[3,3,2,4,3,1,2,4,4,4,3,2],2:[3,1,1,1,2,1,3,3,2,3,4,4],3:[3,2,1,1,4,3,2,4,1,1,2,2],4:[3,4,3,2,3,3,1,4,1,1,3,3],5:[9,0,0,0,0,0,0,0,0,0,0,0],6:[3,2,3,2,3,3,2,2,2,2,1,2],7:[3,2,2,2,4,2,3,7,7,3,2,3],8:[3,2,7,7,2,3,2,1,2,7,7,6]})
cellDB.append_session(oneES)


'''
oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-24_',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160324a',
                 clusterQuality = {1:[3,3,2,2,2,3,3,2,2,1,2,2],2:[3,3,1,2,4,1,4,3,3,2,2,2],3:[3,2,3,2,1,2,1,3,4,1,3,1],4:[3,1,1,2,3,4,2,2,2,3,1,0],5:[9,0,0,0,0,0,0,0,0,0,0,0],6:[3,3,3,3,2,2,7,2,4,3,3,3],7:[3,4,2,2,3,3,2,3,4,2,2,3],8:[3,2,2,3,1,1,6,6,2,2,2,0]})
cellDB.append_session(oneES)



oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-29_',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160329a',
                 clusterQuality = {1:[3,2,4,2,2,2,2,2,3,2,2,2],2:[3,3,1,1,2,3,3,3,2,3,2,2],3:[3,3,1,2,2,1,2,3,3,2,1,2],4:[3,2,2,2,2,2,6,3,2,2,4,2],5:[3,2,2,3,2,3,2,2,2,7,4,3],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,2,3,2,2,2,7,2,3,7,2,0],8:[3,2,4,6,1,2,2,3,4,1,2,2]})
cellDB.append_session(oneES)



oneES = eSession(animalName='adap017',
                 ephysSession = '2016-03-31_',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160331a',
                 clusterQuality = {1:[3,3,2,2,6,3,1,2,2,4,2,2],2:[3,3,2,3,3,2,2,3,1,3,3,2],3:[3,1,2,3,3,4,4,4,2,3,2,3],4:[3,2,2,1,2,2,1,2,2,3,4,4],5:[3,2,3,2,2,2,2,2,2,3,2,3],6:[9,0,0,0,0,0,0,0,0,0,0,0],7:[3,3,2,2,3,1,4,3,7,7,2,2],8:[3,2,7,4,2,3,3,2,7,4,2,3]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-04_',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160404a',
                 clusterQuality = {1:[9,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,3,2,2,7,3,3,3,2,3,2],3:[3,3,2,2,3,2,2,2,2,1,3,2],4:[3,3,4,3,2,2,7,2,2,2,1,1],5:[3,2,4,2,2,2,4,2,3,3,3,2],6:[3,2,2,3,3,7,3,3,3,6,3,2],7:[3,1,2,6,4,1,6,2,3,2,2,2],8:[3,2,2,2,2,2,2,2,7,2,3,2]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap017',
                 ephysSession = '2016-04-06_',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160406a',
                 clusterQuality = {1:[9,0,0,0,0,0,0,0,0,0,0,0],2:[3,3,2,1,3,7,3,2,3,3,3,0],3:[3,3,2,2,2,1,2,3,5,2,1,4],4:[3,3,1,3,1,2,1,4,2,4,1,6],5:[3,2,1,3,2,1,2,1,1,1,3,2],6:[3,3,3,2,4,3,3,2,3,2,2,3],7:[3,2,2,3,2,3,2,4,4,4,2,1],8:[3,3,3,6,2,7,1,7,2,2,3,3]})
cellDB.append_session(oneES)
'''
