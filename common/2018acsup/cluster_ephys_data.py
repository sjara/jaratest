'''
Takes as input a full path to an inforec, generates kk folder containing .clu files
'''

import pandas as pd
import numpy as np

from jaratoolbox import spikesorting

def cluster_spike_data(subjects):
    for subject in subjects:
        inforec = '/home/jarauser/src/jaratest/common/inforecordings/{0}_inforec.py'.format(subject)
        ci = spikesorting.ClusterInforec(inforec)
        ci.process_all_experiments()
        
def cluster_rescue(db, isiThreshold):
    modifiedDB = spikesorting.rescue_clusters(db, isiThreshold)
    return modifiedDB