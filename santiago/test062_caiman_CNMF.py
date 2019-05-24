'''
Testing CaImAn for analysis of two-photon data.
https://github.com/flatironinstitute/CaImAn

This script tests Constrained Nonnegative Matrix Factorization (CNMF)

NOTES and FIXES:

See example results in /data/exampleNeurolabware/stack/
- stack100_240x160_nomotion.tif (MotionCorrected)
'''

from __future__ import division
from __future__ import print_function
import os
import sys
import cv2
import glob
import time
from builtins import range
from skimage import io
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import extraplots
import caiman as cm
#from caiman.motion_correction import MotionCorrect
#from caiman.utils import visualization #plot_contours, view_patches_bar
#from caiman.source_extraction import cnmf.cnmf import cnmf as cnmf
#from caiman.motion_correction import MotionCorrect
#from caiman.source_extraction.cnmf.utilities import detrend_df_f
#from caiman.components_evaluation import estimate_components_quality_auto

import tifffile

#datafile = '/data/exampleNeurolabware/stacks/stack100_240x160.tif'
datafile = '/data/exampleNeurolabware/stacks/stack100_240x160_nomotion.tif'
bord_px_els = 6 #[4,4]
fr = 10#30                             # imaging rate in frames per second
decay_time = 0.4                    # length of a typical transient in seconds

# transients are 20 samples in Phil's data (at 10Hz)

RUN_CNMF = 0
PLOT_RESULTS = 1
#SAVE_TIFF = 0

cv2.setNumThreads(1)
# -- Start a cluster for parallel processing --
#c, dview, n_processes = cm.cluster.setup_cluster(
#    backend='local', n_processes=None, single_thread=False)
dview = None

# -- Parameters for source extraction and deconvolution --
p = 1                       # order of the autoregressive system
gnb = 2                     # number of global background components
merge_thresh = 0.8          # merging threshold, max correlation allowed
# half-size of the patches in pixels. e.g., if rf=25, patches are 50x50
rf = 20#15
stride_cnmf = 8#6             # amount of overlap between the patches in pixels
K = 2#4                       # number of components per patch
gSig = [4, 4]               # expected half size of neurons
# initialization method (if analyzing dendritic data using 'sparse_nmf')
init_method = 'greedy_roi'
is_dendrites = False        # flag for analyzing dendritic data
# sparsity penalty for dendritic data analysis through sparse NMF
alpha_snmf = None

# parameters for component evaluation
min_SNR = 0.8#2.5               # signal to noise ratio for accepting a component
rval_thr = 0.8              # space correlation threshold for accepting a component
cnn_thr = 0.8               # threshold for CNN based classifier

# -- Load the motion-corrected file --
fname_new = '/data/exampleNeurolabware/stacks/memmap__d1_160_d2_240_d3_1_order_C_frames_100_.mmap'
Yr, dims, T = cm.load_memmap(fname_new)
images = np.reshape(Yr.T, [T] + list(dims), order='F')
'''
# Loading like this gives the error:
# cnmf.fit() You need to provide a memory mapped file as input if you use patches!!
images = tifffile.imread(datafile) # This
'''

#%% RUN CNMF ON PATCHES

# First extract spatial and temporal components on patches and combine them
# for this step deconvolution is turned off (p=0)
t1 = time.time()

cnm = cm.source_extraction.cnmf.CNMF(n_processes=1, k=K,
                gSig=gSig, merge_thresh=merge_thresh,
                p=0, dview=dview, rf=rf, stride=stride_cnmf, memory_fact=1,
                method_init=init_method, alpha_snmf=alpha_snmf,
                only_init_patch=False, gnb=gnb, border_pix=bord_px_els)
cnm = cnm.fit(images)

Cn = cm.local_correlations(images.transpose(1, 2, 0))
Cn[np.isnan(Cn)] = 0

# -- Plot contours of found components --
if 0:#PLOT_RESULTS:
    plt.figure(1)
    plt.clf()
    crd = cm.utils.visualization.plot_contours(cnm.A, Cn, thr=0.9)
    plt.title('Contour plots of found components')
    plt.show()

