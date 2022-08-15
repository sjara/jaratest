#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code to load and visualize pupil size

Created on Mon Mar 21 11:53:29 2022

@author: dannybrown
"""

## Import data
import numpy as np
import matplotlib.pyplot as plt
proc = np.load('/data/videos/feat007/feat007_am_tuning_curve_20220311_01_proc.npy', allow_pickle=True).item()
pupil = proc['pupil'][0]  # A dict inside a 1-item list, so you need to get the first element
pArea = pupil['area']

## Plot the pupil area
plt.plot(pArea)
plt.xlabel('Frame')
plt.ylabel('Pupil Size [A.U.]')