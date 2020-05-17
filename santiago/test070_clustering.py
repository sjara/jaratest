'''
Testing tools for clustering (ClusterInforec).
'''

import os
from jaratoolbox import spikesorting
from jaratoolbox import settings

subject = 'test000'
inforecFile = os.path.join(settings.INFOREC_PATH,'{}_inforec.py'.format(subject))
clusteringObj = spikesorting.ClusterInforec(inforecFile)

clusteringObj.process_all_experiments()

# NOTE: we should also have a way to remove FET files
