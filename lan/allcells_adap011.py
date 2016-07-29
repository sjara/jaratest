'''
List of all isolated units from adap011
'''

from jaratoolbox import celldatabase
reload(celldatabase)
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
                 behavSession = '20151209a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-10_13-12-38',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151210a')


oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-11_14-06-01',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151211a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-12_16-14-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151212a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-15_16-07-30',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151215a')
cellDB.append_session(oneES)

oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-16_13-45-55',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151216a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-18_15-34-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151218a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2015-12-21_13-54-05',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151221a')
cellDB.append_session(oneES)


oneES = eSession(animalName='adap011',
                 ephysSession = '2016-01-06_14-34-39',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160106a')
cellDB.append_session(oneES)
