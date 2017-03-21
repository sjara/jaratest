'''
Test corrupted behavior file.
'''

from jaratoolbox import loadbehavior

filev1 = '/data/behavior/test055/test055_2afc_20150313a.h5'
filev2 = '/data/old_behavior_santiago/test055/test055_2afc_20150313a.h5'
filev3 = '/mnt/jarahubdata/behavior/test055/test055_2afc_20150313a.h5'

bdata = loadbehavior.BehaviorData(filev3)
