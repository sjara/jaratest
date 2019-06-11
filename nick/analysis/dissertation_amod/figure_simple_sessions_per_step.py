import numpy as np
from jaratoolbox import extraplots
from matplotlib import pyplot as plt

'''
Behavior steps:
0: Sides direct AM
1: Direct AM
2: Next correct AM
3: If correct AM
4: AM psychometric
5: If correct Tones
6: Tones psychometric
7: If correct Mixed tones
8: Mixed tones psychometric
9: Ready for experiment
'''

#Get the data
dataFn = '/home/nick/data/dissertation_amod/sessions_per_step.npz'
dataZ = np.load(dataFn)

subjects = dataZ['subjects']
stepArrays = dataZ['stepArrays']
trialNumArrays = dataZ['trialNumArrays']
performanceArrays = dataZ['performanceArrays']


