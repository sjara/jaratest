#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 15:16:19 2022

@author: jarauser
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import facemapanalysis as fmap

fileloc = '/data/videos/feat007/Exports_24-05-22/'
filename = 'feat007_am_tuning_curve_20220318_02_proc.npy'
proc_data = fmap.load_data(os.path.join(fileloc, filename), runchecks=False)
#threshold_sync = 15913.00
#threshold_blink = 14534.57
#threshold_groom = 52549.85
# Video: 'feat007_am_tuning_curve_20220318_02'
#threshold_sync = 13879.50
#threshold_blink = 28102.77
#threshold_groom = 26326.03
# Video: 'feat007_am_tuning_curve_20220321_02'
threshold_sync = 26980.00
threshold_blink = 30724.95
threshold_groom = 116017.90


pupil_trace = fmap.extract_pupil(proc_data)
whisking, whisking_raw = fmap.extract_whisking(proc_data)
running, running_raw = fmap.extract_running(proc_data)
sync_bool, sync_timings, sync_raw, threshold_sync = fmap.extract_sync(proc_data, threshold = threshold_sync)
blink_bool, blink_trace, threshold_blink = fmap.extract_blink(proc_data, threshold = threshold_blink)
groom_bool, groom_trace, threshold_groom = fmap.extract_groom(proc_data, threshold = threshold_groom)

    plt.figure()
    ax1 = plt.subplot(4,1,1)
    plt.plot(blink_trace, color='0.7', label='Raw Blink Trace')
    plt.xlabel('Frame')
    plt.ylabel("Area of visible eye [pixels]")
    plt.title('Blinking',fontweight="bold")
    plt.xlim((0,len(blink_trace)))
    plt.ylim((0,np.max(blink_trace)*1.05))
    plt.axhline(y=threshold_blink, color='r', linestyle='-', label='threshold')
    plt.legend(loc="lower right")
    ax2 = plt.subplot(4,1,2, sharex=ax1)
    plt.plot(pupil_trace)
    plt.title('Pupil',fontweight="bold")
    plt.ylabel("Pupil Area [pixels]")
    ax3 = plt.subplot(4,1,3, sharex=ax1)
    plt.plot(groom_trace)
    plt.axhline(y=threshold_groom, color='r', linestyle='-', label='threshold')
    plt.title('Groom',fontweight="bold")
    plt.ylabel("Grooming Roi [non-white pixels]")
    plt.ylim((0,np.max(groom_trace)*1.05))
    ax4 = plt.subplot(4,1,4, sharex=ax1)
    plt.plot(blink_bool, label = 'Blink')
    plt.plot(groom_bool, label = 'Groom')
    plt.ylabel("Boolean")
    plt.legend(loc="lower right")
    plt.title('Blink and Grooming Boolean',fontweight="bold")

plt.tight_layout(pad=1.75)

#outputs = {'filename' : filename, 'threshold_sync' : threshold_sync, 'threshold_blink' : threshold_blink, 'threshold_groom' : threshold_groom}
#saveloc = '/data/videos/feat007/Exports_24-05-22/test'
#savename = filename.replace('_proc.npy','_thresholds.npz')
#np.savez(os.path.join(saveloc, savename), **outputs)
#
#data_test = np.load(os.path.join(saveloc, savename))
#data_test.files