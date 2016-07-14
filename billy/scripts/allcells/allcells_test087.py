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

'''
oneES = eSession(animalName='test087',
                 ephysSession = '2015-10-08_15-30-15',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151008a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-10-09_15-02-29',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151009a')
cellDB.append_session(oneES)
'''
oneES = eSession(animalName='test087',##############################################################
                 ephysSession = '2015-10-22_17-26-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151022a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-05_17-10-53',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151105a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-06_17-12-16',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151106a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-07_20-47-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151107a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-09_18-26-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151109a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-11_17-21-06',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151111a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-13_14-55-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151113a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-16_17-16-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151116a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 363
oneES = eSession(animalName='test087',
                 ephysSession = '2015-10-13_14-12-47',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151013a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 599
oneES = eSession(animalName='test087',
                 ephysSession = '2015-10-21_17-03-43',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151021a')
cellDB.append_session(oneES)

#This session has a skipped trial at trial 248
oneES = eSession(animalName='test087',
                 ephysSession = '2015-11-10_16-44-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151110a')
cellDB.append_session(oneES)


'''
##########################################################################################################
##########################################################################################################
################################THIS IS TEST087 PSYCHOMETRIC CURVE DATA###################################
##########################################################################################################
##########################################################################################################


oneES = eSession(animalName='test087',
                 ephysSession = '2015-12-21_16-22-12',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151221a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-12-18_12-09-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151218a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-12-17_13-07-19',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151217a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-12-16_12-11-22',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151216a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-12-15_14-52-48',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151215a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-12-14_11-19-33',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151214a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-12-11_15-12-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151211a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-12-10_14-41-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151210a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-12-09_14-05-09',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151209a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-12-07_15-10-35',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151207a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-12-04_12-13-59',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151204a')
cellDB.append_session(oneES)

oneES = eSession(animalName='test087',
                 ephysSession = '2015-12-02_14-15-18',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151202a')
cellDB.append_session(oneES)


oneES = eSession(animalName='test087',
                 ephysSession = '2015-12-01_11-57-21',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151201a')
cellDB.append_session(oneES)
'''
'''
#EPHYS FROZE DURING RECORDING
oneES = eSession(animalName='test087',
                 ephysSession = '2015-12-08_14-18-40',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151208a')
cellDB.append_session(oneES)
'''