#sys.exit()

#%% COMPONENT EVALUATION
# the components are evaluated in three ways:
#   a) the shape of each component must be correlated with the data
#   b) a minimum peak SNR is required over the length of a transient
#   c) each shape passes a CNN based classifier

idx_components, idx_components_bad, SNR_comp, r_values, cnn_preds = \
    cm.components_evaluation.estimate_components_quality_auto(images,
                                     cnm.A, cnm.C, cnm.b, cnm.f,
                                     cnm.YrA, fr, decay_time, gSig, dims,
                                     dview=dview, min_SNR=min_SNR,
                                     r_values_min=rval_thr, use_cnn=False,
                                     thresh_cnn_min=cnn_thr)

#%% PLOT COMPONENTS
if PLOT_RESULTS:
    plt.figure(2)
    plt.clf()
    plt.subplot(121)
    crd_good = cm.utils.visualization.plot_contours(
        cnm.A[:, idx_components], Cn, thr=.8, vmax=0.75)
    plt.title('Contour plots of accepted components')
    plt.subplot(122)
    crd_bad = cm.utils.visualization.plot_contours(
        cnm.A[:, idx_components_bad], Cn, thr=.8, vmax=0.75)
    plt.title('Contour plots of rejected components')
    plt.show()


#%% VIEW TRACES (accepted and rejected)
if PLOT_RESULTS:
    cm.utils.visualization.view_patches_bar(Yr,
                     cnm.A.tocsc()[:, idx_components], cnm.C[idx_components],
                     cnm.b, cnm.f, dims[0], dims[1], YrA=cnm.YrA[idx_components],
                     img=Cn)
    '''
    cm.utils.visualization.view_patches_bar(Yr,
                     cnm.A.tocsc()[:, idx_components_bad], cnm.C[idx_components_bad],
                     cnm.b, cnm.f, dims[0], dims[1], YrA=cnm.YrA[idx_components_bad],
                     img=Cn)
    '''
    plt.show()


sys.exit()





#%% RE-RUN seeded CNMF on accepted patches to refine and perform deconvolution
A_in, C_in, b_in, f_in = cnm.A[:,idx_components], cnm.C[idx_components], cnm.b, cnm.f
cnm2 = cm.source_extraction.cnmf.CNMF(n_processes=1, k=A_in.shape[-1],
                 gSig=gSig, p=p, dview=dview,
                 merge_thresh=merge_thresh, Ain=A_in, Cin=C_in, b_in=b_in,
                 f_in=f_in, rf=None, stride=None, gnb=gnb,
                 method_deconvolution='oasis', check_nan=True)

cnm2 = cnm2.fit(images)


sys.exit()
#%% Extract DF/F values

F_dff = cm.source_extraction.cnmf.utilities.detrend_df_f(cnm2.A, cnm2.b, cnm2.C,
                     cnm2.f, YrA=cnm2.YrA,
                     quantileMin=8, frames_window=50)
# NOTE: Previous valus was: frames_window=250


#%% Show final traces
if 0:#PLOT_RESULTS:
    cnm2.view_patches(Yr, dims=dims, img=Cn)

'''
#%% STOP CLUSTER and clean up log files
cm.stop_server(dview=dview)
log_files = glob.glob('*_LOG_*')
for log_file in log_files:
    os.remove(log_file)
'''

#%% reconstruct denoised movie
denoised = cm.movie(cnm2.A.dot(cnm2.C) +
                    cnm2.b.dot(cnm2.f)).reshape(dims + (-1,), order='F').transpose([2, 0, 1])

#%% play along side original data
moviehandle = cm.concatenate([m_els.resize(1, 1, downsample_ratio),
              denoised.resize(1, 1, downsample_ratio)],
              axis=2)

if PLOT_RESULTS:
    moviehandle.play(fr=60, gain=15, magnification=2, offset=0)  # press q to exit

