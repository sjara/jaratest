'''
Generate a figure for the correlation between a photostim site's best frequency and the behavioral bias resulting from photostim.
'''

import os
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)
import figparams
reload(figparams)

dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME)

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_photostim_tuning_vs_bias' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [6,6]

photostimMice = ['d1pi014','d1pi015','d1pi016']

# -- Load tuning data and behavioral bias data -- #
### FIX hardcoded path
tuningData = np.load(os.path.join(dataDir,'sound_freq_selectivity/summary_bilateral_best_freq.npz'))
biasData = np.load(os.path.join(dataDir,'photostim_2afc/summary_photostim_percent_right_choice_change.npz'))

tuningToPlot = []
biasToPlot = []
for mouse in photostimMice:
    for stimHemi in ['left','right']:
        if not np.all(tuningData['{}_{}_sessions'.format(mouse,stimHemi)]==biasData['{}{}HemiStimSessions'.format(mouse,stimHemi)]):
            print '{} {} hemi sessions for tuning and behavior do not match!'.format(mouse,stimHemi)
            continue
        validTuning = ~np.isnan(tuningData['{}_{}'.format(mouse,stimHemi)])
        tuningToPlot.extend(tuningData['{}_{}'.format(mouse,stimHemi)][validTuning])
        biasToPlot.extend(biasData['{}{}HemiStim'.format(mouse,stimHemi)][validTuning])

plt.figure()
plt.plot(tuningToPlot, biasToPlot, 'o')
plt.xlabel('log 2 distance between best freq and boundary')
plt.ylabel('change in percent rightward bias (stim - control)')
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
