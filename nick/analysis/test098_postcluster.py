import os
from jaratoolbox import settings
from jaratoolbox import loadopenephys
import pandas as pd
import numpy as np
SAMPLING_RATE=30000.0
db = pd.io.parsers.read_csv('/home/jarauser/src/jaratest/nick/analysis/test098_celldb.csv', header=0, index_col=0)

for indCell, cell in db.iterrows():
    ephysPath = os.path.join(settings.EPHYS_PATH,
                           cell['subject'],
                           '{}_{}'.format(cell['date'],cell['timestamp']))
    ephysFn = os.path.join(ephysPath,
                           'Tetrode{}.spikes'.format(int(cell['tetrode'])))
    clusterFn = os.path.join('{}_kk'.format(ephysPath),
                           'Tetrode{}.clu.1'.format(int(cell['tetrode'])))
                               
    print ephysFn
    print clusterFn
    dataSpikes = loadopenephys.DataSpikes(ephysFn)
    dataSpikes.set_clusters(clusterFn)
    #print np.unique(dataSpikes.clusters)
    #print int(cell['cluster'])
    dataSpikes.timestamps = dataSpikes.timestamps[dataSpikes.clusters==int(cell['cluster'])]
    #Make timestamps in seconds
    dataSpikes.timestamps = dataSpikes.timestamps/SAMPLING_RATE
    dataSpikes.samples = dataSpikes.samples[dataSpikes.clusters==int(cell['cluster'])]
    nSpikes=len(dataSpikes.timestamps)
    isi=np.diff(dataSpikes.timestamps)
    isiViolations = sum(isi<0.002)/np.double(len(isi))*100
    print isiViolations
    #Add the isi violations to the database
    db.loc[indCell,'isiViolation']=isiViolations
    #Add number of spikes to the database
    db.loc[indCell, 'nSpikes']=nSpikes

    
    

