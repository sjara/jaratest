'''
List of all isolated units from adap011 that meet our criteria of good waveform, persistent firing across the whole session, and having enough spikes and good cluster shape (score#1, can be an inverted spike #6).
Here the persistent firing rate criterion is only based on looking at the ephy session associated with behavior even though all sessions (including noise test and tuning are clustered together)
'''

from jaratoolbox.test.lan.Ephys import celldatabase_quality_vlan as celldatabase
reload(celldatabase)
import numpy as np

eSession = celldatabase.EphysSessionInfo  # Shorter name to simplify code


cellDB = celldatabase.CellDatabase()

'''
oneES = eSession(animalName='adap005',
                 ephysSession = '2015-12-14_16-23-21',
                 clustersEachTetrode = {1:[4,8],3:[4,6,10,11,12]},
                 behavSession = '20151214a')
cellDB.append_session(oneES)

#clusterQuality = {1:[3,4,2,1,2,4,2,1,3,2,2,2],2:[0,0,0,0,0,0,0,0,0,0,0,0],3:[3,4,2,1,3,1,2,2,2,1,1,1],4:[0,0,0,0,0,0,0,0,0,0,0,0],5:[0,0,0,0,0,0,0,0,0,0,0,0],6:[0,0,0,0,0,0,0,0,0,0,0,0],7:[3,4,4,4,4,4,2,4,3,4,4,4],8:[0,0,0,0,0,0,0,0,0,0,0,0]}
'''

oneES = eSession(animalName='adap005',
                 ephysSession = '2015-12-15_14-02-08',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151215a',
                 clusterQuality = {1:[3,1,2,1,3,2,2,2,3,2,3,4],2:[3,2,2,2,2,2,3,4,4,2,2,4],3:[3,2,2,2,2,2,2,2,3,2,2,4],4:[2,0,0,0,0,0,0,0,0,0,0,0],5:[3,1,2,1,2,1,4,4,2,2,4,3],6:[3,1,1,1,4,1,2,1,1,1,3,1],7:[3,2,2,1,3,3,4,2,2,1,1,4],8:[3,4,1,4,4,1,1,4,2,1,2,0]})
cellDB.append_session(oneES)

oneES = eSession(animalName='adap005',
                 ephysSession = '2015-12-16_16-15-56',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151216a',
                 clusterQuality = {1:[3,2,2,2,4,2,3,2,2,1,3,1],2:[3,2,2,2,4,2,2,2,2,3,3,2],3:[3,1,2,2,1,2,2,2,3,2,1,0],4:[1,0,0,0,0,0,0,0,0,0,0,0],5:[3,2,7,2,1,7,1,3,1,2,1,7],6:[3,4,2,1,3,2,4,3,2,2,1,4],7:[3,3,4,2,4,2,3,3,2,4,2,1],8:[3,1,1,1,1,1,1,1,1,1,2,4]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap005',
                 ephysSession = '2015-12-17_15-19-45',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151217a',
                 clusterQuality = {1:[3,2,2,4,1,1,2,2,4,4,2,2],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,3,1,2,4,4,1,1,2,2,3],4:[3,4,1,1,2,1,2,3,2,1,1,4],5:[3,7,1,7,7,1,1,1,1,2,1,1],6:[3,4,2,2,3,1,2,4,2,2,4,0],7:[3,2,1,1,1,2,3,4,3,4,4,1],8:[3,1,2,1,4,1,1,1,1,1,4,0]})
cellDB.append_session(oneES)

oneES = eSession(animalName='adap005',
                 ephysSession = '2015-12-18_13-50-13',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151218a',
                 clusterQuality = {1:[3,4,2,2,2,2,1,1,2,2,1,4],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,2,2,1,2,1,2,2,2,4,1,1],4:[3,1,2,1,3,1,1,2,2,1,4,2],5:[3,1,1,1,2,3,2,1,1,1,2,4],6:[3,3,2,2,4,2,2,4,4,4,4,1],7:[3,1,1,4,3,4,1,2,1,4,2,1],8:[3,1,1,1,4,1,1,2,1,1,1,1]})
cellDB.append_session(oneES)

