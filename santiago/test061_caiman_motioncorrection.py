'''
Testing CaImAn for analysis of two-photon data.
https://github.com/flatironinstitute/CaImAn

This script tests Motion Correction.

NOTES and FIXES:
- caiman/motion_correction.py requires a change:
  Make sure you use tifffile.imread() in lines 2337, 2339
- Note that script may fail if splits_* parameters are too large,
  because caiman does not test if resulting sequence is just one image
  and iterating to one image (as opposed to a 3D array) gives error.

See example results in /data/exampleNeurolabware/stack/
- stack100_240x160.tif  (Original)
- stack100_240x160_nomotion.tif (MotionCorrected)
'''

from __future__ import division
from __future__ import print_function
import os
import sys
import cv2
import glob
from builtins import range
from skimage import io
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import extraplots
import caiman as cm
from caiman.motion_correction import MotionCorrect
import tifffile

#datafile = '/data/exampleCaImAn/demoMovie.tif'
#datafile = '/data/exampleNeurolabware/tiffTiny/image240x160__Z62.ome.tif'
datafile = '/data/exampleNeurolabware/stacks/stack100_240x160.tif'

RUN_MOTION_CORRECTION = 1
SHOW_MOVIE = 0
SAVE_TIFF = 0

cv2.setNumThreads(1)

# -- Start a cluster for parallel processing --
#c, dview, n_processes = cm.cluster.setup_cluster(
#    backend='local', n_processes=None, single_thread=False)
dview = None

# -- Motion correction parameters --
niter_rig = 1               # number of iterations for rigid motion correction
max_shifts = (6, 6)         # maximum allow rigid shift
# for parallelization split the movies in num_splits chuncks across time
splits_rig = 20#56
# start a new patch for pw-rigid motion correction every x pixels
strides = (48, 48)
# overlap between pathes (size of patch strides+overlaps)
overlaps = (24, 24)
# for parallelization split the movies in  num_splits chuncks across time
splits_els = 20#56
upsample_factor_grid = 4    # upsample factor to avoid smearing when merging patches
# maximum deviation allowed for patch with respect to rigid shifts
max_deviation_rigid = 3

moviehandle = cm.load(datafile)
#moviehandle.play(gain=1, fr=30, magnification=8)


if RUN_MOTION_CORRECTION:
    # This will be subtracted from the movie to make it non-negative
    min_mov = cm.load(datafile, subindices=range(200)).min()

    # Note that the file is not loaded in memory
    mc = MotionCorrect(datafile, min_mov,
                       dview=dview, max_shifts=max_shifts, niter_rig=niter_rig,
                       splits_rig=splits_rig,
                       strides=strides, overlaps=overlaps, splits_els=splits_els,
                       upsample_factor_grid=upsample_factor_grid,
                       max_deviation_rigid=max_deviation_rigid,
                       shifts_opencv=True, nonneg_movie=True)

    #%% Run piecewise-rigid motion correction using NoRMCorre
    mc.motion_correct_pwrigid(save_movie=True)

    m_els = cm.load(mc.fname_tot_els)
    bord_px_els = np.ceil(np.maximum(np.max(np.abs(mc.x_shifts_els)),
                                     np.max(np.abs(mc.y_shifts_els)))).astype(np.int)


    # -- Memory map the file in 'C' order --
    fname = mc.fname_tot_els   # name of the pw-rigidly corrected file.
    fname_new = cm.save_memmap(fname, base_name='memmap_', order='C',
                               border_to_0=bord_px_els)  # exclude borders

    moviehandle = cm.load(datafile)
    # now load the file
    #%% compare with original movie
    if SHOW_MOVIE:
        cm.concatenate([moviehandle, m_els], axis=2).play(fr=60, gain=3, magnification=3, offset=0)

if SAVE_TIFF:
    memmapFilename ='/data/exampleNeurolabware/stacks/stack100_240x160_els__d1_160_d2_240_d3_1_order_F_frames_100_.mmap'
    # '/data/exampleNeurolabware/stacks/memmap__d1_160_d2_240_d3_1_order_C_frames_100_.mmap'
    Yr, dims, T = cm.load_memmap(memmapFilename)
    images = np.reshape(Yr.T, [T] + list(dims), order='F')
    tifffile.imsave('/data/exampleNeurolabware/stacks/stack100_240x160_nomotion.tif',images)


#    sys.exit()

'''
downsample_ratio = 0.2
offset_mov = -np.min(m_orig[:100])
moviehandle = m_orig.resize(1, 1, downsample_ratio)
if display_images:
    moviehandle.play(gain=10, offset=offset_mov, fr=30, magnification=2)
'''