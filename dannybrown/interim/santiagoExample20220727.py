#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 15:09:06 2022

@author: jarauser
"""
import numpy as np
import matplotlib.pyplot as plt
#from scipy import stats
#from jaratoolbox import loadbehavior
#from jaratoolbox import settings
import os
import sys

nFreq = 6
data = np.random.rand(nFreq,10)
freqs = np.linspace(4000, 15000, nFreq)
nTrials = np.random.randint(1,6,nFreq)

#average
dataMean = np.mean(data, axis=1)
print(dataMean)
#plot
plt.plot(data.T)
plt.show()
#legend
legendLabels = []
for f_ind, freq in enumerate(freqs):
    iteration = f'{freq} Hz, nTrials = {nTrials[f_ind]}'
    legendLabels.append(iteration)
    
print(legendLabels)
    
plt.legend(legendLabels)