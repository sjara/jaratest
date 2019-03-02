'''
Takes as input a full path to an inforec, generates kk folder containing .clu files
'''

import pandas as pd
import numpy as np

from jaratoolbox import spikesorting

subject = 'band004'
inforec = '/home/jarauser/src/jaratest/common/inforecordings/{0}_inforec.py'.format(subject)
ci = spikesorting.ClusterInforec(inforec)
ci.process_all_experiments()