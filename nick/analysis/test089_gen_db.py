import sys; sys.path.append('/home/jarauser/data')
import os
from inforecordings import test098_inforec as inforec
reload(inforec)
from jaratoolbox import loadopenephys
from jaratoolbox import settings
reload(settings)
from matplotlib import pyplot as plt
from jaratoolbox import spikesorting
from jaratoolbox import celldatabase
import numpy as np

tetrodes = range(1, 9)
sessions = inforec.test098.experiments[0].sites[0].sessions

celldb = celldatabase.NewCellDB()

for experiment in inforec.test098.experiments:
    for site in experiment.sites:
        for session in site.sessions:
            for tetrode in tetrodes:
                fullPath = session.full_ephys_path()
                fullFn = os.path.join(fullPath, 'Tetrode{}.spikes'.format(tetrode))
                #print fullFn
                fullBehav = session.full_behav_filename()
                #print fullBehav
                dataSpikes = loadopenephys.DataSpikes(fullFn)
                ephysSession='{}_{}'.format(session.date, session.timestamp)
                features=['peak', 'valleyFirstHalf']
                oneTT = spikesorting.TetrodeToCluster(session.subject, ephysSession, tetrode, features)


                oneTT.load_waveforms()
                clusterFile = os.path.join(oneTT.clustersDir,'Tetrode%d.clu.1'%oneTT.tetrode)
                if os.path.isfile(clusterFile):
                    oneTT.dataTT.clusters = np.fromfile(clusterFile,dtype='int32',sep=' ')[1:]
                else:
                    oneTT.create_fet_files()
                    oneTT.run_clustering()
                    oneTT.save_report()

                for cluster in np.unique(oneTT.dataTT.clusters):
                    clusterDict=vars(session)
                    clusterDict.update({'tetrode':tetrode, 'cluster':cluster})
                    celldb.db = celldb.db.append(clusterDict, ignore_index=True)

celldb.db.to_csv('/home/jarauser/src/jaratest/nick/analysis/test098_celldb.csv')



#from jaratest.nick.database import ephysinterface
#ei = ephysinterface.EphysInterface('test098', '2016-07-26', '', defaultParadigm='am_tuning_curve')
#
#sessions = ['12-38-47', '13-06-15', '13-11-17', '13-49-09', '14-00-26', '14-10-52', '14-22-31', '14-33-16', '13-42-42', '14-52-07']

#for session in sessions:
#   ei.plot_array_raster(session, replace=1, tetrodes=range(1, 9))
#   plt.waitforbuttonpress()



