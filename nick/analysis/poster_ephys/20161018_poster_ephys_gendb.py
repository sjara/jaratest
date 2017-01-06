import os
import sys
import importlib
from jaratest.nick.utils import clusterutils
import pandas
import numpy as np


def tracefunc(frame, event, arg, indent=[0]):
      if event == "call":
          indent[0] += 2
          print "-" * indent[0] + "> call function", frame.f_code.co_name
      elif event == "return":
          print "<" + "-" * indent[0], "exit function", frame.f_code.co_name
          indent[0] -= 2
      return tracefunc

import sys

# sys.settrace(tracefunc)




cortexDir = '/home/nick/src/jaratest/nick/inforecordings/cortex'
thalamusDir = '/home/nick/src/jaratest/nick/inforecordings/thalamus'
sys.path.append(cortexDir)
sys.path.append(thalamusDir)

cortexInforecs = [fn for fn in os.listdir(cortexDir) if ( os.path.splitext(fn)[1] == '.py' ) & ( fn != '__init__.py')]

thalamusInforecs = [fn for fn in os.listdir(thalamusDir) if ( os.path.splitext(fn)[1] == '.py' ) & ( fn != '__init__.py')]

# #debug
# cortexInforecs = [cortexInforecs[0]]

# cortexDB = pandas.DataFrame()

# for inforecFile in cortexInforecs:

#     modName = os.path.splitext(inforecFile)[0]
#     inforec = importlib.import_module(modName)

#     for experiment in inforec.experiments:
#         for site in experiment.sites:
#             for tetrode in site.tetrodes:
#                 clusteringID = '{}_{}_{}um_T{}'.format(inforec.subject,
#                                        experiment.date,
#                                        site.depth,
#                                        tetrode)
#                 oneTT = clusterutils.cluster_many_sessions(site.subject,
#                                                            site.session_ephys_dirs(),
#                                                            tetrode,
#                                                            clusteringID,
#                                                            saveSingleSessionCluFiles=True)

#                 for cluster in np.unique(oneTT.clusters):
#                     clusterDict = {'tetrode':tetrode,
#                                    'cluster':cluster}
#                     clusterDict.update(site.cluster_info())

#                     clusterTimestamps = oneTT.timestamps[oneTT.clusters==cluster]

#                     nspikes = len(clusterTimestamps)
#                     isi = np.diff(clusterTimestamps)
#                     isiViolations = sum(isi<0.002)/np.double(len(isi))*100

#                     clusterDict.update({'nspikes':nspikes,
#                                         'isiViolations':isiViolations})

#                     cortexDB = cortexDB.append(clusterDict, ignore_index=True)
# cortexDB.to_pickle('/home/nick/src/jaratest/nick/analysis/poster_ephys/cortexdb.pickle')


thalamusDB = pandas.DataFrame()

for inforecFile in thalamusInforecs:

    modName = os.path.splitext(inforecFile)[0]
    inforec = importlib.import_module(modName)

    for experiment in inforec.experiments:
        for site in experiment.sites:
            for tetrode in site.tetrodes:
                clusteringID = '{}_{}_{}um_T{}'.format(inforec.subject,
                                       experiment.date,
                                       site.depth,
                                       tetrode)
                oneTT = clusterutils.cluster_many_sessions(site.subject,
                                                           site.session_ephys_dirs(),
                                                           tetrode,
                                                           clusteringID,
                                                           saveSingleSessionCluFiles=True)

                for cluster in np.unique(oneTT.clusters):
                    clusterDict = {'tetrode':tetrode,
                                   'cluster':cluster}
                    clusterDict.update(site.cluster_info())

                    clusterTimestamps = oneTT.timestamps[oneTT.clusters==cluster]

                    nspikes = len(clusterTimestamps)
                    isi = np.diff(clusterTimestamps)
                    isiViolations = sum(isi<0.002)/np.double(len(isi))*100

                    clusterDict.update({'nspikes':nspikes,
                                        'isiViolations':isiViolations})

                    thalamusDB = thalamusDB.append(clusterDict, ignore_index=True)

thalamusDB.to_pickle('/home/nick/src/jaratest/nick/analysis/poster_ephys/thalamusdb.pickle')