oneES = eSession(animalName='adap005',
                 ephysSession = '2015-12-19_18-00-14',
                 clustersEachTetrode =  {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151219a',
                 trialLimit=[0,1590],
                 clusterQuality = {1:[3,2,1,1,2,4,2,2,4,4,4,2],2:[6,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,3,1,1,1,1,2,2,2,4,7],4:[3,2,2,2,2,1,1,1,1,2,3,1],5:[3,2,4,1,1,3,1,2,1,1,2,0],6:[3,5,4,4,3,4,3,4,2,2,2,4],7:[3,3,4,4,4,4,4,1,1,2,1,3],8:[3,1,1,1,1,1,1,1,1,1,1,2]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap005',
                 ephysSession = '2015-12-21_16-50-58',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151221a',
                 clusterQuality = {1:[3,1,1,2,4,2,2,1,1,4,3,1],2:[4,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,3,2,2,1,1,1,3,1,0],4:[3,1,2,1,2,1,2,1,5,1,3,2],5:[3,2,1,2,1,1,3,2,1,1,1,1],6:[3,3,1,2,1,4,3,4,1,4,2,0],7:[3,3,1,2,1,4,2,1,4,2,2,3],8:[3,1,3,1,1,1,1,1,1,1,1,1]}) #with peak and valley-first-half
#clusterQuality = {7:[3,2,2,4,4,1,3,4,1/4,1,2,3],8:[3,1,1,1,1,1,3,4,1,1,1,1]} #with peak, valley, and energy
cellDB.append_session(oneES)


oneES = eSession(animalName='adap005',
                 ephysSession = '2015-12-22_15-24-04',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151222a',
                 clusterQuality = {1:[3,1,1,1,1,4,3,1,4,1,3,1],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,3,1,6,1,2,1,1,1,4,1,1],4:[3,1,2,1,1,1,2,1,3,1,1,1],5:[3,1,1,1,1,1,1,1,2,6,3,1],6:[3,4,4,3,4,4,4,4,4,3,4,4],7:[3,1,1,2,4,1,1,4,3,1,3,2],8:[3,1,1,1,1,1,2,1,4,1,1,6]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap005',
                 ephysSession = '2015-12-23_14-41-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151223a',
                 trialLimit=[0,1758],
                 clusterQuality = {1:[3,2,1,1,1,4,1,1,2,2,4,1],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,3,1,1,1,6,1,1],4:[3,2,1,1,3,6,1,1,1,1,2,4],5:[3,6,1,1,6,1,1,1,1,1,1,0],6:[3,4,4,3,3,4,1,4,4,4,2,0],7:[3,1,1,1,1,4,4,2,3,3,1,6],8:[3,1,4,1,1,6,3,1,1,1,1,4]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap005',
                 ephysSession = '2015-12-24_14-43-57',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20151224a',
                 clusterQuality = {1:[3,1,1,1,1,1,3,2,1,4,2,1],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,3,1,1,1],4:[3,1,1,1,1,3,1,1,1,1,1,1],5:[3,3,6,1,1,1,1,1,1,2,3,1],6:[3,2,2,4,2,4,4,3,1,3,4,5],7:[3,4,1,2,4,3,1,3,1,4,4,4],8:[3,1,4,1,1,1,6,3,1,1,1,4]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap005',
                 ephysSession = '2016-01-08_11-38-00',
                 clustersEachTetrode = {1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160108a',
                 clusterQuality = {1:[3,1,1,1,3,4,4,1,3,1,1,2],2:[3,0,0,0,0,0,0,0,0,0,0,0],3:[3,4,4,1,1,1,3,1,1,1,1,3],4:[3,3,4,1,1,4,1,1,1,1,1,4],5:[3,4,1,1,3,1,1,1,1,1,1,0],6:[3,4,3,1,1,1,4,4,1,3,2,3],7:[3,2,4,2,3,1,1,3,1,4,3,3],8:[3,1,1,3,1,1,1,3,2,1,1,1]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap005',
                 ephysSession = '2016-01-09_14-21-47',
                 clustersEachTetrode ={1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160109a',
                 clusterQuality = {1:[3,1,4,1,1,1,1,1,2,4,2,1],2:[4,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,4,1,2,4,1,1,1,2,1],4:[3,1,1,1,1,1,2,1,1,1,1,1],5:[3,1,1,1,1,1,1,1,1,1,1,0],6:[3,4,4,1,1,4,4,4,3,3,2,1],7:[3,4,3,4,2,4,4,2,4,2,1,2],8:[3,1,4,1,1,4,1,1,1,1,1,4]})
cellDB.append_session(oneES)


oneES = eSession(animalName='adap005',
                 ephysSession = '2016-01-10_15-55-57',
                 clustersEachTetrode ={1:range(1,13),2:range(1,13),3:range(1,13),4:range(1,13),5:range(1,13),6:range(1,13),7:range(1,13),8:range(1,13)},
                 behavSession = '20160110a',
                 clusterQuality={1:[3,1,2,2,4,3,2,4,1,4,2,0],2:[4,0,0,0,0,0,0,0,0,0,0,0],3:[3,1,1,1,1,1,1,1,4,2,4,3],4:[3,2,4,2,4,1,4,4,2,1,1,4],5:[3,1,1,3,1,1,1,1,1,1,1,1],6:[3,4,4,4,4,4,4,3,4,4,1,0],7:[3,3,3,1,3,3,2,3,2,4,4,3],8:[3,3,4,1,4,4,1,1,1,1,1,4]})
cellDB.append_session(oneES)

