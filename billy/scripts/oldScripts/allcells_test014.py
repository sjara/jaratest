'''
List of all isolated units from one animal
'''

from jaratoolbox import celldatabase
reload(celldatabase)
eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

'''
oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-07_17-37-14',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150107a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-08_16-14-41',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150108a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-09_16-41-49',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150109a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-10_21-45-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150110a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-11_16-15-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150111a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-12_17-10-52',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150112a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-13_15-17-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150113a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-14_16-04-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150114a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-15_14-38-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150115a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-16_17-13-23',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150116a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-17_18-29-02',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150117a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-18_21-33-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150118a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-19_16-46-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150119a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-20_16-06-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20150120a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test014',
                 ephysSession = '2015-01-12_17-10-52',
                 clustersEachTetrode = {1:[3]},
                 behavSession = '20150112a')
cellDB.append_session(oneES)
