"""
Prepare psychoometric data for John Conery.
"""

import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots

subject = 'adap013'
#session = '20160404a' # 0331
session = '20160331a'
paradigm = '2afc'

outputFile = '/tmp/{}_{}_behavior.npz'.format(subject,session)

behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
#behavFile = './adap012_2afc_20160219a.h5'
bdata = loadbehavior.BehaviorData(behavFile)

choice = bdata['choice']
choiceRight = (choice==bdata.labels['choice']['right'])
targetFrequency = bdata['targetFrequency']
valid = bdata['valid'] & (choice!=bdata.labels['choice']['none'])

np.savez(outputFile, choiceRight=choiceRight, validTrials=valid, targetFrequency=targetFrequency)
print('Saved data to {}'.format(outputFile))
