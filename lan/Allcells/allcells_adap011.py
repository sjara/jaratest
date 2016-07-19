'''
List of all isolated units from adap011, with cluster quality added.
Lan Guo 2016-01-11
'''

from jaratoolbox.test.lan.Ephys import celldatabase_quality_vlan as celldatabase
reload(celldatabase)
#from jaratoolbox.test.lan import test012_add_good_clusters as test012

eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

'''
#1203 no good sound response, also experimenter=santiago
oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-03_13-34-44',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151203a')
cellDB.append_session(oneES)


#from here on experimenter='lan'
oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-04_14-50-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151204b')
cellDB.append_session(oneES)

#used 60dB sound
oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-05_14-39-32',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151205a')
cellDB.append_session(oneES)

#used 70dB sound
oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-06_15-58-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151206a')
cellDB.append_session(oneES)


#used 70dB sound
oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-07_12-06-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151207a')
cellDB.append_session(oneES)

#used 70dB sound
oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-08_11-46-07',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151208a')
cellDB.append_session(oneES)
'''

#from here on used <=50dB chords in behavior tasks
oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-09_11-49-36',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151209a',
                 clusterQuality = {1:[3,4,4,4,3,3,5,4,4,4,3,3],2:[3,6,4,4,4,4,2,4,4,6,3,3],3:[3,7,7,3,3,3,4,4,4,4,7,0],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,1,7,7,4,3,6,7,6,1,4],6:[3,3,3,3,3,3,3,3,3,3,3,0],7:[3,3,3,3,3,3,4,4,4,3,3,3],8:[3,3,3,2,3,4,7,2,4,3,4,4]})
cellDB.append_session(oneES)



oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-10_13-12-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151210a',
                 clusterQuality = {1:[3,3,1,7,7,3,3,3,3,1,3,4],2:[3,3,3,3,4,7,3,7,6,4,3,3],3:[3,3,3,3,3,4,6,7,3,7,3,3,3],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,4,4,6,4,7,3,7,3,1,7],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,3,3,3,3,3,3,3,3,3,3],8:[3,7,3,7,3,3,3,6,2,3,2,7]})


oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-11_14-06-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151211a',
                 clusterQuality = {1:[3,3,3,3,3,3,1,3,3,3,3,3],2:[3,3,3,3,6,3,4,3,3,3,3,6],3:[3,3,3,3,3,1,3,3,3,3,3,3],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,3,7,3,4,3,4,4,3,3,6],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,3,3,3,3,3,3,3,3,3,3],8:[3,3,3,2,6,3,6,4,3,3,3,7]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-12_16-14-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151212a',
                 clusterQuality = {1:[3,2,3,3,4,3,3,3,3,3,3,3],2:[3,3,3,3,7,3,3,3,3,3,4,7],3:[3,3,3,7,3,3,4,3,3,3,3,3],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,4,1,4,4,3,3,4,1,3,4],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,3,3,3,3,3,3,3,3,3,3],8:[3,3,3,2,3,1,6,3,3,5,3,4]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-15_16-07-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151215a',
                 clusterQuality = {1:[3,3,4,4,3,3,1,4,3,1,4,1],2:[3,4,3,7,1,3,1,4,4,3,3,4],3:[3,6,3,1,3,3,6,7,3,3,3,3],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,4,4,3,3,4,2,4,1,3,3],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,4,3,3,3,3,3,3,3,3,3,3],8:[3,4,4,3,3,4,3,3,3,3,3,3]})
cellDB.append_session(oneES)

oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-16_13-45-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151216a',
                 clusterQuality = {1:[3,1,1,1,3,3,1,1,3,3,3,0],2:[3,3,3,3,7,3,3,1,1,1,4,3,3,6],3:[3,3,6,4,3,1,4,6,7,6,3,3],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[3,4,3,1,3,1,3,2,1,4,3,1],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,3,3,3,3,3,3,3,3,3,3],8:[3,4,3,3,1,3,3,1,3,3,4,3]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-18_15-34-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151218a',
                 clusterQuality = {1:[3,4,3,3,3,1,3,1,4,3,4,4],2:[3,3,3,1,7,3,3,7,3,7,4,7],3:[3,3,4,1,4,1,4,4,7,3,3,3],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[3,1,3,1,1,1,3,1,1,4,1,0],6:[3,4,7,3,3,3,3,3,3,3,3,3],7:[3,3,3,3,3,3,3,3,3,3,3,3],8:[3,4,3,5,4,3,1,3,3,7,3,3]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-21_13-54-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151221a',
                 clusterQuality = {1:[3,3,3,3,1,1,3,3,3,3,3,1],2:[3,1,3,1,4,4,3,4,1,7,1,3],3:[3,4,1,3,1,1,3,3,6,7,1,3],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[3,3,1,1,6,6,6,1,4,3,3,3],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,3,3,3,3,3,3,3,3,3,3],8:[3,3,3,3,1,1,3,3,4,4,4,0]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2016-01-06_14-34-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160106a',
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,3,3,3],2:[3,3,3,3,3,3,4,3,3,3,3,4],3:[3,1,4,3,4,4,5,4,1,1,1,4],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[3,4,4,3,4,1,1,4,4,4,4,1],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,3,3,3,3,3,3,3,3,3,3],8:[3,4,4,3,3,3,3,3,3,3,3,3]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2016-01-14_12-58-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160114a',
                 clusterQuality = {1:[3,3,4,3,4,3,3,3,3,3,3,2],2:[3,1,4,1,4,1,4,4,5,3,3,1],3:[3,1,7,3,1,3,2,1,1,7,7,7],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[3,1,1,1,1,1,1,1,1,1,4,1],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,3,3,3,3,3,3,3,3,3,3],8:[3,3,4,3,2,3,3,3,3,3,2,2]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2016-01-15_13-38-31',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160115a',
                 clusterQuality = {1:[3,3,3,3,3,3,3,3,3,3,3,3],2:[3,1,1,3,3,3,1,4,1,1,1,3],3:[3,1,1,3,1,2,3,1,1,4,1,3],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[3,1,4,1,1,1,1,4,4,1,1,1],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,3,3,3,3,3,3,3,3,3,3],8:[3,2,3,3,3,3,3,2,3,3,3,3]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2016-01-16_14-30-37',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160116a',
                 clusterQuality = {1:[3,4,2,3,3,3,3,2,3,3,3,3],2:[3,1,3,3,4,3,3,1,1,1,1,3],3:[3,3,1,3,1,3,1,1,4,4,1,1],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[3,1,1,1,1,1,1,1,1,1,1,1],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,2,3,3,3,3,3,3,3,3,3,3],8:[3,3,3,2,3,3,2,3,3,3,3,3]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2016-01-17_15-55-03',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160117a',
                 clusterQuality = {1:[3,2,2,4,4,3,3,3,3,3,3,2],2:[3,4,1,3,3,3,1,4,4,4,1,0],3:[3,3,4,1,4,4,4,4,4,2,3,3],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[3,1,1,4,1,4,1,4,1,4,4,1],6:[3,3,3,3,3,3,3,3,3,3,3,3],7:[3,3,3,3,3,3,3,3,3,3,3,3],8:[3,3,3,3,3,2,2,2,3,2,4,3]})
cellDB.append_session(oneES)

