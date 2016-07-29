##What to write when you are collecting data
import numpy as np

from jaratest.nick.database import cellDB as celldatabase
# from jaratoolbox import celldatabase

exp = celldatabase.Experiment('band001', '2016-07-13', '', 'am_tuning_curve')

site1 = exp.add_site(depth = 809, tetrodes = [1,2,3,4,5,6,7,8])
site1.add_session('15-35-17', None, 'noisebursts')
site1.add_session('15-40-36', 'a', 'tuningCurve')
site1.add_session('16-02-16', 'b', 'AM')
site1.add_session('16-50-01', 'c', 'bandwidth', paradigm='am_bandwidth')

site2 = exp.add_site(depth = 974, tetrodes = [1,2,3,4,5,6,7,8])
site2.add_session('17-06-19', 'd', 'tuningCurve')
site2.add_session('17-29-29', 'e', 'bandwidth', paradigm='am_bandwidth')


#What happens after the data is collected (how to cluster/plot reports and stuff)

from jaratest.nick.database import sitefuncs

site1TT = [sitefuncs.cluster_site(site1, 'site1', tt) for tt in site1.tetrodes]
oneTT = site1TT[0]

print oneTT.sessionList

print site1.get_mouse_relative_behav_filenames()
print site1.get_mouse_relative_ephys_filenames()

## cell database with pandas

import pandas
db = pandas.DataFrame()

for oneTT in site1TT:
    ttClusters = np.unique(oneTT.clusters)
    for indclus, clus in enumerate(ttClusters):
        clusDict = {'subject': oneTT.animalName,
                    'sessionList': site1.get_session_ephys_filenames(),
                    'sessionNames': site1.get_session_types(),
                    'behavFiles': site1.get_session_behav_filenames(),
                    'tetrode': oneTT.tetrode,
                    'cluster': clus}
        db = db.append(clusDict, ignore_index=True)

#Saving to csv is so easy
db.to_csv('/home/nick/src/jaratest/nick/database/database.csv')


#How to do a calculation and add columns to the database

from jaratest.nick.ephysExperiments import clusterManySessions_v2 as cms

isiless2 = []
for indcell, cell in db.iterrows():
    oneTT = cms.MultipleSessionsToCluster(cell['subject'], cell['sessionList'], int(cell['tetrode']), '{}_{}'.format('2016-07-13', 'site1'))
    oneTT.load_all_waveforms()
    oneTT.set_clusters_from_file()
    tsThisCluster = oneTT.timestamps[oneTT.clusters==cell['cluster']]
    isiThisCluster = np.diff(tsThisCluster)
    violations = isiThisCluster<0.002
    vioPercent = sum(violations)/double(len(violations))
    isiless2.append(100* vioPercent)



