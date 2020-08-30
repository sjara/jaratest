# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 10:38:08 2020

@author: devin
"""


from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
import numpy as np
from matplotlib import pyplot as plt

subject = 'adap021'
session = '20160524a'
#subject = 'adap013'
#session = '20160331a'
paradigm = '2afc'
behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
bdata = loadbehavior.BehaviorData(behavFile)

choiceRight = bdata['choice'] == bdata.labels['choice']['right']
targetFrequency = bdata['targetFrequency']
valid = bdata['valid']

(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = \
    behavioranalysis.calculate_psychometric(choiceRight,targetFrequency,valid)
